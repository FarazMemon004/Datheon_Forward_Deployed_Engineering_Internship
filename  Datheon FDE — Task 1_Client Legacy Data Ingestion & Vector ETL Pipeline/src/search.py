
from src.vector_store import VectorStore


def main():
    store = VectorStore()

    print("\nDatheon Legacy Document Semantic Search")
    print("Type 'exit' to quit.")
    print("Leave department blank to search all departments.\n")

    while True:
        query = input("Search query: ").strip()

        if query.lower() in {"exit", "quit"}:
            break

        if not query:
            continue

        department = input(
            "Department filter (Engineering, Human Resources, Finance, IT; "
            "Enter for all): "
        ).strip()

        if not department:
            department = None

        access_tier = input(
            "Access tier filter (Internal, Confidential; Enter for all): "
        ).strip()

        if not access_tier:
            access_tier = None

        results = store.search(
            query,
            n_results=3,
            department=department,
            access_tier=access_tier,
        )

        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]

        if not documents:
            print("No matching documents found.")
            continue

        for index, text in enumerate(documents):
            metadata = metadatas[index]

            print("\n" + "=" * 50)
            print("Source:", metadata.get("source"))
            print("Department:", metadata.get("department"))
            print("Employee ID:", metadata.get("employee_id", "N/A"))
            print("Access tier:", metadata.get("access_tier"))
            print("Cosine distance:", round(distances[index], 4))
            print(text)


if __name__ == "__main__":
    main()
