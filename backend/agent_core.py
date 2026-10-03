"""Orchestrate topic checks, evidence retrieval, and traceable answers."""

from __future__ import annotations

import html
import logging
from pathlib import Path
from typing import Any

from backend.database import DatabaseConfigurationError, retrieve_context
from backend.guardrails import NOT_RELEVANT, classify_query

_logger = logging.getLogger(__name__)
_REFUSAL = (
    "Sorry, your question is outside the scope of plant operations. This information "
    "is not available in the Manufacturing Knowledge Hub database."
)
_local_vector_engine: Any | None = None


def _xml_tag(tag: str, content: str) -> str:
    """Safely wrap untrusted or model-generated text in a simple XML tag."""
    return f"<{tag}>{html.escape(content, quote=False)}</{tag}>"


def _get_local_evidence(query: str, top_k: int = 5) -> list[dict[str, Any]]:
    """Retrieve evidence from the application-wide offline search engine."""
    global _local_vector_engine
    if _local_vector_engine is None:
        try:
            from backend.main import vector_engine

            _local_vector_engine = vector_engine
        except (ImportError, AttributeError):
            from backend.vector_engine import NormalizedVectorEngine

            _local_vector_engine = NormalizedVectorEngine()
    return _local_vector_engine.search(query, top_k=top_k)


def _retrieve_evidence(query: str) -> tuple[list[dict[str, Any]], str]:
    """Prefer the new Chroma index, then use the existing offline RAG index."""
    try:
        context = retrieve_context(query)
        if context:
            return context, "local Chroma"
    except (DatabaseConfigurationError, ImportError, RuntimeError, ValueError) as error:
        _logger.info("Chroma retrieval unavailable; using existing local index: %s", error)
    except Exception as error:
        _logger.warning("Chroma retrieval failed; using existing local index: %s", error)

    try:
        return _get_local_evidence(query), "existing local index"
    except Exception as error:
        _logger.exception("Existing local retrieval failed: %s", error)
        return [], "local index unavailable"


def _source_text(item: dict[str, Any]) -> str:
    """Extract text from either a Chroma result or existing vector result."""
    return str(item.get("text") or item.get("retrieval_text") or item.get("content") or "").strip()


def _source_metadata(item: dict[str, Any]) -> dict[str, Any]:
    """Normalize provenance fields for the response and prompt."""
    metadata = item.get("metadata")
    if isinstance(metadata, dict):
        return metadata
    return {
        "doc_id": item.get("doc_id") or item.get("chunk_id") or "unknown",
        "title": item.get("title") or item.get("source_file") or "Untitled source",
        "approval_status": item.get("approval_status", "unverified"),
        "source_file": item.get("source_file"),
        "version": item.get("version"),
    }


def _build_evidence_answer(query: str, evidence: list[dict[str, Any]]) -> str:
    """Build a conservative response from retrieved text without an LLM."""
    if not evidence:
        return (
            "Sufficient evidence was not found in the database. I will not infer "
            "procedures or operating limits without an appropriate source. Verify "
            "controlled documents and escalate to an SME before field action."
        )

    sections = ["Retrieved technical context for the question: " + query]
    for item in evidence[:3]:
        metadata = _source_metadata(item)
        title = metadata.get("title") or metadata.get("source_file") or "Untitled source"
        doc_id = metadata.get("doc_id") or metadata.get("source_file") or "unknown"
        approval = metadata.get("approval_status", "unverified")
        excerpt = _source_text(item)
        sections.append(f"[{doc_id}] {title} ({approval})\n{excerpt[:1800]}")
    sections.append(
        "Use this information as a reference, not as an automatic field instruction. "
        "Check tags, revisions, and actual conditions against controlled copies; "
        "unverified sources must be confirmed by an SME."
    )
    return "\n\n".join(sections)


def process_input(user_query: str) -> dict[str, Any]:
    """Process one technical query and return auditable structured output.

    LlamaParse requires explicit cloud consent and its API key. Embeddings,
    guardrails, and answer synthesis remain local and deterministic.

    Args:
        user_query: Natural-language question from an engineer.

    Returns:
        A dictionary with ``status``, XML-wrapped ``thinking_logs``, XML-wrapped
        ``answer``, and optional ``generated_image_url``.
    """
    query = user_query.strip()
    if not query:
        return {
            "status": "TIDAK_RELEVAN",
            "thinking_logs": [_xml_tag("thinking", "Empty query rejected.")],
            "answer": _xml_tag("answer", _REFUSAL),
            "generated_image_url": None,
        }

    logs: list[str] = []
    relevance = classify_query(query)
    logs.append(_xml_tag("thinking", f"Guardrail classified the query as: {relevance}."))
    if relevance == NOT_RELEVANT:
        return {
            "status": NOT_RELEVANT,
            "thinking_logs": logs,
            "answer": _xml_tag("answer", _REFUSAL),
            "generated_image_url": None,
        }

    evidence, retrieval_source = _retrieve_evidence(query)
    logs.append(_xml_tag(
        "thinking",
        f"Search completed via {retrieval_source}; found {len(evidence)} relevant sources.",
    ))
    image_evidence = [
        item for item in evidence
        if "image" in str(_source_metadata(item).get("file_type", "")).lower()
        or Path(str(_source_metadata(item).get("source_file", ""))).suffix.lower()
        in {".png", ".jpg", ".jpeg", ".webp", ".tif", ".tiff"}
    ]
    if image_evidence:
        logs.append(_xml_tag(
            "thinking",
            f"Image/P&ID context analysis used {len(image_evidence)} retrieved OCR results.",
        ))
    else:
        logs.append(_xml_tag("thinking", "No matching image/P&ID OCR results were found for this search."))

    answer_text = _build_evidence_answer(query, evidence)
    logs.append(_xml_tag("thinking", "Answer synthesized locally from retrieved sources."))

    return {
        "status": "RELEVAN",
        "thinking_logs": logs,
        "answer": _xml_tag("answer", answer_text),
        "generated_image_url": None,
    }