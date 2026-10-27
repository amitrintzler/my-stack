# Scoping

Every tool here writes something down, and written things leak. A constraint learned on one feature turns up as an assumption on the next one, and nobody notices because it arrives phrased as knowledge. This file is the rule that stops it.

## Three tiers, each with one home

| Tier | Lives in | Read when | Leaves the tier only by |
| --- | --- | --- | --- |
| Feature | `docs/features/<id>-<slug>/`, inside the repo, on the feature branch | working on that feature, and never otherwise | evidence it recurs outside the feature |
| Repo | `~/.agents/shnitzel/profile/repos/<owner>__<repo>.md` and `lessons/repos/<owner>__<repo>.md` | working in that repo | evidence it holds in a second repo, named |
| Global | `lessons/global.md`, and the skills themselves | always | never automatically |

The default tier for anything new is the narrowest one that fits. A fact starts at feature scope and earns its way up. Widening requires a second independent instance you can point at, recorded in the promotion note. Nothing is promoted because it felt general.

## What you load

Global, plus the repo you are in, plus the one feature you are on. Nothing else. Not the neighbouring feature, not the other repo, not last month's project because it sounds similar.

If a task spans two features, that is two tasks. Run them separately. The moment both ledgers are open in one context, the isolation is gone and no rule in this file can restore it.

## What must never carry across features

These are the ones that look like knowledge and are actually contamination.

Acceptance criteria, success metrics, target dates, and scope decisions. Feature B's criteria are not a variation on feature A's, and inheriting them produces a spec that reads plausibly and is wrong.

A rejected alternative. Feature A rejecting a queue does not mean feature B should. The reasons were local to A's constraints, and the second team never sees those reasons, only the conclusion.

Customer names, contract terms, incident details, and anything a specific client told you. Different features often mean different clients, and this is the failure with consequences beyond a bad spec.

Draft replies in `.watch-drafts/`. They are written against one thread in one repo. Reusing one is how a comment meant for one team lands on another.

Estimates and velocity from a different team. Two teams in different countries do not share a throughput number, and pretending they do makes every plan built on it wrong.

## What may carry across, with a citation

Repo conventions and the exact build, test and lint commands, because they are properties of the repo, not the work. Principles and checks that were deliberately promoted, which is what promotion is for. People facts: who owns what, timezone, typical review latency.

When you carry one of these into a piece of work, say where it came from. An uncited fact cannot be checked later, and by then nobody remembers whether it was observed or assumed.

## How it is enforced, not just promised

**Filesystem.** One feature per branch, and per worktree when two run in parallel. A delegate is handed paths inside its own feature directory. It cannot read what is not in its tree.

**Frontmatter.** Every lessons file carries `scope: global` or `scope: repo:<owner>/<repo>`, and the scope must match the file's path. The reader honours it.

**A check that runs.** `bin/scope-check.sh` looks for the leaks this file describes: a lessons file whose scope does not match its location, a repo-scoped lesson naming a different repo, a feature document referencing another feature's id, a draft sitting in the wrong repo. Findings land in the same digest as everything else, at severity 3.

**Tuning stays scoped.** The **tune** skill may not propose a global threshold change from one repo's noise. A finding that only occurs in one repo gets a per-repo override.

Isolation you cannot observe is isolation you do not have. The check is the difference between this being a design and being a habit.
