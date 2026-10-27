---
name: prd
description: Write or sharpen a product requirements document for a feature, ending in acceptance criteria someone else can test. Use for PRD, product spec, requirements, what are we actually building, write the spec.
---

# PRD

Ten minutes here saves three weeks later. The output is not a document, it is a set of acceptance criteria precise enough that an agent or a QA engineer can verify them without asking you what you meant.

## Method

Start from the rough idea and interrogate it. Ask in one batch, not one at a time, and only about things you cannot determine yourself.

The questions that earn their place: who hurts today and how do we know, what do they do instead right now, which number moves and by how much, what does this displace on the roadmap, and what would make us cancel it in week three.

Everything else you work out from the codebase, the tickets, or the metrics. A question whose answer you could observe is not the human's to answer.

## Acceptance criteria

The hard part, and the part worth being pedantic about.

Bad: "the failover is fast". Untestable, so it will be argued about at the end.
Good: "with the primary region unreachable, a read request returns from the secondary within 90 seconds, verified by the `failover-drill` job in CI".

Each criterion names an observable, a threshold, and where it is checked. Where a criterion cannot be made testable, say so explicitly and record it as a known risk instead of quietly leaving it vague.

## Non-goals

Write them before you feel you need them. This is the section that ends the "while we are in there" conversation in week three, and it only works if it existed before the conversation started.

## Success metric

One number, its value today, the target, and when it will be measured. A feature with no metric can ship but cannot be learned from, and it will be cited as a success or a failure by whoever remembers it most loudly.

## Output

`docs/features/<NNN>-<slug>/01-prd.md` from the template in the **feature-flow** skill. Set `stage: prd` and `stage_since` in `feature.yml`. Commit on the feature branch.

Then stop. The gate to HLD is a human other than you agreeing the criteria are testable. Ask for that review, name who you asked, and record their answer in `04-progress.md`.
