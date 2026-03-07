# 🔐 Code Quality & Security

> SAST, container scanning, supply chain security, secrets detection, and dependency management.

---

## Tools

---

### Semgrep

| Field | Value |
|-------|-------|
| **Radar** | 🟢 Adopt |
| **Status** | Production-ready |
| **Website** | [semgrep.dev](https://semgrep.dev) |
| **Projects** | [GCP SaaS Platform](../projects/gcp-saas-platform.md) |

**Why:** Best SAST for modern teams. Rules-as-code (YAML), fast, highly customizable. Write org-specific rules that enforce your architecture decisions, not just CVE patterns. Runs in CI without a server.

**My Pattern:**
```yaml
# .github/workflows/semgrep.yaml
- uses: semgrep/semgrep-action@v1
  with:
    config: >-
      p/default
      p/golang
      p/secrets
    auditOn: push
    generateSarif: "1"
```

**Key Concepts:**
- `semgrep --config auto` runs community ruleset
- Write custom rules for: banned functions, required error handling, API auth enforcement
- SARIF output integrates with GitHub Security tab

**Gotchas:**
- False positive rate varies by ruleset — tune aggressively in first 2 weeks
- Don't block PRs on `WARNING` level — only block on `ERROR`
- Custom rules are your competitive moat — invest in them

**Alternatives Considered:**

| Tool | Notes |
|------|-------|
| SonarQube | Heavy server infra, slower feedback loop |
| CodeQL | More powerful but slower; use for nightly scans |
| Snyk | Better for dependency scanning than SAST |

---

### Trivy

| Field | Value |
|-------|-------|
| **Radar** | 🟢 Adopt |
| **Status** | Production-ready |
| **Website** | [trivy.dev](https://trivy.dev) |
| **Projects** | [GCP SaaS Platform](../projects/gcp-saas-platform.md) |

**Why:** Single tool for container images, filesystems, Git repos, IaC, and SBOMs. Replaces 3–4 specialized tools. Fast, accurate, and integrates everywhere.

**My Pattern:**
```yaml
# Scan image before push
- name: Trivy container scan
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: ${{ env.IMAGE }}
    format: sarif
    output: trivy-results.sarif
    severity: CRITICAL,HIGH
    exit-code: 1  # Fail CI on critical findings

# Scan IaC
- name: Trivy IaC scan
  uses: aquasecurity/trivy-action@master
  with:
    scan-type: config
    scan-ref: ./terraform
```

**Gotchas:**
- `exit-code: 1` on HIGH will break CI on popular base images — start with CRITICAL only, then tighten
- Pin base images to digests (not tags) so Trivy results are reproducible
- SBOM generation (`--format cyclonedx`) is worth enabling early — required for compliance later

---

### Checkov

| Field | Value |
|-------|-------|
| **Radar** | 🟢 Adopt |
| **Status** | Production-ready |
| **Website** | [checkov.io](https://checkov.io) |
| **Projects** | [GCP SaaS Platform](../projects/gcp-saas-platform.md) |

**Why:** Policy-as-code for Terraform/OpenTofu and Kubernetes manifests. Catches misconfigurations before `apply` — public buckets, overly permissive IAM, missing encryption, etc.

**My Pattern:**
```bash
# Run in CI before terraform plan
checkov -d ./terraform \
  --framework terraform \
  --check CKV_GCP_* \
  --soft-fail-on LOW,MEDIUM \
  --hard-fail-on HIGH,CRITICAL
```

**Gotchas:**
- Use `.checkov.yaml` to suppress known-acceptable findings with justification comments — avoids alert fatigue
- Combine with Trivy IaC scan — they have complementary rule sets

---

### Gitleaks

| Field | Value |
|-------|-------|
| **Radar** | 🟢 Adopt |
| **Status** | Production-ready |
| **Website** | [gitleaks.io](https://gitleaks.io) |
| **Projects** | [GCP SaaS Platform](../projects/gcp-saas-platform.md) |

**Why:** Detects secrets (API keys, credentials, tokens) committed to Git. Runs as pre-commit hook AND in CI. Catching secrets post-push is already a breach — shift maximally left.

**My Pattern:**
```toml
# .gitleaks.toml
[allowlist]
  description = "Global allowlist"
  regexes = [
    '''EXAMPLE_KEY''',  # Test fixtures
  ]
```

```yaml
# CI step
- name: Gitleaks scan
  uses: gitleaks/gitleaks-action@v2
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

**Pre-commit hook:**
```bash
# Install: brew install gitleaks
# Add to .pre-commit-config.yaml:
- repo: https://github.com/gitleaks/gitleaks
  rev: v8.18.0
  hooks:
    - id: gitleaks
```

**Gotchas:**
- Pre-commit hooks can be skipped with `--no-verify` — CI scan is the safety net
- Configure `allowlist` carefully — noisy false positives get disabled by engineers

**Alternatives Considered:**

| Tool | Notes |
|------|-------|
| TruffleHog | Better at historical commit scanning; use for repo audits |
| detect-secrets (Yelp) | Python-only, narrower scope |

---

### Binary Authorization

| Field | Value |
|-------|-------|
| **Radar** | 🟡 Trial |
| **Status** | Exploring |
| **Website** | [cloud.google.com/binary-authorization](https://cloud.google.com/binary-authorization) |
| **Projects** | [GCP SaaS Platform](../projects/gcp-saas-platform.md) |

**Why Evaluating:** Enforces that only signed container images from Artifact Registry can run on GKE. Closes the supply chain gap — even if an attacker pushes a malicious image, it won't deploy without a valid attestation.

**Key Concepts:**
- Attestors sign images after CI passes (scan + test gate)
- Policy enforces attestations at deploy time
- `dryrun` mode available — use before enforcing

**Gotchas (so far):**
- Increases deploy pipeline complexity — plan signing step in CI before enforcing policy
- Breakglass procedure required for emergencies — document it before enabling enforcement

---

### Renovate

| Field | Value |
|-------|-------|
| **Radar** | 🟡 Trial |
| **Status** | Exploring |
| **Website** | [docs.renovatebot.com](https://docs.renovatebot.com) |
| **Projects** | [GCP SaaS Platform](../projects/gcp-saas-platform.md) |

**Why Evaluating:** Automated dependency updates. More configurable than Dependabot, especially for monorepos. Auto-merge patch updates, require review for minor/major.

**My Config:**
```json
{
  "extends": ["config:base"],
  "automerge": true,
  "automergeType": "pr",
  "packageRules": [
    {
      "matchUpdateTypes": ["patch"],
      "automerge": true
    },
    {
      "matchUpdateTypes": ["major"],
      "automerge": false,
      "reviewers": ["team:platform"]
    }
  ]
}
```

**Alternatives Considered:**

| Tool | Notes |
|------|-------|
| Dependabot | Simpler but less configurable for monorepos |
