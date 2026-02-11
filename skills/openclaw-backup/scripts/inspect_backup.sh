#!/usr/bin/env bash
set -euo pipefail

if [ $# -lt 1 ]; then
  echo "Usage: $0 <backup.tar.gz>" >&2
  exit 2
fi

tar -tzf "$1" | sed -n '1,120p'
