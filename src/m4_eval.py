from __future__ import annotations

"""Module 4: RAGAS Evaluation — 4 metrics + failure analysis."""

import os, sys, json
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")
from dataclasses import dataclass
from math import isfinite

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import TEST_SET_PATH, RAGAS_LLM_MODEL, RAGAS_EMBEDDING_MODEL


@dataclass
class EvalResult:
    question: str
    answer: str
    contexts: list[str]
    ground_truth: str
    faithfulness: float
    answer_relevancy: float
    context_precision: float
    context_recall: float


def load_test_set(path: str = TEST_SET_PATH) -> list[dict]:
    """Load test set from JSON. (Đã implement sẵn)"""
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def evaluate_ragas(questions: list[str], answers: list[str],
                   contexts: list[list[str]], ground_truths: list[str]) -> dict:
    """Evaluate every row with explicit evaluator models; propagate failures."""
    metric_names = ("faithfulness", "answer_relevancy",
                    "context_precision", "context_recall")
    inputs = (questions, answers, contexts, ground_truths)
    if not all(isinstance(values, list) for values in inputs):
        raise ValueError("All evaluation inputs must be lists")
    if len({len(values) for values in inputs}) != 1 or not questions:
        raise ValueError("Evaluation requires non-empty inputs of the same length")
    if not all(isinstance(value, str) for values in
               (questions, answers, ground_truths) for value in values):
        raise ValueError("Questions, answers and ground truths must contain strings")
    if not all(isinstance(row, list) and all(isinstance(c, str) for c in row)
               for row in contexts):
        raise ValueError("Contexts must be list[list[str]]")

    from copy import deepcopy
    import torch  # RAGAS can import datasets/pyarrow transitively.
    from ragas import evaluate
    from ragas.metrics import (faithfulness, answer_relevancy,
                               context_precision, context_recall)
    from ragas.llms import llm_factory
    from ragas.embeddings import embedding_factory
    from datasets import Dataset

    llm = llm_factory(model=RAGAS_LLM_MODEL)
    embeddings = embedding_factory(model=RAGAS_EMBEDDING_MODEL)
    # Read IDs from the actual wrappers passed to evaluation, not JUDGE_MODEL.
    llm_id = getattr(getattr(llm, "langchain_llm", None), "model_name", None)
    embedding_id = getattr(getattr(embeddings, "embeddings", None), "model", None)
    if any(not isinstance(value, str) or not value.strip() or value != value.strip()
           for value in (llm_id, embedding_id)):
        raise ValueError("Cannot identify actual RAGAS evaluator LLM/embedding models")
    metrics = deepcopy([faithfulness, answer_relevancy, context_precision, context_recall])
    # Fresh metric objects prevent previously configured global metrics overriding models.
    for metric in metrics:
        if hasattr(metric, "llm"):
            metric.llm = llm
        if hasattr(metric, "embeddings"):
            metric.embeddings = embeddings
    dataset = Dataset.from_dict({
        "question": questions, "answer": answers,
        "contexts": contexts, "ground_truth": ground_truths,
    })
    result = evaluate(dataset, metrics=metrics, llm=llm, embeddings=embeddings,
                      raise_exceptions=True)
    frame = result.to_pandas()
    if len(frame) != len(questions):
        raise ValueError("RAGAS returned an unexpected number of records")
    per_question = []
    for i, (_, row) in enumerate(frame.iterrows()):
        if (row["question"] != questions[i] or row["answer"] != answers[i]
                or list(row["contexts"]) != contexts[i]
                or row["ground_truth"] != ground_truths[i]):
            raise ValueError(f"RAGAS row {i} does not match input order/content")
        scores = {name: float(row[name]) for name in metric_names}
        if any(not isfinite(value) or not 0 <= value <= 1 for value in scores.values()):
            raise ValueError(f"RAGAS row {i} has non-finite or out-of-range metrics")
        per_question.append(EvalResult(questions[i], answers[i], list(contexts[i]),
                                       ground_truths[i], **scores))
    return {**{name: sum(getattr(row, name) for row in per_question) / len(per_question)
               for name in metric_names},
            "per_question": per_question,
            "metadata": {"evaluator_models": sorted({llm_id, embedding_id})}}



def failure_analysis(eval_results: list[EvalResult], bottom_n: int = 10) -> list[dict]:
    """Analyze bottom-N worst questions using Diagnostic Tree."""
    if bottom_n <= 0:
        return []
    diagnostic_tree = {
        "faithfulness": ("LLM hallucination", "Tighten the prompt and set temperature=0"),
        "context_recall": ("Retrieval missed relevant chunks", "Improve chunking and BM25 retrieval"),
        "context_precision": ("Irrelevant context", "Improve reranking and metadata filtering"),
        "answer_relevancy": ("Answer is off-topic", "Improve the generation prompt"),
    }
    failures = []
    for result in eval_results:
        scores = {name: float(getattr(result, name)) for name in diagnostic_tree}
        # RAGAS may return NaN for failed metrics; those rows cannot be ranked.
        if not all(isfinite(score) for score in scores.values()):
            continue
        average = sum(scores.values()) / len(scores)
        worst_metric = min(scores, key=scores.get)
        diagnosis, suggested_fix = diagnostic_tree[worst_metric]
        failures.append({"question": result.question, "worst_metric": worst_metric,
                         "score": average, "diagnosis": diagnosis,
                         "suggested_fix": suggested_fix})
    return sorted(failures, key=lambda failure: failure["score"])[:bottom_n]



def save_report(results: dict, failures: list[dict], path: str = "reports/ragas_report.json"):
    """Save evaluation report to JSON. (Đã implement sẵn)"""
    parent_dir = os.path.dirname(path)
    if parent_dir:
        os.makedirs(parent_dir, exist_ok=True)
    report = {
        "aggregate": {k: v for k, v in results.items() if k != "per_question"},
        "num_questions": len(results.get("per_question", [])),
        "failures": failures,
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"Report saved to {path}")


if __name__ == "__main__":
    test_set = load_test_set()
    print(f"Loaded {len(test_set)} test questions")
    print("Run pipeline.py first to generate answers, then call evaluate_ragas().")
