import unittest

from src.positional_index import (
    build_index,
    phrase_query,
    proximity_query,
    term_query,
    tokenize,
)


SAMPLE_DOCUMENTS = [
    {"docid": "doc1", "text": "शिक्षा में तकनीक उपयोगी है"},
    {"docid": "doc2", "text": "तकनीक शिक्षा में मदद करती है"},
    {"docid": "doc3", "text": "शिक्षा शिक्षा में बदलाव"},
]


class PositionalIndexTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.index = build_index(SAMPLE_DOCUMENTS)

    def test_tokenize_hindi(self):
        self.assertEqual(tokenize("शिक्षा, में तकनीक!"), ["शिक्षा", "में", "तकनीक"])

    def test_term_query(self):
        self.assertEqual(term_query(self.index, "शिक्षा"), ["doc1", "doc2", "doc3"])

    def test_phrase_query_exact_order(self):
        self.assertEqual(phrase_query(self.index, "शिक्षा में तकनीक"), ["doc1"])

    def test_phrase_query_wrong_order_does_not_match(self):
        self.assertEqual(phrase_query(self.index, "तकनीक में शिक्षा"), [])

    def test_repeated_word_phrase(self):
        self.assertEqual(phrase_query(self.index, "शिक्षा शिक्षा"), ["doc3"])

    def test_proximity_query(self):
        self.assertEqual(
            proximity_query(self.index, "शिक्षा", "तकनीक", 2),
            ["doc1", "doc2"],
        )

    def test_negative_distance_is_rejected(self):
        with self.assertRaises(ValueError):
            proximity_query(self.index, "शिक्षा", "तकनीक", -1)


if __name__ == "__main__":
    unittest.main()
