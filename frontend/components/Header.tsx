"use client";

import { useEffect, useState } from "react";
import { checkHealth } from "@/lib/api";
import { Cpu, Database, Activity } from "lucide-react";

export default function Header() {
  const [backendStatus, setBackendStatus] = useState<string>("Checking...");
  const [modelType, setModelType] = useState<string>("Financial NLP");

  useEffect(() => {
    checkHealth()
      .then((data) => {
        setBackendStatus("Online");
        if (data.nlp_sentiment_model && data.nlp_sentiment_model.includes("fallback")) {
          setModelType("Financial Domain Lexicon");
        } else if (data.nlp_sentiment_model === "loaded") {
          setModelType("FinBERT Transformer");
        }
      })
      .catch(() => {
        setBackendStatus("Offline");
      });
  }, []);

  return (
    <header className="bg-white border-b border-slate-200 px-6 py-4 flex flex-col md:flex-row md:items-center justify-between gap-4 sticky top-0 z-30 shadow-xs">
      <div>
        <div className="flex items-center gap-2">
          <h1 className="text-lg font-bold text-slate-900 tracking-tight">
            InsightPulse
          </h1>
          <span className="text-xs font-semibold px-2 py-0.5 rounded-full bg-blue-50 text-blue-700 border border-blue-200">
            Financial Intelligence
          </span>
        </div>
        <p className="text-xs text-slate-600 mt-0.5 font-medium">
          Financial News Sentiment, Risk and Market Analysis Using NLP and Predictive Analytics
        </p>
      </div>

      <div className="flex flex-wrap items-center gap-2.5 text-xs">
        {/* Data Architecture Badge */}
        <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-slate-50 border border-slate-200 text-slate-700">
          <Database className="w-3.5 h-3.5 text-slate-500" />
          <span>Data: <strong className="text-slate-900 font-semibold">Live Feed + Fallback</strong></span>
        </div>

        {/* NLP Model Badge */}
        <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-blue-50 border border-blue-200 text-blue-800">
          <Cpu className="w-3.5 h-3.5 text-blue-600" />
          <span>NLP Engine: <strong className="font-semibold">{modelType}</strong></span>
        </div>

        {/* Backend Status */}
        <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-slate-50 border border-slate-200">
          <span className={`w-2 h-2 rounded-full ${backendStatus === "Online" ? "bg-emerald-500" : "bg-amber-500 animate-pulse"}`}></span>
          <span className="text-slate-600">Backend: <strong className="text-slate-900 font-semibold">{backendStatus}</strong></span>
        </div>
      </div>
    </header>
  );
}
