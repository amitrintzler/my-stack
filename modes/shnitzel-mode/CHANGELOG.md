# 1.5.0

Engine moved to pstack-claude v0.9.117 (8ecae68), built on original pstack 0.15.35, the port's own pin. Clean three-way sync with no conflicts or resolutions, and the generator, generator check and playbook check pass. Original pstack 0.15.36 is not taken yet: it rewrites Orchestrate and deletes the orch scripts, which conflicts with the port's fork of `orchestrate.md`, `scripts/package.json` and the orch scripts. It comes in when the port absorbs it.

The `hld` and `feature-flow` skills now describe `interrogate` as it works since port 0.9.112: adversaries run through arena worktrees and only findings a run proves survive.

The default model sheet now carries `thermos reviewers` and `no-comments reviewer` (new roles in port 0.9.115 and 0.9.117) as `inherit-parent`. Without those lines both skills fell back to their stamped default and could spawn reviewers on a higher tier than the session. An existing sheet is left untouched; add the two lines by hand to get the same behaviour. `bin/upstream-check.sh` now refuses a candidate whose `models.json` names a role the default sheet does not cover, so the next new role is caught at sync time.

Direct and Focused tiers are unchanged: both allow zero delegates, so neither the two thermos reviewers nor the comment-sicko subagent start there. Deep's two reviewers match thermos.

`docs/acceptance.md` and `evals/acceptance.json` still record the 1.4 run on v0.9.101; they are evidence of that run, not of this engine.

# 1.4.0

Effort-aware admission, current original pstack over the released port, immutable candidate activation and rollback, owned installation, runtime-specific roles, atomic budget accounting and strict unsupported-cap rejection, collector coverage and completed-check readiness. See docs/acceptance.md for evidence and remaining runtime gaps.

# Changelog

## 1.3.0

Two defects found by a deliberate hunt through the collectors, both of the worst class for a monitoring tool, because both were silent.

**A failing pull request reported as ready to merge.** `statusCheckRollup` returns two different node types. A CheckRun carries `conclusion`; a StatusContext carries `state` and no conclusion at all. The filter read only `conclusion`, so in any repository whose CI posts commit statuses rather than checks, every failing run was invisible. Worse than a miss: with zero failures seen and an approving review, the same pull request then matched the approved-and-green rule and was reported as waiting only on your merge. The watch actively recommended merging a red build. Fixed to read whichever field is present, and `error` added to the failing set.

**A permanent false stall.** `stage_since` written as a full timestamp rather than a bare date produced an unparseable string, which fell through to a 9999 day age and reported a severity 4 stall forever. Dates are now normalised, and a genuinely unreadable date is reported as `feature_bad_date` rather than as very old, because absence of data and a real finding should never look the same.

## 1.2.0

Two documents rather than code. `docs/adoption.md` covers what compounds, what does not, what decays if neglected, the order to turn things on, the three habits that carry the whole thing, and the quarterly ritual for absorbing a new pstack release without letting the overlay drift into a fork.

`docs/architecture-review.md` is a critical review of this kit written to the harsh-review standard: prose is a request rather than a guarantee, MCP tools bypass every shell-level guard, no skill has an eval, fixtures are not reality, the severity model was tuned at a scale far below the real one, and scoping detects rather than prevents.

One bug found by that review and fixed. `bin/scope-check.sh` used `md5sum`, which does not exist on macOS, so every scope finding would have had an empty fingerprint and been suppressed permanently after its first report. Replaced with a portable hash that falls back through `md5` to `cksum`, and verified across all three branches.

## 1.1.0

Platform domains. Seventeen domain cards covering Argo CD, Kubernetes, OpenShift, Helm, Terraform, Vault, GitHub Actions, Jenkins, GitLab CI, Nexus, Artifactory, container registries, AWS, Azure, GCP, Oracle Cloud and observability. Each carries read-only commands, signals with severity, the dry run, the exact rollback, platform-specific stop rules and the real failure modes. The playbooks stay vendor-neutral and the cards carry the specifics.

Three skills where the workflow genuinely differs: `gitops`, `artifact-registry`, `cluster-upgrade`.

`bin/domain-scan.sh`, a fifth collector, probes whichever platforms are configured and feeds the same digest. Every probe is read-only and skips silently when its CLI is absent, so nothing is a hard dependency. Clouds are not polled by design.

## 1.0.0

First public release. Genericised for use by someone other than its author: identity moved out of the skill prose, absolute paths replaced with placeholders, and `bin/publish-check.sh` added so the next release cannot regress that. Licence, notice, contributing guide and a capabilities list added. CI runs the publish check, proves the collectors survive an empty config, and proves the installer dry run writes nothing.

## 0.4.0

Ten more use cases. Manager work: `team-pulse`, `one-on-one`, `exec-update`, `oncall-handover`. Platform work: `dep-sweep`, `migration`, `access-review`, `cost-review`, `slo-review`, `postmortem-actions`.

Scoping. Knowledge now has three tiers with one home each, promotion upward costs a named second instance, and `bin/scope-check.sh` reports four leak classes into the same digest. Acceptance criteria, metrics, dates, rejected alternatives, customer detail, drafts and velocity never move sideways between features.

## 0.3.0

Renamed from amit-mode. Feature lifecycle added: `feature-flow` owns idea, PRD, HLD, shipped and retro, and hands plan and build to pstack. Per-feature ledgers in the repository with a written gate at each stage, plus `bin/feature-scan.sh`. Learning layer added: repo profiles, scoped lessons, and the open-age measurement that `tune` runs on.

## 0.2.0

The watch harness. `bin/gh-collect.sh` gathers deterministically in shell with no model attached, dedupe by id plus fingerprint means only what changed is reported, and the whole thing is read-only by construction. Schedules for Cowork scheduled tasks, launchd and cron.

## 0.1.0

Core. Runtime primitive map for Claude Code, Cowork, Codex, Gemini CLI and local models. Model roles instead of vendor slugs. An always-stop list stricter than pstack's. Playbooks for platform change, pipeline fix, incident, lock-in and handoff.
