# ☁️ GCP Infrastructure

> Compute, IaC, secrets, networking, and database tooling on Google Cloud Platform.

---

## Tools

---

### GKE Autopilot

| Field | Value |
|-------|-------|
| **Radar** | 🟢 Adopt |
| **Status** | Production-ready |
| **Website** | [cloud.google.com/kubernetes-engine/docs/concepts/autopilot-overview](https://cloud.google.com/kubernetes-engine/docs/concepts/autopilot-overview) |
| **Projects** | [GCP SaaS Platform](../projects/gcp-saas-platform.md) |

**Why:** No node management overhead. Workload Identity built-in. GKE-managed security baseline. Right-sized billing per pod. Default choice for all stateless workloads.

**Key Concepts:**
- No node pools — just deploy pods, GCP handles the rest
- Workload Identity Federation replaces service account key files
- `ResourceRequests` are mandatory — Autopilot enforces them (good practice anyway)
- Not all workloads fit: DaemonSets, privileged containers, and some custom CNIs don't work

**My Pattern:**
```yaml
# Workload Identity annotation (required)
apiVersion: v1
kind: ServiceAccount
metadata:
  name: my-service
  annotations:
    iam.gke.io/gcp-service-account: my-service@PROJECT.iam.gserviceaccount.com
```

**Gotchas:**
- Cold start on scale-from-zero is ~30–60s — use PodDisruptionBudgets and minReplicas > 0 for latency-sensitive services
- Spot/preemptible nodes available but pods can be evicted — only for fault-tolerant batch workloads
- Autopilot applies its own resource limits — test locally with Standard cluster if behavior is unexpected

---

### Cloud Run

| Field | Value |
|-------|-------|
| **Radar** | 🟢 Adopt |
| **Status** | Production-ready |
| **Website** | [cloud.google.com/run](https://cloud.google.com/run) |
| **Projects** | [GCP SaaS Platform](../projects/gcp-saas-platform.md) |

**Why:** True scale-to-zero, sub-minute cold start, no cluster to manage. Best for stateless services, event-driven workloads, and internal APIs. Billing only for actual request time.

**My Pattern:**
```yaml
# service.yaml
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: my-service
spec:
  template:
    metadata:
      annotations:
        autoscaling.knative.dev/minScale: "1"
        autoscaling.knative.dev/maxScale: "100"
        run.googleapis.com/execution-environment: gen2
    spec:
      serviceAccountName: my-service@PROJECT.iam.gserviceaccount.com
      containers:
        - image: REGION-docker.pkg.dev/PROJECT/REPO/my-service:TAG
          resources:
            limits:
              cpu: "2"
              memory: 512Mi
```

**Gotchas:**
- Stateless only — don't store anything on the filesystem except `/tmp`
- Max request timeout is 60 minutes — not suitable for very long-running jobs (use Cloud Run Jobs instead)
- VPC egress adds latency — use Direct VPC egress (gen2) not the legacy Serverless VPC Connector

---

### OpenTofu

| Field | Value |
|-------|-------|
| **Radar** | 🟢 Adopt |
| **Status** | Production-ready |
| **Website** | [opentofu.org](https://opentofu.org) |
| **Projects** | [GCP SaaS Platform](../projects/gcp-saas-platform.md) |

**Why:** OSS drop-in replacement for Terraform (post-BSL license change). 1:1 compatible. Backed by Linux Foundation. Avoids HashiCorp license risk for commercial products.

**Key Concepts:**
- State stored in GCS bucket with object versioning + locking via Firestore or GCS
- Use `tofu` CLI — same commands as `terraform`
- Provider ecosystem fully compatible

**Gotchas:**
- Still catching up on some Terraform Enterprise features — check feature parity if migrating from TFE
- Remote state locking with GCS is eventually consistent — plan for rare lock contention

**Alternatives Considered:**

| Tool | Notes |
|------|-------|
| Terraform (HashiCorp) | BSL license risk for SaaS products |
| Pulumi | More flexible (real languages) but steeper learning curve |

---

### Terragrunt

| Field | Value |
|-------|-------|
| **Radar** | 🟡 Trial |
| **Status** | Exploring |
| **Website** | [terragrunt.gruntwork.io](https://terragrunt.gruntwork.io) |
| **Projects** | [GCP SaaS Platform](../projects/gcp-saas-platform.md) |

**Why Evaluating:** DRY wrapper for OpenTofu. Eliminates repeated backend config and provider blocks across environments. Essential for multi-env setups (dev/staging/prod).

**Key Concepts:**
- `terragrunt.hcl` per module = environment-specific config
- Root `terragrunt.hcl` = shared backend + provider config
- `run-all` command = apply across all modules in dependency order

**Gotchas (so far):**
- Adds another abstraction layer — ensure team understands what Terragrunt generates
- Dependency graph can get complex — document it in your projects/ folder

---

### Secret Manager

| Field | Value |
|-------|-------|
| **Radar** | 🟢 Adopt |
| **Status** | Production-ready |
| **Website** | [cloud.google.com/secret-manager](https://cloud.google.com/secret-manager) |
| **Projects** | [GCP SaaS Platform](../projects/gcp-saas-platform.md) |

**Why:** GCP-native secrets store. Integrated with Workload Identity — no credential files. Automatic versioning, rotation support, and audit logging.

**My Pattern:** Always use the **Secret Manager CSI driver** for Kubernetes — mounts secrets as files, never as env vars.
```yaml
volumes:
  - name: secrets
    csi:
      driver: secrets-store.csi.k8s.io
      readOnly: true
      volumeAttributes:
        secretProviderClass: my-service-secrets
```

**Gotchas:**
- Env var injection (`envFrom`) defeats audit logging — avoid it
- Secret rotation requires app restart unless using the CSI driver with `autorotation` enabled

---

### Atlas

| Field | Value |
|-------|-------|
| **Radar** | 🟡 Trial |
| **Status** | Exploring |
| **Website** | [atlasgo.io](https://atlasgo.io) |
| **Projects** | [GCP SaaS Platform](../projects/gcp-saas-platform.md) |

**Why Evaluating:** Schema-as-code for database migrations. Declarative (define desired state, Atlas generates migration). Supports PostgreSQL, MySQL, and more. CI integration for migration linting.

**Key Concepts:**
- `atlas schema inspect` → capture current state
- `atlas migrate diff` → generate migration from schema delta
- `atlas migrate lint` → catch destructive changes in CI
- Pair with **expand-contract pattern** for zero-downtime migrations

**My Pattern (expand-contract):**
```
Phase 1 (Expand):  Add new column as nullable → deploy app v2 (writes both)
Phase 2 (Migrate): Backfill data → make column NOT NULL
Phase 3 (Contract): Remove old column → deploy app v3
```

**Gotchas (so far):**
- Schema drift detection requires Atlas Cloud or local state file — plan this in your CI
- Terraform provider available (`ariga/atlas`) — integrates migration into IaC pipeline
