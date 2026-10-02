# 故事板规格 + build_storyboard.py 用法

## 故事板长什么样（给动效师/生产者的那份）
- 页首：标题（项目 · 版本 · 镜数/时长 · 给谁）、一句话定性、meta（比例/帧率/硬切/音乐/VO/色板/裁切规则）、
  生产方式图例、全片不变量、（多变体时）变体总表
- 主体：每支/每变体一张表，6 列固定 —
  **镜/时间段/槽位 · 参考截图 · VO · 画面描述（DIFF 镜内含完整英文提示词，折叠）· 动效描述 · 生产方式+稳定性+一句理由**
- 页尾：真人插片池（5 类 DIFF 提示词 + 抽卡规则）、AE 制作顺序、交付物、向客户要的素材

变体行浅色底、母版行白底，让"每支只换哪几行"一眼可见。

## 参考截图取法
- 有官网 hero 帧/产品图/内容画面就用它（最贴）
- 对标片的帧只做"景别/节奏参考"，图注写明"→ 换成 X"，防动效师照抄
- CODE 镜头没有现成参考 → 用脚本自带线框 mock（hook / card / end / stage / grid / phone），图注写"布局示意（AE 按品牌字体重排）"

## spec.json 结构

```json
{
  "title": "Example Product · 故事板 v1",
  "subtitle": "首轮 5 支变体 S1–S5 · 母版 8 镜 / 20s · 给 AE 批量制作",
  "thesis": "受众：… 片子是 … <b>每支只讲一个卖点</b> …",
  "meta": ["16:9 · 1920×1080 · 24fps", "硬切 only", "音乐 …", "VO …", "色板 …", "裁切：15s 去 #4 #7；6s = #1+#3+#8"],
  "palette": {"bg": "#101612", "accent": "#B9EC43", "ink": "#F5F6EF", "grey": "#AEB5AD", "panel": "#1E2820"},
  "invariants": ["同一间客厅：…", "同一块板：…", "品牌色只在图形层", "人物只给背影/顶视/侧面/脚部"],
  "summary": {"heading": "变体总表", "columns": ["变体","#1 Hook","#3 VO","#6 证据卡","#4 → #7 插片","#3 生产"], "rows": [["S1 身体即手柄","Your body is the controller.","…","…","P1 → P4","CODE"]]},
  "tables": [
    {"heading": "S1 · 身体即手柄", "sub": "#4 推荐 P1 · #7 推荐 P4",
     "shots": [
       {"no": "01", "tc": "0:00–0:02", "slot": "插槽 A · Hook【S1】", "variant": true,
        "refs": [{"mock": "hook", "args": {"l1": "Your body is", "l2": "the controller."}, "cap": "布局示意"}],
        "vo": "\"Your body is the controller.\"",
        "visual": "深绿 #101612 满屏。米白大字两行 …", "motion": "文字踩拍瞬入；0.5s 后下划线从左画出 …",
        "route": "CODE", "stab": "稳", "note": "换变体只改文本。"},
       {"no": "04", "tc": "0:09–0:11", "slot": "插槽 C · 真人插片 ①",
        "refs": [{"path": "ref_frames/f0001.webp", "cap": "DIFF 参考：官网 hero 顶视踏板"}],
        "vo": "（无 VO）", "visual": "真人：顶视客厅，赤脚踏上白板 …", "motion": "固定顶视，极慢推 3%。",
        "prompt": "Shot: locked-off bird's-eye view … \n\nSetting (identical …) …\n\nProduct (identical …) …\n\nLook: photorealistic … NOT illustration …\n\nAvoid: frontal faces, …",
        "route": "DIFF", "stab": "中", "note": "可换可删；抽 3–5 条备选。"}
     ]}
  ],
  "pool": [{"name": "P1 顶视脚踏板", "prompt": "…", "note": "变体：踏上 / 重心右压 / 跳下"}],
  "pool_rule": "每条 2s；同批固定 seed 系列；只看板形/正脸/脚形三项，不合格直接丢不修。",
  "footer": {"AE 制作顺序": ["母版 …", "S1 全片 → 给客户当样片", "…"], "交付物": ["20s + 15s + 6s；16:9 + 9:16"], "向客户要": ["产品渲染图", "游戏录屏 ≥3 款", "logo/字体/URL/是否露价"]}
}
```

mock 可用类型与参数：`hook{l1,l2}` `card{lines[]}` `end{brand,tagline,cta}` `stage{caption}`（顶视板+脚剪影+热力图）`grid{names[],cols,caption}` `phone{rows[[k,v]]}`。
需要别的线框就临时用 cv2 画，别为了一张图去装新依赖。

## 用法
```bash
python3 scripts/build_storyboard.py spec.json storyboard.html
```
产出自包含 HTML（图片 base64 内嵌），可直接发给动效师或发布为 artifact。发布前用本地
`python3 -m http.server` 打开看一眼编码和布局（脚本已写 `<meta charset="utf-8">`）。

## 时长/镜数经验
- 复现优先骨架：8–10 镜、20s 主版；单镜 2–4s；真人插片 ≤2 处
- 对标片"上限版"（真人蒙太奇）：24 镜/30s 只在用户明确要时做，并标注复现性低
