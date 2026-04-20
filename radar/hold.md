# 🔴 Hold

> Proceed with caution or avoid for new work. Licence, maintenance, or fitness concerns.

| Tool | Domain | Reason |
|------|--------|--------|
| Terraform (HashiCorp) | IaC | BSL license risk for commercial SaaS → replaced by OpenTofu |
| Jenkins | CI/CD | Operational overhead not justified for greenfield |
| SonarQube | SAST | Heavy server infra, slower feedback → replaced by Semgrep |
| Serverless VPC Connector | GCP Infra | Legacy; use Direct VPC egress (gen2) instead |
| SA Key Files | GCP Infra | Static credentials anti-pattern → use Workload Identity Federation |
| Env var secrets | GCP Infra | Defeats audit logging → use Secret Manager CSI driver |
| [Remotion](../domains/video-media.md#remotion) | Video/Media | ⚠️ Commercial licence required for SaaS ($1,500+/yr) — use Motion Canvas, Revideo, or HyperFrames |
| [LibOpenShot](../domains/video-media.md#libopenshot) | Video/Media | LGPL-3 linking restrictions complicate commercial SaaS; fragile Python API |
| [ProjectM](../domains/video-media.md#projectm) | Video/Media | LGPL + C++ heavy, no Python-friendly frame capture path |
| [Pytoon](../domains/video-media.md#pytoon) | Video/Media | Pre-alpha, unstable API, no production usage evidence |

---

> Add tools here when they're superseded or after a failed trial.
