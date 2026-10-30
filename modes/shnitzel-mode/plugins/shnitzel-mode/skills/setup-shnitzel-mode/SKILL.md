---
name: setup-shnitzel-mode
description: Configure Shnitzel routing, effort choices and runtime-specific pstack model roles. Use for setup-shnitzel-mode or changing Shnitzel configuration.
---

# Setup Shnitzel

0. Resolve the distribution. From this plugin's folder run `scripts/bootstrap.sh --print`. If it exits 4, this is a marketplace install with no distribution yet: say that setup will fetch the release matching the plugin version from its repository, then run `scripts/bootstrap.sh` once the user agrees. Use the `dist` it prints as the root for every path below. On a fresh distribution, build and activate the locked engine with `bin/upstream-check.sh --locked --build`, then `--locked --apply`, and show the installer dry run before `./install.sh --apply`.
1. Run `bin/doctor.py` under the Shnitzel distribution to discover the installed engine, runtime binaries and capability gaps. A directory's existence does not identify the current runtime.
2. Read the active pstack setup-pstack skill and its mapping for the actual runtime. Enumerate reachable models and accepted effort levels there. Use its pstack-models.md sheet; do not create a universal model-roles.md.
3. Preserve existing model choices. If a legacy model-roles.md exists, show the installer's migration proposal and confirm reachable models before adopting any mapping. Keep the legacy file intact.
4. Show the resulting model and effort configuration, plus the short Shnitzel standing instruction. pstack's automatic session mandate is off; explicit poteto-mode remains available. Apply the already authorized setup scope without asking twice. New unrelated configuration requires its own authorization.
5. Default implementation requests to meaningful approach choices, focused work to no delegates, and deep panels to two reachable configured reviewers. Do not override an explicit user choice.
6. Show the doctor report. Distinguish installed, contract-tested and live-verified runtimes; identify unavailable telemetry and hard-budget enforcement.
