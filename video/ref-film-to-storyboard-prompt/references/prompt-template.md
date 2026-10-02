# 最终 prompt 模板（可整段复制的混合模型 prompt）

一份文档、英文、整段复制即可用。不点名任何模型/引擎/技术栈；路由靠渲染规则的措辞。
下面每一段都要有，顺序固定。

```
# Complete Video Generation Prompt (copy as a whole)

**Brief:** {时长}-second {类型}, {比例}, {分辨率}, 24 fps. Title: "{品牌} — {定位句}".
{音乐驱动 / 极简 VO 说明}. Tone: {3–5 个形容词} — {是什么场景，不是什么}.

## Narrative Design
{一段：借了对标片的哪几个机制（用机制名，不提对标片名也行）；镜头节奏；唯一慢下来的
地方给什么；收尾形式。}
Beats ({时长}):
1. {幕名} ({起–止}s)
2. …

## Rendering Rules
**Constant product description (repeat in every shot that shows the product):** {尺寸、
材质、颜色、无按钮/无屏、线缆处理、"never changes shape, colour, proportion or brand
mark between shots"}.

**Layer A — Live-action footage ({≈N of T} s).** Photorealistic, cinematic live-action
look: real skin, real fabric, real wood grain, natural {光线}, shallow depth of field,
gentle handheld or locked-off camera, film-like colour, mild grain. These shots must NOT
be rendered as illustration, flat vector, cel-shaded, 3D-cartoon or motion-graphic style
— they must read as footage shot with a camera in a real {场景}. Cast: {人物 + 衣着发型}.
Frame them from behind, from above, from the side, or at feet/mid-body — never a frontal
close-up on a face, never both faces sharp in the same frame. No shot on this layer longer
than {2–4} s. Set: {陈设逐项}. Same set in every live shot.

**Layer B — Precision graphics ({≈N of T} s).** Vector-sharp, digit-accurate typography
and UI; brand palette: {色值 + 角色}. Typeface: {描述}. Text is identical to this prompt,
letter for letter. Charts/counters/heat-maps/cards/title cards live here. When a graphic
is placed over live footage it is pinned to {表面} with correct perspective.

**Layer C — Product hero render ({≈N} s).** One physically-based hero shot on {背景},
studio softbox reflections, real material response; used only in Beat {k}.

**{内容画面} (game/app screens).** {风格描述}; clearly a screen, not the real world.

**Transitions:** hard cuts only. **Music:** {风格 + 脉冲 + 哪一幕抽掉}. **Text animation:**
snap in on the beat, no bounce, no glow.
**Voiceover:** {none / one voice, warm, unhurried; lines land at the timecodes below and
match the on-screen text word for word; silence is allowed}.

---
## {幕名} | m:ss–m:ss
**VO (m:ss–m:ss):** "{句子}"        ← 强制 TTS 时才有
1. **[LIVE · {景别}]** m:ss–m:ss — {画面}. {机位/运动}. Duration {n} s.
2. **[GRAPHIC]** … 
3. **[GRAPHIC over LIVE]** …
4. **[PRODUCT RENDER]** …
5. **[GAME · full-frame]** …
（每镜一行，整秒边界，写清屏幕文字原文）

## Hard Constraints
1. Total {T} s exactly; {N} numbered shots on whole-second boundaries.
2. Live-action shots ({镜号列表}) must read as photorealistic camera footage — no
   illustration/vector/cartoon look. No live shot longer than {n} s.
3. Faces: no frontal close-up; people appear from behind/above/side/feet only.
4. Product appearance identical in every shot per the constant description.
5. Same set in every live shot.
6. All on-screen text letter-for-letter: "{白名单逐条}".
7. Palette on graphic layer only {色值}; live layer keeps natural colour.
8. Transitions: hard cuts only. Music drops out during shots {a–b}.
9. Countable check: shot {x} shows exactly {N} {物件}; shot {y} exactly {M} rows.
10. VO is exactly these {k} lines, in order, at the listed timecodes: … — nothing else
    is spoken; no VO during shots {情绪高潮段}.   （或：No voiceover anywhere.）
```

## VO 规则（引擎强制 TTS 时）
- 30s ≤ 75 词上限，实际写 50–60 词留气口；5–7 句；一位声音、慢、无推销腔。
- 每句逐字等于同时出现的屏幕字（引擎常按 VO 拆镜，字幕不对齐会露怯）。
- 唯一慢镜头段：音乐抽掉、只留那一句 VO；情绪高潮段明确写"无 VO"，防 TTS 填满。
- Hard Constraints 里把 VO 写成白名单，防模型自己加词。

## 交付前事实核对清单
- [ ] 屏幕文字白名单逐条对来源原话（定位句、参数、名称、训练点、CTA）
- [ ] 数字：来源没给具体值的（"under a second"）不要自己填计数器数字
- [ ] URL / 价格 / 日期：来源没有或可能过期的 → `[TBC]` 并注明"generate 前替换，勿编造"
- [ ] 物理细节：线缆、接缝、按钮、logo 位置——来源没有就别加；插电产品别写"无线缆"
- [ ] 人物、陈设、颜色：来自 hero 图/官网视觉，注明若客户换 art direction 需同步改
- [ ] 来源标 "preliminary" 的一律加"以客户渲染图为准"

## 交付时在聊天里说明
- 路由是怎么"逼"的（哪几镜标 LIVE、质感词、排除词）；引擎若有确定生效的渲染标签让用户自加
- 为稳而做的取舍（避正脸、单镜短、无 VO 或极简 VO）
- 实测要看的 3–4 个信号：LIVE 镜是否被降级成图形、产品是否漂、叠加透视是否对、节奏是否被 TTS 拉平
- 备用路径：这份 prompt 的镜头表本身就是动效师的分镜大纲
