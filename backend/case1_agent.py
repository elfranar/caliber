"""Evidence-grounded LangChain runtime for Case 1 technical questions."""

import re
import hashlib
from functools import lru_cache
from pathlib import Path
from typing import Any

from backend.case1_ingestion import markdown_output_path, markdown_chunks, source_files
from backend.dataset_catalog import dataset_id_for_equipment_tag, dataset_id_for_source, source_document_id
from backend.source_governance import get_source_approval, maintenance_approval_id
from backend.config_groq import (
    get_groq_api_key,
    get_groq_model,
    groq_processing_enabled,
)

BASE_DIR = Path(__file__).resolve().parent.parent
MAINTENANCE_DIR = BASE_DIR / "data" / "Maintenance Data"
CHROMA_DIR = BASE_DIR / "data" / "case1_chroma_v2"
COLLECTION_NAME = "case1_sop_pid_markdown"
NO_INFORMATION = "Sorry, the information was not found in the official database."
MIN_RETRIEVAL_SIMILARITY = 0.30
LOW_CONFIDENCE_THRESHOLD = 0.55
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


def groq_api_key() -> str:
    return get_groq_api_key()


def _to_similarity(distance: float) -> float:
    return max(0.0, min(1.0, 1.0 - float(distance)))


@lru_cache(maxsize=1)
def _load_vector_store():
    from langchain_chroma import Chroma
    from langchain_huggingface import HuggingFaceEmbeddings

    embedding_function = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )
    store = Chroma(
        collection_name=COLLECTION_NAME,
        persist_directory=str(CHROMA_DIR),
        embedding_function=embedding_function,
        collection_metadata={"hnsw:space": "cosine"},
    )
    return store


def _sync_vector_store(store: Any) -> None:
    """Keep the persisted Chroma collection aligned with current Markdown and approvals."""
    source_documents: dict[str, tuple[str, list[Any]]] = {}
    for source_file in source_files():
        markdown_file = markdown_output_path(source_file)
        if not markdown_file.is_file():
            continue
        source_id = source_document_id(source_file)
        source_hash = hashlib.sha256(markdown_file.read_bytes()).hexdigest()
        approval = get_source_approval(source_id)
        fingerprint = (
            f"{source_hash}:{approval['approval_status']}:{approval['approved_by'] or ''}"
        )
        chunks = markdown_chunks(markdown_file)
        for chunk_number, chunk in enumerate(chunks):
            dataset_id = dataset_id_for_source(source_file) or ""
            chunk.metadata.update({
                "source_id": source_id,
                "source_file": source_file.relative_to(BASE_DIR / "data").as_posix(),
                "markdown_file": markdown_file.name,
                "source_fingerprint": fingerprint,
                "dataset_id": dataset_id,
                "approval_status": approval["approval_status"],
                "approved_by": approval["approved_by"] or "",
                "doc_id": source_id,
            })
        source_documents[source_id] = (fingerprint, chunks)

    existing = store._collection.get(include=["metadatas"])
    existing_ids = existing.get("ids", [])
    existing_metadatas = existing.get("metadatas", [])
    by_source: dict[str, list[tuple[str, dict[str, Any]]]] = {}
    legacy_ids = []
    for document_id, metadata in zip(existing_ids, existing_metadatas):
        if not isinstance(metadata, dict) or not metadata.get("source_id"):
            legacy_ids.append(document_id)
            continue
        by_source.setdefault(str(metadata["source_id"]), []).append(
            (document_id, metadata)
        )

    if legacy_ids:
        store.delete(ids=legacy_ids)

    for source_id in set(by_source) - set(source_documents):
        store.delete(ids=[document_id for document_id, _ in by_source[source_id]])

    for source_id, (fingerprint, chunks) in source_documents.items():
        existing_for_source = by_source.get(source_id, [])
        if not chunks:
            if existing_for_source:
                store.delete(ids=[document_id for document_id, _ in existing_for_source])
            continue

        source_hash = hashlib.sha256(source_id.encode("utf-8")).hexdigest()[:16]
        desired_ids = [
            hashlib.sha256(
                f"{source_hash}:{chunk.metadata.get('start_index', index)}:{chunk.page_content}".encode("utf-8")
            ).hexdigest()
            for index, chunk in enumerate(chunks)
        ]
        is_current = (
            len(existing_for_source) == len(chunks)
            and all(
                metadata.get("source_fingerprint") == fingerprint
                for _, metadata in existing_for_source
            )
            and {document_id for document_id, _ in existing_for_source} == set(desired_ids)
        )
        if is_current:
            continue
        if existing_for_source:
            store.delete(ids=[document_id for document_id, _ in existing_for_source])
        store.add_documents(chunks, ids=desired_ids)


