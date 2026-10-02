# Codegen 路线：拉片 → 网页动画复原 prompt

适用：画面以**排版文字 / 数据可视化 / 示意图解 / UI 动效 / 几何 MG / 规格表 / 拟人抽象
动画**为主的片。产出 = 一条让 codegen 工具生成"自包含、可播放网页动画"的完整 prompt。

## 核心原则

1. **一条完整 prompt，一个 index.html，一条 master timeline。** 所有 beat 锚绝对时间码（ms）。
2. **招牌机制第一优先级。** 在 prompt 开头一句话声明它，并在时间轴里逐拍写死怎么动——
   不能用统一 fade 糊过去（例如 Apple 的每个动词必须按词义动：Upscale=马赛克→锐化、
   Scrap=落进垃圾桶、Move=字母四散）。
3. **屏幕文字一字不差照抄。** slogan、规格参数、UI 文案全部 verbatim。
4. **参数/清单"累加不清屏"** 时要在 prompt 里明写（append，never clear until scene change）。
5. **长保持要明写。** 规格片可能让一张表静止 ~20s（尊重专业观众逐条阅读），否则会被默认
   快切覆盖。
6. **诚实标注素材边界。** 照片/硬件/真人镜头做成 `[IMG:...]` 内联槽或"透明样机+代码画屏"，
   其余全代码；每个 `[IMG]` 必须能退化成渐变/线稿占位，保证没素材也能整片播完。

## 模板（填空后即为可投喂的 prompt）

```
Build a single self-contained, playable web animation that faithfully recreates
[BRAND]'s [N]-second "[TITLE]". Output ONE index.html with all CSS/JS inline (GSAP via
CDN allowed for the timeline; otherwise Web Animations API). Autoplay, loop, and expose
play/pause + a scrub slider. [ONE-SENTENCE SIGNATURE MECHANIC — the film's core visual
device, stated as the thing to reproduce precisely].

=== GLOBAL DESIGN SYSTEM ===
- Stage: [1920×1080 16:9 | 1080×1920 9:16], letterboxed to fit any viewport, centered.
- Background: [base bg — e.g. pure black #000 throughout except final lockup].
- Total duration [N]s, driven by ONE master timeline (GSAP timeline or a single rAF clock
  in ms). All beats below are keyed to absolute timecodes — honor them.
- Palette (color is used ONLY as information highlight; base is [white/gray line-art on
  black | dark rounded type on pastel | ...]):
  · [role = #hex, when it appears] (list each accent + its meaning)
- Type: [headlines font-family stack]; [specs/labels in monospace, joined by " | "].
- Motion feel: [pace, easing]; [what bursts color vs returns to base].
- Pacing: [~Xs/beat; where it fast-cuts; where it holds long — name the long holds].

=== ASSET SOURCING ===
Nearly everything is pure code (SVG/Canvas): [list the code-drawn parts]. A few beats need
imagery (marked [IMG: ...]) — source each however the build allows (generate, or find a
suitable royalty-free image/render/mockup) and composite it in. Rules:
- DEVICE SHELLS (phone/laptop/tablet): use a transparent-screen mockup as the frame, then
  render the on-screen UI with CODE into the screen rectangle (text stays crisp and
  animatable). Never bake screen contents into a still image.
- Fake all "camera moves" with CODE on the image (rotation/zoom/tilt/parallax via CSS
  transforms; a dive/plunge via layered parallax + CSS filter blur+scale).
- Every [IMG] MUST degrade to a tasteful gradient/line-art fallback — never a gray box.
  The film must play end-to-end regardless.

=== TIMELINE (absolute timecodes) ===
[ACT NAME — one line describing the act (timecode range)]
0:00–0:0X [beat: what forms/appears/animates; on-screen text VERBATIM; how it moves]
0:0X      [next beat ...]
... (walk the whole film act by act, beat by beat, from the 镜头表)
[When a spec/list accumulates: say "append; never clear until the scene changes".]
[When a shot holds: say "hold ~Ns (let the audience read)".]

=== SOUND (optional, if WebAudio is supported) ===
[music bed vibe; per-beat SFX matched to meaning; any audio-visual sync moments].
No voiceover / [or: leave room for VO if the film likely has one].

=== TECHNICAL REQUIREMENTS ===
- One master timeline; all beats keyed to the timecodes above (ms).
- Autoplay + loop; play/pause + scrubber wired to timeline progress.
- Fitted [WxH] stage scaled to viewport; no horizontal scroll; text uses vw/clamp.
- [Repeated motif] is a reusable code component — build once, reuse across [places].
- Prefer SVG + CSS (see technique map). GPU-friendly.
- Clean, commented code. Every [IMG] degrades to a fallback so the film plays end-to-end.
```

