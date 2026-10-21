import json
import re
import unicodedata
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent.parent
DATASET_FILE = PROJECT_DIR / "dataset" / "hindi_documents_100.json"
INDEX_FILE = PROJECT_DIR / "output" / "positional_index.json"


def tokenize(text):
    """Return normalized Hindi, English, and numeric tokens from text."""
    text = unicodedata.normalize("NFC", text.lower())
    pattern = r"[\u0900-\u097F]+|[A-Za-z]+|\d+"
    return re.findall(pattern, text)


def build_index(documents):
    """Build term -> document ID -> list of 1-based token positions."""
    index = {}

    for document in documents:
        doc_id = document["docid"]
        words = tokenize(document["text"])

        for position, word in enumerate(words, start=1):
            if word not in index:
                index[word] = {}

            if doc_id not in index[word]:
                index[word][doc_id] = []

            index[word][doc_id].append(position)

    return index


def term_query(index, term):
    """Return document IDs containing a single search term."""
    words = tokenize(term)

    if len(words) != 1:
        return []

    return sorted(index.get(words[0], {}).keys())


def phrase_query(index, phrase):
    """Return documents where all phrase words occur consecutively and in order."""
    words = tokenize(phrase)

    if not words:
        return []

    # A matching document must contain every word in the phrase.
    candidate_docs = set(index.get(words[0], {}).keys())
    for word in words[1:]:
        candidate_docs.intersection_update(index.get(word, {}).keys())

    matches = []

    for doc_id in candidate_docs:
        first_word_positions = index[words[0]][doc_id]

        # Try each occurrence of the first word as the phrase's starting point.
        for start_position in first_word_positions:
            phrase_found = True

            for offset, word in enumerate(words[1:], start=1):
                required_position = start_position + offset
                word_positions = index[word][doc_id]

                if required_position not in word_positions:
                    phrase_found = False
                    break

            if phrase_found:
                matches.append(doc_id)
                break

    return sorted(matches)


def proximity_query(index, term1, term2, distance):
    """Find documents where two single terms are at most distance positions apart."""
    words1 = tokenize(term1)
    words2 = tokenize(term2)

    if len(words1) != 1 or len(words2) != 1:
        raise ValueError("Enter exactly one word for each proximity term.")

    if not isinstance(distance, int) or distance < 0:
        raise ValueError("Distance must be a non-negative whole number.")

    word1 = words1[0]
    word2 = words2[0]

    docs1 = index.get(word1, {})
    docs2 = index.get(word2, {})
    common_docs = set(docs1.keys()) & set(docs2.keys())

    matches = []

    for doc_id in common_docs:
        positions1 = docs1[doc_id]
        positions2 = docs2[doc_id]

        close_enough = any(
            abs(position1 - position2) <= distance
            for position1 in positions1
            for position2 in positions2
        )

        if close_enough:
            matches.append(doc_id)

    return sorted(matches)


def load_documents():
    """Read and validate the bundled JSON document collection."""
    with open(DATASET_FILE, "r", encoding="utf-8") as file:
        documents = json.load(file)

    if not isinstance(documents, list):
        raise ValueError("The dataset must contain a JSON list of documents.")

    for document in documents:
        if "docid" not in document or "text" not in document:
            raise ValueError("Every document must have 'docid' and 'text' fields.")

    return documents


def save_index(index):
    """Save the positional index as readable UTF-8 JSON."""
    INDEX_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(INDEX_FILE, "w", encoding="utf-8") as file:
        json.dump(index, file, ensure_ascii=False, indent=2)


def main():
    try:
        documents = load_documents()
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print("Could not load the Hindi dataset:", error)
        return

    index = build_index(documents)
    save_index(index)

    print(f"Loaded {len(documents)} Hindi documents")
    print(f"Indexed {len(index)} unique terms")
    print(f"Positional index saved to {INDEX_FILE.relative_to(PROJECT_DIR)}")

    print("\nExamples:")
    print(
        'Phrase: "शिक्षा में तकनीक" ->',
        phrase_query(index, "शिक्षा में तकनीक"),
    )
    print(
        "Proximity: शिक्षा, तकनीक, distance=5 ->",
        proximity_query(index, "शिक्षा", "तकनीक", 5),
    )

    print("\nInteractive retrieval")
    print("1 = term, 2 = phrase, 3 = proximity, q = quit")

    while True:
        choice = input("\nChoice: ").strip().lower()

        if choice == "q":
            print("Exiting search.")
            break

        try:
            if choice == "1":
                query = input("Term: ").strip()
                print("Documents:", term_query(index, query))

            elif choice == "2":
                query = input("Phrase: ").strip()
                print("Documents:", phrase_query(index, query))

            elif choice == "3":
                first_term = input("First term: ").strip()
                second_term = input("Second term: ").strip()
                distance_text = input("Maximum distance: ").strip()
                distance = int(distance_text)

                print(
                    "Documents:",
                    proximity_query(index, first_term, second_term, distance),
                )

            else:
                print("Choose 1, 2, 3 or q.")

        except ValueError as error:
            print("Input error:", error)


if __name__ == "__main__":
    main()
