"use client";

import { useState, useEffect } from "react";
import { 
  analyzeText, 
  getSampleArticles, 
  AnalyzeTextResponse, 
  SampleArticle 
} from "@/lib/api";
import PreprocessingViewer from "@/components/PreprocessingViewer";
import SentimentBadge from "@/components/SentimentBadge";
import EntityTable from "@/components/EntityTable";
import TopicBadge from "@/components/TopicBadge";
import RiskBadge from "@/components/RiskBadge";
import { 
  Play, 
  RotateCcw, 
  Sparkles, 
  AlertCircle, 
  Tag, 
  FileText, 
  Layers, 
  ShieldAlert, 
  Cpu, 
  CheckCircle2 
} from "lucide-react";

export default function TextAnalyzerPage() {
  const [inputText, setInputText] = useState<string>("");
  const [removeStopwords, setRemoveStopwords] = useState<boolean>(false);
  const [sampleArticles, setSampleArticles] = useState<SampleArticle[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<AnalyzeTextResponse | null>(null);

  useEffect(() => {
    getSampleArticles()
      .then((data) => {
        setSampleArticles(data);
        if (data.length > 0 && !inputText) {
          // Preload first sample article for immediate demo readiness
          setInputText(data[0].text);
        }
      })
      .catch((err) => console.error("Could not load sample articles", err));
  }, []);

  const handleAnalyze = async () => {
    if (!inputText.trim()) {
      setError("Please paste or type financial text to analyze.");
      return;
    }

    try {
      setLoading(true);
      setError(null);
      const res = await analyzeText(inputText, removeStopwords);
      setResult(res);
    } catch (err: any) {
      setError(err.message || "Failed to process financial text.");
    } finally {
      setLoading(false);
    }
  };

  const handleSelectSample = (text: string) => {
    setInputText(text);
    setError(null);
  };

  const handleReset = () => {
    setInputText("");
    setResult(null);
    setError(null);
  };

  return (
    <div className="space-y-8 pb-12">
      {/* Header */}
      <div>
        <div className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-blue-50 border border-blue-200 text-blue-700 text-xs font-semibold mb-2">
          <Cpu className="w-3.5 h-3.5" />
          <span>Core NLP Pipeline</span>
        </div>
        <h1 className="text-2xl font-extrabold text-slate-900 tracking-tight">
          Financial Text Analyzer
        </h1>
        <p className="text-xs text-slate-500 mt-1">
          Perform complete financial NLP extraction: domain preprocessing, FinBERT sentiment inference,
          Named Entity Recognition, keyword scoring, topic taxonomy mapping, and NLP-derived risk identification.
        </p>
      </div>

      {/* Input Section */}
      <section className="bg-white rounded-xl border border-slate-200 p-6 shadow-xs space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <label className="text-xs font-bold uppercase tracking-wider text-slate-700 flex items-center gap-2">
            <FileText className="w-4 h-4 text-blue-600" />
            <span>Financial Text Input</span>
          </label>

          {/* Sample Article Picker */}
          {sampleArticles.length > 0 && (
            <div className="flex items-center gap-2 text-xs">
              <span className="text-slate-500 font-medium">Load Sample Article:</span>
              <select
                onChange={(e) => handleSelectSample(e.target.value)}
                className="text-xs bg-slate-50 border border-slate-300 rounded px-2.5 py-1 text-slate-800 focus:outline-hidden focus:ring-2 focus:ring-blue-500"
                defaultValue=""
              >
                <option value="" disabled>Choose preset sample...</option>
                {sampleArticles.map((sample) => (
                  <option key={sample.id} value={sample.text}>
                    {sample.company}: {sample.title}
                  </option>
                ))}
              </select>
            </div>
          )}
        </div>

        {/* Text Area */}
        <textarea
          rows={5}
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          placeholder="Paste financial news headline, article excerpt, earnings call statement, or quarterly report..."
          className="w-full text-sm text-slate-900 bg-slate-50/50 border border-slate-200 rounded-lg p-3.5 font-normal leading-relaxed focus:bg-white focus:outline-hidden focus:ring-2 focus:ring-blue-500 transition-all resize-y"
        />

        {/* Controls & Options */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pt-2">
          <div className="flex items-center gap-2">
            <input
              type="checkbox"
              id="stopwordsCheck"
              checked={removeStopwords}
              onChange={(e) => setRemoveStopwords(e.target.checked)}
              className="rounded border-slate-300 text-blue-600 focus:ring-blue-500"
            />
            <label htmlFor="stopwordsCheck" className="text-xs text-slate-600 select-none cursor-pointer">
              Enable strict stopword filtering <span className="text-slate-400 font-mono">(retains financial negation & directional markers)</span>
            </label>
          </div>

          <div className="flex items-center gap-2.5">
            {result && (
              <button
                type="button"
                onClick={handleReset}
                className="px-3.5 py-2 text-xs font-medium text-slate-600 hover:text-slate-900 bg-slate-100 hover:bg-slate-200 rounded-lg transition-colors flex items-center gap-1.5"
              >
                <RotateCcw className="w-3.5 h-3.5" />
                <span>Reset</span>
              </button>
            )}

            <button
              type="button"
              onClick={handleAnalyze}
              disabled={loading}
              className={`px-5 py-2 text-xs font-bold text-white rounded-lg transition-all flex items-center gap-2 shadow-sm ${
                loading
                  ? "bg-blue-400 cursor-not-allowed"
                  : "bg-blue-600 hover:bg-blue-700 shadow-blue-500/20"
              }`}
            >
              {loading ? (
                <>
                  <div className="w-3.5 h-3.5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                  <span>Executing Pipeline...</span>
                </>
              ) : (
                <>
                  <Play className="w-3.5 h-3.5 fill-current" />
                  <span>Analyze Text</span>
                </>
              )}
            </button>
          </div>
        </div>

        {error && (
          <div className="p-3 bg-rose-50 border border-rose-200 rounded-lg text-xs text-rose-700 flex items-center gap-2">
            <AlertCircle className="w-4 h-4 text-rose-500 shrink-0" />
            <span>{error}</span>
          </div>
        )}
      </section>

      {/* Analysis Results Display */}
      {result && (
        <div className="space-y-6 animate-fadeIn">
          {/* Section 1: Preprocessing Overview (Requirement 7) */}
          <PreprocessingViewer data={result.preprocessing} />

          {/* Section 2: Article Summary Card (Requirement 13) */}
          <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-xs space-y-4">
            <div className="flex items-center justify-between pb-3 border-b border-slate-100">
              <div className="flex items-center gap-2">
                <CheckCircle2 className="w-5 h-5 text-emerald-600" />
                <h2 className="text-base font-bold text-slate-900">
                  Article-Level NLP Analysis Result
                </h2>
              </div>
              <button
                type="button"
                onClick={handleReset}
                className="text-xs text-blue-600 hover:text-blue-700 font-semibold"
              >
                Analyze Another Article →
              </button>
            </div>

            {/* Quick summary metrics */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
              <div className="p-3 bg-slate-50 rounded-lg border border-slate-200">
                <span className="text-[10px] uppercase font-bold text-slate-500 block mb-1">
                  Sentiment
                </span>
                <span className={`text-base font-extrabold ${
                  result.sentiment.sentiment === "Positive"
                    ? "text-emerald-700"
                    : result.sentiment.sentiment === "Negative"
                    ? "text-rose-700"
                    : "text-slate-800"
                }`}>
                  {result.sentiment.sentiment}
                </span>
                <span className="text-[11px] text-slate-500 block mt-0.5 font-mono">
                  {result.sentiment.confidence}% Confidence
                </span>
              </div>

              <div className="p-3 bg-slate-50 rounded-lg border border-slate-200">
                <span className="text-[10px] uppercase font-bold text-slate-500 block mb-1">
                  Primary Topic
                </span>
                <span className="text-sm font-bold text-slate-900 block truncate">
                  {result.article_summary.primary_topic}
                </span>
                <span className="text-[11px] text-slate-500 block mt-0.5 font-mono">
                  Rank #1 Relevance
                </span>
              </div>

              <div className="p-3 bg-slate-50 rounded-lg border border-slate-200">
                <span className="text-[10px] uppercase font-bold text-slate-500 block mb-1">
                  Primary Risk
                </span>
                <span className="text-sm font-bold text-amber-800 block truncate">
                  {result.article_summary.primary_risk}
                </span>
                <span className="text-[11px] text-slate-500 block mt-0.5 font-mono">
                  {result.risk_indicators.length} Risk Signals
                </span>
              </div>

              <div className="p-3 bg-slate-50 rounded-lg border border-slate-200">
                <span className="text-[10px] uppercase font-bold text-slate-500 block mb-1">
                  Primary Entity
                </span>
                <span className="text-sm font-bold text-blue-900 block truncate">
                  {result.article_summary.top_entity}
                </span>
                <span className="text-[11px] text-slate-500 block mt-0.5 font-mono">
                  {result.entities.length} Extracted Spans
                </span>
              </div>
            </div>

            {/* Analytical Synthesis note */}
            <div className="p-3.5 rounded-lg bg-blue-50/60 border border-blue-200 text-xs text-slate-800 leading-relaxed">
              <span className="font-bold text-blue-900">Analytical Insight: </span>
              {result.article_summary.analytical_insight}
            </div>
          </div>

          {/* Section 3: Two Column Layout: Sentiment + NER */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Sentiment Breakdown */}
            <SentimentBadge sentiment={result.sentiment} />

            {/* Named Entities Table */}
            <EntityTable entities={result.entities} />
          </div>

          {/* Section 4: Topics + Keywords + Risks */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Topics */}
            <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-xs">
              <div className="flex items-center justify-between mb-3 pb-2 border-b border-slate-100">
                <span className="text-xs font-bold uppercase tracking-wider text-slate-700">
                  Detected Topics
                </span>
                <span className="text-xs font-mono text-slate-500">
                  {result.topics.length} Mapped
                </span>
              </div>
              <TopicBadge topics={result.topics} />
            </div>

            {/* Key Financial Keywords */}
            <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-xs">
              <div className="flex items-center justify-between mb-3 pb-2 border-b border-slate-100">
                <span className="text-xs font-bold uppercase tracking-wider text-slate-700">
                  Key Financial Keywords
                </span>
                <span className="text-xs font-mono text-slate-500">
                  Domain TF-IDF
                </span>
              </div>
              <div className="flex flex-wrap gap-2">
                {result.keywords.length > 0 ? (
                  result.keywords.map((kw, idx) => (
                    <span
                      key={idx}
                      className="px-2.5 py-1 rounded-md text-xs font-medium bg-slate-100 text-slate-800 border border-slate-200 flex items-center gap-1.5 shadow-2xs hover:bg-slate-200/80 transition-colors"
                    >
                      <Tag className="w-3 h-3 text-slate-400" />
                      <span>{kw.keyword}</span>
                      <span className="text-[10px] text-slate-400 font-mono">
                        ({kw.score})
                      </span>
                    </span>
                  ))
                ) : (
                  <span className="text-xs text-slate-400 italic">No key terms extracted.</span>
                )}
              </div>
            </div>

            {/* NLP-Derived Risk Indicators */}
            <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-xs">
              <div className="flex items-center justify-between mb-3 pb-2 border-b border-slate-100">
                <span className="text-xs font-bold uppercase tracking-wider text-slate-700">
                  NLP-Derived Risk Indicators
                </span>
                <span className="text-[11px] font-mono text-amber-800 bg-amber-50 px-1.5 py-0.5 rounded border border-amber-200">
                  Language Signals
                </span>
              </div>
              <RiskBadge risks={result.risk_indicators} />
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
