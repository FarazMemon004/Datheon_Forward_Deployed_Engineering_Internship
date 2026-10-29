
import re
import hashlib
from typing import Any


def extract_metadata(document: dict[str, Any]) -> dict[str, str]:
    """Extract document-level metadata from text."""
    text = document.get("text", "")

    def find_value(pattern: str, default: str = "Unknown") -> str:
        match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
        return match.group(1).strip() if match else default

    return {
        "source": document.get("source", "unknown"),
        "file_type": document.get("file_type", "unknown"),
        "department": find_value(r"^\s*Department\s*:\s*(.+)$"),
        "access_tier": find_value(r"^\s*Access Tier\s*:\s*(.+)$"),
        "document_date": find_value(r"^\s*Document Date\s*:\s*(.+)$"),
    }


def semantic_chunks(
    text: str,
    max_chars: int = 700,
    overlap_chars: int = 100,
) -> list[str]:
    """Split text into paragraph-based chunks with overlap."""
    if max_chars <= 0:
        raise ValueError("max_chars must be greater than zero")

    if not 0 <= overlap_chars < max_chars:
        raise ValueError("overlap_chars must be between 0 and max_chars")

    paragraphs = [
        p.strip()
        for p in re.split(r"\n\s*\n", text)
        if p.strip()
    ]

    chunks = []
    current = ""

    for paragraph in paragraphs:
        if len(paragraph) > max_chars:
            if current:
                chunks.append(current)
                current = ""

            start = 0
            while start < len(paragraph):
                end = min(start + max_chars, len(paragraph))
                chunks.append(paragraph[start:end].strip())

                if end == len(paragraph):
                    break

                start = end - overlap_chars
            continue

        candidate = f"{current}\n\n{paragraph}" if current else paragraph

        if len(candidate) <= max_chars:
            current = candidate
        else:
            if current:
                chunks.append(current)

            overlap = current[-overlap_chars:] if overlap_chars and current else ""
            current = f"{overlap}\n\n{paragraph}".strip() if overlap else paragraph

    if current.strip():
        chunks.append(current.strip())

    return chunks


def chunk_document(
    document: dict[str, Any],
    max_chars: int = 700,
    overlap_chars: int = 100,
) -> list[dict[str, Any]]:
    """Create chunks and preserve metadata."""
    metadata = extract_metadata(document)
    text = document.get("text", "")

    # CSV extractors format each row as a separate Record.
    if document.get("file_type") == ".csv":
        records = re.split(r"(?=^Record \d+\s*$)", text, flags=re.MULTILINE)
        records = [record.strip() for record in records if record.strip()]
    else:
        records = semantic_chunks(text, max_chars, overlap_chars)

    results = []

    for index, chunk in enumerate(records):
        chunk_metadata = dict(metadata)

        # CSV metadata belongs to each employee row, not the entire file.
        if document.get("file_type") == ".csv":
            department_match = re.search(
                r"^\s*department\s*:\s*(.+)$",
                chunk,
                re.IGNORECASE | re.MULTILINE,
            )
            chunk_metadata["department"] = (
                department_match.group(1).strip()
                if department_match
                else "Unknown"
            )

            employee_match = re.search(
                r"^\s*employee_id\s*:\s*(.+)$",
                chunk,
                re.IGNORECASE | re.MULTILINE,
            )
            chunk_metadata["employee_id"] = (
                employee_match.group(1).strip()
                if employee_match
                else "Unknown"
            )

        # Use a stable unique ID for each source chunk.
        digest = hashlib.sha1(chunk.encode("utf-8")).hexdigest()[:10]
        source = metadata["source"]
        chunk_id = f"{source}::chunk-{index}-{digest}"

        results.append({
            "id": chunk_id,
            "text": chunk,
            "metadata": {
                **chunk_metadata,
                "chunk_index": index,
            },
        })

    return results
