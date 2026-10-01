import { RiskIndicatorItem } from "@/lib/api";
import { AlertTriangle, AlertCircle, ShieldAlert } from "lucide-react";

interface Props {
  risks: RiskIndicatorItem[];
}

export default function RiskBadge({ risks }: Props) {
  if (!risks || risks.length === 0) {
    return (
      <div className="p-4 rounded-lg bg-emerald-50/60 border border-emerald-200 text-xs text-emerald-800 flex items-center gap-2">
        <ShieldAlert className="w-4 h-4 text-emerald-600 shrink-0" />
        <span>No elevated NLP-derived risk language detected in analyzed text.</span>
      </div>
    );
  }

  return (
    <div className="space-y-2.5">
      {risks.map((r, idx) => (
        <div
          key={idx}
          className={`p-3 rounded-lg border transition-all ${
            r.severity === "High"
              ? "bg-rose-50/70 border-rose-200"
              : "bg-amber-50/70 border-amber-200"
          }`}
        >
          <div className="flex items-start justify-between gap-2">
            <div className="flex items-center gap-2">
              {r.severity === "High" ? (
                <AlertCircle className="w-4 h-4 text-rose-600 shrink-0" />
              ) : (
                <AlertTriangle className="w-4 h-4 text-amber-600 shrink-0" />
              )}
              <span className="text-xs font-bold text-slate-900">{r.category}</span>
            </div>
            <span
              className={`text-[10px] font-bold uppercase tracking-wider px-1.5 py-0.5 rounded font-mono border ${
                r.severity === "High"
                  ? "bg-rose-100 text-rose-800 border-rose-300"
                  : "bg-amber-100 text-amber-800 border-amber-300"
              }`}
            >
              {r.severity} Severity
            </span>
          </div>

          <p className="text-xs text-slate-600 mt-1 leading-relaxed">{r.description}</p>

          {r.evidence_phrases && r.evidence_phrases.length > 0 && (
            <div className="mt-2 pt-2 border-t border-slate-200/60 flex flex-wrap items-center gap-1.5 text-[11px]">
              <span className="text-slate-500 font-mono">Matched Phrases:</span>
              {r.evidence_phrases.map((phrase, pIdx) => (
                <span
                  key={pIdx}
                  className="px-2 py-0.5 rounded bg-white text-slate-800 font-mono border border-slate-200 shadow-2xs"
                >
                  &ldquo;{phrase}&rdquo;
                </span>
              ))}
            </div>
          )}
        </div>
      ))}
    </div>
  );
}