## 技术 → 效果 对照（写进 TECHNICAL REQUIREMENTS，帮 codegen 选对手段）

| 想要的效果 | 让 codegen 用 |
|---|---|
| logo/图标描线出现、手写笔迹、蚂蚁线选区、连接树生长 | SVG `stroke-dasharray` draw-on |
| 液态/沙砾/AI 生成质感文字 | SVG `feTurbulence` / `feDisplacementMap` |
| 俯冲潜入 / 数据隧道 | 分层 parallax + CSS `filter: blur()` + `scale()` |
| 芯片旋转、逐级拉远、跨设备切换 | CSS `transform`（rotate/scale/translate）驱动"假运镜" |
| 粉彩流动底 | 动画化 `conic-gradient` / `linear-gradient` |
| 商品卡/UI 卡弹出 | spring easing 的 `transform` 弹入 |
| 马赛克→锐化（upscale 演示）| CSS `filter: blur()`+`contrast()` 左右分区过渡 |
| 逐区点亮（芯片楼层图/网格）| 对分区块动画化 `fill`/`opacity`/`filter` |
| 大量拟人小人流动+排队+环流 | Canvas 或多个小 SVG sprite + 路径 + 队列/拥堵状态机 |

## 精简实例（NVIDIA 示意图型，节选，供 few-shot 参照）

```
Build a single self-contained, playable web animation that faithfully recreates NVIDIA's
174-second "Vera — The CPU for Agents" technical explainer. Output ONE index.html ... The
signature mechanic is ANTHROPOMORPHISM: a crowd of little human figures represents agentic
tasks flowing between GPU and CPU — queuing/congesting at the overloaded (red) Traditional
CPU, then flowing freely once Vera replaces it. Build that as a real code-driven agent
flow, not a canned clip.
=== GLOBAL DESIGN SYSTEM ===
- Stage: 1920×1080 16:9 ... Pure black bg (#000) for the ENTIRE film EXCEPT the final logo
  lockup, which inverts to WHITE.
- Color ONLY as highlight: agents=warm gray; ALERT RED (#FF3B30) used ONCE, only for the
  congested Traditional CPU; NVIDIA green (#76B900) only at the final logo ...
- Specs in monospace, joined by " | ", ACCUMULATING and never clearing until scene change.
- This is a SLOW film. Respect long holds — especially the ~20s static spec sheet.
=== TIMELINE ===
0:24–0:28.5 The Traditional CPU turns ALERT RED; little figures PILE UP in a long queue
  (the sole negative beat). 0:30 red chip replaced by a "Vera CPU" label; figures disperse.
0:31.5–0:44 figures CIRCULATE smoothly in a big loop between GPU and Vera ...
1:43.5–2:04 FULL Vera CPU hero shot [IMG: dark substrate with green/blue die] held ~20s,
  full spec sheet animated in line by line then STATIC: "88 NVIDIA Custom Olympus Core ..."
=== TECHNICAL REQUIREMENTS ===
- The agent-figure flow is a real code system: a path spawner + a queue/congestion state at
  the CPU that switches from "jammed"(red, piling up) to "free-flowing"(looping) ...
```

## 交付前 checklist

- [ ] 开头一句声明了招牌机制？
- [ ] 画幅（竖/横）写死且正确？
- [ ] 一条 master timeline + 所有 beat 有绝对时间码？
- [ ] 屏幕文字（slogan/规格/UI 文案）一字不差照抄？
- [ ] 累加不清屏 / 长保持 这类节奏特例明写了？
- [ ] 每个 `[IMG]` 有退化占位规则？设备类用"样机+代码画屏"？
- [ ] 重复动作母题做成可复用组件？
- [ ] 给了 autoplay/loop/scrub + 响应式 + 优先 SVG/CSS 的技术要求？
