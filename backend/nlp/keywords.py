import re
import math
from collections import Counter
from typing import List, Dict, Any

FINANCIAL_DOMAIN_VOCAB = {
    "revenue", "earnings", "profit", "profitability", "margins", "margin", "ebitda",
    "growth", "demand", "cloud", "ai", "copilot", "chips", "gpu", "datacenter",
    "deliveries", "shipments", "guidance", "capex", "capital expenditure", "cash flow",
    "free cash flow", "dividend", "buyback", "shareholders", "debt", "leverage",
    "inflation", "valuation", "investment", "clean energy", "gigafactory", "solar",
    "hydrogen", "antitrust", "litigation", "investigation", "tariff", "subsidies",
    "contract", "backlog", "discretionary", "workforce", "attrition", "efficiency"
}

class FinancialKeywordExtractor:
    """
    Financial keyword extractor utilizing domain-weighted TF-IDF and
    frequency extraction for high-value unigrams and key financial collocations.
    """

    def __init__(self):
        self.domain_vocab = FINANCIAL_DOMAIN_VOCAB

    def extract_keywords(self, text: str, top_k: int = 8) -> List[Dict[str, Any]]:
        if not text:
            return []

        # Find words (alphanumeric, 2+ letters)
        clean_text = text.lower()
        words = re.findall(r'\b[a-zA-Z]{2,}\b', clean_text)
        
        # Stop words to ignore
        stopwords = {
            "the", "and", "for", "with", "that", "this", "from", "are", "was", "were",
            "been", "have", "has", "had", "will", "could", "would", "reported", "said",
            "noted", "during", "while", "after", "into", "their", "quarterly", "annual",
            "which", "about", "other", "some", "more", "also", "amid", "across"
        }
        
        filtered_words = [w for w in words if w not in stopwords]
        if not filtered_words:
            return []

        word_counts = Counter(filtered_words)
        total_words = len(filtered_words)

        scored_candidates = {}

        # 1. Score unigrams
        for word, count in word_counts.items():
            tf = count / total_words
            # Boost if in financial domain dictionary
            domain_boost = 2.5 if word in self.domain_vocab else 1.0
            length_boost = 1.0 + (min(len(word), 10) * 0.05)
            score = round(tf * domain_boost * length_boost * 100, 2)
            
            # Format display label (e.g. AI, GPU uppercase)
            if word in ["ai", "gpu", "tpu", "npu", "aws", "ev", "roi", "cfo", "ceo", "ebitda"]:
                display_label = word.upper()
            else:
                display_label = word.capitalize()

            scored_candidates[display_label] = score

        # 2. Check for key bigrams (e.g. "revenue growth", "capital expenditure", "data center", "operating margin")
        bigram_targets = [
            ("revenue", "growth"), ("operating", "margins"), ("operating", "margin"),
            ("capital", "expenditure"), ("data", "center"), ("clean", "energy"),
            ("cash", "flow"), ("free", "cash"), ("supply", "chain"), ("artificial", "intelligence"),
            ("digital", "transformation"), ("electric", "vehicle"), ("share", "buyback")
        ]
        
        for w1, w2 in bigram_targets:
            pattern = rf'\b{w1}\s+{w2}\b'
            matches = len(re.findall(pattern, clean_text))
            if matches > 0:
                bigram_label = f"{w1.capitalize()} {w2.capitalize()}"
                bigram_score = round((matches / total_words) * 3.5 * 100, 2)
                scored_candidates[bigram_label] = bigram_score

        # Sort by score descending
        sorted_keywords = sorted(scored_candidates.items(), key=lambda x: x[1], reverse=True)

        return [{"keyword": kw, "score": score} for kw, score in sorted_keywords[:top_k]]

keyword_extractor = FinancialKeywordExtractor()