def refresh_case1_index_if_loaded() -> None:
    """Apply approval or source changes immediately when the Chroma index is active."""
    if _load_vector_store.cache_info().currsize:
        _sync_vector_store(_load_vector_store())


def _clean_value(value: Any) -> Any:
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


def _search_maintenance(
    query: str,
    limit: int = 5,
    dataset_id: str | None = None,
) -> list[dict[str, Any]]:
    import pandas as pd

    workbooks = sorted(MAINTENANCE_DIR.rglob("*.xlsx")) if MAINTENANCE_DIR.exists() else []
    if not workbooks:
        return []

    terms = list(dict.fromkeys(re.findall(r"[A-Za-z0-9][A-Za-z0-9._/-]{2,}", query.casefold())))
    terms = [term for term in terms if term not in {"what", "when", "where", "which", "were", "with", "from", "have", "does", "did", "the", "and", "for"}]
    if not terms:
        return []
    required_matches = 1 if re.search(r"\b[A-Za-z]{1,5}-\d{2,5}[A-Za-z]?\b", query) else 2

    matches: list[tuple[int, int, dict[str, Any]]] = []
    for workbook in workbooks:
        sheets = pd.read_excel(workbook, sheet_name=None)
        for sheet_name, frame in sheets.items():
            for row_offset, row in frame.iterrows():
                values = {str(column): _clean_value(value) for column, value in row.items()}
                source_file = workbook.relative_to(BASE_DIR / "data").as_posix()
                row_index = int(row_offset) + 2
                approval_id = maintenance_approval_id(
                    source_file,
                    str(sheet_name),
                    row_index,
                )
                approval = get_source_approval(approval_id)
                # Allowed all approval statuses to be processed by LLM
                equipment_tag = values.get("Equipment_Tag")
                if dataset_id and dataset_id_for_equipment_tag(equipment_tag) != dataset_id:
                    continue
                text = " ".join(str(value) for value in values.values() if value is not None).casefold()
                matched_terms = [term for term in terms if term in text]
                if len(matched_terms) < required_matches:
                    continue
                date_value = next(
                    (value for column, value in values.items() if "date" in column.casefold() and value is not None),
                    None,
                )
                source = {
                    "file_name": workbook.name,
                    "sheet_name": str(sheet_name),
                    "row_index": row_index,
                    "date": date_value,
                    "matched_terms": matched_terms,
                    "similarity_score": round(len(matched_terms) / len(terms), 4),
                    "record": values,
                    "dataset_id": dataset_id_for_equipment_tag(
                        values.get("Equipment_Tag")
                    ),
                    "approval_id": approval_id,
                    "approval_status": approval["approval_status"],
                    "approved_by": approval["approved_by"],
                }
                matches.append((len(matched_terms), int(row_offset), source))

    matches.sort(key=lambda match: (-match[0], match[1]))
    return [match[2] for match in matches[:limit]]


