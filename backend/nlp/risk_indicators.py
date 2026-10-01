import re
from typing import List, Dict, Any

RISK_DEFINITIONS = [
    {
        "category": "Cost & Margin Pressure",
        "description": "Indicators of rising operational expenses, input costs, wage pressures, or margin compression.",
        "patterns": [
            r'pressure(?:\s+on)?\s+margins', r'rising\s+(?:production|operating|employee|labor|input|subcontractor)\s+costs',
            r'margin\s+contraction', r'contracted\s+to', r'price\s+cuts', r'pricing\s+pressure',
            r'elevated\s+raw\s+material', r'expenditures\s+pressuring', r'cost\s+inflation'
        ],
        "keywords": ["cost pressure", "margin contraction", "wage hikes", "price cuts", "margin risk"]
    },
    {
        "category": "Supply Chain & Capacity Constraints",
        "description": "Indicators of bottlenecks, packaging tightness, inventory shortages, or manufacturing delays.",
        "patterns": [
            r'supply\s+chain\s+bottlenecks?', r'capacity\s+limits?', r'packaging\s+capacity',
            r'shortages?', r'component\s+delay', r'delivery\s+setbacks?', r'foundry\s+capacity',
            r'grid\s+power\s+connection\s+queues?'
        ],
        "keywords": ["supply bottleneck", "capacity shortage", "lead time delays", "packaging constraints"]
    },
    {
        "category": "Regulatory & Antitrust Scrutiny",
        "description": "Indicators of government investigations, antitrust lawsuits, regulatory compliance fees, or export curbs.",
        "patterns": [
            r'regulatory\s+scrutiny', r'antitrust\s+(?:investigation|lawsuit|litigation|review)',
            r'monopoly\s+probe', r'export\s+control', r'licensing\s+thresholds?', r'compliance\s+risk',
            r'investigation\s+into', r'ftc\s+litigation', r'doj\s+monopolization', r'digital\s+markets\s+act'
        ],
        "keywords": ["regulatory scrutiny", "antitrust inquiry", "export restrictions", "compliance penalties"]
    },
    {
        "category": "Competition & Pricing Headwinds",
        "description": "Indicators of market share erosion, rival aggressive pricing, or domestic substitutes.",
        "patterns": [
            r'intensifying\s+competition', r'fierce\s+(?:domestic\s+)?competition', r'rival\s+offerings',
            r'price\s+war', r'market\s+share\s+erosion', r'gained\s+market\s+share', r'low-cost\s+polymer\s+exports'
        ],
        "keywords": ["competitive pressure", "market share loss", "pricing competition"]
    },
    {
        "category": "Geopolitical & Trade Friction",
        "description": "Indicators of cross-border sanctions, tariff disputes, or trade policy uncertainty.",
        "patterns": [
            r'geopolitical\s+export\s+restrictions', r'trade\s+tariff', r'tariffs?\s+uncertaint(?:y|ies)',
            r'geopolitical\s+tensions?', r'sanctions?', r'foreign\s+trade\s+policy'
        ],
        "keywords": ["geopolitical tension", "trade tariffs", "export curbs"]
    },
    {
        "category": "Discretionary Spending & Demand Softness",
        "description": "Indicators of client budget tightening, elongation of sales cycles, or postponed contracts.",
        "patterns": [
            r'curtailed\s+discretionary', r'spending\s+caution', r'deferred\s+(?:non-critical\s+)?projects',
            r'decision\s+cycles?\s+remained\s+elongated', r'budgeting\s+scrutiny', r'subdued\s+spending'
        ],
        "keywords": ["spending caution", "demand slowdown", "budget deferrals"]
    },
    {
        "category": "Legal & Patent Litigation",
        "description": "Indicators of active courtroom disputes, patent infringement claims, or arbitration overhead.",
        "patterns": [
            r'patent\s+dispute', r'antitrust\s+litigation', r'arbitration\s+matters',
            r'legal\s+penalties', r'lawsuit\s+examining', r'litigation\s+overhang'
        ],
        "keywords": ["patent litigation", "legal dispute", "arbitration"]
    }
]

class FinancialRiskDetector:
    """
    NLP-Derived Financial Risk Indicator module.
    Labels risk signals based on financial language analysis.
    """

    def __init__(self):
        self.risk_definitions = RISK_DEFINITIONS

    def detect_risks(self, text: str) -> List[Dict[str, Any]]:
        if not text:
            return []

        lower_text = text.lower()
        detected_risks = []

        for item in self.risk_definitions:
            matched_evidence = []
            
            # 1. Check regex patterns
            for pat in item["patterns"]:
                found = re.findall(pat, lower_text)
                if found:
                    for f in found:
                        if isinstance(f, str):
                            matched_evidence.append(f)
                        elif isinstance(f, tuple):
                            matched_evidence.append(" ".join(f))

            # 2. Check keyword overlaps
            for kw in item["keywords"]:
                if kw in lower_text and kw not in matched_evidence:
                    matched_evidence.append(kw)

            if matched_evidence:
                severity = "High" if len(matched_evidence) >= 2 else "Moderate"
                detected_risks.append({
                    "category": item["category"],
                    "description": item["description"],
                    "severity": severity,
                    "evidence_phrases": list(dict.fromkeys(matched_evidence))[:3]
                })

        return detected_risks

risk_detector = FinancialRiskDetector()
