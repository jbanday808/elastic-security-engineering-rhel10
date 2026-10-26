#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
missing=0
for n in $(seq -w 0 26); do
  if ! find assets/architecture assets/screenshots -maxdepth 1 -type f -name "${n}_*.png" -print -quit | grep -q .; then
    echo "MISSING: Figure ${n} PNG"
    missing=$((missing + 1))
  fi
done
if [[ "$missing" -gt 0 ]]; then
  echo "Missing ${missing} numbered figure(s). See docs/SCREENSHOTS-TO-ADD.md"
  exit 1
fi
echo "All 27 numbered figure PNG files are present."
