---
name: feature-flow
description: Drive a feature from idea through PRD, high level design, phased plan, implementation and retro, with a gate and a written decision at every stage. Use for new feature, PRD, spec, HLD, design doc, feature planning, track this feature, where is feature X.
---

# Feature flow

pstack starts at the engineering plan. It assumes the feature is already decided and you are the senior engineer executing it. An engineering manager running twenty plus engineers sees the expensive mistakes happen earlier than that: building the wrong thing, an acceptance criterion nobody can test, a design nobody argued with, and a shipped feature nobody checked against the metric that justified it.

This skill owns the stages pstack does not, and hands the middle back to pstack where pstack is better.

Use this lifecycle for substantial features or when explicitly requested. Bounded changes use Shnitzel focused execution without generating these documents. An accepted user plan satisfies approach selection.

## The ledger is the feature

Everything lives in the repo, never in a session. One directory per feature.

```
docs/features/<NNN>-<slug>/
  feature.yml        the state machine and the facts
  01-prd.md          why, for whom, what done means
  02-hld.md          the design, the alternatives rejected, the data shape
  03-plan/           phased implementation plan
  04-progress.md     append-only decision trail, one entry per gate and per phase
  reviews/           feedback captured at each gate
```

`feature.yml` is deliberately flat `key: value`, so `bin/feature-scan.sh` reads it with grep and needs no parser. Do not nest it. Templates are in `templates/`.

Committed to the branch, so it survives a session ending, a context compaction, a runtime switch, and you handing the feature to someone else. That is the whole point.

## Stages and gates

Each stage ends at a gate. A gate is one written entry in `04-progress.md` with the date, the decision, and who made it. Passing a gate silently is the failure mode this exists to prevent.

| Stage | Produces | Gate to leave it |
| --- | --- | --- |
| `idea` | a paragraph | Worth building at all. Name what it displaces. |
| `prd` | `01-prd.md` | Acceptance criteria are testable by someone who did not write them, and non-goals are named. The **prd** skill. |
| `hld` | `02-hld.md` | The design was argued with, not just written. Data shape named, boundaries drawn, at least one alternative rejected in writing, lock-in priced. The **hld** skill. |
| `plan` | `03-plan/` | Phases are independently shippable and each ends in a check. pstack's plan reference if installed, otherwise the **hld** skill's plan section. |
| `build` | PRs | Each phase verified on the real surface before the next starts. pstack's feature playbook, or **platform-change** for infrastructure. |
| `shipped` | a release | The metric from the PRD was actually measured. |
| `retro` | an entry | What the estimate missed, and what changes in the next one. |

Stages can go backwards. A design that falls apart during build returns to `hld` and the ledger records why. A feature that moves forward only is a feature nobody is learning from.

## Feedback, continuously rather than at the end

Four loops run at different speeds. Naming them separately matters, because "get feedback" without a cadence means feedback at the end, which is too late.

**Per gate.** Record the authorized decision maker. Require another human only where the project or user requires that gate. For the PRD that is whoever asked for the feature. For the HLD it is a senior engineer plus a multi-model panel if pstack is installed (`interrogate`, `arena`). Record who, and what they changed.

**Per phase.** A PR, verified on the real surface, reviewed. The **watch** harness already reports failing checks and unanswered review threads on it. That is your build-time feedback and it needs no new machinery.

**Per week.** `bin/feature-scan.sh` reports stage drift and stalls into the same digest the watch harness uses. A feature that has sat in `hld` for eleven days shows up next to a red pipeline, because both are things you would want to know.

**Per feature, once.** The retro. Compare the shipped metric against the PRD's claim. This is the only loop that improves estimates, and it is the one always skipped.

## Where pstack fits

Install pstack and this skill hands off rather than reimplements.

- `hld` routes into **pstack:architect** for parallel design exploration and **pstack:interrogate** for the adversarial multi-model review.
- `plan` uses **pstack:poteto-mode**'s plan reference, which is a genuinely good phased-plan spec. Do not rewrite it.
- `build` uses **pstack:poteto-mode**'s feature playbook, including its throughput checkpoint.
- Long autonomous stretches use **pstack:show-me-your-work** for the decision trail, written into `04-progress.md`.

Without pstack, run the same stages with a single reviewer and say in the reply that the design panel was single-model.

## Starting one

Create the directory, copy the templates, set `stage: idea`, commit on a `feature/<slug>` branch. Then run the stage's skill. Start at the earliest stage that has not already been satisfied by an accepted artifact. Reuse accepted plans and requirements rather than recreating them.
