"""
Configuration and Master Metadata for Manufacturing Knowledge Hub
PT Chandra Asri Pacific Tbk - CALIBER 2026
"""

from pathlib import Path

# Base Paths (Centralized, persistent paths - No fragile relative pathing)
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
REGISTRY_PATH = DATA_DIR / "asset_registry.json"
GRAPH_PATH = DATA_DIR / "topology_graph.json"
QUARANTINE_PATH = DATA_DIR / "quarantine_store.json"

# Operational Constants
DEFAULT_DECAY_RATE = 0.70  # Hop distance decay factor: 0.7^(hop - 1)
SIMILARITY_METRIC = "cosine_normalized"  # Bounded strictly between 0.0 and 1.0

# Deployment Architecture Modes
DEPLOYMENT_MODES = {
    "ON_PREMISE_SECURE": {
        "name": "On-Premise Air-Gapped (Llama-3-70B Local)",
        "data_classification": "Confidential / Proprietary Chemical Data",
        "cloud_transit": False,
        "compliance": "Internal Petrochemical Security & Data Governance"
    },
    "HYBRID_CLOUD": {
        "name": "Hybrid Cloud Gateway",
        "data_classification": "Sanitized Public Queries Only",
        "cloud_transit": True,
        "compliance": "Selective PII & Secret Redaction Required"
    }
}

CURRENT_DEPLOYMENT = "ON_PREMISE_SECURE"

# ISA-5.1 Instrument & Equipment Codes
FUNCTION_CODES = {
    "PT": "Pressure Transmitter",
    "PI": "Pressure Indicator",
    "PSLL": "Pressure Switch Low-Low (Trip)",
    "TI": "Temperature Indicator",
    "FIC": "Flow Indicating Controller",
    "LAHH": "Level Alarm High-High",
    "PDT": "Pressure Differential Transmitter",
    "VT": "Vibration Transmitter"
}

EQUIPMENT_PREFIXES = {
    "GA": "Centrifugal / Rotary Pump",
    "DC": "Reactor / Polymerization Vessel",
    "KC": "Process Gas Compressor",
    "TK": "Storage Tank / Surge Drum",
    "HE": "Heat Exchanger / Reboiler",
    "FV": "Flow Control Valve",
    "MOV": "Motor Operated Valve"
}
