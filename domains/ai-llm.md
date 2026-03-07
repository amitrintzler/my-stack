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
