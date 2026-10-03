"""Parse Case 1 source documents to Markdown without rewriting source data."""

import argparse
import hashlib
import os
import re
from pathlib import Path
from typing import Iterable

BASE_DIR = Path(__file__).resolve().parent.parent
PDF_DIR = BASE_DIR / "data" / "supporting data pdf"
PID_DIR = BASE_DIR / "data" / "P&ID Data"
MARKDOWN_DIR = BASE_DIR / "data" / "case1_markdown"
SOURCE_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg", ".tif", ".tiff"}


def source_files() -> list[Path]:
    """Return the supplied PDF and P&ID image sources, excluding generated data."""
    files = [
        path for path in PDF_DIR.rglob("*")
        if path.is_file() and path.suffix.lower() in SOURCE_EXTENSIONS
    ]
    files.extend(
        path for path in PID_DIR.glob("*")
        if path.is_file() and path.suffix.lower() in SOURCE_EXTENSIONS
    )
    return sorted(files, key=lambda path: str(path).casefold())


def extract_version(markdown: str) -> str:
    match = re.search(
        r"\b(?:revision|rev\.?|version)\s*[:#-]?\s*([A-Z0-9][A-Z0-9._/-]*)",
        markdown,
        re.IGNORECASE,
    )
    return match.group(1) if match else "Not specified"


def markdown_output_path(source: Path, output_dir: Path = MARKDOWN_DIR) -> Path:
    try:
        relative = source.relative_to(BASE_DIR).as_posix()
    except ValueError:
        relative = source.name
    digest = hashlib.sha1(relative.encode("utf-8")).hexdigest()[:10]
    safe_stem = re.sub(r"[^A-Za-z0-9._-]+", "_", source.stem).strip("_")
    return output_dir / f"{safe_stem}_{digest}.md"


def parse_source(source: Path, output_dir: Path = MARKDOWN_DIR) -> Path:
    """Use LlamaParse to persist a source as Markdown with traceable front matter."""
    from llama_parse import LlamaParse

    if os.getenv("CALIBER_ALLOW_CLOUD_PROCESSING", "").strip().lower() not in {
        "1", "true", "yes", "on"
    }:
        raise RuntimeError(
            "Cloud document parsing is disabled. Set "
            "CALIBER_ALLOW_CLOUD_PROCESSING=true only after approving document transfer."
        )
    api_key = os.getenv("LLAMA_CLOUD_API_KEY") or os.getenv("LLAMA_PARSE_API_KEY")
    if not api_key:
        raise RuntimeError("Set LLAMA_CLOUD_API_KEY before running Case 1 ingestion.")

    parser = LlamaParse(api_key=api_key, result_type="markdown", verbose=False)
    parsed_documents = parser.load_data(str(source))
    markdown = "\n\n".join(
        document.text.strip()
        for document in parsed_documents
        if getattr(document, "text", "").strip()
    )
    if not markdown:
        raise ValueError(f"LlamaParse returned no Markdown for {source.name}.")

    output_path = markdown_output_path(source, output_dir)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    front_matter = (
        f"<!-- case1_doc_name: {source.name} | "
        f"case1_version: {extract_version(markdown)} -->\n\n"
    )
    output_path.write_text(front_matter + markdown + "\n", encoding="utf-8")
    return output_path


def ingest_sources(sources: Iterable[Path] | None = None) -> list[Path]:
    """Parse every configured source, continuing after per-file service errors."""
    if os.getenv("CALIBER_ALLOW_CLOUD_PROCESSING", "").strip().lower() not in {
        "1", "true", "yes", "on"
    }:
        raise RuntimeError(
            "Cloud document parsing is disabled. Set "
            "CALIBER_ALLOW_CLOUD_PROCESSING=true only after approving document transfer."
        )
    if not (os.getenv("LLAMA_CLOUD_API_KEY") or os.getenv("LLAMA_PARSE_API_KEY")):
        raise RuntimeError("Set LLAMA_CLOUD_API_KEY before running Case 1 ingestion.")
    source_list = list(sources if sources is not None else source_files())
    if not source_list:
        raise FileNotFoundError("No supported PDFs or P&ID images were found in the source folders.")

    results = []
    failures = []
    for source in source_list:
        try:
            output_path = parse_source(source)
            print(f"Parsed {source.name} -> {output_path.name}")
            results.append(output_path)
        except Exception as error:
            failures.append((source, error))
            print(f"Failed {source.name}: {error}")

    if failures and not results:
        raise RuntimeError(f"LlamaParse failed for all {len(failures)} source files.") from failures[0][1]
    if failures:
        print(f"Completed with {len(failures)} failed source file(s).")
    return results


def markdown_chunks(markdown_file: Path, chunk_size: int = 1000, chunk_overlap: int = 150):
    """Load one Markdown file and split it while retaining heading/source metadata."""
    from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
    from langchain_core.documents import Document

    text = markdown_file.read_text(encoding="utf-8")
    source_match = re.match(r"<!-- case1_doc_name: (.*?) \| case1_version: (.*?) -->\s*", text)
    doc_name = source_match.group(1) if source_match else markdown_file.name
    version = source_match.group(2) if source_match else extract_version(text)
    body = text[source_match.end():] if source_match else text

    header_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=[("#", "section"), ("##", "subsection"), ("###", "subsubsection")],
        strip_headers=False,
    )
    sections = header_splitter.split_text(body)
    if not sections:
        sections = [Document(page_content=body)]
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        add_start_index=True,
    )
    chunks = splitter.split_documents(sections)
    for chunk in chunks:
        chunk.metadata.update({
            "doc_name": doc_name,
            "version": version,
            "section":
                chunk.metadata.get("subsubsection")
                or chunk.metadata.get("subsection")
                or chunk.metadata.get("section")
                or "Unsectioned",
            "markdown_file": markdown_file.name,
        })
    return chunks


def main() -> None:
    parser = argparse.ArgumentParser(description="Parse Case 1 SOP/P&ID sources to Markdown.")
    parser.add_argument("--source", type=Path, help="Parse only this PDF or P&ID image.")
    args = parser.parse_args()
    outputs = ingest_sources([args.source] if args.source else None)
    print(f"Wrote {len(outputs)} Markdown file(s) to {MARKDOWN_DIR}.")


if __name__ == "__main__":
    main()