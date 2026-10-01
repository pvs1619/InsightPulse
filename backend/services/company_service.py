import os
import pandas as pd
from typing import Dict, Any, List
from collections import Counter
import yfinance as yf

from services.ticker_resolver import ticker_resolver
from services.market_service import market_service
from utils.serializer import sanitize_json_value
from nlp.sentiment import sentiment_analyzer
from nlp.keywords import keyword_extractor
from nlp.topics import topic_classifier
from nlp.risk_indicators import risk_detector

class CompanyAnalysisService:
    """
    Dynamic Company Analysis Service resolving company queries,
    retrieving live financial news / offline datasets, running NLP pipelines,
    and generating corporate analytical aggregations.
    """

    def __init__(self, news_csv_path: str = "data/financial_news.csv"):
        self.news_csv_path = news_csv_path

    def analyze_company(self, query: str) -> Dict[str, Any]:
        resolved = ticker_resolver.resolve(query)
        ticker = resolved["ticker"]
        company_name = resolved["company"]
        currency = resolved["currency"]

        # 1. Fetch market snapshot (live or offline)
        try:
            mkt = market_service.get_market_analysis(ticker, period="1mo")
            market_snapshot = mkt["summary"]
            market_source = mkt["data_source"]
            if mkt.get("company"):
                company_name = mkt["company"]
        except Exception:
            market_snapshot = None
            market_source = "Unavailable"

        # 2. Extract news text items (dynamic live news or offline dataset)
        raw_articles = []
        news_source = "None"

        # Try live yfinance news first
        try:
            yf_ticker = yf.Ticker(ticker)
            live_news = yf_ticker.news
            if live_news and isinstance(live_news, list) and len(live_news) > 0:
                for idx, n in enumerate(live_news[:12]):
                    cnt = n.get("content", {}) if isinstance(n.get("content"), dict) else {}
                    title = cnt.get("title") or n.get("title") or ""
                    summary = cnt.get("summary") or n.get("summary") or ""
                    pub_date = (cnt.get("pubDate") or "")[:10]
                    provider = cnt.get("provider", {}).get("displayName") or n.get("publisher") or "Financial News"

                    if title:
                        raw_articles.append({
                            "article_id": f"live_{idx + 1}",
                            "headline": title,
                            "text": summary or title,
                            "date": pub_date or "Recent",
                            "source": provider
                        })
                if raw_articles:
                    news_source = "Live Financial News"
        except Exception:
            pass

        # If no live news, check offline demo dataset
        if not raw_articles and os.path.exists(self.news_csv_path):
            df = pd.read_csv(self.news_csv_path)
            clean_ticker = ticker.split(".")[0].lower()
            matched_df = df[
                (df["company"].str.lower() == company_name.lower()) |
                (df["company"].str.lower().str.contains(clean_ticker, na=False))
            ].copy()

            if not matched_df.empty:
                for _, row in matched_df.iterrows():
                    raw_articles.append({
                        "article_id": str(row.get("article_id", "")),
                        "headline": str(row["headline"]),
                        "text": str(row["text"]),
                        "date": str(row.get("date", "Recent")),
                        "source": str(row.get("source", "Financial News"))
                    })
                news_source = "Offline Demo Dataset"

        # 3. If no articles available, return clean state without fabricating
        if not raw_articles:
            return sanitize_json_value({
                "company": company_name,
                "ticker": ticker,
                "currency": currency,
                "data_source": market_source,
                "news_source": "Unavailable",
                "has_news": False,
                "news_message": "Live financial news is not currently available for this company. You can analyze financial text manually using the Text Analyzer.",
                "article_count": 0,
                "market_snapshot": market_snapshot,
                "sentiment_overview": {
                    "dominant_sentiment": "No News Available",
                    "positive_count": 0,
                    "neutral_count": 0,
                    "negative_count": 0,
                    "distribution": []
                },
                "sentiment_trend": [],
                "top_topics": [],
                "keywords": [],
                "risk_indicators": [],
                "articles": []
            })

        # 4. Run real NLP pipeline across the articles
        sentiments = []
        all_topics = []
        all_keywords = []
        all_risks = []
        sentiment_trend = []
        articles_list = []
        combined_text = ""

        for art in raw_articles:
            text_content = f"{art['headline']}. {art['text']}"
            combined_text += " " + text_content

            sent_res = sentiment_analyzer.analyze(text_content)
            top_res = topic_classifier.classify_topics(text_content)
            risk_res = risk_detector.detect_risks(text_content)

            sentiments.append(sent_res["sentiment"])

            sentiment_score = 1.0 if sent_res["sentiment"] == "Positive" else (-1.0 if sent_res["sentiment"] == "Negative" else 0.0)
            sentiment_trend.append({
                "date": art["date"],
                "headline": art["headline"],
                "sentiment": sent_res["sentiment"],
                "score": sentiment_score,
                "confidence": sent_res["confidence"]
            })

            for t in top_res:
                all_topics.append(t["topic"])

            for r in risk_res:
                all_risks.append(r["category"])

            articles_list.append({
                "article_id": art["article_id"],
                "headline": art["headline"],
                "date": art["date"],
                "source": art["source"],
                "text": art["text"],
                "sentiment": sent_res["sentiment"],
                "confidence": sent_res["confidence"],
                "topics": [t["topic"] for t in top_res[:2]],
                "risks": [r["category"] for r in risk_res[:2]]
            })

        total_articles = len(raw_articles)
        sent_counts = Counter(sentiments)
        pos_count = sent_counts.get("Positive", 0)
        neu_count = sent_counts.get("Neutral", 0)
        neg_count = sent_counts.get("Negative", 0)

        distribution = [
            {"name": "Positive", "value": pos_count, "percentage": round((pos_count / total_articles) * 100, 1)},
            {"name": "Neutral", "value": neu_count, "percentage": round((neu_count / total_articles) * 100, 1)},
            {"name": "Negative", "value": neg_count, "percentage": round((neg_count / total_articles) * 100, 1)}
        ]

        topic_counts = Counter(all_topics).most_common(5)
        top_topics = [{"topic": topic, "count": count} for topic, count in topic_counts]
        top_keywords = keyword_extractor.extract_keywords(combined_text, top_k=10)
        unique_risks = list(dict.fromkeys(all_risks))

        dominant = max(sent_counts, key=sent_counts.get) if sent_counts else "Neutral"

        return sanitize_json_value({
            "company": company_name,
            "ticker": ticker,
            "currency": currency,
            "data_source": market_source,
            "news_source": news_source,
            "has_news": True,
            "article_count": total_articles,
            "market_snapshot": market_snapshot,
            "sentiment_overview": {
                "dominant_sentiment": dominant,
                "positive_count": pos_count,
                "neutral_count": neu_count,
                "negative_count": neg_count,
                "distribution": distribution
            },
            "sentiment_trend": sentiment_trend,
            "top_topics": top_topics,
            "keywords": top_keywords,
            "risk_indicators": unique_risks,
            "articles": articles_list
        })

company_service = CompanyAnalysisService()
