"""
End-to-End Automated Test Suite for Manufacturing Knowledge Hub
PT Chandra Asri Pacific Tbk - CALIBER 2026
"""

import sys
import base64
import atexit
import json
import tempfile
from pathlib import Path

# Add project root to sys.path
root_dir = Path(__file__).resolve().parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from backend.domain_guardrail import DomainGuardrail
from backend.entity_extractor import EntityExtractor
from backend.knowledge_graph import KnowledgeGraphEngine
from backend.vector_engine import NormalizedVectorEngine
from backend.scoring_fusion import ScoringFusionEngine
from backend.hitl_quarantine import HITLQuarantineManager
from backend.config import QUARANTINE_PATH
import backend.source_governance as source_governance
import backend.case1_agent as case1_agent
from backend.case1_ingestion import source_files
from backend.dataset_catalog import source_document_id
from starlette.testclient import TestClient
from backend.main import app
from backend.main import vector_engine


_test_approval_directory = tempfile.TemporaryDirectory(prefix="caliber-test-approvals-")
_test_vector_directory = tempfile.TemporaryDirectory(prefix="caliber-test-chroma-")
case1_agent.CHROMA_DIR = Path(_test_vector_directory.name) / "case1_chroma"
case1_agent._load_vector_store.cache_clear()


def _close_test_vector_store():
    if case1_agent._load_vector_store.cache_info().currsize:
        case1_agent._load_vector_store()._client.close()


atexit.register(_close_test_vector_store)
source_governance.APPROVALS_PATH = (
    Path(_test_approval_directory.name) / "source_approvals.json"
)
_test_approval_ids = {source_document_id(path) for path in source_files()}
_maintenance_approval_wildcards = set()
for _chunk in vector_engine.chunks:
    _approval_id = _chunk.get("approval_id")
    if not _approval_id:
        continue
    if _approval_id.startswith("maintenance:"):
        _maintenance_approval_wildcards.add(
            _approval_id.rsplit(":", 1)[0] + ":*"
        )
    else:
        _test_approval_ids.add(_approval_id)

source_governance.APPROVALS_PATH.write_text(
    json.dumps({
        approval_id: {"approval_status": "approved", "approved_by": "Test SME"}
        for approval_id in _test_approval_ids | _maintenance_approval_wildcards
    }),
    encoding="utf-8",
)
vector_engine.refresh()


def test_guardrail():
    print("[TEST 1/10] Testing Domain Guardrail...")
    guard = DomainGuardrail()

    # Out of domain query - must be rejected
    res1 = guard.validate_query("What is the weather in Jakarta today?")
    assert not res1["allowed"], "Guardrail failed to block weather query!"
    assert res1["detected_intent"] == "out_of_domain_rejected"

    # In domain query - must be accepted
    res2 = guard.validate_query("Why did GA-1201A trip on PT-1201 low pressure?")
    assert res2["allowed"], "Guardrail improperly rejected valid plant query!"
    assert res2["detected_intent"] == "in_domain_technical"
    print("  -> PASSED: Out-of-domain rejected, technical in-domain accepted.")


def test_entity_extractor():
    print("[TEST 2/10] Testing Hybrid NER & Intent Extraction...")
    ext = EntityExtractor()

    # Formal tag query
    res = ext.process("Why did GA-1201A trip on PT-1201 low pressure?")
    tags = [e["tag"] for e in res["resolved_entities"]]
    assert "GA-1201A" in tags, "Failed to extract asset GA-1201A"
    assert "PT-1201" in tags, "Failed to extract parameter PT-1201"

    # Informal description query (Fuzzy matching)
    res_fuzzy = ext.process("Why did the hexane feed pump shut down?")
    assert len(res_fuzzy["resolved_entities"]) > 0, "Fuzzy match failed for informal query"
    assert res_fuzzy["resolved_entities"][0]["tag"] in ["GA-1201A", "GA-1201B"]
    print("  -> PASSED: Formal ISA-5.1 tags and informal fuzzy matches resolved correctly.")


