# 取证手册

怎么把"他们说的"变成"我看到的"。按证据层组织。

---

## L1 公开面：抓什么、怎么读

### 定价页——逐字读脚注

定价页的机关几乎全在小字里。要做的事：

1. **抄下计价规则原文**，包括所有换算公式
2. **自己把每档的实际可得量算出来**，和卡片上的营销标注对比
3. 差距本身是发现：官网标"20 分钟"、按主流程口径实际 6.7 分钟，这是一个**付费后落差结构**
4. 算**单位价格**（每 credit / 每分钟 / 每席位）。中间档比高档贵 3 倍是典型的诱饵档设计
5. 找**自动续购**条款——把额度耗尽从流失点变成收入点，很多产品只在应用内写

**注意**：定价页常常是手写的营销页面，和产品实际口径不一致。L3 阶段必须用真实交易验证。

### 企业页——措辞是证据

安全合规的措辞差异极大：

| 写法 | 实际含义 |
|---|---|
| "SOC 2–aligned infrastructure" | 对齐，**未必通过审计** |
| "SOC 2 Type II certified" | 已认证 |
| "encryption in transit & at rest" | 标配，无信息量 |
| "we never train on your content" | 有实质承诺 |

同一站点内不同页面对同一项的写法不一致（一处写 "aligned"、一处直接写 "SOC 2"），
**要单独拎出来标注**。

企业页还常出现"拆件报价"：把 N 项能力逐条标"在别处要花多少钱"，合计一个大数。
这不是给终端用户看的，是**给客户内部要申请预算的人填 business case 用的**。

### 落地页矩阵——最诚实的客户画像

数三个维度各有几页、分别是什么：
- **用例页**：占比最高的那类场景就是它真正的主战场
- **行业页**：全是强合规行业 = 它在打培训/合规预算，不是营销预算
- **工具词页**：如果下沉到具体法规名（HIPAA/OSHA/GDPR），意图纯度接近 100%

**行业页 + 用例页的交集，比任何"关于我们"都准确地定义了它的 ICP。**

### 内容矩阵——看词的层级

不要只数文章篇数，要看它打什么层级的词：

- **同级词**（"AI 视频生成器"）：红海，用户已经知道自己要什么，你要在比价里赢
- **上游品类词**（"best LMS platforms"）：用户还没想到需要你，**在需求形成之前截住他**
- **法规/场景长尾**：词量小但意图纯

打上游品类词是高价值发现，值得单独成段。

### 第三方源——找和官网不一致的地方

- **Product Hunt**：创始人自述往往比官网直白，会明说"我们要反的是什么"
- **YC/Crunchbase**：团队规模是关键。6 个人同时跑两种毛利结构是重大组织风险
- **G2/Capterra**：找具体吐槽（"元素重叠"这类），比评分有用
- **⚠️ 检查有没有评价激励**：如果产品内有"写评价换额度"的入口，它的公开评分必须打折

### 产出物取样——直接看质量水位

内容生成类产品，从它 CDN 抓样片封面帧/成片：

```bash
curl -sL -o sample.mp4 "<cdn-url>"
qlmanage -t -s 1280 -o . sample.mp4   # macOS 无 ffmpeg 时抽首帧
```

看的时候注意：
- **展示片 ≠ 自助档平均产出**。看它把哪些归到"人工服务"、哪些标"用平台做的"
- **样片有没有借用第三方品牌资产**（用真实大品牌名做的 demo 但没有案例页佐证）——说服力强，法务敞口也真
- logo 墙的措辞："Trusted by teams at X" 通常只是"有 X 的员工注册过"

---

## L2 登录态：遍历手法

### 开场

```
mcp__Claude_Browser__preview_start  {url: "<app-login-url>"}
mcp__Claude_Browser__resize_window  {width: 1440, height: 900}
```

然后**请用户自己登录**。等他确认。面板重开会丢 session，重开后要重新确认登录态。

### 抓结构优先于截图

