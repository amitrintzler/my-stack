#!/usr/bin/env bash
# publish-check.sh
#
# Run before publishing or opening a pull request. Fails on the things that are
# embarrassing in public and easy to miss locally.
#
#   ./bin/publish-check.sh          report and exit non-zero on any failure
#   ./bin/publish-check.sh --quiet  only print failures
#
# Checks: absolute home paths, personal identifiers, credential-shaped strings,
# hardcoded vendor model slugs in skills, the banned long dash, skill frontmatter
# matching its directory, and a command stub per skill.

set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
QUIET=0
[ "${1:-}" = "--quiet" ] && QUIET=1

fails=0
say()  { [ "$QUIET" -eq 1 ] || printf '%s\n' "$*"; }
ok()   { say "  ok    $*"; }
bad()  { printf '  FAIL  %s\n' "$*"; fails=$((fails+1)); }

files() { git -C "$ROOT" ls-files --cached --others --exclude-standard 2>/dev/null || find "$ROOT" -type f -not -path '*/.git/*'; }
# This script necessarily contains the patterns it searches for, so it excludes
# itself. Nothing else is exempt.
scan()  { files | grep -v 'publish-check.sh' | while IFS= read -r f; do [ -f "$ROOT/$f" ] && printf '%s\n' "$ROOT/$f" || printf '%s\n' "$f"; done; }
DASH="$(printf '\xe2\x80\x94')"

say "publish-check"

# 1. absolute home paths
hits="$(grep -rIn -E '/(Users|home)/[a-z][a-z0-9_.-]+/' $(scan) 2>/dev/null | grep -v 'ABSOLUTE/PATH' || true)"
if [ -n "$hits" ]; then bad "absolute home paths"; say "$hits" | head -5; else ok "no absolute home paths"; fi

# 2. credential shaped strings
hits="$(grep -rIn -E '(ghp_|github_pat_|gho_|AKIA|xox[baprs]-|BEGIN [A-Z ]*PRIVATE KEY|-----BEGIN)' $(scan) 2>/dev/null || true)"
if [ -n "$hits" ]; then bad "credential shaped strings"; say "$hits" | head -5; else ok "no credential shaped strings"; fi

# 3. email addresses outside the licence
hits="$(grep -rIn -E '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}' $(scan) 2>/dev/null | grep -v LICENSE || true)"
if [ -n "$hits" ]; then bad "email addresses"; say "$hits" | head -5; else ok "no email addresses"; fi

# 4. hardcoded model slugs in skills. roles only. A leading dot is a manifest
# directory such as .claude-plugin, not a model.
hits="$(grep -rIn -E '(^|[^.[:alnum:]_])(claude|gpt|gemini|llama|mistral|grok)-[0-9a-z.-]+' "$ROOT/plugins" 2>/dev/null | grep -v 'references/model-roles.md' || true)"
if [ -n "$hits" ]; then bad "hardcoded model slugs in skills, use a role"; say "$hits" | head -5; else ok "no hardcoded model slugs"; fi

# 5. the banned long dash
hits="$(grep -rIn -- "$DASH" $(scan) 2>/dev/null || true)"
if [ -n "$hits" ]; then bad "long dash characters"; say "$hits" | head -5; else ok "no long dash characters"; fi

# 6. skill frontmatter matches its directory
bad_fm=""
for d in "$ROOT"/plugins/*/skills/*/; do
  [ -f "$d/SKILL.md" ] || { bad_fm="$bad_fm $d(no SKILL.md)"; continue; }
  name="$(sed -n 's/^name:[[:space:]]*//p' "$d/SKILL.md" | head -1)"
  [ "$name" = "$(basename "$d")" ] || bad_fm="$bad_fm $(basename "$d")(name=$name)"
done
if [ -n "$bad_fm" ]; then bad "skill frontmatter mismatch:$bad_fm"; else ok "skill frontmatter matches directories"; fi

# 7. a command stub per skill
missing=""
for d in "$ROOT"/plugins/*/skills/*/; do
  s="$(basename "$d")"
  [ -f "$ROOT/plugins/$(basename "$(dirname "$(dirname "$d")")")/commands/$s.md" ] || missing="$missing $s"
done
if [ -n "$missing" ]; then bad "skills with no command stub:$missing"; else ok "every skill has a command stub"; fi

# 8. every script parses
for f in "$ROOT"/bin/*.sh "$ROOT"/install.sh; do
  bash -n "$f" 2>/dev/null || bad "syntax error in $(basename "$f")"
done
ok "shell syntax"

# 9. json parses
for f in $(find "$ROOT" -name '*.json' -not -path '*/.git/*'); do
  python3 -c "import json,sys;json.load(open(sys.argv[1]))" "$f" 2>/dev/null || bad "invalid json: ${f#"$ROOT"/}"
done
ok "json parses"

say ""
if [ "$fails" -eq 0 ]; then
  say "clean, ready to publish"
  exit 0
fi
printf '%d check(s) failed\n' "$fails"
exit 1
