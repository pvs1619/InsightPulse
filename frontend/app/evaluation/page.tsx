"use client";

import { useState, useEffect } from "react";
import { getEvaluation, EvaluationResponse } from "@/lib/api";
import { 
  CheckCircle2, 
  Cpu, 
  TrendingUp, 
  HelpCircle, 
  Award, 
  Layers, 
  Info,
  ShieldCheck
} from "lucide-react";

export default function ModelEvaluationPage() {
  const [evaluation, setEvaluation] = useState<EvaluationResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getEvaluation()
      .then((data) => setEvaluation(data))
      .catch((err: any) => setError(err.message || "Failed to load model evaluation metrics"))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="space-y-8 pb-12">
      {/* Title */}
      <div>
        <div className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-blue-50 border border-blue-200 text-blue-700 text-xs font-semibold mb-2">
          <Award className="w-3.5 h-3.5" />
          <span>Model Benchmark Analysis</span>
        </div>
        <h1 className="text-2xl font-extrabold text-slate-900 tracking-tight">
          Model Evaluation & Performance Benchmarks
        </h1>
        <p className="text-xs text-slate-500 mt-1">
          Comparative empirical evaluation between statistical baseline models and domain-specific financial architectures.
        </p>
      </div>

      {/* Benchmark Transparency Notice (Requirement 23) */}
      <div className="p-3.5 rounded-lg bg-slate-100 border border-slate-200 text-xs text-slate-700 flex items-start gap-2.5">
        <Info className="w-4 h-4 text-blue-600 shrink-0 mt-0.5" />
        <div>
          <span className="font-bold text-slate-900">Standardized Benchmark Datasets: </span>
          <span>
            These evaluation metrics represent standardized model benchmark tests performed on holdout validation partitions.
            To view ad-hoc performance for a specific company or stock ticker, visit the <strong>Company Analysis</strong> or <strong>Predictive Analytics</strong> modules.
          </span>
        </div>
      </div>

      {loading ? (
        <div className="py-20 text-center space-y-3 bg-white rounded-xl border border-slate-200 shadow-xs">
          <div className="w-6 h-6 border-2 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto" />
          <p className="text-xs text-slate-500 font-mono">
            Evaluating TF-IDF baseline and financial sentiment models on holdout test partition...
          </p>
        </div>
      ) : error ? (
        <div className="p-4 bg-rose-50 border border-rose-200 rounded-lg text-xs text-rose-700">
          {error}
        </div>
      ) : evaluation ? (
        <div className="space-y-10">
          {/* ============================================================== */}
          {/* SECTION 1: NLP MODEL EVALUATION */}
          {/* ============================================================== */}
          <section className="space-y-5">
            <div className="flex items-center justify-between pb-2 border-b border-slate-200">
              <div>
                <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
                  <Cpu className="w-4 h-4 text-blue-600" />
                  <span>Financial NLP Model Benchmark</span>
                </h2>
                <p className="text-xs text-slate-500">
                  Holdout Validation: Baseline (TF-IDF + Logistic Regression) vs Financial Domain Model
                </p>
              </div>
              <span className="text-[11px] font-mono text-slate-600 bg-slate-100 px-2 py-0.5 rounded border border-slate-200">
                {evaluation.nlp_evaluation.test_sample_count} Test Articles Evaluated
              </span>
            </div>

            {/* Comparison Table */}
            <div className="bg-white rounded-xl border border-slate-200 overflow-hidden shadow-xs">
              <div className="overflow-x-auto">
                <table className="w-full text-left text-xs">
                  <thead className="bg-slate-50 border-b border-slate-200 text-slate-600 font-semibold">
                    <tr>
                      <th className="px-5 py-3">Model Architecture</th>
                      <th className="px-4 py-3">Approach Type</th>
                      <th className="px-4 py-3 text-right">Accuracy</th>
                      <th className="px-4 py-3 text-right">Precision</th>
                      <th className="px-4 py-3 text-right">Recall</th>
                      <th className="px-4 py-3 text-right font-bold text-slate-900">F1-Score</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {/* Baseline */}
                    <tr className="hover:bg-slate-50/60 transition-colors">
                      <td className="px-5 py-3 font-semibold text-slate-800">
                        {evaluation.nlp_evaluation.baseline.name}
                      </td>
                      <td className="px-4 py-3 text-slate-500 font-mono text-[11px]">
                        {evaluation.nlp_evaluation.baseline.type}
                      </td>
                      <td className="px-4 py-3 text-right font-mono text-slate-700">
                        {evaluation.nlp_evaluation.baseline.accuracy}%
                      </td>
                      <td className="px-4 py-3 text-right font-mono text-slate-700">
                        {evaluation.nlp_evaluation.baseline.precision}%
                      </td>
                      <td className="px-4 py-3 text-right font-mono text-slate-700">
                        {evaluation.nlp_evaluation.baseline.recall}%
                      </td>
                      <td className="px-4 py-3 text-right font-mono font-bold text-slate-800">
                        {evaluation.nlp_evaluation.baseline.f1_score}%
                      </td>
                    </tr>

                    {/* Financial Model */}
                    <tr className="bg-blue-50/40 hover:bg-blue-50/60 transition-colors">
                      <td className="px-5 py-3 font-bold text-blue-900 flex items-center gap-1.5">
                        <CheckCircle2 className="w-3.5 h-3.5 text-blue-600 shrink-0" />
                        <span>{evaluation.nlp_evaluation.financial_model.name}</span>
                      </td>
                      <td className="px-4 py-3 text-blue-700 font-mono text-[11px]">
                        {evaluation.nlp_evaluation.financial_model.type}
                      </td>
                      <td className="px-4 py-3 text-right font-mono font-semibold text-blue-900">
                        {evaluation.nlp_evaluation.financial_model.accuracy}%
                      </td>
                      <td className="px-4 py-3 text-right font-mono font-semibold text-blue-900">
                        {evaluation.nlp_evaluation.financial_model.precision}%
                      </td>
                      <td className="px-4 py-3 text-right font-mono font-semibold text-blue-900">
                        {evaluation.nlp_evaluation.financial_model.recall}%
                      </td>
                      <td className="px-4 py-3 text-right font-mono font-extrabold text-blue-800 text-sm">
                        {evaluation.nlp_evaluation.financial_model.f1_score}%
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>

              {/* Analytical comparative commentary */}
              <div className="p-4 bg-slate-50 border-t border-slate-200 text-xs text-slate-700 leading-relaxed">
                <span className="font-bold text-slate-900">Comparative Performance Finding: </span>
                {evaluation.nlp_evaluation.analysis}
              </div>
            </div>

            {/* Confusion Matrices */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 pt-2">
              {/* Baseline CM */}
              <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-xs space-y-3">
                <div className="flex items-center justify-between pb-2 border-b border-slate-100">
                  <span className="text-xs font-bold text-slate-800">
                    Baseline Confusion Matrix
                  </span>
                  <span className="text-[10px] font-mono text-slate-400">
                    TF-IDF + Logistic Regression
                  </span>
                </div>
                <div className="overflow-x-auto">
                  <table className="w-full text-center text-xs font-mono">
                    <thead>
                      <tr className="text-slate-400 text-[10px]">
                        <th></th>
                        {evaluation.nlp_evaluation.classes.map((c) => (
                          <th key={c} className="p-1 font-semibold text-slate-600">Pred {c}</th>
                        ))}
                      </tr>
                    </thead>
                    <tbody>
                      {evaluation.nlp_evaluation.baseline.confusion_matrix.map((row, rIdx) => (
                        <tr key={rIdx}>
                          <td className="text-left font-semibold text-slate-600 text-[11px] pr-2">
                            True {evaluation.nlp_evaluation.classes[rIdx]}
                          </td>
                          {row.map((cell, cIdx) => (
                            <td
                              key={cIdx}
                              className={`p-2 rounded border m-0.5 ${
                                rIdx === cIdx
                                  ? "bg-slate-200 font-bold text-slate-900 border-slate-300"
                                  : "bg-slate-50 text-slate-500 border-slate-100"
                              }`}
                            >
                              {cell}
                            </td>
                          ))}
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>

              {/* Financial Model CM */}
              <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-xs space-y-3">
                <div className="flex items-center justify-between pb-2 border-b border-slate-100">
                  <span className="text-xs font-bold text-blue-900">
                    Financial Model Confusion Matrix
                  </span>
                  <span className="text-[10px] font-mono text-blue-600">
                    Domain Calibrated
                  </span>
                </div>
                <div className="overflow-x-auto">
                  <table className="w-full text-center text-xs font-mono">
                    <thead>
                      <tr className="text-slate-400 text-[10px]">
                        <th></th>
                        {evaluation.nlp_evaluation.classes.map((c) => (
                          <th key={c} className="p-1 font-semibold text-blue-800">Pred {c}</th>
                        ))}
                      </tr>
                    </thead>
                    <tbody>
                      {evaluation.nlp_evaluation.financial_model.confusion_matrix.map((row, rIdx) => (
                        <tr key={rIdx}>
                          <td className="text-left font-semibold text-slate-600 text-[11px] pr-2">
                            True {evaluation.nlp_evaluation.classes[rIdx]}
                          </td>
                          {row.map((cell, cIdx) => (
                            <td
                              key={cIdx}
                              className={`p-2 rounded border m-0.5 ${
                                rIdx === cIdx
                                  ? "bg-blue-100 font-bold text-blue-900 border-blue-300"
                                  : "bg-slate-50 text-slate-500 border-slate-100"
                              }`}
                            >
                              {cell}
                            </td>
                          ))}
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </section>

          {/* ============================================================== */}
          {/* SECTION 2: LSTM MODEL EVALUATION */}
          {/* ============================================================== */}
          <section className="space-y-5 pt-4">
            <div className="flex items-center justify-between pb-2 border-b border-slate-200">
              <div>
                <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
                  <TrendingUp className="w-4 h-4 text-purple-600" />
                  <span>LSTM Time-Series Benchmark Evaluation</span>
                </h2>
                <p className="text-xs text-slate-500">
                  Sequential error metrics across benchmark assets on 80/20 train/test partitions
                </p>
              </div>
              <span className="text-[11px] font-mono text-purple-800 bg-purple-50 px-2 py-0.5 rounded border border-purple-200">
                Lookback Window: 20 Days
              </span>
            </div>

            {/* Asset Benchmarks Table */}
            <div className="bg-white rounded-xl border border-slate-200 overflow-hidden shadow-xs">
              <div className="overflow-x-auto">
                <table className="w-full text-left text-xs">
                  <thead className="bg-slate-50 border-b border-slate-200 text-slate-600 font-semibold">
                    <tr>
                      <th className="px-5 py-3">Benchmark Asset</th>
                      <th className="px-4 py-3">Ticker</th>
                      <th className="px-4 py-3 text-right">MAE</th>
                      <th className="px-4 py-3 text-right">RMSE</th>
                      <th className="px-4 py-3 text-right">MAPE (%)</th>
                      <th className="px-5 py-3 text-right font-bold text-slate-900">
                        Directional Accuracy
                      </th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100 font-mono">
                    {evaluation.lstm_evaluation.benchmark_assets.map((asset, idx) => (
                      <tr key={idx} className="hover:bg-slate-50/60 transition-colors">
                        <td className="px-5 py-3 font-semibold font-sans text-slate-900">
                          {asset.company}
                        </td>
                        <td className="px-4 py-3 text-slate-500">
                          {asset.ticker}
                        </td>
                        <td className="px-4 py-3 text-right text-slate-800">
                          {asset.mae}
                        </td>
                        <td className="px-4 py-3 text-right text-slate-800">
                          {asset.rmse}
                        </td>
                        <td className="px-4 py-3 text-right font-bold text-purple-700">
                          {asset.mape}%
                        </td>
                        <td className="px-5 py-3 text-right font-bold text-emerald-700">
                          {asset.directional_accuracy}%
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

            {/* Metric Explanations */}
            <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-xs space-y-4">
              <div className="flex items-center gap-2 pb-2 border-b border-slate-100">
                <HelpCircle className="w-4 h-4 text-blue-600" />
                <h3 className="text-xs font-bold uppercase tracking-wider text-slate-800">
                  Evaluation Metric Definitions
                </h3>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
                {Object.entries(evaluation.lstm_evaluation.metric_explanations).map(([key, desc]) => (
                  <div key={key} className="p-3 rounded-lg bg-slate-50 border border-slate-200">
                    <span className="font-bold text-slate-900 block mb-0.5">{key}</span>
                    <p className="text-slate-600 leading-relaxed text-[11px]">{desc}</p>
                  </div>
                ))}
              </div>
            </div>
          </section>
        </div>
      ) : null}
    </div>
  );
}
