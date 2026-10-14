import os
import re
import datetime
import logging
import requests
import xml.etree.ElementTree as ET
from typing import List, Dict, Any, Tuple
import pandas as pd

from utils.paths import get_financial_news_path

logger = logging.getLogger("news_service")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

class NewsRetrievalService:
    """
    Multi-tiered production financial news retrieval engine:
    1. Server-side API key integrations (Finnhub, Marketaux, NewsAPI) if configured in environment
    2. Real-time Yahoo Finance Search API news stream
    3. Google News RSS financial search feed (global & domestic equities)
    4. Verified offline dataset fallback (financial_news.csv)
    5. Clean zero-fabrication unavailable state
    """

    def __init__(self, timeout: int = 5):
        self.timeout = timeout

    def _fetch_from_finnhub(self, ticker: str) -> List[Dict[str, Any]]:
        api_key = os.getenv("FINNHUB_API_KEY")
        if not api_key:
            return []

        try:
            today = datetime.date.today()
            from_date = (today - datetime.timedelta(days=7)).strftime("%Y-%m-%d")
            to_date = today.strftime("%Y-%m-%d")
            clean_sym = ticker.split(".")[0].upper()
            url = f"https://finnhub.io/api/v1/company-news?symbol={clean_sym}&from={from_date}&to={to_date}&token={api_key}"
            resp = requests.get(url, timeout=self.timeout)
            if resp.status_code == 200:
                data = resp.json()
                articles = []
                for idx, item in enumerate(data[:10]):
                    headline = (item.get("headline") or "").strip()
                    if not headline:
                        continue
                    dt_epoch = item.get("datetime")
                    date_str = datetime.datetime.fromtimestamp(dt_epoch).strftime("%Y-%m-%d") if dt_epoch else "Recent"
                    articles.append({
                        "article_id": f"fh_{idx + 1}",
                        "headline": headline,
                        "text": item.get("summary") or headline,
                        "date": date_str,
                        "source": item.get("source") or "Finnhub",
                        "url": item.get("url") or ""
                    })
                return articles
        except Exception as e:
            logger.warning(f"Finnhub news retrieval error for {ticker}: {e}")
        return []

    def _fetch_from_yahoo_search(self, ticker: str, company_name: str) -> List[Dict[str, Any]]:
        # Try ticker first, then company name if needed
        search_terms = [ticker]
        if company_name and company_name.lower() != ticker.lower():
            clean_co = re.sub(r'\b(Limited|Inc|Corp|Corporation|Ltd|LLC|PLC)\b', '', company_name, flags=re.IGNORECASE).strip()
            if clean_co and clean_co != ticker:
                search_terms.append(clean_co)

        for term in search_terms:
            try:
                url = f"https://query2.finance.yahoo.com/v1/finance/search?q={requests.utils.quote(term)}&newsCount=10"
                resp = requests.get(url, headers=HEADERS, timeout=self.timeout)
                if resp.status_code == 200:
                    items = resp.json().get("news", [])
                    articles = []
                    for idx, item in enumerate(items[:10]):
                        title = (item.get("title") or "").strip()
                        if not title:
                            continue
                        pub_time = item.get("providerPublishTime")
                        date_str = datetime.datetime.fromtimestamp(pub_time).strftime("%Y-%m-%d") if pub_time else "Recent"
                        articles.append({
                            "article_id": f"yf_{idx + 1}",
                            "headline": title,
                            "text": title,
                            "date": date_str,
                            "source": item.get("publisher") or "Yahoo Finance",
                            "url": item.get("link") or ""
                        })
                    if articles:
                        return articles
            except Exception as e:
                logger.warning(f"Yahoo search news error for {term}: {e}")
        return []

    def _fetch_from_google_rss(self, ticker: str, company_name: str) -> List[Dict[str, Any]]:
        try:
            clean_name = re.sub(r'\b(Limited|Inc|Corp|Corporation|Ltd|LLC|PLC)\b', '', company_name, flags=re.IGNORECASE).strip()
            query = f"{clean_name} stock" if clean_name else f"{ticker} stock"
            rss_url = f"https://news.google.com/rss/search?q={requests.utils.quote(query)}&hl=en-US&gl=US&ceid=US:en"
            resp = requests.get(rss_url, headers=HEADERS, timeout=self.timeout)
            if resp.status_code == 200:
                root = ET.fromstring(resp.content)
                items = root.findall(".//item")
                articles = []
                for idx, item in enumerate(items[:10]):
                    raw_title = item.find("title").text if item.find("title") is not None else ""
                    link = item.find("link").text if item.find("link") is not None else ""
                    raw_date = item.find("pubDate").text if item.find("pubDate") is not None else ""

                    date_str = "Recent"
                    if raw_date:
                        try:
                            dt = datetime.datetime.strptime(raw_date[:25].strip(), "%a, %d %b %Y %H:%M:%S")
                            date_str = dt.strftime("%Y-%m-%d")
                        except Exception:
                            date_str = raw_date[:16]

                    title = raw_title
                    source = "Financial Press"
                    if " - " in raw_title:
                        parts = raw_title.rsplit(" - ", 1)
                        title = parts[0].strip()
                        source = parts[1].strip()

                    if title:
                        articles.append({
                            "article_id": f"gn_{idx + 1}",
                            "headline": title,
                            "text": title,
                            "date": date_str,
                            "source": source,
                            "url": link
                        })
                if articles:
                    return articles
        except Exception as e:
            logger.warning(f"Google News RSS error for {ticker}: {e}")
        return []

    def _fetch_from_offline_dataset(self, ticker: str, company_name: str) -> List[Dict[str, Any]]:
        csv_path = get_financial_news_path()
        if not os.path.exists(csv_path):
            return []

        try:
            df = pd.read_csv(csv_path)
            clean_name = re.sub(r'\b(Corporation|Corp|Inc|Incorporated|Limited|Ltd|LLC|PLC|S\.A\.|Holdings|Group|Company|Co)\b', '', company_name, flags=re.IGNORECASE).strip().lower()
            clean_ticker = ticker.split(".")[0].lower()
            target_name = company_name.lower()

            def matches(csv_co: str) -> bool:
                if not isinstance(csv_co, str):
                    return False
                c = csv_co.strip().lower()
                return (
                    c == target_name or
                    c in target_name or
                    target_name in c or
                    (bool(clean_name) and (c == clean_name or c in clean_name or clean_name in c)) or
                    c == clean_ticker or
                    clean_ticker in c
                )

            matched_mask = df["company"].apply(matches)
            matched_df = df[matched_mask].copy()

            if not matched_df.empty:
                articles = []
                for _, row in matched_df.iterrows():
                    articles.append({
                        "article_id": str(row.get("article_id", "")),
                        "headline": str(row["headline"]),
                        "text": str(row["text"]),
                        "date": str(row.get("date", "Recent")),
                        "source": str(row.get("source", "Financial News")),
                        "url": ""
                    })
                return articles
        except Exception as e:
            logger.warning(f"Offline dataset fallback read error: {e}")
        return []

    def get_news_for_company(self, ticker: str, company_name: str) -> Tuple[List[Dict[str, Any]], str, bool]:
        """
        Retrieves company news via prioritized tiers.
        Returns: (articles_list, news_source_label, is_fallback)
        """
        # Tier 1: Finnhub API if configured
        articles = self._fetch_from_finnhub(ticker)
        if articles:
            return articles, "Live Financial News (Finnhub API)", False

        # Tier 2: Yahoo Finance Search News API
        articles = self._fetch_from_yahoo_search(ticker, company_name)
        if articles:
            return articles, "Live Financial News (Yahoo Finance)", False

        # Tier 3: Google News RSS Financial Feed
        articles = self._fetch_from_google_rss(ticker, company_name)
        if articles:
            return articles, "Live Financial News (Google News RSS)", False

        # Tier 4: Offline Demo Dataset Fallback
        articles = self._fetch_from_offline_dataset(ticker, company_name)
        if articles:
            return articles, "Offline Demo Dataset (Fallback)", True

        # Tier 5: Genuinely unavailable (zero fabrication)
        return [], "Unavailable", False

news_service = NewsRetrievalService()
