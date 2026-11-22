# fastpath v1.0.0

Context-diet plugin for Hermes Agent. Compresses oversized tool results before they enter the model context (head 60% + tail 40% + omission marker), reducing tokens, latency and cost.

Author: Siavash Mirtaheri (BlackVash)
License: MIT
Requires Hermes >= 0.23

## Install
Copy the `fastpath` folder into `<HERMES_HOME>/plugins/` and add `fastpath` to `plugins.enabled` in config.yaml, then restart the gateway.

## Commands
/fastpath | /fastpath on|off | /fastpath limit N | /fastpath reset

## Artifact
fastpath-plugin-1.0.0.zip
SHA256: acbdfca8dad395e839f8714124bb3df39183ed4a651626e78cfd4f3b3872c355
