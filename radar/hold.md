# 🔴 Hold

> Tools to avoid for new work. Either superseded, risky, or not worth the tradeoff.

| Tool | Domain | Reason |
|------|--------|--------|
| Terraform (HashiCorp) | IaC | BSL license risk for commercial SaaS → replaced by OpenTofu |
| Jenkins | CI/CD | Operational overhead not justified for greenfield |
| SonarQube | SAST | Heavy server infra, slower feedback → replaced by Semgrep |
| Serverless VPC Connector | GCP Infra | Legacy; use Direct VPC egress (gen2) instead |
| SA Key Files | GCP Infra | Static credentials anti-pattern → use Workload Identity Federation |
| Env var secrets | GCP Infra | Defeats audit logging → use Secret Manager CSI driver |

---

> Add tools here when they're superseded or after a failed trial.
