"""fastpath — context-diet plugin for Hermes Agent.

Compresses oversized tool results (web pages, search dumps, file reads) before
they enter the model context. Fewer tokens in = faster turns, lower cost,
less context-compression churn.

Hooks:
  * transform_tool_result — head+tail compression with an explicit omission marker
  * pre_llm_call          — no-op today; kept as a stable extension point

Command:
  /fastpath              -> status
  /fastpath on|off       -> toggle
  /fastpath limit N      -> set max kept characters (default 12000)
  /fastpath reset        -> reset counters
"""

from __future__ import annotations

import logging
from pathlib import Path

logger = logging.getLogger("fastpath")

_STATE = None

DEFAULTS = {
    "enabled": True,
    "max_chars": 12000,
    "head_ratio": 0.6,
    "truncations": 0,
    "chars_saved": 0,
}


def _home() -> Path:
    try:
        from hermes_constants import get_hermes_home
        return Path(get_hermes_home())
    except Exception:  # pragma: no cover - defensive
        return Path.home() / ".hermes"


def _state_path() -> Path:
    return _home() / "fastpath" / "state.json"


def _load() -> dict:
    state = dict(DEFAULTS)
    try:
        data = __import__("json").loads(_state_path().read_text(encoding="utf-8"))
        if isinstance(data, dict):
            state.update({k: v for k, v in data.items() if k in DEFAULTS})
    except Exception:
        pass
    return state


def _save(state: dict) -> None:
    try:
        path = _state_path()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(__import__("json").dumps(state, indent=2), encoding="utf-8")
    except Exception as exc:
        logger.warning("fastpath: could not persist state: %s", exc)


def _get_state() -> dict:
    global _STATE
    if _STATE is None:
        _STATE = _load()
    return _STATE


def register(ctx) -> None:
    global _STATE
    _STATE = _load()
    ctx.register_hook("transform_tool_result", _transform_tool_result)
    ctx.register_hook("pre_llm_call", _pre_llm_call)
    ctx.register_command(
        name="fastpath",
        handler=_command,
        description="Context-diet controls: /fastpath [status|on|off|limit N|reset]",
    )
    logger.info("fastpath registered (enabled=%s, limit=%s)", _STATE["enabled"], _STATE["max_chars"])


def _transform_tool_result(**kwargs):
    """Replace a too-long tool result with head + tail + omission marker.

    Hermes reads the returned string as the tool result. Returning None leaves
    the original result untouched. Nothing is written to disk except counters.
    """
    state = _get_state()
    if not state.get("enabled", True):
        return None
    result = kwargs.get("result")
    if not isinstance(result, str):
        return None
    limit = int(state.get("max_chars", 12000))
    if limit < 1000 or len(result) <= limit:
        return None

    head_ratio = float(state.get("head_ratio", 0.6))
    head = int(limit * head_ratio)
    tail = limit - head
    omitted = len(result) - limit
    marker = (
        f"\n\n… [fastpath omitted {omitted:,} chars to save context. "
        f"Use a narrower query, or /fastpath limit {max(limit, omitted + limit)}] …\n\n"
    )
    state["truncations"] = int(state.get("truncations", 0)) + 1
    state["chars_saved"] = int(state.get("chars_saved", 0)) + omitted
    _save(state)
    return result[:head] + marker + result[-tail:]


def _pre_llm_call(**kwargs):
    """Reserved extension point; intentionally does nothing.

    Keeping the hook registered lets a future version add prompt-level routing
    without changing the plugin manifest or requiring a gateway restart.
    """
    return None


def _command(args: str):
    state = _get_state()
    parts = (args or "").strip().split()
    if not parts:
        parts = ["status"]
    op = parts[0].lower()

    if op == "on":
        state["enabled"] = True
        _save(state)
        return "fastpath: on"
    if op == "off":
        state["enabled"] = False
        _save(state)
        return "fastpath: off"
    if op == "limit" and len(parts) > 1:
        try:
            value = int(parts[1])
        except ValueError:
            return "usage: /fastpath limit <integer>"
        if value < 1000:
            return "limit must be >= 1000"
        state["max_chars"] = value
        _save(state)
        return f"fastpath: limit={value:,} chars"
    if op == "reset":
        state["truncations"] = 0
        state["chars_saved"] = 0
        _save(state)
        return "fastpath: counters reset"

    saved = int(state.get("chars_saved", 0))
    return (
        f"fastpath: {'on' if state.get('enabled') else 'off'} · "
        f"limit={int(state.get('max_chars', 12000)):,} chars · "
        f"truncated {int(state.get('truncations', 0))} result(s) · "
        f"~{saved:,} chars saved (~{saved // 4:,} tokens)"
    )
