"""Build equipment catalogs from the official PDF, P&ID, and Excel sources."""

import hashlib
import re
from pathlib import Path
from typing import Any, Dict, List
from backend.case1_ingestion import source_files
from backend.config import DATA_DIR

DATASET_DEFINITIONS = [
    {
        "dataset_id": "dataset_01",
        "dataset_number": 1,
        "dataset_name": "Feed / Pumping System",
        "equipment_tag": "GA-1201A",
        "equipment_tags": ["GA-1201A", "GA-1201B"],
        "description": "Hexane feed pumps, process flow, seal plans, interlocks, OPLs, and maintenance history.",
    },
    {
        "dataset_id": "dataset_02",
        "dataset_number": 2,
        "dataset_name": "Polymer Fluid Bed Dryer",
        "equipment_tag": "YD-2301",
        "equipment_tags": ["YD-2301"],
        "description": "Dryer process, nitrogen purge, interlocks, operating lessons, and maintenance records.",
    },
    {
        "dataset_id": "dataset_03",
        "dataset_number": 3,
        "dataset_name": "Catalyst Reduction Reactor",
        "equipment_tag": "DC-3401A",
        "equipment_tags": ["DC-3401A"],
        "description": "Hydrogen injection, reactor temperature control, safety interlocks, and catalyst procedures.",
    },
    {
        "dataset_id": "dataset_04",
        "dataset_number": 4,
        "dataset_name": "Recycle Gas Compressor",
        "equipment_tag": "KC-4501",
        "equipment_tags": ["KC-4501"],
        "description": "Compressor anti-surge, seal gas, lube oil, cooling water, and trip logic.",
    },
    {
        "dataset_id": "dataset_05",
        "dataset_number": 5,
        "dataset_name": "Solvent Heater",
        "equipment_tag": "EA-5601",
        "equipment_tags": ["EA-5601"],
        "description": "Hexane heating, steam and condensate, fouling monitoring, and heater safeguards.",
    },
    {
        "dataset_id": "dataset_06",
        "dataset_number": 6,
        "dataset_name": "Separation Level Control",
        "equipment_tag": "LV-6701",
        "equipment_tags": ["LV-6701"],
        "description": "Separator level control, instrument air, valve positioner, alarms, and ESD actions.",
    },
    {
        "dataset_id": "dataset_07",
        "dataset_number": 7,
        "dataset_name": "Cooling Tower Fan",
        "equipment_tag": "CT-7801",
        "equipment_tags": ["CT-7801"],
        "description": "Cooling tower fan, gearbox, motor, vibration and temperature interlocks, and spare-cell logic.",
    },
    {
        "dataset_id": "dataset_08",
        "dataset_number": 8,
        "dataset_name": "Solvent Fractionation",
        "equipment_tag": "FA-8901",
        "equipment_tags": ["FA-8901"],
        "description": "Reflux accumulator, pumps, level protection, venting, and start permissives.",
    },
]

_DATASET_BY_TAG = {
    tag: definition
    for definition in DATASET_DEFINITIONS
    for tag in definition["equipment_tags"]
}


def dataset_id_for_equipment_tag(equipment_tag: Any) -> str | None:
    definition = _DATASET_BY_TAG.get(str(equipment_tag or "").strip().upper())
    return definition["dataset_id"] if definition else None


def dataset_id_for_source(path: Path) -> str | None:
    path_text = str(path).replace("\\", "/")
    match = re.search(r"data\s*set\s*0?(\d+)", path_text, re.IGNORECASE)
    if not match:
        match = re.search(r"(?:p\s*&?\s*id|pid)[_ -]*set[_ -]*0?(\d+)", path.name, re.IGNORECASE)
    if not match:
        return None
    dataset_id = f"dataset_{int(match.group(1)):02d}"
    return dataset_id if any(item["dataset_id"] == dataset_id for item in DATASET_DEFINITIONS) else None


def source_document_id(path: Path) -> str:
    opl_match = re.search(r"OPL-[A-Z]{2,5}-\d{3,5}[A-Z]?-\d{2}", path.stem, re.IGNORECASE)
    if opl_match:
        return opl_match.group(0).upper()
    relative_path = path.resolve().relative_to(DATA_DIR.resolve()).as_posix()
    slug = re.sub(r"[^A-Za-z0-9]+", "_", path.stem).strip("_").lower()
    digest = hashlib.sha1(relative_path.encode("utf-8")).hexdigest()[:8]
    return f"{slug}_{digest}"


def source_category(path: Path) -> str:
    name = path.name.casefold()
    if path.suffix.casefold() in {".png", ".jpg", ".jpeg", ".tif", ".tiff"} or "p&id" in name or name.startswith("pid"):
        return "pid"
    if "opl" in name or "one point lesson" in name:
        return "opl"
    if "interlock" in name or "logic" in name:
        return "interlock_logic"
    if "datasheet" in name:
        return "equipment_datasheet"
    if "plot plan" in name:
        return "plot_plan"
    return "engineering_document"


def _source_record(path: Path) -> Dict[str, Any]:
    return {
        "source_id": source_document_id(path),
        "file_name": path.name,
        "source_file": path.relative_to(DATA_DIR).as_posix(),
        "category": source_category(path),
        "file_type": path.suffix.lstrip(".").lower(),
        "content": "",
        "approval_status": "unverified",
        "approved_by": None,
    }


def load_dataset_manifests() -> List[Dict[str, Any]]:
    """Group official source files by dataset without reading generated JSON manifests."""
    workbook_paths = sorted((DATA_DIR / "Maintenance Data").glob("*.xlsx"))
    workbook = workbook_paths[0] if workbook_paths else None
    grouped_sources: Dict[str, List[Dict[str, Any]]] = {
        definition["dataset_id"]: [] for definition in DATASET_DEFINITIONS
    }

    for source_path in source_files():
        dataset_id = dataset_id_for_source(source_path)
        if dataset_id:
            grouped_sources[dataset_id].append(_source_record(source_path))

    manifests = []
    for definition in DATASET_DEFINITIONS:
        dataset_id = definition["dataset_id"]
        equipment_tag = definition["equipment_tag"]
        sources = grouped_sources[dataset_id]
        if workbook:
            sources.append({
                "source_id": f"maintenance_history_{dataset_id}",
                "file_name": workbook.name,
                "source_file": workbook.relative_to(DATA_DIR).as_posix(),
                "category": "maintenance_history",
                "file_type": "xlsx",
                "content": "",
                "approval_status": "unverified",
                "approved_by": None,
            })
        manifests.append({
            "manifest_file": None,
            "dataset_id": dataset_id,
            "dataset_name": definition["dataset_name"],
            "description": definition["description"],
            "equipment_tag": equipment_tag,
            "equipment_name": definition["dataset_name"],
            "aliases": definition["equipment_tags"],
            "approval_status": "unverified",
            "sources": sources,
        })
    return manifests