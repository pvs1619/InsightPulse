"use client";

import { useState } from "react";
import { PreprocessingData } from "@/lib/api";
import { ChevronDown, ChevronUp, Code2, Check, Sparkles } from "lucide-react";

interface Props {
  data: PreprocessingData;
}

export default function PreprocessingViewer({ data }: Props) {
  const [isOpen, setIsOpen] = useState(false);
  const [showAllTokens, setShowAllTokens] = useState(false);

  return (
    <div className="border border-slate-200 rounded-lg bg-white overflow-hidden shadow-xs">
      <div
        onClick={() => setIsOpen(!isOpen)}
        className="px-4 py-3 bg-slate-50 border-b border-slate-200 flex items-center justify-between cursor-pointer hover:bg-slate-100/80 transition-colors"
      >
        <div className="flex items-center gap-2.5">
          <Code2 className="w-4 h-4 text-blue-600" />
          <span className="text-sm font-semibold text-slate-800">
            Financial Text Preprocessing Pipeline
          </span>
          <span className="text-[11px] px-2 py-0.5 rounded-full bg-blue-100 text-blue-800 font-mono">
            {data.token_count} Tokens
          </span>
          <span className="text-[11px] px-2 py-0.5 rounded-full bg-slate-200 text-slate-700 font-mono">
            Vocab: {data.vocabulary_size}
          </span>
        </div>
        <div className="flex items-center gap-2 text-xs text-slate-500">
          <span>{isOpen ? "Hide Pipeline Details" : "View Processing Details"}</span>
          {isOpen ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
        </div>
      </div>

      {isOpen && (
        <div className="p-5 space-y-4 text-sm bg-white">
          {/* Pipeline flow visual */}
          <div className="flex items-center justify-between text-xs text-slate-500 pb-2 border-b border-slate-100">
            <span className="font-semibold text-slate-700">Pipeline Flow:</span>
            <div className="flex items-center gap-1.5 font-mono">
              <span className="px-2 py-0.5 rounded bg-slate-100 text-slate-700">Raw Input</span>
              <span>→</span>
              <span className="px-2 py-0.5 rounded bg-slate-100 text-slate-700">Financial Clean</span>
              <span>→</span>
              <span className="px-2 py-0.5 rounded bg-slate-100 text-slate-700">Tokenize</span>
              <span>→</span>
              <span className="px-2 py-0.5 rounded bg-blue-50 text-blue-700 font-bold">NLP Inference</span>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Cleaned text */}
            <div className="p-3 bg-slate-50 rounded-md border border-slate-200">
              <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1.5">
                Cleaned Normalized Text
              </div>
              <p className="text-xs text-slate-800 leading-relaxed font-mono bg-white p-2.5 rounded border border-slate-200">
                {data.cleaned_text}
              </p>
            </div>

            {/* Preserved Financial Tokens */}
            <div className="p-3 bg-slate-50 rounded-md border border-slate-200">
              <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1.5 flex items-center justify-between">
                <span>Preserved Financial Tokens</span>
                <span className="text-[10px] text-emerald-700 font-mono bg-emerald-50 px-1.5 py-0.5 rounded border border-emerald-200">
                  Protected Currency & %
                </span>
              </div>
              <div className="flex flex-wrap gap-1.5">
                {data.financial_tokens.length > 0 ? (
                  data.financial_tokens.map((tok, i) => (
                    <span
                      key={i}
                      className="px-2 py-0.5 rounded text-xs font-mono font-medium bg-emerald-100 text-emerald-900 border border-emerald-300"
                    >
                      {tok}
                    </span>
                  ))
                ) : (
                  <span className="text-xs text-slate-400 italic">No specific currency/percentage tokens found.</span>
                )}
              </div>
            </div>
          </div>

          {/* Tokens list */}
          <div>
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-semibold text-slate-700">
                Generated Token Sequence ({data.tokens.length} tokens):
              </span>
              {data.tokens.length > 30 && (
                <button
                  type="button"
                  onClick={() => setShowAllTokens(!showAllTokens)}
                  className="text-xs text-blue-600 hover:text-blue-700 font-medium"
                >
                  {showAllTokens ? "Show Fewer" : `Show All ${data.tokens.length}`}
                </button>
              )}
            </div>
            <div className="flex flex-wrap gap-1 p-2.5 bg-slate-50 rounded border border-slate-200 max-h-48 overflow-y-auto font-mono text-xs">
              {(showAllTokens ? data.tokens : data.tokens.slice(0, 30)).map((tok, i) => (
                <span
                  key={i}
                  className="px-1.5 py-0.5 bg-white text-slate-800 rounded border border-slate-200 shadow-2xs"
                >
                  {tok}
                </span>
              ))}
              {!showAllTokens && data.tokens.length > 30 && (
                <span className="px-1.5 py-0.5 text-slate-400 italic">
                  +{data.tokens.length - 30} more tokens...
                </span>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
