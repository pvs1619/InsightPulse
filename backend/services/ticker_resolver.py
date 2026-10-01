import re
import requests
from typing import Optional, Dict, Any

POPULAR_COMPANIES = {
    "nvidia": {"ticker": "NVDA", "name": "NVIDIA Corporation", "currency": "$"},
    "nvda": {"ticker": "NVDA", "name": "NVIDIA Corporation", "currency": "$"},
    "tesla": {"ticker": "TSLA", "name": "Tesla, Inc.", "currency": "$"},
    "tsla": {"ticker": "TSLA", "name": "Tesla, Inc.", "currency": "$"},
    "apple": {"ticker": "AAPL", "name": "Apple Inc.", "currency": "$"},
    "aapl": {"ticker": "AAPL", "name": "Apple Inc.", "currency": "$"},
    "microsoft": {"ticker": "MSFT", "name": "Microsoft Corporation", "currency": "$"},
    "msft": {"ticker": "MSFT", "name": "Microsoft Corporation", "currency": "$"},
    "amazon": {"ticker": "AMZN", "name": "Amazon.com, Inc.", "currency": "$"},
    "amzn": {"ticker": "AMZN", "name": "Amazon.com, Inc.", "currency": "$"},
    "google": {"ticker": "GOOGL", "name": "Alphabet Inc.", "currency": "$"},
    "alphabet": {"ticker": "GOOGL", "name": "Alphabet Inc.", "currency": "$"},
    "googl": {"ticker": "GOOGL", "name": "Alphabet Inc.", "currency": "$"},
    "goog": {"ticker": "GOOG", "name": "Alphabet Inc.", "currency": "$"},
    "meta": {"ticker": "META", "name": "Meta Platforms, Inc.", "currency": "$"},
    "facebook": {"ticker": "META", "name": "Meta Platforms, Inc.", "currency": "$"},
    "netflix": {"ticker": "NFLX", "name": "Netflix, Inc.", "currency": "$"},
    "nflx": {"ticker": "NFLX", "name": "Netflix, Inc.", "currency": "$"},
    "reliance": {"ticker": "RELIANCE.NS", "name": "Reliance Industries Limited", "currency": "₹"},
    "reliance industries": {"ticker": "RELIANCE.NS", "name": "Reliance Industries Limited", "currency": "₹"},
    "ril": {"ticker": "RELIANCE.NS", "name": "Reliance Industries Limited", "currency": "₹"},
    "tcs": {"ticker": "TCS.NS", "name": "Tata Consultancy Services Limited", "currency": "₹"},
    "tata consultancy services": {"ticker": "TCS.NS", "name": "Tata Consultancy Services Limited", "currency": "₹"},
    "infosys": {"ticker": "INFY", "name": "Infosys Limited", "currency": "$"},
    "infy": {"ticker": "INFY", "name": "Infosys Limited", "currency": "$"},
    "jpmorgan": {"ticker": "JPM", "name": "JPMorgan Chase & Co.", "currency": "$"},
    "jpmorgan chase": {"ticker": "JPM", "name": "JPMorgan Chase & Co.", "currency": "$"},
    "jpm": {"ticker": "JPM", "name": "JPMorgan Chase & Co.", "currency": "$"},
    "amd": {"ticker": "AMD", "name": "Advanced Micro Devices, Inc.", "currency": "$"},
    "intel": {"ticker": "INTC", "name": "Intel Corporation", "currency": "$"},
    "intc": {"ticker": "INTC", "name": "Intel Corporation", "currency": "$"},
    "tsmc": {"ticker": "TSM", "name": "Taiwan Semiconductor Manufacturing Company", "currency": "$"},
    "tsm": {"ticker": "TSM", "name": "Taiwan Semiconductor Manufacturing Company", "currency": "$"},
    "spotify": {"ticker": "SPOT", "name": "Spotify Technology S.A.", "currency": "$"},
    "spot": {"ticker": "SPOT", "name": "Spotify Technology S.A.", "currency": "$"},
    "uber": {"ticker": "UBER", "name": "Uber Technologies, Inc.", "currency": "$"},
    "disney": {"ticker": "DIS", "name": "The Walt Disney Company", "currency": "$"},
    "walmart": {"ticker": "WMT", "name": "Walmart Inc.", "currency": "$"}
}

class TickerResolver:
    """
    Resolves arbitrary company names or ticker queries to validated
    ticker symbols and corporate profiles.
    """

    @staticmethod
    def resolve(query: str) -> Dict[str, Any]:
        if not query or not query.strip():
            raise ValueError("Company or ticker name cannot be empty.")

        q_clean = query.strip()
        q_lower = q_clean.lower()

        # 1. Direct dictionary match
        if q_lower in POPULAR_COMPANIES:
            info = POPULAR_COMPANIES[q_lower]
            return {
                "ticker": info["ticker"],
                "company": info["name"],
                "currency": info["currency"],
                "resolved_from": "known_directory"
            }

        # 2. Check if the query is already an explicit ticker pattern (e.g. AAPL, TSLA, TCS.NS, RELIANCE.NS)
        ticker_pattern = re.compile(r'^[A-Z0-9\.\-\^]{1,10}$', re.IGNORECASE)
        is_direct_ticker = bool(ticker_pattern.match(q_clean)) and (q_clean.isupper() or len(q_clean) <= 5 or "." in q_clean)

        ticker_candidate = q_clean.upper() if is_direct_ticker else None

        # 3. Dynamic lookup via Yahoo Finance search API
        try:
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
            url = f"https://query2.finance.yahoo.com/v1/finance/search?q={requests.utils.quote(q_clean)}&quotesCount=3"
            resp = requests.get(url, headers=headers, timeout=4)
            if resp.status_code == 200:
                quotes = resp.json().get("quotes", [])
                for q in quotes:
                    sym = q.get("symbol")
                    if sym and ("EQUITY" in q.get("quoteType", "") or "ETF" in q.get("quoteType", "") or not q.get("quoteType")):
                        name = q.get("shortname") or q.get("longname") or q_clean.title()
                        curr = "₹" if sym.endswith(".NS") or sym.endswith(".BO") else "$"
                        return {
                            "ticker": sym,
                            "company": name,
                            "currency": curr,
                            "resolved_from": "live_directory"
                        }
        except Exception:
            # Fall back to candidate if search network fails
            pass

        if is_direct_ticker:
            curr = "₹" if ticker_candidate.endswith(".NS") or ticker_candidate.endswith(".BO") else "$"
            return {
                "ticker": ticker_candidate,
                "company": ticker_candidate,
                "currency": curr,
                "resolved_from": "direct_symbol"
            }

        raise ValueError(f"We couldn't identify a supported market ticker for '{query}'. Try entering the company's stock ticker instead (e.g., NVDA, AAPL, TCS.NS).")

ticker_resolver = TickerResolver()
