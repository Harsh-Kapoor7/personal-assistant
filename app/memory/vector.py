from __future__ import annotations
import os
from typing import List
import numpy as np

from sentence_transformers import SentenceTransformer
import faiss
from app.config import settings

VEC_DIR = os.path.join(settings.app_data_dir, "vectors")
os.makedirs(VEC_DIR, exist_ok=True)
INDEX_PATH = os.path.join(VEC_DIR, "commitments.faiss")
EMB_PATH = os.path.join(VEC_DIR, "model.txt")

_model = None
_index = None


def _load_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def _load_index(dim: int = 384):
    global _index
    if _index is None:
        if os.path.exists(INDEX_PATH):
            _index = faiss.read_index(INDEX_PATH)
        else:
            _index = faiss.IndexFlatIP(dim)
    return _index


def upsert_texts(texts: List[str]):
    model = _load_model()
    index = _load_index()
    vecs = model.encode(texts, normalize_embeddings=True)
    index.add(np.array(vecs, dtype="float32"))
    faiss.write_index(index, INDEX_PATH)
    with open(EMB_PATH, "w") as f:
        f.write("all-MiniLM-L6-v2")


def search(query: str, k: int = 5) -> List[str]:
    if not os.path.exists(INDEX_PATH):
        return []
    model = _load_model()
    index = _load_index()
    q = model.encode([query], normalize_embeddings=True).astype("float32")
    D, I = index.search(q, k)
    # In a real app we’d persist the raw texts separately; for Phase-1,
    # we simply return placeholders (demonstration only)
    return [f"match_{i}_score_{float(D[0][rank]):.3f}" for rank, i in enumerate(I[0])]