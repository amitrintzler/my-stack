---
name: tune
description: Make the harness cheaper and quieter by measuring what was reported and never acted on, then proposing concrete config changes. Use for tune the harness, too noisy, weekly tune, why do I keep seeing this.
---

# Tune

A watch harness decays in one specific way. It reports something you have decided not to care about, you skim past it, and within a month you skim past everything. This skill stops that by measuring it rather than guessing.

## The measurement already exists

`bin/digest.sh --all` maintains `~/.agents/shnitzel/open-ages.json`, which records when each open item was first seen, and appends a line per run to `metrics.jsonl` with the mean age of open items per kind.

Read it as intent. An item open for forty days is not a backlog item, it is a decision you have already made and are re-reading weekly. That is the waste.

## What to propose

Work from the numbers, one proposal per finding, each with the actual figure behind it.

A kind whose mean open age exceeds thirty days is being ignored. Propose demoting its severity, raising its threshold, or scoping it to the repos where you do act. Say which items and how long.

A kind that never appears has a broken query or an irrelevant config. A `security_alert` count that is permanently zero across ten repos usually means the feature is off, not that the code is clean.

A repo generating findings you never touch is probably not yours any more. Propose removing it from `REPOS`.

A repo you keep asking about by hand that is not in `REPOS` should be added. The evidence is in `lessons.md` and in the conversation, not in the metrics.

Thresholds that never fire, `STALE_DAYS` for example, are either right or too loose. Compare against the actual distribution of pull request ages before touching them.

## Lessons review

Read `lessons.md` in the same pass. Any lesson cited or restated three times gets promoted into a skill, a lint, or a gate, and then deleted from the file with a note saying where it went. A lessons file that only grows becomes an archive nobody reads.

## Output

A diff, not a rewrite. Show the exact lines to change in `~/.agents/watch.conf` and any skill edit, each with the measurement that justifies it. Then stop and wait. Config that quietly tunes itself is config you can no longer reason about, and the first time it hides something real you will not know why.

Every proposal is scoped. A finding that only occurs in one repository gets a per-repo override, never a global threshold change, because a global change made from one repository's noise silently suppresses the same finding everywhere else. Read `lessons/global.md` and the repo-scoped files separately for the same reason.

Two things this must never propose: suppressing severity 1 and 2 entirely, and raising a threshold to hide a problem rather than because the problem is not yours. If main has been red for nine days, the finding is not that the alert is noisy.

## Cadence

Weekly, alongside the hygiene pass. Four weeks of metrics is the minimum before the numbers mean anything, so early runs should say the sample is thin rather than tuning on noise.
