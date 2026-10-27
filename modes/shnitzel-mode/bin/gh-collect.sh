#!/usr/bin/env bash
# gh-collect.sh
#
# Read-only GitHub digest for the shnitzel-mode watch harness. Runs every query
# deterministically in shell, emits one compact JSON document, and never writes
# to GitHub. The model reads the digest, it does not run the queries. That is
# the whole point: collection is cheap, reproducible, and free of token spend.
#
#   ./gh-collect.sh                     digest of what changed since the last run
#   ./gh-collect.sh --all               ignore the dedupe state, report everything
#   ./gh-collect.sh --config PATH       default ~/.agents/watch.conf
#   ./gh-collect.sh --no-state          do not update the state file
#   ./gh-collect.sh --pretty            human readable instead of JSON
#
# Requires gh (authenticated) and jq. Exits 3 if either is missing, 4 if the
# config names no repositories.

set -euo pipefail

CONFIG="${HOME}/.agents/watch.conf"
ALL=0
NO_STATE=0
PRETTY=0

while [ $# -gt 0 ]; do
  case "$1" in
    --all) ALL=1 ;;
    --no-state) NO_STATE=1 ;;
    --pretty) PRETTY=1 ;;
    --config) CONFIG="$2"; shift ;;
    -h|--help) sed -n '3,18p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "unknown argument: $1" >&2; exit 2 ;;
  esac
  shift
done

command -v gh >/dev/null || { echo "gh not found. brew install gh && gh auth login" >&2; exit 3; }
command -v jq >/dev/null || { echo "jq not found. brew install jq" >&2; exit 3; }

REPOS=""; OWNERS=""; DEFAULT_BRANCH="main"; STALE_DAYS=5; REVIEW_SLA_DAYS=2
CHECK_SECURITY=1; STATE_FILE="${HOME}/.agents/watch-state.json"
# shellcheck disable=SC1090
[ -f "$CONFIG" ] && . "$CONFIG"

[ -n "$REPOS$OWNERS" ] || { echo "no REPOS or OWNERS in $CONFIG" >&2; exit 4; }

NOW="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
: > "$TMP/items.jsonl"
: > "$TMP/unavailable.jsonl"

# emit <id> <kind> <severity> <repo> <title> <url> <fingerprint> <detail-json>
emit() {
  jq -nc --arg id "$1" --arg kind "$2" --argjson sev "$3" --arg repo "$4" \
        --arg title "$5" --arg url "$6" --arg fp "$7" --argjson detail "${8:-null}" \
    '{id:$id,kind:$kind,severity:$sev,repo:$repo,title:$title,url:$url,fingerprint:$fp,detail:$detail}' \
    >> "$TMP/items.jsonl"
}

# gh calls are best effort. A repo you cannot see must not kill the whole run.
try() {
  local output
  if output="$("$@" 2>/dev/null)" && printf '%s' "$output" | jq -e '(type == "array" or type == "object") and (if type=="object" then (.errors // [] | length)==0 else true end)' >/dev/null 2>&1; then
    printf '%s' "$output"
  else
    jq -nc --arg repo "${repo:-global}" --arg query "${2:-query}" '{repo:$repo,query:$query,status:"unavailable"}' >> "$TMP/unavailable.jsonl"
    printf ''
  fi
}

branch_for() {
  local key
  key="DEFAULT_BRANCH_$(printf '%s' "$1" | tr '/.-' '___')"
  printf '%s' "${!key:-$DEFAULT_BRANCH}"
}

