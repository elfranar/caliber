"""LlamaParse ingestion with locally persisted Chroma and local embeddings."""

from __future__ import annotations

import os
import re
import inspect
import logging
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from backend.config import BASE_DIR
from backend.dataset_catalog import source_document_id
from backend.case1_ingestion import source_files
from backend.source_governance import get_source_approval

_logger = logging.getLogger(__name__)
DEFAULT_DATA_DIR = BASE_DIR / "data"
DEFAULT_COLLECTION_NAME = "caliber_manufacturing_knowledge"
IMAGE_OUTPUT_DIRECTORY = "parsed_images"
CHROMA_DIRECTORY = ".chroma"
EMBEDDING_PROVIDER_MARKER = "embedding_provider.txt"


class DatabaseConfigurationError(RuntimeError):
    """Raised when database dependencies, credentials, or consent are missing."""


def _cloud_processing_enabled() -> bool:
    """Return whether sending document content to cloud services is authorized."""
    return os.getenv("CALIBER_ALLOW_CLOUD_PROCESSING", "").strip().lower() in {
        "1", "true", "yes", "on"
    }


def _require_cloud_configuration() -> None:
    """Validate consent and credentials before sending documents to LlamaParse."""
    if not _cloud_processing_enabled():
        raise DatabaseConfigurationError(
            "Cloud document parsing is disabled. Set "
            "CALIBER_ALLOW_CLOUD_PROCESSING=true only after approving cloud transfer."
        )
    if not os.getenv("LLAMA_CLOUD_API_KEY"):
        raise DatabaseConfigurationError("LLAMA_CLOUD_API_KEY is required for LlamaParse.")
    base_url = os.getenv("LLAMA_CLOUD_BASE_URL", "").strip()
    if base_url:
        parsed_url = urlparse(base_url)
        if parsed_url.scheme not in {"http", "https"} or not parsed_url.netloc:
            raise DatabaseConfigurationError(
                "LLAMA_CLOUD_BASE_URL must be a complete URL beginning with "
                "https://. Leave it unset to use the default Llama Cloud region."
            )


def _require_database_dependencies() -> tuple[Any, Any, Any, Any, Any]:
    """Import the optional LlamaIndex, Chroma, and parser integrations lazily."""
    try:
        import chromadb
        from llama_index.core import Document, StorageContext, VectorStoreIndex
        from llama_index.vector_stores.chroma import ChromaVectorStore
        from llama_parse import LlamaParse
    except ImportError as error:
        raise DatabaseConfigurationError(
            "Document database dependencies are missing. Install requirements.txt "
            "to use LlamaParse and ChromaDB."
        ) from error
    return chromadb, Document, StorageContext, VectorStoreIndex, (ChromaVectorStore, LlamaParse)


def _safe_metadata(metadata: dict[str, Any]) -> dict[str, str | int | float | bool]:
    """Keep only Chroma-compatible primitive metadata values."""
    clean: dict[str, str | int | float | bool] = {}
    for key, value in metadata.items():
        if value is None:
            continue
        if isinstance(value, (str, int, float, bool)):
            clean[str(key)] = value
        else:
            clean[str(key)] = str(value)
    return clean


def _dataset_id_for_path(path: Path) -> str | None:
    """Infer the existing dataset identifier from a source path when possible."""
    match = re.search(r"data\s*set\s*0?(\d+)", str(path), re.IGNORECASE)
    return f"dataset_{int(match.group(1)):02d}" if match else None


def _make_local_embedding() -> Any:
    """Create an offline hash embedding compatible with LlamaIndex BaseEmbedding."""
    import hashlib
    import math
    from llama_index.core.embeddings import BaseEmbedding

    class LocalHashEmbedding(BaseEmbedding):
        """Deterministic bag-of-hashes embedding for offline Chroma indexing."""

        dimensions: int = 384

        def _embed(self, text: str) -> list[float]:
            vector = [0.0] * self.dimensions
            tokens = re.findall(r"[a-zA-Z0-9_-]{2,}", text.lower())
            for token in tokens:
                digest = hashlib.sha256(token.encode("utf-8")).digest()
                index = int.from_bytes(digest[:4], "big") % self.dimensions
                vector[index] += 1.0
                if "-" in token:
                    tag_index = int.from_bytes(digest[4:8], "big") % self.dimensions
                    vector[tag_index] += 0.5
            norm = math.sqrt(sum(value * value for value in vector)) or 1.0
            return [value / norm for value in vector]

        def _get_query_embedding(self, query: str) -> list[float]:
            return self._embed(query)

        def _get_text_embedding(self, text: str) -> list[float]:
            return self._embed(text)

        async def _aget_query_embedding(self, query: str) -> list[float]:
            return self._embed(query)

    return LocalHashEmbedding(model_name="local-hash-384", embed_batch_size=32)


