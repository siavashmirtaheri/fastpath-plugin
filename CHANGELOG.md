# Changelog

## 1.0.0

- Initial release: `transform_tool_result` head+tail compression with an
  explicit omission marker, `pre_llm_call` extension point, and `/fastpath`
  status/on/off/limit/reset command.
- Local state at `~/.hermes/fastpath/state.json` with truncation and
  characters-saved counters.
- Fail-open hook: any error leaves the original tool result unchanged.
- State loading ignores missing, corrupt or wrong-typed files; `head_ratio`
  is clamped to 0..1 and a zero tail never duplicates the head.
- stdlib-only functional test suite (12 tests) plus GitHub Actions test run.
- Reproducible size benchmark (`benchmark.py`, `docs/benchmark.md`): ~85%
  fewer characters on an 80k-char tool result at the default limit.
- Marketplace banner and status screenshot, plus ready-to-copy promo text.
- Published to the Hermes plugin catalog and suggested to awesome-hermes-agent.
- Sponsorship credit added: Metadigi (https://metadigi.ir).
