from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import csv
import os

from nlp.preprocessor import preprocessor
from nlp.sentiment import sentiment_analyzer
from nlp.ner import financial_ner
from nlp.keywords import keyword_extractor
from nlp.topics import topic_classifier
from nlp.risk_indicators import risk_detector

from services.ticker_resolver import ticker_resolver
from services.company_service import company_service
from services.market_service import market_service
from prediction.lstm_model import lstm_service
from services.evaluation_service import evaluation_service

router = APIRouter(prefix="/api")

# --- Pydantic Request Models ---
class TextAnalysisRequest(BaseModel):
    text: str
    remove_stopwords: Optional[bool] = False

class PredictionRequest(BaseModel):
    company: Optional[str] = "NVIDIA"
    ticker: Optional[str] = None
    lookback: Optional[int] = 20

# --- Endpoints ---

@router.get("/health")
def get_health():
    return {
        "status": "online",
        "service": "InsightPulse Backend",
        "nlp_sentiment_model": sentiment_analyzer.model_status,
        "sample_articles_available": os.path.exists("data/sample_articles.csv"),
        "financial_news_available": os.path.exists("data/financial_news.csv"),
        "market_data_available": os.path.exists("data/market_data/NVDA.csv")
    }

@router.get("/sample-articles")
def get_sample_articles():
    csv_path = "data/sample_articles.csv"
    if not os.path.exists(csv_path):
        return []
    articles = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            articles.append(row)
    return articles

@router.post("/analyze-text")
def analyze_financial_text(req: TextAnalysisRequest):
    text = req.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Financial text input cannot be empty.")

    # 1. Text Preprocessing Stage
    prep_data = preprocessor.preprocess(text, remove_stopwords=req.remove_stopwords)

    # 2. Financial Sentiment Analysis
    sentiment_data = sentiment_analyzer.analyze(prep_data["cleaned_text"])

    # 3. Named Entity Recognition
    entities = financial_ner.extract_entities(prep_data["original_text"])

    # 4. Keyword Extraction
    keywords = keyword_extractor.extract_keywords(prep_data["cleaned_text"], top_k=8)

    # 5. Topic Classification
    topics = topic_classifier.classify_topics(prep_data["cleaned_text"])

    # 6. NLP-Derived Risk Indicators
    risks = risk_detector.detect_risks(prep_data["cleaned_text"])

    return {
        "preprocessing": prep_data,
        "sentiment": sentiment_data,
        "entities": entities,
        "keywords": keywords,
        "topics": topics,
        "risk_indicators": risks,
        "article_summary": {
            "primary_topic": topics[0]["topic"] if topics else "General Finance",
            "primary_risk": risks[0]["category"] if risks else "No Critical Risk Flagged",
            "top_entity": entities[0]["entity"] if entities else "Target Asset",
            "analytical_insight": (
                f"Text exhibits predominantly {sentiment_data['sentiment'].lower()} tone ({sentiment_data['confidence']}% confidence). "
                f"Core focus centers on {topics[0]['topic'] if topics else 'market activity'}"
                f"{f' with notable exposure to {risks[0]['category']}' if risks else ' without immediate distress signals'}."
            )
        }
    }

@router.get("/company/resolve")
def resolve_company(query: Optional[str] = Query(None), q: Optional[str] = Query(None)):
    search_term = query or q
    if not search_term:
        raise HTTPException(status_code=400, detail="Missing query parameter. Provide 'query' or 'q'.")
    try:
        return ticker_resolver.resolve(search_term)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/company/{company}")
def get_company_analysis(company: str):
    try:
        return company_service.analyze_company(company)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/company/{company}/market")
def get_company_market(company: str, period: str = Query("1y", description="Time window")):
    try:
        return market_service.get_market_analysis(company, period=period)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/predict")
def predict_price(req: PredictionRequest):
    target = req.ticker or req.company or "NVIDIA"
    try:
        return lstm_service.predict_and_evaluate(target, lookback=req.lookback or 20)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/evaluation")
def get_model_evaluation():
    try:
        return evaluation_service.get_full_evaluation()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Evaluation error: {str(e)}")
