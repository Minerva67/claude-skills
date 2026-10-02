# 文生视频路线：拉片 → 逐镜生成 prompt

适用：画面以**实拍真人 / 真实环境 / 情绪品牌大片 / 写实 b-roll**为主的片。产出 = 一套
喂给 Veo / Seedance / LTX 等模型、逐镜抽卡再拼接的 prompt。

## 先讲清的现实约束（一定写给用户）

- **文生视频模型无法可靠渲染精确 UI 和可读文字。** 精确界面、代码编辑器、准确 slogan 字幕
  硬生成会得到"糊成一团的假 UI + 乱码文字"。这类镜头→标 `[COMP]`，建议真实录屏/高保真
  截图叠层，prompt 只负责生成载体环境或抽象动效底。
- **单条时长 4–8s，不是 1s。** 原片 1 秒/镜头的密度靠剪辑，不是单条 1 秒素材。把镜头表
  归并成 **~10–14 条可生成片段（4–6s/条）**，拼接时再按原片节奏切碎。
- **精密 MG 镜头**（logo 变形、pill 展开等）别交给视频模型——标注走 After Effects/Rive。

## 结构

### 1) 全局风格前缀（Master Style Block）——拼在每条 clip 前面，保证一致性

```
STYLE: [genre, e.g. premium tech brand commercial] aesthetic. [mood adjectives].
Shot on [camera, e.g. ARRI Alexa], [lens], shallow depth of field. [lighting]. Color
science: [look]. Palette — [when tech: ...; when real life: ...]. [fps], subtle cinematic
motion blur. [immaculate/uncluttered]. No on-screen captions unless specified.
```

### 2) 通用负向提示（Negative）——每条都带

```
NEGATIVE: garbled text, distorted UI, unreadable interface, warped hands, extra fingers,
deformed faces, watermark, logo artifacts, low-res, jpeg artifacts, oversaturated,
flickering, uncanny expressions, cluttered background, text errors.
```

### 3) 逐条 clip prompt（按幕分组，每条 4–6s）

每条给：镜头类型 + 主体 + 动作 + 场景 + 光 + 镜头运动 + 色彩 + 情绪 + 转场，并打标签：
- **`[GEN]`** = 模型能直接抽卡的实拍/3D 类（人物、环境、运镜、地图俯冲）——模型强项。
- **`[COMP]`** = UI/文字类，建议真实素材叠层；prompt 只出载体环境或抽象底。

```
CLIP NN [GEN|COMP] — [what it is] ([timecode] / [Ns])
[cinematic prompt: shot type, subject, action, setting, lighting, lens, camera move,
palette, mood, transition-in/out]
```

### 4) 拼接 / 音频 / 版权（结尾补）

- 拼接：按原片时间码把 4–6s 素材切碎到目标节奏；标"反应镜头"当呼吸点。
- 音频：TTS 台词 cue（谁在何时说什么）；音乐情绪曲线。
- **版权**：若原片用有版权音乐（如 Google 用 Jay-Z），提示商用需授权；测试可用 similar-
  vibe 替代，但保留"歌词呼应叙事"的灵魂。

## 精简实例（Google 情绪大片型，节选）

```
STYLE: Premium tech brand commercial, Google/Gemini launch film aesthetic. Optimistic,
cinematic. Shot on ARRI Alexa, 35mm, shallow DoF, soft natural light, gentle bloom. DUAL
PALETTE — tech: near-black #111 + blue→purple→pink gradient glow; real life: warm daylight,
soft pastels. 24fps. NEGATIVE: garbled text, warped hands, deformed faces, watermark...

CLIP 04 [GEN] — overhead desk with Pixel (0:19 / 4s)
Overhead top-down shot of a bright wooden desk. A hand holds a light-blue Pixel phone
pointing its camera at a red apple beside a child's drawing, sticky notes around. Warm
daylight, soft shadows, shallow focus on the phone. Gentle handheld motion. Authentic.

CLIP 02 [COMP] — Gemini sparkle anchor (0:08–0:14 / 5s)  [UI cards → overlay real screen
recording; generate only the glowing sparkle anchor]
Macro close-up of a single glowing four-pointed star icon floating in pure black space,
blue-purple-pink gradient glow, soft particles drifting, gentle pulsing. Slow push-in.
```

## 交付前 checklist

- [ ] 开头讲清了"UI/文字不可靠 + 单条 4–8s"两个约束？
- [ ] 有 Master Style Block（拼在每条前）+ 统一 Negative？
- [ ] 镜头表归并成 ~10–14 条 4–6s clip，而不是逐秒 60 条？
- [ ] 每条打了 `[GEN]`/`[COMP]` 标签？UI/文字镜头建议叠层？
- [ ] 精密 MG 镜头标注"走 AE/Rive，别交给视频模型"？
- [ ] 补了拼接 + TTS/音乐 + 版权提醒？
- [ ] 人物/场景多样性写进了相关 clip？
