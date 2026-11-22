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

## Artifact
fastpath-plugin-1.0.0.zip
SHA256: 4b0341efcb89793e8e62e8cb6632602690d986d0a556d2d1d03b8bb3a88172d6
