# 🤖 AI / LLM Tooling

> Code generation, autonomous agents, PR review, observability, and orchestration.

---

## Tools

---

### Claude Code

| Field | Value |
|-------|-------|
| **Radar** | 🟢 Adopt |
| **Status** | Production-ready |
| **Website** | [claude.ai/code](https://claude.ai/code) |
| **Projects** | [GCP SaaS Platform](../projects/gcp-saas-platform.md) |

**Why:** Best agentic coding tool available. Multi-file edits, MCP-aware, understands large codebases via context window. Highest ROI on complex tasks: spec-to-code, refactors, architecture scaffolding.

**My Pattern:**
- Feed OpenAPI / proto specs as input → generate service skeletons
- Use with `CLAUDE.md` in repo root to inject project conventions
- Combine with MCP servers for GitHub, GCP, and internal tools

**CLAUDE.md template (repo root):**
```markdown
# Project Context for Claude Code

## Stack
- Language: Go / TypeScript
- Platform: GCP (GKE Autopilot + Cloud Run)
- IaC: OpenTofu + Terragrunt
- DB migrations: Atlas (expand-contract pattern)

## Conventions
- All PRs require unit + integration tests
- Use Workload Identity Federation — no static credentials
- Secrets via Secret Manager CSI driver only
- Follow trunk-based development — no long-lived branches
```

**Gotchas:**
- Context window has limits on very large monorepos — structure your CLAUDE.md to guide scope
- Don't use for security-sensitive code without human review gate
- Pair with CodeRabbit: Claude Code writes → CodeRabbit reviews

---

### GitHub Copilot

| Field | Value |
|-------|-------|
| **Radar** | 🟢 Adopt |
| **Status** | Production-ready |
| **Website** | [github.com/features/copilot](https://github.com/features/copilot) |
| **Projects** | [GCP SaaS Platform](../projects/gcp-saas-platform.md) |

**Why:** Best inline autocomplete. Complements Claude Code — Copilot for keystroke-level suggestions, Claude Code for task-level agentic work. Copilot Autofix for security fixes in PRs.

**Key Concepts:**
- Copilot Chat (IDE) = interactive, context-aware Q&A
- Copilot Autofix = auto-generates fix PRs for CodeQL/Dependabot findings
- Copilot for CLI = shell command generation

**Gotchas:**
- Disable for files containing secrets or proprietary algorithms (`.copilotignore`)
- Inline suggestions can over-fit to bad patterns in your codebase — review critically

---

### CodeRabbit

| Field | Value |
|-------|-------|
| **Radar** | 🟢 Adopt |
| **Status** | Production-ready |
| **Website** | [coderabbit.ai](https://coderabbit.ai) |
| **Projects** | [GCP SaaS Platform](../projects/gcp-saas-platform.md) |

**Why:** Best AI PR reviewer available. Does semantic diffs, not just line-by-line comments. Understands PR intent. Surfaces architectural issues, not just nits. Integrates with GitHub natively.

**My Pattern:**
```yaml
# .coderabbit.yaml
reviews:
  auto_review:
    enabled: true
    drafts: false
  path_filters:
    - "!**/*.md"
    - "!**/vendor/**"
  profile: "chill"  # assertive | chill
```

**Gotchas:**
- `assertive` profile generates noise on large PRs — tune per repo
- Teach it your conventions via the `.coderabbit.yaml` `instructions` field
- Not a replacement for human review on security-critical paths

---

### LangGraph

| Field | Value |
|-------|-------|
| **Radar** | 🟡 Trial |
| **Status** | Exploring |
| **Website** | [langchain-ai.github.io/langgraph](https://langchain-ai.github.io/langgraph) |
| **Projects** | [GCP SaaS Platform](../projects/gcp-saas-platform.md) |

**Why Evaluating:** Best framework for stateful multi-agent orchestration. Graph-based state machine model gives fine control over agent loops. Better than LangChain for production — less magic, more explicit.

**Key Concepts:**
- `StateGraph` = the orchestration graph
- `nodes` = individual agents or tool calls
- `edges` = conditional routing between nodes
- `checkpointer` = persistence layer for long-running workflows
- Human-in-the-loop via `interrupt_before` / `interrupt_after`

**Gotchas (so far):**
- Steeper learning curve than LangChain — invest in understanding the state model first
- Checkpointer setup (Postgres/Redis) needed for production — don't skip this
- Debug with LangSmith — blind debugging of agent graphs is painful

---

### LangSmith

| Field | Value |
|-------|-------|
| **Radar** | 🟡 Trial |
| **Status** | Exploring |
| **Website** | [smith.langchain.com](https://smith.langchain.com) |

**Why Evaluating:** Tracing, evals, and prompt regression testing for LLM apps. Essential for catching prompt drift in production. Pairs naturally with LangGraph.

**Key Concepts:**
- Traces every LLM call with full input/output
- Datasets + evaluators for automated regression testing
- Prompt hub for versioned prompt management

**Gotchas:**
- Data leaves your infra — check compliance requirements before using in prod
- Braintrust is a strong alternative if data residency is a concern

---

### Braintrust

| Field | Value |
|-------|-------|
| **Radar** | 🟡 Trial |
| **Status** | Exploring |
| **Website** | [braintrust.dev](https://braintrust.dev) |

**Why Evaluating:** LLM observability alternative to LangSmith. Better data residency story (self-hostable). Strong eval framework. Evaluating alongside LangSmith.

**Alternatives Considered:**

| Tool | Notes |
|------|-------|
| LangSmith | Strong, but SaaS-only data |
| Helicone | Simpler, good for cost tracking |
| Arize Phoenix | OSS, heavier infra footprint |

---

### Karpathy Skills

| Field | Value |
|-------|-------|
| **Radar** | 🟡 Trial |
| **Status** | Exploring |
| **Licence** | MIT |
| **Website** | [github.com/forrestchang/andrej-karpathy-skills](https://github.com/forrestchang/andrej-karpathy-skills) |
| **Projects** | [GCP SaaS Platform](../projects/gcp-saas-platform.md) |

**Why Evaluating:** Small, opinionated `CLAUDE.md` that codifies Andrej Karpathy's observations about common LLM coding failure modes into four rules — **Think Before Coding**, **Simplicity First**, **Surgical Changes**, **Goal-Driven Execution**. Installable as a Claude Code plugin or dropped straight into a repo. Low-cost way to reduce over-engineering and unrequested refactors in agentic edits. Pairs cleanly with our existing [Claude Code](#claude-code) + [CodeRabbit](#coderabbit) loop.

**The Four Rules (at a glance):**

| Rule | What it enforces |
|------|------------------|
| 1. Think Before Coding | State assumptions, surface ambiguity, ask before picking an interpretation |
| 2. Simplicity First | No speculative abstractions, no unrequested flexibility, no error handling for impossible cases |
| 3. Surgical Changes | Edit only what the task requires; don't "improve" adjacent code or delete pre-existing dead code |
| 4. Goal-Driven Execution | Turn tasks into verifiable success criteria and loop until they pass (tests, checks) |

**My Pattern:**
- Use as a **baseline** `CLAUDE.md` on greenfield repos, then append project-specific conventions below it (stack, IaC, DB migration rules, etc.)
- On existing repos with a curated `CLAUDE.md`, cherry-pick rules 3 (Surgical) and 4 (Goal-Driven) — the biggest wins in agentic PRs
- Install as a plugin for **personal/exploratory repos** where pinning a file isn't worth it

**Install — Option A: Claude Code plugin (reusable across repos):**
```bash
# Inside a Claude Code session
/plugin marketplace add forrestchang/andrej-karpathy-skills
/plugin install andrej-karpathy-skills@karpathy-skills
```

**Install — Option B: drop into a new repo:**
```bash
# From repo root
curl -o CLAUDE.md https://raw.githubusercontent.com/forrestchang/andrej-karpathy-skills/main/CLAUDE.md
```

**Install — Option C: append to an existing CLAUDE.md:**
```bash
echo "" >> CLAUDE.md
curl https://raw.githubusercontent.com/forrestchang/andrej-karpathy-skills/main/CLAUDE.md >> CLAUDE.md
```

**Example — Goal-Driven rewrites in practice:**

The skill reframes vague asks into verifiable loops. Instead of:

> "Add validation to the signup endpoint."

…Claude is nudged to plan as:

```
1. Write failing tests for invalid inputs (empty email, bad format, weak password) → verify: tests fail
2. Add validator on POST /signup → verify: tests pass
3. Run full test suite → verify: no regressions
```

**Example — composing with our stack:**

```markdown
<!-- CLAUDE.md (repo root) -->

# (Contents of karpathy-skills CLAUDE.md pasted above this line)

---

## Project-Specific Guidelines

## Stack
- Language: Go / TypeScript
- Platform: GCP (GKE Autopilot + Cloud Run)
- IaC: OpenTofu + Terragrunt
- DB migrations: Atlas (expand-contract pattern)

## Conventions
- All PRs require unit + integration tests
- Use Workload Identity Federation — no static credentials
- Secrets via Secret Manager CSI driver only
- Follow trunk-based development — no long-lived branches
```

**Gotchas:**
- The guidelines "bias toward caution over speed" (stated in the upstream README) — for trivial one-line fixes they can over-trigger clarifying questions. Tell Claude to skip Rule 1 for trivial tasks when needed.
- Rule 3 (Surgical Changes) conflicts with `simplify` / cleanup-style skills that *want* to touch adjacent code. Don't load both at once — pick per task.
- Upstream file is a living doc; pin a commit SHA in the `curl` URL if you need reproducible onboarding across a team.
- Plugin install path (`@karpathy-skills`) is the marketplace slug, not a version — there's no semver yet. Re-install to pick up updates.

**Alternatives Considered:**

| Tool | Why I didn't choose it (yet) |
|------|------------------------------|
| Hand-rolled `CLAUDE.md` | What I use today — Karpathy Skills is a structured baseline on top of it, not a replacement |
| Anthropic "Claude best practices" docs | More general; Karpathy Skills is tighter and enforcement-oriented |
| Cursor Rules / `.cursorrules` | IDE-specific; Karpathy Skills is tool-agnostic Markdown |
