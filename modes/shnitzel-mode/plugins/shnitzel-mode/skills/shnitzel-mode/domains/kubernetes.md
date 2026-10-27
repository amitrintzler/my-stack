# Kubernetes

The runtime everything else here deploys onto.

**Lock-in class.** Shallow at the API, structural at the managed-service boundary. Manifests move between providers; the ingress controller, storage classes, load balancer annotations and IAM integration do not.

## Read only

```bash
kubectl get nodes -o wide
kubectl get pods -A --field-selector=status.phase!=Running
kubectl get events -A --sort-by=.lastTimestamp | tail -40
kubectl top nodes ; kubectl top pods -A --sort-by=memory
kubectl get deploy,sts,ds -A -o json | jq '[.items[] | select(.status.readyReplicas != .status.replicas)]'
kubectl get pdb -A
kubectl describe node <node> | sed -n '/Conditions/,/Events/p'
```

## Signals

| Signal | Severity | Means |
| --- | --- | --- |
| Node `NotReady` | 2 | Capacity lost, and pods may be rescheduling right now |
| `CrashLoopBackOff` | 2 | A workload is failing repeatedly, not starting slowly |
| `ImagePullBackOff` | 3 | Registry, credentials or a tag that does not exist |
| Pods `Pending` with no node | 3 | Insufficient capacity, or a taint or affinity nobody expected |
| `OOMKilled` in recent events | 3 | Memory limit is wrong or a leak is real |
| PDB blocking a drain | 3 | Maintenance cannot proceed, which surfaces during upgrades |
| Certificate expiring in under 14 days | 2 | The classic silent outage |

## Dry run

```bash
kubectl diff -f manifest.yaml
kubectl apply -f manifest.yaml --dry-run=server
```

Server-side dry run catches admission webhooks. Client-side does not, which is why it passes and the real apply fails.

## Rollback

```bash
kubectl rollout undo deployment/<name> -n <ns>
kubectl rollout status deployment/<name> -n <ns>
```

Rollback covers the workload. It does not cover a migration the workload already ran, which is the case that turns a rollback into an incident.

## Never without approval

`apply`, `delete`, `drain`, `cordon`, `scale`, `rollout restart`, editing a resource in place, or anything against a context that is not local. Check `kubectl config current-context` before every command and say which context you are on.

## Failure modes

Requests and limits set from a guess produce either eviction or a cluster that cannot schedule. Both look like a scheduler problem.

A rollout that reports success only means the new pods passed their readiness probe. A readiness probe that returns 200 on a dead dependency reports success for a broken deploy.

DNS and NetworkPolicy failures present identically to application errors. Check them before reading application code.
