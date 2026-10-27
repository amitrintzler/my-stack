# Architecture review

Historical review of version 1.3. Current changes and verification are recorded in docs/acceptance.md.

A review of this kit by the person who built it, written to the standard the `thermo-nuclear-code-quality-review` skill asks for rather than to make the thing look good. Findings are ordered by how much they should change your decisions, not by how easy they are to fix.

## The central weakness

**Almost every guarantee here is prose, and prose is a request.**

The always-stop list, the scoping rules, "never post a comment", "drafts only": all of it is markdown that a model reads and usually follows. Usually is not a security property. Three things in this kit are actually enforced, and it is worth knowing exactly which three.

The collectors are separate shell scripts that contain no mutating command, so they cannot write even if instructed to. `bin/publish-check.sh` fails a build. A read-only token, if you use one, is enforced by GitHub rather than by the agent.

Everything else is a strongly worded suggestion. That is not a reason to abandon the design, since a well-written constraint changes behaviour most of the time, and most of the time is a real improvement over nothing. It is a reason to not describe this as safe, and to put the genuinely irreversible actions behind something that is not prose.

**What I would do.** Use a read-only PAT for the watch harness, a separate write-capable one only in interactive sessions. That single change converts "the harness will not push" from a promise into a fact.

## The hole the prose cannot cover

**MCP tools bypass every guard in this kit.**

You have the GitHub MCP server connected with a PAT. The always-stop list is written in terms of shell commands: no `git push`, no `gh pr create`. A model can call `create_pull_request` through MCP and never touch a shell. Nothing in this kit sees it, nothing blocks it, and the report will say drafts only because as far as the skill is concerned, it was.

This is the most specific and most serious finding here. Two mitigations, in order: scope the MCP PAT to read-only for anything unattended, and restate the always-stop list in terms of effects rather than commands, so "opening a pull request" is banned regardless of which tool opens it. I have written the list in terms of effects, but the examples throughout are shell-shaped, and a model pattern-matches on examples.

## Volume versus attention

**Thirty skills, seventeen domain cards, about three thousand lines. Nothing reads all of it.**

Routing depends on the router being loaded and followed, and every skill added makes the correct one slightly less likely to fire. I have no evidence about where that curve turns. The kit is at the size where I would expect degradation and I cannot prove it either way.

**What I would do.** Before adding a thirty-first skill, delete one. Track which skills actually fire over a month, using the same open-age instinct applied to skills rather than findings. A skill that never triggers is worse than absent, because it dilutes the routing table.

## The gap that matters most

**There are no evals. Nothing here is proven to change behaviour.**

Every collector is tested. Not one skill is. I verified that `gh-collect.sh` emits the right JSON, and I verified nothing about whether `platform-change` actually makes an agent name the rollback before the change. pstack ships an `eval` playbook for exactly this and I did not use it.

This is the difference between "I wrote instructions" and "the instructions work". Right now this kit is the former.

**What I would do.** Pick the three skills whose failure would cost most, which are `platform-change`, `incident-drill` and `review-reply`, and write one eval each: a fixed scenario, run with and without the skill, with a rubric for what a good answer contains. That is an afternoon and it converts the whole thing from a hypothesis to something measured.

## Fixtures are not reality

**Every collector was verified against mocks I wrote, which means mock-shaped bugs are invisible.**

The `gh` JSON field names, the Argo CD status shape, the Nexus blob store fields, the OpenShift cluster operator conditions: all from documentation and memory, none against a live API. A field renamed upstream, or a shape that differs on your version, produces a probe that silently returns nothing. A collector that reports zero findings looks identical to a healthy system.

This class of bug already bit once. `scope-check.sh` used `md5sum`, which does not exist on macOS, so on your machine every scope finding would have had an empty fingerprint and been suppressed permanently after its first report. Found and fixed during this review, but only because I went looking.

**What I would do.** Add a self-test to each probe: if a query returns valid JSON with zero items where the schema expects a list, report that as a low-severity finding rather than as silence. Absence of findings should be distinguishable from absence of data.

## Scale is untested

**The severity model was tuned on one repository and two features.**

