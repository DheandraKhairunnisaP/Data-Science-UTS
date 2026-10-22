import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_valid_schema_and_exact_offsets():
    title = "Malaysia and Maybank Announce New Plans"
    body = "Maybank said the company would expand its services in Kuala Lumpur on October 22, 2026."
    response = client.post("/extract-entities", json={"title": title, "body": body})
    assert response.status_code == 200
    data = response.json()
    assert set(data) == {"entities", "meta"}
    assert data["meta"]["entity_count"] == len(data["entities"])
    combined = title + "\n" + body
    for ent in data["entities"]:
        assert set(ent) == {"text", "label", "start", "end"}
        assert combined[ent["start"]:ent["end"]] == ent["text"]
        assert ent["label"] in {"PERSON", "ORG", "GPE", "LOC", "DATE", "EVENT"}

def test_empty_title_rejected():
    assert client.post("/extract-entities", json={"title": " ", "body": "Article text."}).status_code == 400

def test_empty_body_rejected():
    assert client.post("/extract-entities", json={"title": "Headline", "body": " "}).status_code == 400

def test_non_string_field_rejected():
    assert client.post("/extract-entities", json={"title": 42, "body": "Article text."}).status_code == 400

def test_title_limit():
    assert client.post("/extract-entities", json={"title": "T"*501, "body": "Article text."}).status_code == 400

def test_body_limit():
    assert client.post("/extract-entities", json={"title": "Headline", "body": "x"*10001}).status_code == 400

def test_malformed_json_rejected():
    response = client.post("/extract-entities", content="{bad json", headers={"Content-Type": "application/json"})
    assert response.status_code == 400

def test_repeat_request_deterministic():
    payload = {"title": "Malaysia and Maybank Announce New Plans", "body": "Maybank said the company would expand in Kuala Lumpur."}
    assert client.post("/extract-entities", json=payload).json() == client.post("/extract-entities", json=payload).json()

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
