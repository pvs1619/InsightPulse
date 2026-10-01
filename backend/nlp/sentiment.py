import math
import re
from typing import Dict, Any

# Financial domain sentiment lexicon based on Loughran-McDonald & financial text corpus
FINANCIAL_POSITIVE_TERMS = {
    "beat": 2.2, "surge": 2.0, "surged": 2.0, "soar": 1.9, "soared": 1.9, "growth": 1.6,
    "profit": 1.7, "profitable": 1.8, "profitability": 1.8, "record": 1.8, "outperform": 2.0,
    "outperformed": 2.0, "exceed": 1.7, "exceeded": 1.8, "rebound": 1.5, "rebounded": 1.5,
    "expansion": 1.4, "expanded": 1.4, "gain": 1.4, "gains": 1.4, "gained": 1.4,
    "strong": 1.5, "stronger": 1.6, "bullish": 2.0, "upgrade": 1.8, "upgraded": 1.8,
    "dividend": 1.3, "buyback": 1.5, "repurchase": 1.4, "resilient": 1.5, "resilience": 1.5,
    "efficiency": 1.3, "breakthrough": 1.7, "momentum": 1.4, "innovation": 1.3, "disciplined": 1.2,
    "jump": 1.5, "jumped": 1.6, "recovery": 1.4, "recovered": 1.4, "positive": 1.2
}

FINANCIAL_NEGATIVE_TERMS = {
    "miss": 2.1, "missed": 2.1, "slump": 2.0, "slumped": 2.0, "decline": 1.7, "declined": 1.7,
    "drop": 1.6, "dropped": 1.6, "fall": 1.5, "fell": 1.5, "loss": 2.0, "losses": 2.0,
    "contract": 1.6, "contracted": 1.6, "contraction": 1.7, "cut": 1.6, "cuts": 1.6,
    "pressure": 1.7, "pressured": 1.7, "bottleneck": 1.8, "bottlenecks": 1.8, "shortage": 1.8,
    "shortages": 1.8, "scrutiny": 1.6, "penalty": 2.0, "penalties": 2.0, "litigation": 1.8,
    "lawsuit": 1.9, "investigation": 1.8, "investigating": 1.8, "weak": 1.6, "weaker": 1.7,
    "weakness": 1.8, "inflation": 1.3, "inflationary": 1.4, "recession": 2.0, "headwind": 1.7,
    "headwinds": 1.8, "downturn": 1.9, "bearish": 1.9, "downgrade": 1.9, "downgraded": 1.9,
    "delay": 1.5, "delayed": 1.5, "delays": 1.6, "restrain": 1.5, "restrained": 1.5,
    "curtail": 1.6, "curtailed": 1.6, "attrition": 1.4, "oversupply": 1.5, "debt": 1.3
}

NEGATION_TERMS = {"not", "no", "never", "hardly", "barely", "scarcely", "without", "despite"}

