---
name: ref-film-to-storyboard-prompt
description: >-
  Turn "客户指着一支对标视频说要这个" into two deliverables — (1) a production-ready
  storyboard (逐镜表 + 参考截图 + 动效描述 + 每镜标 diffusion / code-gen / AE 一次性 / 素材
  + 复现稳定性 + 可直接用的 diffusion 提示词) and (2) one complete, copy-as-a-whole
  hybrid video-generation prompt (TapVid 类混合模型：程序化图形 + 扩散实拍质感) with
  rendering-rule routing and hard constraints. The method: 拉片对标视频提机制（不是抄镜头）
  → 抓官网/brief 提炼品牌内容槽并逐条事实核对 → 定性 + 受众核对 → 坑位/填法 merge →
  复现优先的"图形骨架 × 卖点插槽"设计 → 故事板 → 最终 prompt。Use this WHENEVER the user
  gives a reference/对标/benchmark video (URL 或文件) plus a brand, website, or brief and
  wants a 宣传片 / 品牌片 / 曝光素材 / 参考样片 / storyboard / 故事板 / 分镜 / video prompt
  out of it — including "帮我拉片然后写 prompt", "做一个像 X 那样的片子", "给动效师出故事板",
  "哪些用 diffusion 哪些用 codegen", "批量出素材测卖点" — even if they only ask for one
  of the two deliverables or don't say "拉片". Do not use for pure teardown with no
  production intent (that is video-lapian) or for article→explainer prompts with no
  reference film (that is explainer-video-prompt).
---

# Ref Film → Storyboard + Prompt

把"对标视频 + 品牌内容"变成两样能直接投入生产的东西：**故事板**（给动效师/生产者）和
**一整段可直接使用的混合模型 prompt**（给 TapVid 类引擎）。中间那一步——怎么把对标片
和品牌 merge、每个镜头该走 diffusion 还是 code-gen——是这个 skill 真正的价值。

## 先想清楚这三件事（做之前）

1. **客户要的是"那支片的感觉"，不是那支片。** 拉片的目的是提炼 3–6 个可迁移的**机制**
   （签名视角、节奏结构、慢镜头留给差异点、色卡节拍器…），不是复刻镜头表。曾经的教训：
   24 镜 1s/拍完全照 Board 的结构做，用户直接说"我的目标不是 1:1 拉片"。
2. **复现性是设计约束，不是后期检查项。** 真人蒙太奇每一拍都要单独抽卡，24 镜 = 24 个
   失败点。能稳定复产的片子是"图形骨架 + 少量可换插片"，先按这个设计，再往里加对标片的
   感觉。详见 `references/merge-method.md` §4。
3. **基础信息只能来自来源。** 品牌文案、参数、游戏名、网址、数字——全部从官网/brief 原话
   来；凡是自己"补"的（一个计数器数字、一个域名、一根线缆的有无）都要么删掉要么标
   `[TBC]`。用户会逐条问"基础信息属实吗"。

## 工作流

### Step 0 · 收集输入
- 对标视频：URL 或本地文件（可能不止一支：首屏品牌片 + 产品短片 + 游戏 trailer…）
- 品牌来源：官网 / brief / 设计系统。官网若是 SPA，文案在 JS bundle 里——用
  `scripts/scrape_site.py <url>` 抽文案、色板、素材 URL、序列帧
- 生产上下文：交付给谁（TapVid 直出？AE 手搓？）、目标（一支样片？批量测卖点？）、
  是否强制 TTS、时长与比例

### Step 1 · 拉片对标视频 → 机制表
用 `video-lapian` skill 的脚本下载 + 抽帧（`extract_frames.py --step 1.0`，Read 每张
montage），但产出物不是十节报告，而是一张**分幕机制表**：幕 / 时长 / 在干什么 / 机制。
再收敛成 **3–6 个可迁移机制** + **1–2 条不能直接搬的原因**（通常是：它 70% 靠真人正脸
实拍，而我们没有真机/实拍）。格式见 `references/merge-method.md` §1。

多支视频时区分角色：品牌主片学结构与情绪，产品短片学微距/屏幕切法，trailer 学游戏画面。

### Step 2 · 品牌内容槽 + 事实核对
从来源提炼内容槽：定位句 / 产品构成 / 技术卖点 / 内容阵容 / 反馈机制 / 受众信号 /
CTA / 视觉系统（色值、字体、场景陈设、人物）。每条附来源原话。
**受众核对**：不要接受用户或自己的第一直觉，用来源里的证据判断（FAQ 对谁说话、
身体焦虑词、hero 图里谁在用产品、有没有年龄标注）。受众决定卖点库和真人镜头选谁。

