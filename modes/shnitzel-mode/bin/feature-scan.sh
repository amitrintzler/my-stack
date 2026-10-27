#!/usr/bin/env bash
# feature-scan.sh
#
# Reads every feature ledger under the configured project roots and emits items
# in the same shape as gh-collect.sh, so one digest carries both the GitHub
# state and the feature state. Deterministic, read-only, no model.
#
#   ./feature-scan.sh              JSON items array
#   ./feature-scan.sh --pretty     human readable
#   ./feature-scan.sh --config PATH
#
# Ledgers are docs/features/<NNN>-<slug>/feature.yml, flat key: value only.

set -euo pipefail

CONFIG="${HOME}/.agents/watch.conf"
PRETTY=0
while [ $# -gt 0 ]; do
  case "$1" in
    --pretty) PRETTY=1 ;;
    --config) CONFIG="$2"; shift ;;
    -h|--help) sed -n '3,13p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "unknown argument: $1" >&2; exit 2 ;;
  esac
  shift
done

command -v jq >/dev/null || { echo "jq not found. brew install jq" >&2; exit 3; }

PROJECT_ROOTS=""
STAGE_DAYS_idea=3; STAGE_DAYS_prd=5; STAGE_DAYS_hld=7
STAGE_DAYS_plan=5; STAGE_DAYS_build=21; STAGE_DAYS_shipped=5
# shellcheck disable=SC1090
[ -f "$CONFIG" ] && . "$CONFIG"

[ -n "$PROJECT_ROOTS" ] || { echo '[]'; exit 0; }

TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
: > "$TMP/items.jsonl"

val() { sed -n "s/^$2:[[:space:]]*//p" "$1" | head -1 | sed 's/[[:space:]]*$//'; }

# A ledger date may be written as 2026-08-05 or as a full timestamp. Appending
# a time to a value that already had one produced an unparseable string, which
# fell through to 9999 and reported a permanent stall at severity 4. Normalise
# first, and report an unreadable date as unreadable rather than as very old.
days_since() {
  [ -n "$1" ] || { echo -1; return; }
  local d="${1%%[T ]*}"
  jq -nr --arg d "$d" 'try ((now - ($d + "T00:00:00Z" | fromdateiso8601)) / 86400 | floor) catch -1'
}

emit() {
  jq -nc --arg id "$1" --arg kind "$2" --argjson sev "$3" --arg repo "$4" \
        --arg title "$5" --arg url "$6" --arg fp "$7" --argjson detail "${8:-null}" \
    '{id:$id,kind:$kind,severity:$sev,repo:$repo,title:$title,url:$url,fingerprint:$fp,detail:$detail}' \
    >> "$TMP/items.jsonl"
}

for root in $PROJECT_ROOTS; do
  if [ ! -d "$root" ]; then
    echo "configured project root unavailable: $root" >&2
    exit 5
  fi
  while IFS= read -r ledger; do
    [ -n "$ledger" ] || continue
    dir="$(dirname "$ledger")"
    slug="$(basename "$dir")"
    proj="$(basename "$(dirname "$(dirname "$(dirname "$dir")")")")"

    stage="$(val "$ledger" stage)";      stage="${stage:-unknown}"
    since="$(val "$ledger" stage_since)"
    title="$(val "$ledger" title)";      title="${title:-$slug}"
    owner="$(val "$ledger" owner)"
    metric="$(val "$ledger" metric)"
    status="$(val "$ledger" status)"
    age="$(days_since "$since")"

    limit_var="STAGE_DAYS_${stage}"
    limit="${!limit_var:-14}"

    if [ "$age" -lt 0 ]; then
      emit "featdate:$proj:$slug" feature_bad_date 4 "$proj" \
           "$slug has an unreadable stage_since, so its age cannot be judged" "$dir" "baddate" 'null'
    elif [ "$age" -gt "$limit" ]; then
      sev=4; [ "$status" = "red" ] && sev=2
      [ "$stage" = "shipped" ] && sev=4
      emit "featstall:$proj:$slug" feature_stalled "$sev" "$proj" \
           "$slug stuck in $stage for $age days, limit $limit" "$dir" "$stage:$age" \
           "$(jq -nc --arg o "$owner" --arg s "$status" '{owner:$o,status:$s}')"
    fi

    # a stage past prd with no gate entry recorded is an unrecorded decision
    prog="$dir/04-progress.md"
    if [ "$stage" != "idea" ] && [ "$stage" != "prd" ]; then
      if [ ! -f "$prog" ] || ! grep -q '^## .*gate:' "$prog" 2>/dev/null; then
        emit "featgate:$proj:$slug" feature_gate_missing 3 "$proj" \
             "$slug reached $stage with no gate recorded in 04-progress.md" "$dir" "$stage" 'null'
      fi
    fi

    case "$metric" in
      ""|*"has to move"*)
        [ "$stage" != "idea" ] && emit "featmetric:$proj:$slug" feature_no_metric 4 "$proj" \
          "$slug has no success metric, so it cannot have a retro" "$dir" "$stage" 'null' ;;
    esac

    hld="$dir/02-hld.md"
    if [ -f "$hld" ]; then
      body="$(sed -n '/^## Review/,/^## /p' "$hld" | sed '1d;$d' | tr -d '[:space:]')"
      [ -z "$body" ] && emit "featreview:$proj:$slug" feature_no_review 3 "$proj" \
        "$slug has an HLD whose review section is empty, so the design was never argued with" "$dir" "$stage" 'null'
    fi

    if [ "$stage" = "shipped" ] && [ "$age" -ge 0 ] && [ "$age" -gt "$STAGE_DAYS_shipped" ]; then
      emit "featretro:$proj:$slug" feature_retro_due 5 "$proj" \
           "$slug shipped $age days ago with no retro against its metric" "$dir" "$stage:$age" 'null'
    fi

    if [ "$stage" = "plan" ] && [ "$age" -ge 0 ] && [ "$age" -gt 7 ] && [ -z "$(val "$ledger" prs)" ]; then
      emit "featnopr:$proj:$slug" feature_no_pr 4 "$proj" \
           "$slug has a plan and no pull request after $age days" "$dir" "$stage:$age" 'null'
    fi
  done < <(find "$root" -maxdepth 6 -path '*/docs/features/*/feature.yml' -type f 2>/dev/null)
done

jq -s 'sort_by(.severity)' "$TMP/items.jsonl" > "$TMP/out.json" 2>/dev/null || echo '[]' > "$TMP/out.json"

if [ "$PRETTY" -eq 1 ]; then
  jq -r 'if length == 0 then "no feature findings" else (.[] | "  [\(.severity)] \(.kind)  \(.repo)\n      \(.title)") end' "$TMP/out.json"
else
  cat "$TMP/out.json"
fi
