# 🏗️ GCP SaaS Platform

> Greenfield multi-tenant SaaS platform on Google Cloud Platform.  
> Large team (~20+ devs), GitHub-based, trunk-based development.

---

## Overview

| Field | Value |
|-------|-------|
| **Type** | Greenfield SaaS |
| **Cloud** | GCP |
| **Team Size** | 20+ engineers |
| **VCS** | GitHub |
| **Branching** | Trunk-based development |
| **Status** | Active / In development |

---

## Architecture Summary

```
GitHub (source of truth)
  │
  ├── PR → GitHub Actions
  │         ├── Semgrep (SAST)
  │         ├── Trivy (container + IaC scan)
  │         ├── Checkov (IaC policy)
  │         ├── Gitleaks (secrets detection)
  │         └── CodeRabbit (AI PR review)
  │
  └── Merge to main → Cloud Build
                        └── Build + sign image → Artifact Registry
                              └── Google Cloud Deploy
                                    ├── Staging (auto)
                                    └── Production (canary 25→50→75→100 + approval gate)
                                          └── GKE Autopilot / Cloud Run
```

---

## Stack by Layer

### Compute
| Tool | Purpose |
|------|---------|
| [GKE Autopilot](../domains/gcp-infra.md#gke-autopilot) | Long-running services, stateful workloads |
| [Cloud Run](../domains/gcp-infra.md#cloud-run) | Stateless APIs, event-driven, scale-to-zero |

### CI/CD
| Tool | Purpose |
|------|---------|
| [GitHub Actions](../domains/cicd-devops.md#github-actions) | PR-time quality gates |
| [Cloud Build](../domains/cicd-devops.md#cloud-build) | GCP-native image builds |
| [Google Cloud Deploy](../domains/cicd-devops.md#google-cloud-deploy) | Progressive delivery (canary) |
| [Flux v2](../domains/cicd-devops.md#flux-v2) | GitOps reconciliation (evaluating) |

### IaC
| Tool | Purpose |
|------|---------|
| [OpenTofu](../domains/gcp-infra.md#opentofu) | Infrastructure provisioning |
| [Terragrunt](../domains/gcp-infra.md#terragrunt) | DRY multi-env wrapper (evaluating) |
| [Checkov](../domains/code-quality-security.md#checkov) | IaC policy enforcement |

### Security
| Tool | Purpose |
|------|---------|
| [Semgrep](../domains/code-quality-security.md#semgrep) | SAST / custom rules |
| [Trivy](../domains/code-quality-security.md#trivy) | Container + IaC vulnerability scanning |
| [Gitleaks](../domains/code-quality-security.md#gitleaks) | Secrets detection (pre-commit + CI) |
| [Binary Authorization](../domains/code-quality-security.md#binary-authorization) | Supply chain enforcement (evaluating) |
| [Secret Manager](../domains/gcp-infra.md#secret-manager) | Secrets storage + rotation |

### Database
| Tool | Purpose |
|------|---------|
| [Atlas](../domains/gcp-infra.md#atlas) | Schema migrations (expand-contract pattern) |

### AI Tooling
| Tool | Purpose |
|------|---------|
| [Claude Code](../domains/ai-llm.md#claude-code) | Agentic coding, spec-to-code |
| [GitHub Copilot](../domains/ai-llm.md#github-copilot) | Inline autocomplete + Autofix |
| [CodeRabbit](../domains/ai-llm.md#coderabbit) | AI PR review |
| [LangGraph](../domains/ai-llm.md#langgraph) | Multi-agent pipeline orchestration |
| [LangSmith](../domains/ai-llm.md#langsmith) | LLM observability + evals |

---

## Key Architectural Decisions

### ADR-001: Trunk-Based Development
- **Decision:** All devs commit to `main` via short-lived feature branches (< 1 day)
- **Rationale:** Eliminates merge debt, enables continuous integration, forces feature flags
- **Consequence:** Requires feature flag strategy (LaunchDarkly / GCP Feature Flags)

### ADR-002: No Static Credentials
- **Decision:** All GCP access via Workload Identity Federation
- **Rationale:** Eliminates credential rotation burden and secret leakage risk
- **Consequence:** Slightly more complex initial IAM setup

### ADR-003: Expand-Contract for DB Migrations
- **Decision:** All schema changes via 3-phase expand-contract
- **Rationale:** Zero-downtime deployments with large teams writing concurrent migrations
- **Consequence:** Slower migration cycles — every change is 2–3 deployments

### ADR-004: OpenTofu over Terraform
- **Decision:** Use OpenTofu (OSS fork) instead of HashiCorp Terraform
- **Rationale:** BSL license risk for commercial SaaS; OpenTofu is Linux Foundation backed
- **Consequence:** Slight lag on new Terraform features; mitigated by 1:1 compatibility

---

## Runbooks

- [ ] Canary rollback procedure
- [ ] Secret rotation runbook
- [ ] Atlas migration emergency rollback
- [ ] Gitleaks remediation when secret found in history

---

*Last updated: 2026-03*
