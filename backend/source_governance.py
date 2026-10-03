"""Persistent human approval state for searchable source documents and rows."""

from __future__ import annotations

import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from threading import RLock
from typing import Any

from backend.config import DATA_DIR

APPROVALS_PATH = DATA_DIR / "source_approvals.json"
_lock = RLock()


def maintenance_approval_id(source_file: str, sheet_name: str, row_index: int) -> str:
    return f"maintenance:{source_file}:{sheet_name}:{row_index}"


def _read_approvals() -> dict[str, dict[str, Any]]:
    if not APPROVALS_PATH.exists():
        return {}
    try:
        payload = json.loads(APPROVALS_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise RuntimeError(f"Could not read source approval registry: {error}") from error
    if not isinstance(payload, dict):
        raise RuntimeError("Source approval registry must contain a JSON object.")
    return payload


def get_source_approval(approval_id: str) -> dict[str, Any]:
    with _lock:
        approvals = _read_approvals()
        approval = approvals.get(approval_id)
        if approval is None and approval_id.startswith("maintenance:"):
            source_parts = approval_id.split(":")
            for prefix_length in range(len(source_parts) - 1, 1, -1):
                approval = approvals.get(":".join(source_parts[:prefix_length]) + ":*")
                if approval is not None:
                    break
    if not isinstance(approval, dict):
        return {"approval_status": "unverified", "approved_by": None}
    return {
        "approval_status": approval.get("approval_status", "unverified"),
        "approved_by": approval.get("approved_by"),
    }


def set_source_approval(
    approval_id: str,
    approval_status: str,
    approved_by: str | None,
) -> dict[str, Any]:
    if approval_status not in {"approved", "rejected", "unverified"}:
        raise ValueError("Approval status must be approved, rejected, or unverified.")
    with _lock:
        approvals = _read_approvals()
        if approval_status == "unverified":
            approvals.pop(approval_id, None)
            result = {"approval_status": "unverified", "approved_by": None}
        else:
            result = {
                "approval_status": approval_status,
                "approved_by": approved_by,
                "updated_at": datetime.now(timezone.utc).isoformat(),
            }
            approvals[approval_id] = result

        APPROVALS_PATH.parent.mkdir(parents=True, exist_ok=True)
        handle, temporary_path = tempfile.mkstemp(
            prefix="source_approvals_",
            suffix=".tmp",
            dir=APPROVALS_PATH.parent,
        )
        try:
            with os.fdopen(handle, "w", encoding="utf-8") as stream:
                json.dump(approvals, stream, indent=2)
                stream.write("\n")
            os.replace(temporary_path, APPROVALS_PATH)
        except OSError:
            try:
                os.unlink(temporary_path)
            except OSError:
                pass
            raise
    return result


def list_source_approvals() -> dict[str, dict[str, Any]]:
    with _lock:
        return _read_approvals()
