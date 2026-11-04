#!/usr/bin/env bash
# bootstrap.sh
#
# Find, or fetch, the Shnitzel distribution that matches this plugin's version.
# A marketplace install copies only the plugin folder. The installer, the
# collectors, the budget checker and the upstream lock live in the
# distribution, so setup resolves it here first.
#
#   scripts/bootstrap.sh          print the distribution, fetching it if missing
#   scripts/bootstrap.sh --print  print it only if it is already present
#
# Prints one JSON object: {"version", "dist", "source"}, where source is
# checkout, cached or fetched. It never builds the pstack engine and never runs
# the installer. Setup does both, with the user's consent.
#
# Exit codes: 0 found, 4 not present (--print), 5 fetch failed.
#
# Overrides:
#   SHNITZEL_DIST_HOME  where fetched copies live (default ~/.agents/shnitzel/dist)
#   SHNITZEL_REPO       repository to fetch from
#   SHNITZEL_REF        tag or branch to fetch (default shnitzel-mode--v<version>)

set -euo pipefail

PLUGIN="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MODE=fetch
[ "${1:-}" = "--print" ] && MODE=print

field() { python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["version"])' "$1"; }
emit()  { python3 -c 'import json,sys;print(json.dumps({"version":sys.argv[1],"dist":sys.argv[2],"source":sys.argv[3]}))' "$version" "$1" "$2"; }
is_dist() { [ -f "$1/install.sh" ] && [ -f "$1/bin/doctor.py" ] && [ -f "$1/config/upstream-lock.json" ]; }

version="$(field "$PLUGIN/.claude-plugin/plugin.json")"

# Inside a checkout of the repository the distribution sits two levels above
# the plugin folder, and no network is needed.
checkout="$(cd "$PLUGIN/../.." && pwd)"
if is_dist "$checkout"; then emit "$checkout" checkout; exit 0; fi

# Fetched copies keep the whole repository, because the upstream playbook
# check runs against the repository root.
home="${SHNITZEL_DIST_HOME:-$HOME/.agents/shnitzel/dist}"
dist="$home/$version/modes/shnitzel-mode"
if is_dist "$dist"; then emit "$dist" cached; exit 0; fi

if [ "$MODE" = print ]; then
  echo "no Shnitzel distribution for $version; run scripts/bootstrap.sh to fetch it" >&2
  exit 4
fi

repo="${SHNITZEL_REPO:-https://github.com/amitrintzler/my-stack}"
ref="${SHNITZEL_REF:-shnitzel-mode--v$version}"
command -v git > /dev/null || { echo "git is required to fetch the distribution" >&2; exit 5; }
mkdir -p "$home"
scratch="$(mktemp -d "$home/.fetch.XXXXXX")"
trap 'rm -rf "$scratch"' EXIT

if ! git -c advice.detachedHead=false clone --quiet --depth 1 --branch "$ref" "$repo" "$scratch/repo" >&2; then
  echo "could not fetch $ref from $repo" >&2
  exit 5
fi
fetched="$scratch/repo/modes/shnitzel-mode"
is_dist "$fetched" || { echo "$ref has no Shnitzel distribution at modes/shnitzel-mode" >&2; exit 5; }
got="$(field "$fetched/plugins/shnitzel-mode/.claude-plugin/plugin.json")"
[ "$got" = "$version" ] || { echo "$ref holds version $got but this plugin is $version" >&2; exit 5; }

rm -rf "$scratch/repo/.git"
if [ -e "$home/$version" ]; then
  echo "$home/$version exists but is not a Shnitzel distribution; move it aside and retry" >&2
  exit 5
fi
mv "$scratch/repo" "$home/$version"
emit "$dist" fetched
