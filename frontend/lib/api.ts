/**
 * Centralized API Base URL configuration.
 * Dynamically adapts to browser location (localhost vs 127.0.0.1) and environment variables,
 * preventing origin mismatch errors.
 */
export function getApiBaseUrl(): string {
  if (process.env.NEXT_PUBLIC_API_URL) {
    return process.env.NEXT_PUBLIC_API_URL.replace(/\/+$/, "");
  }
  if (typeof window !== "undefined" && window.location) {
    const host = window.location.hostname || "localhost";
    return `http://${host}:8000/api`;
  }
  return "http://127.0.0.1:8000/api";
}

export const API_BASE_URL = getApiBaseUrl();
const API_BASE = API_BASE_URL;

export interface PreprocessingData {
  original_text: string;
  cleaned_text: string;
  tokens: string[];
  token_count: number;
  raw_token_count: number;
  char_count: number;
  vocabulary_size: number;
  financial_tokens: string[];
  stopwords_removed: number;
}

export interface SentimentData {
  sentiment: "Positive" | "Neutral" | "Negative";
  confidence: number;
  probabilities: {
    positive: number;
    neutral: number;
    negative: number;
  };
  model_source: string;
  is_fallback: boolean;
  explanation: string;
}

export interface EntityItem {
  entity: string;
  type: "Organization" | "Money" | "Percentage" | "Person" | "Location" | "Date/Period";
  start_char: number;
  end_char: number;
}

export interface KeywordItem {
  keyword: string;
  score: number;
}

export interface TopicItem {
  topic: string;
  confidence: number;
  relevance_rank: number;
  matched_terms: string[];
}

export interface RiskIndicatorItem {
  category: string;
  description: string;
  severity: "High" | "Moderate";
  evidence_phrases: string[];
}

export interface ArticleSummary {
  primary_topic: string;
  primary_risk: string;
  top_entity: string;
  analytical_insight: string;
}

export interface AnalyzeTextResponse {
  preprocessing: PreprocessingData;
  sentiment: SentimentData;
  entities: EntityItem[];
  keywords: KeywordItem[];
  topics: TopicItem[];
  risk_indicators: RiskIndicatorItem[];
  article_summary: ArticleSummary;
}

export interface CompanySentimentDistribution {
  name: string;
  value: number;
  percentage: number;
}

export interface CompanySentimentOverview {
  dominant_sentiment: string;
  positive_count: number;
  neutral_count: number;
  negative_count: number;
  distribution: CompanySentimentDistribution[];
}

export interface SentimentTrendPoint {
  date: string;
  headline: string;
  sentiment: string;
  score: number;
  confidence: number;
}

export interface CompanyArticleItem {
  article_id: string;
  headline: string;
  date: string;
  source: string;
  text: string;
  sentiment: string;
  confidence: number;
  topics: string[];
  risks: string[];
}

export interface MarketSummary {
  latest_close: number;
  previous_close: number;
  change: number;
  percent_change: number;
  day_high: number;
  day_low: number;
  day_open: number;
  volume: number;
  average_volume_30d: number;
  volatility_annualized: number;
  high_52w: number;
  low_52w: number;
  as_of_date: string;
}

export interface CompanyAnalysisResponse {
  company: string;
  ticker: string;
  currency: string;
  data_source: string;
  news_source: string;
  has_news: boolean;
  news_message?: string;
  article_count: number;
  market_snapshot: MarketSummary | null;
  sentiment_overview: CompanySentimentOverview;
  sentiment_trend: SentimentTrendPoint[];
  top_topics: { topic: string; count: number }[];
  keywords: KeywordItem[];
  risk_indicators: string[];
  articles: CompanyArticleItem[];
}

export interface MarketHistoryPoint {
  date: string;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
  sma20: number | null;
  sma50: number | null;
}

export interface MarketDataResponse {
  company: string;
  ticker: string;
  currency: string;
  data_source: string;
  summary: MarketSummary;
  history: MarketHistoryPoint[];
}

export interface PredictionMetric {
  mae: number;
  rmse: number;
  mape: number;
  directional_accuracy: number;
}

export interface PredictionChartPoint {
  date: string;
  actual: number;
  predicted: number | null;
  is_test: boolean;
}

export interface PredictionResponse {
  company: string;
  ticker: string;
  currency: string;
  data_source: string;
  dataset_info: {
    total_trading_days: number;
    train_samples: number;
    test_samples: number;
    lookback_window: number;
    split_ratio: string;
  };
  metrics: PredictionMetric;
  chart_data: PredictionChartPoint[];
  future_forecast: number[];
  model_architecture: {
    layers: { name: string; type: string }[];
    optimizer: string;
    loss_function: string;
  };
  disclaimer: string;
}

