"""Reproducible size benchmark for fastpath (stdlib only).

Run: python benchmark.py
Prints a markdown table of characters kept/omitted for representative tool
result sizes using the plugin's default limit (12,000 chars, head 60% / tail 40%).
"""

from __future__ import annotations

import importlib.util
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("fastpath_benchmark", ROOT / "__init__.py")
fastpath = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(fastpath)

_tmp = tempfile.TemporaryDirectory(prefix="fastpath-bench-")
fastpath._home = lambda: Path(_tmp.name)

SAMPLES = [
    ("web_extract — short page", 2_000),
    ("web_search — search dump", 20_000),
    ("read_file — large source", 80_000),
]


def measure(size: int) -> dict:
    """Compress a printable string of `size` chars at default settings."""
    fastpath._STATE = dict(fastpath.DEFAULTS)
    result = "".join(chr(33 + (i % 90)) for i in range(size))
    out = fastpath._compress(result)
    if out is None:
        return {
            "original": size,
            "kept": size,
            "omitted": 0,
            "marker_chars": 0,
            "output": size,
            "saved_pct": 0.0,
            "saved_chars": 0,
        }
    limit = fastpath.DEFAULTS["max_chars"]
    return {
        "original": size,
        "kept": limit,
        "omitted": size - limit,
        "marker_chars": len(out) - limit,
        "output": len(out),
        "saved_pct": round(100 * (size - len(out)) / size, 1),
        "saved_chars": size - len(out),
    }


def main() -> None:
    print("| Tool result | Original chars | Kept chars | Omitted chars | Output chars | Saved |")
    print("|---|---:|---:|---:|---:|---:|")
    for label, size in SAMPLES:
        r = measure(size)
        print(
            f"| {label} | {r['original']:,} | {r['kept']:,} | {r['omitted']:,} | "
            f"{r['output']:,} | {r['saved_pct']}% |"
        )


if __name__ == "__main__":
    main()
