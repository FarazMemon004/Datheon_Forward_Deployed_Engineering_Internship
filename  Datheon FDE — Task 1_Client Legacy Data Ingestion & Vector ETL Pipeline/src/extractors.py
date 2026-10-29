from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd
import pymupdf


SUPPORTED_EXTENSIONS = {".pdf", ".csv", ".md", ".markdown", ".txt"}


def extract_pdf(file_path: Path) -> str:
    """Extract text from all pages of a PDF."""
    pages = []

    with pymupdf.open(file_path) as document:
        for page_number, page in enumerate(document, start=1):
            text = page.get_text("text").strip()

            if text:
                pages.append(
                    f"[Page {page_number}]\n{text}"
                )

    return "\n\n".join(pages)


def extract_csv(file_path: Path) -> str:
    """Convert CSV rows into readable text records."""
    dataframe = pd.read_csv(file_path).fillna("")

    records = []

    for row_number, (_, row) in enumerate(
        dataframe.iterrows(), start=1
    ):
        fields = [
            f"{column}: {value}"
            for column, value in row.items()
        ]

        records.append(
            f"Record {row_number}\n" + "\n".join(fields)
        )

    return "\n\n".join(records)


def extract_text(file_path: Path) -> str:
    """Extract text from Markdown and plain-text files."""
    return file_path.read_text(encoding="utf-8-sig")


def extract_document(file_path: str | Path) -> dict[str, Any]:
    """Extract a document and return its text and source metadata."""
    path = Path(file_path)

    if not path.is_file():
        raise FileNotFoundError(f"File not found: {path}")

    extension = path.suffix.lower()

    if extension == ".pdf":
        text = extract_pdf(path)
    elif extension == ".csv":
        text = extract_csv(path)
    elif extension in {".md", ".markdown", ".txt"}:
        text = extract_text(path)
    else:
        raise ValueError(
            f"Unsupported file format: {extension}"
        )

    return {
        "source": path.name,
        "file_path": str(path.resolve()),
        "file_type": extension,
        "text": text.strip(),
        "character_count": len(text.strip()),
    }


def discover_documents(
    directory: str | Path,
) -> list[Path]:
    """Find all supported documents recursively."""
    root = Path(directory)

    if not root.exists():
        raise FileNotFoundError(
            f"Directory not found: {root}"
        )

    if not root.is_dir():
        raise NotADirectoryError(
            f"Expected a directory: {root}"
        )

    return sorted(
        path
        for path in root.rglob("*")
        if path.is_file()
        and path.suffix.lower() in SUPPORTED_EXTENSIONS
    )


def extract_directory(
    directory: str | Path,
) -> list[dict[str, Any]]:
    """Extract all supported documents, skipping failed files."""
    documents = []

    for path in discover_documents(directory):
        try:
            document = extract_document(path)

            if document["text"]:
                documents.append(document)
                print(
                    f"[OK] {path.name}: "
                    f"{document['character_count']} characters"
                )
            else:
                print(f"[WARNING] No text found: {path.name}")

        except Exception as error:
            print(f"[ERROR] {path.name}: {error}")

    return documents
