# fastpath v1.0.0

Context-diet plugin for Hermes Agent. Compresses oversized tool results before they enter the model context (head 60% + tail 40% + omission marker), reducing tokens, latency and cost.

Author: Siavash Mirtaheri (BlackVash)
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

The package ships a stdlib-only functional test suite (9 tests):

```bash
python -m unittest discover -s fastpath/tests -v
```

## Artifact
fastpath-plugin-1.0.0.zip
SHA256: ab7cdccb0db4df1c5890fe2182c72c50389c1fa0e11358e5c30fe508516c3475