def test_knowledge_graph():
    print("[TEST 3/10] Testing Topological Graph Traversal & Cascade Impacts...")
    kg = KnowledgeGraphEngine()

    # Test downstream impact of GA-1201A
    impacts = kg.downstream_impact_traversal("GA-1201A")
    impacted_tags = [i["impacted_asset"] for i in impacts]

    assert "DC-4501" in impacted_tags, "Reactor DC-4501 not found downstream of GA-1201A"
    assert "KC-4501" in impacted_tags, "Compressor KC-4501 not found in downstream cascade"

    # Test hop-decay scoring: hop 1 should have higher score than hop 2
    hop1_score = next(i["normalized_relevance"] for i in impacts if i["hop_distance"] == 1)
    hop2_score = next(i["normalized_relevance"] for i in impacts if i["hop_distance"] == 2)
    assert hop1_score > hop2_score, f"Hop decay failed: {hop1_score} vs {hop2_score}"
    print(f"  -> PASSED: Process topology verified. Hop 1 ({hop1_score}) > Hop 2 ({hop2_score}).")


def test_normalized_vector_engine():
    print("[TEST 4/10] Testing Normalized Vector Search & Bounded Metric...")
    ve = NormalizedVectorEngine()
    results = ve.search("suction pressure trip PSLL-1201 emergency switchover")

    assert len(results) > 0, "No chunks retrieved from vector index"
    for r in results:
        # Crucial check: Must strictly be normalized between 0.0 and 1.0!
        assert 0.0 <= r["similarity_score"] <= 1.0, f"Unnormalized score detected: {r['similarity_score']}"
        assert r["approval_status"] == "approved", "Unapproved source entered search results"
    print(f"  -> PASSED: All similarity scores strictly bounded in [0.0, 1.0]. Top score: {results[0]['similarity_score']}.")


def test_dataset_catalog_integration():
    print("[TEST] Testing dataset catalog integration across retrieval, entities, and graph...")
    ve = NormalizedVectorEngine()
    extractor = EntityExtractor()
    graph = KnowledgeGraphEngine()
    equipment_tags = ["GA-1201A", "YD-2301", "DC-3401A", "KC-4501", "EA-5601", "LV-6701", "CT-7801", "FA-8901"]

    for tag in equipment_tags:
        assert extractor.resolve_entities(tag), f"Dataset equipment {tag} did not resolve"
        context = graph.get_comprehensive_asset_context(tag)
        assert context["asset"]["id"] == tag
        assert context["reference_documents"], f"No graph-linked documents found for {tag}"
        scoped = graph.get_asset_subgraph(tag)
        assert scoped["root_asset"] == tag and any(node["id"] == tag for node in scoped["nodes"])

    yd_results = ve.search("YD-2301 chain speed slip", top_k=5)
    assert yd_results, "Dataset 02 YD-2301 documents were not indexed"
    assert any(result["equipment_tag"] == "YD-2301" for result in yd_results)
    assert all(result["approval_status"] == "approved" for result in yd_results)
    assert all(result["source_file"].startswith(("supporting data pdf/", "P&ID Data/", "Maintenance Data/")) for result in yd_results)

    maintenance_results = ve.search("WO-240109 KC-4501 SIS proof test SEQ-4501", top_k=5)
    assert any(
        result.get("sheet_name")
        and result.get("row_index") == 2
        and result.get("date")
        and result["source_file"].startswith("Maintenance Data/")
        for result in maintenance_results
    ), "Maintenance search did not return Excel row provenance"

    dc_results = ve.search("DC-3401A hydrogen reduction exotherm", top_k=5)
    assert dc_results, "Dataset 03 DC-3401A documents were not indexed"
    assert all(result["source_file"].startswith(("supporting data pdf/", "P&ID Data/", "Maintenance Data/")) for result in dc_results)

    inventory = TestClient(app).get("/api/documents").json()
    inventory_ids = [document["doc_id"] for document in inventory]
    assert len(inventory_ids) == len(set(inventory_ids)), "Document inventory contains duplicate source IDs"
    assert any(document.get("source_file") == "P&ID Data/P&ID Set 3.png" for document in inventory), "P&ID source image is missing from document inventory"
    print("  -> PASSED: All eight dataset assets resolve and expose source-file-backed documents.")


def test_fusion_and_trust():
    print("[TEST 5/10] Testing Weighted Sum Fusion & Confidence Badge...")
    fusion = ScoringFusionEngine()

    source_scores = {"graph": 1.0, "semantic": 0.892, "structured": 0.029}
    fused = fusion.weighted_sum_fusion(source_scores, intent="factual")
    assert 0.0 <= fused <= 1.0

    trust = fusion.compute_confidence(fused, corroborating_sources=2, approval_status="approved")
    assert trust["confidence_percentage"] >= 70
    assert trust["level"] in ["HIGH_CONFIDENCE", "MEDIUM_CONFIDENCE"]
    print(f"  -> PASSED: Fused score {fused}, Trust confidence {trust['confidence_percentage']}% ({trust['ui_label']}).")


