# Template — Tool Entry

> Paste this block into the appropriate `domains/*.md` file. Keep headings at `### ToolName` (H3) — the domain file wraps tools under a single `## Tools` section.

---

### [Tool Name]

| Field | Value |
|-------|-------|
| **Radar** | 🟢 Adopt / 🟡 Trial / 🔴 Hold |
| **Status** | Production-ready / Exploring / Deprecated |
| **Score** | _optional, e.g. 90 / 100_ |
| **Licence** | e.g. MIT, BSD-3, Apache 2.0, LGPL _(flag commercial gotchas)_ |
| **Website** | [link](https://...) |
| **Projects** | e.g. [GCP SaaS Platform](../projects/gcp-saas-platform.md) _— optional_ |

**Why:** One paragraph. What problem does this solve, why it beats alternatives in your context.

**My Pattern:** _(optional — how you actually wire it up)_
- Bullet the pipeline / integration points
- Config defaults you always set

**Code / Config:** _(optional — minimal working snippet)_
```lang
// paste a real snippet you've run, not pseudo-code
```

**Gotchas:**
- Things that burned you or took time to figure out
- Sharp edges a reader should know before adopting

**Alternatives Considered:** _(optional table)_

| Tool | Why I didn't choose it |
|------|----------------------|
| | |

---

## Notes on format

- Root-level files (`frontend-ui.md`) are legacy; canonical entries live under `domains/`.
- After adding a tool, mirror its status into `radar/adopt.md`, `radar/trial.md`, or `radar/hold.md`.
- Update the domain tool count in `README.md` if you're adding/removing entries.
- Date the README (`*Last updated: YYYY-MM*`) when the radar materially changes.
