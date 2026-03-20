# Design: Video Catalog — Interactive HTML Comparison Page

**Date:** 2026-03-19
**Status:** Approved
**Replaces:** Original markdown-only design (same file, revised scope)

---

## Goal

Build a self-contained interactive HTML comparison page for all video tools in the catalog, served via GitHub Pages from the `my-stack` repo. Same aesthetic as the existing `ultra-video-tool-comparison.html` (dark theme, card grid, filter bar, scores).

Total tools: **28** (11 existing with demo videos + 17 new with code snippets only).

---

## Scope

### All 28 Tools (11 existing + 17 new)

**Players & Playback**
- Video.js (🟢 88), Plyr (🟡 82), Shaka Player (🟡 85)

**Processing & Pipelines**
- FFmpeg (🟢 95), MediaPipe (🟡 83)

**Programmatic Generation — Adopt**
- PyAV (🟢 97), Manim CE (🟢 94), Motion Canvas (🟢 93), Three.js headless (🟢 92), MoviePy (🟢 91), fluent-ffmpeg (🟢 91), D3.js (🟢 90), Anime.js (🟢 86), PixiJS (🟢 87)

**Programmatic Generation — Trial**
- Revideo (🟡 90), Skia-Python (🟡 88), GStreamer (🟡 87), Lottie-Web (🟡 78), Rive (🟡 80), Vispy (🟡 75), Movis (🟡 72), Matplotlib Animation (🟡 74), Editly (🟡 77), p5.js (🟡 72)

**Hold**
- Remotion (🔴 — commercial licence), LibOpenShot (🔴 — LGPL-3), ProjectM (🔴 — LGPL), Pytoon (🔴 — pre-alpha)

---

## Output File

`docs/video-tools.html` — single self-contained file, no external dependencies (all CSS + JS inline).

---

## GitHub Pages Setup

- Enable GitHub Pages on `my-stack` repo, serving from `main` branch `/docs` folder
- Page URL: `https://amitrintzler.github.io/my-stack/video-tools.html`

---

## Page Structure

```
Header
  Title: "Video & Media Tools"
  Subtitle: "28 tools evaluated for programmatic video generation"
  Stats bar: total tools / adopt count / trial count / hold count

Filter Bar
  By language:   All | Python | TypeScript | JavaScript
  By radar:      All | 🟢 Adopt | 🟡 Trial | 🔴 Hold
  By capability: All | Video | Audio | 3D | Data Viz | ML | Cloud (filter label matches matrix column "Cloud")

Card Grid (responsive, 2-col on wide, 1-col on narrow)
  Each card:
    - Tool name + score badge (top right)
    - Radar pill (Adopt / Trial / Hold)
    - Language tag(s)
    - Code snippet panel (syntax-highlighted, scrollable, max ~20 lines)
    - Capability dots row (filled = yes, empty = no)
    - Licence tag (colour-coded: green=permissive, amber=LGPL, red=commercial)
    - Links row: Website → | GitHub → | (Demo video → for the 11 existing tools)
    - Hold cards: show licence warning banner instead of code snippet
```

---

## Code Snippet Format

Each card shows the most useful minimal example for that tool — same examples as in `domains/video-media.md`. Syntax highlighting via a small inline Prism.js bundle (Python + JS/TS only — keeps size minimal).

For the 11 tools that have demo videos in `programmatic-video-tools`, a "▶ Demo video" link points to `https://amitrintzler.github.io/programmatic-video-tools/`.

---

## Card Capabilities Matrix

| Tool | Video | Audio | 3D | Data Viz | ML | Cloud |
|------|-------|----|----|----|----|----|
| PyAV | ● | ● | ○ | ○ | ○ | ● |
| Manim CE | ● | ○ | ○ | ● | ○ | ● |
| Motion Canvas | ● | ○ | ○ | ● | ○ | ● |
| Three.js | ● | ○ | ● | ○ | ○ | ● |
| fluent-ffmpeg | ● | ● | ○ | ○ | ○ | ● |
| MoviePy | ● | ● | ○ | ○ | ○ | ● |
| D3.js | ● | ○ | ○ | ● | ○ | ● |
| FFmpeg | ● | ● | ○ | ○ | ○ | ● |
| MediaPipe | ○ | ○ | ○ | ○ | ● | ● |
| Video.js | ● | ● | ○ | ○ | ○ | ● |
| Shaka Player | ● | ● | ○ | ○ | ○ | ● |
| Plyr | ● | ● | ○ | ○ | ○ | ● |
| Anime.js | ● | ○ | ○ | ○ | ○ | ● |
| PixiJS | ● | ○ | ○ | ○ | ○ | ● |
| Revideo | ● | ● | ○ | ● | ○ | ● |
| Skia-Python | ● | ○ | ○ | ○ | ○ | ● |
| GStreamer | ● | ● | ○ | ○ | ○ | ● |
| Lottie-Web | ● | ○ | ○ | ○ | ○ | ● |
| Rive | ● | ○ | ○ | ○ | ○ | ○ |
| Vispy | ● | ○ | ● | ● | ○ | ○ |
| Movis | ● | ● | ○ | ○ | ○ | ○ |
| Matplotlib Anim | ● | ○ | ○ | ● | ○ | ● |
| Editly | ● | ● | ○ | ○ | ○ | ● |
| p5.js | ● | ○ | ○ | ○ | ○ | ● |
| Remotion | ● | ● | ○ | ● | ○ | ● |
| LibOpenShot | ● | ● | ○ | ○ | ○ | ○ |
| ProjectM | ● | ○ | ● | ○ | ○ | ○ |
| Pytoon | ● | ○ | ○ | ○ | ○ | ○ |

---

## Design Aesthetic (matching existing comparison page)

- Background: `#0a0a1a`
- Card background: `#12122a`
- Card border: `#2a2a4a`
- Accent: `#4ecdc4`
- Title gradient: `#4ecdc4 → #ff6b6b → #ffd93d`
- Score badge colour is independent of radar status (a tool can be Adopt with a mid-range score badge): high (≥90): `#4ecdc4`; mid (75-89): `#ffd93d`; low (<75): `#ff6b6b`
- Radar pill colour is always based on radar status (Adopt=green, Trial=amber, Hold=red), not score
- Hover: lift + teal glow shadow
- Font: system-ui stack

---

## Out of Scope

- Actual video file generation for the 17 new tools
- Changes to `domains/video-media.md` (separate task if desired)
- Other domain HTML pages (this is video only)