# --- per repository -----------------------------------------------------------
for repo in $REPOS; do
  branch="$(branch_for "$repo")"

  # 1. default branch red. the highest severity thing that exists.
  runs="$(try gh run list --repo "$repo" --branch "$branch" --limit 100 \
      --json conclusion,status,workflowName,url,headSha,createdAt)"
  if [ -n "$runs" ]; then
    echo "$runs" | jq -c 'sort_by(.createdAt) | reverse | unique_by(.workflowName) | .[] | select(.status=="completed" and (.conclusion=="failure" or .conclusion=="timed_out"))'  2>/dev/null \
    | while IFS= read -r r; do
        [ -n "$r" ] || continue
        sha="$(echo "$r" | jq -r '.headSha')"
        wf="$(echo "$r" | jq -r '.workflowName')"
        emit "mainred:$repo:$wf:$sha" main_red 1 "$repo" \
             "$branch is red: $wf" "$(echo "$r" | jq -r '.url')" "$sha" "$r"
      done
  fi

  # 2. my open pull requests in this repo
  prs="$(try gh pr list --repo "$repo" --author "@me" --state open --limit 50 \
      --json number,title,url,updatedAt,isDraft,mergeStateStatus,reviewDecision,headRefName,headRefOid,statusCheckRollup)"
  [ -n "$prs" ] || continue

  echo "$prs" | jq -c '.[]' 2>/dev/null | while IFS= read -r pr; do
    [ -n "$pr" ] || continue
    num="$(echo "$pr" | jq -r '.number')"
    url="$(echo "$pr" | jq -r '.url')"
    ttl="$(echo "$pr" | jq -r '.title')"
    sha="$(echo "$pr" | jq -r '.headRefOid')"
    draft="$(echo "$pr" | jq -r '.isDraft')"

    # statusCheckRollup mixes two node types. A CheckRun carries .conclusion,
    # a StatusContext carries .state and no conclusion at all. Reading only
    # .conclusion made every failing legacy commit status invisible, so a repo
    # whose CI posts statuses rather than checks reported all clear while its
    # pull requests were red. Read whichever field is present.
    failed="$(echo "$pr" | jq -c '[.statusCheckRollup[]?
      | select((((.conclusion // .state) // "") | ascii_downcase)
               | IN("failure","timed_out","cancelled","action_required","error"))]')"
    nfail="$(echo "$failed" | jq 'length')"
    if [ "$nfail" -gt 0 ]; then
      emit "prci:$repo:$num:$sha" my_pr_ci_red 2 "$repo" \
           "PR #$num checks failing: $ttl" "$url" "$sha" "$failed"
    fi

    case "$(echo "$pr" | jq -r '.mergeStateStatus')" in
      DIRTY)   emit "prconf:$repo:$num:$sha" my_pr_conflict 3 "$repo" \
                    "PR #$num has conflicts: $ttl" "$url" "$sha" 'null' ;;
      BLOCKED) : ;;
    esac

    checks_green="$(echo "$pr" | jq -r '(.statusCheckRollup // []) as $checks
      | ($checks|length)>0 and all($checks[];
         if .conclusion != null then .status=="COMPLETED" and (.conclusion|ascii_downcase|IN("success","neutral","skipped"))
         else (.state // "" | ascii_downcase)=="success" end)')"
    if [ "$checks_green" != "true" ] && [ "$nfail" -eq 0 ]; then
      emit "prpending:$repo:$num:$sha" my_pr_checks_pending 5 "$repo" \
           "PR #$num checks pending or unavailable: $ttl" "$url" "$sha" 'null'
    fi
    if [ "$checks_green" = "true" ] && [ "$(echo "$pr" | jq -r '.mergeStateStatus')" = "CLEAN" ] && [ "$draft" = "false" ] && [ "$(echo "$pr" | jq -r '.reviewDecision')" = "APPROVED" ] && [ "$nfail" -eq 0 ]; then
      emit "prmerge:$repo:$num:$sha" my_pr_ready 4 "$repo" \
           "PR #$num approved and green, waiting on you: $ttl" "$url" "$sha" 'null'
    fi

    stale="$(echo "$pr" | jq --argjson d "$STALE_DAYS" -r 'if ((now - (.updatedAt|fromdateiso8601))/86400) > $d then "yes" else "no" end')"
    if [ "$stale" = "yes" ]; then
      emit "prstale:$repo:$num" my_pr_stale 6 "$repo" \
           "PR #$num idle over $STALE_DAYS days: $ttl" "$url" "$(echo "$pr" | jq -r '.updatedAt')" 'null'
    fi

    # 3. review threads on my PR that nobody has resolved. graphql is the only
    #    endpoint that reports resolution state.
    owner="${repo%%/*}"; name="${repo##*/}"
    threads="$(try gh api graphql -f owner="$owner" -f name="$name" -F number="$num" -f query='
      query($owner:String!,$name:String!,$number:Int!){
        repository(owner:$owner,name:$name){
          pullRequest(number:$number){
            reviewThreads(first:100){nodes{
              id isResolved isOutdated
              comments(first:1){nodes{author{login} body url createdAt}}
            }}}}}')"
    if [ -n "$threads" ]; then
      open_threads="$(echo "$threads" | jq -c '[.data.repository.pullRequest.reviewThreads.nodes[]?
          | select(.isResolved==false and .isOutdated==false)
          | {author:(.comments.nodes[0].author.login//"unknown"),
             url:(.comments.nodes[0].url//""),
             at:(.comments.nodes[0].createdAt//""),
             body:((.comments.nodes[0].body//"")[0:280])}]' 2>/dev/null || echo '[]')"
      n="$(echo "$open_threads" | jq 'length')"
      if [ "${n:-0}" -gt 0 ]; then
        emit "prthreads:$repo:$num" my_pr_unanswered 2 "$repo" \
             "PR #$num has $n unresolved review threads: $ttl" "$url" "n=$n:$sha" "$open_threads"
      fi
    fi
  done

  # 4. open security alerts. 403 where the feature is off, which try() absorbs.
  if [ "${CHECK_SECURITY}" = "1" ]; then
    alerts="$(try gh api "/repos/$repo/dependabot/alerts?state=open&per_page=100")"
    if [ -n "$alerts" ]; then
      echo "$alerts" | jq -c '[.[]? | select((.security_advisory.severity//"")|IN("critical","high"))]' 2>/dev/null \
      | while IFS= read -r a; do
          [ -n "$a" ] || continue
          n="$(echo "$a" | jq 'length')"
          [ "${n:-0}" -gt 0 ] || continue
          emit "sec:$repo" security_alert 3 "$repo" \
               "$n open high or critical Dependabot alerts" \
               "https://github.com/$repo/security/dependabot" "n=$n" \
               "$(echo "$a" | jq -c '[.[] | {pkg:.dependency.package.name, sev:.security_advisory.severity, ghsa:.security_advisory.ghsa_id}]')"
        done
    fi
  fi
done

# --- global, not per repository ------------------------------------------------
owner_flags=()
for o in $OWNERS; do owner_flags+=(--owner "$o"); done

reqs="$(try gh search prs --review-requested=@me --state open --limit 50 ${owner_flags[@]+"${owner_flags[@]}"} \
    --json repository,number,title,url,updatedAt,isDraft)"
if [ -n "$reqs" ]; then
  echo "$reqs" | jq -c --argjson sla "$REVIEW_SLA_DAYS" \
    '.[] | select(.isDraft==false) | . + {age:((now - (.updatedAt|fromdateiso8601))/86400|floor), late:(((now - (.updatedAt|fromdateiso8601))/86400) > $sla)}' 2>/dev/null \
  | while IFS= read -r p; do
      [ -n "$p" ] || continue
      rp="$(echo "$p" | jq -r '.repository.nameWithOwner // .repository.name')"
      num="$(echo "$p" | jq -r '.number')"
      age="$(echo "$p" | jq -r '.age')"
      sev=5; [ "$(echo "$p" | jq -r '.late')" = "true" ] && sev=3
      emit "review:$rp:$num" review_requested "$sev" "$rp" \
           "review requested $age days ago: $(echo "$p" | jq -r '.title')" \
           "$(echo "$p" | jq -r '.url')" "$(echo "$p" | jq -r '.updatedAt')" 'null'
    done
fi

# --- dedupe against the previous run -------------------------------------------
if [ -f "$STATE_FILE" ]; then
  cp "$STATE_FILE" "$TMP/previous-state.json"
else
  echo '{"seen":{}}' > "$TMP/previous-state.json"
fi
STATE_READ="$TMP/previous-state.json"

jq -s '.' "$TMP/items.jsonl" > "$TMP/all.json" 2>/dev/null || echo '[]' > "$TMP/all.json"

if [ "$ALL" -eq 1 ]; then
  cp "$TMP/all.json" "$TMP/new.json"
else
  jq -s --slurpfile st "$STATE_READ" \
    '[ .[0][] | select( ($st[0].seen[.id] // "") != .fingerprint ) ]' \
    "$TMP/all.json" > "$TMP/new.json"
fi

jq -s 'unique_by(.repo + ":" + .query)' "$TMP/unavailable.jsonl" > "$TMP/unavailable.json"

jq -n --arg now "$NOW" --slurpfile unavailable "$TMP/unavailable.json" \
      --slurpfile all "$TMP/all.json" \
      --slurpfile new "$TMP/new.json" \
  '{generated_at:$now,
    coverage:{status:(if ($unavailable[0]|length)>0 then "incomplete" else "observed" end),unavailable:$unavailable[0]},
    total:($all[0]|length),
    new:($new[0]|length),
    suppressed:(($all[0]|length)-($new[0]|length)),
    counts:($new[0]|group_by(.kind)|map({key:.[0].kind,value:length})|from_entries),
    items:($new[0]|sort_by(.severity))}' > "$TMP/digest.json"

if [ "$NO_STATE" -eq 0 ]; then
  mkdir -p "$(dirname "$STATE_FILE")"
  jq -s '{seen:(.[0].seen + (.[1] | map({key:.id,value:.fingerprint}) | from_entries))}' \
    "$STATE_READ" "$TMP/all.json" > "$TMP/state.new" && mv "$TMP/state.new" "$STATE_FILE"
fi

if [ "$PRETTY" -eq 1 ]; then
  jq -r '"shnitzel-mode watch  " + .generated_at,
         "  new \(.new) of \(.total) open, \(.suppressed) already seen","",
         (.items[] | "  [\(.severity)] \(.kind)  \(.repo)\n      \(.title)\n      \(.url)")' "$TMP/digest.json"
else
  cat "$TMP/digest.json"
fi
