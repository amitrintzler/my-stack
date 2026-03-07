# ⚙️ CI/CD & DevOps

> Pipeline orchestration, deployment strategies, and GitOps tooling.

---

## Tools

---

### GitHub Actions

| Field | Value |
|-------|-------|
| **Radar** | 🟢 Adopt |
| **Status** | Production-ready |
| **Website** | [github.com/features/actions](https://github.com/features/actions) |
| **Projects** | [GCP SaaS Platform](../projects/gcp-saas-platform.md) |

**Why:** Best ecosystem for AI agent integration (Claude Code, Copilot Autofix, CodeRabbit). Widest marketplace. Use for all PR-time workflows — lint, test, scan, review.

**My Pattern:**
```yaml
# .github/workflows/pr.yaml
on: [pull_request]
jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Semgrep scan
        uses: semgrep/semgrep-action@v1
      - name: Trivy scan
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: fs
```

**Gotchas:**
- Use `GITHUB_TOKEN` with least privilege — scope per job, not per workflow
- Cache dependencies aggressively; cold runs on large monorepos are slow
- Reusable workflows (`.github/workflows/reusable-*.yaml`) are underused — kill duplication early

**Alternatives Considered:**

| Tool | Why I didn't choose it |
|------|----------------------|
| GitLab CI | Vendor lock-in, team already on GitHub |
| CircleCI | Less GCP-native integration |
| Jenkins | Operational overhead not worth it for greenfield |

---

### Google Cloud Deploy

| Field | Value |
|-------|-------|
| **Radar** | 🟢 Adopt |
| **Status** | Production-ready |
| **Website** | [cloud.google.com/deploy](https://cloud.google.com/deploy) |
| **Projects** | [GCP SaaS Platform](../projects/gcp-saas-platform.md) |

**Why:** Managed progressive delivery with built-in canary/blue-green, approval gates, and rollback. Native GCP IAM — no extra auth layer. Integrates directly with GKE and Cloud Run.

**My Pattern:**
```yaml
# clouddeploy.yaml
apiVersion: deploy.cloud.google.com/v1
kind: DeliveryPipeline
metadata:
  name: my-service-pipeline
serialPipeline:
  stages:
    - targetId: staging
      profiles: [staging]
    - targetId: production
      profiles: [production]
      strategy:
        canary:
          runtimeConfig:
            kubernetes:
              gatewayServiceMesh:
                httpRoute: my-route
          canaryDeployment:
            percentages: [25, 50, 75]
            verify: true
```

**Gotchas:**
- `verify` step (post-deploy validation) needs a Skaffold verify config — plan this upfront
- Approval gates are per-target, not per-pipeline stage — model your environments accordingly
- Rollback is one CLI command but plan your DB migration strategy separately (expand-contract)

**Alternatives Considered:**

| Tool | Why I didn't choose it |
|------|----------------------|
| Spinnaker | Heavyweight, significant ops burden |
| ArgoRollouts | Viable but requires ArgoCD coupling |
| Manual kubectl | No auditability, no progressive delivery |

---

### Flux v2

| Field | Value |
|-------|-------|
| **Radar** | 🟡 Trial |
| **Status** | Exploring |
| **Website** | [fluxcd.io](https://fluxcd.io) |
| **Projects** | [GCP SaaS Platform](../projects/gcp-saas-platform.md) |

**Why Evaluating:** Lightweight GitOps for GKE. Pull-based model fits security posture better than push. Smaller footprint than ArgoCD. Native Kustomize support.

**Key Concepts:**
- `GitRepository` → source of truth
- `Kustomization` → what gets reconciled and where
- `HelmRelease` → for Helm-managed components
- Flux controllers run in-cluster — no external access needed

**Gotchas (so far):**
- Multi-tenancy model (path-based isolation) requires careful RBAC planning
- Notifications to Slack/PagerDuty need the notification controller configured separately

**Alternatives Considered:**

| Tool | Why I didn't choose it (yet) |
|------|----------------------|
| ArgoCD | Heavier, but better UI — still on the table for multi-cluster |

---

### Cloud Build

| Field | Value |
|-------|-------|
| **Radar** | 🟡 Trial |
| **Status** | Exploring |
| **Website** | [cloud.google.com/build](https://cloud.google.com/build) |
| **Projects** | [GCP SaaS Platform](../projects/gcp-saas-platform.md) |

**Why:** Used for GCP-native build steps — container image builds, pushing to Artifact Registry, triggering Cloud Deploy. Runs inside GCP VPC with no outbound credential exposure.

**My Pattern:** Triggered by GitHub Actions via `gcloud builds submit`, not as a standalone pipeline. Handles the GCP-side build steps that benefit from VPC-native access.

**Gotchas:**
- Substitution variables have a verbose syntax (`$_VAR`) — easy to mix up with shell vars
- Default service account has broad permissions — scope it down per trigger
