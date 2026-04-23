# 🗂️ My Tech Stack Index

> Personal reference of tools I've explored, evaluated, and use in production.
> Structured as a **Tech Radar** — updated as my stack evolves.

---

## 📡 Radar at a Glance

Full radar lists: [🟢 Adopt](radar/adopt.md) · [🟡 Trial](radar/trial.md) · [🔴 Hold](radar/hold.md)

| Domain | 🟢 Adopt | 🟡 Trial | 🔴 Hold |
|--------|----------|---------|--------|
| **AI / LLM** | Claude Code, GitHub Copilot, CodeRabbit | LangGraph, LangSmith, Braintrust, Karpathy Skills | — |
| **CI/CD** | GitHub Actions, Google Cloud Deploy | Flux v2, Cloud Build | Jenkins |
| **GCP Infra** | GKE Autopilot, Cloud Run, OpenTofu, Secret Manager | Terragrunt, Atlas | Terraform, SA Key Files, VPC Connector |
| **Code Quality & Security** | Semgrep, Trivy, Checkov, Gitleaks | Binary Authorization, Renovate | SonarQube |
| **Video / Media** | FFmpeg, PyAV, MoviePy, Manim CE, Motion Canvas, Three.js, fluent-ffmpeg, D3.js, Anime.js, PixiJS, Video.js | Plyr, Shaka, MediaPipe, Revideo, **HyperFrames**, Skia-Python, GStreamer, Vispy, Movis, Matplotlib Animation, Lottie, p5.js, Rive, Editly | Remotion, LibOpenShot, ProjectM, Pytoon |

---

## 🗂️ Domain Index

| Domain | File | Tool Count |
|--------|------|-----------|
| AI / LLM Tooling | [domains/ai-llm.md](domains/ai-llm.md) | 7 |
| CI/CD & DevOps | [domains/cicd-devops.md](domains/cicd-devops.md) | 4 |
| GCP Infrastructure | [domains/gcp-infra.md](domains/gcp-infra.md) | 6 |
| Code Quality & Security | [domains/code-quality-security.md](domains/code-quality-security.md) | 6 |
| Video & Media | [domains/video-media.md](domains/video-media.md) | 29 |
| Frontend & UI _(scaffolding)_ | [frontend-ui.md](frontend-ui.md) | 7 |

---

## 📁 Projects Index

| Project | Description | File |
|---------|-------------|------|
| GCP SaaS Platform | Greenfield multi-tenant SaaS on GCP | [projects/gcp-saas-platform.md](projects/gcp-saas-platform.md) |
| Programmatic Video Tools | Research spike: video libraries for SaaS pipeline | [projects/programmatic-video-tools.md](projects/programmatic-video-tools.md) |

---

## 🔖 Radar Legend

| Symbol | Meaning |
|--------|---------|
| 🟢 **Adopt** | Confident. Use this. Proven in my context. |
| 🟡 **Trial** | Promising. Actively evaluating. |
| 🔴 **Hold** | Proceed with caution or avoid for new work. |

| Badge | Meaning |
|-------|---------|
| `Production-ready` | Running in production or ready to be |
| `Exploring` | Being evaluated, not yet in prod |
| `Deprecated` | Replaced or phased out |

---

## ➕ Adding a Tool

Use [TEMPLATE.md](TEMPLATE.md) to add a new tool entry in the appropriate [domains/](domains/) file. Then update [radar/](radar/) if its status is Adopt / Trial / Hold.

---

*Last updated: 2026-04*
