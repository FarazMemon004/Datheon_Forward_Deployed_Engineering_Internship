
from pathlib import Path

from src.extractors import extract_directory
from src.chunker import chunk_document


def main():
    documents = extract_directory(Path("data/raw"))

    all_chunks = []

    for document in documents:
        chunks = chunk_document(document)
        all_chunks.extend(chunks)

        print(f"\nSource: {document['source']}")
        print(f"Chunks created: {len(chunks)}")

        for chunk in chunks:
            print("-" * 50)
            print("ID:", chunk["id"])
            print("Metadata:", chunk["metadata"])
            print("Text:", chunk["text"][:200])

    print(f"\nTotal chunks created: {len(all_chunks)}")


if __name__ == "__main__":
    main()
