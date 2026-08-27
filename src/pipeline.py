"""Runnable local Day 18 RAG pipeline."""
from src.m1_chunking import load_documents, chunk_hierarchical
from src.m2_search import HybridSearch
from src.m3_rerank import CrossEncoderReranker

def build_pipeline():
    chunks = []
    for document in load_documents():
        _, children = chunk_hierarchical(document["text"], metadata=document["metadata"])
        chunks.extend({"text": child.text, "metadata": child.metadata} for child in children)
    search = HybridSearch(); search.index(chunks)
    return search, CrossEncoderReranker()

def run_query(query, search, reranker):
    results = search.search(query)
    ranked = reranker.rerank(query, [{"text": r.text, "score": r.score, "metadata": r.metadata} for r in results])
    contexts = [item.text for item in ranked]
    return (contexts[0] if contexts else "Không tìm thấy thông tin liên quan trong chính sách."), contexts
