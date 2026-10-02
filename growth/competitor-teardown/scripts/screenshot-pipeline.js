// 界面截图落盘管道 —— 已验证可用（2026-08）
//
// 背景：浏览器面板的 computer{action:"screenshot"} 只把图回传给模型，拿不到文件字节，
// 因此没法嵌进 artifact。这个管道让页面自己把 DOM 渲染成位图，经剪贴板落盘。
//
// 用法：把下面各步分别丢进 mcp__Claude_Browser__javascript_tool 执行。

// ─────────────────────────────────────────────────────────────
// STEP 1：注入 html2canvas-pro
// 必须用 -pro 版本。普通 html2canvas 1.4.1 会抛
// "Attempting to parse an unsupported color function oklab"（Tailwind v4 站点）
// ─────────────────────────────────────────────────────────────
(async () => {
  if (window.html2canvas) return 'already loaded';
  const r = await new Promise(res => {
    const s = document.createElement('script');
    s.src = 'https://cdn.jsdelivr.net/npm/html2canvas-pro@1.5.8/dist/html2canvas-pro.min.js';
    s.onload = () => res('loaded');
    s.onerror = () => res('blocked');
    document.head.appendChild(s);
    setTimeout(() => res('timeout'), 10000);
  });
  return r + ' typeof=' + (typeof window.html2canvas);
})();


// ─────────────────────────────────────────────────────────────
// STEP 2：定义捕获函数 + 攒图数组
// ─────────────────────────────────────────────────────────────
(() => {
  window.__pile = window.__pile || [];

  // 清掉所有定时器。SPA 首屏的 demo 动画会不停重渲染把弹层顶掉，
  // 不清的话截到的常是过渡态或空壳。
  window.__kill = () => {
    const hi = setInterval(() => {}, 9999);
    for (let i = 1; i <= hi; i++) clearInterval(i);
    clearInterval(hi);
  };

  window.__snap = async () => {
    const c = await html2canvas(document.body, {
      useCORS: true,
      backgroundColor: '#0b0b0d',   // 换成目标站的底色
      scale: 1,
      logging: false,
      imageTimeout: 20000           // 缩略图多的面板要给足时间
    });
    window.__png = c.toDataURL('image/jpeg', 0.78).split(',')[1];
    return 'OK ' + window.__png.length;
  };

  window.__take = async (name) => {
    const r = await window.__snap();
    if (String(r).startsWith('OK')) {
      window.__pile.push({ n: name, d: window.__png });
      return name + ' ' + r + ' pile=' + window.__pile.length;
    }
    return name + ' FAIL ' + r;
  };

  return 'ready';
})();


// ─────────────────────────────────────────────────────────────
// STEP 3：拍一张（每个场景重复）
// html2canvas 单次要 5–20 秒，javascript_tool 30 秒会超时。
// 超时不代表失败——之后轮询 window.__pile 即可。
// ─────────────────────────────────────────────────────────────
(async () => {
  window.__kill();
  // …在这里把界面切到目标状态（打开弹层、切 tab、滚动到位）…
  await new Promise(r => setTimeout(r, 2000));   // 等图片/动画稳定
  window.__kill();
  return await window.__take('01-home');
})();


// ─────────────────────────────────────────────────────────────
// STEP 3.5：质量自检（可选但强烈建议）
// 把捕获结果铺成全屏 overlay，然后用 computer{action:"screenshot"} 肉眼看。
// 比事后发现整批是黑图强得多。
// ─────────────────────────────────────────────────────────────
(() => {
  document.getElementById('__preview')?.remove();
  const o = document.createElement('img');
  o.id = '__preview';
  o.src = 'data:image/jpeg;base64,' + window.__png;
  o.style.cssText = 'position:fixed;inset:0;width:100vw;height:100vh;' +
                    'z-index:2147483647;background:#f0f;object-fit:contain';
  document.body.appendChild(o);
  return 'overlaid — 现在用 computer screenshot 看一眼，看完记得 remove';
})();


// ─────────────────────────────────────────────────────────────
// STEP 4：出仓 —— 挂手势监听
// 异步 clipboard API 会被面板拒（NotAllowedError）；
// execCommand('copy') 需要真实用户手势，所以挂在 click 捕获阶段，
// 再用 computer{action:"left_click"} 触发。
// ─────────────────────────────────────────────────────────────
(() => {
  window.__cr = 'pending';
  const h = () => {
    const ta = document.createElement('textarea');
    ta.value = JSON.stringify(window.__pile);
    document.body.appendChild(ta);
    ta.select();
    window.__cr = 'exec=' + document.execCommand('copy');
    ta.remove();
    document.removeEventListener('click', h, true);
  };
  document.addEventListener('click', h, true);
  return 'armed, pile=' + window.__pile.length;
})();

// 然后：mcp__Claude_Browser__computer {action:"left_click", coordinate:[x,y]}
//       （点空白处即可；点之前需要先有一次 screenshot 以缓存坐标系）


// ─────────────────────────────────────────────────────────────
// STEP 5：落盘（Bash）
// ─────────────────────────────────────────────────────────────
/*
cd <workdir> && pbpaste > pile.json && /usr/bin/python3 -c "
import json, base64
d = {}
for it in json.load(open('pile.json')): d[it['n']] = it['d']   # 同名保留最后一次
for n, v in sorted(d.items()):
    open(n + '.jpg', 'wb').write(base64.b64decode(v))
    print(n, len(v)//1024, 'KB')
" && printf '' | pbcopy && echo '== clipboard cleared =='
*/


// ═════════════════════════════════════════════════════════════
// 注意事项
// ═════════════════════════════════════════════════════════════
//
// 剪贴板竞争：用户日常复制会覆盖掉。所以要「多张攒够再一次出仓」，
//   并在动手前提醒用户暂时别用复制，完事后 pbcopy 清空。
//
// 跨域图片：没有 CORS 头的资源（如 fal.media）会渲染成空框。
//   这类图直接用 curl 从 CDN 取原图，另行嵌入。
//
// 时序错位：切完界面状态要等够再拍，否则会拍到上一个状态。
//   拍完务必抽查，废片直接丢弃重拍。
//
// ── 已验证的死路，别浪费时间 ──
// ✗ 页面 fetch POST 到 localhost —— 被面板网络层拦死，
//   即使服务端补了 Access-Control-Allow-Private-Network 也一样
// ✗ screencapture —— 权限可能是通的，但 Claude 窗口常在独立全屏 Space，
//   物理屏上抓不到面板
// ✗ 手搓 SVG foreignObject 克隆 DOM —— Tailwind v4 的 @property 和入场动画
//   会让结果变成黑屏（简单页面如登录页反而可行）
// ✗ navigator.clipboard.writeText —— 面板权限拒绝
