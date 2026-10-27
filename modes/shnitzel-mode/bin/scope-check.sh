#!/usr/bin/env bash
# scope-check.sh
#
# Looks for knowledge crossing a boundary it should not: a lessons file whose
# declared scope disagrees with its path, a repo-scoped lesson naming another
# repo, a feature document citing a different feature, a draft reply sitting in
# a repo it was not written for.
#
#   ./scope-check.sh            JSON items, same shape as the other collectors
#   ./scope-check.sh --pretty
#
# Read-only. Reports, never edits.

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

command -v jq >/dev/null || { echo "jq not found" >&2; exit 3; }

PROJECT_ROOTS=""
# shellcheck disable=SC1090
[ -f "$CONFIG" ] && . "$CONFIG"
LESSONS="${HOME}/.agents/shnitzel/lessons"

TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
: > "$TMP/items.jsonl"

# md5sum is GNU, md5 is BSD, cksum is everywhere. Without this the fingerprint
# was empty on macOS, which suppressed a finding permanently after its first
# report even when the underlying leak changed.
hash8() {
  if command -v md5sum >/dev/null 2>&1; then md5sum
  elif command -v md5 >/dev/null 2>&1; then md5 -q
  else cksum
  fi | tr -d ' -' | cut -c1-8
}

emit() {
  jq -nc --arg id "$1" --arg kind "$2" --argjson sev "$3" --arg repo "$4" \
        --arg title "$5" --arg url "$6" --arg fp "$7" \
    '{id:$id,kind:$kind,severity:$sev,repo:$repo,title:$title,url:$url,fingerprint:$fp,detail:null}' \
    >> "$TMP/items.jsonl"
}

# 1. lessons files: declared scope must match the path
if [ -d "$LESSONS" ]; then
  while IFS= read -r f; do
    [ -n "$f" ] || continue
    declared="$(sed -n 's/^scope:[[:space:]]*//p' "$f" | head -1)"
    rel="${f#"$LESSONS"/}"
    case "$rel" in
      global.md) expected="global" ;;
      repos/*.md)
        base="$(basename "$f" .md)"
        expected="repo:${base%%__*}/${base#*__}" ;;
      *) expected="" ;;
    esac
    if [ -z "$declared" ]; then
      emit "scopemissing:$rel" scope_missing 3 "$rel" \
           "lessons file has no scope header, so a reader cannot tell where it applies" "$f" "nohdr"
    elif [ -n "$expected" ] && [ "$declared" != "$expected" ]; then
      emit "scopemismatch:$rel" scope_mismatch 3 "$rel" \
           "lessons file declares $declared but sits at a path meaning $expected" "$f" "$declared"
    fi

    # a repo-scoped lesson naming a different owner/repo
    if [ "${expected#repo:}" != "$expected" ]; then
      own="${expected#repo:}"
      others="$(grep -oE '\b[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+\b' "$f" 2>/dev/null \
                | grep -vE '^(https?|docs|bin|src|lib|etc|usr|tmp|var|home)/' \
                | grep -v "^$own$" | sort -u | head -5 || true)"
      if [ -n "$others" ]; then
        emit "scopeforeign:$rel" scope_foreign_repo 3 "$own" \
             "lesson scoped to $own names other repositories: $(echo "$others" | tr '\n' ' ')" "$f" "$(printf '%s' "$others" | hash8)"
      fi
    fi
  done < <(find "$LESSONS" -name '*.md' -type f 2>/dev/null)
fi

# 2. a feature document citing another feature's id
for root in $PROJECT_ROOTS; do
  if [ ! -d "$root" ]; then
    echo "configured project root unavailable: $root" >&2
    exit 5
  fi
  while IFS= read -r dir; do
    [ -n "$dir" ] || continue
    slug="$(basename "$dir")"
    id="${slug%%-*}"
    hits="$(grep -rhoE '\b[0-9]{3}-[a-z0-9-]+\b' "$dir" 2>/dev/null | sort -u | grep -v "^$slug$" || true)"
    if [ -n "$hits" ]; then
      emit "scopefeat:$slug" scope_cross_feature 3 "$slug" \
           "feature $id references other features: $(echo "$hits" | tr '\n' ' ')" "$dir" \
           "$(printf '%s' "$hits" | hash8)"
    fi
  done < <(find "$root" -maxdepth 5 -type d -path '*/docs/features/*' 2>/dev/null | grep -E '/[0-9]{3}-' || true)

  # 3. drafts referencing a repo other than the one they sit in
  while IFS= read -r d; do
    [ -n "$d" ] || continue
    repodir="$(dirname "$d")"
    name="$(basename "$repodir")"
    foreign="$(grep -rhoE 'github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+' "$d" 2>/dev/null \
               | sed 's|github.com/||' | sort -u | grep -v "/$name\$" || true)"
    if [ -n "$foreign" ]; then
      emit "scopedraft:$name" scope_foreign_draft 3 "$name" \
           "drafts in $name reference other repositories: $(echo "$foreign" | tr '\n' ' ')" "$d" \
           "$(printf '%s' "$foreign" | hash8)"
    fi
  done < <(find "$root" -maxdepth 3 -type d -name '.watch-drafts' 2>/dev/null)
done

jq -s 'sort_by(.severity)' "$TMP/items.jsonl" > "$TMP/out.json" 2>/dev/null || echo '[]' > "$TMP/out.json"

if [ "$PRETTY" -eq 1 ]; then
  jq -r 'if length == 0 then "no scope leaks found" else (.[] | "  [\(.severity)] \(.kind)  \(.repo)\n      \(.title)") end' "$TMP/out.json"
else
  cat "$TMP/out.json"
fi
