#!/usr/bin/env bash
# domain-scan.sh
#
# Read-only health probes for the platforms listed in DOMAINS. Every probe
# observes and changes nothing, every probe is skipped when its CLI is absent
# or unconfigured, and no probe can fail the run. Emits the same item shape as
# the other collectors.
#
#   ./domain-scan.sh            JSON items
#   ./domain-scan.sh --pretty
#   ./domain-scan.sh --list     which probes would run, and why the others would not
#
# Clouds are deliberately not polled here. Cost, IAM and quota questions are
# answered on a cadence by cost-review and access-review, not every hour.

set -uo pipefail

CONFIG="${HOME}/.agents/watch.conf"
PRETTY=0; LIST=0; COVERAGE=0
while [ $# -gt 0 ]; do
  case "$1" in
    --pretty) PRETTY=1 ;;
    --coverage) COVERAGE=1 ;;
    --list) LIST=1 ;;
    --config) CONFIG="$2"; shift ;;
    -h|--help) sed -n '3,14p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "unknown argument: $1" >&2; exit 2 ;;
  esac
  shift
done

command -v jq >/dev/null || { echo "jq not found" >&2; exit 3; }

DOMAINS=""
PROM_URL=""; JENKINS_URL=""; NEXUS_URL=""; ARTIFACTORY_URL=""
KUBE_CONTEXT=""
# shellcheck disable=SC1090
[ -f "$CONFIG" ] && . "$CONFIG"

TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
: > "$TMP/items.jsonl"
: > "$TMP/coverage.jsonl"

emit() {
  jq -nc --arg id "$1" --arg kind "$2" --argjson sev "$3" --arg repo "$4" \
        --arg title "$5" --arg url "$6" --arg fp "$7" \
    '{id:$id,kind:$kind,severity:$sev,repo:$repo,title:$title,url:$url,fingerprint:$fp,detail:null}' \
    >> "$TMP/items.jsonl"
}

# run with a timeout where one is available, and without where it is not
t() {
  local output status
  if command -v timeout >/dev/null; then
    output="$(timeout 20 "$@")"; status=$?
  else
    output="$("$@")"; status=$?
  fi
  if [ "$status" -eq 2 ] && [ "${1:-}" = "vault" ] && [ "${2:-}" = "status" ] && printf '%s' "$output" | jq -e '.sealed==true' >/dev/null 2>&1; then
    printf '%s' "$output"
    return 0
  fi
  if [ "$status" -ne 0 ]; then
    note_skip "${CURRENT_DOMAIN:-unknown}" "query failed"
    return "$status"
  fi
  printf '%s' "$output"
}
has() { command -v "$1" >/dev/null 2>&1; }
enabled() { case " $DOMAINS " in *" $1 "*) return 0 ;; *) return 1 ;; esac; }

skips=""
note_skip() {
  skips="$skips
  skip  $1: $2"
  local status="unavailable"
  case "$2" in
    *"not set"|"not in DOMAINS") status="not_configured" ;;
    *"not installed") [ -n "${CONFIGURED_DOMAINS:-}" ] || status="not_configured" ;;
  esac
  jq -nc --arg domain "$1" --arg reason "$2" --arg status "$status" '{domain:$domain,reason:$reason,status:$status}' >> "$TMP/coverage.jsonl"
}

valid_json() {
  printf '%s' "$1" | jq -e "$2" >/dev/null 2>&1 || {
    note_skip "${CURRENT_DOMAIN:-unknown}" "unexpected response schema"
    return 1
  }
}

