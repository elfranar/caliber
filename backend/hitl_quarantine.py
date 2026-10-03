"""
Human-In-The-Loop (HITL) Data Quality & Conflict Quarantine Engine
PT Chandra Asri Pacific Tbk - CALIBER 2026

Design Rationale & Intellectual Honesty:
- Conflict detection in this pipeline is strictly DETERMINISTIC AND RULE-BASED,
  not machine learning. It performs field-level cross-checks across heterogeneous
  documents (e.g., P&ID drawing notes vs. mechanical equipment datasheets).
- Treating conflict detection as rule-based is an intentional engineering choice:
  safety-critical petrochemical parameter validation requires deterministic,
  auditable, and zero-hallucination verification before any record reaches
  the vector database.
- Conflicted or unapproved records are held in a staging quarantine table until
  a designated Subject Matter Expert (SME) reviews and authorizes them.
"""

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
from backend.case1_ingestion import markdown_output_path, source_files
from backend.config import DATA_DIR, QUARANTINE_PATH
from backend.dataset_catalog import source_document_id
from backend.source_governance import maintenance_approval_id, set_source_approval


class HITLQuarantineManager:
    def __init__(self, quarantine_path=QUARANTINE_PATH):
        self.quarantine_path = quarantine_path
        self.data_dir = DATA_DIR
        self.records: List[Dict[str, Any]] = []
        self._load()
        self._merge_detected_conflicts()
        self.total_sources = self._count_sources()

    def _load(self):
        if self.quarantine_path.exists():
            with open(self.quarantine_path, "r", encoding="utf-8") as f:
                self.records = json.load(f)
        else:
            self.records = []

    def _save(self):
        with open(self.quarantine_path, "w", encoding="utf-8") as f:
            json.dump(self.records, f, indent=2)

    def _read_sources(self):
        documents = {}
        records = []
        for source_path in source_files():
            markdown_path = markdown_output_path(source_path)
            if not markdown_path.is_file():
                continue
            text = markdown_path.read_text(encoding="utf-8", errors="replace")
            documents[source_document_id(source_path)] = {
                "doc_id": source_document_id(source_path),
                "file_name": source_path.name,
                "source_file": source_path.relative_to(self.data_dir).as_posix(),
                "text": text,
            }

        workbook_dir = self.data_dir / "Maintenance Data"
        for workbook_path in sorted(workbook_dir.rglob("*.xlsx")) if workbook_dir.exists() else []:
            try:
                import pandas as pd
            except ImportError:
                break
            for sheet_name, frame in pd.read_excel(workbook_path, sheet_name=None).items():
                if str(sheet_name).casefold() == "explanation":
                    continue
                for row_offset, row in frame.iterrows():
                    values = {
                        str(column): self._excel_value(value)
                        for column, value in row.items()
                    }
                    records.append({
                        **values,
                        "approval_id": maintenance_approval_id(
                            workbook_path.relative_to(self.data_dir).as_posix(),
                            str(sheet_name),
                            int(row_offset) + 2,
                        ),
                        "work_order": values.get("WO_Number"),
                        "root_cause_code": values.get("Root_Cause"),
                        "corrective_action": values.get("Corrective_Action"),
                        "failure_mode": values.get("Problem_Description"),
                    })
        return documents, records

    @staticmethod
    def _excel_value(value: Any) -> Any:
        if value is None:
            return None
        if hasattr(value, "isoformat"):
            try:
                return value.isoformat()
            except (TypeError, ValueError):
                pass
        try:
            import pandas as pd

            if pd.isna(value):
                return None
        except (ImportError, TypeError, ValueError):
            pass
        return value.item() if hasattr(value, "item") else value

    def _count_sources(self) -> int:
        source_count = len(source_files())
        workbook_dir = self.data_dir / "Maintenance Data"
        return source_count + sum(1 for _ in workbook_dir.rglob("*.xlsx")) if workbook_dir.exists() else source_count

    def _merge_detected_conflicts(self):
        documents, records = self._read_sources()
        candidates = []

        pid_text = "\n".join(
            document["text"]
            for document in documents.values()
            if Path(document["source_file"]).suffix.casefold() in {".png", ".jpg", ".jpeg", ".tif", ".tiff"}
        )
        engineering_text = "\n".join(document["text"] for document in documents.values())
        placeholder = re.search(r"TJC[- ]LLD[- ]PID[- ]XXXX", pid_text, re.IGNORECASE)
        expected_pid = re.search(r"TJC[- ]LLD[- ]PID[- ]\d+", engineering_text, re.IGNORECASE)
        if placeholder and expected_pid:
            source_ids = [
                document["doc_id"]
                for document in documents.values()
                if Path(document["source_file"]).suffix.casefold()
                in {".png", ".jpg", ".jpeg", ".tif", ".tiff"}
                or expected_pid.group(0).casefold() in document["text"].casefold()
            ]
            candidates.append({
                "conflict_id": "AUTO-PID-REFERENCE-1201",
                "source_approval_ids": source_ids,
                "source_system": "P&ID source image vs parsed engineering documents",
                "document_ref": "P&ID Data / supporting data pdf",
                "conflict_type": "Placeholder drawing number",
                "severity": "HIGH",
                "issue_description": f"A supplied P&ID image contains {placeholder.group(0)} while parsed engineering documents reference {expected_pid.group(0)}.",
                "quarantined_payload": {"drawing_number": placeholder.group(0), "expected_reference": expected_pid.group(0)},
            })

        pid_plan_two = re.search(r"API\s+PLAN\s+II\b", pid_text, re.IGNORECASE)
        datasheet_plan_eleven = re.search(r"API\s+PLAN\s+11\s*\+\s*PLAN\s+62", engineering_text, re.IGNORECASE)
        if pid_plan_two and datasheet_plan_eleven:
            source_ids = [
                document["doc_id"]
                for document in documents.values()
                if pid_plan_two.group(0).casefold() in document["text"].casefold()
                or datasheet_plan_eleven.group(0).casefold() in document["text"].casefold()
            ]
            candidates.append({
                "conflict_id": "AUTO-SEAL-FLUSH-PLAN-1201",
                "source_approval_ids": source_ids,
                "source_system": "P&ID source image vs parsed equipment datasheet/OPL",
                "document_ref": "GA-1201A P&ID / datasheet / OPL",
                "conflict_type": "Seal flush plan notation mismatch",
                "severity": "HIGH",
                "issue_description": "The supplied P&ID image says API Plan II while parsed engineering text specifies API Plan 11 + Plan 62.",
                "quarantined_payload": {"drawing_text": pid_plan_two.group(0), "technical_reference": datasheet_plan_eleven.group(0)},
            })

        for work_order in records:
            completeness = self.check_work_order_completeness(work_order)
            if work_order.get("work_order") and completeness:
                wo_number = work_order["work_order"]
                candidates.append({
                    "conflict_id": f"AUTO-WO-INCOMPLETE-{wo_number}",
                    "source_approval_ids": [work_order["approval_id"]],
                    "source_system": "Maintenance History Excel workbook",
                    "document_ref": wo_number,
                    "conflict_type": "Incomplete maintenance failure record",
                    "severity": "MEDIUM",
                    "issue_description": completeness["description"],
                    "quarantined_payload": work_order,
                })

        existing_ids = {record.get("conflict_id") for record in self.records}
        timestamp = datetime.utcnow().isoformat() + "Z"
        for conflict in candidates:
            if conflict["conflict_id"] in existing_ids:
                existing = next(
                    record
                    for record in self.records
                    if record.get("conflict_id") == conflict["conflict_id"]
                )
                if not existing.get("source_approval_ids"):
                    existing["source_approval_ids"] = conflict.get("source_approval_ids", [])
                    if existing.get("status") in {"APPROVED_BY_SME", "REJECTED"}:
                        approval_status = (
                            "approved"
                            if existing["status"] == "APPROVED_BY_SME"
                            else "rejected"
                        )
                        for approval_id in existing["source_approval_ids"]:
                            set_source_approval(
                                approval_id,
                                approval_status,
                                existing.get("resolved_by"),
                            )
                continue
            self.records.append({
                **conflict,
                "detected_at": timestamp,
                "status": "QUARANTINED",
                "assigned_sme": None,
                "resolution_notes": None,
            })
            existing_ids.add(conflict["conflict_id"])

    # -----------------------------------------------------------------------
    # Deterministic Rule-Based Cross-Checks (Genuinely Non-ML / Auditable)
    # -----------------------------------------------------------------------
    @staticmethod
    def cross_check_design_pressure(datasheet_val: str, drawing_note_val: str) -> Optional[Dict[str, Any]]:
        """Rule 1: Deterministic numerical check between P&ID note and Datasheet casing rating."""
        if datasheet_val != drawing_note_val:
            return {
                "rule": "RULE-DESIGN-PRESS-MISMATCH",
                "severity": "HIGH",
                "description": f"Design pressure contradiction: Datasheet specifies '{datasheet_val}' while drawing note cites '{drawing_note_val}'."
            }
        return None

    @staticmethod
    def check_work_order_completeness(wo: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Rule 2: Schema validation ensuring required failure analysis fields are populated."""
        missing = []
        required_fields = {
            "root cause": ("root_cause_code", "Root_Cause"),
            "corrective action": ("corrective_action", "Corrective_Action"),
            "problem description": ("failure_mode", "Problem_Description"),
        }
        for label, field_names in required_fields.items():
            if not any(wo.get(field_name) for field_name in field_names):
                missing.append(label)
        if missing:
            return {
                "rule": "RULE-WO-INCOMPLETE",
                "severity": "MEDIUM",
                "description": f"Incomplete work order {wo.get('work_order') or wo.get('WO_Number')}: Missing critical fields [{', '.join(missing)}]."
            }
        return None

    @staticmethod
    def check_document_governance(doc: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Rule 3: Enforce formal MOC and Chief Engineer approval stamp."""
        if doc.get("approval_status") != "approved" or not doc.get("approved_by"):
            return {
                "rule": "RULE-GOVERNANCE-UNAPPROVED",
                "severity": "HIGH",
                "description": f"Unapproved document {doc.get('doc_id')}: Missing formal management sign-off stamp."
            }
        return None

    # -----------------------------------------------------------------------
    # Quarantine Management & Promotion Workflow
    # -----------------------------------------------------------------------
    def list_all(self, status_filter: Optional[str] = None) -> List[Dict[str, Any]]:
        if status_filter:
            return [r for r in self.records if r.get("status") == status_filter]
        return self.records

    def get_metrics(self) -> Dict[str, Any]:
        quarantined = sum(1 for r in self.records if r.get("status") == "QUARANTINED")
        approved = sum(1 for r in self.records if r.get("status") == "APPROVED_BY_SME")
        rejected = sum(1 for r in self.records if r.get("status") == "REJECTED")

        clean = max(0, self.total_sources - quarantined)
        health = round((clean / self.total_sources) * 100, 1) if self.total_sources else 100.0
        return {
            "total_ingested_sources": self.total_sources,
            "clean_active_chunks": clean,
            "quarantined_conflicts": quarantined,
            "sme_approved_promoted": approved,
            "rejected_purged": rejected,
            "data_health_score": health,
            "detection_method": "Deterministic Rule-Based Cross-Checks (Auditable)"
        }

    def resolve_item(self, conflict_id: str, action: str, sme_name: str, notes: str) -> Dict[str, Any]:
        """
        SME Decision Workflow:
        - APPROVE: Promotes quarantined record to clean vector index.
        - REJECT: Purges record from active indexing while preserving audit log.
        """
        normalized_action = action.upper()
        if normalized_action not in {"APPROVE", "REJECT"}:
            raise ValueError("Action must be APPROVE or REJECT.")
        for r in self.records:
            if r["conflict_id"] == conflict_id:
                now_str = datetime.utcnow().isoformat() + "Z"
                if normalized_action == "APPROVE":
                    r["status"] = "APPROVED_BY_SME"
                    r["resolved_by"] = sme_name
                    r["resolved_at"] = now_str
                    r["resolution_notes"] = notes or "Manually reviewed and authorized for AI vector memory by SME."
                    approval_status = "approved"
                else:
                    r["status"] = "REJECTED"
                    r["resolved_by"] = sme_name
                    r["resolved_at"] = now_str
                    r["resolution_notes"] = notes or "Contradiction confirmed. Blocked permanently from vector index."
                    approval_status = "rejected"
                for approval_id in r.get("source_approval_ids", []):
                    set_source_approval(approval_id, approval_status, sme_name)
                self._save()
                return {"success": True, "record": r}

        return {"success": False, "error": f"Conflict ID '{conflict_id}' not found."}
