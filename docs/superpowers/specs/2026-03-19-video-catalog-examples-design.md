# Design: Video Catalog Examples — Extend domains/video-media.md

**Date:** 2026-03-19
**Status:** Approved

---

## Goal

Extend `domains/video-media.md` with rich code examples for all 17 tools currently missing from that file. The root `video-media.md` serves as the broad catalog; `domains/video-media.md` is the deep-dive implementation reference.

---

## Scope

### Tools to Add (17 total)

**Players & Playback (new section)**
- Video.js — web player, HLS/DASH, plugin ecosystem
- Plyr — lightweight player, YouTube/Vimeo embeds
- Shaka Player — adaptive streaming, DRM (Widevine/PlayReady/FairPlay)

**Processing & Pipelines (new section)**
- FFmpeg — CLI wrapper patterns (subprocess Python, fluent-ffmpeg Node)
- MediaPipe — real-time ML on video (pose, face, hand tracking)

**Programmatic Generation (additions to existing section)**
- Anime.js — DOM/SVG/CSS timeline animations, Puppeteer capture
- PixiJS — WebGL 2D, sprites, GPU filters, Puppeteer capture
- Lottie-Web — AE JSON animations in browser
- p5.js — creative coding sketches (LGPL-2.1 warning)
- Rive — state machine animations (editor closed-source warning)
- Vispy — OpenGL scientific viz, point clouds
- Movis — After Effects-style Python compositing
- Matplotlib Animation — chart animation via FuncAnimation + FFMpegWriter
- Editly — declarative JSON video editing (Node.js)

**Hold (new section, abbreviated)**
- LibOpenShot — LGPL-3 warning, redirect to alternatives
- ProjectM — LGPL warning, redirect
- Pytoon — pre-alpha warning, redirect

---

## Entry Format

Each entry follows the established pattern from existing tools:

```markdown
### ToolName

| Field | Value |
| Radar | 🟢/🟡/🔴 |
| Status | ... |
| Score | N / 100 |
| Licence | ... |
| Website | ... |
| Projects | [Programmatic Video Tools](../projects/programmatic-video-tools.md) |

**Why:** / **Why Evaluating:** / **Why Hold:** paragraph

**My Pattern:** bullet points (omitted for Hold entries)

**[Descriptive heading]:**
```code snippet```

**Gotchas:** bullet points

**Alternatives Considered:** table (omitted for Hold entries)
```

Hold entries use the Remotion pattern: licence warning block + redirect table, minimal code. Hold entries omit Score, My Pattern, and Alternatives Considered.

---

## Score Assignments

| Tool | Score |
|------|-------|
| FFmpeg | 95 |
| Video.js | 88 |
| Shaka Player | 85 |
| Plyr | 82 |
| MediaPipe | 83 |
| Anime.js | 86 |
| PixiJS | 87 |
| Lottie-Web | 78 |
| Rive | 80 |
| Vispy | 75 |
| Movis | 72 |
| Matplotlib Animation | 74 |
| Editly | 77 |
| p5.js | 72 |

---

## File Structure After Changes

The current file has a single flat `## Tools` section with 11 tools. This restructuring:
- Renames `## Tools` → `## Programmatic Generation`
- Adds three new top-level sections: `## Players & Playback`, `## Processing & Pipelines`, `## Hold`
- Moves the existing `### Remotion` entry from `## Programmatic Generation` into `## Hold`
- Keeps `### fluent-ffmpeg` in `## Programmatic Generation` (it is a Node.js wrapper, not a CLI tool — distinct from the new `### FFmpeg` entry in Processing)
- Updates the H1 title from `# 🎬 Video & Media — Programmatic Generation` to `# 🎬 Video & Media` and updates the intro blockquote to reflect the broader scope
- Updates the header licence warning list to include new entries with licence concerns (p5.js LGPL-2.1 already present; add Rive closed-source editor, ProjectM LGPL, LibOpenShot LGPL-3 already present)

```
domains/video-media.md
  ## Players & Playback        ← NEW SECTION
    ### Video.js
    ### Plyr
    ### Shaka Player
  ## Processing & Pipelines    ← NEW SECTION
    ### FFmpeg
    ### MediaPipe
  ## Programmatic Generation   ← RENAMED from "## Tools"
    ### PyAV                   ← existing
    ### Manim CE               ← existing
    ### Motion Canvas          ← existing
    ### fluent-ffmpeg          ← existing (stays here, not moved to Processing)
    ### MoviePy                ← existing
    ### Three.js (headless)    ← existing
    ### Revideo                ← existing
    ### Skia-Python            ← existing
    ### GStreamer               ← existing
    ### D3.js                  ← existing
    ### Anime.js               ← NEW
    ### PixiJS                 ← NEW
    ### Lottie-Web             ← NEW
    ### p5.js                  ← NEW
    ### Rive                   ← NEW
    ### Vispy                  ← NEW
    ### Movis                  ← NEW
    ### Matplotlib Animation   ← NEW
    ### Editly                 ← NEW
  ## Hold                      ← NEW SECTION
    ### Remotion               ← MOVED from Programmatic Generation
    ### LibOpenShot            ← NEW
    ### ProjectM               ← NEW
    ### Pytoon                 ← NEW
```

---

## Out of Scope

- Changes to root `video-media.md`
- Changes to `projects/programmatic-video-tools.md`
- New files or per-tool files
