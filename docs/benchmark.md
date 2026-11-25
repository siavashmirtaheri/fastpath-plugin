# Size benchmark

`benchmark.py` is a reproducible, dependency-free measurement of how much
context fastpath keeps for representative tool results at the default settings
(`max_chars: 12000`, `head_ratio: 0.6`). Run it from the repo root:

```bash
python benchmark.py
```

Output (generated 2026-11-25):

| Tool result | Original chars | Kept chars | Omitted chars | Output chars | Saved |
|---|---:|---:|---:|---:|---:|
| web_extract — short page | 2,000 | 2,000 | 0 | 2,000 | 0% |
| web_search — search dump | 20,000 | 12,000 | 8,000 | 12,102 | 39.5% |
| read_file — large source | 80,000 | 12,000 | 68,000 | 12,103 | 84.9% |

Kept chars are `head 7,200 + tail 4,800`. The output adds a short omission
marker (~102 chars) that tells the model content was skipped and suggests a
narrower query or a higher `/fastpath limit`.

## Interpretation

- Results at or below the limit are never touched — no marker, no counters.
- Savings grow with result size; an 80k-char file read sends ~85% fewer chars
  to the model while still preserving the beginning and the end.
- The middle is not stored anywhere. The only disk write is the small state
  file (`~/.hermes/fastpath/state.json`) holding the enable flag, limit and
  truncation/savings counters.
- Numbers are character counts, not token counts. In practice tokens saved
  scale with characters; `/fastpath` reports a rough `chars // 4` estimate.

## Reproduce / adjust

```bash
python -m unittest discover -s tests -v   # 12 tests, includes benchmark checks
python benchmark.py                        # regenerate the table
```

Raise or lower the limit at runtime with `/fastpath limit N` (minimum 1000).
To benchmark a different configuration, edit `SAMPLES` in `benchmark.py`.