# --- argo cd -----------------------------------------------------------------
probe_argocd() {
  has argocd || { note_skip argocd "argocd cli not installed"; return; }
  local out; out="$(t argocd app list -o json 2>/dev/null)" || { note_skip argocd "argocd not logged in"; return; }
  [ -n "$out" ] || return
  valid_json "$out" 'type=="array"' || return
  echo "$out" | jq -c '.[]? | {n:.metadata.name, h:.status.health.status, s:.status.sync.status}' 2>/dev/null \
  | while IFS= read -r a; do
      n="$(echo "$a" | jq -r .n)"; h="$(echo "$a" | jq -r .h)"; s="$(echo "$a" | jq -r .s)"
      case "$h" in
        Degraded) emit "argo:h:$n" argocd_degraded 2 "argocd/$n" "app $n is Degraded" "" "$h" ;;
        Missing)  emit "argo:h:$n" argocd_missing 2 "argocd/$n" "app $n is Missing, resources that should exist do not" "" "$h" ;;
      esac
      case "$s" in
        OutOfSync) emit "argo:s:$n" argocd_outofsync 3 "argocd/$n" "app $n is OutOfSync, git and cluster disagree" "" "$s" ;;
        Unknown)   emit "argo:s:$n" argocd_unknown 3 "argocd/$n" "app $n sync state Unknown, repo or cluster unreachable" "" "$s" ;;
      esac
    done
}

# --- kubernetes --------------------------------------------------------------
probe_kubernetes() {
  has kubectl || { note_skip kubernetes "kubectl not installed"; return; }
  local ctx; ctx="$(t kubectl config current-context 2>/dev/null)" || { note_skip kubernetes "no current context"; return; }
  [ -n "$KUBE_CONTEXT" ] && [ "$KUBE_CONTEXT" != "$ctx" ] && { note_skip kubernetes "current context $ctx is not the configured $KUBE_CONTEXT"; return; }

  local nodes; nodes="$(t kubectl get nodes -o json 2>/dev/null)"
  if [ -n "$nodes" ]; then
    valid_json "$nodes" '.items | type=="array"' || return
    echo "$nodes" | jq -r '.items[]? | select([.status.conditions[]? | select(.type=="Ready" and .status=="True")] | length == 0) | .metadata.name' 2>/dev/null \
    | while IFS= read -r n; do [ -n "$n" ] && emit "k8s:node:$ctx:$n" k8s_node_notready 2 "$ctx" "node $n is NotReady" "" "notready"; done
  fi

  local pods; pods="$(t kubectl get pods -A -o json 2>/dev/null)"
  if [ -n "$pods" ]; then
    valid_json "$pods" '.items | type=="array"' || return
    local n
    n="$(echo "$pods" | jq '[.items[]? | select(.status.containerStatuses[]?.state.waiting.reason == "CrashLoopBackOff")] | length' 2>/dev/null)"
    [ "${n:-0}" -gt 0 ] && emit "k8s:crash:$ctx" k8s_crashloop 2 "$ctx" "$n pods in CrashLoopBackOff" "" "n=$n"
    n="$(echo "$pods" | jq '[.items[]? | select(.status.containerStatuses[]?.state.waiting.reason | test("ImagePull|ErrImage") // false)] | length' 2>/dev/null)"
    [ "${n:-0}" -gt 0 ] && emit "k8s:pull:$ctx" k8s_imagepull 3 "$ctx" "$n pods cannot pull their image" "" "n=$n"
    n="$(echo "$pods" | jq '[.items[]? | select(.status.phase=="Pending" and (.spec.nodeName // "") == "")] | length' 2>/dev/null)"
    [ "${n:-0}" -gt 0 ] && emit "k8s:pending:$ctx" k8s_unschedulable 3 "$ctx" "$n pods pending with no node assigned" "" "n=$n"
  fi
}

