---
name: video-lapian
description: >-
  Produce a deep shot-by-shot teardown (拉片 / 逐秒镜头表 + 十节分析) of a
  commercial, ad, or product-launch video — the kind of competitive/creative
  analysis where you break the film into per-beat shots and analyze visual
  language, pacing, copy, music, transitions, emotion curve, and a reusable
  script template. Use this WHENEVER the user gives a video URL (YouTube etc.)
  or local video file and asks to 拉片 / 拉这个片 / 逐帧或逐秒分析 / 分镜分析 /
  "break down this ad" / "shot-by-shot" / "分析这支广告/宣传片/发布视频" /
  teardown / competitive video analysis — even if they don't say the word
  "拉片". Also triggers when they want to study a reference video to inform
  their own product/marketing video. Downloads the video, extracts frames,
  and writes the full structured report. Default output language 中文.
---

# 视频拉片分析（Video 拉片 / Shot-by-Shot Teardown）

## 这个 skill 做什么

把一支商业/广告/发布类视频拆成**逐秒镜头表 + 十个分析章节**的深度拉片报告。
产出既是"这支片每一拍在干什么"，也是"它凭什么这么做、你能偷师什么"。

核心难点是：你无法直接"看"视频。所以流程是 **下载 → 抽帧 → 拼图速览 → 单帧
核对 → 按固定结构成文**。全程忠于实际画面，不臆造。

## 前置依赖

需要 `yt-dlp`（下载）和 `opencv`（抽帧），**不需要 ffmpeg**。若未安装：
```bash
pip3 install --quiet yt-dlp opencv-python-headless numpy
```
安装可能较慢——放后台跑，就绪后再继续。详见 `references/method-notes.md`。

## 工作流

按顺序做。scripts 目录里的两个脚本封装了最容易踩坑的部分（YouTube 反爬、
无 ffmpeg 抽帧），优先用它们。

### 1. 识别 + 下载视频
```bash
bash scripts/get_video.sh "<url>" <workdir>
```
会打印标题/时长/频道/观看量/描述（写报告 header 用），并把 360p 带音频的
`vid.mp4` 存到 `<workdir>`。下载可能慢，**放后台，用 Monitor 或 until-loop 等**，
别死等。多支视频就一支一支后台下。

若是本地文件或非 YouTube，跳过下载，直接对文件抽帧。

### 2. 抽帧 + 拼图
按时长选 `--step`（≤60s 用 0.5；2-3min 用 1.5；见 method-notes 的表）：
```bash
python3 scripts/extract_frames.py --video <workdir>/vid.mp4 --out <workdir> --step 0.5
```
产出 `<workdir>/frames/f_*.png`（单帧全分辨率）和 `<workdir>/montage_*.png`
（4×3 拼图，每格带黄色时间戳）。

### 3. 速览全片
**按顺序 Read 每一张 montage_N.png。** 一张拼图=12 帧=一次 Read，能高效扫完
整片。边看边记：每个镜头切换、屏幕文字、色调翻转、出现的产品/功能、真人反应。

### 4. 核对细节（关键）
拼图会把密集文字（规格表、UI 标签、价格、slogan）压小。凡是需要**逐字准确**的
地方——芯片参数、价格、工具网格、口号——**Read 对应的单帧** `frames/f_<时间>.png`
（如 `frames/f_105.0.png`）放大确认。屏幕文字的准确性是整份拉片可信度的地基，
不要靠糊掉的拼图猜数字。

### 5. 判定视频类型
成文前先定性：这是**品牌情绪片 / 功能演示 / B2B 规格发布 / C 端功能广告 /
捆绑发布**里的哪种？类型决定分析视角与各章节的权重。见 method-notes
"按类型调整分析视角"。

### 6. 写报告
严格按 `references/output-template.md` 的结构成文：
- **一、逐秒镜头表**：分幕，6 列（时间｜画面内容｜景别/角度｜视觉元素｜音频｜分析），
  分析列点出"为什么"。
- **二~十节**：产品展示策略 / 视觉设计语言 / 节奏与信息密度 / 场景与人物 /
  音乐与声音 / 文案策略 / 转场 / 情绪曲线 / 可参考模板。
默认中文输出（除非用户要英文）。

## 铁律

- **忠于所见**：所有画面描述来自实际抽帧。看不清就 zoom 单帧，别臆造。
- **文字逐字准确**：产品名、参数、slogan、UI 标签必须与画面一致。
- **音频诚实**：cv2 抽不出音频。无法转写就在 header ⚠️ 和第六节标注"推断 +
  置信度"，绝不虚构旁白或歌词。若用户要精确 VO/音乐 ID，说明那需要实际听音，
  作为单独一步提供。
- **答"为什么"**：每个分析回答策略意图，而非仅描述画面。第十节的"可复用模板"
  通常是用户最想要的——因为多数拉片是为竞品分析/给自己产品做参考。

## 参考文件
- `references/output-template.md` — 报告的精确结构与章节骨架（成文时必读）。
- `references/method-notes.md` — 下载/抽帧/看片的踩坑细节、类型分析视角、
  转场词库。
- `scripts/get_video.sh` — 识别 + 下载（含反 SABR 的 yt-dlp 参数）。
- `scripts/extract_frames.py` — 抽帧 + 拼图（OpenCV，无需 ffmpeg）。
