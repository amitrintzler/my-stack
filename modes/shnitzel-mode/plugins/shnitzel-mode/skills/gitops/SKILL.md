---
name: gitops
description: Work with Argo CD or Flux where Git is the desired state. Reconcile drift, unstick a sync, and route changes through the repository rather than the cluster. Use for argocd, argo, flux, gitops, out of sync, app is degraded, sync failed, drift.
---

# GitOps

Under GitOps the cluster is an output. Editing it directly is not a fix, it is drift with a countdown, because the controller will either revert it or fight it forever.

Read [`shnitzel-mode/domains/argocd.md`](../shnitzel-mode/domains/argocd.md) for the commands and the failure modes.

## Diagnose in this order

**Is Git reachable and current.** A sync status of `Unknown` is usually a repository or credential problem, not an application problem, and it is the cheapest thing to rule out.

**Is the desired state what you think.** `argocd app diff` before anything else. Half of "the deploy did not work" is a chart value or an overlay resolving differently than expected.

**Is it drift or a failure.** OutOfSync means Git and cluster disagree. Degraded means what is running is unhealthy. They have different causes and different fixes, and treating one as the other wastes the first hour.

**If drift, find the source.** A manual `kubectl edit` during an incident, a mutating webhook, or a controller writing to a field it owns. The third one produces permanent OutOfSync that no sync will ever clear, and the fix is `ignoreDifferences`, not repeated syncing.

## Fix in Git

Every change goes through the repository. If the situation is urgent enough that the cluster must be touched directly, that is a decision the owner makes, and the same change must land in Git immediately afterwards or the next reconcile undoes it.

Disabling auto-sync during an incident is legitimate. Leaving it disabled afterwards is how the next incident happens, so record it as a follow-up rather than trusting memory.

## Stuck rollouts

Progressing for more than fifteen minutes is stuck, not slow. Check sync waves and hooks before the workload, since ordering is the usual cause. A failed PreSync hook blocks everything behind it with an error that names the hook rather than the effect.

## Never

`argocd app sync`, `--prune`, `--force`, `app delete`, and toggling auto-sync all require explicit authorization within the current task scope. Prune deserves its own mention: it deletes live resources absent from Git, so a bad Git state plus prune removes production.

## App of apps

One bad commit in the parent repository changes every child at once. Treat the parent as production and require the same review as a deploy.
