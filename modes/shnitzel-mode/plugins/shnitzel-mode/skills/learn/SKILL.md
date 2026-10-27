---
name: learn
description: Capture a durable lesson from what just happened, as a rule with a why and a how, into the shared lessons file. Use for remember this, that was wrong, note for next time, learn from this, capture that.
---

# Learn

The model does not remember anything between sessions. Files do. Everything called learning here is a file being written and read again, and saying that plainly keeps the expectations honest.

## Pick the scope before you write

Three destinations, and choosing wrong is how one project's constraint becomes another project's bug.

A lesson about one feature goes in that feature's directory, next to its ledger. It is probably about this design, not about the codebase.

A lesson about one repository goes in `~/.agents/shnitzel/lessons/repos/<owner>__<repo>.md`, with `scope: repo:<owner>/<repo>` as the first line.

A lesson goes in `lessons/global.md` only once you can name a second repository where it also held. Not because it sounds general. Name the second instance in the entry, because that is what a later reader needs to judge it.

Default to the narrowest tier. Widening later is cheap. A wrong global rule is expensive and invisible, since it will be applied confidently in a context you never checked. `references/scoping.md` in the **shnitzel-mode** skill has the full rules.

Append only, newest last, shared by every runtime because they all read the same directory.

## What earns an entry

Four things, and nothing else.

A correction the owner made to your output, in their words where possible. A constraint discovered the hard way, for example that a deploy needs a specific approval or that a test suite is flaky above a concurrency level. A decision and the reasoning behind it, because reasoning is what does not survive. An approach that failed, which is worth more than one that worked, since the failure will look attractive again in three months.

Not worth an entry: anything derivable from the repository, anything already in a `CLAUDE.md` or `AGENTS.md`, and the details of the current task.

## Shape

```
## 2026-08-24 · acme/api · deploy
Rule: the failover drill job must pass before any change to the region router merges.
Why: it is the only test that exercises real DNS, and unit tests pass while failover is broken.
Apply: block the merge, do not just report the red job.
```

Date, scope, rule, why, apply. The `apply` line is the one that makes it usable later. A lesson without it is a diary entry.

## Promotion

Two kinds, and they are different moves.

Widening scope: feature to repo, or repo to global. Requires a named second instance. Record it as `promoted from <where>, second instance <what>` so the claim can be checked later.

Promotion out of prose entirely: a lesson cited three times is not a lesson any more, it is a rule that belongs in a skill, a lint, or a gate. Encode it there, delete the lesson, and note where it went. Writing the same instruction a fourth time is the failure.

Demotion is also allowed and rarely used. A global rule that turns out to be one repo's habit moves down, and the entry says why.

The **tune** skill runs this review weekly. You do not have to notice it yourself.

## When pstack is installed

`pstack:reflect` mines recent transcripts and drafts a skill from repeated behaviour. That is the heavier version of this and worth running monthly. This skill is the cheap one you run in the moment, before the reason is forgotten.
