
from pathlib import Path

from src.extractors import extract_document, extract_directory
from src.chunker import chunk_document, semantic_chunks


def test_extract_markdown(tmp_path: Path):
    """Markdown files should be extracted with their text preserved."""
    file_path = tmp_path / "policy.md"
    content = (
        "Department: IT\n"
        "Access Tier: Confidential\n"
        "Document Date: 2026-09-15\n\n"
        "Passwords must be stored securely."
    )
    file_path.write_text(content, encoding="utf-8")

    document = extract_document(file_path)

    assert document["source"] == "policy.md"
    assert document["file_type"] == ".md"
    assert "Passwords must be stored securely." in document["text"]


def test_extract_csv(tmp_path: Path):
    """CSV rows should be converted into readable records."""
    file_path = tmp_path / "employees.csv"
    file_path.write_text(
        "employee_id,department,role\n"
        "E001,Engineering,Software Engineer\n"
        "E002,Human Resources,HR Manager\n",
        encoding="utf-8",
    )

    document = extract_document(file_path)

    assert "E001" in document["text"]
    assert "Software Engineer" in document["text"]
    assert "HR Manager" in document["text"]


def test_csv_chunks_preserve_employee_metadata(tmp_path: Path):
    """Each CSV chunk should preserve its employee's department and ID."""
    file_path = tmp_path / "employees.csv"
    file_path.write_text(
        "employee_id,department,role\n"
        "E001,Engineering,Software Engineer\n"
        "E002,Human Resources,HR Manager\n"
        "E003,Finance,Financial Analyst\n",
        encoding="utf-8",
    )

    document = extract_document(file_path)
    chunks = chunk_document(document)

    assert len(chunks) == 3

    by_employee = {
        chunk["metadata"]["employee_id"]: chunk
        for chunk in chunks
    }

    assert by_employee["E001"]["metadata"]["department"] == "Engineering"
    assert by_employee["E002"]["metadata"]["department"] == "Human Resources"
    assert by_employee["E003"]["metadata"]["department"] == "Finance"


def test_markdown_chunks_preserve_document_metadata(tmp_path: Path):
    """Document chunks should retain department, access tier, and date."""
    file_path = tmp_path / "policy.md"
    file_path.write_text(
        "Department: IT\n"
        "Access Tier: Confidential\n"
        "Document Date: 2026-09-15\n\n"
        "Employees must use secure passwords.\n\n"
        "Systems must be updated regularly.",
        encoding="utf-8",
    )

    document = extract_document(file_path)
    chunks = chunk_document(document)

    assert chunks
    metadata = chunks[0]["metadata"]
    assert metadata["department"] == "IT"
    assert metadata["access_tier"] == "Confidential"
    assert metadata["document_date"] == "2026-09-15"


def test_semantic_chunking_respects_maximum_size():
    """Chunking should split long text into manageable pieces."""
    text = (
        "First paragraph. " * 20
        + "\n\n"
        + "Second paragraph. " * 20
    )

    chunks = semantic_chunks(
        text,
        max_chars=200,
        overlap_chars=20,
    )

    assert len(chunks) > 1
    assert all(len(chunk) <= 200 for chunk in chunks)


def test_extract_directory_discovers_supported_files(tmp_path: Path):
    """Directory extraction should discover Markdown and CSV files."""
    (tmp_path / "policy.md").write_text(
        "A sample policy.", encoding="utf-8"
    )
    (tmp_path / "employees.csv").write_text(
        "employee_id,department\nE001,Engineering\n",
        encoding="utf-8",
    )
    (tmp_path / "ignore.json").write_text(
        '{"example": true}', encoding="utf-8"
    )

    documents = extract_directory(tmp_path)
    filenames = {document["source"] for document in documents}

    assert filenames == {"policy.md", "employees.csv"}
