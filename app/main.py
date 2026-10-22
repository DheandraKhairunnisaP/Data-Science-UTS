from __future__ import annotations
import os
from pathlib import Path
from typing import Any

import spacy
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse

BASE_DIR = Path(__file__).resolve().parents[1]
MODEL_DIR = Path(os.environ.get("NER_MODEL_PATH", str(BASE_DIR / "models" / "ner_custom_v1")))
MAX_TITLE_CHARS = int(os.environ.get("NER_MAX_TITLE_CHARS", "500"))
MAX_BODY_CHARS = int(os.environ.get("NER_MAX_BODY_CHARS", "10000"))
TARGET_LABELS = {"PERSON", "ORG", "GPE", "LOC", "DATE", "EVENT"}

if not (MODEL_DIR / "config.cfg").is_file():
    raise RuntimeError(
        f"Model spaCy tidak ditemukan di '{MODEL_DIR}'. "
        "Pastikan model Role 2 diekstrak ke models/ner_custom_v1/."
    )

nlp = spacy.load(MODEL_DIR)
nlp.max_length = max(nlp.max_length, MAX_TITLE_CHARS + MAX_BODY_CHARS + 10)
MODEL_NAME = "ner_custom_v1 (spaCy)"

app = FastAPI(title="Article Named-Entity Recognition Service",
              description="Extract named entities from an article title and body.",
              version="1.0.0")

@app.get("/", response_class=HTMLResponse)
def home() -> str:
    html_path = BASE_DIR / "web" / "index.html"
    if not html_path.is_file():
        raise HTTPException(status_code=500, detail="File antarmuka web tidak ditemukan.")
    return html_path.read_text(encoding="utf-8")

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "model": MODEL_NAME, "spacy_version": spacy.__version__}

@app.get("/model-info")
def model_info() -> dict[str, Any]:
    return {
        "model": MODEL_NAME,
        "pipeline": nlp.pipe_names,
        "supported_output_labels": sorted(TARGET_LABELS),
        "model_ner_labels": list(nlp.get_pipe("ner").labels),
        "max_title_chars": MAX_TITLE_CHARS,
        "max_body_chars": MAX_BODY_CHARS,
        "offset_convention": "zero-based; start inclusive; end exclusive; title + newline + body",
    }

@app.post("/extract-entities")
async def extract_entities(request: Request) -> dict[str, Any]:
    try:
        payload = await request.json()
    except Exception as exc:
        raise HTTPException(status_code=400, detail="Request body harus berupa JSON yang valid.") from exc
    if not isinstance(payload, dict):
        raise HTTPException(status_code=400, detail="JSON harus berbentuk object dengan field title dan body.")

    title, body = payload.get("title"), payload.get("body")
    if not isinstance(title, str) or not isinstance(body, str):
        raise HTTPException(status_code=400, detail="Field title dan body wajib berupa string.")
    title, body = title.strip(), body.strip()
    if not title:
        raise HTTPException(status_code=400, detail="Judul artikel tidak boleh kosong.")
    if not body:
        raise HTTPException(status_code=400, detail="Isi artikel tidak boleh kosong.")
    if len(title) > MAX_TITLE_CHARS:
        raise HTTPException(status_code=400, detail=f"Judul artikel maksimal {MAX_TITLE_CHARS} karakter.")
    if len(body) > MAX_BODY_CHARS:
        raise HTTPException(status_code=400, detail=f"Isi artikel maksimal {MAX_BODY_CHARS} karakter.")

    analyzed_text = title + "\n" + body
    doc = nlp(analyzed_text)
    entities = [
        {"text": ent.text, "label": ent.label_, "start": int(ent.start_char), "end": int(ent.end_char)}
        for ent in doc.ents if ent.label_ in TARGET_LABELS
    ]
    return {"entities": entities, "meta": {
        "entity_count": len(entities), "model": MODEL_NAME,
        "text_convention": "title + newline + body"
    }}
