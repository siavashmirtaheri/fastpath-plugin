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
- stdlib-only functional test suite (9 tests) plus GitHub Actions test run.
- Published to the Hermes plugin catalog and the awesome-hermes-agent list.