def answer_case1_query(
    query: str,
    dataset_id: str | None = None,
    telemetry_data: dict[str, Any] | None = None,
) -> dict[str, Any]:
    query = query.strip()
    if not query:
        raise ValueError("Query is required.")

    vector_store = _load_vector_store()
    _sync_vector_store(vector_store)
    metadata_filter: dict[str, Any] | None = None
    if dataset_id:
        metadata_filter = {"dataset_id": dataset_id}
    results = vector_store.similarity_search_with_score(
        query,
        k=8,
        filter=metadata_filter,
    )
    query_terms = {
        term
        for term in re.findall(r"[a-z0-9]+(?:[-._/][a-z0-9]+)*", query.casefold())
        if len(term) > 2
    }
    asks_for_numeric_evidence = bool(
        re.search(
            r"\b(?:what\s+is|what\s+are|how\s+many|how\s+high|how\s+low|"
            r"limit|limits|alarm|trip|set\s*point|threshold|thresholds|"
            r"berapa|batas|setpoint)\b",
            query.casefold(),
        )
    )
    requested_opl_numbers = set(
        re.findall(r"\bopl[- ]?0*(\d+)\b", query.casefold())
    )
    asks_for_procedure = bool(
        re.search(r"\b(?:prosedur|procedure|langkah|steps?)\b", query.casefold())
    )

    def rerank_key(result: tuple[Any, float]) -> tuple[float, float]:
        document, distance = result
        content = document.page_content.casefold()
        content_terms = set(
            re.findall(r"[a-z0-9]+(?:[-._/][a-z0-9]+)*", content)
        )
        lexical_coverage = (
            len(query_terms & content_terms) / len(query_terms)
            if query_terms
            else 0.0
        )
        has_numeric_evidence = asks_for_numeric_evidence and bool(
            re.search(
                r"\b\d+(?:[.,]\d+)?\s*(?:mm/s|mm|bar|barg|rpm|m3/h|kpa|mpa|psi|%)\b",
                content,
            )
        )
        source_id = str(document.metadata.get("doc_id", "")).casefold()
        source_opl_numbers = set(
            re.findall(r"(?:^|[-_])0*(\d+)$", source_id)
        )
        lesson_match = bool(requested_opl_numbers & source_opl_numbers)
        section = str(document.metadata.get("section", "")).casefold()
        procedure_match = asks_for_procedure and "detailed procedure" in section
        relevance = (
            _to_similarity(distance)
            + 0.25 * lexical_coverage
            + (0.20 if has_numeric_evidence else 0.0)
            + (0.50 if lesson_match else 0.0)
            + (0.15 if procedure_match else 0.0)
        )
        return relevance, _to_similarity(distance)

    results.sort(key=rerank_key, reverse=True)
    sources: list[dict[str, Any]] = []
    markdown_context: list[str] = []
    similarities: list[float] = []
    for document, distance in results:
        similarity = _to_similarity(distance)
        if similarity < MIN_RETRIEVAL_SIMILARITY:
            continue
        metadata = document.metadata
        source = {
            "type": "markdown",
            "doc_id": metadata.get("doc_id") or metadata.get("source_id") or "unknown",
            "doc_name": metadata.get("doc_name", metadata.get("source", "Unknown")),
            "title": metadata.get("doc_name", metadata.get("source", "Unknown")),
            "version": metadata.get("version", "Not specified"),
            "section": metadata.get("section", "Unsectioned"),
            "dataset_id": metadata.get("dataset_id"),
            "approval_status": metadata.get("approval_status", "unverified"),
            "approved_by": metadata.get("approved_by") or None,
            "distance": round(float(distance), 4),
            "similarity": round(similarity, 4),
            "similarity_score": round(similarity, 4),
            "content": document.page_content,
        }
        sources.append(source)
        similarities.append(similarity)
        markdown_context.append(
            f"[{source['doc_id']} | {source['title']} | {source['version']} | "
            f"{source['section']}]\n{document.page_content[:1200]}"
        )

    maintenance_rows = _search_maintenance(query, dataset_id=dataset_id)
    for row in maintenance_rows:
        sources.append({
            "type": "excel",
            "doc_id": row["approval_id"],
            "title": row["file_name"],
            "file_name": row["file_name"],
            "sheet_name": row["sheet_name"],
            "row_index": row["row_index"],
            "date": row["date"],
            "dataset_id": row["dataset_id"],
            "approval_status": row["approval_status"],
            "approved_by": row["approved_by"],
            "similarity_score": None,
            "content": " | ".join(
                f"{key}: {value}"
                for key, value in row["record"].items()
                if value is not None
            ),
        })

    if not sources:
        answer = NO_INFORMATION
        generation_mode = "local_no_evidence"
    else:
        evidence_context = "\n\n".join(
            markdown_context
            + [
                f"[{row['file_name']} | {row['sheet_name']} | row {row['row_index']} | "
                f"{row['date']}]\n{row['record']}"
                for row in maintenance_rows
            ]
        )
        if telemetry_data and telemetry_data.get("proactive_alert"):
            alert = telemetry_data["proactive_alert"]
            evidence_context += (
                f"\n\n[LIVE TELEMETRY ALERT]\n"
                f"Sensor {telemetry_data['tag_id']} ({telemetry_data['sensor_name']}) is in state {alert['severity']}!\n"
                f"Current Value: {alert['current_val']}, Trip Limit: {alert['trip_limit']}\n"
                f"Failure Memory Match: {alert['matched_incident_id']} - {alert['incident_title']}\n"
                f"Recommended Action: {alert['recommended_action']}"
            )

        if groq_processing_enabled():
            api_key = groq_api_key()
            from langchain_groq import ChatGroq

            llm = ChatGroq(
                model=get_groq_model(),
                temperature=0,
                api_key=api_key,
                max_tokens=600,
            )
            prompt = (
                "Answer the technical question in English. Use only facts from the "
                "provided evidence; do not create operating instructions or add "
                "technical values that are not present. If the evidence is insufficient, "
                f"say: {NO_INFORMATION} Cite source names, sections, and row numbers.\n"
                "Note: Some evidence may have approval_status as 'unverified' or 'rejected'. "
                "If you use information from unapproved sources, you MUST explicitly mention that "
                "this information is pending SME approval or has been rejected.\n\n"
                "CRITICAL INSTRUCTION: If [LIVE TELEMETRY ALERT] is present in the Retrieved evidence, "
                "you MUST start your response with a prominent '### ⚠️ Live Telemetry & Failure Memory Alert' section. "
                "In this section, explicitly state the Sensor, its current state, the Failure Memory Match, and the Recommended Action "
                "before answering the user's question.\n\n"
                f"Question: {query}\n\nRetrieved evidence (check status):\n{evidence_context}"
            )
            try:
                answer = str(llm.invoke(prompt).content).strip()
            except Exception as error:
                import traceback
                traceback.print_exc()
                raise RuntimeError(f"Groq request failed: {error}") from error
            generation_mode = "groq_grounded"
        else:
            excerpts = [
                (
                    f"[{source['doc_id']}] {source['title'].replace('_', ' ')} — {source['section']}\n"
                    f"{source['content'][:1200]}"
                    if source["type"] == "markdown"
                    else (
                        f"[{source['doc_id']}] {source['title']} — "
                        f"{source['sheet_name']} row {source['row_index']} "
                        f"({source['date']})\n{source['content'][:1200]}"
                    )
                )
                for source in sources[:3]
            ]
            answer = "Most relevant verified evidence:\n\n" + "\n\n".join(excerpts)
            generation_mode = "local_evidence_only"

    retrieval_similarity = max(similarities) if similarities else None
    low_confidence = (
        retrieval_similarity is None
        or retrieval_similarity < LOW_CONFIDENCE_THRESHOLD
        or not markdown_context
    )
    warning_flags = ["LOW_CONFIDENCE"] if low_confidence else []
    if not sources:
        warning_flags.append("NO_APPROVED_EVIDENCE")

    return {
        "answer": answer,
        "sources": sources,
        "confidence": None,
        "confidence_type": "not_calibrated",
        "retrieval_similarity": (
            round(retrieval_similarity, 4)
            if retrieval_similarity is not None
            else None
        ),
        "low_confidence": low_confidence,
        "warning_flags": warning_flags,
        "generation_mode": generation_mode,
    }