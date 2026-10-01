"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { 
  LayoutDashboard, 
  FileText, 
  Building2, 
  LineChart, 
  TrendingUp, 
  CheckCircle2,
  Database,
  Layers,
  Activity
} from "lucide-react";

interface NavItem {
  name: string;
  href: string;
  icon: any;
  badge?: string;
}

const NAV_ITEMS: NavItem[] = [
  { name: "Dashboard", href: "/", icon: LayoutDashboard },
  { name: "Analyze Text", href: "/analyze", icon: FileText, badge: "NLP" },
  { name: "Company Analysis", href: "/company", icon: Building2 },
  { name: "Market Analysis", href: "/market", icon: LineChart },
  { name: "Predictive Analytics", href: "/predict", icon: TrendingUp, badge: "LSTM" },
  { name: "Model Evaluation", href: "/evaluation", icon: CheckCircle2, badge: "Metrics" },
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="w-64 bg-slate-900 text-slate-200 min-h-screen flex flex-col border-r border-slate-800 shrink-0">
      {/* Brand Header */}
      <div className="p-5 border-b border-slate-800">
        <Link href="/" className="flex items-center gap-3 group">
          <div className="w-9 h-9 rounded-lg bg-blue-600 flex items-center justify-center text-white font-bold shadow-md shadow-blue-500/20 group-hover:bg-blue-500 transition-colors">
            IP
          </div>
          <div>
            <div className="font-semibold text-white tracking-tight text-base flex items-center gap-1.5">
              InsightPulse
            </div>
            <p className="text-xs text-slate-400 font-mono">Investment NLP & Analytics</p>
          </div>
        </Link>
      </div>

      {/* Navigation Links */}
      <nav className="flex-1 px-3 py-4 space-y-1 overflow-y-auto">
        <div className="px-3 pb-2 text-[11px] font-semibold uppercase tracking-wider text-slate-400">
          Analytics Platform
        </div>

        {NAV_ITEMS.map((item) => {
          const isActive = pathname === item.href;
          const Icon = item.icon;

          return (
            <Link
              key={item.href}
              href={item.href}
              className={`flex items-center justify-between px-3 py-2.5 rounded-lg text-sm font-medium transition-all ${
                isActive
                  ? "bg-blue-600 text-white shadow-sm shadow-blue-600/30"
                  : "text-slate-300 hover:text-white hover:bg-slate-800/70"
              }`}
            >
              <div className="flex items-center gap-3">
                <Icon className={`w-4 h-4 ${isActive ? "text-white" : "text-slate-400"}`} />
                <span>{item.name}</span>
              </div>
              {item.badge && (
                <span
                  className={`text-[10px] font-mono px-1.5 py-0.5 rounded ${
                    isActive
                      ? "bg-blue-700 text-blue-100"
                      : "bg-slate-800 text-slate-300 border border-slate-700"
                  }`}
                >
                  {item.badge}
                </span>
              )}
            </Link>
          );
        })}
      </nav>

      {/* System Status Indicator */}
      <div className="p-3.5 mx-3 mb-4 rounded-lg bg-slate-800/80 border border-slate-700/60 text-xs text-slate-300">
        <div className="flex items-center gap-2 mb-1.5">
          <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
          <span className="font-semibold text-slate-200">System Online</span>
        </div>
        <p className="text-[11px] text-slate-400 leading-relaxed">
          Dynamic market data integration & real-time financial NLP pipelines active.
        </p>
        <div className="mt-2.5 pt-2 border-t border-slate-700/60 flex items-center justify-between text-[10px] text-slate-400 font-mono">
          <span className="flex items-center gap-1">
            <Activity className="w-3 h-3 text-emerald-400" />
            Live Market Feed
          </span>
          <span className="flex items-center gap-1">
            <Layers className="w-3 h-3 text-blue-400" />
            FinBERT / LSTM
          </span>
        </div>
      </div>
    </aside>
  );
}
