"""Lexical reranker used when a cross-encoder is not available."""
from dataclasses import dataclass
import re
from config import RERANK_TOP_K

@dataclass
class RerankResult:
    text: str
    score: float
    metadata: dict

class CrossEncoderReranker:
    def rerank(self, query: str, documents: list[dict], top_k: int = RERANK_TOP_K) -> list[RerankResult]:
        terms = set(re.findall(r"\w+", query.lower(), flags=re.UNICODE))
        output = [RerankResult(row["text"], row.get("score", 0) + len(terms & set(re.findall(r"\w+", row["text"].lower(), flags=re.UNICODE))) / max(1, len(terms)), row.get("metadata", {})) for row in documents]
        return sorted(output, key=lambda row: row.score, reverse=True)[:top_k]
