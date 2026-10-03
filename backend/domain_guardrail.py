"""
Domain Guardrail Engine
PT Chandra Asri Pacific Tbk - CALIBER 2026

Enforces industrial context boundaries and blocks non-technical / out-of-domain
queries (e.g. 'What is the weather in Jakarta today?') before invoking the LLM.
Provides an immutable audit trail for security governance.
"""

import re
from datetime import datetime
from typing import Dict, Any, List

class DomainGuardrail:
    """
    Dual-stage domain filter:
    1. Fast regex pattern rejection for common off-topic themes (weather, general banter, politics).
    2. In-domain engineering keyword density scoring.
    """

    OFF_TOPIC_PATTERNS = [
        r"\b(weather|cuaca|hujan|suhu jakarta|prakiraan)\b",
        r"\b(who is the president|presiden|pemilu|politik|pilpres)\b",
        r"\b(movie|film|lagu|song|celebrity|artis)\b",
        r"\b(football|sepak bola|premier league|liga champion)\b",
        r"\b(tell me a joke|lelucon|cerita lucu|puisi|poem)\b",
        r"\b(crypto|bitcoin|saham non-chandra|forex)\b",
        r"\b(ignore previous instructions|system prompt|jailbreak|DAN mode)\b"
    ]

    IN_DOMAIN_ANCHORS = [
        # Equipment & Core Assets
        "pump", "pompa", "compressor", "kompresor", "reactor", "reaktor", "pressure",
        "tekanan", "temperature", "suhu", "flow", "aliran", "trip", "interlock", "alarm",
        "psll", "pt-", "ga-", "kc-", "dc-", "tk-", "fv-", "pdi-", "fic-", "ti-", "vt-", "vshh-",
        "sop", "p&id", "pid", "rca", "incident", "insiden", "seq-", "matrix", "matriks",
        # Process, Fluid & Plant Context
        "process", "proses", "safety", "keselamatan", "hazard", "psm", "osha", "moc", "sil", "sis", "hazop",
        "hexane", "heksana", "polyethylene", "train a", "plant", "chandra asri", "pabrik",
        # Maintenance & One Point Lesson (OPL)
        "opl", "one point lesson", "lesson", "pelajaran", "alignment", "pelurusan", "laser",
        "thermal growth", "thermal", "growth", "ekspansi", "soft foot", "shim", "shimming",
        "priming", "venting", "vent", "bump start", "jog", "startup", "start-up", "shutdown",
        "vibrasi", "vibration", "bearing", "rms", "transducer", "transmitter",
        # Mechanical & Fluid Dynamics
        "leak", "bocor", "cavitation", "kavitasi", "strainer", "seal", "mechanical seal",
        "seal flush", "plan 11", "plan 62", "npsh", "npsha", "npshr", "flange", "gland",
        "bypass", "recycle", "minimum flow", "min-flow", "impeller", "casing",
        # Engineering Documentation & P&ID Validation
        "drawing", "gambar", "skema", "schematic", "piping", "line spec", "pipe", "pipa",
        "datasheet", "switchover", "maintenance", "troubleshoot", "edms", "aims", "centum",
        "triconex", "work order", "validasi", "verifikasi", "check", "checker", "audit", "draft"
    ]

    def __init__(self):
        self.audit_log: List[Dict[str, Any]] = []

    def validate_query(self, query: str) -> Dict[str, Any]:
        """
        Evaluates incoming natural language query.
        Returns:
            {
                "allowed": bool,
                "reason": str,
                "detected_intent": "in_domain_technical" | "out_of_domain_rejected",
                "timestamp": str,
                "confidence": float
            }
        """
        clean_text = query.strip().lower()
        timestamp = datetime.utcnow().isoformat() + "Z"

        # Check explicit off-topic blacklists
        for pattern in self.OFF_TOPIC_PATTERNS:
            if re.search(pattern, clean_text, re.IGNORECASE):
                log_entry = {
                    "query": query,
                    "allowed": False,
                    "reason": f"Violates domain guardrail: Detected out-of-domain theme '{pattern.strip(r'\\b()')}'",
                    "detected_intent": "out_of_domain_rejected",
                    "timestamp": timestamp,
                    "confidence": 0.99
                }
                self.audit_log.append(log_entry)
                return log_entry

        # Check domain anchor score
        match_count = sum(1 for word in self.IN_DOMAIN_ANCHORS if word in clean_text)

        # Also check if it mentions ISA-5.1 tag format (e.g. GA-1201A, PT-1201)
        tag_match = bool(re.search(r"\b[A-Z]{2,4}[\s\-]?[0-9]{3,4}[A-Z]?\b", query, re.IGNORECASE))

        if match_count > 0 or tag_match:
            return {
                "query": query,
                "allowed": True,
                "reason": "Query is within the plant engineering and operations domain.",
                "detected_intent": "in_domain_technical",
                "anchor_hits": match_count,
                "has_tag_pattern": tag_match,
                "timestamp": timestamp,
                "confidence": min(0.6 + (0.1 * match_count), 0.98)
            }

        # If too ambiguous / short / unrelated
        log_entry = {
            "query": query,
            "allowed": False,
            "reason": "Query lacks plant engineering context. Please specify equipment, instrument tag, or procedure.",
            "detected_intent": "out_of_domain_rejected",
            "timestamp": timestamp,
            "confidence": 0.85
        }
        self.audit_log.append(log_entry)
        return log_entry

    def get_audit_trail(self) -> List[Dict[str, Any]]:
        return self.audit_log[-50:]