# --- openshift ---------------------------------------------------------------
probe_openshift() {
  has oc || { note_skip openshift "oc not installed"; return; }
  local co; co="$(t oc get co -o json 2>/dev/null)" || { note_skip openshift "not logged in"; return; }
  [ -n "$co" ] || { note_skip openshift "no cluster operators returned"; return; }
  echo "$co" | jq -r '.items[]? | select([.status.conditions[]? | select(.type=="Degraded" and .status=="True")] | length > 0) | .metadata.name' 2>/dev/null \
  | while IFS= read -r n; do [ -n "$n" ] && emit "ocp:co:$n" ocp_operator_degraded 1 "openshift" "cluster operator $n is Degraded, the platform itself" "" "degraded"; done
  local mcp; mcp="$(t oc get mcp -o json 2>/dev/null)"
  if [ -n "$mcp" ]; then
    echo "$mcp" | jq -r '.items[]? | select([.status.conditions[]? | select(.type=="Degraded" and .status=="True")] | length > 0) | .metadata.name' 2>/dev/null \
    | while IFS= read -r n; do [ -n "$n" ] && emit "ocp:mcp:$n" ocp_mcp_degraded 2 "openshift" "machine config pool $n is Degraded, nodes cannot take config" "" "degraded"; done
  fi
}

# --- helm --------------------------------------------------------------------
probe_helm() {
  has helm || { note_skip helm "helm not installed"; return; }
  local out; out="$(t helm list -A -o json 2>/dev/null)" || { note_skip helm "no cluster access"; return; }
  [ -n "$out" ] || return
  valid_json "$out" 'type=="array"' || return
  echo "$out" | jq -c '.[]? | select(.status != "deployed") | {n:.name,ns:.namespace,s:.status}' 2>/dev/null \
  | while IFS= read -r r; do
      [ -n "$r" ] || continue
      n="$(echo "$r" | jq -r .n)"; ns="$(echo "$r" | jq -r .ns)"; s="$(echo "$r" | jq -r .s)"
      emit "helm:$ns:$n" helm_release_bad 2 "$ns/$n" "helm release $n is $s, later upgrades are blocked" "" "$s"
    done
}

# --- vault -------------------------------------------------------------------
probe_vault() {
  has vault || { note_skip vault "vault cli not installed"; return; }
  local out; out="$(t vault status -format=json 2>/dev/null)"
  [ -n "$out" ] || { note_skip vault "vault unreachable"; return; }
  valid_json "$out" '.sealed | type=="boolean"' || return
  [ "$(echo "$out" | jq -r '.sealed')" = "true" ] && emit "vault:sealed" vault_sealed 1 "vault" "vault is sealed, everything needing a secret is down" "" "sealed"
  return 0
}

# --- prometheus --------------------------------------------------------------
probe_observability() {
  [ -n "$PROM_URL" ] || { note_skip observability "PROM_URL not set"; return; }
  local out; out="$(t curl -sf "$PROM_URL/api/v1/targets" 2>/dev/null)" || { note_skip observability "prometheus unreachable"; return; }
  valid_json "$out" '.data.activeTargets | type=="array"' || return
  local n; n="$(echo "$out" | jq '[.data.activeTargets[]? | select(.health != "up")] | length' 2>/dev/null)"
  [ "${n:-0}" -gt 0 ] && emit "prom:targets" prom_target_down 2 "prometheus" "$n scrape targets down, you are blind to those services" "$PROM_URL/targets" "n=$n"
  local s; s="$(t curl -sf "$PROM_URL/api/v1/alerts" 2>/dev/null | jq '[.data.alerts[]? | select(.state=="firing")] | length' 2>/dev/null)"
  [ "${s:-0}" -gt 10 ] && emit "prom:firing" prom_alert_storm 3 "prometheus" "$s alerts firing at once, likely one cause" "$PROM_URL/alerts" "n=$s"
  return 0
}

# --- jenkins -----------------------------------------------------------------
probe_jenkins() {
  [ -n "$JENKINS_URL" ] || { note_skip jenkins "JENKINS_URL not set"; return; }
  local out; out="$(t curl -sfn "$JENKINS_URL/computer/api/json?tree=computer[displayName,offline]" 2>/dev/null)" \
    || { note_skip jenkins "jenkins unreachable or no .netrc credentials"; return; }
  local n; n="$(echo "$out" | jq '[.computer[]? | select(.offline==true)] | length' 2>/dev/null)"
  [ "${n:-0}" -gt 0 ] && emit "jenkins:agents" jenkins_agents_offline 2 "jenkins" "$n agents offline, jobs queue with no failure" "$JENKINS_URL/computer/" "n=$n"
  local q; q="$(t curl -sfn "$JENKINS_URL/queue/api/json" 2>/dev/null | jq '.items | length' 2>/dev/null)"
  [ "${q:-0}" -gt 20 ] && emit "jenkins:queue" jenkins_queue_deep 3 "jenkins" "$q jobs queued, check labels before capacity" "$JENKINS_URL/queue/" "n=$q"
  return 0
}

