#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
npm run build
scripts/render_preview.sh
git add index.html briefing.json briefing.png sky.js
git diff --cached --quiet && { echo "No briefing changes to publish"; exit 0; }
git commit -m "chore: refresh morning briefing $(TZ=America/New_York date +%F)"
git push origin main
echo "Published https://evan-luther.github.io/morning-briefing/"
