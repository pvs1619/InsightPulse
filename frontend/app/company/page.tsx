"use client";

import { useState, useEffect, Suspense } from "react";
import { useSearchParams } from "next/navigation";
import { 
  getCompanyAnalysis, 
  CompanyAnalysisResponse,
  getSavedCompany,
  saveCompany
} from "@/lib/api";
import CompanySearch from "@/components/CompanySearch";
import { 
  Building2, 
  TrendingUp, 
  TrendingDown,
  FileText, 
  ShieldAlert, 
  Tag, 
  Calendar, 
  Layers,
  Activity,
  Database,
  AlertCircle,
  ExternalLink
} from "lucide-react";
import {
  PieChart,
  Pie,
  Cell,
  Tooltip as RechartsTooltip,
  Legend,
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  BarChart,
  Bar
} from "recharts";
import Link from "next/link";

const PIE_COLORS = {
  Positive: "#059669",
  Neutral: "#64748b",
  Negative: "#e11d48"
};

function CompanyAnalysisContent() {
  const searchParams = useSearchParams();
  const [selectedCompany, setSelectedCompany] = useState<string>("NVIDIA");
  const [data, setData] = useState<CompanyAnalysisResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const paramCompany = searchParams?.get("company");
    if (paramCompany) {
      setSelectedCompany(paramCompany);
      fetchCompanyData(paramCompany);
    } else {
      const saved = getSavedCompany();
      setSelectedCompany(saved);
      fetchCompanyData(saved);
    }
  }, [searchParams]);

  const fetchCompanyData = async (query: string) => {
    if (!query.trim()) return;
    setLoading(true);
    setError(null);
    saveCompany(query);
    setSelectedCompany(query);

    try {
      const res = await getCompanyAnalysis(query);
      setData(res);
    } catch (err: any) {
      setError(err.message || "Failed to retrieve company intelligence.");
      setData(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-8 pb-12">
      {/* Title */}
      <div>
        <div className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-blue-50 border border-blue-200 text-blue-700 text-xs font-semibold mb-2">
          <Building2 className="w-3.5 h-3.5" />
          <span>Corporate Financial NLP</span>
        </div>
        <h1 className="text-2xl font-extrabold text-slate-900 tracking-tight">
          Company Analysis
        </h1>
        <p className="text-xs text-slate-500 mt-1">
          Search any global or domestic company to analyze financial news sentiment, thematic topics, and NLP-derived risks.
        </p>
      </div>

      {/* Dynamic Company Search (Requirement 7 & 36) */}
      <CompanySearch
        initialValue={selectedCompany}
        onSearch={fetchCompanyData}
        loading={loading}
        placeholder="Enter company name or stock ticker (e.g., Apple, TSLA, Google, TCS.NS, Meta, Microsoft)..."
        buttonText="Analyze Company"
      />

      {loading ? (
        <div className="py-20 text-center space-y-3 bg-white rounded-xl border border-slate-200 shadow-xs">
          <div className="w-6 h-6 border-2 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto" />
          <p className="text-xs text-slate-500 font-mono">
            Resolving ticker and extracting NLP intelligence for {selectedCompany}...
          </p>
        </div>
      ) : error ? (
        <div className="p-4 bg-rose-50 border border-rose-200 rounded-lg text-xs text-rose-700 flex items-center gap-2">
          <AlertCircle className="w-4 h-4 text-rose-600 shrink-0" />
          <span>{error}</span>
        </div>
      ) : data ? (
        <div className="space-y-6">
          {/* Company Header & Data Source Labels (Requirement 11 & 12) */}
          <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-xs flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div>
              <div className="flex items-center gap-2.5">
                <h2 className="text-xl font-bold text-slate-900 tracking-tight">
                  {data.company}
                </h2>
                <span className="text-xs font-mono font-bold px-2 py-0.5 rounded bg-slate-100 text-slate-800 border border-slate-200">
                  {data.ticker}
                </span>
              </div>
              <p className="text-xs text-slate-500 mt-0.5">
                Financial narrative sentiment and risk monitoring profile
              </p>
            </div>

            <div className="flex flex-wrap items-center gap-2 text-xs font-mono">
              <span className="px-2.5 py-1 rounded-md bg-emerald-50 text-emerald-800 border border-emerald-200 flex items-center gap-1.5">
                <Activity className="w-3.5 h-3.5 text-emerald-600" />
                <span>Market: {data.data_source}</span>
              </span>

              <span className="px-2.5 py-1 rounded-md bg-blue-50 text-blue-800 border border-blue-200 flex items-center gap-1.5">
                <Database className="w-3.5 h-3.5 text-blue-600" />
                <span>News: {data.news_source}</span>
              </span>
            </div>
          </div>

          {/* Market Snapshot Row */}
          {data.market_snapshot && (
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
              <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs">
                <span className="text-[10px] font-semibold text-slate-500 uppercase tracking-wider block mb-1">
                  Market Price
                </span>
                <div className="text-2xl font-extrabold text-slate-900 font-mono">
                  {data.currency}{data.market_snapshot.latest_close}
                </div>
                <div className="text-[11px] text-slate-400 font-mono mt-0.5">
                  Prev: {data.currency}{data.market_snapshot.previous_close}
                </div>
              </div>

              <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs">
                <span className="text-[10px] font-semibold text-slate-500 uppercase tracking-wider block mb-1">
                  Daily Change
                </span>
                <div className={`text-2xl font-extrabold font-mono flex items-center gap-1 ${
                  data.market_snapshot.percent_change >= 0 ? "text-emerald-700" : "text-rose-700"
                }`}>
                  {data.market_snapshot.percent_change >= 0 ? (
                    <TrendingUp className="w-4 h-4" />
                  ) : (
                    <TrendingDown className="w-4 h-4" />
                  )}
                  <span>
                    {data.market_snapshot.percent_change >= 0 ? "+" : ""}{data.market_snapshot.percent_change}%
                  </span>
                </div>
                <div className="text-[11px] text-slate-500 font-mono mt-0.5">
                  {data.market_snapshot.change >= 0 ? "+" : ""}{data.currency}{data.market_snapshot.change}
                </div>
              </div>

              <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs">
                <span className="text-[10px] font-semibold text-slate-500 uppercase tracking-wider block mb-1">
                  Trading Volume
                </span>
                <div className="text-xl font-bold text-slate-900 font-mono">
                  {data.market_snapshot.volume.toLocaleString()}
                </div>
                <div className="text-[11px] text-slate-400 font-mono mt-0.5">
                  Avg 30d: {data.market_snapshot.average_volume_30d.toLocaleString()}
                </div>
              </div>

              <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs">
                <span className="text-[10px] font-semibold text-slate-500 uppercase tracking-wider block mb-1">
                  Annualized Volatility
                </span>
                <div className="text-xl font-bold text-slate-800 font-mono">
                  {data.market_snapshot.volatility_annualized}%
                </div>
                <div className="text-[11px] text-slate-400 font-sans mt-0.5">
                  Daily Log Return Std.
                </div>
              </div>
            </div>
          )}

          {/* If no news is available, show clear notice (Requirement 13) */}
          {!data.has_news && (
            <div className="p-6 bg-slate-50 border border-slate-200 rounded-xl space-y-2 text-center">
              <FileText className="w-8 h-8 text-slate-400 mx-auto" />
              <h3 className="text-sm font-bold text-slate-800">
                News Feed Unavailable
              </h3>
              <p className="text-xs text-slate-600 max-w-lg mx-auto">
                {data.news_message || "Live financial news is not currently available for this company. You can analyze financial text manually using the Text Analyzer."}
              </p>
              <div className="pt-2">
                <Link
                  href="/analyze"
                  className="inline-flex items-center gap-1.5 px-4 py-2 rounded-lg bg-blue-600 text-white text-xs font-semibold hover:bg-blue-700 transition-colors"
                >
                  <span>Open Text Analyzer</span>
                </Link>
              </div>
            </div>
          )}

          {/* Sentiment Overview & Distribution Cards */}
          {data.has_news && (
            <>
              <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-xs">
                  <span className="text-[11px] font-semibold text-slate-500 uppercase tracking-wider block mb-1">
                    Dominant Sentiment
                  </span>
                  <div className="flex items-baseline gap-2">
                    <span className={`text-2xl font-extrabold ${
                      data.sentiment_overview.dominant_sentiment === "Positive"
                        ? "text-emerald-700"
                        : data.sentiment_overview.dominant_sentiment === "Negative"
                        ? "text-rose-700"
                        : "text-slate-800"
                    }`}>
                      {data.sentiment_overview.dominant_sentiment}
                    </span>
                    <span className="text-xs text-slate-400 font-mono">
                      ({data.article_count} items)
                    </span>
                  </div>
                </div>

                <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-xs">
                  <span className="text-[11px] font-semibold text-slate-500 uppercase tracking-wider block mb-1">
                    Positive Coverage
                  </span>
                  <div className="flex items-baseline gap-2">
                    <span className="text-2xl font-extrabold text-emerald-700 font-mono">
                      {data.sentiment_overview.positive_count}
                    </span>
                    <span className="text-xs text-slate-500">
                      ({data.sentiment_overview.distribution[0]?.percentage || 0}%)
                    </span>
                  </div>
                </div>

                <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-xs">
                  <span className="text-[11px] font-semibold text-slate-500 uppercase tracking-wider block mb-1">
                    Neutral Coverage
                  </span>
                  <div className="flex items-baseline gap-2">
                    <span className="text-2xl font-extrabold text-slate-700 font-mono">
                      {data.sentiment_overview.neutral_count}
                    </span>
                    <span className="text-xs text-slate-500">
                      ({data.sentiment_overview.distribution[1]?.percentage || 0}%)
                    </span>
                  </div>
                </div>

                <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-xs">
                  <span className="text-[11px] font-semibold text-slate-500 uppercase tracking-wider block mb-1">
                    Negative Coverage
                  </span>
                  <div className="flex items-baseline gap-2">
                    <span className="text-2xl font-extrabold text-rose-700 font-mono">
                      {data.sentiment_overview.negative_count}
                    </span>
                    <span className="text-xs text-slate-500">
                      ({data.sentiment_overview.distribution[2]?.percentage || 0}%)
                    </span>
                  </div>
                </div>
              </div>

              {/* Charts Row: Donut Distribution & Sentiment Trend Line */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Donut Chart: Sentiment Distribution */}
                <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-xs space-y-4">
                  <div>
                    <h3 className="text-sm font-bold text-slate-900">
                      Sentiment Distribution
                    </h3>
                    <p className="text-xs text-slate-500">
                      Distribution of positive, neutral, and negative coverage
                    </p>
                  </div>

                  <div className="h-64 w-full flex items-center justify-center">
                    <ResponsiveContainer width="100%" height="100%">
                      <PieChart>
                        <Pie
                          data={data.sentiment_overview.distribution}
                          dataKey="value"
                          nameKey="name"
                          cx="50%"
                          cy="50%"
                          innerRadius={60}
                          outerRadius={85}
                          paddingAngle={4}
                        >
                          {data.sentiment_overview.distribution.map((entry, index) => (
                            <Cell
                              key={`cell-${index}`}
                              fill={PIE_COLORS[entry.name as keyof typeof PIE_COLORS] || "#64748b"}
                            />
                          ))}
                        </Pie>
                        <RechartsTooltip
                          formatter={(val: any, name: any) => [`${val} Articles`, name]}
                        />
                        <Legend />
                      </PieChart>
                    </ResponsiveContainer>
                  </div>
                </div>

                {/* Line Chart: Sentiment Trend */}
                <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-xs space-y-4">
                  <div>
                    <h3 className="text-sm font-bold text-slate-900">
                      Sentiment Trend
                    </h3>
                    <p className="text-xs text-slate-500">
                      Chronological progression (+1.0 Positive, 0.0 Neutral, -1.0 Negative)
                    </p>
                  </div>

                  <div className="h-64 w-full">
                    <ResponsiveContainer width="100%" height="100%">
                      <LineChart data={data.sentiment_trend}>
                        <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                        <XAxis dataKey="date" tick={{ fontSize: 10 }} stroke="#94a3b8" />
                        <YAxis
                          domain={[-1.2, 1.2]}
                          ticks={[-1, 0, 1]}
                          tickFormatter={(val) => (val === 1 ? "Pos" : val === -1 ? "Neg" : "Neu")}
                          tick={{ fontSize: 10 }}
                          stroke="#94a3b8"
                        />
                        <RechartsTooltip
                          formatter={(val: any) => [
                            val === 1 ? "Positive (+1.0)" : val === -1 ? "Negative (-1.0)" : "Neutral (0.0)",
                            "Score"
                          ]}
                          labelFormatter={(label) => `Date: ${label}`}
                        />
                        <Line
                          type="monotone"
                          dataKey="score"
                          stroke="#2563eb"
                          strokeWidth={2.5}
                          dot={{ r: 4, fill: "#2563eb" }}
                          activeDot={{ r: 6 }}
                        />
                      </LineChart>
                    </ResponsiveContainer>
                  </div>
                </div>
              </div>

              {/* Topics & Keywords & Risks */}
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {/* Top Discussed Topics Bar Chart */}
                <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-xs space-y-4">
                  <div>
                    <h3 className="text-sm font-bold text-slate-900">
                      Most Discussed Topics
                    </h3>
                    <p className="text-xs text-slate-500">
                      Occurrence frequency across analyzed texts
                    </p>
                  </div>

                  <div className="h-56 w-full">
                    <ResponsiveContainer width="100%" height="100%">
                      <BarChart
                        data={data.top_topics}
                        layout="vertical"
                        margin={{ top: 5, right: 10, left: 20, bottom: 5 }}
                      >
                        <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="#f1f5f9" />
                        <XAxis type="number" tick={{ fontSize: 10 }} stroke="#94a3b8" />
                        <YAxis
                          type="category"
                          dataKey="topic"
                          tick={{ fontSize: 10 }}
                          width={100}
                          stroke="#94a3b8"
                        />
                        <RechartsTooltip />
                        <Bar dataKey="count" fill="#3b82f6" radius={[0, 4, 4, 0]} />
                      </BarChart>
                    </ResponsiveContainer>
                  </div>
                </div>

                {/* Major Keywords */}
                <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-xs space-y-4">
                  <div>
                    <h3 className="text-sm font-bold text-slate-900">
                      Major Financial Keywords
                    </h3>
                    <p className="text-xs text-slate-500">
                      TF-IDF weighted domain keywords
                    </p>
                  </div>

                  <div className="flex flex-wrap gap-2 pt-2">
                    {data.keywords.map((kw, i) => (
                      <span
                        key={i}
                        className="px-2.5 py-1 rounded-md bg-slate-100 text-slate-800 text-xs font-medium border border-slate-200 flex items-center gap-1.5 shadow-2xs"
                      >
                        <Tag className="w-3 h-3 text-slate-400" />
                        <span>{kw.keyword}</span>
                        <span className="text-[10px] text-slate-400 font-mono">({kw.score})</span>
                      </span>
                    ))}
                  </div>
                </div>

                {/* NLP-Derived Risk Indicators */}
                <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-xs space-y-4">
                  <div>
                    <h3 className="text-sm font-bold text-slate-900">
                      NLP-Derived Risk Indicators
                    </h3>
                    <p className="text-xs text-slate-500">
                      Risk indicators identified from news narratives
                    </p>
                  </div>

                  <div className="space-y-2 pt-2">
                    {data.risk_indicators.length > 0 ? (
                      data.risk_indicators.map((risk, i) => (
                        <div
                          key={i}
                          className="p-2.5 rounded-lg bg-amber-50 border border-amber-200 text-xs font-semibold text-amber-900 flex items-center gap-2"
                        >
                          <ShieldAlert className="w-4 h-4 text-amber-600 shrink-0" />
                          <span>{risk}</span>
                        </div>
                      ))
                    ) : (
                      <span className="text-xs text-slate-400 italic">No elevated risks flagged.</span>
                    )}
                  </div>
                </div>
              </div>

              {/* Analyzed Financial Articles / Text */}
              <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-xs space-y-4">
                <div className="flex items-center justify-between pb-3 border-b border-slate-100">
                  <h3 className="text-sm font-bold text-slate-900">
                    Recent Analyzed Financial Content ({data.article_count} items)
                  </h3>
                  <span className="text-xs text-slate-500 font-mono">
                    Source: {data.news_source}
                  </span>
                </div>

                <div className="divide-y divide-slate-100">
                  {data.articles.map((art) => (
                    <div key={art.article_id} className="py-3.5 space-y-1.5">
                      <div className="flex flex-wrap items-center justify-between gap-2">
                        <span className="text-xs font-bold text-slate-900">
                          {art.headline}
                        </span>
                        <div className="flex items-center gap-2 font-mono text-[11px]">
                          <span className="text-slate-500">{art.source}</span>
                          <span className="text-slate-300">•</span>
                          <span className="text-slate-500">{art.date}</span>
                          <span className={`px-2 py-0.5 rounded font-bold ${
                            art.sentiment === "Positive"
                              ? "bg-emerald-50 text-emerald-700 border border-emerald-200"
                              : art.sentiment === "Negative"
                              ? "bg-rose-50 text-rose-700 border border-rose-200"
                              : "bg-slate-100 text-slate-700 border border-slate-200"
                          }`}>
                            {art.sentiment} ({art.confidence}%)
                          </span>
                        </div>
                      </div>

                      <p className="text-xs text-slate-600 leading-relaxed font-sans">
                        {art.text}
                      </p>

                      <div className="flex flex-wrap items-center gap-2 pt-1 text-[11px]">
                        {art.topics.map((t, idx) => (
                          <span key={idx} className="px-2 py-0.5 rounded bg-blue-50 text-blue-700 border border-blue-200">
                            {t}
                          </span>
                        ))}
                        {art.risks.map((r, idx) => (
                          <span key={idx} className="px-2 py-0.5 rounded bg-amber-50 text-amber-800 border border-amber-200">
                            Risk: {r}
                          </span>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </>
          )}
        </div>
      ) : null}
    </div>
  );
}

export default function CompanyAnalysisPage() {
  return (
    <Suspense fallback={
      <div className="py-20 text-center text-xs text-slate-400 font-mono">
        Loading Company Analysis...
      </div>
    }>
      <CompanyAnalysisContent />
    </Suspense>
  );
}
