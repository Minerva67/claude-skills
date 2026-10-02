# 拉片方法笔记（Method Notes）

Hard-won details from running this workflow on real commercial videos.

## 环境准备（一次性）

No ffmpeg is needed. You need `yt-dlp` (download) and `opencv` (frame extraction):

```bash
pip3 install --quiet yt-dlp opencv-python-headless numpy
```

Installs can be slow — run in the background and continue once ready. Verify:
```bash
python3 -c "import cv2; print('cv2', cv2.__version__)" && python3 -m yt_dlp --version
```

If a package's console script isn't on PATH, always call the module form
(`python3 -m yt_dlp`) — it works regardless of PATH.

## 下载

Use `scripts/get_video.sh <url> <out-dir>`. It handles the metadata dump AND the
download with the flags that get past YouTube's SABR throttling.

If you download without the skill's script, the two flags that matter:
- `--extractor-args "youtube:player_client=android,ios,web"` — bypasses the
  "The page needs to be reloaded" / "forcing SABR streaming" failures.
- `-f "18/worst[ext=mp4]/worst"` — format 18 is 360p **with audio**, small and
  fast. 360p is enough to read on-screen text from montages. Big/high-res files
  get throttled to ~5-50 KiB/s and can take many minutes — avoid them.

Downloads can still be slow. Kick them off in the background and wait via a
Monitor/until-loop rather than blocking. For several videos, download them
one at a time in the background.

Non-YouTube / already-local video: skip the download, point extract_frames.py
straight at the file.

## 抽帧与看片

Pick `--step` by total duration so you get a reviewable number of montages
(each montage = 12 frames = one Read):

| 视频时长 | 建议 --step | 帧数 | montage 数 |
|---------|-----------|------|-----------|
| ≤ 60s   | 0.5s      | ~60-120 | 5-10 |
| 60-90s  | 0.75-1.0s | ~90 | ~8 |
| 2-3 min | 1.5s      | ~80-120 | ~8-10 |
| > 3 min | 2.0-2.5s  | scale down | keep ≤ ~12 |

```bash
python3 scripts/extract_frames.py --video <out>/vid.mp4 --out <out> --step 0.5
```

Then **Read each montage_N.png in order** to review the whole film. The
timestamp chips tell you where you are. Note every scene change, on-screen text,
color/tone flip, product/feature, and human reaction as you go.

## 看清细节：zoom 单帧

Montage cells shrink dense text (spec sheets, UI labels, fine print). When you
need exact wording — chip specs, prices, tool-call grids, slogans — **Read the
individual full-res frame** `frames/f_<TTTTT.T>.png` (e.g. `frames/f_105.0.png`).
Always verify verbatim: product names, numbers, and slogans are the credibility
floor of the whole teardown. Don't guess spec numbers from a blurry cell.

## 音频的诚实处理

cv2 extracts video only — you get **no audio transcript**. Never fabricate
voiceover or lyrics. Instead:
- Infer the audio's *nature* from the edit (text-driven films are usually
  music/SFX-only; long explainers may have VO).
- State it as an inference with a confidence level in the header ⚠️ and in
  section 六.
- If the user needs exact VO/lyrics/music ID, tell them that requires actually
  listening — offer it as a separate step (they can play the file, or you can
  try audio tooling if available).

## 按类型调整分析视角

The single most important judgment call: **what kind of film is this?** It sets
the whole analytical lens. Common types seen in practice:

- **品牌情绪大片** (e.g. Google Gemini): multi-climax emotional arc, real-people
  social proof, "歌词即文案", zero specs. Lens: emotion curve, cultural signals.
- **功能解说/操作演示** (e.g. Visa Click-to-Pay): teaches one action; jussive
  verb checklist; a concrete fake transaction for trust; "Approved" reassurance.
  Lens: information clarity, does the闭环 land.
- **B2B 硅片/规格发布** (e.g. AWS Trainium3, NVIDIA Vera): spec accumulation,
  silicon-to-datacenter zoom-out, term-precise copy. Lens: parameter delivery,
  scale narrative. NVIDIA-style long explainers often lead with an
  **anthropomorphized pain point** (little agent figures queueing/jamming).
- **C 端功能广告** (e.g. Amazon Lens):口语 hook, real results as typographic
  elements, repeated action loop across categories, 对仗 slogan. Lens: joy/ease.
- **捆绑/订阅发布** (e.g. Apple Creator Studio): "排版即演示" kinetic typography,
  verb+it, price + app lineup. Lens: type-as-demo, breadth.

State the type in the header and let it shape which sections carry the weight.

## 常见转场/手法词库（帮助命名）

形态变形 · 维度升级(2D→3D) · 词内嵌媒介 · UI→实拍→3D 三层切换 · 俯冲潜入 ·
闪白(情绪高峰) · 逐级放大 · 参数累加不清屏 · 首尾符号呼应 · 底色反转(黑↔白) ·
拟人化流动 · 声画同源 · 排版即演示 · 真实内容当排版元素。

## 工作流小结

1. `get_video.sh` → 拿到 metadata + vid.mp4（后台等下载）
2. 定 --step → `extract_frames.py` → 得到 montages + frames
3. 按序 Read 所有 montage，记录每个 beat
4. zoom 单帧核对所有屏幕文字/参数/slogan
5. 判定视频类型 → 定分析视角
6. 按 `output-template.md` 写完整报告（逐秒表 + 十节）
