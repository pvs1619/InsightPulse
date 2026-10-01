import { SentimentData } from "@/lib/api";
import { TrendingUp, TrendingDown, Minus, Info } from "lucide-react";

interface Props {
  sentiment: SentimentData;
}

export default function SentimentBadge({ sentiment }: Props) {
  const isPos = sentiment.sentiment === "Positive";
  const isNeg = sentiment.sentiment === "Negative";

  const colorClass = isPos
    ? "bg-emerald-50 text-emerald-800 border-emerald-300"
    : isNeg
    ? "bg-rose-50 text-rose-800 border-rose-300"
    : "bg-slate-100 text-slate-800 border-slate-300";

  const Icon = isPos ? TrendingUp : isNeg ? TrendingDown : Minus;

  return (
    <div className="p-5 rounded-lg border border-slate-200 bg-white shadow-xs">
      <div className="flex items-center justify-between mb-3">
        <span className="text-xs font-semibold uppercase tracking-wider text-slate-500">
          Financial Sentiment Classification
        </span>
        <span
          className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold border ${colorClass}`}
        >
          <Icon className="w-3.5 h-3.5" />
          {sentiment.sentiment}
        </span>
      </div>

      <div className="flex items-baseline gap-2 mb-4">
        <span className="text-3xl font-extrabold tracking-tight text-slate-900">
          {sentiment.confidence}%
        </span>
        <span className="text-xs text-slate-500 font-medium">Confidence Score</span>
      </div>

      {/* Probabilities Distribution */}
      <div className="space-y-2 mb-4">
        <div className="text-xs font-medium text-slate-600 flex justify-between">
          <span>Probability Distribution</span>
          <span className="font-mono text-[11px] text-slate-500">Softmax Calibrated</span>
        </div>

        {/* Positive bar */}
        <div>
          <div className="flex justify-between text-[11px] mb-1">
            <span className="text-emerald-700 font-medium">Positive</span>
            <span className="font-mono text-slate-700">
              {Math.round(sentiment.probabilities.positive * 1000) / 10}%
            </span>
          </div>
          <div className="w-full bg-slate-100 h-2 rounded-full overflow-hidden">
            <div
              className="bg-emerald-500 h-full rounded-full transition-all duration-500"
              style={{ width: `${sentiment.probabilities.positive * 100}%` }}
            />
          </div>
        </div>

        {/* Neutral bar */}
        <div>
          <div className="flex justify-between text-[11px] mb-1">
            <span className="text-slate-600 font-medium">Neutral</span>
            <span className="font-mono text-slate-700">
              {Math.round(sentiment.probabilities.neutral * 1000) / 10}%
            </span>
          </div>
          <div className="w-full bg-slate-100 h-2 rounded-full overflow-hidden">
            <div
              className="bg-slate-400 h-full rounded-full transition-all duration-500"
              style={{ width: `${sentiment.probabilities.neutral * 100}%` }}
            />
          </div>
        </div>

        {/* Negative bar */}
        <div>
          <div className="flex justify-between text-[11px] mb-1">
            <span className="text-rose-700 font-medium">Negative</span>
            <span className="font-mono text-slate-700">
              {Math.round(sentiment.probabilities.negative * 1000) / 10}%
            </span>
          </div>
          <div className="w-full bg-slate-100 h-2 rounded-full overflow-hidden">
            <div
              className="bg-rose-500 h-full rounded-full transition-all duration-500"
              style={{ width: `${sentiment.probabilities.negative * 100}%` }}
            />
          </div>
        </div>
      </div>

      {/* Model Source metadata */}
      <div className="pt-3 border-t border-slate-100 flex items-start gap-2 text-[11px] text-slate-500">
        <Info className="w-3.5 h-3.5 text-blue-500 shrink-0 mt-0.5" />
        <div>
          <span className="font-medium text-slate-700">Model Source: </span>
          <span className="font-mono text-slate-800">{sentiment.model_source}</span>
          {sentiment.is_fallback && (
            <span className="block mt-0.5 text-amber-800 bg-amber-50 px-1.5 py-0.5 rounded border border-amber-200">
              Demonstration Mode: Loughran-McDonald Financial Lexicon Inference Active
            </span>
          )}
        </div>
      </div>
    </div>
  );
}
