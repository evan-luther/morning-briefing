#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
CHROME="$(python3 - <<'PY'
from pathlib import Path
hits=sorted(Path.home().glob('.cache/ms-playwright/chromium-*/chrome-linux64/chrome'))
if not hits:
    raise SystemExit('Playwright Chromium binary not found')
print(hits[-1])
PY
)"
export LD_LIBRARY_PATH="$ROOT/.browser-libs/usr/lib/x86_64-linux-gnu${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
"$CHROME" \
  --headless \
  --no-sandbox \
  --disable-dev-shm-usage \
  --hide-scrollbars \
  --window-size=1200,630 \
  --force-device-scale-factor=1 \
  --virtual-time-budget=2500 \
  --screenshot="$ROOT/briefing.png" \
  "file://$ROOT/index.html?og=1"