At your actual scale, twenty engineers across many repositories, the first `--all` run could return several hundred items. The ranking that looked sensible against thirty-two findings may be useless against three hundred, and the open-age tuning loop needs four weeks before it helps. That is four weeks of a possibly unusable report.

**What I would do.** On the first real run, do not schedule anything. Read the raw count per kind and set the config from that, rather than from my defaults. If severity 3 alone returns fifty items, the severity model is wrong for you and it is cheaper to know on day one.

## Enforcement lag in scoping

**Scope leaks are detected after they happen, never prevented.**

`scope-check.sh` finds a lesson naming a foreign repo or a feature citing another feature, after both have been written and possibly after both have been acted on. Nothing stops a session opening two feature ledgers at once, which is the actual contamination event.

The honest framing is that this is a smoke detector, not a firewall. It is genuinely useful and it is not the thing its name suggests.

**What I would do.** Accept it as detection, and get prevention from the filesystem instead: one feature per worktree, so the other ledgers are not on disk in that session. That is a real boundary rather than a checked one.

## State sprawl

**Six state files under `~/.agents`, no schema versions, no migration path.**

`model-roles.md`, `watch.conf`, `watch-state.json`, `open-ages.json`, `lessons/`, `profile/`. When a format changes, the only migration that exists is the one-off in `install.sh` that moves a flat `lessons.md` aside. A second format change will need another hack, and eventually a version somebody upgrades into will silently misread an old file.

**What I would do.** Put a `version:` line in each file now, while there is only one version, and have the collectors refuse rather than guess when they see a number they do not know.

## No multi-user story

**Everything is per-machine and per-person.**

If two of your engineers adopt this, they build separate repo profiles and separate lessons about the same repositories, and neither benefits from the other's. There is no sharing mechanism, no conflict handling, and no notion of a team-level lesson.

For a personal kit this is correct and simple. For a team of twenty it is the largest missing piece, and it is not a small addition: shared lessons need review, ownership and a way to disagree.

**What I would do.** Do not solve it yet. Use it alone for a quarter. If it still earns its place, the team version is repo-scoped lessons committed into each repository rather than into a home directory, which makes them reviewable through the pull request process you already trust.

## Ledger discipline

**The feature lifecycle assumes a discipline that teams under pressure abandon first.**

Gates get skipped during a crunch, and the ledger then reports a stage that is not true. `feature-track` will confidently describe a feature that moved on three weeks ago. A stale ledger is worse than no ledger, because a wrong status gets acted on while a missing one gets investigated.

The scanner partly covers this by flagging a stage advanced with no gate recorded, which is a good design. It cannot detect a ledger that is simply frozen while the work continues elsewhere.

**What I would do.** Cross-check the ledger against git. A feature whose branch has commits from this week and a ledger untouched for a month is a specific, detectable finding, and I did not implement it.

## Portability claims are broader than the testing

**Five runtimes claimed, two actually exercised.**

The Codex and Prime paths are symlinks into `~/.agents/skills/`, which is a reasonable inference from how those tools work and is not the same as having run them. The Gemini CLI and local model paths are a rules block appended to a file, which is a weaker integration than the table implies. The degradation rules are written but unproven.

**What I would do.** Either test the three untested runtimes or downgrade the claim in `CAPABILITIES.md` from support to expected-to-work. The table currently reads more confidently than the evidence supports, and that is my error rather than a design flaw.

## What I would keep unchanged

Deterministic collection with no model attached is the best decision in the kit and everything else benefits from it.

Roles instead of vendor slugs has already paid for itself and will keep paying every time a model is deprecated.

Measuring what stays open, rather than asking whether the reports are useful, is the right way to tune anything a human skims.

Overlay rather than fork. Every week that pstack ships and this repository needs no merge is that decision continuing to pay.

The refusal to auto-apply anything. It is the constraint most likely to be relaxed later for convenience, and the one most worth defending.

## Summary

The engineering is sound where it is deterministic and unproven where it is prose. The two things to do next, in order: scope the tokens so the important guarantees stop depending on good behaviour, and write three evals so the skills stop being an untested hypothesis. Everything else on this list can wait a quarter.
