# Datheon FDE — Task 1: Client Legacy Data Ingestion & Vector ETL Pipeline

A Python-based document ingestion and semantic search pipeline that transforms legacy business documents into searchable vector embeddings using **ChromaDB** and **Sentence Transformers**.

## Overview

Organizations often store important information across PDFs, CSV files, and Markdown documents. This project extracts text from these sources, divides it into manageable chunks, preserves document metadata, generates vector embeddings, and stores them for semantic retrieval.

The pipeline is designed as a foundation for enterprise knowledge retrieval and retrieval-augmented generation (RAG) systems.

## Features

- **Multi-format ingestion:** PDF, CSV, Markdown, and TXT files.
- **Text extraction:** PyMuPDF for PDF documents and pandas for CSV files.
- **Chunking:** Paragraph-aware chunking with configurable chunk size and overlap.
- **Metadata preservation:** Source file, file type, department, access tier, document date, and employee ID where applicable.
- **Semantic embeddings:** `sentence-transformers/all-MiniLM-L6-v2`.
- **Vector database:** Persistent ChromaDB storage.
- **Similarity search:** Cosine-distance-based semantic retrieval.
- **Metadata filtering:** Filter search results by department and access tier.
- **Automated tests:** Pytest coverage for extraction, chunking, metadata, and file discovery.

## Technology Stack

| Component | Technology |
|---|---|
| Language | Python 3.11 |
| PDF extraction | PyMuPDF |
| CSV processing | pandas |
| Embeddings | Sentence Transformers |
| Embedding model | all-MiniLM-L6-v2 |
| Vector database | ChromaDB |
| Testing | pytest |

## Project Structure

```text
.
├── data/
│   ├── raw/
│   │   ├── pdf/
│   │   ├── csv/
│   │   └── markdown/
│   └── chroma_db/
├── src/
│   ├──data/
│   │   ├──chroma_db/
│   │   └──chroma.sqlite3
│   ├── extractors.py
│   ├── chunker.py
│   ├── vector_store.py
│   ├── search.py
│   ├── check_db.py
│   └── reset_db.py
├── tests/
│   ├── test_chunker.py
│   ├── test_extractors.py
│   └── test_pipeline.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

*The structure above describes the intended layout; adjust filenames if your repository differs.*

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/FarazMemon004/Datheon_Forward_Deployed_Engineering_Internship/tree/main/%20Datheon%20FDE%20%E2%80%94%20Task%201_Client%20Legacy%20Data%20Ingestion%20%26%20Vector%20ETL%20Pipeline
cd Task 1-Client Legacy Data Ingestion & Vector ETL Pipeline
```

Navigate into the Task 1 project directory if it is stored inside this repository.

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Usage

### 1. Add source documents

Place supported files in the appropriate directories under `data/raw/`:

- `data/raw/pdf/`
- `data/raw/csv/`
- `data/raw/markdown/`

You can organize additional files into subdirectories.

### 2. Ingest documents

From the project root, run:

```bash
PYTHONPATH=. python -m src.vector_store
```

The pipeline extracts supported files, chunks the text, creates embeddings, and stores the chunks in the persistent ChromaDB collection.

### 3. Search documents

```bash
PYTHONPATH=. python -m src.search
```

Example queries:

```text
Who works in Engineering?
Who manages Human Resources?
Who works in Finance?
```

You can provide a department filter and an access-tier filter to narrow the results.

### 4. Check the vector database

```bash
PYTHONPATH=. python -m src.check_db
```

## Running Tests

Run the automated pipeline tests:

```bash
python -m pytest tests/test_pipeline.py -v
```

Run the full test suite:

```bash
python -m pytest -v
```

**Current validation:** 6 pipeline tests passed on Python 3.11.8.

## Metadata

The pipeline preserves metadata where available:

| Field | Description |
|---|---|
| `source` | Original filename |
| `file_type` | Document extension |
| `department` | Associated department |
| `access_tier` | Document access classification |
| `document_date` | Date recorded in document metadata |
| `employee_id` | Employee identifier for CSV records |
| `chunk_index` | Position of the chunk within its source |

Metadata availability depends on the source document. Missing values may be represented as `Unknown`.

## Vector Search

The project uses Sentence Transformers to generate embeddings and ChromaDB to retrieve semantically similar text chunks. The collection is configured to use cosine distance.

**Note:** Cosine distance is a similarity-search metric, not a confidence score. Lower distances generally indicate closer vectors. Search returns relevant text chunks; it does not independently generate natural-language answers.

## Limitations and Future Improvements

- Improve metadata validation and support additional metadata formats.
- Add more automated tests for PDF extraction and vector-search filtering.
- Add configurable access-control enforcement before returning restricted documents.
- Support larger document collections through batch processing.
- Add a retrieval-augmented generation layer for answer synthesis and source citations.
- Add a command-line interface and structured logging.

## Project Context

**Program:** Datheon Forward Deployed Engineering Internship  
**Task:** Client Legacy Data Ingestion & Vector ETL Pipeline

## Author

**Muhammad Faraz Memon**

- GitHub: https://github.com/FarazMemon004
- LinkedIn: https://www.linkedin.com/in/muhammad-faraz-memon-92582a43a/
