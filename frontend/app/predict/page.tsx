"use client";

import { useState, useEffect, Suspense } from "react";
import { useSearchParams } from "next/navigation";
import { 
  runPrediction, 
  PredictionResponse, 
  getSavedCompany, 
  saveCompany 
} from "@/lib/api";
import CompanySearch from "@/components/CompanySearch";
import { 
  TrendingUp, 
  BrainCircuit, 
  AlertTriangle, 
  Sparkles, 
  Layers, 
  Clock,
  AlertCircle
} from "lucide-react";
import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip as RechartsTooltip,
  Legend
} from "recharts";

function PredictionContent() {
  const searchParams = useSearchParams();
  const [selectedCompany, setSelectedCompany] = useState<string>("NVIDIA");
  const [lookback, setLookback] = useState<number>(20);
  const [prediction, setPrediction] = useState<PredictionResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const paramCompany = searchParams?.get("company");
    if (paramCompany) {
      setSelectedCompany(paramCompany);
      executePrediction(paramCompany, lookback);
    } else {
      const saved = getSavedCompany();
      setSelectedCompany(saved);
      executePrediction(saved, lookback);
    }
  }, [searchParams]);

  const executePrediction = async (companyQuery: string, lookbackWindow: number) => {
    if (!companyQuery.trim()) return;
    setLoading(true);
    setError(null);
    saveCompany(companyQuery);
    setSelectedCompany(companyQuery);

    try {
      const res = await runPrediction(companyQuery, lookbackWindow);
      setPrediction(res);
    } catch (err: any) {
      setError(err.message || "Failed to generate time-series prediction.");
      setPrediction(null);
    } finally {
      setLoading(false);
    }
  };

  const handleLookbackChange = (newLookback: number) => {
    setLookback(newLookback);
    executePrediction(selectedCompany, newLookback);
  };

  return (
    <div className="space-y-8 pb-12">
      {/* Page Title */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-purple-50 border border-purple-200 text-purple-800 text-xs font-semibold mb-2">
            <BrainCircuit className="w-3.5 h-3.5" />
            <span>Time-Series Predictive Analytics</span>
          </div>
          <h1 className="text-2xl font-extrabold text-slate-900 tracking-tight">
            LSTM Price Forecasting
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            Recurrent Neural Network sequential price regression evaluated on holdout test partitions.
          </p>
        </div>

        {/* Lookback Window Selector */}
        <div className="flex items-center gap-2 text-xs">
          <label htmlFor="lookbackSelect" className="font-bold text-slate-600">
            Lookback Window:
          </label>
          <select
            id="lookbackSelect"
            value={lookback}
            onChange={(e) => handleLookbackChange(Number(e.target.value))}
            className="text-xs font-semibold bg-white border border-slate-300 rounded-lg px-3 py-1.5 text-slate-900 shadow-2xs focus:outline-hidden focus:ring-2 focus:ring-blue-500"
          >
            <option value={15}>15 Trading Days</option>
            <option value={20}>20 Trading Days</option>
            <option value={30}>30 Trading Days</option>
          </select>
        </div>
      </div>

      {/* Dynamic Company Search (Requirement 17) */}
      <CompanySearch
        initialValue={selectedCompany}
        onSearch={(q) => executePrediction(q, lookback)}
        loading={loading}
        placeholder="Enter company or stock ticker for LSTM forecasting (e.g. AAPL, TSLA, NVDA, GOOGL)..."
        buttonText="Generate Prediction"
      />

      {/* Experimental Disclaimer (Requirement 21) */}
      <div className="p-3.5 rounded-lg bg-amber-50 border border-amber-200 text-xs text-amber-900 flex items-start gap-2.5">
        <AlertTriangle className="w-4 h-4 text-amber-600 shrink-0 mt-0.5" />
        <div>
          <span className="font-bold">Analytical Disclaimer: </span>
          <span>
            Historical price prediction is experimental and does not guarantee future market performance.
            Intended strictly for quantitative time-series pattern analysis and error validation.
          </span>
        </div>
      </div>

      {loading ? (
        <div className="py-20 text-center space-y-3 bg-white rounded-xl border border-slate-200 shadow-xs">
          <div className="w-6 h-6 border-2 border-purple-600 border-t-transparent rounded-full animate-spin mx-auto" />
          <p className="text-xs text-slate-500 font-mono">
            Retrieving price series, generating sequence tensors, and fitting LSTM model for {selectedCompany}...
          </p>
        </div>
      ) : error ? (
        <div className="p-4 bg-rose-50 border border-rose-200 rounded-lg text-xs text-rose-700 flex items-center gap-2">
          <AlertCircle className="w-4 h-4 text-rose-600 shrink-0" />
          <span>{error}</span>
        </div>
      ) : prediction ? (
        <div className="space-y-6">
          {/* Header with Asset & Source Info */}
          <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs flex flex-wrap items-center justify-between gap-3 text-xs">
            <div className="flex items-center gap-2 font-bold text-slate-900 text-sm">
              <span>{prediction.company}</span>
              <span className="text-slate-500 font-mono text-xs">({prediction.ticker})</span>
            </div>
            <div className="flex items-center gap-2 font-mono text-xs">
              <span className="px-2 py-0.5 rounded bg-slate-100 text-slate-700 border border-slate-200">
                Source: {prediction.data_source}
              </span>
              <span className="px-2 py-0.5 rounded bg-purple-50 text-purple-800 border border-purple-200">
                Partition: {prediction.dataset_info.split_ratio}
              </span>
            </div>
          </div>

          {/* Authentic Metrics Cards (Requirement 20) */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {/* MAE */}
            <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs">
              <span className="text-[10px] font-semibold text-slate-500 uppercase tracking-wider block mb-1">
                Mean Absolute Error (MAE)
              </span>
              <div className="text-2xl font-extrabold text-slate-900 font-mono">
                {prediction.metrics.mae}
              </div>
              <p className="text-[11px] text-slate-400 font-sans mt-0.5">
                Mean absolute price deviation
              </p>
            </div>

            {/* RMSE */}
            <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs">
              <span className="text-[10px] font-semibold text-slate-500 uppercase tracking-wider block mb-1">
                Root Mean Squared Error (RMSE)
              </span>
              <div className="text-2xl font-extrabold text-slate-900 font-mono">
                {prediction.metrics.rmse}
              </div>
              <p className="text-[11px] text-slate-400 font-sans mt-0.5">
                Quadratic penalty on outliers
              </p>
            </div>

            {/* MAPE */}
            <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs">
              <span className="text-[10px] font-semibold text-slate-500 uppercase tracking-wider block mb-1">
                Percentage Error (MAPE)
              </span>
              <div className="text-2xl font-extrabold text-purple-700 font-mono">
                {prediction.metrics.mape}%
              </div>
              <p className="text-[11px] text-slate-400 font-sans mt-0.5">
                Scale-independent relative error
              </p>
            </div>

            {/* Directional Accuracy */}
            <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs">
              <span className="text-[10px] font-semibold text-slate-500 uppercase tracking-wider block mb-1">
                Directional Accuracy
              </span>
              <div className="text-2xl font-extrabold text-emerald-700 font-mono">
                {prediction.metrics.directional_accuracy}%
              </div>
              <p className="text-[11px] text-slate-400 font-sans mt-0.5">
                Correct up/down movement forecast
              </p>
            </div>
          </div>

          {/* Actual vs Predicted Line Chart */}
          <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-xs space-y-4">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-slate-100">
              <div>
                <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
                  <span>Historical vs LSTM Predicted Price</span>
                  <span className="text-xs font-mono text-slate-400">({prediction.ticker})</span>
                </h3>
                <p className="text-xs text-slate-500">
                  Model evaluated on holdout test partition ({prediction.dataset_info.test_samples} trading days)
                </p>
              </div>
            </div>

            <div className="h-80 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={prediction.chart_data}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                  <XAxis dataKey="date" tick={{ fontSize: 10 }} stroke="#94a3b8" />
                  <YAxis
                    domain={["auto", "auto"]}
                    tick={{ fontSize: 10 }}
                    stroke="#94a3b8"
                  />
                  <RechartsTooltip
                    formatter={(val: any, name: any) => [
                      val !== null ? `${val}` : "N/A",
                      name === "actual" ? "Actual Close" : "LSTM Predicted"
                    ]}
                  />
                  <Legend />
                  <Line
                    type="monotone"
                    dataKey="actual"
                    name="Actual Close"
                    stroke="#0f172a"
                    strokeWidth={2}
                    dot={false}
                  />
                  <Line
                    type="monotone"
                    dataKey="predicted"
                    name="LSTM Predicted (Test Split)"
                    stroke="#8b5cf6"
                    strokeWidth={2}
                    dot={{ r: 3, fill: "#8b5cf6" }}
                    strokeDasharray="3 3"
                    connectNulls={false}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Autoregressive 5-Day Forecast & Model Architecture */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Future 5-Day Forecast */}
            <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-xs space-y-3">
              <div className="flex items-center justify-between pb-2 border-b border-slate-100">
                <span className="text-xs font-bold uppercase tracking-wider text-slate-700 flex items-center gap-1.5">
                  <Clock className="w-3.5 h-3.5 text-purple-600" />
                  <span>Experimental 5-Day Projection</span>
                </span>
                <span className="text-[10px] font-mono text-purple-700 bg-purple-50 px-2 py-0.5 rounded border border-purple-200">
                  Recursive Sequence
                </span>
              </div>
              <p className="text-xs text-slate-500 leading-relaxed">
                Projected price progression computed autoregressively from the most recent sequence:
              </p>
              <div className="grid grid-cols-5 gap-2 pt-1 font-mono text-center">
                {prediction.future_forecast.map((val, idx) => (
                  <div key={idx} className="p-2.5 rounded-lg bg-slate-50 border border-slate-200">
                    <div className="text-[10px] text-slate-400 font-sans">T+{idx + 1}</div>
                    <div className="text-xs font-bold text-slate-900 mt-0.5">{val}</div>
                  </div>
                ))}
              </div>
            </div>

            {/* Architecture Explanations */}
            <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-xs space-y-3">
              <div className="flex items-center justify-between pb-2 border-b border-slate-100">
                <span className="text-xs font-bold uppercase tracking-wider text-slate-700 flex items-center gap-1.5">
                  <Layers className="w-3.5 h-3.5 text-blue-600" />
                  <span>LSTM Architecture Specification</span>
                </span>
                <span className="text-[10px] font-mono text-slate-400">
                  Sequential Topology
                </span>
              </div>
              <div className="space-y-1.5 text-xs">
                {prediction.model_architecture.layers.map((layer, idx) => (
                  <div key={idx} className="flex items-center justify-between p-2 rounded bg-slate-50 border border-slate-200">
                    <span className="font-semibold text-slate-800">{layer.name}</span>
                    <span className="text-[11px] font-mono text-slate-500">{layer.type}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      ) : null}
    </div>
  );
}

export default function PredictionPage() {
  return (
    <Suspense fallback={
      <div className="py-20 text-center text-xs text-slate-400 font-mono">
        Loading Predictive Analytics...
      </div>
    }>
      <PredictionContent />
    </Suspense>
  );
}