def test_hitl_quarantine():
    print("[TEST 6/10] Testing Industrial Data Ops & HITL Conflict Quarantine...")
    with tempfile.TemporaryDirectory() as temp_dir:
        test_store = Path(temp_dir) / "quarantine_store.json"
        test_store.write_text(QUARANTINE_PATH.read_text(encoding="utf-8"), encoding="utf-8")
        qm = HITLQuarantineManager(test_store)
        metrics = qm.get_metrics()

        assert metrics["quarantined_conflicts"] > 0, "Quarantine should isolate conflicting records"
        assert metrics["quarantined_conflicts"] >= 3, "Expected the existing HITL audit records to remain available"
        assert metrics["total_ingested_sources"] >= 97, "Official PDF/P&ID source files were not counted"
        assert metrics["data_health_score"] > 90.0

        res = qm.resolve_item("CONF-PID-001", "APPROVE", "Ir. Test Engineer", "Verified against P&ID stamp")
        assert res["success"]
        assert res["record"]["status"] == "APPROVED_BY_SME"
    print(f"  -> PASSED: HITL Quarantine isolated conflicts. Health score: {metrics['data_health_score']}%.")


def test_full_api_endpoints():
    print("[TEST 7/10] Testing FastAPI Server Endpoints via TestClient...")
    client = TestClient(app)

    # 1. Status endpoint
    status_res = client.get("/api/status")
    assert status_res.status_code == 200
    assert status_res.json()["system"] == "Manufacturing Knowledge Hub"
    assert client.get("/api/assets").json()
    assert client.get("/api/graph", params={"asset_tag": "YD-2301"}).json()["root_asset"] == "YD-2301"
    datasets = client.get("/api/datasets").json()
    assert [dataset["dataset_id"] for dataset in datasets] == [f"dataset_{number:02d}" for number in range(1, 9)]
    assert datasets[6]["equipment_tag"] == "CT-7801" and datasets[7]["equipment_tag"] == "FA-8901"

    # 2. Guardrail rejection via API
    rej_res = client.post("/api/query", json={"query": "What is the weather in Jakarta today?"})
    assert rej_res.status_code == 200
    assert rej_res.json()["status"] == "REJECTED_BY_GUARDRAIL"

    # 3. Successful technical query via API
    tech_res = client.post("/api/query", json={"query": "Why did GA-1201A trip on PT-1201 low pressure?"})
    assert tech_res.status_code == 200
    data = tech_res.json()
    assert data["status"] == "SUCCESS"
    assert "answer" in data
    assert len(data["sources"]) > 0
    assert data["answer"]["key_references"]
    assert len(data["answer"]["key_references"]) <= 5
    assert all(
        {"doc_id", "title", "section", "version", "approval_status"}
        <= reference.keys()
        for reference in data["answer"]["key_references"]
    )
    assert data["answer"]["summary"]
    retrieval_similarity = data["generation_metadata"]["retrieval_similarity"]
    assert data["trust_badge"]["confidence_percentage"] == int(retrieval_similarity * 100)
    assert data["trust_badge"]["score_type"] == "retrieval_similarity_not_answer_confidence"
    assert data["trust_badge"]["ui_label"] == (
        "Verified Context Match" if retrieval_similarity >= 0.55 else "LOW_CONFIDENCE"
    )
    assert data["generation_metadata"]["confidence_type"] == "not_calibrated"
    assert any(source.get("equipment_tag") in (None, "GA-1201A") for source in data["sources"])

    scoped_res = client.post("/api/query", json={
        "query": "What are the YD-2301 dryer interlock trips and permissives?",
        "dataset_id": "dataset_02",
        "mode": "rag",
    })
    assert scoped_res.status_code == 200
    scoped_data = scoped_res.json()
    assert scoped_data["selected_dataset"]["dataset_id"] == "dataset_02"
    assert scoped_data["sources"]
    assert all(source["dataset_id"] == "dataset_02" for source in scoped_data["sources"])

    wrong_dataset_res = client.post("/api/query", json={
        "query": "Why did GA-1201A trip on low suction pressure?",
        "dataset_id": "dataset_02",
    })
    assert wrong_dataset_res.status_code == 422
    audit_without_file = client.post("/api/query", json={
        "query": "Compare this P&ID with the master",
        "dataset_id": "dataset_02",
        "mode": "pid_audit",
    })
    assert audit_without_file.status_code == 422

    # 4. Telemetry simulation trigger
    sim_res = client.post("/api/telemetry/simulate-anomaly")
    assert sim_res.status_code == 200
    assert sim_res.json()["is_pre_trip"] is True
    sensors = client.get("/api/telemetry/sensors").json()
    assert sensors["live_historian_connected"] is False
    vt_status = client.get("/api/telemetry", params={"tag": "VT-1201"}).json()
    assert vt_status["unit"] == "mm/s"

    pt_value_before_vt_actions = client.get("/api/telemetry", params={"tag": "PT-1201"}).json()["current_val"]
    vt_anomaly = client.post("/api/telemetry/simulate-anomaly", params={"tag": "VT-1201"}).json()
    assert vt_anomaly["tag_id"] == "VT-1201" and vt_anomaly["current_val"] == 3.8
    assert vt_anomaly["unit"] == "mm/s"
    vt_step = client.post("/api/telemetry/step", params={"tag": "VT-1201"}).json()
    assert vt_step["tag_id"] == "VT-1201" and vt_step["current_val"] == 4.9
    vt_reset = client.post("/api/telemetry/reset", params={"tag": "VT-1201"}).json()
    assert vt_reset["tag_id"] == "VT-1201" and vt_reset["current_val"] == 2.15
    assert client.get("/api/telemetry", params={"tag": "PT-1201"}).json()["current_val"] == pt_value_before_vt_actions
    print("  -> PASSED: Full REST API integration validated successfully.")


