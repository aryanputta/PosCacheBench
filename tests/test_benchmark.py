import unittest

from poscachebench.benchmark import BenchmarkConfig, run_benchmark
from poscachebench.encodings import ENCODINGS
from poscachebench.policies import ChunkScore, budget_to_count, select_chunks


class BenchmarkTests(unittest.TestCase):
    def test_budget_to_count(self):
        self.assertEqual(budget_to_count(10, 0.25), 2)
        self.assertEqual(budget_to_count(10, 0.01), 1)

    def test_recent_policy_respects_budget(self):
        scores = [ChunkScore(i, 1.0, 1.0, 1.0, 10 - i) for i in range(10)]
        selected = select_chunks("recent", scores, 3)
        self.assertEqual(selected, {7, 8, 9})

    def test_encodings_are_positive(self):
        for encoding in ENCODINGS.values():
            self.assertGreater(encoding.weight(1, 100), 0)


if __name__ == "__main__":
    unittest.main()