### Step 3 · 定性 + Merge
- 写**一句话定性**（这是一支什么片 + 不是什么）和一条**验收标准**（如"关掉字幕和 VO
  还能看懂什么"）。
- 做 **坑位 → 填法** 映射表：对标片的每个不变量坑位，对应品牌的填法。只保留 Step 1 收敛
  的那几个机制，其余用品牌自己的图形语言。
- 三个**全片不变量**（同一场景 / 同一产品描述 / 品牌色只在图形层），每镜都守。

### Step 4 · 复现优先的骨架设计
默认产出"**母版 × 插槽**"结构（8–10 镜，15–30s）：
- 固定位：舞台镜头（把对标片的签名视角图形化）、内容/游戏镜头、收尾卡
- 插槽：hook 句 / 卖点展示 / 证据卡（随卖点整套换）+ 真人插片 ×2（可换可删）
- 卖点库：每个卖点 = hook + 图形展示 + 证据卡 + 适合的插片；文案来自来源原话
若用户明确要"完整一支片"而非批量素材，仍按此骨架，只是插槽固定为一个卖点。
只有在用户明确要"Board 式真人蒙太奇上限版"时才做多镜真人版，并标注其复现性低。

### Step 5 · 逐镜路由（diffusion / code-gen / AE 一次性 / 素材）
按 `references/routing-rules.md` 给每镜标生产方式 + 稳定性（稳/中/险）+ 一句理由。
真人镜头只用生成模型稳的景别（顶视、背影、侧面、脚部/微距、环境定场），
不给正脸、不多人同框清晰、单镜 ≤2–4s、每镜 2–3 备选。

### Step 6 · 产出 ① 故事板
用 `scripts/build_storyboard.py <spec.json> <out.html>` 生成自包含 HTML（参考截图内嵌
base64）。列：镜/时间段/槽位 · 参考截图 · VO · 画面描述（DIFF 镜内含完整英文提示词）·
动效描述 · 生产方式+稳定性。页首放定性/不变量/图例，页尾放插片池提示词、AE 交付物、
待要素材。spec 格式见 `references/storyboard-spec.md`；有多个卖点变体时每个变体一张表 +
一张变体总表。CODE 镜头没有现成参考图时用脚本自带的线框 mock（板/卡片/网格）。

### Step 7 · 产出 ② 可直接使用的 prompt
按 `references/prompt-template.md` 写一整段英文 prompt（可整段复制）：Brief → Narrative
Design → Rendering Rules（Layer A 实拍质感 / Layer B 精确图形 / Layer C 产品英雄 / 内容
画面）→ 逐镜 shot list（每镜带 `[LIVE]` `[GRAPHIC]` `[GRAPHIC over LIVE]` `[PRODUCT
RENDER]` 标签）→ Hard Constraints。**不点名任何模型/引擎**，路由靠渲染规则的质感描述
逼出（"photorealistic camera footage… NOT illustration/vector/cartoon/3D-render/motion-
graphic"）。若引擎强制 TTS，给 5–7 句极简 VO，逐字等于屏幕字，情绪高潮段明确写"无 VO"。
交付前跑事实核对：屏幕文字白名单逐条对来源；删掉编造的数字/URL/物理细节。

### Step 8 · 交付与提醒
在聊天里给：三桶占比（DIFF/CODE/AE 各多少镜、多少秒）、真正的卡点（几乎总是客户素材：
产品渲染图、游戏录屏、logo/字体、URL、是否露价）、以及"这版离对标片的感觉差在哪、
代价是什么"——让用户在复现性和相似度之间自己拍板。

## 铁律
- 机制迁移，不复刻镜头；被指出"太像原片"时先升抽象高度（留机制去形式）再改。
- 复现性先于好看：镜头数少、单镜长、图形承担结构、真人只做佐料。
- 屏幕文字与数字逐字来自来源；编造的一律删或 `[TBC]`。
- 真人镜头避正脸、避多人同框、避手指精细交互；产品外形精确的镜头不交给生成模型。
- 交付时说清代价与卡点，不替用户决定"要不要更像 Board"。

## 参考文件
- `references/merge-method.md` — 拉片机制表格式、内容槽、坑位/填法、复现优先骨架、卖点库
- `references/routing-rules.md` — 什么时候 code-gen / diffusion / AE / 素材，稳定性评级
- `references/storyboard-spec.md` — spec.json 结构 + build_storyboard.py 用法
- `references/prompt-template.md` — 最终 prompt 骨架、渲染规则措辞、VO 规则、事实核对清单
- `scripts/scrape_site.py` — SPA 官网抽文案/色板/素材
- `scripts/build_storyboard.py` — spec.json → 自包含 HTML 故事板
- 拉片下载/抽帧复用 `~/.claude/skills/video-lapian/scripts/`
