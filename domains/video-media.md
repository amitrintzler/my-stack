# 🎬 Video & Media

> Libraries and tools for video processing, playback, programmatic generation, and media pipelines.

---

## Players & Playback

---

## FFmpeg

| Field | Value |
|-------|-------|
| **Link** | [ffmpeg.org](https://ffmpeg.org) |
| **Use Case** | Transcoding, thumbnail generation, stream processing, pipeline glue |
| **Radar** | 🟢 Adopt |
| **Status** | Production-ready |

**Pros:**
- Universal codec support (H.264, H.265, VP9, AV1, ProRes, WebM)
- Runs anywhere — Linux, macOS, Docker, Cloud Run, Lambda
- Powerful filter graph for compositing, scaling, colour grading

**Cons:**
- CLI-only — wrap with fluent-ffmpeg (Node) or subprocess (Python)
- Filter graph syntax is complex for advanced pipelines

---

## fluent-ffmpeg

| Field | Value |
|-------|-------|
| **Radar** | 🟢 Adopt |
| **Status** | Production-ready |
| **Score** | 91 / 100 |
| **Licence** | MIT |
| **Website** | [github.com/fluent-ffmpeg/node-fluent-ffmpeg](https://github.com/fluent-ffmpeg/node-fluent-ffmpeg) |
| **Projects** | [Programmatic Video Tools](../projects/programmatic-video-tools.md) |

**Why:** The standard Node.js pipeline layer. Wraps FFmpeg's filter graph in a chainable API. Used to concatenate clips from Motion Canvas/Three.js renders, mux background audio, apply colour grades, and produce the final deliverable.

**My Pattern:**
- Motion Canvas renders individual scenes to MP4 → fluent-ffmpeg concatenates with `concat` filter
- Background music: `volume=0.3` audio filter on music track
- Final encode: `-c:v libx264 -crf 18 -c:a aac -b:a 256k`

**Concat + audio mix:**
```js
import ffmpeg from 'fluent-ffmpeg';

ffmpeg()
  .input('scene1.mp4')
  .input('scene2.mp4')
  .input('background.mp3')
  .complexFilter([
    '[0:v][1:v]concat=n=2:v=1:a=0[v]',
    '[2:a]volume=0.3[music]',
  ])
  .outputOptions([
    '-map [v]', '-map [music]', '-shortest',
    '-c:v libx264', '-crf 18',
    '-c:a aac', '-b:a 256k',
  ])
  .output('final.mp4')
  .run();
```

**Gotchas:**
- `concat` filter requires same resolution and framerate on all inputs — normalise first
- `-shortest` cuts to the shortest stream — omit if music should loop to video length
- Use `-an` on video inputs when audio is handled separately

---

## Video.js

| Field | Value |
|-------|-------|
| **Link** | [videojs.com](https://videojs.com) |
| **Use Case** | Web video player, HLS/DASH playback, custom UI skin |
| **Radar** | 🟢 Adopt |
| **Status** | Production-ready |

**Pros:**
- Largest community of any open-source HTML5 player
- Rich plugin ecosystem (ads, analytics, thumbnails, chapters)
- HLS/DASH via hls.js / videojs-contrib-eme

**Cons:**
- Heavier than Plyr for simple use cases
- Default skin needs heavy CSS override for custom branding

---

## Plyr

| Field | Value |
|-------|-------|
| **Link** | [plyr.io](https://plyr.io) |
| **Use Case** | Lightweight customisable HTML5/YouTube/Vimeo player |
| **Radar** | 🟡 Trial |
| **Status** | Exploring |

**Pros:**
- Very clean API, easy to brand
- YouTube and Vimeo embeds work out of the box
- Small bundle size

**Cons:**
- Less mature HLS/DASH support than Video.js
- Smaller plugin ecosystem

---

## Shaka Player

| Field | Value |
|-------|-------|
| **Link** | [github.com/shaka-project/shaka-player](https://github.com/shaka-project/shaka-player) |
| **Use Case** | Adaptive streaming (HLS/DASH), DRM (Widevine, PlayReady, FairPlay) |
| **Radar** | 🟡 Trial |
| **Status** | Exploring |

**Pros:**
- Best-in-class DASH + DRM support (Google-backed)
- Handles live streams and low-latency DASH
- Works with Chromecast and media sessions

**Cons:**
- Overkill for simple VOD without DRM
- Larger learning curve than Video.js for basic use

---

## Remotion

> ⚠️ **COMMERCIAL LICENCE REQUIRED FOR SAAS**
> Remotion is **not free for SaaS products**. A company licence starts at **$1,500 USD/year** (as of 2026-04) and is mandatory if you use Remotion to render videos on a server for end users — even if your product is free. Read the [licence FAQ](https://remotion.dev/license) before using in any commercial context.

| Field | Value |
|-------|-------|
| **Radar** | 🔴 Hold |
| **Status** | Exploring |
| **Score** | 88 / 100 (technical) · ⚠️ Blocked for SaaS |
| **Licence** | **Remotion Company Licence** — NOT free for commercial server-side rendering |
| **Website** | [remotion.dev](https://remotion.dev) |
| **Licence FAQ** | [remotion.dev/license](https://remotion.dev/license) |

**Why Hold:** The technical quality is high — React-based declarative video, great DX, TypeScript-first, good docs. The blocking reason is purely commercial: any server-side render of Remotion videos in a product sold to users (even B2B SaaS) requires a paid company licence. Unsuitable for our pipeline unless we budget for the licence fee.

**What it does well (technically):**
- React components as video frames — any React developer is immediately productive
- `useCurrentFrame()` and `useVideoConfig()` hooks for data-driven animations
- `<Sequence>` and `<Series>` for timeline composition
- Remotion Studio: browser-based preview with frame scrubbing

**Where the licence kicks in:**
```
Personal / open-source projects  → Free
Internal company tools            → Free (not customer-facing)
SaaS product (renders on server)  → REQUIRES paid licence
White-label / embedded            → REQUIRES paid licence
```

**Free alternatives with equivalent capability:**

| Alternative | Why it's a better fit for SaaS |
|-------------|-------------------------------|
| [Motion Canvas](#motion-canvas) | MIT, TypeScript-first, generator-based timeline — best direct replacement |
| [Revideo](#revideo) | Motion Canvas fork with cloud render queue — MIT runtime |
| [HyperFrames](#hyperframes) | Apache 2.0, HTML-native, agent-first CLI |
| [PyAV + PIL](#pyav) | Python path, BSD-3, frame-accurate, GPU-ready |

**Gotchas:**
- The licence applies even if you use only the open-source `@remotion/renderer` package on a server
- "Internal tools" exception only applies if the rendered output is not delivered to paying customers

---

## MediaPipe

| Field | Value |
|-------|-------|
| **Link** | [mediapipe.dev](https://mediapipe.dev) |
| **Use Case** | Real-time ML on video: pose estimation, face mesh, hand tracking, object detection |
| **Radar** | 🟡 Trial |
| **Status** | Exploring |

**Pros:**
- Cross-platform (Web WASM, Python, Android, iOS)
- Pre-trained models, no GPU needed for many tasks
- Low latency on-device inference

**Cons:**
- Model selection limited to what Google ships
- WASM performance lower than native for complex pipelines

---

## Programmatic Video Generation

> Free, licence-safe libraries for generating video programmatically — no commercial licence fees.
> Full comparison: [programmatic-video-tools](projects/programmatic-video-tools.md)

---

## PyAV

| Field | Value |
|-------|-------|
| **Radar** | 🟢 Adopt |
| **Status** | Production-ready |
| **Score** | 97 / 100 |
| **Licence** | BSD-3 |
| **Website** | [pyav.org](https://pyav.org) |
| **Projects** | [Programmatic Video Tools](../projects/programmatic-video-tools.md) |

**Why:** The highest-fidelity Python path to H.264/H.265 video. Binds directly to libav (the library inside FFmpeg) — no subprocess overhead, no temp files. Precise per-frame pts control, GPU encode via NVENC or VideoToolbox, and full audio mux in a single container pass. When you're building a SaaS video export pipeline, this is the encoding layer everything else feeds into.

**My Pattern:**
- PIL/Pillow or Skia-Python renders each frame as an RGBA numpy array
- PyAV encodes frame-by-frame with `crf=17`, `preset=fast`
- Audio synthesised separately (NumPy) → muxed as AAC 256 kbps in the same pass

**Minimal encode loop:**
```python
import av
import numpy as np
from PIL import Image, ImageDraw

W, H, FPS = 1280, 720, 30

with av.open("output.mp4", "w") as container:
    vstream = container.add_stream("h264", rate=FPS)
    vstream.width, vstream.height = W, H
    vstream.pix_fmt = "yuv420p"
    vstream.options = {"crf": "17", "preset": "fast"}

    for i in range(FPS * 10):
        img = Image.new("RGB", (W, H), (10, 10, 30))
        draw = ImageDraw.Draw(img)
        x = int(W * (i / (FPS * 10)))
        draw.ellipse([x-40, H//2-40, x+40, H//2+40], fill=(80, 200, 120))
        frame = av.VideoFrame.from_ndarray(np.array(img), format="rgb24")
        frame.pts = i
        for packet in vstream.encode(frame):
            container.mux(packet)
    for packet in vstream.encode():
        container.mux(packet)
```

**Gotchas:**
- Flush encoder after loop with `vstream.encode()` (no args) or last frames drop
- For GPU encode (NVENC): `container.add_stream('h264_nvenc', rate=FPS)`
- Set audio layout at creation: `container.add_stream('aac', rate=44100, layout='stereo')` — `astream.channels` is not writable

---

## MoviePy

| Field | Value |
|-------|-------|
| **Radar** | 🟢 Adopt |
| **Status** | Production-ready |
| **Score** | 91 / 100 |
| **Licence** | MIT |
| **Website** | [zulko.github.io/moviepy](https://zulko.github.io/moviepy/) |
| **Projects** | [Programmatic Video Tools](../projects/programmatic-video-tools.md) |

**Why:** Best Python tool for compositing *existing* clips — watermarks, subtitles, text overlays, concatenation. Used as the post-processing layer after PyAV or Manim renders raw video.

**Text overlay on existing clip:**
```python
from moviepy import VideoFileClip, TextClip, CompositeVideoClip

base = VideoFileClip("input.mp4")
label = (
    TextClip("PyAV Demo", font_size=60, color="white", font="DejaVu-Sans-Bold")
    .with_position(("center", 50))
    .with_duration(base.duration)
)
final = CompositeVideoClip([base, label])
final.write_videofile("output.mp4", fps=30, codec="libx264", audio_codec="aac")
```

**Gotchas:**
- v2.x changes `.set_position()` → `.with_position()`, `.set_duration()` → `.with_duration()`
- Font must be installed system-wide or passed as a path

---

## Manim CE

| Field | Value |
|-------|-------|
| **Radar** | 🟢 Adopt |
| **Status** | Production-ready |
| **Score** | 94 / 100 |
| **Licence** | MIT |
| **Website** | [manim.community](https://www.manim.community/) |
| **Projects** | [Programmatic Video Tools](../projects/programmatic-video-tools.md) |

**Why:** The best tool for math animations, diagram explainers, and data storytelling. Declarative scene graph — you describe *what* to render, not *how*. LaTeX is first-class. Used by 3Blue1Brown, free Community Edition (MIT), no licence cost for commercial SaaS.

**My Pattern:**
- One `Scene` class per logical section → render independently → FFmpeg concat
- `run_time` parameter controls animation duration — pair with `rate_func=smooth` for easing
- For long-form: render each scene to a file, concatenate with FFmpeg `concat` demuxer

**Animated bar chart:**
```python
from manim import *

class BarChartDemo(Scene):
    def construct(self):
        chart = BarChart(
            values=[4, 7, 2, 9, 5],
            bar_names=["Q1", "Q2", "Q3", "Q4", "Q5"],
            y_range=[0, 10, 2],
            bar_colors=[BLUE, GREEN, YELLOW, RED, PURPLE],
        )
        self.play(Create(chart), run_time=2)
        self.play(chart.animate.change_bar_values([6, 3, 8, 4, 7]), run_time=1.5)
        self.wait()
```

```bash
manim -pqh demo.py BarChartDemo   # 1080p production render
manim -pql demo.py BarChartDemo   # fast preview
```

**Gotchas:**
- LaTeX errors are cryptic — install `texlive-full` or test MathTex strings incrementally
- `run_time` is wall-clock seconds at FPS, not frames — 2.0 @ 30fps = 60 frames
- 4K: `config.pixel_height = 2160; config.pixel_width = 3840; config.frame_rate = 60`
- Needs `self.wait()` at the end or the last frame is cut

---

## Motion Canvas

| Field | Value |
|-------|-------|
| **Radar** | 🟢 Adopt |
| **Status** | Production-ready |
| **Score** | 93 / 100 |
| **Licence** | MIT |
| **Website** | [motioncanvas.io](https://motioncanvas.io) |
| **Projects** | [Programmatic Video Tools](../projects/programmatic-video-tools.md) |

**Why:** Best TypeScript-first declarative animation library for product demos and explainers. Generator-based timeline (`yield*` advances time) makes complex sequences readable. Real-time browser preview, hot-reload, exports to MP4. MIT licence — no commercial restrictions.

**My Pattern:**
- One `makeScene2D` per logical section
- Use `createRef<>()` to mutate component properties mid-animation
- Typing effects: loop characters with `yield* waitFor(0.04)` between each char

**Code typing effect:**
```ts
import { makeScene2D, Txt, Rect } from '@motion-canvas/2d';
import { waitFor, createRef } from '@motion-canvas/core';

export default makeScene2D(function* (view) {
  const codeEl = createRef<Txt>();
  view.add(
    <Rect fill="#1e1e2e" radius={12} padding={32} width={800} height={400}>
      <Txt ref={codeEl} fill="#cdd6f4" fontFamily="JetBrains Mono" fontSize={24} text="" />
    </Rect>
  );
  const snippet = 'const video = await render(scene);';
  for (const char of snippet) {
    codeEl().text(codeEl().text() + char);
    yield* waitFor(0.04);
  }
  yield* waitFor(1);
});
```

**Gotchas:**
- `createRef()` targets must be added to the view *before* reading `.text()`
- Export to MP4 requires the CLI: `npx @motion-canvas/cli render`
- Fonts must be registered before use: `import '@fontsource/jetbrains-mono'`

---

## Three.js (headless)

| Field | Value |
|-------|-------|
| **Radar** | 🟢 Adopt |
| **Status** | Production-ready |
| **Score** | 92 / 100 |
| **Licence** | MIT |
| **Website** | [threejs.org](https://threejs.org) |
| **Projects** | [Programmatic Video Tools](../projects/programmatic-video-tools.md) |

**Why:** GPU-accelerated 3D from Node.js via Puppeteer CDP frame capture. Best tool when you need real 3D — product reveals, data globes, particle systems — at production quality.

**Headless capture pattern:**
```js
import puppeteer from 'puppeteer';

const browser = await puppeteer.launch({ args: ['--use-gl=egl', '--no-sandbox'] });
const page = await browser.newPage();
await page.setViewport({ width: 1280, height: 720 });
await page.goto('http://localhost:3000/scene');

const FPS = 30, DURATION = 10;
const frames = [];
for (let i = 0; i < FPS * DURATION; i++) {
  await page.evaluate(f => window.renderFrame(f), i);
  frames.push(await page.screenshot({ type: 'png' }));
}
await browser.close();
// pipe frames[] → ffmpeg stdin
```

**Gotchas:**
- `--use-gl=egl` is required for headless GPU on Linux (Cloud Run / GKE)
- CDP `Page.screencastFrame` is faster than `page.screenshot()` for high-fps capture
- `THREE.CapsuleGeometry` not available until r142

---

## D3.js

| Field | Value |
|-------|-------|
| **Radar** | 🟢 Adopt |
| **Status** | Production-ready |
| **Score** | 90 / 100 |
| **Licence** | ISC |
| **Website** | [d3js.org](https://d3js.org) |
| **Projects** | [Programmatic Video Tools](../projects/programmatic-video-tools.md) |

**Why:** Unmatched control over data-bound SVG animations. Standard tool for animated data documentaries — bar chart races, time-series, chord diagrams, geographic maps. Captured via Puppeteer for MP4 export.

**Animated bar update:**
```js
const bars = svg.selectAll('rect').data(data, d => d.name);

bars.enter().append('rect')
  .attr('x', 0)
  .attr('y', d => yScale(d.name))
  .attr('height', yScale.bandwidth())
  .attr('width', 0)
  .attr('fill', d => colorScale(d.category));

bars.transition()
  .duration(750)
  .ease(d3.easeLinear)
  .attr('width', d => xScale(d.value));
```

**Gotchas:**
- `d3.easeLinear` for bar chart races; `d3.easeCubicOut` for UI
- SVG transitions cap at ~60fps — use Canvas renderer for higher rates
- `d3.select` in headless Node.js requires `jsdom` + `d3-node` wrapper

---

## Anime.js

| Field | Value |
|-------|-------|
| **Link** | [animejs.com](https://animejs.com) |
| **Use Case** | DOM/SVG/CSS animations for UI mockups and web capture pipelines |
| **Radar** | 🟢 Adopt |
| **Status** | Production-ready |

**Pros:**
- Chainable timeline API, very readable
- Supports CSS, SVG, DOM, and plain JS object animation
- Tiny bundle (~17 KB)

**Cons:**
- No WebGL/3D — use Three.js or PixiJS for that
- Relies on browser render — needs Puppeteer for MP4 export

---

## PixiJS

| Field | Value |
|-------|-------|
| **Link** | [pixijs.com](https://pixijs.com) |
| **Use Case** | WebGL 2D renderer for sprite-heavy scenes, dashboards, particle systems |
| **Radar** | 🟢 Adopt |
| **Status** | Production-ready |

**Pros:**
- WebGL batching: thousands of sprites at 60+ fps
- GPU filters (blur, glow, CRT effect) as shaders
- Spine animation integration

**Cons:**
- No built-in video export — requires Puppeteer headless capture
- Overkill for simple text animations

---

## Revideo

| Field | Value |
|-------|-------|
| **Radar** | 🟡 Trial |
| **Status** | Exploring |
| **Score** | 90 / 100 |
| **Licence** | MIT |
| **Website** | [re.video](https://re.video) |
| **Projects** | [Programmatic Video Tools](../projects/programmatic-video-tools.md) |

**Why Evaluating:** Motion Canvas fork with a cloud render queue — ideal for generating N personalised videos from a dataset. API is 1:1 compatible with Motion Canvas so switching cost is low.

**Key Concepts:**
- Same `makeScene2D` / `createRef` API as Motion Canvas
- `renderVideo({ variables })` accepts data-driven parameters per render
- Cloud queue distributes renders across workers — useful for bulk generation

**Gotchas (so far):**
- API still shifting between minor versions — pin exact version in `package.json`
- Cloud pricing not yet announced — budget accordingly

---

## HyperFrames

| Field | Value |
|-------|-------|
| **Link** | [github.com/heygen-com/hyperframes](https://github.com/heygen-com/hyperframes) |
| **Use Case** | Write plain HTML + CSS/GSAP, render deterministic MP4/WebM via headless Chrome + FFmpeg. Agent-friendly non-interactive CLI. |
| **Radar** | 🟡 Trial |
| **Status** | Exploring |
| **Licence** | Apache 2.0 |

**Pros:**
- HTML-native — no proprietary DSL or React compiler. `data-start`, `data-duration`, `data-track-index` attributes drive the timeline; a `window.__timelines[id]` GSAP timeline drives animation.
- `npx hyperframes init` → working project in one command. Ships `doctor`, `lint`, `snapshot`, `render`, `preview` subcommands — all non-interactive, composable in CI.
- Parallel frame capture (8 Chrome workers on 16 cores rendered 5s @ 1080p30 in **7.1s** in my test) — faster than single-process Puppeteer capture.
- Linter caught a real issue (`missing_timeline_registry`) in one of my test compositions.
- Apache 2.0 — no commercial gotcha like Remotion.
- First-class agent story: `hyperframes skills` drops AGENTS.md / CLAUDE.md guides into the project.

**Cons:**
- Pulls a ~110 MB Chrome Headless Shell on first run (`hyperframes browser ensure`) — heavy for ephemeral CI runners; cache the `~/.cache/hyperframes/chrome` path.
- CDN `<script>` tags (e.g. GSAP from jsdelivr) failed in my sandboxed network — render continued but animation silently didn't run. **Bundle animation libs locally** (`./vendor/gsap.min.js`) to be safe in airgapped / restricted networks.
- `render -o out.mp4` short flag errored with `Not a directory`; `--output out.mp4` works. Minor CLI parsing bug in v0.4.6.
- Linter flags `missing_timeline_registry` even for pure CSS `@keyframes` compositions that don't need a GSAP timeline — render still succeeds (non-strict by default) but the warning is a false positive for CSS-only scenes.
- Young project (v0.4.6 at test time) — expect API churn.

**Tested Example 1 — animated title card (GSAP):**

![HyperFrames GSAP title card demo](../samples/hyperframes/01-title-card-gsap.gif)

_Rendered MP4: [`samples/hyperframes/01-title-card-gsap.mp4`](../samples/hyperframes/01-title-card-gsap.mp4) — 1920×1080 · H.264 · 30fps · 5s · 228 KB_

```html
<!-- index.html -->
<!doctype html>
<html>
  <head>
    <meta name="viewport" content="width=1920, height=1080" />
    <script src="./vendor/gsap.min.js"></script>
    <style>
      html, body { width: 1920px; height: 1080px; background: #0f172a; }
      .stage { display: flex; align-items: center; justify-content: center; height: 100%; flex-direction: column; }
      .title { font-size: 140px; font-weight: 800; color: #f8fafc; }
      .accent { color: #60a5fa; }
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="5" data-width="1920" data-height="1080">
      <div class="stage clip" data-start="0" data-duration="5" data-track-index="1">
        <div class="title">
          <span id="w1">Render</span>
          <span id="w2" class="accent">video</span>
          <span id="w3">from HTML</span>
        </div>
      </div>
    </div>
    <script>
      const tl = gsap.timeline({ paused: true });
      tl.from("#w1", { opacity: 0, y: 40, duration: 0.5 }, 0.3);
      tl.from("#w2", { opacity: 0, y: 40, duration: 0.5 }, 0.5);
      tl.from("#w3", { opacity: 0, y: 40, duration: 0.5 }, 0.7);
      window.__timelines = { main: tl };
    </script>
  </body>
</html>
```

```bash
npx hyperframes lint                    # 0 errors, 0 warnings
npx hyperframes render --output out.mp4 # 150 frames, 227 KB, 7.1s wall-clock
```

**Tested Example 2 — animated bar chart (pure CSS, no GSAP):**

![HyperFrames CSS bar chart demo](../samples/hyperframes/02-bar-chart-css.gif)

_Rendered MP4: [`samples/hyperframes/02-bar-chart-css.mp4`](../samples/hyperframes/02-bar-chart-css.mp4) — 1920×1080 · H.264 · 30fps · 6s · 102 KB_

```html
<div id="root" data-composition-id="main" data-start="0" data-duration="6"
     data-width="1920" data-height="1080">
  <div class="stage clip" data-start="0" data-duration="6" data-track-index="1">
    <h1>Video-Media Stack Usage</h1>
    <div class="row r1">
      <div class="label">PyAV</div>
      <div class="track"><div class="bar" style="--w: 92%"></div></div>
      <div class="value">92%</div>
    </div>
    <!-- ... more rows ... -->
  </div>
</div>

<style>
  .bar { width: 0; animation: grow 1.6s cubic-bezier(0.16, 1, 0.3, 1) forwards; }
  .r1 .bar { background: linear-gradient(90deg, #3b82f6, #60a5fa); animation-delay: 0.3s; }
  @keyframes grow { to { width: var(--w); } }
</style>
```

```bash
npx hyperframes render --output out.mp4
# ✗ missing_timeline_registry: Missing `window.__timelines` registration.  ← false positive for CSS-only
# Render continues → 180 frames, 102 KB, 7.3s
```

**Honest verdict:**

Slotted between Motion Canvas and Remotion. If your designers / agents already speak HTML+CSS and you want MP4 out without React or a $1,500/yr commercial licence, HyperFrames is the cleanest path I've tested. The agent-first CLI (every command works non-interactively, with `--quiet`, `--strict`, JSON-ish output) is genuinely well-designed for Claude-Code / Cursor pipelines. Not yet production-ready for me — the CDN-blocking and linter false-positive burn time — but a strong **🟡 Trial** to revisit at v1.0.

---

## Skia-Python

| Field | Value |
|-------|-------|
| **Radar** | 🟡 Trial |
| **Status** | Exploring |
| **Score** | 88 / 100 |
| **Licence** | BSD-3 |
| **Website** | [kyamagu.github.io/skia-python](https://kyamagu.github.io/skia-python/) |
| **Projects** | [Programmatic Video Tools](../projects/programmatic-video-tools.md) |

**Why Evaluating:** Chrome-quality 2D rendering from Python — better font shaping and anti-aliasing than Pillow. Drops in as a Pillow replacement in PyAV pipelines. GPU-accelerated on Metal/Vulkan.

**Frame rendering:**
```python
import skia

surface = skia.Surface(1280, 720)
with surface as canvas:
    paint = skia.Paint(Shader=skia.GradientShader.MakeLinear(
        [(0, 0), (1280, 720)],
        [0xFF1e1e2e, 0xFF313244]
    ))
    canvas.drawPaint(paint)
    blob = skia.TextBlob.MakeFromString("Hello Skia", skia.Font(None, 72))
    canvas.drawTextBlob(blob, 400, 380,
                        skia.Paint(Color=0xFFcdd6f4, AntiAlias=True))

frame_array = surface.toarray()   # BGRA numpy array
```

**Gotchas:**
- `pip install skia-python` — wheels are bundled, no system Skia needed
- `surface.toarray()` returns BGRA — convert to RGB before PyAV: `frame_array[:, :, :3][:, :, ::-1]`

---

## Vispy

| Field | Value |
|-------|-------|
| **Link** | [vispy.org](https://vispy.org) |
| **Use Case** | OpenGL scientific visualisation: point clouds, volume renders, real-time data |
| **Radar** | 🟡 Trial |
| **Status** | Exploring |

**Pros:**
- Renders millions of points at 60+ fps via GPU
- Good for geospatial and scientific data
- Python API

**Cons:**
- Requires a display (Xvfb in CI)
- Scene API dated vs Three.js

---

## Movis

| Field | Value |
|-------|-------|
| **Link** | [github.com/rezoo/movis](https://github.com/rezoo/movis) |
| **Use Case** | After Effects-style layer compositing in Python |
| **Radar** | 🟡 Trial |
| **Status** | Exploring |

**Pros:**
- Layer-based timeline with easing functions
- Simple API — accessible to non-video engineers

**Cons:**
- Small community, slow development cadence
- Performance limited by Python frame loop

---

## GStreamer

| Field | Value |
|-------|-------|
| **Radar** | 🟡 Trial |
| **Status** | Exploring |
| **Score** | 87 / 100 |
| **Licence** | LGPL |
| **Website** | [gstreamer.freedesktop.org](https://gstreamer.freedesktop.org) |
| **Projects** | [Programmatic Video Tools](../projects/programmatic-video-tools.md) |

**Why Evaluating:** Broadcast-grade pipeline processing. Relevant for embedded targets (Jetson, Pi) and GPU-accelerated live pipelines. LGPL — usable in commercial products with dynamic linking.

**Key Concepts:**
- Pipeline = source → filters → sink, described as a string or built programmatically
- `appsrc` + `appsink` = inject/extract frames from Python
- `nvh264enc` = NVENC hardware encode element

**Simple pipeline (Python):**
```python
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst

Gst.init(None)
pipeline = Gst.parse_launch(
    'videotestsrc num-buffers=300 ! '
    'video/x-raw,width=1280,height=720,framerate=30/1 ! '
    'x264enc bitrate=4000 ! mp4mux ! filesink location=out.mp4'
)
pipeline.set_state(Gst.State.PLAYING)
pipeline.get_bus().timed_pop_filtered(Gst.CLOCK_TIME_NONE, Gst.MessageType.EOS)
pipeline.set_state(Gst.State.NULL)
```

**Gotchas:**
- `appsrc` pushes frames as `Gst.Buffer` — convert from numpy: `Gst.Buffer.new_wrapped(array.tobytes())`
- LGPL requires dynamic linking — don't statically bundle GStreamer into a proprietary binary

---

## Matplotlib Animation

| Field | Value |
|-------|-------|
| **Link** | [matplotlib.org/stable/api/animation_api.html](https://matplotlib.org/stable/api/animation_api.html) |
| **Use Case** | Quick animated chart exports from existing Matplotlib plots |
| **Radar** | 🟡 Trial |
| **Status** | Exploring |

**Pros:**
- Zero extra dependencies if Matplotlib already in stack
- `FuncAnimation` + `FFMpegWriter` — simple path to MP4

**Cons:**
- Slow render (CPU-only Python frame loop)
- No compositing or text overlay beyond Matplotlib primitives

---

## Lottie-Web

| Field | Value |
|-------|-------|
| **Link** | [airbnb.io/lottie](https://airbnb.io/lottie/#/) |
| **Use Case** | Render After Effects JSON animations in browser — micro-animations, loaders |
| **Radar** | 🟡 Trial |
| **Status** | Exploring |

**Pros:**
- Designer-friendly (AE → Bodymovin → JSON workflow)
- Tiny runtime, transparent video support
- Works headless via Puppeteer for MP4 export

**Cons:**
- Dependent on designer AE toolchain
- Complex animations lose fidelity in JSON conversion

---

## p5.js

| Field | Value |
|-------|-------|
| **Link** | [p5js.org](https://p5js.org) |
| **Use Case** | Generative art, creative coding sketches, educational animations |
| **Radar** | 🟡 Trial |
| **Status** | Exploring |

**Pros:**
- Very beginner-friendly API
- Large creative coding community
- Canvas + WebGL modes

**Cons:**
- LGPL-2.1 — disclosure required in commercial products
- Not optimised for production video pipelines

---

## Rive

| Field | Value |
|-------|-------|
| **Link** | [rive.app](https://rive.app) |
| **Use Case** | State machine animations (idle → hover → active) for interactive product UI |
| **Radar** | 🟡 Trial |
| **Status** | Exploring |

**Pros:**
- State machine model — animations respond to real data, not just time
- MIT runtime, small `.riv` binary files
- WASM runtime works in any JS environment

**Cons:**
- Editor is closed-source (runtime is MIT)
- Not designed for video export

---

## Editly

| Field | Value |
|-------|-------|
| **Link** | [github.com/mifi/editly](https://github.com/mifi/editly) |
| **Use Case** | Declarative JSON-defined video editing and clip assembly in Node.js |
| **Radar** | 🟡 Trial |
| **Status** | Exploring |

**Pros:**
- JSON spec → MP4 — zero code for simple clip assembly
- Built-in transitions, text overlays, audio mixing

**Cons:**
- Limited to built-in transitions and effects
- Slow for large batches vs fluent-ffmpeg

---

## LibOpenShot

| Field | Value |
|-------|-------|
| **Link** | [openshot.org](https://www.openshot.org/developers/) |
| **Use Case** | Python bindings to OpenShot video editor C++ engine |
| **Radar** | 🔴 Hold |
| **Status** | Exploring |

**Pros:**
- Powerful clip timeline engine

**Cons:**
- **LGPL-3** — linking restrictions complicate commercial SaaS
- Python API surface is fragile and poorly documented

---

## ProjectM

| Field | Value |
|-------|-------|
| **Link** | [github.com/projectM-visualizer/projectm](https://github.com/projectM-visualizer/projectm) |
| **Use Case** | MilkDrop-style audio-reactive generative visuals |
| **Radar** | 🔴 Hold |
| **Status** | Exploring |

**Pros:**
- GPU-accelerated generative visuals with audio input

**Cons:**
- **LGPL** — commercial use restrictions
- C++ heavy — no Python-friendly frame capture path

---

## Pytoon

| Field | Value |
|-------|-------|
| **Link** | [github.com/atomicshark/pytoon](https://github.com/atomicshark/pytoon) |
| **Use Case** | Experimental Python cartoon animation library |
| **Radar** | 🔴 Hold |
| **Status** | Exploring |

**Pros:**
- MIT licence

**Cons:**
- Pre-alpha — API unstable, no reliable release cadence
- No production usage evidence

---
