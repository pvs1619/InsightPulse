import { TopicItem } from "@/lib/api";
import { Tag } from "lucide-react";

interface Props {
  topics: TopicItem[];
}

export default function TopicBadge({ topics }: Props) {
  if (!topics || topics.length === 0) {
    return <span className="text-xs text-slate-400 italic">No topics identified.</span>;
  }

  return (
    <div className="space-y-2.5">
      {topics.map((t, idx) => (
        <div
          key={idx}
          className="p-3 bg-slate-50 border border-slate-200 rounded-lg flex items-center justify-between hover:bg-slate-100/70 transition-colors"
        >
          <div className="flex items-center gap-2.5">
            <span className="w-5 h-5 rounded-full bg-blue-100 text-blue-800 text-[11px] font-bold flex items-center justify-center font-mono">
              {idx + 1}
            </span>
            <div>
              <div className="text-xs font-semibold text-slate-900">{t.topic}</div>
              {t.matched_terms && t.matched_terms.length > 0 && (
                <div className="text-[11px] text-slate-500 flex items-center gap-1 mt-0.5 font-mono">
                  <span>Signals:</span>
                  <span>{t.matched_terms.join(", ")}</span>
                </div>
              )}
            </div>
          </div>
          <div className="text-right">
            <span className="text-xs font-bold text-blue-700 bg-blue-50 px-2 py-0.5 rounded border border-blue-200 font-mono">
              {t.confidence}%
            </span>
          </div>
        </div>
      ))}
    </div>
  );
}
