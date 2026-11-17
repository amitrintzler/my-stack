# Shnitzel mode

An effort-aware overlay around a current, pinned pstack engine. Ordinary questions get direct answers. Engineering requests get brief approach choices, then the smallest selected workflow that meets the acceptance criteria. Focused edits do not trigger PRDs, HLDs, review panels or the full pstack router.

Version 1.10.0, engine pinned to pstack-claude v0.9.135 on original pstack 0.15.36. **[Architecture](docs/architecture.md)** explains how it layers on pstack and poteto-mode, effort routing, what loads when, the engine lock, install and the hook, in a few minutes.

Only the two Shnitzel entry skills and explicit poteto-mode are linked for discovery by default. The other skills remain available by path and are loaded on demand. `--all-skills` enables full discovery at the cost of additional standing metadata.

The 28 optional skills and 17 domain cards remain available, loaded only when relevant. A marketplace plugin install also lists the plugin's own 30 skills to the runtime; see [what is loaded, and when](docs/architecture.md#what-is-loaded-and-when). Deterministic collectors gather state before a model interprets it. Unavailable data is reported explicitly. Hard-budget requests stop before execution when the runtime cannot enforce the requested unit across every call.

## Install from a marketplace

```bash
claude plugin marketplace add amitrintzler/my-stack
claude plugin install shnitzel-mode@my-stack
codex plugin marketplace add amitrintzler/my-stack   # Codex
```

Cursor runs original pstack natively, so install Cursor's own pstack plugin from its marketplace, then add Shnitzel as a Cursor plugin: from a checkout, `./install.sh --apply cursor` links it to `~/.cursor/plugins/local/shnitzel-mode` (reload the window afterwards); Teams and Enterprise can import this repository, whose `.cursor-plugin/marketplace.json` lists it. The plugin's always-applied rule carries the same admission text as the other runtimes. Run setup-pstack once so its roles stop using upstream's default models. See [runtime adapters](docs/runtimes.md) for what is and is not verified.

Then run setup-shnitzel-mode in each runtime. It fetches the distribution tagged `shnitzel-mode--v<version>` with `scripts/bootstrap.sh` and continues with the steps below; each release needs that tag pushed. Publishing a new version is covered in [docs/publishing.md](docs/publishing.md).

## Setup from a checkout

```bash
bin/upstream-check.sh --check
bin/upstream-check.sh --build       # isolated candidate, no activation
bin/upstream-check.sh --apply       # validate, activate, record exact revisions
./install.sh                       # dry run
./install.sh --apply               # managed blocks and owned skill symlinks
bin/doctor.py
```

Requires Python 3, Git, Node/npm and Bun for engine updates; jq and authenticated gh for GitHub collection. Existing runtime model sheets are preserved; new sheets inherit the parent session until reachable models are configured. Run setup-shnitzel-mode in each runtime. The isolated current CLI toolchain used for acceptance is in `$HOME/.cache/shnitzel/runtime-tools/node_modules/.bin`; global commands are not replaced. Do not assume one vendor's model aliases work elsewhere.

For Cursor use `./install.sh --apply cursor`; it is not part of the default target set. For local execution use `./install.sh --apply local --local-root /path/to/project`. Run `bin/cowork-package.py` to build a self-contained `.runtime/cowork` connected folder with its own START.md. See [runtime adapters](docs/runtimes.md) and [acceptance evidence](docs/acceptance.md).

The installer updates only its marked blocks, refuses foreign skill collisions and keeps backups outside working repositories. Uninstall restores owned model-sheet changes only if they have not been edited afterward, and never deletes somebody else's skill link. `./install.sh --uninstall --apply` removes the default runtime targets; local installations are removed explicitly from their project.

## What each feature costs

Claude Code records it on its own. The plugin (and `install.sh --apply` for `claude`) adds a Stop and SubagentStop hook that reads the token counts Claude Code already writes to the session transcript and appends them to `~/.agents/shnitzel/usage/ledger-YYYY-MM.jsonl`, tagged with the skill or command that was active, the pstack playbook, the effort tier the turn named, the model and whether a subagent made the call. Nothing to configure. It stores counts and those labels only, never prompts, code, tool output or reasoning, and it never blocks or fails a session.

```bash
bin/shnitzel-cost                       # last 30 days, per feature and per effort tier
bin/shnitzel-cost --days 0 --by feature,model,playbook,subagent
bin/shnitzel-cost --json                # the same, for scripts
```

In Claude Code, `/shnitzel-mode:shnitzel-cost` prints the same table. Tokens are measured. USD is an estimate from API list prices in [`plugins/shnitzel-mode/config/model-pricing.json`](plugins/shnitzel-mode/config/model-pricing.json), dated there, and is not a bill: on a Claude subscription you are not charged per token. A model missing from that file is counted in tokens and marked `*`. Work that no skill or command claimed shows as `unattributed`, and a turn that named no tier shows as `not stated`; neither is guessed. Turn recording off with `touch ~/.agents/shnitzel/usage.off` (or `install.sh --apply --no-usage-hook` for the installer's hook). Codex, Gemini, Cowork and Cursor are not covered: their hooks do not hand over token usage, so `bin/budget.py record` stays the manual path there.

## Choosing effort

- Direct: questions, text work and status, with evidence when needed.
- Focused: clear bounded reversible change, one agent and targeted verification.
- Standard: relevant pstack workflow with required review.
- Deep: architecture, production risk, migration or uncertainty, with staged verification.

Before implementation, show meaningful alternatives in at most 120 words and wait for a choice. A previously accepted plan or explicit approach already satisfies the choice. Risk overrides diff size. About 20% of an estimated budget is reserved for verification and handoff. Two failed rounds trigger a premise check. No effort tier removes required correctness checks.

[Effort policy](config/effort-policy.json) configures the defaults. Explicit hard limits use `bin/budget.py preflight`; shipped native adapters do not claim exact hard-cap enforcement. The request-host BudgetLedger is tested accounting infrastructure, not proof that an arbitrary CLI intercepts every model call. [Budget guidance](plugins/shnitzel-mode/skills/shnitzel-mode/references/budgets.md) describes the distinction.

## Updates and verification

`--locked --build` rebuilds recorded source revisions. `--rollback` restores the previous engine. Failed candidates never replace the working engine. [Upstream procedure](docs/upstream-sync.md) explains temporary upstream adaptations, policy differences and provenance.

Run `python3 -m unittest discover -s tests -v` and `bin/publish-check.sh`. Contract tests do not prove that a model follows a skill. Behavioral acceptance and token comparisons are recorded separately, including failures and missing telemetry. The [current architecture](docs/architecture.md) describes 1.11.0. The [earlier architecture review](docs/architecture-review.md) is a historical review of 1.3, not a current verification report, and [acceptance evidence](docs/acceptance.md) records the 1.4 live run.

## Collectors

Configure watch.conf, then run `bin/digest.sh --all --pretty`. Add `--no-state` for an observational run. The digest includes coverage so failed queries cannot masquerade as healthy empty results. Approved PRs need completed successful checks and a clean merge state before being labeled ready. Scheduled runs remain read-only and never post replies.

MIT. See [NOTICE](NOTICE.md) for the original pstack and port attribution.
