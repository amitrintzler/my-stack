# OpenShift

Kubernetes plus an opinionated platform layer: operators for everything, an integrated registry, Routes instead of raw Ingress, and SCCs that reject manifests which run fine elsewhere.

**Lock-in class.** Structural. Routes, DeploymentConfigs, ImageStreams, BuildConfigs and SCC assumptions do not port to vanilla Kubernetes without work. Plain Deployments and Ingress do.

## Read only

```bash
oc get clusterversion
oc get co                              # cluster operators, the real health surface
oc get nodes ; oc get mcp              # machine config pools, upgrade progress
oc adm upgrade                         # available channels and versions
oc get co -o json | jq '[.items[] | select(.status.conditions[]? | select(.type=="Degraded" and .status=="True"))] | map(.metadata.name)'
oc get csv -A                          # operator versions and install state
oc get routes -A
```

## Signals

| Signal | Severity | Means |
| --- | --- | --- |
| Any ClusterOperator `Degraded` | 1 | The platform itself is broken, not a workload |
| ClusterVersion `Progressing` for hours | 2 | An upgrade is stuck mid flight, the worst state |
| MachineConfigPool `Degraded` | 2 | Nodes cannot take config, so the upgrade will not finish |
| Operator CSV in `Failed` | 3 | Something the platform depends on is not reconciling |
| Cluster within 60 days of end of life | 3 | Upgrades take planning, and this window closes quietly |
| Certificate rotation pending | 2 | OpenShift rotates a lot of internal certs, and a stuck rotation is an outage on a timer |

## Dry run

```bash
oc apply -f manifest.yaml --dry-run=server
oc adm upgrade --to=<version> --dry-run 2>/dev/null || oc adm release info <version>
```

## Rollback

Version rollback is not supported on OpenShift once an upgrade has begun. That is the single most important fact on this card. Plan forward-only, and make the pre-upgrade backup real rather than assumed.

Workload rollback is standard: `oc rollout undo deployment/<name>`.

## Never without approval

`oc adm upgrade`, `oc adm drain`, changing a channel, applying a MachineConfig, deleting an operator, touching anything in `openshift-*` namespaces.

## Failure modes

SCCs reject pods that run anywhere else, usually anything wanting a fixed UID or a hostPath. This is the most common cause of "it works on our other cluster".

An upgrade blocked by a single Degraded operator can sit for hours with no obvious error. Read `oc get co` first, always.

ImageStreams add a layer of indirection that hides which image is actually running. Resolve the digest before debugging a deploy.

The internal registry filling up degrades builds cluster-wide, and it presents as unrelated build failures.
