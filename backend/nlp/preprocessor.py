import re
import unicodedata
from typing import Dict, List, Any

# Financial-aware stopwords: keeping negation and direction words
STANDARD_STOPWORDS = {
    "a", "an", "the", "and", "or", "in", "on", "at", "to", "for", "with",
    "by", "about", "into", "through", "during", "before", "after", "above",
    "below", "from", "up", "down", "in", "out", "over", "under", "again",
    "further", "then", "once", "here", "there", "when", "where", "why", "how",
    "all", "any", "both", "each", "few", "more", "most", "other", "some", "such",
    "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will",
    "just", "should", "now", "it", "its", "itself", "they", "them", "their",
    "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these",
    "those", "am", "is", "are", "was", "were", "be", "been", "being", "have",
    "has", "had", "having", "do", "does", "did", "doing"
}

# Preserve words with strong financial sentiment or negation
PRESERVED_WORDS = {
    "not", "no", "nor", "against", "without", "gain", "loss", "rise", "fall",
    "drop", "growth", "decline", "cut", "boost", "beat", "miss", "surge", "slump"
}

FINANCIAL_STOPWORDS = STANDARD_STOPWORDS - PRESERVED_WORDS

# Regex patterns for financial token identification
CURRENCY_PATTERN = re.compile(r'[$€£¥₹]\s*\d+(?:[.,]\d+)*(?:\s*(?:billion|million|trillion|crore|lakh|bn|mn|k|b|m))?', re.IGNORECASE)
PERCENT_PATTERN = re.compile(r'\b\d+(?:\.\d+)?%')
NUMERIC_PATTERN = re.compile(r'\b\d+(?:[.,]\d+)*\b')
ACRONYMS_TO_PRESERVE = {"AI", "GPU", "EBITDA", "CEO", "CFO", "TSMC", "AWS", "CoWoS", "BFSI", "NPU", "SEC", "FTC", "DOJ", "O2C", "EV", "CAGR", "EPS", "ROIC", "ROI", "IT"}

class FinancialTextPreprocessor:
    """
    Financial-aware text preprocessing engine designed specifically
    to retain critical financial tokens ($ , % , numbers, currency units, acronyms).
    """

    def __init__(self):
        self.currency_pattern = CURRENCY_PATTERN
        self.percent_pattern = PERCENT_PATTERN

    def clean_text(self, text: str) -> str:
        """
        Normalizes unicode, clears excess whitespace, but preserves financial currency
        symbols ($ , € , £ , ₹), percentages, decimal numbers, and capitalization of acronyms.
        """
        if not text:
            return ""
        # Normalize unicode (e.g. special quotes, non-breaking spaces)
        text = unicodedata.normalize("NFKC", text)
        # Standardize quotes and hyphens
        text = text.replace("“", '"').replace("”", '"').replace("‘", "'").replace("’", "'")
        text = text.replace("—", " - ").replace("–", " - ")
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def tokenize(self, text: str) -> List[str]:
        """
        Custom financial tokenizer that preserves entities like '$2.5 billion', '₹75,000 crore', '17.2%'
        """
        cleaned = self.clean_text(text)
        # Token pattern: currency phrases, percentage expressions, hyphenated financial terms, words, numbers
        token_regex = re.compile(
            r'[$€£¥₹]\s*\d+(?:[.,]\d+)*(?:\s*(?:billion|million|trillion|crore|lakh|bn|mn))?'
            r'|\b\d+(?:\.\d+)?%'
            r'|\b[A-Za-z0-9]+(?:[-_][A-Za-z0-9]+)*\b'
            r'|[^\w\s]',
            re.IGNORECASE
        )
        tokens = token_regex.findall(cleaned)
        return [t.strip() for t in tokens if t.strip()]

    def extract_financial_tokens(self, text: str) -> List[str]:
        """Identifies monetary and percentage markers within the text."""
        currencies = self.currency_pattern.findall(text)
        percentages = self.percent_pattern.findall(text)
        return list(dict.fromkeys(currencies + percentages))

    def preprocess(self, text: str, remove_stopwords: bool = False) -> Dict[str, Any]:
        """
        Executes full preprocessing pipeline and produces technical audit metadata
        for educational/viva inspection.
        """
        if not text or not text.strip():
            return {
                "original_text": "",
                "cleaned_text": "",
                "tokens": [],
                "token_count": 0,
                "char_count": 0,
                "vocabulary_size": 0,
                "financial_tokens": [],
                "stopwords_removed": 0
            }

        original = text
        cleaned = self.clean_text(original)
        tokens = self.tokenize(cleaned)
        
        filtered_tokens = []
        stopwords_count = 0

        for token in tokens:
            lower = token.lower()
            if remove_stopwords and lower in FINANCIAL_STOPWORDS:
                stopwords_count += 1
            else:
                filtered_tokens.append(token)

        vocab = sorted(list(set(t.lower() for t in tokens if t.isalnum())))
        financial_tokens = self.extract_financial_tokens(original)

        return {
            "original_text": original,
            "cleaned_text": cleaned,
            "tokens": filtered_tokens,
            "token_count": len(filtered_tokens),
            "raw_token_count": len(tokens),
            "char_count": len(original),
            "vocabulary_size": len(vocab),
            "financial_tokens": financial_tokens,
            "stopwords_removed": stopwords_count
        }

preprocessor = FinancialTextPreprocessor()
