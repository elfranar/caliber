# backend/qdrant_store.py
"""
Qdrant Cloud Vector Store integration for CALIBER RAG pipeline.
Replaces local Chroma with cloud-based Qdrant for production-grade vector search.
"""

from qdrant_client import QdrantClient, models
from sentence_transformers import SentenceTransformer
from typing import Any, Dict, List, Optional
import hashlib

from backend.config_qdrant import QDRANT_API_KEY, QDRANT_URL

# ── Constants ──────────────────────────────────────────────────────────────────
COLLECTION_NAME = "caliber_knowledge"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
EMBEDDING_DIM = 384

# ── Singleton instances ────────────────────────────────────────────────────────
_qdrant_client: Optional[QdrantClient] = None
_embed_model: Optional[SentenceTransformer] = None


def get_qdrant_client() -> QdrantClient:
    """Return a reusable Qdrant Cloud client."""
    global _qdrant_client
    if _qdrant_client is None:
        _qdrant_client = QdrantClient(
            url=QDRANT_URL,
            api_key=QDRANT_API_KEY,
            timeout=30,
        )
    return _qdrant_client


def get_embed_model() -> SentenceTransformer:
    """Return a reusable sentence-transformer embedding model."""
    global _embed_model
    if _embed_model is None:
        _embed_model = SentenceTransformer(EMBEDDING_MODEL)
    return _embed_model


def ensure_collection(collection_name: str = COLLECTION_NAME) -> None:
    """Create the Qdrant collection if it does not already exist."""
    client = get_qdrant_client()
    if not client.collection_exists(collection_name):
        client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(
                size=EMBEDDING_DIM,
                distance=models.Distance.COSINE,
            ),
        )


def upsert_documents(
    texts: List[str],
    payloads: List[Dict[str, Any]],
    collection_name: str = COLLECTION_NAME,
) -> int:
    """
    Embed a list of texts and upsert them into the Qdrant collection.
    Returns the number of points upserted.
    """
    ensure_collection(collection_name)
    client = get_qdrant_client()
    model = get_embed_model()

    vectors = model.encode(texts, show_progress_bar=False).tolist()

    points = []
    for i, (vec, payload) in enumerate(zip(vectors, payloads)):
        # Deterministic ID based on content hash
        point_id = hashlib.md5(texts[i].encode("utf-8")).hexdigest()
        points.append(models.PointStruct(
            id=point_id,
            vector=vec,
            payload=payload,
        ))

    # Batch upsert (max 100 per batch)
    batch_size = 100
    for start in range(0, len(points), batch_size):
        batch = points[start:start + batch_size]
        client.upsert(collection_name=collection_name, points=batch)

    return len(points)


def search(
    query: str,
    top_k: int = 5,
    collection_name: str = COLLECTION_NAME,
    score_threshold: float = 0.3,
    filter_conditions: Optional[Dict[str, Any]] = None,
) -> List[Dict[str, Any]]:
    """
    Perform semantic vector search on Qdrant Cloud.
    Returns a list of results with payload and similarity score.
    """
    ensure_collection(collection_name)
    client = get_qdrant_client()
    model = get_embed_model()

    query_vector = model.encode(query).tolist()

    # Build optional filter
    qdrant_filter = None
    if filter_conditions:
        must_conditions = []
        for key, value in filter_conditions.items():
            must_conditions.append(
                models.FieldCondition(
                    key=key,
                    match=models.MatchValue(value=value),
                )
            )
        qdrant_filter = models.Filter(must=must_conditions)

    hits = client.search(
        collection_name=collection_name,
        query_vector=query_vector,
        limit=top_k,
        score_threshold=score_threshold,
        query_filter=qdrant_filter,
    )

    results = []
    for hit in hits:
        result = dict(hit.payload) if hit.payload else {}
        result["similarity_score"] = round(hit.score, 3)
        result["point_id"] = str(hit.id)
        results.append(result)

    return results
