# 路由规则：什么时候 code-gen，什么时候 diffusion，什么时候手搓 / 等素材

四种生产方式，每镜必标一种（可组合），并给稳定性 稳/中/险 + 一句理由。
术语对照：**CODE** = code-gen / codegen / cog-video / 程序化动效（混合模型里精确图形那一路）；
**DIFF** = diffusion / 视频生成模型出的实拍质感片段。用户口头可能混用，标签统一用 CODE / DIFF。

## 决策顺序（从上往下问，第一个"是"就定）

1. **画面里有必须逐字/逐数精确的东西吗？**（文字、数字、UI、图表、色卡、品牌排版、
   传感器/数据可视化）→ **CODE**。程序化图形是混合模型的主场，换文本/色值即新版本，
   100% 可复现。
2. **画面是"产品本身长什么样"且客户会盯外形吗？**（产品英雄镜头、三件套定格）→
   **AE 一次性**（或 3D）。生成模型会漂外形；手搓一次母版永久复用。需要客户渲染图/工程图。
3. **画面是客户独有的内容吗？**（游戏画面、App 录屏、真实 UI）→ **素材**。没素材前
   标"险"，只能用官网插画做视差顶一下；拿到即转"稳"。
4. **画面需要"实拍的空气"——真实光线、皮肤、织物、环境——且没有可用素材吗？**
   → **DIFF**。但只用于情绪/温度，不承担结构，可换可删。
5. **既要实拍空气又要精确图形贴在上面？**（热力图贴板面、字幕叠实拍、电视换屏）→
   **DIFF + CODE 合成**。底板 DIFF、元素 CODE、贴合由 AE 跟踪；若后期要全生成，
   给一个"纯 CODE 保底写法"（如把叠加改成图形满屏）。

## 各方式的稳定性与边界

| 方式 | 稳定性 | 何时用 | 别用来 |
|---|---|---|---|
| CODE 程序化 | 稳 | 标题卡、hook 卡、色卡节拍器、字幕、数据卡、热力图/波纹元素、UI 示意、收尾 CTA | 表现真实光线/皮肤/材质 |
| DIFF 扩散/视频生成 | 中 | 顶视脚部、背影、侧面、地面微距、环境定场；单镜 ≤2–4s；每镜 2–3 备选 | 正脸特写、多人同框清晰、手指精细交互、产品外形必须准的镜头、承担叙事结构的镜头 |
| AE 一次性 | 稳（做一次） | 产品英雄、精确外形三件套、复杂合成跟踪 | 每支都要重做的东西（那说明该 CODE 化） |
| 素材 | 取决于客户 | 游戏/App 画面、真机实拍 | 拿不到时别硬生成——生成的游戏画面会被客户认出不是自家的 |

## DIFF 镜头怎么写才稳
- 头部固定三段常量：场景常量（陈设逐项）、产品常量（尺寸/材质/无按钮无屏/线缆处理）、
  质感常量（"photorealistic live-action footage… NOT illustration / vector / cartoon /
  3D-render look / motion graphics; no text, no logo, no UI"）+ 负面清单（正脸、多肢、
  变形、产品变形、文字、水印、抖动、快动作、眩光）。
- 人物只写背影/顶视/侧面/脚部；写清衣着发型以便跨镜一致；同批次固定 seed 系列。
- 屏幕内容不靠生成：电视/手机屏写成"plain soft glow, to be replaced in post"。
- 按景别做 5 类模板（顶视脚部 / 背影看屏 / 地面微距 / 侧面反应 / 环境定场），换动作句。

## 在最终 prompt 里怎么"逼"路由（不点名模型/引擎）
- Layer A（→ diffusion）：只用质感词——real skin, real fabric, wood grain, natural
  daylight, shallow DOF, film grain, "must NOT be rendered as illustration/vector/
  cel-shaded/3D-cartoon/motion-graphic style — must read as footage shot with a camera"。
- Layer B（→ code-gen）：vector-sharp, digit-accurate, text identical letter for letter,
  counters roll and lock, charts draw in, pinned in correct perspective。
- Layer C（→ 产品渲染）：physically-based, studio softbox reflections, real material
  response，只用于一处。
- 每镜前缀 `[LIVE]` `[GRAPHIC]` `[GRAPHIC over LIVE]` `[PRODUCT RENDER]` `[GAME]`，
  Hard Constraints 里列出哪些镜号必须是实拍质感、单镜上限秒数。
- 若引擎内部有确定生效的渲染标签，让用户自己加到镜头开头，结构不动；prompt 本身不依赖它。

## 汇总口径（交付时说清）
- 按**内容时长**：CODE + DIFF 通常能出 2/3；
- 按**活儿**：合成/跟踪/换屏/调色是 AE 的，混合模型天生不做；
- 真正的分水岭是 DIFF 桶能否从引擎里出来——出得来引擎是主生产者，出不来就只剩排版卡。
  实测时只测 DIFF 桶的 3–5 个代表镜头，看是否被降级成图形、产品是否漂、节奏是否被 TTS 拉平。
