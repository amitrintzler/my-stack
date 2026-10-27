# Argo CD

Declarative GitOps for Kubernetes. Git is the desired state, Argo reconciles the cluster toward it. The important consequence: changing the cluster directly is not a fix, it is drift that Argo will either revert or fight.

**Lock-in class.** Shallow. The manifests are portable, the Application CRs are not, and a move to Flux is days rather than a rewrite.

## Read only

```bash
argocd app list -o json
argocd app get <app> -o json
argocd app diff <app>                  # desired versus live, changes nothing
argocd app history <app>
kubectl get applications -A -o json    # same data without the CLI logged in
```

## Signals

| Signal | Severity | Means |
| --- | --- | --- |
| `health.status` is `Degraded` | 2 | Running workload is unhealthy now |
| `health.status` is `Missing` | 2 | Something that should exist does not |
| `sync.status` is `OutOfSync` on a production app | 3 | Git and cluster disagree, deliberately or not |
| `OutOfSync` for more than a day | 3 | Nobody is reconciling, which usually means manual edits |
| `sync.status` `Unknown` | 3 | Argo cannot reach the repo or the cluster |
| Auto-sync disabled on an app that should have it | 4 | Someone turned it off during an incident and never restored it |
| `Progressing` for over 15 minutes | 3 | A rollout is stuck, not slow |

## Dry run

```bash
argocd app diff <app>
argocd app sync <app> --dry-run
```

## Rollback

```bash
argocd app history <app>
argocd app rollback <app> <history-id>
```

Rollback in Argo means the previous Git revision. If the bad state came from a manual `kubectl edit`, rolling back Argo will not fix it and a hard refresh plus sync will.

## Never without approval

`argocd app sync`, `--prune`, `--force`, `argocd app delete`, disabling or enabling auto-sync, editing an Application in the cluster rather than in Git.

Prune is the dangerous one. It deletes live resources no longer in Git, and a bad Git state plus prune removes production.

## Failure modes

A resource edited directly in the cluster shows OutOfSync forever, and each sync reverts a change someone believed was applied.

Sync waves and hooks silently reorder things. When a rollout stalls, check the wave annotations before the workload.

An app-of-apps pattern means one bad parent commit changes every child at once. Treat the parent repo as production.

Argo reports Healthy for resources it does not know how to health check. Custom resources without a health script are Healthy by default, which is not the same as working.
