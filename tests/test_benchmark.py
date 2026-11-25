"""Checks that the benchmark reports real numbers (stdlib unittest)."""

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location("fastpath_benchmark_test", ROOT / "benchmark.py")
benchmark = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(benchmark)


class BenchmarkTests(unittest.TestCase):
    def test_small_result_is_not_compressed(self):
        r = benchmark.measure(2_000)
        self.assertEqual(r["omitted"], 0)
        self.assertEqual(r["saved_pct"], 0.0)

    def test_large_result_is_compressed(self):
        r = benchmark.measure(80_000)
        self.assertEqual(r["kept"], 12_000)
        self.assertEqual(r["omitted"], 68_000)
        self.assertGreater(r["output"], 12_000)  # marker adds a few chars
        self.assertLess(r["output"], 80_000)
        self.assertGreater(r["saved_pct"], 80)

    def test_sample_table_has_rows(self):
        self.assertEqual(len(benchmark.SAMPLES), 3)


if __name__ == "__main__":
    unittest.main()
