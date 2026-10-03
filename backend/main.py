"""
Manufacturing Knowledge Hub - FastAPI Server
PT Chandra Asri Pacific Tbk - CALIBER 2026
Case 1: AI-Powered Knowledge Integration
"""

from fastapi import Depends, FastAPI, Header, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Literal, Optional
import os
import re
import html
import secrets

from dotenv import load_dotenv
load_dotenv()

from backend.config import BASE_DIR, CURRENT_DEPLOYMENT, DEPLOYMENT_MODES
from backend.domain_guardrail import DomainGuardrail
from backend.entity_extractor import EntityExtractor
from backend.knowledge_graph import KnowledgeGraphEngine
from backend.vector_engine import NormalizedVectorEngine
from backend.scoring_fusion import ScoringFusionEngine
from backend.hitl_quarantine import HITLQuarantineManager
from backend.event_simulator import SENSOR_CONFIGS, TelemetryEventSimulator
from backend.document_ingestion import extract_uploaded_document
from backend.dataset_catalog import DATASET_DEFINITIONS, dataset_id_for_equipment_tag
from backend.source_governance import set_source_approval
from backend.case1_api import router as case1_router

app = FastAPI(
    title="Chandra Asri Manufacturing Knowledge Hub",
    description="Trusted, Traceable, and Topologically-Aware AI Architecture for Petrochemical Plant Operations",
    version="1.0.0"
)
app.include_router(case1_router)

# Same-origin browser access does not require CORS. Permit only explicit local
# development origins for clients that do.
allowed_origins = [
    origin.strip()
    for origin in os.getenv(
        "CALIBER_ALLOWED_ORIGINS",
        "http://127.0.0.1:8000,http://localhost:8000",
    ).split(",")
    if origin.strip()
]
if "*" in allowed_origins:
    raise RuntimeError("CALIBER_ALLOWED_ORIGINS must not contain the wildcard origin '*'.")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Core Industrial AI Engines
guardrail = DomainGuardrail()
extractor = EntityExtractor()
graph_engine = KnowledgeGraphEngine()
vector_engine = NormalizedVectorEngine()
fusion_engine = ScoringFusionEngine()
quarantine_mgr = HITLQuarantineManager()
telemetry_sim = TelemetryEventSimulator()

active_deployment = CURRENT_DEPLOYMENT


class QueryRequest(BaseModel):
    query: str
    asset_context_override: Optional[str] = None
    image_data: Optional[str] = None
    image_name: Optional[str] = None
    dataset_id: Optional[str] = None
    mode: Literal["rag", "pid_audit"] = "rag"


class AgentProcessRequest(BaseModel):
    query: str


class QuarantineResolveRequest(BaseModel):
    conflict_id: str
    action: Literal["APPROVE", "REJECT"]
    sme_name: str = Field(min_length=1, max_length=120)
    notes: Optional[str] = Field(default="", max_length=2000)


class SourceApprovalRequest(BaseModel):
    approval_id: str = Field(min_length=1, max_length=500)
    approval_status: Literal["approved", "rejected", "unverified"]


class DeploymentToggleRequest(BaseModel):
    mode: str  # "ON_PREMISE_SECURE" or "HYBRID_CLOUD"


class PIDValidationRequest(BaseModel):
    drawing_title: Optional[str] = "P&ID Schematic Draft (Feed Pump GA-1201A/B)"
    drawing_author: Optional[str] = "Junior Process Engineer"
    sample_id: Optional[str] = "DRAFT-JR-01"
    raw_notes: Optional[str] = None
    image_name: Optional[str] = None
    image_data: Optional[str] = None


def authenticate_sme(x_sme_token: str = Header(default="")) -> str:
    """Require a configured SME credential; caller-supplied names are not identity."""
    configured_key = os.getenv("SME_API_KEY", "")
    if not configured_key:
        raise HTTPException(
            status_code=503,
            detail="SME actions are disabled until SME_API_KEY is configured.",
        )
    if not secrets.compare_digest(x_sme_token, configured_key):
        raise HTTPException(status_code=403, detail="A valid SME API token is required.")
    return os.getenv("SME_APPROVER_NAME", "SME API key holder")


