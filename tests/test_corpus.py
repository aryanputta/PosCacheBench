import unittest

from poscachebench.corpus import Document, build_tasks, chunk_tokens, tokenize


class CorpusTests(unittest.TestCase):
    def test_tokenize_strips_links(self):
        tokens = tokenize("[FlashAttention](https://example.com) uses [[KV cache]] state.")
        self.assertIn("flashattention", tokens)
        self.assertIn("kv", tokens)
        self.assertIn("cache", tokens)
        self.assertNotIn("https", tokens)

    def test_chunk_tokens(self):
        chunks = chunk_tokens(tuple(str(i) for i in range(10)), 4)
        self.assertEqual(len(chunks), 3)
        self.assertEqual(chunks[0], ("0", "1", "2", "3"))

    def test_build_tasks_from_realistic_document(self):
        tokens = tuple(f"token{i % 20}" for i in range(1000)) + tuple("uniquealpha uniquebeta uniquegamma".split())
        doc = Document("doc0", "Doc", "doc.md", tokens)
        tasks = build_tasks([doc], chunk_size=64)
        self.assertGreaterEqual(len(tasks), 1)


if __name__ == "__main__":
    unittest.main()

