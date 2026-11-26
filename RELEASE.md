# fastpath v1.0.0

Context-diet plugin for Hermes Agent. Compresses oversized tool results before they enter the model context (head 60% + tail 40% + omission marker), reducing tokens, latency and cost.

Author: Siavash Mirtaheri (BlackVash)
Backed by Metadigi — https://metadigi.ir
License: MIT
Requires Hermes >= 0.23

## Install

1. Download `fastpath-plugin-1.0.0.zip` and extract it.
2. Copy the `fastpath` folder into `<HERMES_HOME>/plugins/` (e.g. `~/.hermes/plugins/fastpath/`).
3. Add `fastpath` to `plugins.enabled` in `<HERMES_HOME>/config.yaml`:

   ```yaml
   plugins:
     enabled:
       - fastpath
   ```

4. Restart the gateway, then run `/fastpath` to confirm the plugin is active.

## Commands

/fastpath | /fastpath on|off | /fastpath limit N | /fastpath reset

## Tests

The package ships a stdlib-only functional test suite (12 tests) and a
reproducible size benchmark:

```bash
python -m unittest discover -s fastpath/tests -v
python fastpath/benchmark.py
```

Results: an 80,000-char tool result keeps 12,000 chars — ~85% fewer chars
sent to the model. See `fastpath/docs/benchmark.md`.

## Artifact
fastpath-plugin-1.0.0.zip
SHA256: fb3a38f2edfd9c671cbdd79da4b23ea4033bf23e51ada5f79d26a115aff8c3a5
