"""Functional tests for the fastpath plugin (stdlib unittest only).

Run from the repository root:
    python -m unittest discover -s tests -v
"""

from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

PLUGIN_PATH = Path(__file__).resolve().parents[1] / "__init__.py"

_spec = importlib.util.spec_from_file_location("fastpath_under_test", PLUGIN_PATH)
fastpath = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(fastpath)


class FakeContext:
    def __init__(self):
        self.hooks = {}
        self.commands = {}

    def register_hook(self, name, handler):
        self.hooks[name] = handler

    def register_command(self, name, handler, description=""):
        self.commands[name] = (handler, description)


class FastpathTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(prefix="fastpath-test-")
        self.home = Path(self._tmp.name)
        fastpath._home = lambda: self.home
        fastpath._STATE = None
        self.ctx = FakeContext()
        fastpath.register(self.ctx)
        self.transform = self.ctx.hooks["transform_tool_result"]
        self.command = self.ctx.commands["fastpath"][0]

    def tearDown(self):
        self._tmp.cleanup()

    @property
    def state_file(self):
        return self.home / "fastpath" / "state.json"

    def test_registration(self):
        self.assertEqual(set(self.ctx.hooks), {"transform_tool_result", "pre_llm_call"})
        self.assertIn("fastpath", self.ctx.commands)
        self.assertIsNone(fastpath._pre_llm_call())

    def test_short_and_non_string_results_are_untouched(self):
        self.assertIsNone(self.transform(result="short"))
        self.assertIsNone(self.transform(result=12345))
        self.assertIsNone(self.transform(result=None))
        self.assertFalse(self.state_file.exists())

    def test_compression_head_tail_and_marker(self):
        state = fastpath._get_state()
        state["max_chars"] = 1000
        original = "A" * 700 + "B" * 700

        result = self.transform(result=original)

        self.assertIsInstance(result, str)
        self.assertEqual(result[:600], "A" * 600)
        self.assertEqual(result[-400:], original[-400:])
        self.assertIn("fastpath omitted 400 chars", result)
        self.assertEqual(len(original), 1400)  # source string untouched

    def test_counters_are_saved_and_reloaded(self):
        fastpath._get_state()["max_chars"] = 1000
        self.transform(result="X" * 2500)

        saved = json.loads(self.state_file.read_text(encoding="utf-8"))
        self.assertEqual(saved["truncations"], 1)
        self.assertEqual(saved["chars_saved"], 1500)

        reloaded = fastpath._load()
        self.assertEqual(reloaded["truncations"], 1)
        self.assertEqual(reloaded["chars_saved"], 1500)

    def test_disabled_and_small_limit_are_skipped(self):
        state = fastpath._get_state()
        big = "Y" * 5000
        state["enabled"] = False
        self.assertIsNone(self.transform(result=big))
        state["enabled"] = True
        state["max_chars"] = 999
        self.assertIsNone(self.transform(result=big))

    def test_ratio_is_clamped_and_tail_never_duplicates(self):
        state = fastpath._get_state()
        state["max_chars"] = 1000
        state["head_ratio"] = 1.0  # would make tail 0; result[-0:] is the whole string
        original = "Z" * 3000

        result = self.transform(result=original)

        self.assertEqual(result.count("fastpath omitted"), 1)
        self.assertLess(len(result), len(original))
        self.assertTrue(result.startswith(original[:1000]))
        self.assertEqual(result.count("Z" * 1000), 1)  # tail must not duplicate the head

        state["head_ratio"] = 5.0  # clamped to 1.0
        result2 = self.transform(result=original)
        self.assertLess(len(result2), len(original))

    def test_corrupt_or_wrong_typed_state_is_ignored(self):
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        self.state_file.write_text("{ not json", encoding="utf-8")
        fastpath._STATE = None
        self.assertEqual(fastpath._get_state()["max_chars"], 12000)

        self.state_file.write_text(
            json.dumps({"max_chars": "oops", "enabled": "false", "head_ratio": "bad"}),
            encoding="utf-8",
        )
        fastpath._STATE = None
        state = fastpath._get_state()
        self.assertEqual(state["max_chars"], 12000)
        self.assertFalse(state["enabled"])
        self.assertEqual(state["head_ratio"], 0.6)

    def test_hook_is_fail_open(self):
        original_get_state = fastpath._get_state

        def broken():
            raise RuntimeError("simulated hook failure")

        fastpath._get_state = broken
        try:
            self.assertIsNone(self.transform(result="Q" * 100000))
        finally:
            fastpath._get_state = original_get_state

    def test_commands(self):
        status = self.command("")
        self.assertIn("on", status)
        self.assertIn("limit=12,000", status)

        self.assertEqual(self.command("off"), "fastpath: off")
        self.assertFalse(fastpath._get_state()["enabled"])
        self.assertEqual(self.command("on"), "fastpath: on")
        self.assertTrue(fastpath._get_state()["enabled"])

        self.assertEqual(self.command("limit 8000"), "fastpath: limit=8,000 chars")
        self.assertEqual(fastpath._get_state()["max_chars"], 8000)
        self.assertEqual(self.command("limit 10"), "limit must be >= 1000")
        self.assertEqual(self.command("limit abc"), "usage: /fastpath limit <integer>")

        self.assertEqual(self.command("reset"), "fastpath: counters reset")
        self.assertEqual(fastpath._get_state()["truncations"], 0)
        self.assertEqual(fastpath._get_state()["chars_saved"], 0)


if __name__ == "__main__":
    unittest.main()
