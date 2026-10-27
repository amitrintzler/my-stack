# GitHub Actions

CI on GitHub, where the workflow file is also a privileged execution surface.

**Lock-in class.** Structural in practice. The YAML dialect, the marketplace actions and the OIDC trust relationships all have to be rebuilt elsewhere, even though the underlying shell commands port fine.

## Read only

```bash
gh run list --limit 20 --json conclusion,status,workflowName,headBranch,url,createdAt
gh run view <id> --log-failed
gh api /repos/{owner}/{repo}/actions/cache/usage
gh api /repos/{owner}/{repo}/actions/permissions
gh api /repos/{owner}/{repo}/actions/secrets --jq '.secrets[].name'   # names only
gh api /repos/{owner}/{repo}/branches/main/protection
```

## Signals

| Signal | Severity | Means |
| --- | --- | --- |
| Default branch red | 1 | Everyone is blocked behind it |
| Same job failing across repos | 2 | A shared action or runner image changed |
| Actions pinned to a tag rather than a SHA | 3 | Supply chain risk, since a tag can be moved |
| `permissions: write-all` or a missing permissions block | 3 | The workflow can push and publish |
| Self-hosted runner offline or unlabeled | 3 | Jobs queue with no error |
| Cache usage near the limit | 4 | Builds silently get slower |
| A workflow triggered by `pull_request_target` checking out PR code | 2 | The classic path to a compromised repository |

## Dry run

There is no server-side dry run. `act` runs locally with caveats. The honest dry run is a branch and a real run, which is why workflow changes belong in their own pull request.

## Rollback

Revert the workflow file and push to the branch. There is no separate deploy step to undo, but a workflow that already published an artifact or a release has done that irreversibly.

## Never without approval

Merging to a protected branch, `gh workflow run`, re-running a job, `gh run cancel`, editing repository or environment secrets, changing protection rules, and approving a deployment gate.

## Failure modes

`GITHUB_TOKEN` permission changes at the org level break workflows that never changed.

Marketplace actions pinned to `@v3` move under you. Pin to a full SHA for anything with write access.

Matrix jobs that fail only on one OS often mean a path or a shell difference rather than a real bug.

Concurrency groups cancel runs in ways that look like flakiness, and the cancelled run is reported as a failure.
