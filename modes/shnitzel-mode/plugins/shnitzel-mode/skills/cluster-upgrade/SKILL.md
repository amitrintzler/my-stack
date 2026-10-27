---
name: cluster-upgrade
description: Plan and execute a Kubernetes or OpenShift cluster upgrade, including the parts that cannot be rolled back. Use for cluster upgrade, k8s upgrade, OCP upgrade, EKS AKS GKE version bump, node pool upgrade, control plane upgrade.
---

# Cluster upgrade

The one platform change with a genuine no-return point. On OpenShift, version rollback is not supported once an upgrade has begun. On managed Kubernetes, the control plane moves forward only. Everything else here follows from that.

See [`domains/kubernetes.md`](../shnitzel-mode/domains/kubernetes.md) and [`domains/openshift.md`](../shnitzel-mode/domains/openshift.md).

## Before anything

**Read the deprecation and removal notes for every version you are crossing**, not only the target. Skipping a minor version still applies its API removals.

**Find the removed APIs actually in use.** `kubectl get --raw /metrics | grep apiserver_requested_deprecated_apis`, or `pluto detect-all-in-cluster`. Manifests in Git are not enough, since operators and Helm charts create resources you never wrote.

**Check operator and add-on compatibility**: the CNI, the CSI drivers, the ingress controller, cert-manager, the service mesh, and every operator. One incompatible add-on stalls the upgrade halfway, which is the worst state.

**Verify the backup and verify a restore.** Not that a backup exists, that a restore worked. Etcd snapshot for self-managed, and the provider's mechanism otherwise.

**Check PodDisruptionBudgets.** A PDB that cannot be satisfied blocks node drains forever, and this is the single most common cause of an upgrade that hangs with no error.

## Sequence

Control plane first, then node pools, then add-ons, in that order and never in parallel. Non-production first, and leave enough time between them to see the delayed failures, which usually means days rather than hours.

Upgrade one node pool, watch it, then continue. A surge upgrade of every node at once removes the ability to stop.

Have a stop point defined before starting: what observation makes you halt, and who decides.

## During

Watch cluster operator or component health rather than the upgrade percentage. On OpenShift, `oc get co` is the real status, and a single Degraded operator will stall the whole thing quietly.

Progress that has not moved in thirty minutes is stuck. Investigate rather than waiting, because the failure mode is almost always a drain blocked by a PDB or a node that cannot take its new config.

## Rollback

Say it plainly in the plan: for the control plane there is none. The mitigation for a failed upgrade is forward, or a rebuild from backup, and both need to be decided before you start rather than during.

Workload rollback still works and is unrelated to the cluster version.

## Never without approval

Starting the upgrade, changing the channel, draining a node, applying a MachineConfig, or upgrading a node pool. Each of these is its own approval, not one approval for the whole operation.