`read_page {filter:"interactive"}` 拿 refs 和路由，比截图省 token 且更准。
弹层内容用 `javascript_tool` 抓 `innerText`：

```js
[...document.querySelectorAll('[role=dialog],[role=menu],[data-radix-popper-content-wrapper]')]
  .map(n => n.innerText.trim()).filter(Boolean).sort((a,b)=>b.length-a.length)[0]
```

### 常见障碍与对策

| 症状 | 原因 | 对策 |
|---|---|---|
| 弹层一闪即关 | 首屏 demo 动画在重渲染 | 清掉所有定时器：`const hi=setInterval(()=>{},9999); for(let i=1;i<=hi;i++)clearInterval(i)` |
| `.click()` 无反应 | Radix 等组件需要完整指针事件 | 派发 `['pointerdown','mousedown','pointerup','mouseup','click']` |
| tab 切换不生效 | 同上 | 同上，并对 `button[role=tab]` 操作 |
| `javascript_tool` 30 秒超时 | 长任务（如渲染截图） | fire-and-forget，之后轮询结果变量 |
| 视口被重置成小尺寸 | 导航/重开面板 | 每次导航后重新 `resize_window` |

### 要重点看的东西

1. **产品内的 `<title>` 和自我描述** —— 常比官网更硬地暴露真实定位
2. **每个下拉的完整选项清单** —— 选项数量和命名方式信息量极大
3. **参数/预置面板** —— 领域知识产品化的地方。如果有按行业预置的规范（"每镜一个动作，带准备/安全/验证提示"），这是它最难被复制的资产
4. **付费墙的位置** —— 切"能不能用"和切"能不能改"是完全不同的商业设计
5. **应用内定价页** —— 和官网对比，不一致就是发现
6. **激励入口** —— 评价换额度、分享换额度、onboarding 任务奖励，构成它的激励矩阵

---

## L3 行为实测：设计能证伪的实验

**每次实测都要先问用户授权**，说清成本和验证目标。

### 高价值实测清单

| 实测 | 怎么做 | 能证伪什么 |
|---|---|---|
| 计价口径 | 用最小单位跑一次，记录余额变化 | 定价页的计价规则是否属实 |
| 扣费时机 | 观察提交时 vs 完成时余额 | 失败是否计费、他们怎么处理风险 |
| 管线架构 | 全程记录状态文案序列 | 是端到端还是多段外采 |
| 耗时 | 掐表 | "in minutes" 这类宣称 |
| 输入差异定价 | 换不同输入类型各跑一次 | 是否存在宣称的倍率 |
| 产出质量 | 下载成品抽帧 | 展示片和实际产出的差距 |

### 供应链指纹

实测时留意这些，它们比任何架构猜测都硬：

- **资源 host**：`v3b.fal.media` → fal.ai；`*.cloudfront.net` → 自建 CDN
- **命名习惯**：音色叫 Aoede/Callirrhoe/Gacrux → Google Gemini TTS 预置名；叫 Adam/James/Jessica → ElevenLabs
- **产物路径**：`agent-create/.../scene1.mp4` → `agent-mux/assemble/*.mp4` 说明是逐镜渲染后合成
- **鉴权强度**：母版能不能无 cookie 直接 curl 到？水印是烧进去的还是播放器叠层？

最后一条常有惊喜：**水印如果是 UI 叠层、母版在 CDN 上公开可取，那免费档的水印约束形同虚设**——这是真实的业务逻辑漏洞。

### 用 JS 注入文件测试输入路径

不用真的手动上传，可以构造 File 对象注入：

```js
const inp = [...document.querySelectorAll('input[type=file]')][0];
const f = new File([content], 'test.txt', {type:'text/plain'});
const dt = new DataTransfer(); dt.items.add(f);
inp.files = dt.files;
inp.dispatchEvent(new Event('change', {bubbles:true}));
```

先看 `inp.accept` 能知道它真实接受哪些格式——常和官网宣称不一致。
