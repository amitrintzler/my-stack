# 🌐 Web Games

> Web-native game engines and 2D/3D libraries built for the browser as the primary target. Distinct from `game-engines.md`, which covers desktop-first engines that *also* export to web.

---

## Quick Decision Matrix

| Need | Pick |
|------|------|
| 2D arcade / puzzle / RPG, fully free, mobile-friendly | **Phaser** |
| 3D production game with editor + asset pipeline | **PlayCanvas** |
| 3D engine with Microsoft backing + WebGPU first | **Babylon.js** |
| Full control, code-first 3D, smallest bundle | **Three.js** (see [video-media.md](video-media.md#threejs)) |

---

## Phaser

| Field | Value |
|-------|-------|
| **Radar** | 🟡 Trial |
| **Status** | Exploring |
| **Licence** | MIT — free, no revenue cap |
| **Website** | [phaser.io](https://phaser.io) |
| **Languages** | JavaScript, TypeScript |

**Why:** The de-facto standard for HTML5 2D games. Canvas + WebGL renderer, Arcade and Matter.js physics built-in, tight mobile-touch support, 2,000+ runnable examples in the repo. Used by indie studios and ad-tech alike for instant-play browser games.

**What you can build:**
- Arcade games, puzzlers, deckbuilders, top-down RPGs
- Playable ads / marketing mini-games
- Educational games and edu-tech apps
- Game-jam prototypes (fastest 2D iteration on the web)

**Playable samples:**
- [itch.io — HTML5 games made with Phaser](https://itch.io/games/html5/made-with-phaser) — hundreds, in-browser
- [Official Phaser site](https://phaser.io/) — rotating showcase
- [9 Fun HTML5 Games Built with Phaser](https://www.joshmorony.com/9-fun-html5-games-built-with-phaser/) — curated playable list
- [phaser examples repo](https://github.com/phaserjs/phaser) — 2,000+ runnable examples
- Notable titles: **Curvatron** (multiplayer Tron-snake), **Ramp Lab** (physics sandbox), **Exhibit of Sorrows**

**Gotchas:**
- 2D only — for 3D you need a different tool
- API surface is large; expect a learning curve on scenes/state machines
- No visual editor — code-first workflow

---

## PlayCanvas

| Field | Value |
|-------|-------|
| **Radar** | 🟡 Trial |
| **Status** | Exploring |
| **Licence** | MIT (engine) — editor has free tier; paid tiers for private projects / collaboration |
| **Website** | [playcanvas.com](https://playcanvas.com) |
| **Languages** | JavaScript, TypeScript |

**Why:** Built browser-first from day one. Tiny runtime (~300KB), WebGL2 + WebGPU support, full visual editor running in the browser. Used in production for ads, AR try-on, configurators, and console-quality 3D games delivered as URLs. Better web fidelity than Unity WebGL exports.

**What you can build:**
- Browser FPS / multiplayer 3D games (Mini Royale: Nations, Robostorm)
- Product configurators and AR try-on experiences
- WebXR / VR experiences
- High-end playable ads and interactive marketing
- Gaussian Splat → playable scene workflows

**Playable samples:**
- [Explore Projects gallery](https://playcanvas.com/explore) — official curated showcase
- [Made with PlayCanvas](https://developer.playcanvas.com/user-manual/getting-started/made-with-playcanvas/) — production games
- [Turning a Gaussian Splat Into a Videogame](https://blog.playcanvas.com/turning-a-gaussian-splat-into-a-videogame/) — photogrammetry → browser FPS
- [awesome-playcanvas](https://github.com/playcanvas/awesome-playcanvas) — community master list
- [PlayCanvas Examples](https://playcanvas.vercel.app/) — code-level demos
- Notable: **Mini Royale: Nations**, **Robostorm**, **SWOOOP**, **After the Flood** (Mozilla WebGL2), **Star-Lord** (PBR demo)

**Gotchas:**
- Engine is MIT, but the cloud editor's free tier limits private projects — host the editor yourself or pay for privacy
- Smaller asset marketplace than Unity / Unreal
- WebGPU support evolving; some features still WebGL2-only

---

## Babylon.js

| Field | Value |
|-------|-------|
| **Radar** | 🟡 Trial |
| **Status** | Exploring |
| **Licence** | Apache 2.0 — fully free |
| **Website** | [babylonjs.com](https://www.babylonjs.com) |
| **Languages** | TypeScript (primary), JavaScript |

**Why:** Microsoft-backed full-featured 3D engine for the browser. WebGPU is first-class (often ahead of competitors). Live Playground editor lets you prototype scenes by URL. Strong on technical fidelity — physics, PBR, post-processing, node-based materials.

**What you can build:**
- 3D games and interactive simulations
- Accessibility-first games (e.g., audio-only Breakout for visually impaired)
- WebXR / VR / AR experiences
- Engineering and CAD viewers
- Data visualisation in 3D

**Playable samples:**
- [Babylon.js Playground](https://playground.babylonjs.com/) — live editor with hundreds of runnable scenes
- [Community Demos](https://www.babylonjs.com/community/) — curated showcases
- [Feature Demos](https://www.babylonjs.com/featureDemos/) — graphics tech
- [Games gallery](https://www.babylonjs.com/games/)
- [DiStraction](https://www.babylonjs.com/Demos/Distraction/) — interactive demo
- [Demos & projects forum](https://forum.babylonjs.com/c/demos/9)
- [awesome-babylonjs](https://github.com/Symbitic/awesome-babylonjs)

**Gotchas:**
- Smaller game-dev community than Unity / Unreal — more "graphics engine" energy than "game engine"
- Editor is less integrated than PlayCanvas (Playground ≠ full scene editor)
- TypeScript-first; some JS-only examples lag

---

## Three.js — cross-reference

**Three.js** is catalogued in [domains/video-media.md](video-media.md#threejs) as 🟢 Adopt for programmatic 3D rendering. It is *also* the most flexible foundation for code-first 3D web games:

**Playable game samples:**
- [itch.io — Made With Three.js](https://itch.io/games/made-with-threejs) — playable in-browser
- [10+ Three.js Games (Free Frontend)](https://freefrontend.com/three-js-games/)
- [15+ Three.js Games with code](https://devsnap.me/three-js-games)
- [20 Best Three.js Examples 2026](https://uicookies.com/threejs-examples/)
- [Alfi's Adventures showcase](https://discourse.threejs.org/t/alfis-adventures-three-js-game/85754)
- Notable: **HexGL** (Wipeout-style racer), **Polycraft** (multiplayer survival), **Desert Dunes Explorer**

Pair with **react-three-fiber** for declarative React-style scene composition.

---

## Decision Cheat Sheet

| Scenario | Engine |
|----------|--------|
| 2D mobile-web game, small bundle | Phaser |
| 3D game with visual editor, ship URL | PlayCanvas |
| 3D, want WebGPU + open-source backing | Babylon.js |
| 3D, code-first, max control, smallest deps | Three.js + r3f |
| Already on Godot, web export acceptable | Godot HTML5 (see [game-engines.md](game-engines.md#godot)) |

---

## Alternatives Considered (not added)

| Tool | Why not added |
|------|---------------|
| Construct 3 | Proprietary, subscription-only — fails the "free" bar |
| GDevelop | Free + open-source 2D, worth a revisit on next pass |
| Cocos Creator | Strong in Asia for web/mobile 2D + 3D; outside current radar |
| Pixi.js | 2D renderer, not a full engine — already in `video-media.md` |
| Kaboom.js / Kaplay | Tiny 2D JS lib, great for jams; revisit if I do a jam |

---

*Last updated: 2026-05*
