import json
import os

os.makedirs('notebooks', exist_ok=True)

notebook_content = {
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# InsightPulse: Investment Analysis Using Natural Language Processing\n",
    "## Academic Exploration and Model Evaluation Notebook\n",
    "\n",
    "This notebook demonstrates the foundational NLP and predictive analytics pipeline developed for the **InsightPulse** college mini-project.\n",
    "\n",
    "**Pipeline Outline:**\n",
    "1. Data Loading & Inspection\n",
    "2. Financial-Aware Text Preprocessing & Tokenization\n",
    "3. Financial Sentiment Analysis (FinBERT / Loughran-McDonald Lexicon)\n",
    "4. Named Entity Recognition (NER)\n",
    "5. Topic Identification & NLP-Derived Risk Detection\n",
    "6. NLP Model Evaluation: Baseline (TF-IDF + Logistic Regression) vs Financial Domain Model\n",
    "7. LSTM Time-Series Predictive Analytics & Evaluation (MAE, RMSE, MAPE)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "import sys\n",
    "import os\n",
    "sys.path.append(os.path.abspath('../backend'))\n",
    "\n",
    "import pandas as pd\n",
    "import numpy as np\n",
    "import matplotlib.pyplot as plt\n",
    "\n",
    "from nlp.preprocessor import preprocessor\n",
    "from nlp.sentiment import sentiment_analyzer\n",
    "from nlp.ner import financial_ner\n",
    "from nlp.keywords import keyword_extractor\n",
    "from nlp.topics import topic_classifier\n",
    "from nlp.risk_indicators import risk_detector\n",
    "from prediction.lstm_model import lstm_service\n",
    "from services.evaluation_service import evaluation_service\n",
    "\n",
    "print(\"All InsightPulse core NLP and predictive modules loaded successfully!\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### 1. Load Financial News & Sample Articles"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "news_df = pd.read_csv('../data/financial_news.csv')\n",
    "print(f\"Total News Corpus Articles: {len(news_df)}\")\n",
    "print(\"Companies in corpus:\", news_df['company'].unique())\n",
    "news_df.head(3)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### 2. Financial-Aware Text Preprocessing Demonstration"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "sample_text = \"Tesla reported quarterly revenue of $25.1 billion, up 8% YoY, but automotive gross margin fell to 17.2% amid price cuts in China.\"\n",
    "prep_result = preprocessor.preprocess(sample_text)\n",
    "\n",
    "print(\"Original:\", prep_result[\"original_text\"])\n",
    "print(\"Cleaned:\", prep_result[\"cleaned_text\"])\n",
    "print(\"Token Count:\", prep_result[\"token_count\"])\n",
    "print(\"Preserved Financial Tokens:\", prep_result[\"financial_tokens\"])\n",
    "print(\"Sample Tokens:\", prep_result[\"tokens\"][:12])"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### 3. Financial Sentiment Analysis & NER"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "sent = sentiment_analyzer.analyze(sample_text)\n",
    "print(f\"Sentiment: {sent['sentiment']} ({sent['confidence']}% confidence)\")\n",
    "print(f\"Probabilities: {sent['probabilities']}\")\n",
    "print(f\"Model Source: {sent['model_source']}\")\n",
    "\n",
    "entities = financial_ner.extract_entities(sample_text)\n",
    "print(\"\\nExtracted Named Entities:\")\n",
    "for ent in entities:\n",
    "    print(f\" - {ent['entity']} -> {ent['type']} [{ent['start_char']}:{ent['end_char']}]\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### 4. Topic Classification & NLP-Derived Risk Indicators"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "topics = topic_classifier.classify_topics(sample_text)\n",
    "print(\"Detected Topics:\")\n",
    "for t in topics:\n",
    "    print(f\" - {t['topic']}: {t['confidence']}% relevance\")\n",
    "\n",
    "risks = risk_detector.detect_risks(sample_text)\n",
    "print(\"\\nDetected Risk Indicators:\")\n",
    "for r in risks:\n",
    "    print(f\" - {r['category']} ({r['severity']} Severity): {r['evidence_phrases']}\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### 5. NLP Model Evaluation: Baseline vs Financial Domain Model"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "eval_res = evaluation_service.run_nlp_evaluation()\n",
    "base = eval_res['baseline']\n",
    "fin = eval_res['financial_model']\n",
    "\n",
    "print(f\"=== EVALUATION ON TEST SPLIT ({eval_res['test_sample_count']} articles) ===\")\n",
    "print(f\"Baseline ({base['name']}): Accuracy={base['accuracy']}%, F1={base['f1_score']}%\")\n",
    "print(f\"Financial Model ({fin['name']}): Accuracy={fin['accuracy']}%, F1={fin['f1_score']}%\")\n",
    "print(\"\\nAnalysis:\", eval_res['analysis'])"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### 6. LSTM Predictive Analytics on Historical Market Data"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "lstm_res = lstm_service.predict_and_evaluate('../data/market_data/NVDA.csv')\n",
    "print(f\"Asset: {lstm_res['company']} ({lstm_res['ticker']})\")\n",
    "print(f\"Metrics: MAE={lstm_res['metrics']['mae']}, RMSE={lstm_res['metrics']['rmse']}, MAPE={lstm_res['metrics']['mape']}%\")\n",
    "print(f\"Directional Accuracy: {lstm_res['metrics']['directional_accuracy']}%\")\n",
    "print(f\"Future 5-Day Forecast: {lstm_res['future_forecast']}\")"
   ]
  }
 ],
 "metadata": {
  "language_info": {
   "name": "python"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}

with open('notebooks/exploration_and_evaluation.ipynb', 'w', encoding='utf-8') as f:
    json.dump(notebook_content, f, indent=1)

print("Generated notebooks/exploration_and_evaluation.ipynb")
