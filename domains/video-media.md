# 🎬 Video & Media — Programmatic Generation

> Libraries for generating video programmatically from Python and TypeScript/JavaScript.
> Evaluated for a SaaS video pipeline.
>
> ⚠️ **Licence warning:** Some tools in this domain (Remotion, GSAP SaaS plan, p5.js LGPL-2.1, LibOpenShot LGPL-3) carry commercial-use restrictions. See each tool entry before adopting in a closed-source SaaS product.

---

## Tools

---

### PyAV

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

    for i in range(FPS * 10):  # 10 seconds
        img = Image.new("RGB", (W, H), (10, 10, 30))
        draw = ImageDraw.Draw(img)
        x = int(W * (i / (FPS * 10)))
        draw.ellipse([x-40, H//2-40, x+40, H//2+40], fill=(80, 200, 120))

        frame = av.VideoFrame.from_ndarray(np.array(img), format="rgb24")
        frame.pts = i
        for packet in vstream.encode(frame):
            container.mux(packet)

    for packet in vstream.encode():  # flush
        container.mux(packet)
```

**Gotchas:**
- `astream.channels` is not writable — set layout at stream creation: `container.add_stream('aac', rate=44100, layout='stereo')`
- Remove `vf.time_base = '1/30'` — this causes `AttributeError: 'str' has no attribute 'numerator'`
- Flush encoder after loop with `vstream.encode()` (no args) or last frames are dropped
- For GPU encode (NVENC): `vstream = container.add_stream('h264_nvenc', rate=FPS)`

**Alternatives Considered:**

| Tool | Why I didn't choose it |
|------|----------------------|
| subprocess + ffmpeg | Temp file I/O overhead, harder to control pts |
| MoviePy | Higher abstraction — good for compositing, slower for pure generation |
| imageio-ffmpeg | Less control over codec parameters |

---

### Manim CE

| Field | Value |
|-------|-------|
| **Radar** | 🟢 Adopt |
| **Status** | Production-ready |
| **Score** | 94 / 100 |
| **Licence** | MIT |
| **Website** | [manim.community](https://www.manim.community/) |
| **Projects** | [Programmatic Video Tools](../projects/programmatic-video-tools.md) |

**Why:** The best tool for math animations, diagram explainers, and data storytelling. Declarative scene graph — you describe *what* to render, not *how* to render it. LaTeX is first-class. Used by 3Blue1Brown, free Community Edition (MIT), no licence cost for commercial SaaS.

**My Pattern:**
- One `Scene` class per logical section → render independently → FFmpeg concat
- `run_time` parameter controls animation duration — pair with `rate_func=smooth` for easing
- For long-form content: render each scene to a file, concatenate with FFmpeg `concat` demuxer

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
        label = chart.get_axis_labels(x_label="Quarter", y_label="Revenue")
        self.play(Create(chart), Write(label), run_time=2)
        self.play(chart.animate.change_bar_values([6, 3, 8, 4, 7]), run_time=1.5)
        self.wait()
```

```bash
manim -pqh demo.py BarChartDemo   # 1080p production render
manim -pql demo.py BarChartDemo   # fast preview
```

**Gotchas:**
- LaTeX errors are cryptic — install `texlive-full` or use MathTex strings that you test one at a time
- `run_time` is wall-clock animation duration at FPS, not frames — 2.0 at 30fps = 60 frames
- For 4K output: `config.pixel_height = 2160; config.pixel_width = 3840; config.frame_rate = 60`
- Scene-level `self.wait()` is needed at the end or the last frame is cut

**Alternatives Considered:**

| Tool | Why I didn't choose it |
|------|----------------------|
| Matplotlib Animation | Less expressive for complex geometry, slower |
| Motion Canvas | TypeScript-first — better for JS teams |
| Adobe After Effects | Not programmatic, expensive licence |

---

### Motion Canvas

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
- For typing effects: loop characters with `yield* waitFor(0.04)` between each char

**Animated code typing effect:**
```ts
import { makeScene2D, Txt, Rect } from '@motion-canvas/2d';
import { all, waitFor, createRef } from '@motion-canvas/core';

export default makeScene2D(function* (view) {
  const codeEl = createRef<Txt>();

  view.add(
    <Rect fill="#1e1e2e" radius={12} padding={32} width={800} height={400}>
      <Txt
        ref={codeEl}
        fill="#cdd6f4"
        fontFamily="JetBrains Mono"
        fontSize={24}
        text=""
      />
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
- `createRef()` targets must be added to the view *before* reading `.text()` — order matters
- Export to MP4 requires the CLI: `npx @motion-canvas/cli render`
- Hot-reload only works in `dev` mode — CI renders use `render` command
- Fonts must be registered before use: `import '@fontsource/jetbrains-mono'`

**Alternatives Considered:**

| Tool | Why I didn't choose it |
|------|----------------------|
| Remotion | Commercial licence required for SaaS ($1,500+/yr) |
| Revideo | Younger fork of Motion Canvas — evaluating |
| GreenSock (GSAP) | Licence restricts commercial use on SaaS without paid plan |

---

### fluent-ffmpeg

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
- Add background music: `volume=0.3` audio filter on music track
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
    '-map [v]', '-map [music]',
    '-shortest',
    '-c:v libx264', '-crf 18',
    '-c:a aac', '-b:a 256k',
  ])
  .output('final.mp4')
  .on('end', () => console.log('Done'))
  .run();
```

**Gotchas:**
- `concat` filter requires same resolution and framerate on all inputs — normalise first
- `-shortest` cuts to the shortest stream — omit if music should loop to video length
- Use `-an` on video inputs when audio is handled separately

---

### MoviePy

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
    TextClip(
        "PyAV Demo",
        font_size=60,
        color="white",
        font="DejaVu-Sans-Bold"
    )
    .with_position(("center", 50))
    .with_duration(base.duration)
)
final = CompositeVideoClip([base, label])
final.write_videofile("output.mp4", fps=30, codec="libx264", audio_codec="aac")
```

**Gotchas:**
- v2.x changes `.set_position()` → `.with_position()`, `.set_duration()` → `.with_duration()`
- Font must be installed system-wide or passed as a path — `font="DejaVu-Sans-Bold"` works on Linux

---

### Three.js (headless)

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
// capture.js
import puppeteer from 'puppeteer';
import { createFFmpeg } from '@ffmpeg/ffmpeg';

const browser = await puppeteer.launch({
  args: ['--use-gl=egl', '--no-sandbox'],
});
const page = await browser.newPage();
await page.setViewport({ width: 1280, height: 720 });
await page.goto('http://localhost:3000/scene');   // serve your Three.js scene

const FPS = 30, DURATION = 10;
const frames = [];
for (let i = 0; i < FPS * DURATION; i++) {
  await page.evaluate(f => window.renderFrame(f), i);   // call your render fn
  frames.push(await page.screenshot({ type: 'png' }));
}
await browser.close();
// pipe frames[] → ffmpeg stdin
```

**Gotchas:**
- `THREE.CapsuleGeometry` not available until r142 — use `CylinderGeometry` + `SphereGeometry` for older builds
- `--use-gl=egl` is required for headless GPU on Linux (Cloud Run / GKE)
- CDP `Page.screencastFrame` is faster than `page.screenshot()` for high-fps capture

---

### Revideo

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

### Skia-Python

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
import skia, numpy as np

surface = skia.Surface(1280, 720)
with surface as canvas:
    # gradient background
    paint = skia.Paint(Shader=skia.GradientShader.MakeLinear(
        [(0, 0), (1280, 720)],
        [0xFF1e1e2e, 0xFF313244]
    ))
    canvas.drawPaint(paint)

    # text
    blob = skia.TextBlob.MakeFromString("Hello Skia", skia.Font(None, 72))
    canvas.drawTextBlob(blob, 400, 380,
                        skia.Paint(Color=0xFFcdd6f4, AntiAlias=True))

frame_array = surface.toarray()   # numpy array → PyAV VideoFrame
```

**Gotchas:**
- Install via `pip install skia-python` — no system Skia dependency needed (wheels are bundled)
- `surface.toarray()` returns BGRA — convert to RGB before passing to PyAV: `frame_array[:, :, :3][:, :, ::-1]`

---

### GStreamer

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
- On macOS: use `videotestsrc` for testing — real camera requires `avfvideosrc`
- `appsrc` pushes frames as `Gst.Buffer` — convert from numpy with `Gst.Buffer.new_wrapped(array.tobytes())`
- LGPL requires dynamic linking — don't statically bundle GStreamer into a proprietary binary

---

### D3.js

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
  .attr('width', d => xScale(d.value))
  .attr('y',     d => yScale(d.name));
```

**Gotchas:**
- `d3.easeLinear` for bar chart races (consistent speed) vs `d3.easeCubicOut` for UI animations
- SVG transitions cap at ~60fps — use Canvas renderer (`d3-canvas`) for higher frame rates
- `d3.select` in a headless Node.js context requires `jsdom` + `d3-node` wrapper

---

### Remotion

> ⚠️ **COMMERCIAL LICENCE REQUIRED FOR SAAS**
> Remotion is **not free for SaaS products**. A company licence starts at **$1,500 USD/year** (as of 2026-03) and is mandatory if you use Remotion to render videos on a server for end users — even if your product is free. Read the [licence FAQ](https://remotion.dev/license) before using in any commercial context.

| Field | Value |
|-------|-------|
| **Radar** | 🔴 Hold |
| **Status** | Exploring |
| **Score** | 88 / 100 (technical) · ⚠️ Blocked for SaaS |
| **Licence** | **Remotion Company Licence** — NOT free for commercial server-side rendering |
| **Website** | [remotion.dev](https://remotion.dev) |
| **Licence FAQ** | [remotion.dev/license](https://remotion.dev/license) |

**Why Hold:** The technical quality is high — React-based declarative video, great DX, TypeScript-first, good docs. The blocking reason is purely commercial: any server-side render of Remotion videos in a product sold to users (even B2B SaaS) requires a paid company licence. This makes it unsuitable for our pipeline unless we budget for the licence fee.

**What it does well (technically):**
- React components as video frames — any React developer is immediately productive
- `useCurrentFrame()` and `useVideoConfig()` hooks for data-driven animations
- `<Sequence>` and `<Series>` for timeline composition
- Remotion Studio: browser-based preview with frame scrubbing
- Cloud rendering via Lambda or GCP Cloud Run (with licence)

**Where the licence kicks in:**
```
Personal / open-source projects  → Free
Internal company tools            → Free (not customer-facing)
SaaS product (renders on server)  → REQUIRES paid licence
White-label / embedded            → REQUIRES paid licence
```

**Example (what the code looks like — not for production use without licence):**
```tsx
import { AbsoluteFill, useCurrentFrame, interpolate } from 'remotion';

export const MyScene: React.FC = () => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 30], [0, 1], { extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill style={{ background: '#1e1e2e', justifyContent: 'center', alignItems: 'center' }}>
      <h1 style={{ color: '#cdd6f4', fontSize: 72, opacity }}>
        Hello Remotion
      </h1>
    </AbsoluteFill>
  );
};
```

**Free alternatives with equivalent capability:**

| Alternative | Why it's a better fit for SaaS |
|-------------|-------------------------------|
| [Motion Canvas](../domains/video-media.md#motion-canvas) | MIT licence, TypeScript-first, generator-based timeline — best direct replacement |
| [Revideo](../domains/video-media.md#revideo) | Motion Canvas fork with cloud render queue — MIT runtime |
| [PyAV + PIL](../domains/video-media.md#pyav) | Python path, BSD-3, frame-accurate, GPU-ready |

**Gotchas:**
- The licence applies even if you use only the open-source `@remotion/renderer` package on a server
- "Internal tools" exception only applies if the rendered output is not delivered to paying customers
- Lambda/GCP render templates are provided but the licence cost is on top of infra costs

---
