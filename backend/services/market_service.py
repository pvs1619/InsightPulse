import os
import math
import logging
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional
import yfinance as yf

from services.ticker_resolver import ticker_resolver
from utils.serializer import sanitize_json_value

logger = logging.getLogger("market_service")

PERIOD_MAP = {
    "1m": "1mo",
    "1mo": "1mo",
    "3m": "3mo",
    "3mo": "3mo",
    "6m": "6mo",
    "6mo": "6mo",
    "1y": "1y",
    "5y": "5y"
}

class MarketDataService:
    """
    Dynamic Market Data Service retrieving live historical OHLCV data
    via yfinance with fallback to offline CSV datasets when appropriate.
    Ensures 100% JSON-compliant values without NaN / Inf leaking.
    """

    def __init__(self, offline_dir: str = "data/market_data"):
        self.offline_dir = offline_dir

    def _process_dataframe(self, df: pd.DataFrame, ticker: str, company_name: str, currency: str, data_source: str) -> Dict[str, Any]:
        df = df.copy()
        df.columns = [c.lower() for c in df.columns]

        if "close" not in df.columns:
            raise ValueError(f"Close price column missing from dataset for {ticker}.")

        # Ensure date format
        if "date" not in df.columns:
            df["date"] = df.index

        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        # Drop rows with invalid date or NaN/non-positive close
        df = df[df["date"].notna() & df["close"].notna() & (df["close"] > 0)].copy()

        if len(df) == 0:
            raise ValueError(f"No valid trading observations available for {ticker}.")

        df = df.sort_values("date").reset_index(drop=True)

        # Fill open, high, low if missing with close
        if "open" in df.columns:
            df["open"] = df["open"].fillna(df["close"])
        else:
            df["open"] = df["close"]

        if "high" in df.columns:
            df["high"] = df["high"].fillna(df["close"])
        else:
            df["high"] = df["close"]

        if "low" in df.columns:
            df["low"] = df["low"].fillna(df["close"])
        else:
            df["low"] = df["close"]

        if "volume" in df.columns:
            df["volume"] = pd.to_numeric(df["volume"], errors="coerce").fillna(0)
        else:
            df["volume"] = 0

        # Technical Indicators
        df["sma_20"] = df["close"].rolling(window=20, min_periods=3).mean()
        df["sma_50"] = df["close"].rolling(window=50, min_periods=5).mean()
        df["daily_return"] = df["close"].pct_change().fillna(0.0)

        # Volatility: annualized standard deviation of daily returns
        daily_std = df["daily_return"].std()
        annualized_volatility = round(float(daily_std * math.sqrt(252) * 100), 2) if (not np.isnan(daily_std) and not math.isinf(daily_std)) else 0.0

        latest = df.iloc[-1]
        prev = df.iloc[-2] if len(df) > 1 else latest

        curr_close = round(float(latest["close"]), 2)
        prev_close = round(float(prev["close"]), 2)
        price_change = round(curr_close - prev_close, 2)
        pct_change = round(((curr_close - prev_close) / prev_close) * 100, 2) if prev_close != 0 else 0.0

        day_high = round(float(latest["high"]), 2)
        day_low = round(float(latest["low"]), 2)
        day_open = round(float(latest["open"]), 2)
        volume = int(latest["volume"]) if not math.isnan(float(latest["volume"])) else 0

        # 52-week range
        high_tail = df["high"].tail(252).dropna()
        high_52w = round(float(high_tail.max()), 2) if not high_tail.empty else curr_close
        low_tail = df["low"].tail(252).dropna()
        low_52w = round(float(low_tail.min()), 2) if not low_tail.empty else curr_close

        vol_tail = df["volume"].tail(30).dropna()
        avg_vol_mean = float(vol_tail.mean()) if not vol_tail.empty else volume
        avg_volume = int(avg_vol_mean) if not math.isnan(avg_vol_mean) else volume

        # Format history points for chart
        history_points = []
        for _, row in df.iterrows():
            sma20_val = row["sma_20"]
            sma50_val = row["sma_50"]
            history_points.append({
                "date": row["date"].strftime("%Y-%m-%d"),
                "open": round(float(row["open"]), 2),
                "high": round(float(row["high"]), 2),
                "low": round(float(row["low"]), 2),
                "close": round(float(row["close"]), 2),
                "volume": int(row["volume"]) if not math.isnan(float(row["volume"])) else 0,
                "sma20": round(float(sma20_val), 2) if (not pd.isna(sma20_val) and not math.isinf(float(sma20_val))) else None,
                "sma50": round(float(sma50_val), 2) if (not pd.isna(sma50_val) and not math.isinf(float(sma50_val))) else None
            })

        result = {
            "company": company_name,
            "ticker": ticker,
            "currency": currency,
            "data_source": data_source,
            "summary": {
                "latest_close": curr_close,
                "previous_close": prev_close,
                "change": price_change,
                "percent_change": pct_change,
                "day_high": day_high,
                "day_low": day_low,
                "day_open": day_open,
                "volume": volume,
                "average_volume_30d": avg_volume,
                "volatility_annualized": annualized_volatility,
                "high_52w": high_52w,
                "low_52w": low_52w,
                "as_of_date": latest["date"].strftime("%Y-%m-%d")
            },
            "history": history_points
        }

        return sanitize_json_value(result)

    def get_market_analysis(self, query: str, period: str = "1y") -> Dict[str, Any]:
        resolved = ticker_resolver.resolve(query)
        ticker = resolved["ticker"]
        company_name = resolved["company"]
        currency = resolved["currency"]

        safe_period = PERIOD_MAP.get(period.lower(), "1y")

        # 1. Attempt live data retrieval via yfinance
        try:
            yf_ticker = yf.Ticker(ticker)
            hist = yf_ticker.history(period=safe_period)
            if hist is not None and not hist.empty:
                # Filter out any tail row that has NaN for Close
                hist_clean = hist[hist["Close"].notna() & (hist["Close"] > 0)]
                if len(hist_clean) >= 3:
                    if hasattr(yf_ticker, "info") and isinstance(yf_ticker.info, dict):
                        live_name = yf_ticker.info.get("shortName") or yf_ticker.info.get("longName")
                        if live_name:
                            company_name = live_name
                    return self._process_dataframe(hist_clean, ticker, company_name, currency, "Live Market Data")
        except Exception as e:
            logger.warning(f"Live market data fetch failed for '{ticker}': {e}")

        # 2. Check offline demo dataset
        clean_symbol = ticker.split(".")[0].upper() # e.g. NVDA, TSLA, AAPL, TCS
        offline_file = os.path.join(self.offline_dir, f"{clean_symbol}.csv")
        if os.path.exists(offline_file):
            try:
                df = pd.read_csv(offline_file)
                return self._process_dataframe(df, ticker, company_name, currency, "Offline Demo Dataset")
            except Exception as e:
                logger.error(f"Error reading offline market data for '{clean_symbol}': {e}")

        # 3. Neither live nor offline data could be retrieved
        raise ValueError(f"Market data could not be retrieved for '{query}' ({ticker}) at the moment. Please verify the company name or ticker and try again.")

market_service = MarketDataService()