def _extract_pdf_visuals(pdf_path: Path, output_dir: Path) -> list[Path]:
    """Save embedded PDF images and vector-drawn pages as local image files."""
    try:
        import fitz
    except ImportError:
        return []

    saved_paths: list[Path] = []
    output_dir.mkdir(parents=True, exist_ok=True)
    try:
        with fitz.open(pdf_path) as pdf:
            for page_number, page in enumerate(pdf, start=1):
                for image_number, image_info in enumerate(page.get_images(full=True), start=1):
                    extracted = pdf.extract_image(image_info[0])
                    image_bytes = extracted.get("image")
                    if not image_bytes:
                        continue
                    extension = extracted.get("ext", "png").lower()
                    if extension not in {"png", "jpg", "jpeg", "webp", "tif", "tiff"}:
                        extension = "png"
                    image_path = output_dir / f"page-{page_number:03d}-image-{image_number:03d}.{extension}"
                    image_path.write_bytes(image_bytes)
                    saved_paths.append(image_path)
                if page.get_drawings():
                    drawing_path = output_dir / f"page-{page_number:03d}-drawing.png"
                    if not drawing_path.exists():
                        pixmap = page.get_pixmap(matrix=fitz.Matrix(1.5, 1.5), alpha=False)
                        pixmap.save(drawing_path)
                    saved_paths.append(drawing_path)
    except (OSError, RuntimeError, ValueError):
        return saved_paths
    return saved_paths