export interface NLPModelMetrics {
  name: string;
  type: string;
  accuracy: number;
  precision: number;
  recall: number;
  f1_score: number;
  confusion_matrix: number[][];
}

export interface NLPEvaluationData {
  evaluation_mode: string;
  test_sample_count: number;
  classes: string[];
  baseline: NLPModelMetrics;
  financial_model: NLPModelMetrics;
  analysis: string;
}

export interface LSTMBenchmarkAsset {
  company: string;
  ticker: string;
  mae: number;
  rmse: number;
  mape: number;
  directional_accuracy: number;
}

export interface LSTMEvaluationData {
  model_type: string;
  input_features: string;
  output: string;
  benchmark_assets: LSTMBenchmarkAsset[];
  metric_explanations: Record<string, string>;
}

export interface EvaluationResponse {
  nlp_evaluation: NLPEvaluationData;
  lstm_evaluation: LSTMEvaluationData;
}

export interface SampleArticle {
  id: string;
  title: string;
  company: string;
  text: string;
}

// --- Centralized API Request Helpers ---

async function safeFetch(url: string, init?: RequestInit): Promise<Response> {
  try {
    const res = await fetch(url, init);
    return res;
  } catch (err: any) {
    if (err?.name === "TypeError" && (err?.message?.includes("Failed to fetch") || err?.message?.includes("NetworkError") || err?.message?.includes("fetch"))) {
      throw new Error("Unable to connect to the InsightPulse backend server. Please verify the FastAPI service is running on http://127.0.0.1:8000.");
    }
    throw err;
  }
}

async function handleApiResponse<T>(res: Response, fallbackError: string): Promise<T> {
  if (!res.ok) {
    let message = fallbackError;
    try {
      const data = await res.json();
      message = data.detail || data.error || data.message || fallbackError;
    } catch {
      message = `${fallbackError} (HTTP ${res.status})`;
    }
    throw new Error(message);
  }
  return res.json();
}

// --- API Client Functions ---

export async function checkHealth(): Promise<{ status: string; nlp_sentiment_model: string }> {
  const res = await safeFetch(`${getApiBaseUrl()}/health`);
  return handleApiResponse(res, "Backend service is offline.");
}

export async function getSampleArticles(): Promise<SampleArticle[]> {
  const res = await safeFetch(`${getApiBaseUrl()}/sample-articles`);
  return handleApiResponse(res, "Failed to load sample articles.");
}

export async function analyzeText(text: string, removeStopwords: boolean = false): Promise<AnalyzeTextResponse> {
  const res = await safeFetch(`${getApiBaseUrl()}/analyze-text`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text, remove_stopwords: removeStopwords }),
  });
  return handleApiResponse(res, "Text analysis failed.");
}

export async function resolveCompany(query: string): Promise<{ ticker: string; company: string; currency: string }> {
  const res = await safeFetch(`${getApiBaseUrl()}/company/resolve?query=${encodeURIComponent(query)}`);
  return handleApiResponse(res, "Company lookup failed.");
}

export async function getCompanyAnalysis(company: string): Promise<CompanyAnalysisResponse> {
  const res = await safeFetch(`${getApiBaseUrl()}/company/${encodeURIComponent(company)}`);
  return handleApiResponse(res, "Company analysis not available.");
}

export async function getMarketData(company: string, period: string = "1y"): Promise<MarketDataResponse> {
  const res = await safeFetch(`${getApiBaseUrl()}/company/${encodeURIComponent(company)}/market?period=${encodeURIComponent(period)}`);
  return handleApiResponse(res, "Market data not available.");
}

export async function runPrediction(company: string, lookback: number = 20): Promise<PredictionResponse> {
  const res = await safeFetch(`${getApiBaseUrl()}/predict`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ company, ticker: company, lookback }),
  });
  return handleApiResponse(res, "Prediction error.");
}

export async function getEvaluation(): Promise<EvaluationResponse> {
  const res = await safeFetch(`${getApiBaseUrl()}/evaluation`);
  return handleApiResponse(res, "Failed to fetch evaluation metrics.");
}

// Session state helper
export function getSavedCompany(): string {
  if (typeof window !== "undefined") {
    return localStorage.getItem("insightpulse_selected_company") || "NVIDIA";
  }
  return "NVIDIA";
}

export function saveCompany(company: string) {
  if (typeof window !== "undefined") {
    localStorage.setItem("insightpulse_selected_company", company);
  }
}
