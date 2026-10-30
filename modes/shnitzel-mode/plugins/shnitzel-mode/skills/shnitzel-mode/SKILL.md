---
name: shnitzel-mode
description: Choose a proportionate approach to engineering work, then use pstack or a focused workflow. Use for shnitzel-mode or engineering implementation requests. Answer ordinary questions directly.
---

# Shnitzel mode

Start with the outcome, not a playbook. Resolve this skill's real path; the distribution root is four directories above its folder when that root holds `install.sh`. Otherwise this is a marketplace install: the root is the `dist` printed by `scripts/bootstrap.sh --print` in the plugin folder, and if it reports none, run setup-shnitzel-mode first. All bin/config paths below are relative to that root. Resolve policy from `config/effort-policy.json` under the installed Shnitzel distribution. Apply runtime_overrides for the actual runtime over shared defaults. Task-specific instructions override its defaults. Runtime and repository permissions always apply.

## Admission

- **Direct.** Questions, explanations, text edits and status requests get the answer. Inspect evidence when needed. No approach menu, feature ledger, todo file, full pstack router or delegates. A read-only investigation remains read-only.
- **Implementation.** Establish the desired observable outcome and evidence of a problem. Consider existing functionality, configuration, a bounded change, and doing nothing. Compare the smallest sufficient solution with a broader one only when the broader one buys something concrete. Include maintenance and verification in the effort, not just coding. Do not invent ROI, token precision or extra requirements.
- Approach selection is inline. Do not delegate research or begin broad exploration to decide which approaches to offer. Use small targeted observational reads only when essential; otherwise identify the evidence to gather as part of the recommended approach. If this host exposes no tools, describe the next action without inventing tool calls or markup.
- Before implementing, use no introductory paragraph: two numbered one-sentence options, then a short recommendation and direct choice question. Aim for 60 to 80 words; the maximum is 120 words for the entire message. A third option is allowed only when distinct. Never offer an unsupported expensive approach merely as a worse comparison. Do not append a design, instrumentation plan or extra closing offer. Recommend one and wait for the user's selection. If only one implementation is sensible, offer it and deferral. A specific approach already selected by the user, including an accepted plan, satisfies this gate. Do not ask again for the same choice.

## Effort

**Focused:** bounded, reversible change with clear acceptance criteria. One agent, targeted reads, smallest change, relevant verification. Do not load the full pstack router, generate PRD/HLD documents, launch panels, create backup files beside tracked files, or commit just to satisfy ceremony. Git supplies recovery in a repository; outside one preserve recoverability without initializing repositories unsolicited.

**Standard:** a change spanning behavior or interfaces. Load the matching installed pstack workflow and only relevant domain guidance. Use workflow-required independent review; do not add a panel merely to plan a panel.

**Deep:** architecture, migrations, production risk or substantial uncertainty. Plan verifiable stages. Use two independent reviewers when supported and required. Preserve required review gates when no independent reviewer is available. Do not represent a sequential self-review as independent.

Risk overrides diff size. Authentication, data deletion, production infrastructure and security boundaries require appropriate checks even for a one-line change. PRD/HLD/retro ledgers are for substantial features or explicit requests. Read `references/effort.md` for standard/deep work and `references/runtimes.md` before using runtime-specific primitives.

## Budget and scope

Include planning, repeated input context, tools, delegates, implementation and verification. Reserve about 20% of an estimated budget for verification and handoff. After two failed exploration or repair rounds, test the premise before spending on another attempt. Material scope growth or exceeding the selected effort returns to the user with revised choices. Do not reduce correctness checks to fit a cheap tier.

For an explicit hard token or dollar cap, run `bin/budget.py preflight` first. It must report verified enforcement for that runtime, mode, unit and all participating calls. Estimates, turn limits and continuation limits are not hard caps. Unsupported means stop before model execution and name an alternative. Missing usage is unknown, never zero. Read `references/budgets.md` before capped or delegated work.

## Authority and pstack

Explicit task authorization persists within its scope. Do reversible authorized work without repeated approval; ask before an external action not already authorized. Repository and host permission requirements still hold. Scheduled watch work stays read-only and drafts only. Never widen authorization because a task is difficult.

The Shnitzel entry instruction owns automatic routing; pstack's session mandate is off in managed installations. Explicit `/poteto-mode` requests the full upstream workflow. For standard/deep work, locate pstack through the active engine and load its real workflow rather than copying it here. Runtime-specific `pstack-models.md` is the model source of truth. Never invent model aliases, silently raise the model tier, or claim an unavailable capability.

Load repo-scoped lessons only when relevant. Learnings stay in the narrowest scope; read `references/scoping.md` when recording them. Preserve unrelated and generated work.
