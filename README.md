# fastpath

Context-diet plugin for Hermes Agent. It compresses oversized tool results
before they enter the model context, reducing token use, latency and cost.

## What it does

- Registers `transform_tool_result`: any string tool result longer than the
  configured limit is replaced by its first 60% + last 40%, with an explicit
  omission marker so the model knows content was skipped.
- Registers `pre_llm_call` as a no-op extension point (stable manifest).
- Adds `/fastpath` slash command.

## Commands

| Command | Effect |
|---|---|
| `/fastpath` | status + savings |
| `/fastpath on` / `off` | enable/disable compression |
| `/fastpath limit 8000` | set max kept characters (default 12000) |
| `/fastpath reset` | reset counters |

State lives at `~/.hermes/fastpath/state.json` (respects `HERMES_HOME`).

## Safety

- Never modifies the original tool output on disk; only replaces what is
  handed to the model for that turn.
- Skips non-string results and anything under the limit.
- Errors are logged and degradation is fail-open: a broken hook leaves the
  result unchanged.

## Author

Siavash Mirtaheri (BlackVash) — 2026. MIT license.
