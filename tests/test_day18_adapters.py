"""Offline regression checks for imported Day18 adapters; no models or APIs."""
import sys
from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from src import m2_search, m4_eval


@pytest.mark.parametrize("modern", [True, False])
def test_dense_search_both_client_apis(modern):
    point = SimpleNamespace(payload={"text": "context", "source": "policy"}, score=.8)
    client = SimpleNamespace(collection_exists=lambda **kw: True,
                             get_collection=lambda **kw: SimpleNamespace(points_count=1))
    call = Mock(return_value=SimpleNamespace(points=[point]) if modern else [point])
    setattr(client, "query_points" if modern else "search", call)
    dense = object.__new__(m2_search.DenseSearch)
    dense.client = client
    vector = SimpleNamespace(tolist=lambda: [0.] * m2_search.EMBEDDING_DIM)
    dense._encoder = SimpleNamespace(encode=lambda q: vector)
    rows = dense.search("question")
    assert rows == [m2_search.SearchResult("context", .8, point.payload, "dense")]
    assert ("query" if modern else "query_vector") in call.call_args.kwargs


@pytest.fixture
def evaluator(monkeypatch):
    rows = [{"question": "Q", "answer": "A", "contexts": ["C"], "ground_truth": "GT",
             "faithfulness": .8, "answer_relevancy": .7,
             "context_precision": .6, "context_recall": .5}]
    frame = SimpleNamespace(iterrows=lambda: iter(enumerate(rows)))
    class Frame:
        def __len__(self):
            return len(rows)
        def iterrows(self):
            return frame.iterrows()
    evaluate = Mock(return_value=SimpleNamespace(to_pandas=lambda: Frame()))
    llm = SimpleNamespace(langchain_llm=SimpleNamespace(model_name="actual-llm"))
    embeddings = SimpleNamespace(embeddings=SimpleNamespace(model="actual-embedding"))
    metrics = {name: SimpleNamespace(llm=None, embeddings=None) for name in
               ("faithfulness", "answer_relevancy", "context_precision", "context_recall")}
    for name, module in {
        "ragas": SimpleNamespace(evaluate=evaluate),
        "ragas.metrics": SimpleNamespace(**metrics),
        "ragas.llms": SimpleNamespace(llm_factory=lambda **kw: llm),
        "ragas.embeddings": SimpleNamespace(embedding_factory=lambda **kw: embeddings),
        "datasets": SimpleNamespace(Dataset=SimpleNamespace(from_dict=lambda data: data)),
    }.items():
        monkeypatch.setitem(sys.modules, name, module)
    return rows, evaluate, llm, embeddings


def run_eval():
    return m4_eval.evaluate_ragas(["Q"], ["A"], [["C"]], ["GT"])


def test_evaluator_uses_actual_wrappers(evaluator):
    _, call, llm, embeddings = evaluator
    report = run_eval()
    assert report["metadata"]["evaluator_models"] == ["actual-embedding", "actual-llm"]
    assert len(report["per_question"]) == 1
    assert type(report["per_question"][0].faithfulness) is float
    assert call.call_args.kwargs["raise_exceptions"] is True
    assert call.call_args.kwargs["llm"] is llm
    assert call.call_args.kwargs["embeddings"] is embeddings
    assert all(m.llm is llm for m in call.call_args.kwargs["metrics"])


@pytest.mark.parametrize("bad", [float("nan"), float("inf"), -.1, 1.1])
def test_evaluator_rejects_invalid_metrics(evaluator, bad):
    evaluator[0][0]["faithfulness"] = bad
    with pytest.raises(ValueError, match="metrics"):
        run_eval()


@pytest.mark.parametrize("mutation", ["count", "order", "models", "exception"])
def test_evaluator_fails_clearly(evaluator, mutation):
    rows, call, llm, _ = evaluator
    if mutation == "count":
        rows.clear()
    elif mutation == "order":
        rows[0]["question"] = "different"
    elif mutation == "models":
        llm.langchain_llm.model_name = None
    else:
        call.side_effect = RuntimeError("evaluation failed")
    with pytest.raises((ValueError, RuntimeError)):
        run_eval()


def test_evaluator_validates_lengths_before_imports():
    with pytest.raises(ValueError, match="same length"):
        m4_eval.evaluate_ragas(["Q"], [], [["C"]], ["GT"])
