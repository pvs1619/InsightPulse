import { EntityItem } from "@/lib/api";
import { Building, DollarSign, Percent, User, MapPin, Calendar } from "lucide-react";

interface Props {
  entities: EntityItem[];
}

export default function EntityTable({ entities }: Props) {
  if (!entities || entities.length === 0) {
    return (
      <div className="p-6 text-center text-xs text-slate-400 border border-slate-200 rounded-lg bg-slate-50">
        No recognized named entities identified in the submitted text.
      </div>
    );
  }

  const getTypeIcon = (type: string) => {
    switch (type) {
      case "Organization":
        return <Building className="w-3.5 h-3.5 text-blue-600" />;
      case "Money":
        return <DollarSign className="w-3.5 h-3.5 text-emerald-600" />;
      case "Percentage":
        return <Percent className="w-3.5 h-3.5 text-amber-600" />;
      case "Person":
        return <User className="w-3.5 h-3.5 text-purple-600" />;
      case "Location":
        return <MapPin className="w-3.5 h-3.5 text-rose-600" />;
      case "Date/Period":
        return <Calendar className="w-3.5 h-3.5 text-slate-600" />;
      default:
        return null;
    }
  };

  const getTypeBadge = (type: string) => {
    switch (type) {
      case "Organization":
        return "bg-blue-50 text-blue-700 border-blue-200";
      case "Money":
        return "bg-emerald-50 text-emerald-800 border-emerald-200";
      case "Percentage":
        return "bg-amber-50 text-amber-800 border-amber-200";
      case "Person":
        return "bg-purple-50 text-purple-700 border-purple-200";
      case "Location":
        return "bg-rose-50 text-rose-700 border-rose-200";
      case "Date/Period":
        return "bg-slate-100 text-slate-700 border-slate-200";
      default:
        return "bg-slate-50 text-slate-600 border-slate-200";
    }
  };

  return (
    <div className="border border-slate-200 rounded-lg overflow-hidden bg-white shadow-xs">
      <div className="px-4 py-3 bg-slate-50 border-b border-slate-200 flex items-center justify-between">
        <span className="text-xs font-semibold text-slate-700 uppercase tracking-wider">
          Named Entity Recognition (NER)
        </span>
        <span className="text-xs font-mono text-slate-500">
          {entities.length} {entities.length === 1 ? "Entity" : "Entities"} Found
        </span>
      </div>

      <div className="overflow-x-auto max-h-64 overflow-y-auto">
        <table className="w-full text-left text-xs">
          <thead className="bg-slate-50/70 border-b border-slate-200 text-slate-500 font-semibold sticky top-0">
            <tr>
              <th className="px-4 py-2.5">Extracted Entity</th>
              <th className="px-4 py-2.5">Entity Type</th>
              <th className="px-4 py-2.5 font-mono text-right">Span</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {entities.map((ent, idx) => (
              <tr key={idx} className="hover:bg-slate-50/60 transition-colors">
                <td className="px-4 py-2 font-medium text-slate-900">
                  {ent.entity}
                </td>
                <td className="px-4 py-2">
                  <span
                    className={`inline-flex items-center gap-1.5 px-2 py-0.5 rounded text-[11px] font-medium border ${getTypeBadge(
                      ent.type
                    )}`}
                  >
                    {getTypeIcon(ent.type)}
                    {ent.type}
                  </span>
                </td>
                <td className="px-4 py-2 text-right font-mono text-slate-400 text-[11px]">
                  [{ent.start_char}:{ent.end_char}]
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
