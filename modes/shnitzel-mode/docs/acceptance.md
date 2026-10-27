# Acceptance evidence, 2026-10-22

Shnitzel 1.4 is installed locally with a three-skill discovery surface. The active engine combines pstack-claude v0.9.101 at 903e7385382389806c59d6989b6274e24165082b with original pstack v0.15.30 at 4ec7ffa173eaa70d3d9467a627baf0954645a353. The tracked lock records included files, exclusions and port documentation adaptations. No remote publication was performed.

## Deterministic checks

- 25 contract tests pass: shared reservations, uncertain usage, insufficient budgets, concurrent spending, installer ownership/idempotency, native discovery, partial uninstall, multiple local projects, collector coverage, sealed Vault responses, pending checks, engine conflicts and rollback.
- Publish checks and shell/JSON validation pass, including new untracked source files rather than only files already in Git.
- The derived engine passes the port generator, generator check, Shnitzel-to-pstack skill-reference check and project-playbook validation. A locked rebuild and activation succeeded; the prior engine is retained.
- The new statechart suite's final runs have 29 passing tests and 38 TLC-dependent skips. An upstream help-output test failed intermittently in earlier runs; six later complete runs passed. Its cause is unresolved. TLC-based formal verification has not been exercised.
- Explicit native hard-cap preflight exits 3 for every unverified adapter. No native runtime is advertised as exact token or dollar enforcement. BudgetLedger is tested infrastructure for a host intercepting every request, not an installed model gateway.

## Live runtime evidence

| Runtime | Observed result | Remaining acceptance |
| --- | --- | --- |
| Claude Code 2.1.280 | A real print-mode request returned HTTP 429, weekly usage exhausted. | Behavioral cases and current native-plugin integration remain blocked. |
| Codex 0.163.0, isolated toolchain | Direct answer without tools; compact approach choices; authorization-risk diagnosis; focused edit with exact bytes and no extra files. | Full multi-scenario comparison and unsupported-cap/sharpen behavior in the live host. |
| Cowork | Self-contained connected-folder payload built with engine, skills, configuration and attribution. Desktop visibly reports weekly usage 100%. | Actual connected-folder session has not run; package construction is not live Cowork verification. |
| Gemini CLI 0.65.0, isolated toolchain | Installed successfully. Real request exited 41: authentication not configured. Native skill discovery directories are installed and contract-tested. | Authenticated behavior and usage collection. |
| Local Qwen 3.8 27B / LM Studio | Codex 0.163.0 local-provider path produced a correct direct answer after using a 32K context and an isolated configuration. | Full tool-driven editing suite. A warning reported fallback model metadata, and an earlier 8K-context attempt timed out. |

The user's existing global Codex command remains at 0.46.0. The isolated current toolchain was used for acceptance; global executables were not replaced. Doctor reports actual detected global binaries rather than claiming they are upgraded.

Raw local test traces are in the ignored `.eval-results/` directory. They are not published. Source-backed routing tests remain distinct from live completion.

## Token evidence and limits

The same focused label fixture first consumed 80,880 total tokens with a full-router read, then 51,243 with the complete focused admission embedded in the standing instruction. Both produced exactly `Save` followed by a newline, retained only the original two fixture files, and used no delegates. This is a measured 36.6% reduction for one fixture, not a median across the requested end-to-end benchmark. Most tokens were runtime input context; repeated cached input is still included in total tokens. No API-price or subscription-dollar saving is inferred.

The local prompt-only comparison uses identical host capability declarations, model and sampling settings for pstack, Shnitzel 1.3 and Shnitzel 1.4. It tests routing responses without execution tools. It must not be presented as a completed engineering-task benchmark. An initial run exposed invented Agent markup in a tool-less host; the router was corrected to make approach selection inline and to respect actual exposed tools. Output termination on the native API is reported as unknown rather than fabricated from token counts. A later local response avoided fake tool calls but exceeded the 120-word choice limit (131 words), so the final router now targets 60 to 80 words with no introductory paragraph. The targeted final rerun produced 49 words with no invented tool markup. That passes the format check, but it still offered the unmeasured expensive stack as an option despite the rule against unsupported alternatives. Local decision quality therefore remains partial; use the stronger verified host for consequential approach selection. Token reduction alone is not evidence of better judgment.

The target of at least 30% lower median usage on successful end-to-end simple tasks is not yet established. Claude's exhausted quota and Gemini's missing authentication prevent full five-runtime acceptance. These are recorded gaps, not successful tests.

## Reproduction

```bash
python3 -m unittest discover -s tests -v
bin/publish-check.sh
bin/upstream-check.sh --locked --build
bin/doctor.py
bin/budget.py preflight --runtime codex --max-tokens 100
python3 evals/run.py --cases direct choices focused risk hard-cap
```

The final command uses an already-loaded local model with identifier `shnitzel-eval`. It does not install a model, enable paid overage, change authentication or measure a complete tool-driven task. Optional `--cases` and `--treatments` limit its scope.

For Cowork, run `bin/cowork-package.py`, connect the generated `.runtime/cowork` folder, and start with its START.md. It contains real copies rather than symlinks into a host home directory. Building that payload never submits a Cowork task.