def _compare_uploaded_document(uploaded: Dict[str, Any], asset_tag: Optional[str], master_chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
    uploaded_text = uploaded.get("text", "")
    if len(uploaded_text.strip()) < 20:
        return {
            "verdict": "INSUFFICIENT_EXTRACTED_EVIDENCE",
            "detected_equipment": asset_tag,
            "message": "The document did not yield enough OCR text/tags for comparison. No discrepancies can be concluded.",
            "discrepancies": [],
            "ocr_items": uploaded.get("ocr_items", []),
            "source_name": uploaded.get("file_name"),
            "comparison_scope": "No extracted text; no visual conclusions made.",
            "master_sources": [],
        }

    tag_pattern = re.compile(r"\b[A-Z]{2,5}[\s-]?\d{3,5}[A-Z]?\b", re.IGNORECASE)
    master_chunks = [
        chunk for chunk in master_chunks
        if chunk.get("section_id") in {"pid", "P&ID Specs", "interlock_logic", "interlock_matrix", "equipment_datasheet"}
        or "pid" in chunk.get("doc_id", "").lower()
    ]
    master_text = "\n".join(chunk.get("retrieval_text") or chunk.get("content", "") for chunk in master_chunks)
    uploaded_tags = {match.group(0).upper().replace(" ", "-") for match in tag_pattern.finditer(uploaded_text)}
    master_tags = {match.group(0).upper().replace(" ", "-") for match in tag_pattern.finditer(master_text)}
    master_sources = [
        {"doc_id": chunk["doc_id"], "title": chunk["title"], "approval_status": chunk["approval_status"]}
        for chunk in master_chunks[:8]
    ]

    if not asset_tag or not master_chunks or not master_tags:
        return {
            "verdict": "INSUFFICIENT_MASTER_CONTEXT",
            "detected_equipment": asset_tag,
            "message": "A matching asset or P&ID master could not be identified from the indexed context.",
            "discrepancies": [],
            "ocr_items": uploaded.get("ocr_items", []),
            "source_name": uploaded.get("file_name"),
            "comparison_scope": "OCR tag presence only; no pipe connectivity or symbol semantics inferred.",
            "master_sources": master_sources,
        }

    missing_tags = sorted(master_tags - uploaded_tags)
    unexpected_tags = sorted(uploaded_tags - master_tags)
    locations = {}
    for item in uploaded.get("ocr_items", []):
        for match in tag_pattern.finditer(item.get("text", "")):
            tag = match.group(0).upper().replace(" ", "-")
            locations.setdefault(tag, []).append({"page": item.get("page"), "bbox": item.get("bbox"), "confidence": item.get("confidence")})

    discrepancies = [
        {
            "item": "Master tag not detected in uploaded drawing",
            "tag": tag,
            "severity": "REVIEW",
            "golden_standard": "Tag appears in retrieved master document.",
            "draft_finding": "OCR did not detect this tag in the uploaded drawing.",
            "hazard_impact": "Potential omission; OCR miss is also possible.",
            "required_correction": "Inspect this item manually on the drawing and verify against the cited master source.",
            "location": locations.get(tag, []),
        }
        for tag in missing_tags[:30]
    ]
    return {
        "verdict": "OCR_TAG_REVIEW_REQUIRED" if discrepancies else "OCR_TAGS_MATCHED",
        "detected_equipment": asset_tag,
        "message": f"OCR detected {len(uploaded_tags)} unique tags; {len(missing_tags)} master tags were not detected.",
        "discrepancies": discrepancies,
        "matched_tags": sorted(uploaded_tags & master_tags),
        "unexpected_tags": unexpected_tags[:30],
        "tag_locations": locations,
        "ocr_items": uploaded.get("ocr_items", []),
        "source_name": uploaded.get("file_name"),
        "comparison_scope": "OCR tag presence only. This does not validate line routing, symbol semantics, or safety logic connectivity.",
        "master_sources": master_sources,
    }


# ---------------------------------------------------------------------------
# API Routes
# ---------------------------------------------------------------------------

@app.get("/api/status")
def get_system_status():
    q_metrics = quarantine_mgr.get_metrics()
    return {
        "system": "Manufacturing Knowledge Hub",
        "plant": "Cilegon Petrochemical Complex",
        "process_unit": "Polyethylene Plant - Train A",
        "deployment_mode": active_deployment,
        "deployment_details": DEPLOYMENT_MODES.get(active_deployment, {}),
        "data_ops_metrics": q_metrics,
        "active_assets": sum(1 for node in graph_engine.nodes.values() if node.get("type") == "asset"),
        "indexed_chunks": len(vector_engine.chunks)
    }


@app.get("/api/assets")
def list_assets():
    return sorted(
        [
            {
                "tag": node["id"],
                "name": node.get("name", node["id"]),
                "asset_type": node.get("asset_type", "equipment"),
                "criticality": node.get("criticality", "Unspecified"),
                "dataset_id": node.get("dataset_id"),
            }
            for node in graph_engine.nodes.values()
            if node.get("type") == "asset"
        ],
        key=lambda asset: (asset["dataset_id"] or "", asset["tag"]),
    )


@app.get("/api/datasets")
def list_datasets():
    document_counts = {}
    for chunk in vector_engine.chunks:
        dataset_id = chunk.get("dataset_id")
        if dataset_id:
            document_counts.setdefault(dataset_id, set()).add(chunk["doc_id"])
    return [
        {**definition, "document_count": len(document_counts.get(definition["dataset_id"], set()))}
        for definition in DATASET_DEFINITIONS
    ]


@app.post("/api/deployment/toggle")
def toggle_deployment(req: DeploymentToggleRequest):
    global active_deployment
    if req.mode in DEPLOYMENT_MODES:
        active_deployment = req.mode
        return {"success": True, "active_mode": active_deployment, "details": DEPLOYMENT_MODES[active_deployment]}
    raise HTTPException(status_code=400, detail="Invalid deployment mode")


@app.post("/api/validate-pid")
def validate_pid_schematic(req: PIDValidationRequest):
    """Compare uploaded drawing OCR tags with retrieved, asset-linked master evidence."""
    if not req.image_data:
        raise HTTPException(status_code=422, detail="Attach a drawing image or PDF before requesting a P&ID comparison.")

    candidate_context = f"{req.drawing_title or ''} {req.raw_notes or ''}"
    assets = [entity for entity in extractor.resolve_entities(candidate_context) if entity.category == "asset"]
    if not assets:
        raise HTTPException(status_code=422, detail="The drawing scope must identify an equipment tag found in the connected catalog.")

    target = assets[0].tag
    query_result = process_query(QueryRequest(
        query=f"Compare the P&ID drawing for {target} against the connected master.",
        asset_context_override=target,
        image_data=req.image_data,
        image_name=req.image_name or req.drawing_title or "uploaded-drawing",
    ))
    comparison = query_result.get("image_analysis")
    if not comparison:
        return {
            "verdict": "INSUFFICIENT_EXTRACTED_EVIDENCE",
            "detected_equipment": target,
            "message": "The file was received, but there is insufficient OCR tag evidence for an audit.",
            "discrepancies": [],
            "master_sources": query_result.get("sources", [])[:4],
        }
    return comparison



@app.post("/api/agent/process")
def process_agent_input(req: AgentProcessRequest):
    """Expose the optional modular agent without changing the existing RAG API."""
    from backend.agent_core import process_input

    return process_input(req.query)


def _semantic_query_response(
    query: str,
    dataset_id: Optional[str],
    selected_dataset: Optional[Dict[str, Any]],
) -> Dict[str, Any]:
    guardrail_result = guardrail.validate_query(query)
    if not guardrail_result["allowed"]:
        return {
            "query": html.escape(query, quote=False),
            "status": "REJECTED_BY_GUARDRAIL",
            "execution_timeline": [{
                "step": "Domain guardrail",
                "passed": False,
                "detail": html.escape(str(guardrail_result["reason"]), quote=False),
            }],
            "answer": {
                "summary": "Query blocked by Industrial Domain Guardrail.",
                "explanation": (
                    "The question is outside the scope of plant operations. "
                    "Ask about engineering, maintenance, P&ID, or SOP topics."
                ),
                "suggested_topics": [],
            },
            "trust_badge": {
                "confidence_percentage": 0,
                "ui_label": "Blocked out-of-domain",
                "badge_color": "#EF4444",
            },
            "sources": [],
        }

    entities = extractor.process(query)["resolved_entities"]
    if selected_dataset:
        outside_dataset = [
            entity["tag"]
            for entity in entities
            if entity["category"] == "asset"
            and dataset_id_for_equipment_tag(entity["tag"])
            != selected_dataset["dataset_id"]
        ]
        if outside_dataset:
            raise HTTPException(
                status_code=422,
                detail=(
                    f"{', '.join(outside_dataset)} is outside Dataset "
                    f"{selected_dataset['dataset_number']:02d}. "
                    "Select its dataset to continue."
                ),
            )

    try:
        from backend.case1_agent import answer_case1_query
        telemetry_data = telemetry_sim.get_latest_status()
        result = answer_case1_query(query, dataset_id=dataset_id, telemetry_data=telemetry_data)
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
    except RuntimeError as error:
        raise HTTPException(status_code=503, detail=str(error)) from error
    except ImportError as error:
        raise HTTPException(
            status_code=503,
            detail="Install the semantic search dependencies from requirements.txt.",
        ) from error

    retrieval_similarity = result.get("retrieval_similarity")
    if retrieval_similarity is None:
        retrieval_similarity = 0.0
    retrieval_similarity = max(0.0, min(1.0, float(retrieval_similarity)))
    confidence_percentage = int(retrieval_similarity * 100)

    warning = ""
    if result["low_confidence"]:
        warning = (
            "\n\n**Warning:** answer confidence is not calibrated. "
            "The retrieval score indicates search relevance, not certainty. "
            "Verify controlled sources before taking field action."
        )
    if result["generation_mode"] == "local_evidence_only":
        warning += (
            "\n\n**Local mode:** Groq is not enabled; the output only presents "
            "retrieved evidence excerpts without LLM generation."
        )
    elif result["generation_mode"] == "local_no_evidence":
        warning += (
            "\n\n**Groq skipped:** no relevant evidence was retrieved. "
            "Add the relevant sources to the database before requesting an LLM-generated answer."
        )
    primary_entity = (
        selected_dataset["equipment_tag"]
        if selected_dataset
        else next(
            (entity["tag"] for entity in entities if entity["category"] == "asset"),
            "Plant Knowledge Base",
        )
    )
    answer = _synthesize_answer(
        query=query,
        primary_tag=primary_entity,
        entities=entities,
        intent=None,
        graph_ctx={},
        downstream=[],
        chunks=[],
        telemetry={},
        agent_result=result,
    )
    answer["summary"] += warning
    sources = []
    for source in result["sources"]:
        escaped_source = _escape_html_values(source)
        escaped_source["doc_id"] = html.escape(
            str(source.get("doc_id", "unknown")), quote=False
        )
        escaped_source["title"] = html.escape(
            str(source.get("title", "Untitled source")), quote=False
        )
        escaped_source["content"] = html.escape(
            str(source.get("content", "")), quote=False
        )
        escaped_source["similarity_score"] = (
            source["similarity_score"]
            if source.get("similarity_score") is not None
            else 0.0
        )
        sources.append(escaped_source)

    return {
        "query": html.escape(query, quote=False),
        "status": "SUCCESS",
        "execution_timeline": [
            {"step": "Domain guardrail", "passed": True},
            {
                "step": "Approved semantic retrieval",
                "source_count": len(sources),
                "retrieval_similarity": retrieval_similarity,
            },
            {"step": "Answer generation", "mode": result["generation_mode"]},
        ],
        "primary_entity": html.escape(str(primary_entity), quote=False),
        "selected_dataset": ({
            "dataset_id": selected_dataset["dataset_id"],
            "dataset_name": selected_dataset["dataset_name"],
            "equipment_tag": selected_dataset["equipment_tag"],
        } if selected_dataset else None),
        "fusion_breakdown": {
            "source_scores": {
                "graph": 0.0,
                "semantic": retrieval_similarity,
                "structured": 0.0,
            },
            "fused_score": 0.0,
            "weights_used": None,
        },
        "trust_badge": {
            "confidence_percentage": confidence_percentage,
            "ui_label": (
                "Verified Context Match"
                if confidence_percentage >= 55
                else "LOW_CONFIDENCE"
            ),
            "badge_color": "#059669" if confidence_percentage >= 55 else "#D97706",
            "score_type": "retrieval_similarity_not_answer_confidence",
        },
        "generation_metadata": {
            "mode": result["generation_mode"],
            "confidence_type": result["confidence_type"],
            "retrieval_similarity": retrieval_similarity,
            "warning_flags": result["warning_flags"],
        },
        "answer": answer,
        "downstream_impacts": [],
        "sources": sources,
    }


def _escape_html_values(value: Any) -> Any:
    if isinstance(value, str):
        return html.escape(value, quote=False)
    if isinstance(value, dict):
        return {key: _escape_html_values(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_escape_html_values(item) for item in value]
    return value


@app.post("/api/query")
def process_query(req: QueryRequest):
    query_text = req.query.strip()
    if not query_text:
        raise HTTPException(status_code=400, detail="Query string cannot be empty")
    selected_dataset = next(
        (dataset for dataset in DATASET_DEFINITIONS if dataset["dataset_id"] == req.dataset_id),
        None,
    )
    if req.dataset_id and selected_dataset is None:
        raise HTTPException(status_code=400, detail="Selected dataset is not available in the catalog.")
    if req.mode == "pid_audit" and not req.image_data:
        raise HTTPException(status_code=422, detail="Attach a P&ID image or PDF before using P&ID Audit mode.")
    if req.mode == "rag" and not req.image_data:
        return _semantic_query_response(
            query_text,
            req.dataset_id,
            selected_dataset,
        )

    uploaded_document = None
    if req.image_data:
        try:
            uploaded_document = extract_uploaded_document(
                req.image_name or "attached-document",
                req.image_data,
            )
        except ValueError as error:
            raise HTTPException(status_code=400, detail=str(error)) from error

    uploaded_text = uploaded_document.get("text", "") if uploaded_document else ""
    rag_query = f"{query_text}\n{uploaded_text[:20000]}".strip()
    timeline = []

    # -----------------------------------------------------------------------
    # 1. DOMAIN GUARDRAIL CHECK
    # -----------------------------------------------------------------------
    guardrail_result = guardrail.validate_query(f"{query_text} {uploaded_text[:3000]}".strip())
    timeline.append({
        "step": "1. Domain Guardrail",
        "passed": guardrail_result["allowed"],
        "detail": guardrail_result["reason"],
        "confidence": guardrail_result["confidence"]
    })

    if not guardrail_result["allowed"]:
        return _escape_html_values({
            "query": query_text,
            "status": "REJECTED_BY_GUARDRAIL",
            "execution_timeline": timeline,
            "answer": {
                "summary": "Query blocked by Industrial Domain Guardrail.",
                "explanation": (
                    "This AI hub is strictly restricted to plant engineering, equipment troubleshooting, "
                    "P&ID schematics, SOP guidance, and process safety. Non-operational or general queries "
                    f"('{query_text}') are rejected to prevent hallucination, eliminate token waste, and maintain cybersecurity compliance."
                ),
                "suggested_topics": [
                    "Why did GA-1201A trip on PT-1201 low pressure?",
                    "What units are downstream of recycle pump GA-1201A?",
                    "What is the emergency switchover procedure for GA-1201B?",
                    "Show P&ID DWG-PE-1201 notes and interlock limits"
                ]
            },
            "trust_badge": {
                "confidence_percentage": 0,
                "ui_label": "Blocked Out-of-Domain",
                "badge_color": "#EF4444"
            },
            "sources": []
        })

    # -----------------------------------------------------------------------
    # 2. HYBRID NER & INTENT EXTRACTION
    # -----------------------------------------------------------------------
    extraction = extractor.process(query_text)
    resolved_entities = extraction["resolved_entities"]
    intent_info = extraction["intent"]
    query_asset_tags = [
        entity["tag"]
        for entity in resolved_entities
        if entity["category"] == "asset"
    ]
    if uploaded_text and not any(entity["category"] == "asset" for entity in resolved_entities):
        file_entities = extractor.resolve_entities(uploaded_text)
        known_tags = {entity["tag"] for entity in resolved_entities}
        resolved_entities.extend(entity.__dict__ for entity in file_entities if entity.tag not in known_tags)

    timeline.append({
        "step": "2. Hybrid NER & Query Router",
        "entities_found": [e["tag"] for e in resolved_entities],
        "primary_intent": intent_info["primary_intent"],
        "paths_activated": intent_info["activated_paths"]
    })

    # Keep query retrieval inside the operator-selected dataset.
    primary_entity_tag = None
    if selected_dataset:
        outside_dataset = [
            tag for tag in query_asset_tags
            if dataset_id_for_equipment_tag(tag) != selected_dataset["dataset_id"]
        ]
        if outside_dataset:
            raise HTTPException(
                status_code=422,
                detail=f"{', '.join(outside_dataset)} is outside Dataset {selected_dataset['dataset_number']:02d}. Select its dataset to continue.",
            )
        primary_entity_tag = selected_dataset["equipment_tag"]
    elif resolved_entities:
        asset_entity = next(
            (entity for entity in resolved_entities if entity["category"] == "asset"),
            None,
        )
        selected_entity = asset_entity or resolved_entities[0]
        primary_entity_tag = (
            selected_entity["tag"]
            if selected_entity["category"] == "asset"
            else selected_entity["metadata"].get("parent_asset", selected_entity["tag"])
        )
    elif req.asset_context_override:
        primary_entity_tag = req.asset_context_override

    # -----------------------------------------------------------------------
    # 3. PARALLEL TRI-PATH RETRIEVAL
    # -----------------------------------------------------------------------
    graph_context = {}
    downstream_impacts = []
    vector_results = []
    structured_telemetry = {}

    # Path A: Graph Traversal
    if intent_info["activated_paths"]["graph_traversal"] or primary_entity_tag:
        graph_context = graph_engine.get_comprehensive_asset_context(primary_entity_tag)
        downstream_impacts = graph_context.get("downstream_impacts", [])

    # Path B: Semantic Vector Search
    scoped_asset = primary_entity_tag if primary_entity_tag in extractor.registry.get("assets", {}) else None
    vector_results = vector_engine.search(
        rag_query,
        top_k=8,
        equipment_tag=scoped_asset,
        dataset_id=req.dataset_id,
    )

    image_analysis = None
    if uploaded_document:
        filename_lower = uploaded_document["file_name"].lower()
        asks_for_drawing_audit = any(
            marker in query_text.lower()
            for marker in ["p&id", "pid", "drawing", "gambar", "skema", "schematic", "bandingkan", "audit"]
        )
        looks_like_drawing = (
            "pid" in filename_lower
            or "p&id" in filename_lower
            or "piping and instrumentation" in uploaded_text.lower()
            or "cause & effect" in uploaded_text.lower()
        )
        if req.mode == "pid_audit" or (uploaded_document.get("ocr_items") and (asks_for_drawing_audit or looks_like_drawing)):
            master_candidates = vector_engine.search(
                f"{primary_entity_tag or ''} P&ID interlock datasheet drawing",
                top_k=32,
                equipment_tag=scoped_asset,
                dataset_id=req.dataset_id,
            )
            image_analysis = _compare_uploaded_document(
                uploaded_document,
                primary_entity_tag,
                master_candidates,
            )
            timeline.append({
                "step": "RAG Retrieval & OCR Evidence Comparison",
                "master_sources_used": len(image_analysis["master_sources"]),
                "ocr_items_detected": len(uploaded_document.get("ocr_items", [])),
                "verdict": image_analysis["verdict"],
            })

    # Path C: Structured Historian / Sensor Telemetry
    telemetry_tag = (
        primary_entity_tag
        if primary_entity_tag in telemetry_sim.sensor_states
        else "PT-1201"
        if primary_entity_tag in {"GA-1201A", "GA-1201B"}
        else None
    )
    structured_telemetry = telemetry_sim.get_latest_status(telemetry_tag) if telemetry_tag else {}

    timeline.append({
        "step": "3. Tri-Path Parallel Dispatch",
        "graph_nodes_traversed": len(downstream_impacts),
        "vector_chunks_retrieved": len(vector_results),
        "live_telemetry_attached": structured_telemetry.get("current_pressure")
    })

    # -----------------------------------------------------------------------
    # 4. SCORE NORMALIZATION & FUSION
    # -----------------------------------------------------------------------
    # 1. Graph relevance score
    top_graph_score = downstream_impacts[0]["normalized_relevance"] if downstream_impacts else 0.50

    # 2. Semantic relevance score (already bounded 0.0 - 1.0)
    top_vector_score = vector_results[0]["similarity_score"] if vector_results else 0.0

    # 3. Structured trip proximity score
    structured_score = structured_telemetry.get("trip_proximity", 0.0)

    source_scores = {
        "graph": top_graph_score,
        "semantic": top_vector_score,
        "structured": structured_score
    }

    fused_score = fusion_engine.weighted_sum_fusion(source_scores, intent=intent_info["primary_intent"])

    # Count corroborating sources
    corroborating = sum(1 for s in source_scores.values() if s > 0.45)
    approval_status = vector_results[0]["approval_status"] if vector_results else "unverified"

    trust_badge = fusion_engine.compute_confidence(
        fused_score=fused_score,
        corroborating_sources=corroborating,
        approval_status=approval_status
    )
    trust_badge.update({
        "confidence_percentage": 0,
        "ui_label": "Answer confidence not calibrated",
        "badge_color": "#D97706",
    })

    timeline.append({
        "step": "4. Score Normalization & RRF Fusion",
        "scores": source_scores,
        "fused_score": fused_score,
        "trust_confidence": f"{trust_badge['confidence_percentage']}%"
    })

    # -----------------------------------------------------------------------
    # 5. CONTEXT SYNTHESIS (EXPLAINABLE AI WITH VERIFIED CITATIONS)
    # -----------------------------------------------------------------------
    # Synthesize intelligent industrial guidance
    synthesis = _synthesize_answer(
        query=query_text,
        primary_tag=primary_entity_tag,
        entities=resolved_entities,
        intent=intent_info["primary_intent"],
        graph_ctx=graph_context,
        downstream=downstream_impacts,
        chunks=vector_results,
        telemetry=structured_telemetry,
        uploaded_document=uploaded_document,
    )

    return _escape_html_values({
        "query": query_text,
        "status": "SUCCESS",
        "execution_timeline": timeline,
        "entity_metadata": resolved_entities,
        "primary_entity": primary_entity_tag,
        "selected_dataset": ({
            "dataset_id": selected_dataset["dataset_id"],
            "dataset_name": selected_dataset["dataset_name"],
            "equipment_tag": selected_dataset["equipment_tag"],
        } if selected_dataset else None),
        "fusion_breakdown": {
            "source_scores": source_scores,
            "fused_score": fused_score,
            "weights_used": fusion_engine.INTENT_WEIGHTS.get(intent_info["primary_intent"])
        },
        "trust_badge": trust_badge,
        "generation_metadata": {
            "mode": "Template-based Deterministic Synthesis (Demo Mode - Zero API Dependency)",
            "production_target": "On-Premises Llama-3-70B via vLLM / Ollama (Air-Gapped)",
            "deterministic_reproducible": True
        },
        "answer": synthesis,
        "image_analysis": image_analysis,
        "attached_document": ({
            "file_name": uploaded_document["file_name"],
            "extracted": uploaded_document["extracted"],
            "extracted_characters": len(uploaded_text),
            "source_count": uploaded_document["source_count"],
            "ocr_items": len(uploaded_document.get("ocr_items", [])),
            "text_preview": uploaded_text[:1800],
        } if uploaded_document else None),
        "downstream_impacts": downstream_impacts,
        "sources": vector_results,
        "live_telemetry": structured_telemetry
    })


def _synthesize_answer(
    query,
    primary_tag,
    entities,
    intent,
    graph_ctx,
    downstream,
    chunks,
    telemetry,
    uploaded_document=None,
    agent_result=None,
):
    """
    Map retrieved agent evidence to the response schema used by the existing UI.
    """
    if agent_result is not None:
        agent_sources = agent_result.get("sources", [])
        return {
            "summary": html.escape(str(agent_result.get("answer", "")), quote=False),
            "tactical_action": (
                "Use this answer as search support. Check technical values, tags, "
                "revisions, and actual conditions against controlled documents before "
                "field execution; confirm with an SME."
            ),
            "key_references": [
                {
                    "doc_id": html.escape(str(source.get("doc_id") or "unknown"), quote=False),
                    "title": html.escape(str(source.get("title") or "Untitled source"), quote=False),
                    "section": html.escape(
                        str(source.get("section") or source.get("sheet_name") or ""),
                        quote=False,
                    ),
                    "version": html.escape(str(source.get("version") or ""), quote=False),
                    "approval_status": html.escape(
                        str(source.get("approval_status") or "unverified"),
                        quote=False,
                    ),
                }
                for source in agent_sources[:5]
            ],
        }

    primary_name = graph_ctx.get("asset", {}).get("name", primary_tag or "Plant Knowledge Base")
    uploaded_text = uploaded_document.get("text", "") if uploaded_document else ""
    source_blocks = [
        (
            f"**[{chunk.get('doc_id', 'unknown')}] "
            f"{chunk.get('title', 'Untitled source')}** "
            f"({chunk.get('approval_status', 'unverified')})\n"
            f"{(chunk.get('retrieval_text') or chunk.get('content') or '')[:1200]}"
        )
        for chunk in chunks[:5]
    ]
    if uploaded_text:
        source_blocks.append(
            f"**User-provided attachment (unverified): "
            f"{uploaded_document['file_name']}**\n{uploaded_text[:1200]}"
        )
    summary = (
        "\n\n---\n\n".join(source_blocks)
        if source_blocks
        else (
            "The retrieved documents do not contain enough information to answer "
            f"the question about {primary_tag or primary_name}. "
            "Escalate to an SME before taking field action."
        )
    )
    references = ([{
        "doc_id": f"USER-UPLOAD:{uploaded_document['file_name']}",
        "title": uploaded_document["file_name"],
        "section": "User-provided extracted text",
        "version": "User upload",
        "approval_status": "user_supplied_unverified",
        "approved_by": None,
    }] if uploaded_text else []) + [
        {
            "doc_id": chunk.get("doc_id", "unknown"),
            "title": chunk.get("title", "Untitled source"),
            "section": chunk.get("heading") or chunk.get("section") or "",
            "version": chunk.get("version"),
            "approval_status": chunk.get("approval_status", "unverified"),
            "approved_by": chunk.get("approved_by"),
        }
        for chunk in chunks[:5]
    ]
    return {
        "summary": summary,
        "tactical_action": (
            "Check technical values, tags, revisions, and actual conditions against "
            "controlled documents before field execution; confirm with an SME."
        ),
        "key_references": references[:5],
    }
@app.get("/api/graph")
def get_graph(asset_tag: Optional[str] = Query(default=None)):
    return graph_engine.get_asset_subgraph(asset_tag) if asset_tag else graph_engine.get_full_graph()


@app.get("/api/quarantine")
def get_quarantine():
    return {
        "metrics": quarantine_mgr.get_metrics(),
        "records": quarantine_mgr.list_all()
    }


@app.post("/api/quarantine/resolve")
def resolve_quarantine(
    req: QuarantineResolveRequest,
    authenticated_sme: str = Depends(authenticate_sme),
):
    res = quarantine_mgr.resolve_item(
        conflict_id=req.conflict_id,
        action=req.action,
        sme_name=authenticated_sme,
        notes=req.notes
    )
    if not res["success"]:
        raise HTTPException(status_code=404, detail=res["error"])
    try:
        vector_engine.refresh()
        from backend.case1_agent import refresh_case1_index_if_loaded
        from backend.database import refresh_approval_metadata

        refresh_case1_index_if_loaded()
        refresh_approval_metadata()
    except (OSError, RuntimeError) as error:
        raise HTTPException(status_code=500, detail=f"Could not refresh approved search index: {error}") from error
    return res


@app.post("/api/sources/approval")
def update_source_approval(
    req: SourceApprovalRequest,
    authenticated_sme: str = Depends(authenticate_sme),
):
    known_ids = {
        chunk.get("approval_id")
        for chunk in vector_engine.chunks
        if chunk.get("approval_id")
    }
    matches_known_source = req.approval_id in known_ids or (
        req.approval_id.endswith(":*")
        and any(source_id.startswith(req.approval_id[:-1]) for source_id in known_ids)
    )
    if not matches_known_source:
        raise HTTPException(status_code=404, detail="Source or maintenance row was not found.")
    try:
        approval = set_source_approval(
            req.approval_id,
            req.approval_status,
            authenticated_sme if req.approval_status != "unverified" else None,
        )
        vector_engine.refresh()
        from backend.case1_agent import refresh_case1_index_if_loaded
        from backend.database import refresh_approval_metadata

        refresh_case1_index_if_loaded()
        refresh_approval_metadata()
    except (OSError, RuntimeError) as error:
        raise HTTPException(status_code=500, detail=f"Could not update source approval: {error}") from error
    return {"success": True, "approval_id": req.approval_id, **approval}


@app.get("/api/telemetry")
def get_telemetry(tag: Optional[str] = Query(default=None)):
    if tag and tag not in SENSOR_CONFIGS:
        raise HTTPException(status_code=404, detail=f"No telemetry stream is configured for {tag}")
    target_tag = tag if tag else telemetry_sim.active_sensor_tag
    if telemetry_sim.sensor_states[target_tag]["is_degrading"]:
        return telemetry_sim.step_simulation(target_tag)
    return telemetry_sim.get_latest_status(tag)


@app.get("/api/telemetry/sensors")
def list_telemetry_sensors():
    catalog = []
    for tag, config in SENSOR_CONFIGS.items():
        state = telemetry_sim.sensor_states[tag]
        catalog.append({
            "tag_id": tag,
            "name": config["name"],
            "description": config["desc"],
            "unit": config["unit"],
            "normal": config["normal_val"],
            "setpoint": config["setpoint"],
            "alarm": config["low_alarm"],
            "trip": config["trip_limit"],
            "warn_is_lower": config["warn_is_lower"],
            "current_value": state["current_val"],
            "collapse_steps": config["collapse_steps"],
            "source": "DEMO_SIMULATOR",
            "source_reference": config["sop_reference"],
        })
    return {"sensors": catalog, "live_historian_connected": False}


@app.post("/api/telemetry/simulate-anomaly")
def simulate_telemetry_anomaly(tag: Optional[str] = Query(default=None)):
    if tag and tag not in SENSOR_CONFIGS:
        raise HTTPException(status_code=404, detail=f"No telemetry stream is configured for {tag}")
    return telemetry_sim.trigger_anomaly(tag)


@app.post("/api/telemetry/step")
def step_telemetry(tag: Optional[str] = Query(default=None)):
    if tag and tag not in SENSOR_CONFIGS:
        raise HTTPException(status_code=404, detail=f"No telemetry stream is configured for {tag}")
    return telemetry_sim.step_simulation(tag)


@app.post("/api/telemetry/reset")
def reset_telemetry(tag: Optional[str] = Query(default=None)):
    if tag and tag not in SENSOR_CONFIGS:
        raise HTTPException(status_code=404, detail=f"No telemetry stream is configured for {tag}")
    return telemetry_sim.reset_to_normal(tag)


@app.get("/api/documents")
def list_documents():
    docs_by_id = {}
    for chunk in vector_engine.chunks:
        docs_by_id.setdefault(chunk["doc_id"], {
            "doc_id": chunk["doc_id"],
            "approval_id": chunk.get("approval_id"),
            "title": chunk["title"],
            "version": chunk["version"],
            "approval_status": chunk["approval_status"],
            "approved_by": chunk.get("approved_by"),
            "section": chunk["heading"],
            "equipment_tag": chunk.get("equipment_tag"),
            "dataset_id": chunk.get("dataset_id"),
            "source_file": chunk.get("source_file"),
            "sheet_name": chunk.get("sheet_name"),
            "row_index": chunk.get("row_index"),
            "date": chunk.get("date"),
        })

    for node in graph_engine.nodes.values():
        if node.get("type") != "document" or node["id"] in docs_by_id:
            continue
        asset_edge = next(
            (edge for edge in graph_engine.rev_adj_list.get(node["id"], [])
             if edge.get("type") == "DESCRIBED_BY"),
            None,
        )
        docs_by_id[node["id"]] = {
            "doc_id": node["id"],
            "title": node.get("name", node["id"]),
            "version": node.get("version", "Not specified"),
            "approval_status": node.get("approval_status", "unverified"),
            "section": node.get("doc_type", "other"),
            "equipment_tag": asset_edge.get("source") if asset_edge else None,
            "dataset_id": node.get("dataset_id"),
            "source_file": node.get("source_file"),
        }

    return list(docs_by_id.values())


@app.get("/api/source-approvals")
def list_source_approval_candidates():
    candidates = {}
    for chunk in vector_engine.chunks:
        approval_id = chunk.get("approval_id")
        if not approval_id:
            continue
        candidates.setdefault(approval_id, {
            "approval_id": approval_id,
            "doc_id": chunk["doc_id"],
            "title": chunk["title"],
            "approval_status": chunk["approval_status"],
            "approved_by": chunk.get("approved_by"),
            "source_file": chunk.get("source_file"),
            "sheet_name": chunk.get("sheet_name"),
            "row_index": chunk.get("row_index"),
        })
    return list(candidates.values())


# Mount Static Frontend
static_dir = BASE_DIR / "static"
if static_dir.exists():
    app.mount("/", StaticFiles(directory=str(static_dir), html=True), name="static")
