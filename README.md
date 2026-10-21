# Hindi Positional Inverted Index

## Project purpose

This Information Retrieval mini-project builds a positional inverted index for Hindi text written in Devanagari. It supports term search, exact phrase search, and proximity search.

## Dataset

The main dataset is `dataset/hindi_documents_100.json`, containing 100 documents downloaded from the Hindi portion of the MIRACL corpus. Each document has a `docid` and a `text` field.

The downloader writes to this file and does not overwrite any other dataset file. The original sample dataset is not included in this project archive.

Dataset source: [MIRACL corpus on Hugging Face](https://huggingface.co/datasets/miracl/miracl-corpus). Check the dataset's current licence and citation instructions before redistributing the dataset or submitting it.

## How the index works

For each term, the index stores the document IDs where it appears and the 1-based positions of its occurrences. A simplified example:

```json
{
  "शिक्षा": {
    "doc01": [2, 8],
    "doc02": [4]
  }
}
```

This means `शिक्षा` occurs at positions 2 and 8 in `doc01`, and at position 4 in `doc02`.

## Search features

- **Term search:** finds documents containing a single term.
- **Phrase search:** finds documents where all words appear consecutively and in the specified order.
- **Proximity search:** finds documents where two single terms occur at positions whose absolute difference is no greater than the specified distance.

Positions start at 1. For example, a proximity distance of 5 accepts position pairs with an absolute difference of at most 5.

## Project structure

```text
hindi-positional-index/
├── dataset/
│   └── hindi_documents_100.json
├── output/
│   ├── positional_index.json
│   └── sample_output.txt
├── src/
│   ├── __init__.py
│   └── positional_index.py
├── download_miracl_subset.py
├── positional_index.py
├── test_positional_index.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Requirements

- Python 3.10 or newer
- The bundled 100-document dataset for running the index
- Internet access and the `datasets` package only if downloading the corpus again

The indexer itself uses only Python's standard library.

## Run the project

Open a terminal in the project root, the folder containing `dataset`, `src`, and `positional_index.py`, then run:

```powershell
python positional_index.py
```

The program loads the configured dataset, builds the index, writes `output/positional_index.json`, prints example queries, and opens an interactive menu.

- Enter `1` for term search.
- Enter `2` for phrase search.
- Enter `3` for proximity search.
- Enter `q` to quit.

The example queries may return empty results because the selected 100 documents do not necessarily contain those words or phrases.

## Download the dataset again (optional)

Install the dependency:

```powershell
python -m pip install -r requirements.txt
```

Then run:

```powershell
python download_miracl_subset.py
```

The script saves 100 documents to `dataset/hindi_documents_100.json`. Running it again replaces that same downloaded-subset file.

## Run the tests

From the project root:

```powershell
python -m unittest -v
```

The tests use a small in-memory sample collection to check tokenization, term lookup, phrase order, repeated words, proximity matching, and invalid distances.

## Sample run

The included sample output was generated using the bundled 100-document dataset. It reported 100 documents and 1,953 unique terms. Exact query results depend on the dataset contents.
