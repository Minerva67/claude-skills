---
name: lapian-to-prompt
description: >-
  把一份拉片分析（逐秒镜头表 + 十节分析）转成一条可直接投喂的"视频复原提示词"——
  先自动判断该走 codegen（HTML/CSS/JS 动画，适合排版/图解/数据可视化/UI 动效/几何 MG 类）
  还是文生视频（Veo/Seedance/LTX 逐镜，适合实拍人物/真实场景/情绪大片），或两者混合
  （codegen + [IMG] 素材槽）。Use this WHENEVER the user has a 拉片 / shot-by-shot
  teardown / 逐秒镜头表 / 分镜分析 and wants to 复刻 / 复原 / 重现 / recreate that
  video, or says things like "把这个拉片转成 prompt" / "用 codegen 复刻这个视频" /
  "把这个分析变成能生成视频的提示词" / "reproduce this ad" / "turn this teardown
  into a video-gen prompt" — even if they don't name the target tech. This is the
  DOWNSTREAM step that pairs with the video-lapian skill (which produces the
  teardown): once a teardown exists, use this to turn it into a reproduction
  prompt. Also trigger when the user pastes a detailed 镜头表 / shot list and asks
  how to recreate that video with code or a video model. Default output 中文 框架 +
  英文 prompt 正文。
---

# 拉片 → 视频复原提示词（Lapian → Repro Prompt）

## 这个 skill 做什么

输入一份**拉片报告**（逐秒镜头表 + 视觉/节奏/文案/音乐等分析），输出一条**可以直接
投喂给生成工具、用来"原样复刻"这支片的提示词**。

它的价值不在于把镜头表翻译一遍，而在于三件事：
1. **片型分流**——判断这支片该用 codegen 还是文生视频复原（选错技术，成片必崩）。
2. **抽取招牌机制**——每支好片都有一个核心视觉装置，复原时它是第一优先级。
3. **产出一条完整、自洽、带绝对时间码的 prompt**，而不是零碎片段。

> 上游是 `video-lapian`（把视频拆成拉片报告）。如果用户只给了视频 URL、还没有拉片，
> 先用 `video-lapian` 产出报告，再回到本 skill。如果用户已经贴了镜头表/分析，直接开始。

---

## 第一步：片型分流（最重要，先做这个）

看拉片报告的画面主体，判断复原技术。**规律：画面越"抽象/示意/排版"，codegen 还原度
越高、越接近帧级还原；越"写实/实拍"，越该交给视频模型。** 别把两者搞反。

| 画面主体信号 | 复原路线 | 为什么 |
|---|---|---|
| 黑/白/纯色底 + 排版文字 / 数据可视化 / 示意图解 / UI 动效 / 几何 MG / 规格表 / 拟人抽象小人 | **codegen** | HTML/CSS/JS 能精确控制文字、时间轴、动效，还原度最高 |
| 实拍真人 / 真实环境 / 情绪品牌大片 / 写实 b-roll / 生活场景 | **文生视频** | 代码画不出照片级真人与实景；交给 Veo/Seedance/LTX |
| UI 界面演示（表单/按钮/App 截屏）| **codegen + 合成** | 代码搭结构+动效+文字，真实 UI 用录屏/高保真截图叠层 |
| 芯片/设备等硬件英雄镜头 | **codegen + [IMG]** | 代码搭骨架与"假运镜"，硬件用渲染图/样机占位 |

**分流不是非黑即白，一支片可以拆开处理：**
- 以 codegen 为主的片里，少数照片镜头 → 标成 `[IMG]` 素材槽。
- 以文生视频为主的片里，个别精密 MG 镜头（如 logo 变形）→ 标注"这段走 After
  Effects/Rive，不要让视频模型生成"。

**判断成后，明确告诉用户你选了哪条路线、为什么**，再生成 prompt。若用户已指定路线
（"我要 codegen 版"），尊重用户，但如果该片明显不适合，务必先提示风险再照做。

