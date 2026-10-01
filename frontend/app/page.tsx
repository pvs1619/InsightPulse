"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { 
  getCompanyAnalysis, 
  getMarketData, 
  CompanyAnalysisResponse, 
  MarketDataResponse,
  getSavedCompany,
  saveCompany
} from "@/lib/api";
import CompanySearch from "@/components/CompanySearch";
import { 
  FileText, 
  ShieldAlert, 
  LineChart, 
  TrendingUp, 
  ArrowRight, 
  Sparkles, 
  CheckCircle, 
  Cpu, 
  Building2,
  Layers,
  Activity,
  Database
} from "lucide-react";

export default function HomePage() {
  const [targetCompany, setTargetCompany] = useState<string>("NVIDIA");
  const [companyData, setCompanyData] = useState<CompanyAnalysisResponse | null>(null);
  const [marketData, setMarketData] = useState<MarketDataResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const saved = getSavedCompany();
    if (saved) setTargetCompany(saved);
  }, []);

  const loadData = async (companyQuery: string) => {
    try {
      setLoading(true);
      setError(null);
      saveCompany(companyQuery);
      setTargetCompany(companyQuery);

      const [comp, mkt] = await Promise.all([
        getCompanyAnalysis(companyQuery),
        getMarketData(companyQuery, "1mo")
      ]);
      setCompanyData(comp);
      setMarketData(mkt);
    } catch (e: any) {
      setError(e.message || "Failed to retrieve company intelligence.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData(targetCompany);
  }, []);

  return (
    <div className="space-y-10 pb-12">
      {/* Hero Section */}
      <section className="bg-white rounded-xl border border-slate-200 p-8 md:p-10 shadow-xs relative overflow-hidden">
        <div className="max-w-3xl relative z-10 space-y-4">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-50 border border-blue-200 text-blue-700 text-xs font-semibold">
            <Sparkles className="w-3.5 h-3.5" />
            <span>Financial NLP & Predictive Market Analytics</span>
          </div>

          <h1 className="text-3xl md:text-4xl font-extrabold text-slate-900 tracking-tight leading-tight">
            InsightPulse
          </h1>

          <p className="text-lg md:text-xl text-slate-700 font-semibold">
            Investment Analysis Using Natural Language Processing
          </p>

          <p className="text-sm md:text-base text-slate-600 font-medium">
            Analyze financial text, market trends, sentiment and predictive signals in one place.
          </p>

          <p className="text-xs text-slate-500 leading-relaxed pt-1">
            InsightPulse transforms unstructured corporate disclosures, financial reports, and news narratives
            into structured investment signals. It couples domain-specific sentiment classification,
            named entity extraction, topic modeling, and risk identification with historical price analytics and
            LSTM recurrent neural forecasting.
          </p>

          <div className="pt-4 flex flex-wrap items-center gap-3">
            <Link
              href="/analyze"
              className="inline-flex items-center gap-2 px-5 py-2.5 rounded-lg bg-blue-600 text-white font-semibold text-xs hover:bg-blue-700 transition-colors shadow-sm shadow-blue-500/25"
            >
              <span>Start Analysis</span>
              <ArrowRight className="w-4 h-4" />
            </Link>

            <Link
              href="/company"
              className="inline-flex items-center gap-2 px-4 py-2.5 rounded-lg bg-slate-100 text-slate-700 font-medium text-xs hover:bg-slate-200 transition-colors border border-slate-200"
            >
              <Building2 className="w-4 h-4 text-slate-500" />
              <span>Company Intelligence</span>
            </Link>

            <Link
              href="/predict"
              className="inline-flex items-center gap-2 px-4 py-2.5 rounded-lg bg-slate-100 text-slate-700 font-medium text-xs hover:bg-slate-200 transition-colors border border-slate-200"
            >
              <TrendingUp className="w-4 h-4 text-purple-600" />
              <span>Predictive Analytics</span>
            </Link>
          </div>
        </div>

        {/* Decorative subtle background icon */}
        <div className="hidden lg:block absolute -right-6 -bottom-6 opacity-5 pointer-events-none text-slate-900">
          <Layers className="w-80 h-80" />
        </div>
      </section>

      {/* 4 Core Feature Cards (Requirement 27) */}
      <section className="space-y-4">
        <div>
          <h2 className="text-xs font-bold text-slate-900 uppercase tracking-wider">
            Analytical Platform Capabilities
          </h2>
          <p className="text-xs text-slate-500">
            Four interconnected pillars combining financial domain NLP with predictive time-series models.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
          {/* Card 1: Financial Sentiment */}
          <Link
            href="/analyze"
            className="fin-card p-6 flex flex-col justify-between group hover:border-blue-300"
          >
            <div>
              <div className="w-10 h-10 rounded-lg bg-blue-50 border border-blue-200 flex items-center justify-center text-blue-600 mb-4 group-hover:scale-105 transition-transform">
                <FileText className="w-5 h-5" />
              </div>
              <h3 className="text-sm font-bold text-slate-900 mb-1.5 group-hover:text-blue-600 transition-colors">
                Financial Sentiment
              </h3>
              <p className="text-xs text-slate-600 leading-relaxed">
                Analyze financial text using domain-specific NLP with calibrated probability distributions
                and financial-aware tokenization.
              </p>
            </div>
            <div className="mt-5 pt-3 border-t border-slate-100 flex items-center justify-between text-xs font-medium text-blue-600">
              <span>Analyze Text</span>
              <ArrowRight className="w-3.5 h-3.5 group-hover:translate-x-1 transition-transform" />
            </div>
          </Link>

          {/* Card 2: Risk Detection */}
          <Link
            href="/company"
            className="fin-card p-6 flex flex-col justify-between group hover:border-amber-300"
          >
            <div>
              <div className="w-10 h-10 rounded-lg bg-amber-50 border border-amber-200 flex items-center justify-center text-amber-600 mb-4 group-hover:scale-105 transition-transform">
                <ShieldAlert className="w-5 h-5" />
              </div>
              <h3 className="text-sm font-bold text-slate-900 mb-1.5 group-hover:text-amber-600 transition-colors">
                Risk Detection
              </h3>
              <p className="text-xs text-slate-600 leading-relaxed">
                Identify risk-related signals in financial language: cost pressures, supply shortages,
                litigation, and regulatory probes.
              </p>
            </div>
            <div className="mt-5 pt-3 border-t border-slate-100 flex items-center justify-between text-xs font-medium text-amber-700">
              <span>View Indicators</span>
              <ArrowRight className="w-3.5 h-3.5 group-hover:translate-x-1 transition-transform" />
            </div>
          </Link>

          {/* Card 3: Market Analysis */}
          <Link
            href="/market"
            className="fin-card p-6 flex flex-col justify-between group hover:border-emerald-300"
          >
            <div>
              <div className="w-10 h-10 rounded-lg bg-emerald-50 border border-emerald-200 flex items-center justify-center text-emerald-600 mb-4 group-hover:scale-105 transition-transform">
                <LineChart className="w-5 h-5" />
              </div>
              <h3 className="text-sm font-bold text-slate-900 mb-1.5 group-hover:text-emerald-600 transition-colors">
                Market Analysis
              </h3>
              <p className="text-xs text-slate-600 leading-relaxed">
                Explore historical market data and technical indicators: daily changes, SMA-20,
                SMA-50 overlays, and annualized price volatility.
              </p>
            </div>
            <div className="mt-5 pt-3 border-t border-slate-100 flex items-center justify-between text-xs font-medium text-emerald-700">
              <span>Explore Markets</span>
              <ArrowRight className="w-3.5 h-3.5 group-hover:translate-x-1 transition-transform" />
            </div>
          </Link>

          {/* Card 4: Predictive Analytics */}
          <Link
            href="/predict"
            className="fin-card p-6 flex flex-col justify-between group hover:border-purple-300"
          >
            <div>
              <div className="w-10 h-10 rounded-lg bg-purple-50 border border-purple-200 flex items-center justify-center text-purple-600 mb-4 group-hover:scale-105 transition-transform">
                <TrendingUp className="w-5 h-5" />
              </div>
              <h3 className="text-sm font-bold text-slate-900 mb-1.5 group-hover:text-purple-600 transition-colors">
                Predictive Analytics
              </h3>
              <p className="text-xs text-slate-600 leading-relaxed">
                Experiment with LSTM-based historical price forecasting with authentic MAE, RMSE,
                and MAPE validation metrics.
              </p>
            </div>
            <div className="mt-5 pt-3 border-t border-slate-100 flex items-center justify-between text-xs font-medium text-purple-700">
              <span>Run Predictions</span>
              <ArrowRight className="w-3.5 h-3.5 group-hover:translate-x-1 transition-transform" />
            </div>
          </Link>
        </div>
      </section>

      {/* Dynamic Company Search & Executive Dashboard Overview */}
      <section className="bg-white rounded-xl border border-slate-200 p-6 md:p-8 shadow-xs space-y-6">
        <div className="space-y-1">
          <div className="text-xs font-bold text-slate-500 uppercase tracking-wider">
            Live Corporate Intelligence
          </div>
          <h2 className="text-xl font-bold text-slate-900 tracking-tight">
            Search & Analyze Any Company or Stock Ticker
          </h2>
          <p className="text-xs text-slate-500">
            Enter any global or regional enterprise to retrieve dynamic market quotes, live news sentiment, and risk signals.
          </p>
        </div>

        {/* Dynamic Search Component */}
        <CompanySearch
          initialValue={targetCompany}
          onSearch={(q) => loadData(q)}
          loading={loading}
          placeholder="Enter company name or stock ticker (e.g., Apple, TSLA, Google, TCS.NS, Meta)..."
          buttonText="Analyze Asset"
        />

        {loading ? (
          <div className="py-12 text-center text-xs text-slate-400 font-mono">
            Fetching dynamic intelligence for {targetCompany}...
          </div>
        ) : error ? (
          <div className="p-4 rounded-lg bg-amber-50 border border-amber-200 text-xs text-amber-900">
            {error}
          </div>
        ) : companyData && marketData ? (
          <div className="space-y-6">
            {/* Header info */}
            <div className="flex flex-wrap items-center justify-between gap-3 pb-3 border-b border-slate-100">
              <div>
                <h3 className="text-lg font-bold text-slate-900 flex items-center gap-2">
                  <span>{companyData.company}</span>
                  <span className="text-sm font-mono text-slate-500">({companyData.ticker})</span>
                </h3>
              </div>
              <div className="flex items-center gap-2 font-mono text-xs">
                <span className="px-2.5 py-0.5 rounded bg-slate-100 text-slate-700 border border-slate-200">
                  Market: {marketData.data_source}
                </span>
                <span className="px-2.5 py-0.5 rounded bg-blue-50 text-blue-800 border border-blue-200">
                  News: {companyData.news_source}
                </span>
              </div>
            </div>

            {/* Quick Metrics */}
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4">
              {/* Price */}
              <div className="p-4 rounded-lg bg-slate-50 border border-slate-200">
                <span className="text-[10px] font-semibold text-slate-500 uppercase tracking-wider block mb-1">
                  Market Price
                </span>
                <div className="flex items-baseline gap-2">
                  <span className="text-xl font-bold text-slate-900 font-mono">
                    {marketData.currency}{marketData.summary.latest_close}
                  </span>
                  <span className={`text-xs font-semibold font-mono ${
                    marketData.summary.percent_change >= 0 ? "text-emerald-700" : "text-rose-700"
                  }`}>
                    {marketData.summary.percent_change >= 0 ? "+" : ""}{marketData.summary.percent_change}%
                  </span>
                </div>
                <div className="text-[11px] text-slate-500 mt-1 font-mono">
                  Vol: {marketData.summary.volume.toLocaleString()}
                </div>
              </div>

              {/* Sentiment */}
              <div className="p-4 rounded-lg bg-slate-50 border border-slate-200">
                <span className="text-[10px] font-semibold text-slate-500 uppercase tracking-wider block mb-1">
                  NLP Sentiment
                </span>
                <div className="flex items-baseline gap-2">
                  <span className={`text-xl font-bold ${
                    companyData.sentiment_overview.dominant_sentiment === "Positive"
                      ? "text-emerald-700"
                      : companyData.sentiment_overview.dominant_sentiment === "Negative"
                      ? "text-rose-700"
                      : "text-slate-800"
                  }`}>
                    {companyData.sentiment_overview.dominant_sentiment}
                  </span>
                  <span className="text-xs text-slate-500 font-mono">
                    ({companyData.article_count} items)
                  </span>
                </div>
                {companyData.has_news && companyData.sentiment_overview.distribution.length > 0 ? (
                  <div className="text-[11px] text-slate-500 mt-1 font-mono flex gap-2">
                    <span className="text-emerald-600">Pos: {companyData.sentiment_overview.distribution[0]?.percentage}%</span>
                    <span className="text-slate-500">Neu: {companyData.sentiment_overview.distribution[1]?.percentage}%</span>
                    <span className="text-rose-600">Neg: {companyData.sentiment_overview.distribution[2]?.percentage}%</span>
                  </div>
                ) : (
                  <div className="text-[11px] text-slate-400 italic mt-1">Manual analysis available</div>
                )}
              </div>

              {/* Top Topic */}
              <div className="p-4 rounded-lg bg-slate-50 border border-slate-200">
                <span className="text-[10px] font-semibold text-slate-500 uppercase tracking-wider block mb-1">
                  Primary Theme
                </span>
                <div className="text-sm font-bold text-slate-900 truncate">
                  {companyData.top_topics[0]?.topic || "General Markets"}
                </div>
                <div className="text-[11px] text-slate-500 mt-1 font-mono">
                  {companyData.top_topics[0]?.count || 0} References
                </div>
              </div>

              {/* Primary Risk */}
              <div className="p-4 rounded-lg bg-slate-50 border border-slate-200">
                <span className="text-[10px] font-semibold text-slate-500 uppercase tracking-wider block mb-1">
                  NLP Risk Factor
                </span>
                <div className="text-sm font-bold text-amber-800 truncate">
                  {companyData.risk_indicators[0] || "No Critical Risk Flagged"}
                </div>
                <div className="text-[11px] text-slate-500 mt-1 font-mono">
                  {companyData.risk_indicators.length} Categories Flagged
                </div>
              </div>
            </div>

            {/* Quick Links */}
            <div className="pt-2 flex flex-wrap items-center gap-3">
              <Link
                href={`/company?company=${encodeURIComponent(companyData.ticker)}`}
                className="text-xs font-semibold text-blue-600 hover:text-blue-800 flex items-center gap-1"
              >
                <span>Full Company Report ({companyData.ticker})</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </Link>

              <Link
                href={`/market?company=${encodeURIComponent(companyData.ticker)}`}
                className="text-xs font-semibold text-emerald-600 hover:text-emerald-800 flex items-center gap-1"
              >
                <span>Technical Market Charts</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </Link>

              <Link
                href={`/predict?company=${encodeURIComponent(companyData.ticker)}`}
                className="text-xs font-semibold text-purple-600 hover:text-purple-800 flex items-center gap-1"
              >
                <span>Run LSTM Prediction</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </Link>
            </div>
          </div>
        ) : null}
      </section>
    </div>
  );
}
