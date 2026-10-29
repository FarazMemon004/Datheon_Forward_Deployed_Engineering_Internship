
from pathlib import Path
from typing import Any

import chromadb
from sentence_transformers import SentenceTransformer

from src.chunker import chunk_document
from src.extractors import extract_directory


DEFAULT_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
DEFAULT_COLLECTION = "datheon_legacy_documents"


class VectorStore:
    def __init__(
        self,
        persist_directory: str = "data/chroma_db",
        collection_name: str = DEFAULT_COLLECTION,
        model_name: str = DEFAULT_MODEL,
    ):
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.model = SentenceTransformer(model_name)

        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"},
        )

    def add_chunks(self, chunks: list[dict[str, Any]]) -> int:
        if not chunks:
            return 0

        self.collection.upsert(
            ids=[chunk["id"] for chunk in chunks],
            documents=[chunk["text"] for chunk in chunks],
            metadatas=[chunk["metadata"] for chunk in chunks],
            embeddings=self.model.encode(
                [chunk["text"] for chunk in chunks],
                normalize_embeddings=True,
            ).tolist(),
        )
        return len(chunks)

    def search(
        self,
        query: str,
        n_results: int = 3,
        department: str | None = None,
        access_tier: str | None = None,
    ) -> dict[str, Any]:
        filters = []

        if department:
            filters.append({"department": department})

        if access_tier:
            filters.append({"access_tier": access_tier})

        where = None
        if len(filters) == 1:
            where = filters[0]
        elif len(filters) > 1:
            where = {"$and": filters}

        query_embedding = self.model.encode(
            [query],
            normalize_embeddings=True,
        ).tolist()

        return self.collection.query(
            query_embeddings=query_embedding,
            n_results=min(n_results, max(self.collection.count(), 1)),
            where=where,
            include=["documents", "metadatas", "distances"],
        )


def ingest_directory(
    directory: str = "data/raw",
    persist_directory: str = "data/chroma_db",
) -> int:
    store = VectorStore(persist_directory=persist_directory)
    documents = extract_directory(Path(directory))

    chunks = []
    for document in documents:
        chunks.extend(chunk_document(document))

    count = store.add_chunks(chunks)
    print(f"\nStored {count} chunks in ChromaDB.")
    print(f"Collection total: {store.collection.count()}")
    return count


if __name__ == "__main__":
    ingest_directory()
