"""Topic classification for the Manufacturing Knowledge Hub."""

from __future__ import annotations

import re

from backend.domain_guardrail import DomainGuardrail

RELEVANT = "RELEVAN"
NOT_RELEVANT = "TIDAK_RELEVAN"


def _offline_classification(query: str) -> str:
    """Use the repository's deterministic domain rules without cloud access."""
    result = DomainGuardrail().validate_query(query)
    if result["allowed"]:
        return RELEVANT
    if result["reason"].startswith("Violates domain guardrail"):
        return NOT_RELEVANT

    requested_domain_patterns = (
        r"\bteknik\s+kimia\b",
        r"\bchemical\s+engineering\b",
        r"\bpetrochemical\b",
        r"\bpetrokimia\b",
        r"\brefinery\b",
        r"\bkilang(?:\s+minyak)?\b",
        r"\bmaintenance\s+kilang\b",
        r"\b(?:k3|hse|ehs)\b",
        r"\bindustrial\s+(?:health|safety|environment)\b",
        r"\boperasional\s+pabrik\b",
        r"\bplant\s+operations?\b",
    )
    return (
        RELEVANT
        if any(re.search(pattern, query, re.IGNORECASE) for pattern in requested_domain_patterns)
        else NOT_RELEVANT
    )


def classify_query(query: str, chat_model: object | None = None) -> str:
    """Classify plant and petrochemical questions using offline rules only."""
    return _offline_classification(query.strip())


def check_relevance(query: str, chat_model: object | None = None) -> str:
    """Backward-friendly alias for :func:`classify_query`."""
    return classify_query(query, chat_model=chat_model)