---
name: hld
description: Produce a high level design for a feature, argued with rather than merely written, then break it into phases. Use for HLD, high level design, design doc, architecture for this feature, how should we build it.
---

# HLD

The design stage exists to be attacked. A design nobody argued with is a first draft wearing a document's clothes.

## Order

**Data shape first.** Before any component diagram, name the core types and how state is organised. A state machine instead of scattered booleans, a typed model instead of a repeated shape assumption, a table or registry instead of a growing conditional. Get this wrong and every phase inherits it.

**Then boundaries.** Where untrusted input is validated, where the framework stops and the domain starts, what stays pure. Guards at the edge, trust inside.

**Then components.** What is added, changed, and deleted. Deletion counts as design work and usually improves the result.

**Then failure.** Partial failure, retry, bad deploy, region loss, whichever apply. Name the rollback before the design is finished, not before the deploy. A design whose rollback is "revert the PR" has not considered data.

## Argue with it

Explore in parallel rather than iterating one idea. With pstack installed, run **pstack:architect** for parallel design exploration, and **pstack:interrogate** for adversarial multi-model review, using a panel that spans at least two vendors. A panel that agrees with itself has told you nothing.

Without pstack, write two designs yourself, then attack the one you prefer with the sharpest model available, and say in the reply that the review was single-model.

Run **lock-in-check** when the design introduces material vendor coupling. Skip it when no such decision is being made.

Record in the review section who argued, when, and what changed. If nothing changed, either the design was already right or the review was not real. Say which.

## Phases

Break the accepted design into phases. With pstack installed use its plan reference, which is a good spec and should not be rewritten. Otherwise the rules that matter are:

Make each phase a coherent, independently verifiable outcome. Size follows risk and coupling, not a fixed file or function count. Infrastructure and shared types land first. Every phase ends in a check that can be run, and each is independently shippable.

## Output

`docs/features/<NNN>-<slug>/02-hld.md` and `03-plan/`. Move `feature.yml` to `stage: plan`, record the gate in `04-progress.md`, commit.