class LocalKnowledgeDatabase:
    """Ingest PDFs and drawings into a locally persisted Chroma collection."""

    def __init__(
        self,
        data_dir: str | Path = DEFAULT_DATA_DIR,
        collection_name: str = DEFAULT_COLLECTION_NAME,
    ) -> None:
        """Create a database handle without importing optional packages yet."""
        self.data_dir = Path(data_dir).expanduser().resolve()
        self.persist_dir = self.data_dir / CHROMA_DIRECTORY
        self.image_output_dir = self.data_dir / IMAGE_OUTPUT_DIRECTORY
        self.collection_name = collection_name
        self._index: Any | None = None
        self._collection: Any | None = None

    def ingest_documents(self, data_dir: str | Path = "./data") -> dict[str, Any]:
        """Parse PDFs, OCR PNG/JPEG drawings, and rebuild the local vector index.

        LlamaParse is configured for Markdown and image-block extraction. Parsed
        image blocks are written below ``data_dir/parsed_images``; embedded PDF
        images are extracted locally as a fallback. PDF text and image OCR are
        embedded with a deterministic local hash model after parsing.
        """
        self.data_dir = Path(data_dir).expanduser().resolve()
        self.persist_dir = self.data_dir / CHROMA_DIRECTORY
        self.image_output_dir = self.data_dir / IMAGE_OUTPUT_DIRECTORY

        _require_cloud_configuration()
        chromadb, Document, StorageContext, VectorStoreIndex, integrations = _require_database_dependencies()
        ChromaVectorStore, LlamaParse = integrations

        if not self.data_dir.is_dir():
            raise FileNotFoundError(f"Data directory does not exist: {self.data_dir}")

        self.image_output_dir.mkdir(parents=True, exist_ok=True)
        pdf_paths = sorted({
            *self.data_dir.rglob("*.pdf"),
            *self.data_dir.rglob("*.PDF"),
        })
        dataset_filter = os.getenv("CALIBER_DATASET_FILTER", "").strip().lower()
        if dataset_filter:
            pdf_paths = [
                path for path in pdf_paths
                if dataset_filter in str(path.relative_to(self.data_dir)).lower()
            ]
        max_pdf_files_raw = os.getenv("CALIBER_MAX_PDF_FILES", "").strip()
        if max_pdf_files_raw:
            try:
                max_pdf_files = int(max_pdf_files_raw)
            except ValueError as error:
                raise DatabaseConfigurationError(
                    "CALIBER_MAX_PDF_FILES must be an integer when provided."
                ) from error
            if max_pdf_files < 1:
                raise DatabaseConfigurationError("CALIBER_MAX_PDF_FILES must be at least 1.")
            pdf_paths = pdf_paths[:max_pdf_files]
        parser_documents: list[Any] = []
        parsed_image_paths: list[Path] = []

        total_pdf_files = len(pdf_paths)
        for file_number, pdf_path in enumerate(pdf_paths, start=1):
            _logger.info("LlamaParse ingestion %s/%s: %s", file_number, total_pdf_files, pdf_path.name)
            relative_path = pdf_path.relative_to(self.data_dir)
            image_dir = self.image_output_dir / relative_path.with_suffix("")
            image_dir.mkdir(parents=True, exist_ok=True)
            parser_options: dict[str, Any] = {
                "api_key": os.environ["LLAMA_CLOUD_API_KEY"],
                "result_type": "markdown",
            }
            parser_parameters = inspect.signature(LlamaParse).parameters
            llama_cloud_base_url = os.getenv("LLAMA_CLOUD_BASE_URL", "").strip()
            if llama_cloud_base_url and "base_url" in parser_parameters:
                parser_options["base_url"] = llama_cloud_base_url
            if "extract_image_block_types" in parser_parameters:
                parser_options["extract_image_block_types"] = ["image"]
            if "image_output_dir" in parser_parameters:
                parser_options["image_output_dir"] = str(image_dir)
            if "save_images" in parser_parameters:
                parser_options["save_images"] = True
            if "disable_image_extraction" in parser_parameters:
                parser_options["disable_image_extraction"] = False
            parser = LlamaParse(**parser_options)
            parsed_documents = parser.load_data(str(pdf_path))
            for parsed in parsed_documents:
                text = str(getattr(parsed, "text", "")).strip()
                if not text:
                    continue
                metadata = _safe_metadata(dict(getattr(parsed, "metadata", {}) or {}))
                metadata.update({
                    "source_file": pdf_path.name,
                    "source_path": relative_path.as_posix(),
                    "file_type": "pdf",
                })
                approval_id = source_document_id(pdf_path)
                approval = get_source_approval(approval_id)
                metadata.update({
                    "source_id": approval_id,
                    "approval_status": approval["approval_status"],
                    "approved_by": approval["approved_by"] or "",
                })
                dataset_id = _dataset_id_for_path(relative_path)
                if dataset_id:
                    metadata["dataset_id"] = dataset_id
                parser_documents.append(Document(text=text, metadata=metadata))

            parser_images = {
                path for path in image_dir.rglob("*")
                if path.is_file()
                and path.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp", ".tif", ".tiff", ".bmp"}
            }
            parser_images.update(_extract_pdf_visuals(pdf_path, image_dir))
            parsed_image_paths.extend(sorted(parser_images))

        excluded_roots = [self.persist_dir.resolve(), self.image_output_dir.resolve()]
        source_images = sorted(
            path for path in self.data_dir.rglob("*")
            if path.is_file()
            and path.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp", ".tif", ".tiff", ".bmp"}
            and not any(root == path.resolve() or root in path.resolve().parents for root in excluded_roots)
        )
        indexed_images: list[Any] = []
        from backend.document_ingestion import extract_document_bytes

        for image_path in [*source_images, *parsed_image_paths]:
            try:
                extracted = extract_document_bytes(image_path.name, image_path.read_bytes())
            except (OSError, ValueError):
                continue
            text = extracted.get("text", "").strip()
            if not text:
                continue
            relative_path = image_path.relative_to(self.data_dir)
            original_source = next(
                (
                    source_path for source_path in source_files()
                    if source_path.resolve() == image_path.resolve()
                ),
                None,
            )
            approval_id = source_document_id(original_source) if original_source else ""
            approval = get_source_approval(approval_id) if approval_id else {
                "approval_status": "unverified",
                "approved_by": None,
            }
            metadata = {
                "source_file": image_path.name,
                "source_path": relative_path.as_posix(),
                "file_type": "image",
                "dataset_id": _dataset_id_for_path(relative_path) or "",
                "source_id": approval_id,
                "approval_status": approval["approval_status"],
                "approved_by": approval["approved_by"] or "",
            }
            indexed_images.append(Document(text=text, metadata=_safe_metadata(metadata)))

        documents = [*parser_documents, *indexed_images]
        if not documents:
            raise ValueError(f"No searchable text was extracted from {self.data_dir}")

        self.persist_dir.mkdir(parents=True, exist_ok=True)
        client = chromadb.PersistentClient(path=str(self.persist_dir))
        try:
            client.delete_collection(self.collection_name)
        except Exception:
            pass
        collection = client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"},
        )
        vector_store = ChromaVectorStore(chroma_collection=collection)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        embedding_provider = "local"
        self._index = VectorStoreIndex.from_documents(
            documents,
            storage_context=storage_context,
            embed_model=_make_local_embedding(),
            show_progress=False,
        )
        (self.persist_dir / EMBEDDING_PROVIDER_MARKER).write_text(
            embedding_provider,
            encoding="utf-8",
        )
        self._collection = collection

        return {
            "status": "INDEXED",
            "pdf_count": len(pdf_paths),
            "image_count": len(source_images) + len(parsed_image_paths),
            "document_count": len(documents),
            "index_path": str(self.persist_dir),
            "collection_name": self.collection_name,
        }

    def retrieve_context(self, query: str, top_k: int = 5) -> list[dict[str, Any]]:
        """Return the most relevant local Chroma documents for a query."""
        clean_query = query.strip()
        if not clean_query:
            return []
        if top_k < 1:
            raise ValueError("top_k must be at least 1")
        if not self.persist_dir.is_dir():
            return []

        chromadb, _, _, VectorStoreIndex, integrations = _require_database_dependencies()
        ChromaVectorStore, _ = integrations
        embedding_model = _make_local_embedding()

        if self._index is None:
            client = chromadb.PersistentClient(path=str(self.persist_dir))
            try:
                collection = client.get_collection(self.collection_name)
            except Exception:
                return []
            if collection.count() == 0:
                return []
            vector_store = ChromaVectorStore(chroma_collection=collection)
            self._index = VectorStoreIndex.from_vector_store(
                vector_store,
                embed_model=embedding_model,
            )
            self._collection = collection

        from llama_index.core.vector_stores import (
            FilterOperator,
            MetadataFilter,
            MetadataFilters,
        )

        filters = MetadataFilters(filters=[
            MetadataFilter(
                key="approval_status",
                operator=FilterOperator.EQ,
                value="approved",
            )
        ])
        retriever = self._index.as_retriever(
            similarity_top_k=top_k,
            filters=filters,
        )
        results = retriever.retrieve(clean_query)
        approved_results = []
        for result in results:
            metadata = dict(result.node.metadata)
            source_id = metadata.get("source_id")
            approval = get_source_approval(str(source_id)) if source_id else {
                "approval_status": "unverified",
                "approved_by": None,
            }
            if approval["approval_status"] != "approved":
                continue
            metadata["approval_status"] = approval["approval_status"]
            metadata["approved_by"] = approval["approved_by"]
            approved_results.append({
                "text": result.node.get_content(),
                "metadata": metadata,
                "score": float(result.score) if result.score is not None else None,
            })
            if len(approved_results) >= top_k:
                break
        return approved_results

    def refresh_approval_metadata(self) -> None:
        """Update persisted Chroma metadata after SME approval changes."""
        if not self.persist_dir.is_dir():
            return
        import chromadb

        client = chromadb.PersistentClient(path=str(self.persist_dir))
        collection_names = {
            collection.name for collection in client.list_collections()
        }
        if self.collection_name not in collection_names:
            return
        collection = client.get_collection(self.collection_name)
        records = collection.get(include=["metadatas"])
        for document_id, stored_metadata in zip(
            records.get("ids", []),
            records.get("metadatas", []),
        ):
            metadata = dict(stored_metadata or {})
            source_id = metadata.get("source_id")
            approval = get_source_approval(str(source_id)) if source_id else {
                "approval_status": "unverified",
                "approved_by": None,
            }
            metadata["approval_status"] = approval["approval_status"]
            metadata["approved_by"] = approval["approved_by"] or ""
            collection.update(ids=[document_id], metadatas=[metadata])


_default_database = LocalKnowledgeDatabase()


def ingest_documents(data_dir: str | Path = "./data") -> dict[str, Any]:
    """Ingest documents into the default local Chroma database."""
    return _default_database.ingest_documents(data_dir)


def retrieve_context(query: str) -> list[dict[str, Any]]:
    """Retrieve the top matching documents from the default Chroma database."""
    return _default_database.retrieve_context(query)


def refresh_approval_metadata() -> None:
    """Refresh the optional local Chroma collection if it exists."""
    _default_database.refresh_approval_metadata()