
import chromadb

client = chromadb.PersistentClient(path="data/chroma_db")
collection_name = "datheon_legacy_documents"

try:
    client.delete_collection(collection_name)
    print("Old collection deleted.")
except Exception:
    print("Collection did not exist; nothing to delete.")

print("Now run: PYTHONPATH=. python -m src.vector_store")
