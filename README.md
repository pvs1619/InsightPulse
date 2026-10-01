# InsightPulse: Investment Analysis Using Natural Language Processing

### *Financial News Sentiment, Risk and Market Analysis Using NLP and Predictive Analytics*

[![Python Version](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688.svg)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-16.3-black.svg)](https://nextjs.org/)
[![TailwindCSS](https://img.shields.io/badge/TailwindCSS-v4-38bdf8.svg)](https://tailwindcss.com/)
[![Academic Category](https://img.shields.io/badge/Category-College%20NLP%20Mini--Project-amber.svg)]()

---

## 1. Project Overview

**InsightPulse** is a full-stack, college NLP mini-project designed to bridge unstructured corporate disclosures and financial news with quantitative market analytics and predictive time-series forecasting.

Unlike generic stock predictors, **Natural Language Processing remains the central engine** of InsightPulse. The system demonstrates how domain-adapted NLP transforms raw, volatile narrative text into actionable signals—sentiment distributions, named entity extractions, key topical themes, and risk indicators—which are subsequently synthesized with historical technical price indicators and an explainable Long Short-Term Memory (LSTM) forecasting model.

---

## 2. Research Paper Inspirations

This project is academically inspired by two foundational research directions:

1. **Automated Extraction from Financial Reports Using NLP Approaches**:
   * Explores Financial NLP, domain tokenization, FinBERT transformer sentiment analysis, named entity recognition (NER), topic categorization, and textual risk factor extraction from corporate disclosures.
2. **AI-Powered Investment Advisor: Enhancing Financial Decisions with NLP and Predictive Analytics**:
   * Proposes the integration of qualitative NLP capabilities with quantitative time-series forecasting, introducing an NLP-based analytical assistant and an LSTM architecture for asset price progression.

> *Academic Note*: This project adapts these core principles into a manageable, demonstrable, and fully verifiable student-scale implementation. It does not claim complete commercial replication of either paper.

---

## 3. End-to-End Pipeline Architecture

```
Financial News / Reports
         │
         ▼
[1] Domain-Aware Text Preprocessor ──► (Preserves currency symbols $, ₹, percentages %, numbers, financial acronyms)
         │
         ├───► [2] FinBERT / Lexicon Sentiment Classifier ──► (Positive, Neutral, Negative with calibrated probabilities)
         ├───► [3] Named Entity Recognition (NER) ─────────► (Organizations, Money, Percentages, People, Locations, Periods)
         ├───► [4] Domain Keyword Extractor (TF-IDF) ───────► (Unigrams & Financial Collocations)
         ├───► [5] Topic Taxonomy Classifier ──────────────► (AI & Tech, Margins, Regulations, Supply Chain, ESG)
         └───► [6] NLP-Derived Risk Indicator Scanner ────► (Cost pressure, Capacity bottlenecks, Regulatory scrutiny)
         │
         ▼
[7] Corporate News Aggregator & Sentiment Trend Analysis
         │
         ▼
[8] Historical Market Data Service ──► (SMA-20, SMA-50, Daily Returns, Annualized Volatility)
         │
         ▼
[9] LSTM Recurrent Neural Network ───► (Sequence generation, MinMax scaling, 80/20 train/test split, MAE/RMSE/MAPE)
         │
         ▼
[10] Grounded AI Financial Assistant & Integrated Neutral Synthesis
```

---

## 4. Key Features

* **Financial Text Analyzer**: Paste custom financial articles or headlines, or select preloaded cases (Tesla margins, NVIDIA Blackwell GPUs, Reliance green energy, Apple services, Infosys guidance, Microsoft Azure).
* **Transparent Preprocessing Audit**: Inspect raw text, normalized tokens, preserved monetary symbols, and stopword handling with collapsible educational views.
* **FinBERT Sentiment Inference**: Real model inference with calibrated probability distributions (Positive, Neutral, Negative) and clear fallback transparency.
* **Named Entity Recognition**: Extract corporate entities, monetary values (`₹75,000 crore`, `$2.5B`), percentages (`17.2%`), locations, and reporting periods with exact span tracking.
* **NLP-Derived Risk Indicators**: Classify textual risk phrases across 7 distinct categories (Margin Compression, Supply Shortages, Regulatory Probes, Discretionary Spend Softness).
* **Company-Level Aggregation**: Donut sentiment distributions, chronological sentiment trends over time, topic bar charts, and article archives for 8 major companies.
* **Market Technical Analysis**: Interactive charts with 20-day and 50-day Simple Moving Averages, trading volumes, and annualized historical volatility.
* **LSTM Predictive Analytics**: Mathematically transparent recurrent network with forget, input, and output gates predicting next-day prices, with authentic calculated MAE, RMSE, and MAPE metrics.
* **Empirical Model Evaluation**: Comparative benchmark between a baseline (TF-IDF + Logistic Regression) and the Financial Domain Model, complete with confusion matrices and metric definitions.
* **Grounded AI Financial Assistant**: An NLP conversational assistant that answers queries strictly grounded in the analyzed datasets and models.

---

## 5. Technology Stack

### Backend
* **Python 3.12**: Core runtime environment.
* **FastAPI**: Asynchronous REST API framework with automatic OpenAPI documentation.
* **Uvicorn**: Lightning-fast ASGI production web server.
* **Pydantic**: Request and response schema validation.
* **scikit-learn**: TF-IDF vectorization, baseline logistic regression classifier, and evaluation metrics (`accuracy_score`, `precision_recall_fscore_support`, `confusion_matrix`).
* **NumPy & Pandas**: Array operations, matrix math, and time-series dataframe processing.
* **NLTK**: Domain lexicons, tokenization, and stopword corpora.

### Frontend
* **Next.js 16 (App Router)**: Modern React framework with TypeScript and server/client components.
* **React 19**: Responsive user interface.
* **Tailwind CSS v4**: Restrained, professional financial research visual design.
* **Recharts**: Responsive financial line charts, moving average overlays, donut distributions, and bar charts.
* **Lucide React**: Clean, accessible iconography.

---

## 6. Directory Structure

```
InsightPulse/
│
├── frontend/                     # Next.js 16 + React 19 Frontend
│   ├── app/                      # App router pages
│   │   ├── page.tsx              # Home / Dashboard
│   │   ├── layout.tsx            # Global layout with responsive sidebar & header
│   │   ├── globals.css           # Financial research design system
│   │   ├── analyze/page.tsx      # Text Analyzer module
│   │   ├── company/page.tsx      # Company-level analysis
│   │   ├── market/page.tsx       # Market technical analysis
│   │   ├── predict/page.tsx      # LSTM predictive analytics
│   │   ├── evaluation/page.tsx   # Model evaluation (NLP & LSTM)
│   │   ├── assistant/page.tsx    # Grounded AI financial assistant
│   │   ├── methodology/page.tsx  # Academic 10-step methodology
│   │   └── about/page.tsx        # Project metadata & viva guide
│   ├── components/               # Modular UI components
│   │   ├── Sidebar.tsx
│   │   ├── Header.tsx
│   │   ├── PreprocessingViewer.tsx
│   │   ├── SentimentBadge.tsx
│   │   ├── EntityTable.tsx
│   │   ├── TopicBadge.tsx
│   │   └── RiskBadge.tsx
│   ├── lib/
│   │   └── api.ts                # Typed client for backend communication
│   └── package.json
│
├── backend/                      # Python FastAPI Backend
│   ├── main.py                   # Server entrypoint with CORS & error handlers
│   ├── requirements.txt          # Backend dependencies
│   ├── api/
│   │   └── routes.py             # REST API endpoint definitions
│   ├── nlp/                      # NLP core modules
│   │   ├── preprocessor.py       # Financial-aware tokenization & normalization
│   │   ├── sentiment.py          # FinBERT integration & Loughran-McDonald fallback
│   │   ├── ner.py                # Financial Named Entity Recognition
│   │   ├── keywords.py           # Domain-weighted TF-IDF keyword extractor
│   │   ├── topics.py             # Topic classification taxonomy
│   │   └── risk_indicators.py    # NLP-derived risk indicator detector
│   ├── prediction/               # Predictive analytics
│   │   └── lstm_model.py         # LSTM cell, scaler, sequence generator & metrics
│   ├── services/                 # Business logic services
│   │   ├── company_service.py    # Multi-article aggregation & sentiment trends
│   │   ├── market_service.py     # OHLCV loading, SMAs, volatility calculation
│   │   ├── evaluation_service.py # NLP baseline vs transformer & LSTM metrics
│   │   └── assistant_service.py  # Grounded query-answering engine
│   └── utils/
│
├── data/                         # Verified Self-Contained Offline Datasets
│   ├── financial_news.csv        # 80 categorized news articles across 8 companies
│   ├── sample_articles.csv       # Presets for 1-click testing in Text Analyzer
│   └── market_data/              # 320 daily OHLCV trading records per asset
│       ├── NVDA.csv, TSLA.csv, AAPL.csv, MSFT.csv
│       ├── AMZN.csv, RELIANCE.csv, TCS.csv, INFY.csv
│
├── generate_datasets.py          # Deterministic dataset generation script
├── test_backend.py               # Comprehensive backend automated test suite
├── README.md                     # Academic documentation
└── .gitignore
```

---

## 7. Installation & Quickstart

### Prerequisites
* **Python 3.10+** (Python 3.12 recommended)
* **Node.js 18+** (Node.js 20 or 22 recommended)
* **npm**

---

### Step 1: Clone or Navigate to the Repository

```bash
cd c:\Users\DELL\OneDrive\Desktop\InsightPulse
```

---

### Step 2: Backend Setup

1. Install Python dependencies:
```bash
pip install -r backend/requirements.txt
```

2. Verify datasets exist (or regenerate deterministically):
```bash
python generate_datasets.py
```

3. Run the automated backend test suite:
```bash
python test_backend.py
```

4. Launch the FastAPI server:
```bash
python -m uvicorn main:app --app-dir backend --host 127.0.0.1 --port 8000 --reload
```
*API docs will be available at:* `http://127.0.0.1:8000/docs`

---

### Step 3: Frontend Setup

Open a second terminal window:

1. Navigate to the `frontend/` directory:
```bash
cd frontend
```

2. Install npm dependencies:
```bash
npm install
```

3. Launch the Next.js development server:
```bash
npm run dev
```

4. Open your browser and navigate to:
```
http://localhost:3000
```

---

## 8. API Endpoints Reference

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/health` | Backend status, active sentiment model, dataset availability |
| `GET` | `/api/sample-articles` | Sample financial articles for 1-click text analysis |
| `POST` | `/api/analyze-text` | Executes complete NLP pipeline (Preprocessing, Sentiment, NER, Keywords, Topics, Risks) |
| `GET` | `/api/companies` | List of supported corporate entities |
| `GET` | `/api/company/{company}` | Aggregated sentiment overview, trends, top topics, keywords, risks, and article list |
| `GET` | `/api/company/{company}/market` | Historical market OHLCV, SMA20, SMA50, volume, and annualized volatility |
| `POST` | `/api/predict` | Runs LSTM time-series prediction and returns authentic MAE, RMSE, MAPE metrics |
| `GET` | `/api/evaluation` | Empirical comparison of Baseline vs Financial Model and LSTM cross-asset benchmarks |
| `POST` | `/api/chat` | Context-grounded NLP conversational assistant query answering |

---

## 9. Viva Defense & Academic Q&A

### Q1: Why is specialized preprocessing needed for financial text?
> **Answer**: Standard NLP tokenization often discards punctuation and symbols. In financial NLP, currency symbols (`$`, `₹`), percentages (`17.2%`), and numerical magnitudes (`$2.5 billion`) carry vital semantic meaning. Additionally, financial stopword filtering must preserve critical negation and directional words (`not`, `under`, `loss`, `beat`, `down`) that dictate sentiment polarity.

### Q2: How does FinBERT differ from general BERT or VADER?
> **Answer**: BERT is trained on Wikipedia and BooksCorpus where financial terms like "liability" or "debt" have generic or negative connotations. FinBERT is pre-trained on corporate financial disclosures (10-K, 10-Q reports) and financial news, enabling it to recognize financial domain terminology like "margin contraction" or "revenue beat".

### Q3: Why is F1-Score used instead of Accuracy?
> **Answer**: Financial news has inherent class imbalance—press releases are disproportionately positive or neutral compared to negative disclosures. Accuracy can be artificially inflated by simply predicting the majority class. Weighted F1-score balances precision and recall across all sentiment classes.

### Q4: How does the LSTM architecture prevent vanishing gradients?
> **Answer**: In standard recurrent neural networks, gradient signals vanish exponentially during backpropagation through time. LSTM introduces an internal additive Cell State controlled by three gating mechanisms:
> * **Forget Gate**: $f_t = \sigma(W_f \cdot [h_{t-1}, x_t] + b_f)$
> * **Input Gate**: $i_t = \sigma(W_i \cdot [h_{t-1}, x_t] + b_i)$
> * **Output Gate**: $o_t = \sigma(W_o \cdot [h_{t-1}, x_t] + b_o)$
> These gates allow error gradients to flow across multi-day sequences without vanishing.

---

## 10. Academic Disclaimer

**InsightPulse** is developed solely as an educational mini-project for demonstration in a college computer science and natural language processing curriculum. It is not licensed investment, tax, or legal software. Predicted stock values and analytical insights are experimental research artifacts and must never be construed as formal financial advice.
