"""AI Service — newsworthiness scoring, entity extraction, summarisation."""
import logging
from typing import Optional
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


class AIService:
    """Thin wrapper for AI / LLM calls. Real implementation can use OpenAI, Anthropic, etc."""

    def __init__(self, db: Optional[Session] = None):
        self.db = db

    def generate_summary(self, content: str, max_tokens: int = 150) -> str:
        """Generate a concise summary for article content."""
        if not content:
            return ""
        # Stub: truncate as a fallback
        return content[:max_tokens] + ("..." if len(content) > max_tokens else "")

    def generate_newsworthiness(self, title: str, content: str = "", source_name: str = "") -> float:
        """Compute a newsworthiness score (0-100) based on heuristics.

        Real implementation: send to LLM for scoring.
        Stub: rule-based heuristic.
        """
        score = 50.0

        # Title length heuristic
        if title:
            words = title.split()
            if 5 <= len(words) <= 15:
                score += 10
            elif len(words) > 25:
                score -= 5

        # Breaking / urgent keywords
        urgent_words = ["breaking", "urgent", "alert", "exclusive", "just in", "developing", "launch"]
        title_lower = title.lower() if title else ""
        for w in urgent_words:
            if w in title_lower:
                score += 8
                break

        # Source credibility bonus (stub)
        high_cred_sources = ["reuters", "bloomberg", "associated press", "bbc", "nature", "science", "arxiv"]
        if source_name and any(s in source_name.lower() for s in high_cred_sources):
            score += 10

        # Content richness
        if content and len(content) > 500:
            score += 5

        return min(100.0, max(0.0, score))

    def extract_keywords(self, text: str, top_k: int = 10) -> list[str]:
        """Extract keywords from text. Stub: simple word-frequency."""
        if not text:
            return []
        import re
        from collections import Counter

        # Simple stopwords
        stopwords = {
            "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
            "have", "has", "had", "do", "does", "did", "will", "would", "could",
            "should", "may", "might", "can", "shall", "to", "of", "in", "for",
            "on", "with", "at", "by", "from", "as", "into", "through", "during",
            "before", "after", "above", "below", "between", "and", "but", "or",
            "nor", "not", "so", "yet", "both", "either", "neither", "each", "every",
            "all", "any", "few", "more", "most", "other", "some", "such", "no",
            "only", "own", "same", "than", "too", "very", "just", "about", "now",
            "it", "its", "this", "that", "these", "those", "he", "she", "they",
            "him", "her", "them", "his", "their", "what", "which", "who", "whom",
            "when", "where", "why", "how", "if", "then", "also", "here", "there",
        }
        words = re.findall(r"\b[a-zA-Z]{3,}\b", text.lower())
        filtered = [w for w in words if w not in stopwords]
        counter = Counter(filtered)
        return [word for word, _ in counter.most_common(top_k)]

    def extract_entities(self, text: str) -> list[str]:
        """Extract named entities. Stub: keyword + proper-noun heuristic."""
        if not text:
            return []
        keywords = self.extract_keywords(text, top_k=20)
        # Heuristic: capitalized words not at sentence start likely entities
        import re
        capitalized = re.findall(r"\b[A-Z][a-z]+\b", text)
        return list(dict.fromkeys(keywords[:10] + capitalized[:10]))[:15]


ai_service = AIService()