技术分流之外还要判**片型**（品牌情绪片/功能教学片/排版发布片/硬件规格片/深度技术
解说/C端功能广告/概念能力片/SaaS demo 片，共 8 型）——每型有各自的成功实践、节奏
纪律与情绪目标，**不可跨型混用**。判定表与各型 playbook 见 `references/patterns.md`，
生成或迁移 prompt 前先读它，核对该型招牌实践是否都落实。

竖屏还是横屏，从拉片语境推断并写死在 prompt 里（别忘了，这里最容易踩坑）：
- C 端 / 社交 / 手机功能广告、画面以竖屏手机 UI 为主 → **9:16 竖屏（1080×1920）**
- 品牌大片 / 发布会 / B2B 技术片 → **16:9 横屏（1920×1080）**

---

## 第二步：抽取招牌机制 + 关键参数

从拉片报告里读出下面这些，作为 prompt 的骨架。重点是**招牌机制**——每支片总有一个
"最聪明的一招"，复原时必须逐帧实现，不能用通用 fade 糊过去。

- **招牌机制**：读报告的"视觉设计语言 / 转场 / 核心手法"章节，找出那**一个**核心装置。
  历史样例：Apple「字义即动效」/ NVIDIA「拟人化 agent 流动」/ Amazon「真实商品照=排版
  元素」/ AWS「粉彩→深色→粉彩三明治 + 参数累加不清屏」/ Google「logo 变形 + 歌词即
  文案」/ Visa「词→按钮形变 + 三次点按母题 + 祈使清单累加」。把它写成 prompt 开头的
  一句"signature mechanic"声明，并在时间轴里逐拍落实。
- **幕结构 + 绝对时间码**：直接来自逐秒镜头表。复原 prompt 的时间轴必须锚绝对时间码。
- **色彩系统 + 色调切换节奏**：带上具体 hex（报告里通常有）。
- **节奏**：镜头/秒、哪里快切、哪里长保持（长保持要在 prompt 里明写，别被默认快切覆盖）。
- **屏幕文字逐字保留**：slogan、规格参数、UI 文案，必须**一字不差**照抄进 prompt
  （尤其规格片，架构师要逐条读）。
- **音乐/音效**：能不能复用有版权？（如 Google 用 Jay-Z——提示需授权）。
- **人物/场景多样性**：文生视频路线里要写进 prompt。

---

## 第三步：按路线生成 prompt

根据第一步的路线，读对应的参考文件，套用其模板与规则生成**一条完整 prompt**：

- **codegen 路线** → 读 `references/codegen-prompt.md`
- **文生视频路线** → 读 `references/text-to-video-prompt.md`
- **混合** → 以 codegen 模板为主，实拍/硬件镜头按 `[IMG]` 规则内联（见 codegen 参考的
  "ASSET SOURCING"），个别需实拍的段落再附一小段文生视频 prompt。

两条参考文件里都含：可填空的模板、硬规则、"技术→效果"对照、一个精简实例、交付前
checklist。生成时忠于拉片报告的实际内容，不臆造画面。

---

## 输出约定

- **框架说明用中文，prompt 正文用英文**（生成工具对英文 prompt 表现最好；用户是中文语境）。
- 先用一两句说清**你选了哪条路线、为什么**，以及**这支片 codegen 的适配度**（可用
  ⭐ 粗标：纯排版/图解=高，UI demo=中，实拍大片=不适合）。
- 主体是**一整块可复制的 prompt**（放进代码块），不要拆成零碎片段——用户明确偏好"一个
  完整 prompt"。
- prompt 之后补一个简短的**使用提醒表**：竖/横屏、纯代码 vs 素材槽、节奏陷阱、招牌机制
  别偷懒等该片特有的坑。
- 结尾可提示：这套「拉片→prompt」与 `video-lapian`「视频→拉片」串联使用。
