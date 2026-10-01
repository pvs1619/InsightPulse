import re
from typing import List, Dict, Any

TOPIC_TAXONOMY = {
    "AI & Technology": {
        "keywords": ["ai", "generative ai", "copilot", "gpu", "datacenter", "data center", "chips", "semiconductor", "blackwell", "cuda", "cloud", "azure", "aws", "software", "machine learning", "silicon", "npu", "compute", "topaz"],
        "weight": 1.2
    },
    "Revenue & Growth": {
        "keywords": ["revenue", "sales", "growth", "deliveries", "shipments", "guidance", "order", "bookings", "expansion", "rebound", "soared", "surged", "contract", "tcv", "deal", "subscribers"],
        "weight": 1.1
    },
    "Profitability & Margins": {
        "keywords": ["profit", "profitability", "ebitda", "margin", "margins", "gross margin", "operating margin", "net income", "cash flow", "free cash flow", "earnings", "eps", "operating income"],
        "weight": 1.1
    },
    "Supply Chain & Hardware": {
        "keywords": ["supply chain", "packaging", "tsmc", "cowos", "foundry", "bottleneck", "manufacturing", "inventory", "hardware", "assembly", "raw material", "logistics", "batteries", "oled", "components"],
        "weight": 1.1
    },
    "Regulation & Legal": {
        "keywords": ["antitrust", "regulation", "regulatory", "doj", "ftc", "investigation", "monopoly", "lawsuit", "litigation", "scrutiny", "export control", "licensing", "tariffs", "patent", "dma", "compliance"],
        "weight": 1.2
    },
    "Competition & Market Share": {
        "keywords": ["competition", "competitor", "market share", "rivalry", "pricing war", "price cuts", "huawei", "byd", "peers", "disruption", "inflows", "alternative"],
        "weight": 1.0
    },
    "Workforce & Operational Talent": {
        "keywords": ["workforce", "employee", "attrition", "hiring", "wage", "salaries", "union", "unionization", "upskilling", "subcontractor", "talent", "headcount", "associates"],
        "weight": 1.0
    },
    "Capital & Investment": {
        "keywords": ["capex", "capital expenditure", "investment", "dividend", "buyback", "share repurchase", "debt", "equity", "financing", "gigafactory", "infrastructure", "funding", "balance sheet"],
        "weight": 1.1
    },
    "ESG & Clean Energy": {
        "keywords": ["renewable energy", "green hydrogen", "clean energy", "solar", "esg", "megapack", "energy storage", "grid", "emissions", "sustainability", "electrolyzer"],
        "weight": 1.2
    }
}

class FinancialTopicClassifier:
    """
    NLP-based Financial Topic Classifier mapping text against financial ontology
    with keyword density, bigram matches, and confidence normalization.
    """

    def __init__(self):
        self.taxonomy = TOPIC_TAXONOMY

    def classify_topics(self, text: str, min_confidence: float = 15.0) -> List[Dict[str, Any]]:
        if not text:
            return []

        clean_text = text.lower()
        topic_scores = {}
        matched_indicators = {}

        for topic, config in self.taxonomy.items():
            score = 0.0
            matches = []
            for kw in config["keywords"]:
                # Check exact phrase or word boundary
                pattern = rf'\b{re.escape(kw)}\b'
                occurrences = len(re.findall(pattern, clean_text))
                if occurrences > 0:
                    phrase_boost = 1.6 if " " in kw else 1.0
                    score += occurrences * phrase_boost * config["weight"]
                    matches.append(kw)

            if score > 0:
                topic_scores[topic] = score
                matched_indicators[topic] = matches

        if not topic_scores:
            return [{
                "topic": "General Market Operations",
                "confidence": 50.0,
                "relevance_rank": 1,
                "matched_terms": []
            }]

        total_score = sum(topic_scores.values())
        results = []

        for rank, (topic, raw_score) in enumerate(sorted(topic_scores.items(), key=lambda x: x[1], reverse=True), 1):
            conf = round((raw_score / total_score) * 100, 1)
            if conf >= min_confidence or rank <= 2:
                results.append({
                    "topic": topic,
                    "confidence": conf,
                    "relevance_rank": rank,
                    "matched_terms": matched_indicators.get(topic, [])[:4]
                })

        return results

topic_classifier = FinancialTopicClassifier()
