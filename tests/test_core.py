import pytest
from fastapi.testclient import TestClient
from app.core import chunk_text, build_context
from app.main import app


def test_chunking_overlap():
    chunks = chunk_text("abcdefghij", chunk_size=6, overlap=2)
    assert chunks == ["abcdef", "efghij"]


def test_empty_text():
    assert chunk_text(" \n\t ") == []


def test_bad_chunk_config():
    with pytest.raises(ValueError):
        chunk_text("content", chunk_size=10, overlap=10)


def test_context_deduplicates_sources():
    context, sources = build_context([
        {"source": "guide.txt", "content": "Part one"},
        {"source": "guide.txt", "content": "Part two"},
    ])
    assert sources == ["guide.txt"]
    assert "Part two" in context


def test_health():
    response = TestClient(app).get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_invalid_question_rejected():
    response = TestClient(app).post("/ask", json={"question": ""})
    assert response.status_code == 422
