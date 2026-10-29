
from pathlib import Path

from src.extractors import extract_directory


def main():
    data_directory = Path("data/raw")

    documents = extract_directory(data_directory)

    print(f"\nTotal documents extracted: {len(documents)}")

    for document in documents:
        print("\n" + "=" * 50)
        print("Source:", document["source"])
        print("Type:", document["file_type"])
        print("Characters:", document["character_count"])
        print("Preview:", document["text"][:250])


if __name__ == "__main__":
    main()
