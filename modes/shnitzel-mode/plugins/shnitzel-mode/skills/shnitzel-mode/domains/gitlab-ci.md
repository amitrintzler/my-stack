# GitLab CI

CI integrated with the forge, configured in `.gitlab-ci.yml`, executed by runners you usually own.

**Lock-in class.** Structural. The YAML, the runner model, the registry integration and the environment or deployment model all have to be rebuilt elsewhere.

## Read only

```bash
glab ci list
glab ci view <pipeline-id>
glab api projects/:id/pipelines?status=failed
glab api projects/:id/runners
glab api projects/:id/protected_branches
```

## Signals

| Signal | Severity | Means |
| --- | --- | --- |
| Default branch pipeline failed | 1 | Blocking everyone |
| Runners offline or stale | 2 | Jobs queue silently |
| Shared runner minutes near quota | 3 | Pipelines stop at a boundary nobody watches |
| `rules` or `only` changes altering when a job runs | 3 | A deploy job that stopped triggering looks like a green pipeline |
| Job artifacts with no expiry | 4 | Storage grows without bound |

## Dry run

`glab ci lint` validates syntax, not behaviour. Merge request pipelines are the real dry run, which is why a pipeline change deserves its own merge request.

## Rollback

Revert the `.gitlab-ci.yml`. Environments keep a deployment history, and a rollback there is a redeploy of a previous commit rather than an undo.

## Never without approval

Running or cancelling a pipeline, retrying a deploy job, editing CI variables, changing protected branch or environment rules, and approving a manual deployment gate.

## Failure modes

`rules:if` precedence is subtle, and a job that silently stops running is the common outcome. A green pipeline that skipped the deploy job looks identical to a successful deploy.

Variables defined at group, project and job level shadow each other, and the effective value is not shown anywhere obvious.

Runner tags that no runner carries produce a pipeline that waits forever rather than failing.