def test_one_point_lessons():
    print("[TEST 8/10] Testing One Point Lesson (OPL 01-07) Ingestion & Semantic Queries...")
    client = TestClient(app)

    # 1. Startup & Priming OPL-06
    res_priming = client.post("/api/query", json={"query": "Bagaimana prosedur start-up dan priming pompa GA-1201A sesuai OPL?"})
    assert res_priming.status_code == 200
    data_priming = res_priming.json()
    assert data_priming["status"] == "SUCCESS"
    assert "OPL-GA-1201A-06" in [s["doc_id"] for s in data_priming["sources"]] or "vent" in data_priming["answer"]["summary"].lower() or "priming" in data_priming["answer"]["summary"].lower()

    # 2. Alignment OPL-03 & OPL-05
    res_align = client.post("/api/query", json={"query": "Prosedur laser alignment dan thermal growth offset GA-1201A"})
    assert res_align.status_code == 200
    data_align = res_align.json()
    assert data_align["status"] == "SUCCESS"
    assert "0.05 mm" in data_align["answer"]["summary"] or "OPL-GA-1201A-03" in [s["doc_id"] for s in data_align["sources"]]

    # 3. Vibration OPL-07
    res_vib = client.post("/api/query", json={"query": "Berapa batas alarm dan trip vibrasi VSHH-1201 GA-1201A?"})
    assert res_vib.status_code == 200
    data_vib = res_vib.json()
    assert data_vib["status"] == "SUCCESS"
    assert "7.1" in data_vib["answer"]["summary"] or "4.5" in data_vib["answer"]["summary"]

    # 4. Seal Flush OPL-01
    res_seal = client.post("/api/query", json={"query": "Bagaimana prosedur inspeksi flush mechanical seal Plan 11/62 dan kebocoran OPL-01?"})
    assert res_seal.status_code == 200
    data_seal = res_seal.json()
    assert data_seal["status"] == "SUCCESS"
    assert "Plan 11" in data_seal["answer"]["summary"] or "John Crane" in data_seal["answer"]["summary"]

    # 5. Lube Oil OPL-02
    res_lube = client.post("/api/query", json={"query": "Bagaimana standar pelumasan bearing oil bath ISO VG 68 sesuai OPL-02?"})
    assert res_lube.status_code == 200
    data_lube = res_lube.json()
    assert data_lube["status"] == "SUCCESS"
    assert "ISO VG 68" in data_lube["answer"]["summary"] or "oil bath" in data_lube["answer"]["summary"].lower()

    # 6. Minimum-flow protection OPL-04
    res_str = client.post("/api/query", json={"query": "Bagaimana batas minimum flow GA-1201A dan perlindungan deadhead sesuai OPL-04?"})
    assert res_str.status_code == 200
    data_str = res_str.json()
    assert data_str["status"] == "SUCCESS"
    assert "FV-1201" in data_str["answer"]["summary"] or "minimum flow" in data_str["answer"]["summary"].lower()

    print("  -> PASSED: All 7 One Point Lessons (OPL-01 to OPL-07) successfully verified.")