# --- nexus and artifactory ---------------------------------------------------
probe_nexus() {
  [ -n "$NEXUS_URL" ] || { note_skip nexus "NEXUS_URL not set"; return; }
  t curl -sfn "$NEXUS_URL/service/rest/v1/status" >/dev/null 2>&1 \
    || { emit "nexus:down" nexus_unreachable 1 "nexus" "nexus status endpoint not responding, dependency resolution is down" "$NEXUS_URL" "down"; return; }
  local bs; bs="$(t curl -sfn "$NEXUS_URL/service/rest/v1/blobstores" 2>/dev/null)"
  if [ -n "$bs" ]; then
    echo "$bs" | jq -c '.[]? | select((.availableSpaceInBytes // 0) > 0 and (.totalSizeInBytes // 0) > 0) | {n:.name, pct: ((.totalSizeInBytes / (.totalSizeInBytes + .availableSpaceInBytes)) * 100 | floor)}' 2>/dev/null \
    | while IFS= read -r b; do
        [ -n "$b" ] || continue
        p="$(echo "$b" | jq -r .pct)"; n="$(echo "$b" | jq -r .n)"
        [ "${p:-0}" -ge 80 ] && emit "nexus:blob:$n" nexus_blobstore_full 2 "nexus" "blob store $n at ${p} percent, writes fail before reads" "$NEXUS_URL" "p=$p"
      done
  fi
  return 0
}

probe_artifactory() {
  [ -n "$ARTIFACTORY_URL" ] || { note_skip artifactory "ARTIFACTORY_URL not set"; return; }
  t curl -sfn "$ARTIFACTORY_URL/api/system/ping" >/dev/null 2>&1 \
    || { emit "rt:down" artifactory_unreachable 1 "artifactory" "artifactory ping failing, dependency resolution is down" "$ARTIFACTORY_URL" "down"; return; }
  return 0
}

ALL="argocd kubernetes openshift helm vault observability jenkins nexus artifactory"
CONFIGURED_DOMAINS="$DOMAINS"
[ -n "$DOMAINS" ] || DOMAINS="$ALL"

for d in $ALL; do
  CURRENT_DOMAIN="$d"
  if enabled "$d"; then "probe_$d" 2>/dev/null; else note_skip "$d" "not in DOMAINS"; fi
done

jq -s 'sort_by(.severity)' "$TMP/items.jsonl" > "$TMP/out.json" 2>/dev/null || echo '[]' > "$TMP/out.json"

if [ "$LIST" -eq 1 ]; then
  printf 'domains configured: %s\n' "$DOMAINS"
  printf '%s\n' "$skips"
  exit 0
fi

if [ "$COVERAGE" -eq 1 ]; then
  jq -s '{probes:.,status:(if any(.[]; .status=="unavailable") then "incomplete" else "observed" end)}' "$TMP/coverage.jsonl" > "$TMP/coverage.json"
  jq -n --slurpfile items "$TMP/out.json" --slurpfile coverage "$TMP/coverage.json" '{items:$items[0],coverage:$coverage[0]}'
  exit 0
fi

if [ "$PRETTY" -eq 1 ]; then
  jq -r 'if length == 0 then "no domain findings" else (.[] | "  [\(.severity)] \(.kind)  \(.repo)\n      \(.title)") end' "$TMP/out.json"
  [ -n "$skips" ] && printf '%s\n' "$skips"
else
  cat "$TMP/out.json"
fi
