# 🎬 Programmatic Video Tools

> Research spike: evaluate 22 free, licence-safe video generation libraries for a SaaS video pipeline.
> Goal: find the right stack with no commercial licence fees (no Remotion, no GSAP SaaS plan).

---

## Overview

| Field | Value |
|-------|-------|
| **Type** | Research / Evaluation Spike |
| **Scope** | 22 libraries, 6 multi-tool pipelines |
| **Status** | Exploring |
| **Live Demo** | [amitrintzler.github.io/programmatic-video-tools](https://amitrintzler.github.io/programmatic-video-tools/) |
| **Comparison Repo** | [github.com/amitrintzler/programmatic-video-tools](https://github.com/amitrintzler/programmatic-video-tools) |

---

## Architecture

```
Data / Script / Prompt
         │
         ▼
┌─────────────────────────────────┐
│  Scene Renderer                 │
│  Python: PIL + Skia / Manim     │
│  TypeScript: Motion Canvas /    │
│    Three.js / D3 + Puppeteer    │
└──────────────┬──────────────────┘
               │ numpy arrays / PNG frames
               ▼
┌─────────────────────────────────┐
│  Video Encoder                  │
│  PyAV (Python) — H.264 CRF-17  │
│  fluent-ffmpeg (Node) — concat  │
└──────────────┬──────────────────┘
               │
               ▼
         MP4 / WebM / GIF
```

---

## Stack Used in Spike

| Tool | Role |
|------|------|
| [PyAV](../domains/video-media.md#pyav) | Frame encoding (H.264, CRF-17) |
| [PIL / Pillow](https://pillow.readthedocs.io) | Frame drawing (UI mockups, HUD, text, compositing) |
| NumPy | Audio synthesis (additive synthesis + Schroeder reverb) |
| [Manim CE](../domains/video-media.md#manim-ce) | Math/diagram animation scenes |
| [Motion Canvas](../domains/video-media.md#motion-canvas) | TypeScript declarative scene rendering |
| [fluent-ffmpeg](../domains/video-media.md#fluent-ffmpeg) | Clip concatenation and audio muxing |
| [Skia-Python](../domains/video-media.md#skia-python) | Chrome-quality 2D frame rendering |
| [Three.js](../domains/video-media.md#threejs-headless) | GPU-accelerated 3D scenes via Puppeteer |

---

## Key Findings

| Question | Answer |
|----------|--------|
| Best all-round Python encoder | **PyAV** (score 97) — frame-accurate, GPU-ready, BSD-3 |
| Best TypeScript declarative | **Motion Canvas** (score 93) — MIT, real-time preview |
| Best for math/explainers | **Manim CE** (score 94) — LaTeX-first, MIT |
| Best for data visualisation | **D3.js + Puppeteer** (score 90) — ISC, any chart type |
| Best 3D | **Three.js headless** (score 92) — MIT, GPU-accelerated |
| Avoid for commercial SaaS | Remotion (commercial), LibOpenShot (LGPL-3), ProjectM (LGPL), p5.js (LGPL-2.1) |

---

## Render Performance (1280×720, 30fps, M2 Pro)

| Tool | 10-sec clip | 60-sec clip |
|------|-------------|-------------|
| PyAV + PIL | ~8 s | ~48 s |
| PyAV + Skia | ~10 s | ~58 s |
| Manim CE | ~45 s | ~4.5 min |
| Motion Canvas | ~12 s | ~72 s |
| Three.js + Puppeteer | ~18 s | ~105 s |
| D3 + Puppeteer | ~25 s | ~2.5 min |

---

## Deliverables

| Deliverable | Notes |
|-------------|-------|
| [Live comparison site](https://amitrintzler.github.io/programmatic-video-tools/) | Side-by-side card layout, filter by language/score |
| 22 individual tool demo clips | `videos/ultra-*.mp4` |
| 6 multi-tool mega pipeline demos | `videos/mega-*.mp4` |
| 90-second hero reel | `videos/THE-BUILD-REEL-v3.mp4` |

---

## Mega Pipelines Evaluated

### 1. Cartoon Story
`Manim + PyAV + PIL` — Scene graph → frame extraction → PIL composite → H.264. 2-min 1080p in ~4 min on M2 Pro.

### 2. Action Movie
`Skia-Python + PyAV + NumPy audio` — GPU 2D renders with synthesised audio (additive synthesis + Schroeder reverb).

### 3. Long-Form Math
`Manim CE + FFmpeg concat` — Renders sections independently, stitches with chapter markers. Handles 20+ min without RAM overflow.

### 4. Data Documentary
`D3 + Puppeteer → FFmpeg → MoviePy` — Data-bound animations captured frame-by-frame → narration overlay.

### 5. Four Cartoon Styles
`Manim × 4 passes → MoviePy` — Same scene, 4 colour themes → 2×2 grid composite.

### 6. Limits Demo
`PyAV + PIL` — 4K, 120fps, HDR (BT.2020), transparent WebM (VP9 + alpha channel).

---

## Key Architectural Decisions

### ADR-V001: PyAV as encoding layer
- **Decision:** All Python generation pipelines use PyAV as the final encoder
- **Rationale:** Lowest overhead path to H.264; GPU encode available; BSD-3 licence
- **Consequence:** Frame rendering must produce numpy arrays — constrains renderer choice to PIL, Skia, NumPy

### ADR-V002: Motion Canvas for TypeScript pipelines
- **Decision:** Motion Canvas over Remotion
- **Rationale:** MIT licence — no commercial fee. Generator-based timeline is more readable than React-based hooks. Real-time preview improves iteration speed.
- **Consequence:** TypeScript-only; no React component reuse with Remotion

### ADR-V003: No LGPL-licenced libraries
- **Decision:** Exclude LibOpenShot, ProjectM, p5.js from production stack
- **Rationale:** LGPL-3/LGPL-2.1 create linking obligations that complicate closed-source SaaS distribution
- **Consequence:** Narrower library selection — mitigated by PyAV + Motion Canvas covering all major use cases

---

## Next Steps

- [ ] Wrap PyAV + PIL into a thin Python service for the SaaS pipeline (Cloud Run)
- [ ] Evaluate Motion Canvas cloud render (Revideo) for bulk personalised video generation
- [ ] Add GPU encode path (NVENC) for Cloud Run GPU instances → target <5 s for 10-sec clip
- [ ] Integrate with screen recording / screenshot capture for automated product demo generation
- [ ] Benchmark 4K H.265 encode on GKE Autopilot GPU node pool

---

*Last updated: 2026-03*
