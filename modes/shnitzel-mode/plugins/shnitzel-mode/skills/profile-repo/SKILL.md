---
name: profile-repo
description: Build or refresh the working profile of a repository so future sessions start informed instead of exploring from scratch. Use for profile this repo, learn this codebase, onboard me to X, refresh the repo profile.
---

# Profile repo

The single biggest waste in an agent session is rediscovering facts that were true last week. A repo profile is a small file that answers, in advance, the questions every session asks first.

One file per repository at `~/.agents/shnitzel/profile/repos/<owner>__<repo>.md`. Under 80 lines. A profile nobody reads because it is long is worse than no profile.

## What goes in it

Stack and versions, in one line each. The exact commands to build, test, and lint, copied from CI rather than guessed, because the guess is wrong often enough to matter. Where CI is defined and the names of the workflows that gate a merge. How it deploys, and to which environments. The default branch and the protection rules on it. The parts of the tree that matter and the parts that are generated. Conventions a newcomer breaks: commit format, test layout, error handling, the linter's opinionated rules. Known failure modes, the flaky test, the slow job, the migration that needs a manual step. Who reviews what.

Cite the file each fact came from. A profile whose claims cannot be traced decays into folklore.

## What stays out

Anything already in `CLAUDE.md` or `AGENTS.md` in that repo, because duplicating it means two versions drift apart. Anything that changes weekly. Secrets, tokens, and internal URLs that are not already public in the repo.

## Refresh, do not rewrite

On a later run, read the existing profile first and update only what changed. Mark every fact you re-verified with the date. A profile with a two month old date on the test command is a warning, not a fact, and the reader can then decide to check it.

Refresh when the build or test command fails in a way the profile did not predict, when a major dependency moves, or every quarter, whichever comes first.

## People

`~/.agents/shnitzel/profile/people.md` holds the same idea for humans: who owns what, which timezone they are in, and their typical review latency. For a manager of a team spread across four countries that last one is not trivia, it decides whether waiting for a review is reasonable or a blocker. Keep it factual and work related. Nothing personal belongs in it.
