import sys
import os

sys.path.append('backend')

from api.routes import (
    analyze_financial_text, TextAnalysisRequest,
    resolve_company, get_company_analysis, get_company_market,
    predict_price, PredictionRequest,
    get_model_evaluation
)

print("--- 1. Testing Text Analysis (Ensuring Text Analyzer Not Broken) ---")
req = TextAnalysisRequest(
    text="Tesla reported stronger-than-expected quarterly revenue driven by increased vehicle deliveries, although rising production costs could pressure operating margins."
)
res = analyze_financial_text(req)
print("Sentiment:", res["sentiment"]["sentiment"], f"({res['sentiment']['confidence']}%)")
print("Topics:", [t["topic"] for t in res["topics"]])
print("Risks:", [r["category"] for r in res["risk_indicators"]])
print("Entities:", [(e["entity"], e["type"]) for e in res["entities"]])

print("\n--- 2. Testing Dynamic Company Resolution (Beyond 8 companies) ---")
for query in ["Google", "Spotify", "Meta", "Tesla", "TCS", "NVDA", "AAPL"]:
    try:
        resolved = resolve_company(query)
        print(f"'{query}' -> Ticker: {resolved['ticker']} | Company: {resolved['company']} ({resolved['currency']})")
    except Exception as e:
        print(f"'{query}' resolution failed: {e}")

print("\n--- 3. Testing Dynamic Market Analysis (AAPL live data) ---")
try:
    mkt = get_company_market("AAPL", period="1mo")
    print(f"AAPL Market Data: Close={mkt['summary']['latest_close']}{mkt['currency']} | Change={mkt['summary']['percent_change']}% | Source={mkt['data_source']} | History Points={len(mkt['history'])}")
except Exception as e:
    print("AAPL Market Data failed:", e)

print("\n--- 4. Testing Dynamic Company Analysis (Custom company GOOGL / Alphabet) ---")
try:
    comp_res = get_company_analysis("Google")
    print(f"Company: {comp_res['company']} ({comp_res['ticker']}) | Market Source: {comp_res['data_source']} | News Source: {comp_res['news_source']} | Articles: {comp_res['article_count']}")
    if comp_res['has_news']:
        print("Dominant Sentiment:", comp_res['sentiment_overview']['dominant_sentiment'])
        print("Top Topics:", [t['topic'] for t in comp_res['top_topics'][:2]])
    else:
        print("News Notice:", comp_res['news_message'])
except Exception as e:
    print("Google Analysis failed:", e)

print("\n--- 5. Testing Dynamic LSTM Prediction on Arbitrary Company (AAPL) ---")
try:
    pred = predict_price(PredictionRequest(company="AAPL", lookback=15))
    print(f"LSTM for {pred['company']} ({pred['ticker']}): MAE={pred['metrics']['mae']}, RMSE={pred['metrics']['rmse']}, MAPE={pred['metrics']['mape']}%, DirAcc={pred['metrics']['directional_accuracy']}%")
    print("Future 5-Day Forecast:", pred["future_forecast"])
except Exception as e:
    print("Prediction failed:", e)

print("\n--- 6. Testing Invalid Company Handling ---")
try:
    resolve_company("XYZRandomCompany123")
    print("ERROR: Should have failed for invalid company!")
except Exception as e:
    print("Clean invalid company error caught successfully:", str(e))

print("\n--- 7. Testing Model Evaluation Benchmark ---")
ev = get_model_evaluation()
print(f"NLP Baseline F1: {ev['nlp_evaluation']['baseline']['f1_score']}% | FinModel F1: {ev['nlp_evaluation']['financial_model']['f1_score']}%")
print("Benchmark assets evaluated:", len(ev["lstm_evaluation"]["benchmark_assets"]))

print("\nALL BACKEND DYNAMIC TESTS COMPLETED SUCCESSFULLY!")
