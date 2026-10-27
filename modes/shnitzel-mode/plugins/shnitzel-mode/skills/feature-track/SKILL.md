---
name: feature-track
description: Report where every in-flight feature actually is, what is stalled, and which gate is overdue. Use for feature status, where are we on X, feature review, what is stuck, weekly feature check.
---

# Feature track

Reads the ledgers, not your memory of the standup.

## Input

`bin/feature-scan.sh` walks the configured project roots, reads every `docs/features/*/feature.yml`, and emits items in the same shape as the GitHub collector so both land in one digest. Run it, read the output, do not walk the directories yourself.

## What counts as stuck

Time in a stage, not time since creation. A feature two months old and shipping steadily is healthy. A feature eleven days into `hld` is not.

Defaults, tunable in `watch.conf`: `idea` 3 days, `prd` 5, `hld` 7, `plan` 5, `build` 21, `shipped` 5 before the retro is overdue.

Also stuck, regardless of clock: a stage advanced with no gate entry in `04-progress.md`, a PRD with no measurable success metric, an HLD with an empty review section, a `plan/` with no PR after a week, and anything shipped with no retro.

## Reporting

Lead with the ones where you are the blocker, since those are the ones you can fix in the next hour. Then blocked on someone else, named, with how long. Then healthy, one line each.

For every stalled feature say what specifically is missing, never just that it is stalled. "Waiting on Dana to sign the PRD gate since Tuesday" is actionable. "PRD stage, 6 days" is not.

## Status colour

Green means the target date is still credible. Amber means it is at risk and there is a named reason. Red means it will miss and the date has not been changed yet, which is the real problem. A red feature whose target has been moved and communicated is amber.

Do not let a feature sit green because nobody updated it. Silence is amber.

## Never

Do not edit `feature.yml` to make a report look better. Do not advance a stage on the owner's behalf. Report, and let the gate be a human decision.
