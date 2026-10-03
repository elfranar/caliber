"""
Score Normalization, Reciprocal Rank Fusion (RRF), and Confidence Scoring
PT Chandra Asri Pacific Tbk - CALIBER 2026

Transforms heterogeneous evidence (Graph topology, Vector similarity, and Telemetry delta)
into a unified, explainable trust index for plant engineers.
"""

from typing import Dict, Any, List, Literal, Optional

INTENT_WEIGHTS = {
    "relational": {"graph": 0.60, "semantic": 0.30, "structured": 0.10},
    "factual": {"graph": 0.10, "semantic": 0.75, "structured": 0.15},
    "real_time": {"graph": 0.20, "semantic": 0.15, "structured": 0.65},
    "hybrid": {"graph": 0.35, "semantic": 0.35, "structured": 0.30}
}


class ScoringFusionEngine:
    INTENT_WEIGHTS = INTENT_WEIGHTS

    @staticmethod
    def normalize_graph_score(hop_count: int, edge_type: str = "FEEDS", decay: float = 0.7) -> float:
        edge_weights = {
            "FEEDS": 1.0,
            "PART_OF": 0.85,
            "HAS_PARAMETER": 0.90,
            "DESCRIBED_BY": 0.75,
            "HAS_INCIDENT": 0.85
        }
        w = edge_weights.get(edge_type, 0.5)
        hop = max(1, hop_count)
        return round(w * (decay ** (hop - 1)), 3)

    @staticmethod
    def normalize_semantic_score(raw_similarity: float) -> float:
        return max(0.0, min(1.0, round(raw_similarity, 3)))

    @staticmethod
    def normalize_structured_score(current_val: float, setpoint: float, trip_limit: float) -> float:
        """
        Proximity score to trip point:
        0.0 = safely at or above normal operating setpoint.
        1.0 = has touched or breached the trip boundary.
        """
        span = setpoint - trip_limit
        if span == 0:
            return 0.0
        proximity = (setpoint - current_val) / span
        return max(0.0, min(1.0, round(proximity, 3)))

    @classmethod
    def weighted_sum_fusion(cls, source_scores: Dict[str, float], intent: str = "factual") -> float:
        """
        Calculates explainable fused score. Source weights are transparently visible in the UI.
        """
        weights = INTENT_WEIGHTS.get(intent, INTENT_WEIGHTS["factual"])
        available = {s: w for s, w in weights.items() if s in source_scores}

        if not available:
            return 0.0

        weight_sum = sum(available.values())
        fused = sum(source_scores[s] * w for s, w in available.items()) / weight_sum
        return round(fused, 3)

    @classmethod
    def rrf_fusion(cls, ranked_lists: Dict[str, List[str]], k: int = 60) -> Dict[str, float]:
        """
        Reciprocal Rank Fusion standard for enterprise hybrid search.
        Formula: RRF_score(d) = sum_{s in sources} 1 / (k + rank_s(d))
        """
        scores: Dict[str, float] = {}
        for source, ranked_ids in ranked_lists.items():
            for rank, item_id in enumerate(ranked_ids, start=1):
                scores[item_id] = scores.get(item_id, 0.0) + (1.0 / (k + rank))
        # Round scores
        return {item_id: round(score, 4) for item_id, score in scores.items()}

    @classmethod
    def compute_confidence(
        cls,
        fused_score: float,
        corroborating_sources: int,
        approval_status: str = "approved"
    ) -> Dict[str, Any]:
        """
        Generates the trust badge indicator for the engineer console:
        - Agreement bonus: +0.10 for 2 sources, +0.20 for 3 sources.
        - Approval penalty: -0.30 if document is draft / unapproved.
        """
        agreement_bonus = min(max(0, corroborating_sources - 1), 2) * 0.10
        approval_penalty = 0.0 if approval_status == "approved" else 0.30

        raw_confidence = fused_score + agreement_bonus - approval_penalty
        final_confidence = max(0.05, min(0.99, round(raw_confidence, 2)))

        if final_confidence >= 0.85:
            level = "HIGH_CONFIDENCE"
            badge_color = "#10B981"  # Emerald Green
            ui_label = "Verified & Corroborated"
        elif final_confidence >= 0.65:
            level = "MEDIUM_CONFIDENCE"
            badge_color = "#F59E0B"  # Amber
            ui_label = "Moderate (Requires SOP Cross-Check)"
        else:
            level = "LOW_CONFIDENCE"
            badge_color = "#EF4444"  # Red
            ui_label = "Unverified (HITL Review Required)"

        return {
            "confidence_score": final_confidence,
            "confidence_percentage": int(final_confidence * 100),
            "level": level,
            "badge_color": badge_color,
            "ui_label": ui_label,
            "agreement_bonus": round(agreement_bonus, 2),
            "approval_penalty": round(approval_penalty, 2),
            "corroborating_sources_count": corroborating_sources
        }
