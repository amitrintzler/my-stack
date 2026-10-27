#!/usr/bin/env bash
# Runs every mode's own checks. A mode without a publish-check is reported
# rather than skipped silently, because a mode nobody validates is the one that
# ships someone's home directory path.

set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
fails=0
found=0

for mode in "$ROOT"/modes/*/; do
  [ -d "$mode" ] || continue
  found=$((found+1))
  name="$(basename "$mode")"
  printf '\n=== %s ===\n' "$name"
  if [ -x "$mode/bin/publish-check.sh" ]; then
    "$mode/bin/publish-check.sh" || fails=$((fails+1))
  else
    printf '  FAIL  no bin/publish-check.sh in this mode\n'
    fails=$((fails+1))
  fi
done

printf '\n%d mode(s) checked, %d failed\n' "$found" "$fails"
[ "$found" -gt 0 ] || { echo "no modes found under modes/"; exit 1; }
[ "$fails" -eq 0 ]
