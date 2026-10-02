# Deletion rules — what to cut, what to keep

Goal: from a video-generation prompt, delete every trace of *technical implementation /
render method / model paradigm*, and keep only the creative content — so the prompt reads
as pure intent and doesn't favor any particular video model.

## The one hard rule
**Only delete. Never rewrite, paraphrase, reorder, or add characters.** Every kept word
must be byte-for-byte identical to the original (case, punctuation, spaces, line breaks,
Markdown). Fidelity beats fluency — a slightly rough sentence after a cut is fine. The only
"extra" you may remove is whitespace/separators immediately orphaned by a deletion (so you
don't leave `·  ·` or a blank line); that is still deletion.

## Delete — A. Paradigm / model words
Whole word, all cases and compounds:
`diffusion`, `Diffusion`, `code-gen`, `Code-gen`, `codegen`, `code-generation`, `hybrid`,
`Hybrid`, `video-diffusion`, `diffusion-generated`, `Codegen-dominant`, `code-drawn`, etc.
- `diffused` is conditional: delete when it means "a diffusion-generated plate/world/
  environment" (common in hybrid/compositing context — "the diffused facility", "a diffused
  world"); keep the ordinary physical adjective ("diffused light", "softly diffused glow").

## Delete — B. Bracket render tags
`[CODE]`, `[Code-gen]`, `[DIFF]`, `[Diffusion]`, `[HYB]`, `[Hybrid]`, `[Hybrid + type]`,
`[3D]`, `[2D]`, `[CG]`, `[COMP]`, and similar — together with an orphaned adjacent
separator. Example: `SHOT 2 · [HYB] · 0:05–0:11` → `SHOT 2 · 0:05–0:11`.

## Delete — C. Engine / tech-stack / model names (and the parens around them)
`Remotion`, `React-Three-Fiber`, `R3F`, `GSAP`, `D3`, `Three.js`, `WebGL`, `canvas`,
`shader`, `KaTeX`, `Lottie`, `Pixi`, `p5`, `Blender`, `Houdini`, `Cinema4D`, `Flux`,
`SDXL`, `Runway`, `Sora`, `Kling`, `Veo`, etc. Delete the wrapping parenthetical when it
exists only to list these: `(Remotion / React-Three-Fiber / GSAP timeline, …)`,
`(Three.js / R3F + GSAP)`, `(Remotion + D3)` → gone (including the leading space).

## Delete — D. Whole technical passages / sentences
- Tooling declaration: `> Paste … into a code-generation video tool (…).` — delete the
  sentence, but keep any pure spec that follows it (`Target render: 1920×1080, 30fps…`).
- Render-method definition blocks: `Form: 3D + Diffusion Explainer`; `Purpose: Feed this
  file … into a hybrid render pipeline. Each scene is tagged with a render method:` plus the
  following `[Code-gen] — …`, `[Diffusion] — …`, `[Hybrid] — …` definition lines.
- Paradigm-tagged tech params: `FPS: 60 (code-gen) / 24 (diffusion)` → `FPS: 60 / 24`.
- Whole technical sections/labels (title through the end of that section/bullet):
  `**Stack:** …`, `**Diffusion usage (…):** …`, `2. Technical Notes`, `Code-gen stack: …`,
  `Diffusion approach: …`, `Production note (…): …` when it's about pipeline/engines,
  `**Render notes for code-gen:** …`.
- Compositing / pipeline law lines (hybrid decks): `Compositing law: …`, `Composite: …`,
  `Diffusion plate + CG/3D overlay`, `[HYB]: 5, 10 → diffusion plate first; …`.
- Master-prompt technical sentences: `Use code-gen (Three.js / R3F + GSAP) for all precise
  construction …`, `Use diffusion (text-to-video) for warm human framing …` — delete the
  "use X tech to do Y" technical directive; if the whole sentence is only about
  implementation, delete the whole sentence.
- Technical skeleton phrases: `· Shot List`, `render method`, `render pipeline`,
  `hybrid render pipeline`.

## Delete — E. Per-shot / per-beat technical prefixes (keep the creative text after)
Delete the label, keep the picture it introduces:
- `**3D beat:** R3F scene. A low-poly isometric block model…` → `A low-poly isometric block model…`
- `Scene 1 · The pop (0:00–0:25) · [Hybrid]` → `Scene 1 · The pop (0:00–0:25)`
- `Base [Diffusion]: close overhead of hands pressing a paper button…` → `close overhead of hands pressing a paper button…`
- `**2D motion-graphics:**` / `**3D → 2D transition:**` / `**Data-viz 3D:**` /
  `**Signature 3D data-viz:**` / `**3D → sheet:**` / `**Return to Scene 1's 3D model:**` →
  delete the label, keep the following prose.

A bold label is *technical* (delete) when it names a render dimension/technique/pipeline
(3D, 2D, beat, motion-graphics, transition, data-viz, flow-graph, value-flow, sheet, model,
Stack, Diffusion, Render notes, R3F, CG, overlay, composite, plate). It is *creative* (keep)
when it names picture/story/information.

## Keep — verbatim, never touch
- VO lines, on-screen text, `**Look:** / **Look & feel:** / **Motion grammar:** / **Title:**
  / **On-screen…:** / **VO:** / **Data shown…:** / **Layout:** / **End card:** / **Callback:**
  / **The reveal:** / **Privacy note…:** / **FAST/SLOW…:** / **Animated formula + timeline:**`
  and other content labels.
- Palette + hex, camera, lighting, type, scene titles + timecodes (delete only a trailing
  ` · [Tag]`), story copy, `Source:` lines, `Runtime/Aspect/Tone` specs.
- Ordinary descriptive "3D/2D/overhead" words in prose (e.g. "an open 3D box", "3/4 orbits")
  — these describe the picture, not the tech. Only the *tags* and *tech labels* go.

## Worked micro-examples
Input:  `Techniques…: [CODE] the linked-gauge dashboard … (Remotion + D3) · [3D] the reveal of the wiring · [DIFF] the control-room plates`
Output: `Techniques…: the linked-gauge dashboard … · the reveal of the wiring · the control-room plates`

Input:  `- **Stack:** Remotion (React) for layout … ~145 wpm.`  (whole bullet)
Output: (bullet deleted entirely)

Input:  `reveal the full lit center against the diffusion dusk plate.`
Output: `reveal the full lit center against the dusk plate.`   (delete only the paradigm word)

## Delete — F. Front-end / "build-it-as-code" implementation
Some prompts ask for the film to be *built as code* (a self-contained web animation, an
`index.html`, a GSAP/Canvas/SVG piece) instead of generated by a video model. For a fair
cross-model set, strip the "build it with front-end code" layer too — keep only what the
film looks and sounds like. Delete:
- **Output / tooling declarations:** "Build a single self-contained, playable web
  animation", "Output ONE index.html with all CSS/JS inline", "(GSAP via CDN allowed;
  otherwise Web Animations API)".
- **Animation tech & APIs:** GSAP, Web Animations API / WAAPI, requestAnimationFrame / rAF,
  Three.js, Canvas, SVG *as a tool*, CSS transforms/filters, `feTurbulence`,
  `stroke-dasharray`, WebAudio, CDN, `tl.add(…)`, "rAF clock in ms".
- **Delivery / runtime controls:** autoplay, loop, play/pause button, scrubber / scrub
  slider, "One master timeline (… in ms)", "stage scaled to viewport", "letterboxed to fit
  any viewport", "no horizontal scroll", "text uses vw/clamp", "GPU-friendly".
- **Build markers & how-it's-drawn notes:** the `[IMG: …]` marker *brackets* (keep the
  description inside — that's the picture: `[IMG: white sneaker]` → `white sneaker`);
  "drawn by CODE", "code-drawn", "screen UI drawn by code", device-shell/mockup technical
  notes, "degrade / fall back to a gradient" instructions.
- **Whole technical sections:** `=== ASSET SOURCING ===` and `=== TECHNICAL REQUIREMENTS ===`
  in their entirety — they are only about how to build/source, not what the film is.
- **"Use technique X for effect Y" → delete the technique, keep the effect:** "SVG
  feTurbulence for the sand texture" → "the sand texture"; "stroke-dasharray for marching
  ants and handwriting draw-on" → "marching ants and handwriting draw-on".

**Keep** (verbatim): the timeline beats and timecodes; every on-screen word/verb and *how it
animates* as creative intent ("letters FLIP in on their axis", "chaos→order", "marching-ants
selection marquee", "letters SCATTER"); palette + hex; camera/mood; story; and the creative
parts of `=== SOUND ===` (music feel, per-beat SFX intent) — deleting only its technical
conditions ("if WebAudio is supported", "WebAudio"). Aspect/format like "1920×1080, 16:9" or
"1080×1920 portrait" is creative framing — keep it; delete only the "scaled / letterboxed to
viewport" implementation wrapped around it.
