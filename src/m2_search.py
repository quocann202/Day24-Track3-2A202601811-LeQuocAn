"""Portable lexical hybrid-search fallback for the Day 18 pipeline."""
from dataclasses import dataclass
import re

@dataclass
class SearchResult:
    text: str
    score: float
    metadata: dict

def _tokens(text: str) -> set[str]:
    return set(re.findall(r"\w+", text.lower(), flags=re.UNICODE))

class HybridSearch:
    def __init__(self): self.chunks = []
    def index(self, chunks: list[dict]) -> None: self.chunks = chunks
    def search(self, query: str, top_k: int = 20) -> list[SearchResult]:
        query_tokens = _tokens(query)
        scored = []
        for chunk in self.chunks:
            words = _tokens(chunk["text"])
            score = len(query_tokens & words) / max(1, len(query_tokens))
            scored.append(SearchResult(chunk["text"], score, chunk.get("metadata", {})))
        return sorted(scored, key=lambda item: item.score, reverse=True)[:top_k]
