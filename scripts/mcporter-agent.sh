#!/usr/bin/env bash
set -euo pipefail
exec mcporter --config /home/ubuntu/.openclaw/workspace/config/mcporter.json "$@"