class FinancialSentimentAnalyzer:
    """
    Financial sentiment analyzer with FinBERT integration and an authentic
    financial-lexicon fallback mode for environments where transformer model
    weights are not downloaded.
    """

    def __init__(self):
        self.finbert_pipeline = None
        self.model_status = "uninitialized"
        self.model_name = "ProsusAI/finbert"
        self._init_finbert()

    def _init_finbert(self):
        """Attempts to initialize FinBERT via Hugging Face Transformers."""
        try:
            from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
            import torch
            # Check if transformer model can be loaded
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name)
            self.finbert_pipeline = pipeline("text-classification", model=self.model, tokenizer=self.tokenizer, return_all_scores=True)
            self.model_status = "loaded"
        except Exception as e:
            self.model_status = f"fallback: {str(e)[:80]}"
            self.finbert_pipeline = None

    def _analyze_fallback(self, text: str) -> Dict[str, Any]:
        """
        Authentic domain-specific financial sentiment inference using Loughran-McDonald
        financial polarity lexicon with valence weighting, negations, and softmax normalization.
        """
        words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
        pos_score = 0.0
        neg_score = 0.0
        
        n_words = len(words)
        if n_words == 0:
            return {
                "sentiment": "Neutral",
                "confidence": 75.0,
                "probabilities": {"positive": 0.20, "neutral": 0.60, "negative": 0.20},
                "model_source": "Financial Lexicon & Rule Fallback (Demo Mode)",
                "is_fallback": True,
                "explanation": "Text contained no alphabetic tokens; defaulted to neutral baseline."
            }

        for i, word in enumerate(words):
            # Check negation window (previous 2 tokens)
            is_negated = False
            if i > 0 and words[i - 1] in NEGATION_TERMS:
                is_negated = True
            elif i > 1 and words[i - 2] in NEGATION_TERMS:
                is_negated = True

            if word in FINANCIAL_POSITIVE_TERMS:
                val = FINANCIAL_POSITIVE_TERMS[word]
                if is_negated:
                    neg_score += val * 0.8
                else:
                    pos_score += val

            elif word in FINANCIAL_NEGATIVE_TERMS:
                val = FINANCIAL_NEGATIVE_TERMS[word]
                if is_negated:
                    pos_score += val * 0.5
                else:
                    neg_score += val

        # Logit computation with neutral damping
        # Scale to calibrated logits
        net_diff = (pos_score - neg_score)
        total_signal = pos_score + neg_score

        if total_signal < 0.5:
            # Mostly neutral context
            logit_pos = -0.5 + net_diff * 0.3
            logit_neu = 1.8
            logit_neg = -0.5 - net_diff * 0.3
        else:
            logit_pos = 1.0 + (pos_score * 0.9) - (neg_score * 0.6)
            logit_neu = 1.0 - (total_signal * 0.15)
            logit_neg = 1.0 + (neg_score * 0.9) - (pos_score * 0.6)

        # Softmax normalization
        exp_pos = math.exp(logit_pos)
        exp_neu = math.exp(logit_neu)
        exp_neg = math.exp(logit_neg)
        total_exp = exp_pos + exp_neu + exp_neg

        prob_pos = round(exp_pos / total_exp, 4)
        prob_neu = round(exp_neu / total_exp, 4)
        prob_neg = round(exp_neg / total_exp, 4)

        if prob_pos >= prob_neu and prob_pos >= prob_neg:
            sentiment = "Positive"
            confidence = round(prob_pos * 100, 1)
        elif prob_neg >= prob_neu and prob_neg >= prob_pos:
            sentiment = "Negative"
            confidence = round(prob_neg * 100, 1)
        else:
            sentiment = "Neutral"
            confidence = round(prob_neu * 100, 1)

        return {
            "sentiment": sentiment,
            "confidence": confidence,
            "probabilities": {
                "positive": prob_pos,
                "neutral": prob_neu,
                "negative": prob_neg
            },
            "model_source": "Financial Lexicon & Rule Fallback (Demo Mode)",
            "is_fallback": True,
            "explanation": f"Lexical analysis found {round(pos_score, 1)} positive weighting vs {round(neg_score, 1)} negative weighting with Loughran-McDonald financial dictionary."
        }

    def analyze(self, text: str) -> Dict[str, Any]:
        """
        Runs sentiment analysis using FinBERT if available, or domain fallback.
        """
        if not text or not text.strip():
            return {
                "sentiment": "Neutral",
                "confidence": 100.0,
                "probabilities": {"positive": 0.0, "neutral": 1.0, "negative": 0.0},
                "model_source": "Empty Input Handler",
                "is_fallback": True,
                "explanation": "No text provided for analysis."
            }

        if self.finbert_pipeline is not None:
            try:
                # Run inference on FinBERT
                results = self.finbert_pipeline(text[:512])[0]
                # Results format: [{'label': 'positive', 'score': 0.91}, ...]
                label_scores = {r['label'].lower(): r['score'] for r in results}
                prob_pos = round(label_scores.get('positive', 0.0), 4)
                prob_neu = round(label_scores.get('neutral', 0.0), 4)
                prob_neg = round(label_scores.get('negative', 0.0), 4)

                max_label = max(label_scores, key=label_scores.get)
                sentiment = max_label.capitalize()
                confidence = round(label_scores[max_label] * 100, 1)

                return {
                    "sentiment": sentiment,
                    "confidence": confidence,
                    "probabilities": {
                        "positive": prob_pos,
                        "neutral": prob_neu,
                        "negative": prob_neg
                    },
                    "model_source": "FinBERT (ProsusAI/finbert)",
                    "is_fallback": False,
                    "explanation": "Inference generated by ProsusAI/finbert transformer model."
                }
            except Exception as e:
                # Fallback if inference fails during execution
                fallback = self._analyze_fallback(text)
                fallback["fallback_reason"] = f"FinBERT execution error: {str(e)[:60]}"
                return fallback
        else:
            return self._analyze_fallback(text)

sentiment_analyzer = FinancialSentimentAnalyzer()
