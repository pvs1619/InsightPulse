"use client";

import { useState, useEffect, Suspense } from "react";
import { useSearchParams } from "next/navigation";
import { 
  getMarketData, 
  MarketDataResponse, 
  getSavedCompany, 
  saveCompany 
} from "@/lib/api";
import CompanySearch from "@/components/CompanySearch";
import { 
  LineChart as LineChartIcon, 
  TrendingUp, 
  TrendingDown, 
  Database, 
  Activity, 
  AlertCircle,
  Calendar
} from "lucide-react";
import {
  ResponsiveContainer,
  ComposedChart,
  Line,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip as RechartsTooltip,
  Legend
} from "recharts";

const TIME_RANGES = [
  { label: "1 Month", value: "1mo" },
  { label: "3 Months", value: "3mo" },
  { label: "6 Months", value: "6mo" },
  { label: "1 Year", value: "1y" },
  { label: "5 Years", value: "5y" }
];

function MarketAnalysisContent() {
  const searchParams = useSearchParams();
  const [selectedCompany, setSelectedCompany] = useState<string>("NVIDIA");
  const [selectedPeriod, setSelectedPeriod] = useState<string>("1y");
  const [marketData, setMarketData] = useState<MarketDataResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<"price" | "volume">("price");

  useEffect(() => {
    const paramCompany = searchParams?.get("company");
    if (paramCompany) {
      setSelectedCompany(paramCompany);
      fetchMarket(paramCompany, selectedPeriod);
    } else {
      const saved = getSavedCompany();
      setSelectedCompany(saved);
      fetchMarket(saved, selectedPeriod);
    }
  }, [searchParams]);

  const fetchMarket = async (query: string, period: string) => {
    if (!query.trim()) return;
    setLoading(true);
    setError(null);
    saveCompany(query);
    setSelectedCompany(query);

    try {
      const res = await getMarketData(query, period);
      setMarketData(res);
    } catch (err: any) {
      setError(err.message || "Failed to retrieve market data.");
      setMarketData(null);
    } finally {
      setLoading(false);
    }
  };

  const handlePeriodChange = (period: string) => {
    setSelectedPeriod(period);
    fetchMarket(selectedCompany, period);
  };

  return (
    <div className="space-y-8 pb-12">
      {/* Title */}
      <div>
        <div className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-emerald-50 border border-emerald-200 text-emerald-800 text-xs font-semibold mb-2">
          <LineChartIcon className="w-3.5 h-3.5" />
          <span>Market Analytics & Technical Overlays</span>
        </div>
        <h1 className="text-2xl font-extrabold text-slate-900 tracking-tight">
          Market Analysis
        </h1>
        <p className="text-xs text-slate-500 mt-1">
          Historical price charts, 20-day & 50-day Simple Moving Averages, trading volumes, and annualized price volatility.
        </p>
      </div>

      {/* Dynamic Company Search (Requirement 15) */}
      <CompanySearch
        initialValue={selectedCompany}
        onSearch={(q) => fetchMarket(q, selectedPeriod)}
        loading={loading}
        placeholder="Enter company name or ticker (e.g., TSLA, Apple, GOOGL, Microsoft, TCS.NS)..."
        buttonText="Analyze Market"
      />

      {loading ? (
        <div className="py-20 text-center space-y-3 bg-white rounded-xl border border-slate-200 shadow-xs">
          <div className="w-6 h-6 border-2 border-emerald-600 border-t-transparent rounded-full animate-spin mx-auto" />
          <p className="text-xs text-slate-500 font-mono">
            Fetching technical indicators and historical price series for {selectedCompany}...
          </p>
        </div>
      ) : error ? (
        <div className="p-4 bg-rose-50 border border-rose-200 rounded-lg text-xs text-rose-700 flex items-center gap-2">
          <AlertCircle className="w-4 h-4 text-rose-600 shrink-0" />
          <span>{error}</span>
        </div>
      ) : marketData ? (
        <div className="space-y-6">
          {/* Prominent Header Banner (Requirement 16) */}
          <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-xs flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div>
              <div className="flex items-center gap-2.5">
                <h2 className="text-xl font-bold text-slate-900 tracking-tight">
                  {marketData.company} — {marketData.ticker}
                </h2>
              </div>
              <div className="flex items-center gap-2 mt-1 text-xs">
                <span className="font-semibold text-slate-700">Data Source:</span>
                <span className={`px-2 py-0.5 rounded font-mono font-bold ${
                  marketData.data_source === "Live Market Data"
                    ? "bg-emerald-100 text-emerald-900 border border-emerald-300"
                    : "bg-slate-100 text-slate-800 border border-slate-200"
                }`}>
                  {marketData.data_source}
                </span>
                <span className="text-slate-400 font-mono text-[11px]">
                  ({marketData.history.length} Data Points)
                </span>
              </div>
            </div>

            {/* Time Range Selector Buttons (Requirement 16) */}
            <div className="flex items-center gap-1.5 p-1 bg-slate-100 rounded-lg text-xs font-medium">
              {TIME_RANGES.map((r) => (
                <button
                  key={r.value}
                  type="button"
                  onClick={() => handlePeriodChange(r.value)}
                  className={`px-3 py-1 rounded-md transition-colors ${
                    selectedPeriod === r.value
                      ? "bg-white text-slate-900 font-bold shadow-2xs"
                      : "text-slate-600 hover:text-slate-900"
                  }`}
                >
                  {r.label}
                </button>
              ))}
            </div>
          </div>

          {/* Metric Cards Row */}
          <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
            {/* Stat 1: Close Price */}
            <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs">
              <span className="text-[10px] font-semibold text-slate-500 uppercase tracking-wider block mb-1">
                Latest Close
              </span>
              <div className="text-2xl font-extrabold text-slate-900 font-mono">
                {marketData.currency}{marketData.summary.latest_close}
              </div>
              <div className="text-[11px] text-slate-400 font-mono mt-0.5">
                Prev: {marketData.currency}{marketData.summary.previous_close}
              </div>
            </div>

            {/* Stat 2: Daily Change */}
            <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs">
              <span className="text-[10px] font-semibold text-slate-500 uppercase tracking-wider block mb-1">
                Daily Change
              </span>
              <div className={`text-2xl font-extrabold font-mono flex items-center gap-1 ${
                marketData.summary.percent_change >= 0 ? "text-emerald-700" : "text-rose-700"
              }`}>
                {marketData.summary.percent_change >= 0 ? (
                  <TrendingUp className="w-5 h-5" />
                ) : (
                  <TrendingDown className="w-5 h-5" />
                )}
                <span>
                  {marketData.summary.percent_change >= 0 ? "+" : ""}{marketData.summary.percent_change}%
                </span>
              </div>
              <div className="text-[11px] text-slate-500 font-mono mt-0.5">
                {marketData.summary.change >= 0 ? "+" : ""}{marketData.currency}{marketData.summary.change}
              </div>
            </div>

            {/* Stat 3: Volatility */}
            <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs">
              <span className="text-[10px] font-semibold text-slate-500 uppercase tracking-wider block mb-1">
                Annualized Volatility
              </span>
              <div className="text-2xl font-extrabold text-slate-800 font-mono">
                {marketData.summary.volatility_annualized}%
              </div>
              <div className="text-[11px] text-slate-400 font-mono mt-0.5">
                Std. Dev. of Log Returns
              </div>
            </div>

            {/* Stat 4: Day High / Low */}
            <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs">
              <span className="text-[10px] font-semibold text-slate-500 uppercase tracking-wider block mb-1">
                Day Range
              </span>
              <div className="text-sm font-bold text-slate-900 font-mono">
                H: {marketData.currency}{marketData.summary.day_high}
              </div>
              <div className="text-sm font-bold text-slate-600 font-mono">
                L: {marketData.currency}{marketData.summary.day_low}
              </div>
            </div>

            {/* Stat 5: 52-Week Range */}
            <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs col-span-2 md:col-span-1">
              <span className="text-[10px] font-semibold text-slate-500 uppercase tracking-wider block mb-1">
                52-Week Range
              </span>
              <div className="text-sm font-bold text-slate-900 font-mono">
                H: {marketData.currency}{marketData.summary.high_52w}
              </div>
              <div className="text-sm font-bold text-slate-600 font-mono">
                L: {marketData.currency}{marketData.summary.low_52w}
              </div>
            </div>
          </div>

          {/* Interactive Chart Container */}
          <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-xs space-y-4">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-slate-100">
              <div>
                <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
                  <span>Price History & Moving Averages</span>
                  <span className="text-xs font-mono text-slate-400">({marketData.ticker})</span>
                </h3>
                <p className="text-xs text-slate-500">
                  Daily Closing Price with SMA-20 (Blue) & SMA-50 (Amber)
                </p>
              </div>

              {/* View Switcher Tabs */}
              <div className="flex items-center gap-1.5 p-1 bg-slate-100 rounded-lg text-xs font-medium">
                <button
                  type="button"
                  onClick={() => setActiveTab("price")}
                  className={`px-3 py-1 rounded-md transition-colors ${
                    activeTab === "price"
                      ? "bg-white text-slate-900 font-bold shadow-2xs"
                      : "text-slate-600 hover:text-slate-900"
                  }`}
                >
                  Price & MAs
                </button>
                <button
                  type="button"
                  onClick={() => setActiveTab("volume")}
                  className={`px-3 py-1 rounded-md transition-colors ${
                    activeTab === "volume"
                      ? "bg-white text-slate-900 font-bold shadow-2xs"
                      : "text-slate-600 hover:text-slate-900"
                  }`}
                >
                  Trading Volume
                </button>
              </div>
            </div>

            {/* Recharts Composed Chart */}
            <div className="h-80 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <ComposedChart data={marketData.history}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                  <XAxis dataKey="date" tick={{ fontSize: 10 }} stroke="#94a3b8" />
                  <YAxis
                    yAxisId="price"
                    domain={["auto", "auto"]}
                    tick={{ fontSize: 10 }}
                    stroke="#94a3b8"
                    tickFormatter={(val) => `${marketData.currency}${val}`}
                  />
                  {activeTab === "volume" && (
                    <YAxis
                      yAxisId="volume"
                      orientation="right"
                      domain={["auto", "auto"]}
                      tick={{ fontSize: 10 }}
                      stroke="#94a3b8"
                      tickFormatter={(val) => `${(val / 1000000).toFixed(1)}M`}
                    />
                  )}
                  <RechartsTooltip
                    formatter={(val: any, name: any) => [
                      name === "volume" ? `${Number(val).toLocaleString()} shares` : `${marketData.currency}${val}`,
                      name === "close" ? "Close Price" : name === "sma20" ? "SMA 20" : name === "sma50" ? "SMA 50" : name
                    ]}
                  />
                  <Legend />

                  {/* Price Line */}
                  <Line
                    yAxisId="price"
                    type="monotone"
                    dataKey="close"
                    name="Close"
                    stroke="#0f172a"
                    strokeWidth={2}
                    dot={false}
                  />

                  {/* 20-Day Simple Moving Average */}
                  <Line
                    yAxisId="price"
                    type="monotone"
                    dataKey="sma20"
                    name="SMA 20"
                    stroke="#2563eb"
                    strokeWidth={1.5}
                    strokeDasharray="4 4"
                    dot={false}
                  />

                  {/* 50-Day Simple Moving Average */}
                  <Line
                    yAxisId="price"
                    type="monotone"
                    dataKey="sma50"
                    name="SMA 50"
                    stroke="#f59e0b"
                    strokeWidth={1.5}
                    strokeDasharray="2 2"
                    dot={false}
                  />

                  {/* Volume Bars */}
                  {activeTab === "volume" && (
                    <Bar
                      yAxisId="volume"
                      dataKey="volume"
                      name="Volume"
                      fill="#cbd5e1"
                      opacity={0.6}
                    />
                  )}
                </ComposedChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>
      ) : null}
    </div>
  );
}

export default function MarketAnalysisPage() {
  return (
    <Suspense fallback={
      <div className="py-20 text-center text-xs text-slate-400 font-mono">
        Loading Market Analysis...
      </div>
    }>
      <MarketAnalysisContent />
    </Suspense>
  );
}
