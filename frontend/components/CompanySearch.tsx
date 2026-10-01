"use client";

import { useState } from "react";
import { Search, Loader2, Sparkles, Building2 } from "lucide-react";

interface Props {
  initialValue?: string;
  onSearch: (companyOrTicker: string) => void;
  loading?: boolean;
  placeholder?: string;
  buttonText?: string;
}

const QUICK_SUGGESTIONS = [
  "NVIDIA",
  "Tesla",
  "Apple",
  "Alphabet",
  "Meta",
  "Microsoft",
  "Reliance",
  "TCS",
  "JPMorgan"
];

export default function CompanySearch({
  initialValue = "",
  onSearch,
  loading = false,
  placeholder = "Enter company name or stock ticker (e.g., Apple, TSLA, Google, TCS)...",
  buttonText = "Analyze Company"
}: Props) {
  const [query, setQuery] = useState<string>(initialValue);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim() && !loading) {
      onSearch(query.trim());
    }
  };

  const handleSuggestionClick = (name: string) => {
    setQuery(name);
    onSearch(name);
  };

  return (
    <div className="bg-white rounded-xl border border-slate-200 p-4 shadow-xs space-y-3">
      <form onSubmit={handleSubmit} className="flex flex-col sm:flex-row items-center gap-2">
        <div className="relative flex-1 w-full">
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-slate-400">
            <Search className="w-4 h-4" />
          </div>
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder={placeholder}
            className="w-full text-xs text-slate-900 bg-slate-50 border border-slate-300 rounded-lg pl-9 pr-3.5 py-2.5 focus:bg-white focus:outline-hidden focus:ring-2 focus:ring-blue-500 font-medium transition-colors"
          />
        </div>

        <button
          type="submit"
          disabled={loading || !query.trim()}
          className="w-full sm:w-auto px-5 py-2.5 bg-blue-600 hover:bg-blue-700 disabled:bg-slate-300 text-white rounded-lg text-xs font-bold transition-all flex items-center justify-center gap-2 shadow-sm shrink-0"
        >
          {loading ? (
            <>
              <Loader2 className="w-3.5 h-3.5 animate-spin" />
              <span>Fetching Data...</span>
            </>
          ) : (
            <>
              <Building2 className="w-3.5 h-3.5" />
              <span>{buttonText}</span>
            </>
          )}
        </button>
      </form>

      {/* Quick Suggestions Chips */}
      <div className="flex flex-wrap items-center gap-1.5 pt-1 text-xs">
        <span className="text-[11px] text-slate-400 font-medium flex items-center gap-1 mr-1">
          <Sparkles className="w-3 h-3 text-blue-500" />
          Suggestions:
        </span>
        {QUICK_SUGGESTIONS.map((item) => (
          <button
            key={item}
            type="button"
            onClick={() => handleSuggestionClick(item)}
            className="px-2 py-0.5 rounded text-[11px] font-medium bg-slate-100 hover:bg-blue-50 hover:text-blue-700 hover:border-blue-200 border border-slate-200 text-slate-600 transition-colors"
          >
            {item}
          </button>
        ))}
      </div>
    </div>
  );
}
