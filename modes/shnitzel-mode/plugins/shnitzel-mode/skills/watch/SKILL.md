---
name: watch
description: The recurring watch harness. Reads the deterministic GitHub digest and turns it into a ranked action list. Use for watch, what needs me, check CI, check my PRs, morning brief, anything scheduled or repeating.
---

# Watch

Everything you ask for repeatedly is one shape. Something changed on GitHub, and the question is whether it needs you now, needs you today, or needs nobody.

The harness answers that in three parts. A shell collector gathers state, this skill ranks it, and delivery depends on whether anyone is watching.

## The collector does the gathering, not you

Run `bin/digest.sh` and read its JSON. It runs both collectors, the GitHub one and the feature ledger one, and merges them into a single ranked list. Do not run `gh` queries or walk feature directories yourself. The collectors exist so that gathering costs no tokens, returns the same shape every time, and can run on a schedule with no model attached.

```bash
bin/digest.sh            # only what changed since the last run
bin/digest.sh --all      # everything currently open, and updates the age metrics
bin/digest.sh --pretty   # human readable, for a terminal
```

Only `--all` maintains `open-ages.json` and `metrics.jsonl`, because age is only meaningful over a complete snapshot. That is the data the **tune** skill runs on, so at least one `--all` run a day matters.

Config is `~/.agents/watch.conf`. Dedupe state is `~/.agents/watch-state.json`, keyed by item id and a fingerprint. A pull request whose head commit moved reappears. One that sat still does not. If the collector exits non-zero, say so plainly and stop. A watch that silently reports nothing because `gh` lost its auth is worse than no watch.

## Severity, and what each one means

The collector assigns severity. You act on it.

| Sev | Kind | Meaning |
| --- | --- | --- |
| 1 | `main_red` | The default branch is broken. Everyone else is blocked behind it. This interrupts. |
| 2 | `my_pr_ci_red` | Your own PR is failing. Route to **pipeline-fix**. |
| 2 | `my_pr_unanswered` | A human asked you something and is waiting. Route to **review-reply**. |
| 3 | `my_pr_conflict` | Conflicts. Cheap to fix now, expensive after another week of drift. |
| 3 | `security_alert` | Open high or critical advisory. |
| 3 | `review_requested` | Past the review SLA. Someone is blocked on you. |
| 4 | `my_pr_ready` | Approved and green. Only the merge is left, and merging is the owner's action. |
| 5 | `review_requested` | Inside the SLA. Today, not now. |
| 6 | `my_pr_stale` | Idle beyond the threshold. Decide: revive, split, or close. |

Feature ledger findings arrive in the same list, from `bin/feature-scan.sh`.

| Sev | Kind | Meaning |
| --- | --- | --- |
| 2 or 4 | `feature_stalled` | Too long in one stage. Severity 2 when the feature is already marked red. |
| 3 | `feature_gate_missing` | A stage was advanced with no decision written down. |
| 3 | `feature_no_review` | An HLD whose review section is empty, so the design was never argued with. |
| 4 | `feature_no_metric` | No success metric, so the feature can never have a retro. |
| 4 | `feature_no_pr` | A plan exists and nothing has been opened against it. |
| 5 | `feature_retro_due` | Shipped, and nobody checked whether the metric moved. |

Route feature findings to the **feature-track** skill rather than reporting them raw.

`bin/domain-scan.sh` adds the platform families. Severity 1 is reserved for the platform itself being broken: `ocp_operator_degraded`, `vault_sealed`, `nexus_unreachable`, `artifactory_unreachable`. Severity 2 covers a workload or a capability being down: `argocd_degraded`, `argocd_missing`, `k8s_node_notready`, `k8s_crashloop`, `ocp_mcp_degraded`, `helm_release_bad`, `prom_target_down`, `jenkins_agents_offline`, `nexus_blobstore_full`. Severity 3 covers drift and degradation: `argocd_outofsync`, `argocd_unknown`, `k8s_imagepull`, `k8s_unschedulable`, `prom_alert_storm`, `jenkins_queue_deep`.

Route these to the domain skill rather than acting directly. Argo findings go to **gitops**, cluster findings to **platform-change** or **cluster-upgrade**, registry findings to **artifact-registry**, and a scrape target down to **slo-review**, because a target down means the alerts on that service will not fire either.

`bin/scope-check.sh` adds one more family, all at severity 3: `scope_missing`, `scope_mismatch`, `scope_foreign_repo`, `scope_cross_feature` and `scope_foreign_draft`. These mean knowledge is crossing a boundary it should not, so report them with the exact file and the exact foreign reference, and never fix them silently. Rescoping a lesson changes where it will be applied in future, which is a decision, not a tidy-up.

Severity 1 and 2 lead the report. Everything at 5 and below is one line each, grouped, never expanded.

## What the harness does on its own

Read-only work proceeds with no approval. Reading runs, reading logs, reading diffs and threads, classifying a failure, reproducing it locally, drafting a fix on a branch, drafting a reply.

Nothing leaves the machine. No comment is posted, no PR is opened, no branch is pushed, no merge, no re-run of a workflow, no rebase of a shared branch. Drafts are written to `.watch-drafts/` in the working tree and the report names them. The owner sends them.

This is the unattended read-only boundary; a scheduled run never widens it. Interactive authorization elsewhere does not turn a scheduled watch into a writer. An unattended run that posts a comment is the one failure mode that makes the whole harness untrustworthy.

## Delivery

**On demand.** `/watch` in any session. Full ranked report, then ask what to pick up.

**Scheduled and unattended.** No question at the end, because nobody is there to answer it. Report, draft, and stop. Say explicitly what you did not do and why. Definitions are in `schedules/`.

**Nothing new.** Say so in one line. Do not pad an empty run into a report. `new 0 of 14 open` is the whole message.

## Cadence

| When | What | Why this cadence |
| --- | --- | --- |
| Every 30 min during work hours | severity 1 and 2 only | Main red and a failing PR are the only things worth interrupting for. |
| Hourly | full collector, report only if severity <= 3 | Catches conflicts and SLA breaches without noise. |
| Daily 08:00 Asia/Jerusalem | `--all`, full brief | The one report read start to finish. Include what you deliberately dropped. |
| Weekly Monday 08:00 | stale PRs, security, branch hygiene | The slow decay nothing else catches. |
| After you push | tail the run until it settles | This is the only genuinely continuous one. Bounded, not a loop forever. |

Timezone is the user's, not UTC. Scheduled tasks are configured in UTC, so convert once and write the local time in a comment.

## Escalation

A severity 1 that is still present on the next run is not a repeat, it is an escalation. Say how long main has been red and name the last green commit. A severity 2 unanswered thread older than a working day gets the same treatment.

Do not escalate by repeating. Escalate by adding the fact that time has passed and what it now costs.

## Report shape

Two sentences of state first. What is on fire, what is waiting on you. Then severity 1 and 2 items with the recommended first action for each, one item per short paragraph. Then everything else as single lines. Then the drafts you wrote and where they are. House style from `shnitzel-mode/references/house-style.md` applies, and the closing three items apply.
