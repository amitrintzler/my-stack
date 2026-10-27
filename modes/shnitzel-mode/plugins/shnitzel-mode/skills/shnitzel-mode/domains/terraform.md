# Terraform

Declarative infrastructure. The plan is the artifact under review, not the apply.

**Lock-in class.** Shallow for the language, structural for the state backend and the provider set. HCL is portable; a module tree built around one provider's resource model is not.

## Read only

```bash
terraform plan -detailed-exitcode      # 0 no changes, 1 error, 2 changes pending
terraform show -json plan.out | jq '.resource_changes[] | select(.change.actions != ["no-op"])'
terraform state list
terraform providers
terraform workspace list
```

`-detailed-exitcode` is the drift detector. Run it on a schedule against main and treat exit 2 as a finding.

## Signals

| Signal | Severity | Means |
| --- | --- | --- |
| Drift on production, exit code 2 | 3 | Reality and code disagree, usually a console change |
| Plan contains a destroy on a stateful resource | 2 | A rename or a changed identifier is about to delete data |
| State lock held for over an hour | 3 | A crashed run is blocking everyone |
| Provider or module pinned to a range rather than a version | 4 | Reproducibility is gone, and a plan can change with no commit |
| State file not remote, or unencrypted | 2 | Secrets sit in it in clear text |

## Dry run

`terraform plan -out=plan.out`, then review `terraform show plan.out`. Attach the plan output to the pull request. A plan that a reviewer cannot see is not a reviewed change.

## Rollback

There is no rollback command. The rollback is reverting the code and applying again, which only works when the change was reversible. For anything that destroys or recreates a stateful resource, the rollback is the backup, and it needs to exist before the apply.

## Never without approval

`terraform apply`, `destroy`, `taint`, `untaint`, `state rm`, `state mv`, `import`, or unlocking a lock. State surgery is the most dangerous category here, because a wrong `state rm` orphans real infrastructure with no record of it.

## Failure modes

`count` and `for_each` reindex on list changes and destroy resources that were only meant to move. Use `for_each` over a keyed map, not `count` over a list.

A plan that shows no change while reality differs usually means the resource is not in state at all.

Provider upgrades change defaults, so a plan can show diffs on resources nobody touched. Read the provider changelog before assuming drift.

Cross-workspace `remote_state` references turn one apply into an ordering problem across teams.
