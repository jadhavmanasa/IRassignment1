import json
from pathlib import Path

from datasets import load_dataset


PROJECT_DIR = Path(__file__).resolve().parent
OUTPUT_FILE = PROJECT_DIR / "dataset" / "hindi_documents_100.json"

# Public Parquet export of the Hindi MIRACL training split.
PARQUET_URL = (
    "https://huggingface.co/datasets/miracl/miracl-corpus/"
    "resolve/refs%2Fconvert%2Fparquet/hi/train/0000.parquet"
)


def main():
    print("Loading MIRACL Hindi corpus...")

    dataset = load_dataset(
        "parquet",
        data_files={"train": PARQUET_URL},
        split="train",
        streaming=True,
    )

    documents = []
    for row in dataset:
        documents.append({
            "docid": row["docid"],
            "text": row["text"],
        })
        if len(documents) == 100:
            break

    if len(documents) != 100:
        raise RuntimeError(
            f"Expected 100 documents, but retrieved {len(documents)}."
        )

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(documents, file, ensure_ascii=False, indent=2)

    print(f"Saved {len(documents)} documents to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
