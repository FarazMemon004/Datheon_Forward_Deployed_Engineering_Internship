from src.vector_store import VectorStore

store = VectorStore()

print("Database check")
print("Collection:", store.collection.name)
print("Stored documents:", store.collection.count())

if store.collection.count() > 0:
    results = store.collection.get(
        limit=5,
        include=["documents", "metadatas"],
    )

    for i, doc in enumerate(results["documents"]):
        print(f"\nDocument {i + 1}:")
        print("ID:", results["ids"][i])
        print("Metadata:", results["metadatas"][i])
        print("Text:", doc[:150])
else:
    print("The collection is empty. Run ingestion again.")
