import re
from typing import List, Dict, Any

KNOWN_ORGANIZATIONS = [
    "NVIDIA Corporation", "NVIDIA Corp", "NVIDIA", "Tesla Inc", "Tesla", "Apple Inc", "Apple",
    "Microsoft Corp", "Microsoft Corporation", "Microsoft", "Amazon.com Inc", "Amazon Web Services", "Amazon",
    "Reliance Industries", "Reliance Retail", "Reliance Jio", "Reliance",
    "Tata Consultancy Services", "TCS", "Infosys Limited", "Infosys",
    "Taiwan Semiconductor Manufacturing Co", "TSMC", "Foxconn", "Pegatron", "Samsung Display", "LG Display",
    "Morgan Stanley", "BlackRock", "European Commission", "Department of Justice", "DOJ",
    "Federal Trade Commission", "FTC", "Securities and Exchange Commission", "SEC",
    "National Highway Traffic Safety Administration", "NHTSA", "OpenAI", "Meta", "Google", "Alphabet",
    "Huawei", "BYD", "Masimo", "IG Metall", "Stiesdal", "Run:ai"
]

KNOWN_PEOPLE = [
    "Jensen Huang", "Elon Musk", "Satya Nadella", "Mukesh Ambani", "Tim Cook",
    "Sundar Pichai", "Mark Zuckerberg", "Andy Jassy"
]

KNOWN_LOCATIONS = [
    "United States", "US", "Americas", "European Union", "EU", "Europe", "Mainland China", "China",
    "Greater China", "Taiwan", "Mexico", "Germany", "India", "Gujarat", "Jamnagar", "Texas",
    "California", "Japan", "United Kingdom", "UK", "Australia", "Ireland", "Virginia", "Berlin"
]

KNOWN_PERIODS = [
    "Q1", "Q2", "Q3", "Q4", "fiscal first quarter", "fiscal second quarter", "fiscal third quarter",
    "fiscal fourth quarter", "third quarter", "fourth quarter", "second quarter", "first quarter",
    "2024", "2025", "2026", "trailing twelve month"
]

class FinancialNER:
    """
    Financial Named Entity Recognition module identifying organizations,
    monetary figures, percentages, key executives, locations, and reporting periods.
    """

    def __init__(self):
        # Regex for monetary amounts: Currency symbol + numbers + optional unit (billion, million, crore, lakh)
        self.money_pattern = re.compile(
            r'([$€£¥₹]\s*\d+(?:[.,]\d+)*(?:\s*(?:billion|million|trillion|crore|lakh|bn|mn|k|b|m))?)'
            r'|(\b\d+(?:[.,]\d+)*\s*(?:crore|lakh|billion|million|trillion)\s*(?:rupees|dollars|euros|pounds)\b)',
            re.IGNORECASE
        )
        # Regex for percentages
        self.percentage_pattern = re.compile(
            r'(\b\d+(?:\.\d+)?%\b|\b\d+(?:\.\d+)?\s*percent\b|\b\d+\s*basis\s*points\b)',
            re.IGNORECASE
        )
        # Regex for dates / financial periods
        self.period_pattern = re.compile(
            r'\b(?:Q[1-4]|first quarter|second quarter|third quarter|fourth quarter|fiscal \d{4}|fiscal [a-z]+ quarter|\d{4})\b',
            re.IGNORECASE
        )

    def extract_entities(self, text: str) -> List[Dict[str, Any]]:
        """
        Extracts verified named entities without hallucination or fake mentions.
        """
        if not text:
            return []

        entities = []
        occupied_spans = []

        def overlaps(start, end):
            for s, e in occupied_spans:
                if max(start, s) < min(end, e):
                    return True
            return False

        # 1. Match Organizations (longest match first)
        sorted_orgs = sorted(KNOWN_ORGANIZATIONS, key=len, reverse=True)
        for org in sorted_orgs:
            for match in re.finditer(rf'\b{re.escape(org)}\b', text, re.IGNORECASE):
                s, e = match.span()
                if not overlaps(s, e):
                    entities.append({
                        "entity": text[s:e],
                        "type": "Organization",
                        "start_char": s,
                        "end_char": e
                    })
                    occupied_spans.append((s, e))

        # 2. Match People
        for person in KNOWN_PEOPLE:
            for match in re.finditer(rf'\b{re.escape(person)}\b', text, re.IGNORECASE):
                s, e = match.span()
                if not overlaps(s, e):
                    entities.append({
                        "entity": text[s:e],
                        "type": "Person",
                        "start_char": s,
                        "end_char": e
                    })
                    occupied_spans.append((s, e))

        # 3. Match Locations
        for loc in KNOWN_LOCATIONS:
            for match in re.finditer(rf'\b{re.escape(loc)}\b', text):
                s, e = match.span()
                if not overlaps(s, e):
                    entities.append({
                        "entity": text[s:e],
                        "type": "Location",
                        "start_char": s,
                        "end_char": e
                    })
                    occupied_spans.append((s, e))

        # 4. Match Monetary amounts
        for match in self.money_pattern.finditer(text):
            s, e = match.span()
            if not overlaps(s, e):
                entities.append({
                    "entity": text[s:e].strip(),
                    "type": "Money",
                    "start_char": s,
                    "end_char": e
                })
                occupied_spans.append((s, e))

        # 5. Match Percentages
        for match in self.percentage_pattern.finditer(text):
            s, e = match.span()
            if not overlaps(s, e):
                entities.append({
                    "entity": text[s:e].strip(),
                    "type": "Percentage",
                    "start_char": s,
                    "end_char": e
                })
                occupied_spans.append((s, e))

        # 6. Match Periods / Dates
        for match in self.period_pattern.finditer(text):
            s, e = match.span()
            if not overlaps(s, e):
                entities.append({
                    "entity": text[s:e].strip(),
                    "type": "Date/Period",
                    "start_char": s,
                    "end_char": e
                })
                occupied_spans.append((s, e))

        # Sort by appearance in text
        entities.sort(key=lambda x: x["start_char"])
        return entities

financial_ner = FinancialNER()
