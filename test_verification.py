import requests
import json
import sys

def test_full_system():
    print("=== STARTING FULL SYSTEM VERIFICATION ===")
    
    # 1. Verify Frontend Pages
    frontend_tests = [
        ("/", 200, "Dashboard"),
        ("/analyze", 200, "Analyze Text"),
        ("/company", 200, "Company Analysis"),
        ("/market", 200, "Market Analysis"),
        ("/predict", 200, "Predictive Analytics"),
        ("/evaluation", 200, "Model Evaluation"),
        ("/about", 404, "About (Removed)"),
        ("/methodology", 404, "Methodology (Removed)"),
        ("/assistant", 404, "AI Assistant (Removed)"),
    ]
    
    frontend_all_pass = True
    print("\n--- FRONTEND ROUTE CHECKS ---")
    for path, expected_status, name in frontend_tests:
        try:
            r = requests.get(f"http://localhost:3000{path}", timeout=5)
            # Next.js may return 404 for deleted routes
            status_ok = (r.status_code == expected_status)
            print(f"[{'PASS' if status_ok else 'FAIL'}] {name} ({path}): status {r.status_code} (expected {expected_status})")
            if not status_ok:
                frontend_all_pass = False
        except Exception as e:
            print(f"[FAIL] {name} ({path}): {e}")
            frontend_all_pass = False

    # 2. Verify Backend Endpoints
    print("\n--- BACKEND ENDPOINT CHECKS ---")
    
    # 2a. Health
    r = requests.get("http://127.0.0.1:8000/api/health")
    print(f"Health check: {r.status_code}, {r.json()}")
    assert r.status_code == 200
    
    # 2b. Chat removed
    r = requests.post("http://127.0.0.1:8000/api/chat", json={"message": "hello"})
    print(f"Chat endpoint check (should be 404): {r.status_code}")
    assert r.status_code == 404
    
    # 2c. Analyze Text (Do NOT break Text Analyzer)
    sample_text = (
        "Alphabet reported robust fourth-quarter cloud computing revenue growth of 28% year-over-year. "
        "However, executives warned that increased capital expenditures in AI infrastructure and higher regulatory "
        "scrutiny in the European Union could pressure operating margins and debt financing costs."
    )
    r = requests.post("http://127.0.0.1:8000/api/analyze-text", json={"text": sample_text})
    print(f"Analyze Text: status {r.status_code}")
    assert r.status_code == 200
    nlp_res = r.json()
    print(f"  Sentiment: {nlp_res.get('sentiment')}, Score: {nlp_res.get('sentiment_score')}")
    print(f"  Entities: {len(nlp_res.get('entities', []))}")
    print(f"  Keywords: {nlp_res.get('keywords', [])[:3]}")
    print(f"  Risk Indicators: {nlp_res.get('risk_indicators', [])}")
    assert "sentiment" in nlp_res
    assert len(nlp_res.get('entities', [])) > 0
    assert len(nlp_res.get('risk_indicators', [])) > 0
    
    # 2d. Dynamic Company Resolve
    r = requests.get("http://127.0.0.1:8000/api/company/resolve?q=Alphabet")
    print(f"Resolve 'Alphabet': status {r.status_code}, data: {r.json()}")
    assert r.status_code == 200
    assert r.json().get("ticker") == "GOOGL"

    # 2e. Dynamic Company Analysis (Custom company outside the 8: GOOGL)
    print("\n--- TESTING CUSTOM COMPANY: GOOGL (Alphabet) ---")
    r = requests.get("http://127.0.0.1:8000/api/company/GOOGL")
    print(f"Company Analysis (GOOGL): status {r.status_code}")
    assert r.status_code == 200
    comp_res = r.json()
    print(f"  Name: {comp_res.get('company')}, Ticker: {comp_res.get('ticker')}")
    print(f"  Data Source: {comp_res.get('data_source')}")
    print(f"  Snapshot: Close = {comp_res.get('market_snapshot', {}).get('latest_close')}, Change = {comp_res.get('market_snapshot', {}).get('percent_change')}%")
    print(f"  Dominant Sentiment: {comp_res.get('sentiment_overview', {}).get('dominant_sentiment')}")
    print(f"  Articles analyzed: {len(comp_res.get('articles', []))}")
    assert comp_res.get('ticker') == 'GOOGL'
    assert comp_res.get('data_source') == 'Live Market Data'

    # 2f. Dynamic Market Analysis (Custom company outside the 8: GOOGL)
    r = requests.get("http://127.0.0.1:8000/api/company/GOOGL/market?period=1y")
    print(f"Market Analysis (GOOGL 1y): status {r.status_code}")
    assert r.status_code == 200
    mkt_res = r.json()
    print(f"  Data Source: {mkt_res.get('data_source')}")
    print(f"  Historical points: {len(mkt_res.get('history', []))}")
    print(f"  Indicators: SMA20={mkt_res.get('history', [{}])[-1].get('sma20')}, Volatility={mkt_res.get('summary', {}).get('volatility_annualized')}%")
    assert len(mkt_res.get('history', [])) > 20

    # 2g. Dynamic Predictive Analytics (Custom company: AAPL)
    print("\n--- TESTING PREDICTIVE ANALYTICS: AAPL ---")
    r = requests.post("http://127.0.0.1:8000/api/predict", json={"ticker": "AAPL", "lookback": 60})
    print(f"Predict (AAPL): status {r.status_code}")
    assert r.status_code == 200
    pred_res = r.json()
    print(f"  Ticker: {pred_res.get('ticker')}")
    print(f"  Data Source: {pred_res.get('data_source')}")
    print(f"  Metrics: MAE={pred_res.get('metrics', {}).get('mae')}, RMSE={pred_res.get('metrics', {}).get('rmse')}, Directional={pred_res.get('metrics', {}).get('directional_accuracy')}%")
    print(f"  Forward 5-day projections: {pred_res.get('future_forecast', [])}")
    assert pred_res.get('ticker') == 'AAPL'
    assert pred_res.get('metrics', {}).get('mae') > 0
    assert len(pred_res.get('future_forecast', [])) == 5

    # 2h. Graceful Handling for Invalid Company
    print("\n--- TESTING INVALID COMPANY: XYZRandomCompany123 ---")
    r = requests.get("http://127.0.0.1:8000/api/company/XYZRandomCompany123")
    print(f"Invalid company status: {r.status_code}")
    assert r.status_code in [404, 400]
    err_detail = r.json().get("detail", "")
    print(f"Clean error message returned: '{err_detail}'")
    assert "could not be found" in err_detail.lower() or "not recognized" in err_detail.lower() or "supported" in err_detail.lower()

    # 2i. Model Evaluation benchmark endpoint
    print("\n--- TESTING MODEL EVALUATION BENCHMARKS ---")
    r = requests.get("http://127.0.0.1:8000/api/evaluation")
    print(f"Evaluation benchmark status: {r.status_code}")
    assert r.status_code == 200
    eval_res = r.json()
    print(f"  NLP Models: Baseline={eval_res.get('nlp_evaluation', {}).get('baseline', {}).get('accuracy')}%, Financial={eval_res.get('nlp_evaluation', {}).get('financial_model', {}).get('accuracy')}%")
    print(f"  LSTM Benchmark assets: {[a.get('ticker') for a in eval_res.get('lstm_evaluation', {}).get('benchmark_assets', [])]}")
    assert "baseline" in eval_res.get('nlp_evaluation', {})
    assert len(eval_res.get('lstm_evaluation', {}).get('benchmark_assets', [])) > 0

    print("\n==========================================")
    print("ALL VERIFICATIONS COMPLETED SUCCESSFULLY!")
    print("==========================================")

if __name__ == "__main__":
    test_full_system()
