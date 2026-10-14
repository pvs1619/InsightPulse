import sys
import os
import tempfile
import pandas as pd
import json

sys.path.append('backend')
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from services.news_service import news_service, NewsRetrievalService
from services.company_service import company_service
from services.evaluation_service import ModelEvaluationService, evaluation_service
from services.ticker_resolver import ticker_resolver
from utils.paths import get_financial_news_path, get_sample_articles_path, get_market_data_dir
from utils.serializer import sanitize_json_value

def run_tests():
    print("================================================================")
    print("RUNNING TARGETED NEWS & EVALUATION VERIFICATION TESTS")
    print("================================================================")

    # Test 1: Deployment-safe path resolution
    print("\n--- TEST 1: Path Resolution Checks ---")
    news_p = get_financial_news_path()
    sample_p = get_sample_articles_path()
    mkt_dir = get_market_data_dir()
    print(f"Financial news path resolved: {news_p} (exists: {os.path.exists(news_p)})")
    print(f"Sample articles path resolved: {sample_p} (exists: {os.path.exists(sample_p)})")
    print(f"Market data dir resolved: {mkt_dir} (exists: {os.path.exists(mkt_dir)})")
    assert os.path.exists(news_p), "financial_news.csv must exist!"
    assert os.path.exists(sample_p), "sample_articles.csv must exist!"
    assert os.path.exists(mkt_dir), "market_data directory must exist!"
    assert os.path.exists(os.path.join(mkt_dir, "NVDA.csv")), "NVDA.csv must exist!"
    print("[PASS] Test 1 passed: All paths resolved correctly.")

    # Test 2: Serializer boolean serialization
    print("\n--- TEST 2: Boolean Serialization (Prevent bool -> int conversion) ---")
    sanitized = sanitize_json_value({"has_news": True, "is_fallback": False, "count": 1, "zero": 0})
    print(f"Sanitized: {sanitized}")
    assert sanitized["has_news"] is True, "has_news must be boolean True!"
    assert sanitized["is_fallback"] is False, "is_fallback must be boolean False!"
    assert sanitized["count"] == 1, "count must remain int 1!"
    assert sanitized["zero"] == 0, "zero must remain int 0!"
    json_str = json.dumps(sanitized)
    print(f"JSON string: {json_str}")
    assert '"has_news": true' in json_str
    assert '"is_fallback": false' in json_str
    print("[PASS] Test 2 passed: Boolean serialization preserved.")

    # Test 3: Company / Ticker resolution
    print("\n--- TEST 3: Company and Ticker Resolution ---")
    for q in ["Apple", "NVDA", "Tesla", "Microsoft", "Alphabet", "Reliance"]:
        res = ticker_resolver.resolve(q)
        print(f"Query '{q}' -> Ticker: {res['ticker']} | Company: {res['company']} | Currency: {res['currency']}")
        assert res["ticker"] and res["company"]
    print("[PASS] Test 3 passed: Company/ticker resolution functional.")

    # Test 4: Live news retrieval across multiple providers / companies
    print("\n--- TEST 4: Live Company News Retrieval ---")
    for q in ["Apple", "Tesla", "NVIDIA"]:
        articles, source, is_fallback = news_service.get_news_for_company(q, q)
        print(f"News for '{q}': {len(articles)} articles retrieved | Source: {source} | Fallback: {is_fallback}")
        assert len(articles) > 0, f"Expected articles for {q}"
        first = articles[0]
        print(f"  Sample article: [{first.get('date')}] {first.get('headline')[:60]}... (Source: {first.get('source')}, URL: {first.get('url')[:30]}...)")
        assert first.get("headline"), "Headline must be non-empty"
        assert first.get("date"), "Date must be present"
    print("[PASS] Test 4 passed: Live company news retrieval functional.")

    # Test 5: Fallback behavior when external providers fail
    print("\n--- TEST 5: Fallback Behavior On External Provider Failure ---")
    # Simulate news service with zero timeout or non-existent endpoint
    broken_news = NewsRetrievalService(timeout=0)
    # Even if live fetch fails, offline dataset fallback should catch supported companies (like NVDA)
    fb_articles, fb_source, fb_is_fallback = broken_news.get_news_for_company("NVDA", "NVIDIA Corporation")
    print(f"Fallback fetch for NVDA: {len(fb_articles)} articles | Source: {fb_source} | Fallback: {fb_is_fallback}")
    assert len(fb_articles) > 0, "Fallback should provide articles from financial_news.csv"
    assert fb_is_fallback is True, "is_fallback must be True for offline dataset fallback"
    assert "Offline Demo Dataset (Fallback)" in fb_source
    print("[PASS] Test 5 passed: Fallback triggers cleanly when external providers are unavailable.")

    # Test 6: Zero fabrication when company is completely unknown and no news
    print("\n--- TEST 6: Zero Fabrication for Unknown / Empty News ---")
    no_news_articles, no_source, no_fallback = broken_news.get_news_for_company("UNKNOWN_TICKER_999", "Unknown Co")
    print(f"Unknown company: {len(no_news_articles)} articles | Source: {no_source} | Fallback: {no_fallback}")
    assert len(no_news_articles) == 0, "Must NOT fabricate news for unknown tickers!"
    assert no_source == "Unavailable"
    assert no_fallback is False
    print("[PASS] Test 6 passed: Zero fabrication verified.")

    # Test 7: Company Analysis End-to-End
    print("\n--- TEST 7: Company Analysis End-to-End ---")
    comp_analysis = company_service.analyze_company("Apple")
    print(f"Company: {comp_analysis['company']} ({comp_analysis['ticker']})")
    print(f"Has News: {comp_analysis['has_news']} | News Source: {comp_analysis['news_source']} | Articles: {comp_analysis['article_count']}")
    assert comp_analysis["has_news"] is True
    assert comp_analysis["article_count"] > 0
    assert "sentiment_overview" in comp_analysis
    assert "sentiment_trend" in comp_analysis
    assert "top_topics" in comp_analysis
    assert "keywords" in comp_analysis
    assert "risk_indicators" in comp_analysis
    first_art = comp_analysis["articles"][0]
    print(f"Article 1: {first_art['headline'][:50]}... | Sentiment: {first_art['sentiment']} ({first_art['confidence']}%) | URL: {first_art.get('url')[:30]}...")
    assert "url" in first_art
    print("[PASS] Test 7 passed: Company Analysis end-to-end verified.")

    # Test 8: Model Evaluation Dataset Validation & Metrics Calculation
    print("\n--- TEST 8: Model Evaluation Service (Actual Dataset) ---")
    eval_res = evaluation_service.get_full_evaluation()
    nlp_eval = eval_res["nlp_evaluation"]
    lstm_eval = eval_res["lstm_evaluation"]
    print(f"Evaluation Mode: {nlp_eval['evaluation_mode']}")
    print(f"Test Samples Evaluated: {nlp_eval['test_sample_count']}")
    print(f"Baseline Accuracy: {nlp_eval['baseline']['accuracy']}% | F1: {nlp_eval['baseline']['f1_score']}%")
    print(f"Financial Model Accuracy: {nlp_eval['financial_model']['accuracy']}% | F1: {nlp_eval['financial_model']['f1_score']}%")
    print(f"Confusion Matrix (Baseline): {nlp_eval['baseline']['confusion_matrix']}")
    print(f"Confusion Matrix (FinModel): {nlp_eval['financial_model']['confusion_matrix']}")
    print(f"LSTM Benchmark Assets: {[a['ticker'] for a in lstm_eval['benchmark_assets']]}")

    assert nlp_eval["test_sample_count"] > 0
    assert nlp_eval["baseline"]["accuracy"] > 0
    assert nlp_eval["financial_model"]["accuracy"] > 0
    assert len(lstm_eval["benchmark_assets"]) > 0
    print("[PASS] Test 8 passed: Actual evaluation metrics calculated successfully from CSV.")

    # Test 9: Model Evaluation Error Handling (Missing File, Empty File, Missing Columns)
    print("\n--- TEST 9: Model Evaluation Robust Error Handling ---")
    # Missing file
    missing_service = ModelEvaluationService(news_csv_path="non_existent_file.csv")
    try:
        missing_service.run_nlp_evaluation()
        assert False, "Should have raised FileNotFoundError"
    except FileNotFoundError as e:
        print(f"  Caught missing file error correctly: {e}")

    # Empty file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as tf:
        empty_path = tf.name
    try:
        empty_service = ModelEvaluationService(news_csv_path=empty_path)
        empty_service.run_nlp_evaluation()
        assert False, "Should have raised ValueError for empty file"
    except ValueError as e:
        print(f"  Caught empty file error correctly: {e}")
    finally:
        os.remove(empty_path)

    # Missing columns
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as tf:
        bad_df = pd.DataFrame({"col1": ["a", "b"], "col2": [1, 2]})
        bad_df.to_csv(tf.name, index=False)
        bad_cols_path = tf.name
    try:
        bad_service = ModelEvaluationService(news_csv_path=bad_cols_path)
        bad_service.run_nlp_evaluation()
        assert False, "Should have raised ValueError for missing columns"
    except ValueError as e:
        print(f"  Caught missing columns error correctly: {e}")
    finally:
        os.remove(bad_cols_path)

    print("[PASS] Test 9 passed: Missing, empty, and malformed dataset errors handled with precision.")

    print("\n================================================================")
    print("ALL TARGETED UNIT & INTEGRATION TESTS PASSED 100%!")
    print("================================================================")

if __name__ == "__main__":
    run_tests()
