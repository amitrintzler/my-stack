# Shnitzel mode

An effort-aware overlay around a current, pinned pstack engine. Ordinary questions get direct answers. Engineering requests get brief approach choices, then the smallest selected workflow that meets the acceptance criteria. Focused edits do not trigger PRDs, HLDs, review panels or the full pstack router.

Only the two Shnitzel entry skills and explicit poteto-mode are linked for discovery by default. The other skills remain available by path and are loaded on demand. `--all-skills` enables full discovery at the cost of additional standing metadata.

The 30 optional skills and 17 domain cards remain available, loaded only when relevant. Deterministic collectors gather state before a model interprets it. Unavailable data is reported explicitly. Hard-budget requests stop before execution when the runtime cannot enforce the requested unit across every call.

## Install from a marketplace

```bash
claude plugin marketplace add amitrintzler/my-stack
claude plugin install shnitzel-mode@my-stack
codex plugin marketplace add amitrintzler/my-stack   # Codex
```

Then run setup-shnitzel-mode in each runtime. It fetches the matching tagged distribution with `scripts/bootstrap.sh` and continues with the steps below. Publishing a new version is covered in [docs/publishing.md](docs/publishing.md).

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

For local execution use `./install.sh --apply local --local-root /path/to/project`. Run `bin/cowork-package.py` to build a self-contained `.runtime/cowork` connected folder with its own START.md. See [runtime adapters](docs/runtimes.md) and [acceptance evidence](docs/acceptance.md).

The installer updates only its marked blocks, refuses foreign skill collisions and keeps backups outside working repositories. Uninstall restores owned model-sheet changes only if they have not been edited afterward, and never deletes somebody else's skill link. `./install.sh --uninstall --apply` removes the default runtime targets; local installations are removed explicitly from their project.

## Choosing effort

- Direct: questions, text work and status, with evidence when needed.
- Focused: clear bounded reversible change, one agent and targeted verification.
- Standard: relevant pstack workflow with required review.
- Deep: architecture, production risk, migration or uncertainty, with staged verification.

Before implementation, show meaningful alternatives in at most 120 words and wait for a choice. A previously accepted plan or explicit approach already satisfies the choice. Risk overrides diff size. About 20% of an estimated budget is reserved for verification and handoff. Two failed rounds trigger a premise check. No effort tier removes required correctness checks.

[Effort policy](config/effort-policy.json) configures the defaults. Explicit hard limits use `bin/budget.py preflight`; shipped native adapters do not claim exact hard-cap enforcement. The request-host BudgetLedger is tested accounting infrastructure, not proof that an arbitrary CLI intercepts every model call. [Budget guidance](plugins/shnitzel-mode/skills/shnitzel-mode/references/budgets.md) describes the distinction.

## Updates and verification

`--locked --build` rebuilds recorded source revisions. `--rollback` restores the previous engine. Failed candidates never replace the working engine. [Upstream procedure](docs/upstream-sync.md) explains temporary upstream adaptations, policy differences and provenance.

Run `python3 -m unittest discover -s tests -v` and `bin/publish-check.sh`. Contract tests do not prove that a model follows a skill. Behavioral acceptance and token comparisons are recorded separately, including failures and missing telemetry. The [earlier architecture review](docs/architecture-review.md) is a historical review of 1.3, not a current verification report.

## Collectors

Configure watch.conf, then run `bin/digest.sh --all --pretty`. Add `--no-state` for an observational run. The digest includes coverage so failed queries cannot masquerade as healthy empty results. Approved PRs need completed successful checks and a clean merge state before being labeled ready. Scheduled runs remain read-only and never post replies.

MIT. See [NOTICE](NOTICE.md) for the original pstack and port attribution.
