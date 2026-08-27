"""Small compatibility implementation of the Day 18 RAGAS adapter.

Use this offline-safe adapter when the full Day 18 module is unavailable.
"""
from dataclasses import dataclass

@dataclass
class MetricResult:
    faithfulness: float
    answer_relevancy: float
    context_precision: float
    context_recall: float

def _overlap(left, right):
    a, b = set(left.lower().split()), set(right.lower().split())
    return len(a & b) / max(1, len(a))

def evaluate_ragas(questions, answers, contexts, ground_truths):
    per_question = []
    for question, answer, context, truth in zip(questions, answers, contexts, ground_truths):
        joined = " ".join(context)
        per_question.append(MetricResult(
            round(_overlap(answer, joined), 3), round(_overlap(question, answer), 3),
            round(_overlap(joined, truth), 3), round(_overlap(truth, joined), 3)))
    metrics = ("faithfulness", "answer_relevancy", "context_precision", "context_recall")
    return {**{metric: round(sum(getattr(row, metric) for row in per_question) / max(1, len(per_question)), 3) for metric in metrics},
            "per_question": per_question}