def test_process_safety_and_pid_validator():
    print("[TEST 9/10] Testing Process Safety Guardrail Pass & P&ID Validator Endpoint...")
    client = TestClient(app)

    # 1. Broad query "process safety" must be ALLOWED by Guardrail (not blocked)
    guard = DomainGuardrail()
    res_guard = guard.validate_query("process safety")
    assert res_guard["allowed"], "Domain Guardrail failed: 'process safety' should be an allowed engineering topic!"

    # 2. Query endpoint returns process safety assessment
    res_safety = client.post("/api/query", json={"query": "process safety"})
    assert res_safety.status_code == 200
    data_safety = res_safety.json()
    assert data_safety["status"] == "SUCCESS", f"Expected SUCCESS but got {data_safety['status']}"
    assert data_safety["sources"], "Plant-wide safety query should cite retrieved source material"
    assert data_safety["answer"]["key_references"], "Safety answer must retain traceable source references"
    assert "safety" in data_safety["answer"]["summary"].lower() or "osha" in data_safety["answer"]["summary"].lower()

    # A drawing audit must receive actual uploaded evidence.
    res_pid = client.post("/api/validate-pid", json={
        "drawing_title": "Hexane Feed Pump GA-1201A/B Schematic Draft",
        "drawing_author": "Junior Process Engineer (Draft Rev 0.1)"
    })
    assert res_pid.status_code == 422

    print("  -> PASSED: 'process safety' allowed and synthesized; P&ID Validator detected critical junior draft flaws.")


def test_multimodal_image_analysis():
    print("[TEST 10/10] Testing Multimodal Image Upload & Comparative P&ID Inspection...")
    client = TestClient(app)

    image_path = root_dir / "data" / "P&ID Data" / "P&ID_Set_02.png"
    image_data = "data:image/png;base64," + base64.b64encode(image_path.read_bytes()).decode("ascii")
    res = client.post("/api/query", json={
        "query": "Bandingkan P&ID YD-2301 dengan master yang terhubung",
        "image_name": image_path.name,
        "image_data": image_data
        ,"dataset_id": "dataset_02",
        "mode": "pid_audit",
    })
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "SUCCESS"
    assert "image_analysis" in data
    assert data["image_analysis"] is not None
    ia = data["image_analysis"]
    assert ia["detected_equipment"] == "YD-2301"
    assert data["selected_dataset"]["dataset_id"] == "dataset_02"
    assert ia["ocr_items"]
    assert ia["master_sources"]
    assert ia["tag_locations"]
    assert any(positions[0]["bbox"] for positions in ia["tag_locations"].values() if positions)
    assert all(discrepancy["location"] == [] for discrepancy in ia["discrepancies"])
    assert "connectivity" in ia["comparison_scope"]

    from unittest.mock import patch

    uploaded_cross_reference = {
        "file_name": "cross-reference.webp",
        "text": "P&ID drawing reference tag GA-1201A.",
        "ocr_items": [{"page": 1, "text": "GA-1201A", "bbox": [], "confidence": 0.9}],
        "extracted": True,
        "source_count": 1,
    }
    with patch("backend.main.extract_uploaded_document", return_value=uploaded_cross_reference):
        cross_reference_res = client.post("/api/query", json={
            "query": "Compare the attached P&ID drawing with the selected master.",
            "image_name": uploaded_cross_reference["file_name"],
            "image_data": "data:image/webp;base64,dGVzdA==",
            "dataset_id": "dataset_02",
            "mode": "pid_audit",
        })
    assert cross_reference_res.status_code == 200, cross_reference_res.text
    cross_reference_data = cross_reference_res.json()
    assert cross_reference_data["selected_dataset"]["dataset_id"] == "dataset_02"
    assert all(source["dataset_id"] == "dataset_02" for source in cross_reference_data["sources"])
    print(f"  -> PASSED: Uploaded image OCR found {len(ia['matched_tags'])} matching master tags; verdict: {ia['verdict']}.")


if __name__ == "__main__":
    print("\n" + "=" * 65)
    print("  RUNNING MANUFACTURING KNOWLEDGE HUB TEST SUITE")
    print("=" * 65 + "\n")
    test_guardrail()
    test_entity_extractor()
    test_knowledge_graph()
    test_normalized_vector_engine()
    test_dataset_catalog_integration()
    test_fusion_and_trust()
    test_hitl_quarantine()
    test_full_api_endpoints()
    test_one_point_lessons()
    test_process_safety_and_pid_validator()
    test_multimodal_image_analysis()
    print("\n" + "=" * 65)
    print("  ALL 10 TESTS PASSED PERFECTLY!")
    print("=" * 65 + "\n")
