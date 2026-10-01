import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"
ORIGIN_HEADER = {"Origin": "http://localhost:3000"}

test_companies = ["AAPL", "TSLA", "NVDA", "MSFT", "GOOGL", "META"]

print("=== TESTING ALL REQUIRED COMPANIES DIRECTLY ===")

for comp in test_companies:
    print(f"\n--- Testing {comp} ---")
    
    # 1. Company Analysis
    r_comp = requests.get(f"{BASE_URL}/company/{comp}", headers=ORIGIN_HEADER)
    assert r_comp.status_code == 200, f"Company failed: {r_comp.status_code} {r_comp.text}"
    c_data = r_comp.json()
    assert r_comp.headers.get("access-control-allow-origin") == "http://localhost:3000"
    print(f"  [OK] Company: {c_data.get('company')} ({c_data.get('ticker')}), Source: {c_data.get('data_source')}")
    print(f"       Snapshot Price: {c_data.get('market_snapshot', {}).get('latest_close')}, Sentiment: {c_data.get('sentiment_overview', {}).get('dominant_sentiment')}")

    # 2. Market Analysis (1mo and 1y)
    r_mkt = requests.get(f"{BASE_URL}/company/{comp}/market?period=1mo", headers=ORIGIN_HEADER)
    assert r_mkt.status_code == 200, f"Market 1mo failed: {r_mkt.status_code} {r_mkt.text}"
    m_data = r_mkt.json()
    assert r_mkt.headers.get("access-control-allow-origin") == "http://localhost:3000"
    print(f"  [OK] Market 1mo: {len(m_data.get('history', []))} pts, SMA20: {m_data.get('history', [{}])[-1].get('sma20')}")

    r_mkt_1y = requests.get(f"{BASE_URL}/company/{comp}/market?period=1y", headers=ORIGIN_HEADER)
    assert r_mkt_1y.status_code == 200
    m_data_1y = r_mkt_1y.json()
    print(f"  [OK] Market 1y: {len(m_data_1y.get('history', []))} pts, Volatility: {m_data_1y.get('summary', {}).get('volatility_annualized')}%")

    # 3. Predictive Analytics
    r_pred = requests.post(f"{BASE_URL}/predict", json={"company": comp, "lookback": 20}, headers=ORIGIN_HEADER)
    assert r_pred.status_code == 200, f"Predict failed: {r_pred.status_code} {r_pred.text}"
    p_data = r_pred.json()
    assert r_pred.headers.get("access-control-allow-origin") == "http://localhost:3000"
    print(f"  [OK] Predict: MAE={p_data.get('metrics', {}).get('mae')}, RMSE={p_data.get('metrics', {}).get('rmse')}, DirAcc={p_data.get('metrics', {}).get('directional_accuracy')}%")
    print(f"       Forecast (5d): {p_data.get('future_forecast')}")

# 4. Test Invalid Company
print("\n--- Testing Invalid Company: XYZRandomCompany123 ---")
r_inv = requests.get(f"{BASE_URL}/company/XYZRandomCompany123", headers=ORIGIN_HEADER)
print(f"Status: {r_inv.status_code}")
assert r_inv.status_code == 404
assert r_inv.headers.get("access-control-allow-origin") == "http://localhost:3000"
err_detail = r_inv.json().get("detail", "")
print(f"Clean error message: '{err_detail}'")
assert "could not be found" in err_detail.lower() or "not recognized" in err_detail.lower() or "supported" in err_detail.lower()

# 5. Test Text Analyzer to make sure it's 100% working
print("\n--- Testing Text Analyzer ---")
sample_text = "NVIDIA's data center revenue surged 112% to $26.3 billion, though regulatory constraints on exports remain a risk."
r_nlp = requests.post(f"{BASE_URL}/analyze-text", json={"text": sample_text}, headers=ORIGIN_HEADER)
assert r_nlp.status_code == 200
assert r_nlp.headers.get("access-control-allow-origin") == "http://localhost:3000"
nlp_data = r_nlp.json()
print(f"  [OK] NLP Sentiment: {nlp_data.get('sentiment', {}).get('sentiment')}, Confidence: {nlp_data.get('sentiment', {}).get('confidence')}%")
print(f"       Entities: {[e['entity'] for e in nlp_data.get('entities', [])]}")
print(f"       Risks: {[r['category'] for r in nlp_data.get('risk_indicators', [])]}")

print("\n==============================================")
print("ALL BACKEND COMPONENT TESTS PASSED WITH CORS!")
print("==============================================")
