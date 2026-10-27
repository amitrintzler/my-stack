# The watch harness

Every recurring request has the same shape. Something changed on GitHub, and the question is whether it needs you now, today, or not at all. The harness answers that on a schedule instead of on demand.

## Three layers, deliberately separated

**Collection is deterministic.** `bin/gh-collect.sh` runs every `gh` query in shell and emits one JSON digest. No model is involved, so a run costs nothing, returns the same shape every time, and can fire hourly without anyone paying for it. This is the single most important design choice in the harness. An agent that issues twelve `gh` calls per check is both expensive and non-reproducible.

**Judgement is the model's.** The `watch` skill reads the digest, ranks it, and decides what deserves an interrupt. `pr-inbox` works out whose turn each pull request is. `review-reply` drafts answers to open threads.

**Delivery is a schedule.** The same collector feeds an on-demand `/watch`, a Cowork scheduled task in the cloud, and a launchd job on the Mac.

## What it watches

| Kind | Sev | Source |
| --- | --- | --- |
| `main_red` | 1 | `gh run list` on the default branch |
| `my_pr_ci_red` | 2 | `statusCheckRollup` on your open pull requests |
| `my_pr_unanswered` | 2 | GraphQL review threads where `isResolved` is false |
| `my_pr_conflict` | 3 | `mergeStateStatus` is `DIRTY` |
| `security_alert` | 3 | open high and critical Dependabot advisories |
| `review_requested` | 3 or 5 | `gh search prs --review-requested=@me`, escalated past the SLA |
| `my_pr_ready` | 4 | approved, green, nothing left but a merge |
| `my_pr_stale` | 6 | idle beyond the stale threshold |

Unresolved review threads need GraphQL. No REST endpoint reports thread resolution, which is why that one query is a `gh api graphql` call rather than a list command.

## Dedupe is what makes it bearable

Every item carries an id and a fingerprint. The id is stable, the fingerprint changes when the underlying thing changes: the head commit for a pull request, the run's head SHA for a red build, the thread count for review threads. State lives in `~/.agents/watch-state.json`.

A pull request that sat still since the last run is suppressed. One that got a new commit reappears, because the failure you were told about yesterday is not the failure it has today. Delete the state file to get a full report again, or pass `--all`.

Without this, an hourly watch tells you the same six things sixty times a day and you stop reading it in a week.

## What it never does

Read-only by construction. It never posts a comment, opens or merges a pull request, pushes a branch, re-runs a workflow, or rebases anything. Drafts land in `.watch-drafts/` in the working tree and the report names them.

That holds in scheduled runs too, where nobody is present to object. This is the property that makes it safe to leave running. Give the collector a read-only token and the guarantee is structural rather than a promise.

## The feature ledger feeds the same digest

`bin/feature-scan.sh` walks the configured project roots, reads every `docs/features/*/feature.yml`, and emits items in the same shape. `bin/digest.sh` runs both collectors and merges them, so one ranked list carries a red pipeline and a design stuck in review for eleven days.

The ledger format is flat `key: value` on purpose. That is not laziness, it is so the scanner reads it with `grep` and needs no yaml parser on any machine it runs on.

## How it gets better

Three files under `~/.agents/shnitzel/`, all of them readable and editable by hand.

`profile/repos/<owner>__<repo>.md` is what a session would otherwise rediscover every time: build and test commands taken from CI rather than guessed, deploy path, protection rules, conventions, the known flake. `lessons.md` is append only, one entry per correction or hard-won constraint, each written as a rule plus a why plus how to apply it.

`open-ages.json` is the interesting one. `digest.sh --all` records when each open finding was first seen, and `metrics.jsonl` gets a line per run with the mean open age by kind. An item open for forty days is not a backlog item, it is a decision you have already made and keep re-reading. `/tune` turns that into a proposed diff to `watch.conf`, with the number behind every line, and waits for approval rather than applying it.

## Scope leaks are a watched property

`bin/scope-check.sh` is the third collector and it runs on every digest. It reports a lessons file whose declared scope disagrees with its path, a repo-scoped lesson that names a different repository, a feature document citing another feature's id, and a `.watch-drafts/` reply referencing a repo other than the one it sits in.

None of these are fixed automatically. Rescoping a lesson changes where it will be applied in future, which is a decision rather than a tidy-up.

## Setup

```bash
brew install gh jq && gh auth login
cp config/watch.example.conf ~/.agents/watch.conf
$EDITOR ~/.agents/watch.conf        # list your repos and orgs
bin/gh-collect.sh --pretty --all    # confirm it sees what you expect
```

Then create the Cowork scheduled tasks from `schedules/cowork-tasks.md`, and optionally install the launchd job for a local digest that costs nothing.

## Cadence, and why

Hourly during work hours for severity 1 and 2 only, because a broken main branch and your own failing pull request are the only two things worth an interruption. A daily 08:00 brief that is read start to finish. A Monday hygiene pass for the slow decay that nothing else catches. After a push, tail the run until it settles, bounded by the run finishing rather than by a timer.

Crons are stored in UTC and the work week is Sunday to Thursday, so the day field reads `0-4`. Israel leaves summer time in late October and every cloud schedule then drifts an hour later in local terms. That is a calendar reminder, not a bug to discover in November.
