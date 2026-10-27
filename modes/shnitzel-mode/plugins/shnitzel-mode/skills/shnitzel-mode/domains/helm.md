# Helm

Templating and release tracking for Kubernetes manifests.

**Lock-in class.** Shallow. Charts render to plain manifests, and `helm template` is the exit.

## Read only

```bash
helm list -A -o json
helm history <release> -n <ns>
helm get values <release> -n <ns>
helm get manifest <release> -n <ns>
helm template <chart> -f values.yaml   # renders locally, touches nothing
```

## Signals

| Signal | Severity | Means |
| --- | --- | --- |
| Release status `failed` | 2 | The last upgrade did not complete |
| Status `pending-upgrade` or `pending-install` | 2 | A previous run was interrupted and the release is wedged |
| Chart version far behind upstream | 5 | Not urgent until it is a CVE |
| Values drifting from the repository copy | 3 | Someone upgraded with `--set` and nothing recorded it |

## Dry run

```bash
helm upgrade <release> <chart> --dry-run --debug
helm diff upgrade <release> <chart>    # helm-diff plugin, worth installing
```

## Rollback

```bash
helm history <release> -n <ns>
helm rollback <release> <revision> -n <ns>
```

## Never without approval

`helm upgrade`, `helm install`, `helm uninstall`, `helm rollback`, and `--force`, which deletes and recreates resources rather than patching them.

## Failure modes

A release stuck in `pending-upgrade` blocks every later upgrade until it is resolved, and the usual cause is a killed CI job.

`--set` on the command line produces a release nobody can reproduce from the repository. Values belong in a file in Git.

Hooks that fail leave partial state, and Helm's own rollback does not undo hook side effects.

CRDs are installed but never upgraded by Helm. A chart bump that expects a new CRD field fails in a way that points at the workload rather than the CRD.
