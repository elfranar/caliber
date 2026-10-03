"""
Asset Tag & Intent Entity Extraction
PT Chandra Asri Pacific Tbk - CALIBER 2026

Hybrid NER Pipeline:
1. ISA-5.1 Regex matcher for deterministic formal engineering tags.
2. RapidFuzz matching for informal colloquial operator descriptions.
3. Multi-slot intent classification (Relational, Factual/SOP, Real-time telemetry).
"""

import re
import json
from dataclasses import dataclass, asdict
from typing import Dict, Any, List, Optional
from backend.config import REGISTRY_PATH, FUNCTION_CODES, EQUIPMENT_PREFIXES
from backend.dataset_catalog import load_dataset_manifests

try:
    from rapidfuzz import fuzz
except ImportError:
    fuzz = None


@dataclass
class ResolvedEntity:
    tag: str
    name: str
    category: str  # "asset" or "parameter"
    asset_type: str
    matched_via: str  # "exact_tag" or "description_fuzzy"
    confidence: float
    metadata: Dict[str, Any]


class EntityExtractor:
    TAG_PATTERN = re.compile(r"\b([A-Z]{2,5})[\s\-]?(\d{3,5})([A-Z]?)\b", re.IGNORECASE)

    RELATIONAL_KEYWORDS = [
        "downstream", "upstream", "affect", "impact", "connected", "leads to",
        "dampak", "pengaruh", "terhubung", "aliran", "hilir", "hulu", "cascade"
    ]
    FACTUAL_KEYWORDS = [
        "how to", "procedure", "sop", "opl", "one point lesson", "startup", "shutdown",
        "switchover", "priming", "venting", "alignment", "laser", "cold alignment",
        "hot check", "bearing", "thermal growth", "cara", "langkah", "prosedur",
        "pedoman", "action", "spec", "datasheet", "rca", "root cause", "troubleshooting"
    ]
    REALTIME_KEYWORDS = [
        "current", "now", "reading", "value", "trip limit", "pressure now", "status",
        "berapa", "sekarang", "nilai", "kondisi", "setpoint", "alarm", "vibration",
        "vshh", "vt-1201", "getaran", "temperature", "suhu"
    ]

    def __init__(self, registry_path=REGISTRY_PATH):
        self.registry = self._load_registry(registry_path)

    def _load_registry(self, path) -> Dict[str, Any]:
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                registry = json.load(f)
        else:
            registry = {"assets": {}, "parameters": {}}

        assets = registry.setdefault("assets", {})
        for manifest in load_dataset_manifests():
            tag = manifest.get("equipment_tag")
            if not tag:
                continue
            assets.setdefault(tag, {
                "asset_tag": tag,
                "asset_name": manifest.get("equipment_name") or tag,
                "asset_type": "equipment",
                "description": manifest.get("description", ""),
                "aliases": manifest.get("aliases", []),
                "dataset_id": manifest.get("dataset_id"),
            })
        return registry

    def extract_candidate_tags(self, text: str) -> List[str]:
        """Pulls all strings matching ISA-5.1 tag formats."""
        matches = self.TAG_PATTERN.findall(text.upper())
        candidates = []
        for prefix, number, suffix in matches:
            candidates.append(f"{prefix}-{number}{suffix}")
            # Also add unhyphenated form for lookup flexibility
            candidates.append(f"{prefix}{number}{suffix}")
        return list(dict.fromkeys(candidates))

    def resolve_entities(self, text: str) -> List[ResolvedEntity]:
        candidates = self.extract_candidate_tags(text)
        resolved: List[ResolvedEntity] = []
        seen_tags = set()

        # 1. Exact match pass against Asset & Parameter registries
        for c in candidates:
            # Try with hyphen and without
            normalized_c = c.replace(" ", "-")
            prefix = normalized_c.split("-")[0]
            number_suffix = "-".join(normalized_c.split("-")[1:]) if "-" in normalized_c else ""

            # Check assets
            for tag, meta in self.registry.get("assets", {}).items():
                if tag.replace("-", "") == c.replace("-", ""):
                    if tag not in seen_tags:
                        seen_tags.add(tag)
                        resolved.append(ResolvedEntity(
                            tag=tag,
                            name=meta.get("asset_name", tag),
                            category="asset",
                            asset_type=meta.get("asset_type", "equipment"),
                            matched_via="exact_tag",
                            confidence=1.0,
                            metadata=meta
                        ))

            # Check parameters
            for tag, meta in self.registry.get("parameters", {}).items():
                if tag.replace("-", "") == c.replace("-", ""):
                    if tag not in seen_tags:
                        seen_tags.add(tag)
                        resolved.append(ResolvedEntity(
                            tag=tag,
                            name=meta.get("parameter_name", tag),
                            category="parameter",
                            asset_type=meta.get("source_system", "telemetry"),
                            matched_via="exact_tag",
                            confidence=1.0,
                            metadata=meta
                        ))

        # 2. Fuzzy match pass on asset descriptions if no exact tag was matched
        if not resolved and fuzz is not None:
            text_lower = text.lower()
            query_terms = set(re.findall(r"[a-z0-9]+", text_lower))
            for tag, meta in self.registry.get("assets", {}).items():
                name = meta.get("asset_name", "").lower()
                aliases = [alias.lower() for alias in meta.get("aliases", [])]
                names = [name, *aliases]
                candidate_terms = set(re.findall(r"[a-z0-9]+", " ".join(names)))
                meaningful_overlap = {
                    term for term in query_terms & candidate_terms
                    if len(term) >= 4
                }
                if not meaningful_overlap:
                    continue

                best_score = max(fuzz.token_set_ratio(text_lower, candidate) for candidate in names if candidate)

                if best_score >= 75 and tag not in seen_tags:
                    seen_tags.add(tag)
                    resolved.append(ResolvedEntity(
                        tag=tag,
                        name=meta.get("asset_name", tag),
                        category="asset",
                        asset_type=meta.get("asset_type", "equipment"),
                        matched_via="description_fuzzy",
                        confidence=round(best_score / 100.0, 2),
                        metadata=meta
                    ))

        return resolved

    def classify_intent(self, text: str) -> Dict[str, Any]:
        text_lower = text.lower()
        rel_hits = sum(1 for k in self.RELATIONAL_KEYWORDS if k in text_lower)
        fact_hits = sum(1 for k in self.FACTUAL_KEYWORDS if k in text_lower)
        rt_hits = sum(1 for k in self.REALTIME_KEYWORDS if k in text_lower)

        # Primary intent determination
        intent_scores = {
            "relational": rel_hits,
            "factual": fact_hits,
            "real_time": rt_hits
        }
        max_score = max(intent_scores.values())
        if max_score == 0:
            primary_intent = "factual"  # Default assumption
        else:
            primary_intent = max(intent_scores, key=intent_scores.get)

        is_hybrid = sum(1 for score in intent_scores.values() if score > 0) > 1

        return {
            "primary_intent": primary_intent,
            "is_hybrid": is_hybrid,
            "activated_paths": {
                "graph_traversal": rel_hits > 0 or "relational" == primary_intent,
                "semantic_search": fact_hits > 0 or "factual" == primary_intent or max_score == 0,
                "structured_query": rt_hits > 0 or "real_time" == primary_intent
            },
            "intent_scores": intent_scores
        }

    def process(self, query: str) -> Dict[str, Any]:
        entities = self.resolve_entities(query)
        intent = self.classify_intent(query)
        return {
            "query": query,
            "resolved_entities": [asdict(e) for e in entities],
            "intent": intent,
            "has_confident_entities": len(entities) > 0 and entities[0].confidence >= 0.8
        }
