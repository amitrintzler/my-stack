# 🎮 Game Engines

> Real-time 3D / 2D engines for games, AR/VR, simulation, and interactive media. Comparison of the major proprietary option (Unity) against the leading open-source and source-available alternatives.

---

## Quick Decision Matrix

| Need | Pick |
|------|------|
| Mobile + AR/VR + Asset Store + console export | **Unity** |
| 2D-first / fully FOSS / no royalties ever | **Godot** |
| AAA 3D / large-world simulation / cloud-native | **O3DE** |
| Pure C# / Unity-like API under MIT | **Stride** |
| Unity-style workflow with Unreal-tier visuals | **Flax** |

---

## Unity

| Field | Value |
|-------|-------|
| **Radar** | 🟡 Trial |
| **Status** | Exploring |
| **Licence** | Proprietary — Personal tier free under $200k/yr revenue; Pro/Enterprise paid |
| **Website** | [unity.com](https://unity.com) |
| **Languages** | C# (primary), C++ via native plugins |

**Why:** Industry-standard real-time engine. Largest asset store and tutorial ecosystem, one-click export to iOS/Android/Web/Windows/macOS/Linux + every major console. AR Foundation (ARKit + ARCore) and XR Toolkit make it the default for mobile AR and VR work. Cinematic real-time visuals are now competitive with Unreal for stylised content.

**What you can build:**
- Mobile games (Among Us, Pokémon GO, Genshin Impact)
- AR/VR apps (Quest, Vision Pro, HoloLens)
- Indie 3D and 2D titles, gacha games, simulation
- Real-time cinematics and virtual production
- Automotive / arch-viz / training sims

**Showcase videos:**
- [Made With Unity sizzle reel — Spring 2024](https://www.youtube.com/watch?v=09XGap8QiL8) — montage of recent shipped games
- [Enemies — real-time cinematic teaser](https://www.youtube.com/watch?v=eXYUNrgqWUU) — photoreal humans rendered live
- [Wide-ranging showcase — Unite 2022](https://www.youtube.com/watch?v=bUxzjmgLq0g) — 100+ titles
- [The Future of the Unity Game Engine — GDC 2026](https://www.youtube.com/watch?v=oPK5FmL7sO4) — current roadmap
- [Triple-i Initiative 2026 recap](https://unity.com/blog/Triple-i-Initiative-Showcase-recap-2026)

**Gotchas:**
- Licensing model has been re-litigated repeatedly — read the current terms before committing a commercial project
- Per-install Runtime Fee was rolled back in 2024, but reputational scar remains
- IL2CPP build times can be brutal on large iOS/console projects
- GameObject/Component model encourages prefab sprawl without discipline

---

## Godot

| Field | Value |
|-------|-------|
| **Radar** | 🟡 Trial |
| **Status** | Exploring |
| **Licence** | MIT — no royalties, no telemetry, no tiers |
| **Website** | [godotengine.org](https://godotengine.org) |
| **Languages** | GDScript (Python-like), C#, C++ via GDExtension |

**Why:** Best-in-class open-source engine. ~100MB self-contained editor, no account/login required. Scene-as-tree-of-nodes design is cleaner than Unity's GameObject/Component once you internalise it. 2D engine is a first-class citizen (not a 3D engine in disguise) — that's why it dominates indie 2D. 3D is shipping commercial titles now (Slay the Spire 2 in 2026).

**What you can build:**
- 2D roguelikes, deckbuilders, narrative games (Brotato, Slay the Spire 2, Case of the Golden Idol, Cassette Beasts, Dome Keeper)
- 3D indie titles — fidelity is now respectable post-Vulkan rewrite
- Game-jam prototypes (fastest iteration loop of any engine)
- Editor tooling and non-game apps (Godot itself runs on Godot)

**Showcase videos:**
- [#MadeInGodot Yearly Showreels playlist](https://www.youtube.com/playlist?list=PLeG_dAglpVo6EpaO9A1nkwJZOwrfiLdQ8) — official annual sizzle reels
- [Official Showcase page](https://godotengine.org/showcase/) — curated gallery
- [35 Famous Games Made with Godot](https://gamedesignskills.com/game-design/famous-godot-games/) — written gallery + clips
- [itch.io — Made With Godot](https://itch.io/games/made-with-godot) — playable browser demos
- [Steam growth report 2026](https://www.explosion.com/183705/godot-engine-shows-exponential-growth-on-steam-in-2026/) — exponential review-count growth

**Playable web samples (HTML5 export):**
- [itch.io — HTML5 games made with Godot](https://itch.io/games/html5/made-with-godot) — biggest browser-playable collection
- [itch.io — Godot-tagged HTML5](https://itch.io/games/html5/tag-godot)
- Notable browser-playable: **Dynamine**, **Welcome, Dear Human (Demo)**, **BACKSTORY**, **Sinner Maker**
- [Godot web export docs](https://docs.godotengine.org/en/latest/tutorials/export/exporting_for_web.html) — WebAssembly + WebGL2 pipeline
- For web-first engines see [domains/web-games.md](web-games.md)

**Gotchas:**
- Console export requires third-party publishers (W4 Games, Pineapple Works) — not direct
- C# support is solid but smaller community than GDScript — most tutorials assume GDScript
- 3D rendering still trails Unity/Unreal on high-end visual fidelity
- Asset store is much smaller than Unity's — expect to build more from scratch

---

## O3DE (Open 3D Engine)

| Field | Value |
|-------|-------|
| **Radar** | 🟡 Trial |
| **Status** | Exploring |
| **Licence** | Apache 2.0 — Linux Foundation governance |
| **Website** | [o3de.org](https://o3de.org) |
| **Languages** | C++, Lua, Python (tooling) |

**Why:** AAA-quality renderer (forked from Amazon Lumberyard / CryEngine lineage), modular Gem architecture, and corporate backing from AWS, Adobe, Huawei, Niantic, and Red Hat. Networked multiplayer, PhysX/Blast, audio, and large-world streaming are first-class. Apache 2.0 means no royalties and no commercial obligations.

**What you can build:**
- AAA-style 3D games and large open worlds
- Robotics simulation and synthetic data generation
- Cinema-quality 3D scenes and virtual production
- Networked multiplayer titles (built-in netcode)
- Industrial / aerospace / defence sims

**Showcase videos:**
- [Open 3D Engine YouTube channel](https://www.youtube.com/c/Open3DEngine) — official demos and dev streams
- [O3DE Basic Demo](https://www.youtube.com/watch?v=BEXlseH9FKI) — editor + sample scene walkthrough
- [Made with O3DE gallery](https://docs.o3de.org/docs/learning-guide/made-with-o3de/) — community projects
- [Sample projects docs](https://docs.o3de.org/docs/learning-guide/samples/) — runnable starter scenes (FPS, multiplayer, PhysX)

**Gotchas:**
- Steeper learning curve than Unity/Godot — C++ centric, Gem system is its own thing
- Smaller tutorial ecosystem; most learning comes from official docs and Discord
- Windows + Linux are first-class; macOS support trails
- Hardware requirements for editor are high (it's an AAA engine)

---

## Stride (formerly Xenko)

| Field | Value |
|-------|-------|
| **Radar** | 🟡 Trial |
| **Status** | Exploring |
| **Licence** | MIT — fully open source |
| **Website** | [stride3d.net](https://www.stride3d.net) |
| **Languages** | C# only (engine + scripts) |

**Why:** Pure-C# engine — no C++ in the runtime, full source readable and forkable. API is cleaner than Unity's (no `MonoBehaviour` boilerplate) and the editor feels familiar to Unity devs. Practical choice for C#-only studios that want Unity-like workflow without the licensing terms or closed source.

**What you can build:**
- 3D / 2D games in pure C# (Distant Worlds 2 — 4X space strategy)
- Custom rendering experiments (cel shading, voxel GI demos)
- Procedural terrain + water sims
- VR experiences on Windows
- Internal tooling that benefits from .NET ecosystem integration

**Showcase videos:**
- [Stride For Unity Developers](https://www.youtube.com/watch?v=u_ksFlHHXYU) — side-by-side workflow comparison
- [Official Games & Demos list](https://doc.stride3d.net/latest/en/community-resources/games-and-demos.html) — Rescue Drone, Procedural Terrain, Cel Shading, VXGI demos
- [Steam titles using Stride](https://steamdb.info/tech/Engine/Stride/) — including Distant Worlds 2
- [Awesome-Stride resource list](https://github.com/Doprez/Awesome-Stride) — community projects + clips

**Gotchas:**
- Small community — fewer Stack Overflow answers, expect to read source
- Mobile and console export less mature than Unity
- Editor stability and polish lag behind Unity/Godot
- Asset pipeline is less rich; bring your own DCC tooling

---

## Flax Engine

| Field | Value |
|-------|-------|
| **Radar** | 🟡 Trial |
| **Status** | Exploring |
| **Licence** | Source-available — free under $250k/yr revenue, paid above |
| **Website** | [flaxengine.com](https://flaxengine.com) |
| **Languages** | C# and C++ |

**Why:** Unreal-tier visual fidelity from a small, source-available engine with a Unity-like editor. Real-time DDGI global illumination, modern PBR, and a tighter iteration loop than Unity for many workflows. Source is on GitHub (readable + forkable), though not OSI-open-source.

**What you can build:**
- Photoreal arch-viz and product visualisation
- Racing / driving prototypes (Flax Web Racing)
- Indie 3D titles needing Unreal-level visuals without Unreal's complexity
- Tech-demo style real-time scenes with dynamic GI

**Showcase videos:**
- [Flax Engine — Features Showcase](https://www.youtube.com/watch?v=_KCl_m1IGp4) — official feature reel
- [Tech Demo 2022 — interactive arch-viz](https://flaxengine.com/tech-demo-2022/) — runnable DDGI scene
- [Tech Demo 2022 on Steam](https://store.steampowered.com/app/2138130/Flax_Engine__Tech_Demo_2022/) — free download
- [FLAX ENGINE Tutorial #00 — Features review & test drive](https://www.youtube.com/watch?v=iWGOgBfWNkQ)
- [Showcase forum](https://forum.flaxengine.com/c/showcase/13) — community projects

**Gotchas:**
- Source-available ≠ open source — read the EULA before commercial use
- Smallest community of the engines listed here — niche knowledge base
- Asset / plugin marketplace is thin
- Console export requires direct contact with Flax team

---

## Alternatives Considered (not added)

| Engine | Why not added |
|--------|---------------|
| Unreal Engine | Different tier — its own deep evaluation; would warrant a separate doc if I take it on |
| Bevy | Rust ECS engine, promising but pre-1.0 and missing editor — revisit later |
| Cocos Creator | Strong in Asia for mobile/web 2D; outside my current radar |
| GameMaker | Excellent for 2D but proprietary scripting language locks you in |
| Defold | Lua-based, free, great for mobile 2D — worth a look on next pass |

---

*Last updated: 2026-05*
