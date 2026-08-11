#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LOG="$(mktemp)"
trap 'rm -f "$LOG"' EXIT
if "$ROOT/scripts/publish_daily.sh" >"$LOG" 2>&1; then
  exit 0
fi
cat "$LOG"
exit 1
