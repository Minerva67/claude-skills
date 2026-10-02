#!/usr/bin/env python3
"""
spec.json -> self-contained HTML storyboard (reference stills embedded as base64).

Why: the storyboard is handed to a motion designer / producer who needs, per shot,
the timecode, a reference still, VO, what's on screen, how it moves, and how it will
be produced (diffusion / code-gen / AE one-off / client asset) with a reproducibility
rating. One file, no external assets, renders in light and dark.

Usage:
    python3 build_storyboard.py spec.json out.html

spec.json (see references/storyboard-spec.md):
{
  "title": "...", "subtitle": "...", "thesis": "...", "meta": ["16:9 · 1080p · 24fps", ...],
  "invariants": ["同一间客厅…", ...],
  "footer": {"AE 制作顺序": ["..."], "交付物": ["..."], "向客户要": ["..."]},
  "pool": [{"name": "P1 顶视脚踏板", "prompt": "...", "note": "..."}],
  "tables": [ {"heading": "S1 · 身体即手柄", "sub": "...", "shots": [SHOT, ...]} ]
}
SHOT = {"no": "01", "tc": "0:00–0:02", "slot": "插槽 A · Hook", "variant": true|false,
        "refs": [{"path": "frame.png", "cap": "..."} | {"mock": "hook", "args": {...}, "cap": "..."}],
        "vo": "...", "visual": "...", "motion": "...", "prompt": "(optional diffusion prompt)",
        "route": "CODE|DIFF|DIFF+CODE|AE 一次性|素材/CODE", "stab": "稳|中|险", "note": "..."}
Mocks available (line-drawn wireframes for CODE shots without a reference):
  hook{l1,l2}  card{lines[]}  end{brand,tagline,cta}  stage{}  grid{names[]}  phone{rows[[k,v],...]}
"""
import sys, json, base64, html
import cv2, numpy as np

W, H = 960, 540
def hexbgr(h): h=h.lstrip('#'); return (int(h[4:6],16), int(h[2:4],16), int(h[0:2],16))
PAL = {}
def canvas(): return np.full((H, W, 3), PAL['bg'], np.uint8)
def txt(im, s, org, scale, color, th=2, font=cv2.FONT_HERSHEY_DUPLEX): cv2.putText(im, s, org, font, scale, color, th, cv2.LINE_AA)

def mock_hook(a):
    im=canvas(); txt(im,a.get('l1',''),(80,225),1.5,PAL['ink'],3); txt(im,a.get('l2',''),(80,300),1.5,PAL['ink'],3)
    cv2.line(im,(80,325),(min(880,80+len(a.get('l2',''))*30),325),PAL['accent'],5); return im
def mock_card(a):
    im=canvas()
    for i,s in enumerate(a.get('lines',[])[:4]):
        y=150+i*95; cv2.rectangle(im,(110,y-42),(850,y+22),PAL['panel'],-1); cv2.circle(im,(140,y-10),9,PAL['accent'],-1); txt(im,s,(170,y),0.8,PAL['ink'],1,cv2.FONT_HERSHEY_SIMPLEX)
    return im
def mock_end(a):
    im=canvas(); txt(im,a.get('brand','BRAND'),(280,220),1.8,PAL['ink'],3); txt(im,a.get('tagline',''),(330,290),1.1,PAL['accent'],2); txt(im,a.get('cta',''),(300,360),0.7,PAL['grey'],1,cv2.FONT_HERSHEY_SIMPLEX); return im
def mock_stage(a):
    im=canvas(); cx,cy=W//2,H//2; x0,y0,x1,y1=cx-280,cy-170,cx+280,cy+170
    cv2.rectangle(im,(x0,y0),(x1,y1),(240,240,236),-1); cv2.rectangle(im,(x0,y0),(x1,y1),(200,200,195),2)
    for (x,y) in [(x0+28,y0+28),(x1-28,y0+28),(x0+28,y1-28),(x1-28,y1-28)]: cv2.circle(im,(x,y),7,PAL['accent'],-1)
    for dx in (-70,70): cv2.ellipse(im,(cx+dx,cy),(28,70),0,0,360,(60,90,40),-1)
    ov=im.copy(); cv2.circle(ov,(cx+40,cy),60,PAL['accent'],-1); cv2.addWeighted(ov,0.35,im,0.65,0,im); cv2.circle(im,(cx+40,cy),20,PAL['accent'],-1)
    if a.get('caption'): txt(im,a['caption'],(60,H-40),0.7,PAL['grey'],1,cv2.FONT_HERSHEY_SIMPLEX)
    return im
def mock_grid(a):
    im=canvas(); names=a.get('names',[]); cols=a.get('cols',6)
    for i,n in enumerate(names):
        c,r=i%cols,i//cols; x=60+c*145; y=120+r*110
        cv2.rectangle(im,(x,y),(x+130,y+80),PAL['panel'],-1); txt(im,str(n)[:12],(x+8,y+45),0.42,PAL['ink'],1,cv2.FONT_HERSHEY_SIMPLEX)
    if a.get('caption'): txt(im,a['caption'],(60,70),0.8,PAL['ink'],1,cv2.FONT_HERSHEY_SIMPLEX)
    return im
def mock_phone(a):
    im=canvas(); cv2.rectangle(im,(330,60),(630,500),PAL['panel'],-1); cv2.rectangle(im,(330,60),(630,500),(80,90,80),2)
    for i,(k,v) in enumerate(a.get('rows',[])[:3]):
        y=140+i*120; txt(im,k,(360,y),0.8,PAL['accent'],1,cv2.FONT_HERSHEY_SIMPLEX); txt(im,v,(360,y+35),0.55,PAL['grey'],1,cv2.FONT_HERSHEY_SIMPLEX)
    return im
MOCKS={'hook':mock_hook,'card':mock_card,'end':mock_end,'stage':mock_stage,'grid':mock_grid,'phone':mock_phone}

def b64(im): ok,buf=cv2.imencode('.jpg',im,[cv2.IMWRITE_JPEG_QUALITY,74]); return base64.b64encode(buf).decode()
def load(p,w=460):
    im=cv2.imread(p)
    if im is None: raise SystemExit(f'cannot read {p}')
    h,ww=im.shape[:2]; return cv2.resize(im,(w,int(w*h/ww)))
def fig(im,cap): return f'<figure><img src="data:image/jpeg;base64,{b64(im)}" alt=""><figcaption>{html.escape(cap)}</figcaption></figure>'
def render_ref(r):
    if 'mock' in r: return fig(MOCKS[r['mock']](r.get('args',{})), r.get('cap','布局示意'))
    return fig(load(r['path']), r.get('cap',''))
ROUTE_CLASS={'CODE':'r-code','DIFF':'r-diff','DIFF+CODE':'r-mix','AE 一次性':'r-ae','素材/CODE':'r-asset','素材':'r-asset'}
def route_class(route):
    for k,v in ROUTE_CLASS.items():
        if route.startswith(k): return v
    return 'r-code'

def shot_row(s):
    prompt = f'<details><summary>Diffusion prompt（英文，直接可用）</summary><pre>{html.escape(s["prompt"])}</pre></details>' if s.get('prompt') else ''
    refs=''.join(render_ref(r) for r in s.get('refs',[]))
    return f'''<tr class="{'var' if s.get('variant') else ''}"><td class="tc"><span class="no">{html.escape(str(s['no']))}</span><span class="time">{html.escape(s['tc'])}</span><span class="slot">{html.escape(s.get('slot',''))}</span></td>
<td class="ref">{refs}</td><td class="vo">{html.escape(s.get('vo','—'))}</td><td class="vis">{html.escape(s.get('visual',''))}{prompt}</td><td class="mot">{html.escape(s.get('motion',''))}</td>
<td class="route"><span class="tag {route_class(s['route'])}">{html.escape(s['route'])}</span> <b class="stab">{html.escape(s.get('stab',''))}</b><p>{html.escape(s.get('note',''))}</p></td></tr>'''

def main():
    spec=json.load(open(sys.argv[1])); out=sys.argv[2]
    pal=spec.get('palette',{}); PAL.update({'bg':hexbgr(pal.get('bg','#101612')),'accent':hexbgr(pal.get('accent','#B9EC43')),'ink':hexbgr(pal.get('ink','#F5F6EF')),'grey':hexbgr(pal.get('grey','#AEB5AD')),'panel':hexbgr(pal.get('panel','#1E2820'))})
    tables=''
    for t in spec.get('tables',[]):
        rows=''.join(shot_row(s) for s in t['shots'])
        tables+=f'''<section><h2>{html.escape(t.get('heading',''))} <small>{html.escape(t.get('sub',''))}</small></h2>
<div class="wrap"><table><thead><tr><th>镜 / 时间段 / 槽位</th><th>参考截图</th><th>VO</th><th>画面描述</th><th>动效描述</th><th>生产 · 复现</th></tr></thead><tbody>{rows}</tbody></table></div></section>'''
    summary=''
    if spec.get('summary'):
        sm=spec['summary']; hdr=''.join(f'<th>{html.escape(h)}</th>' for h in sm['columns']); body=''.join('<tr>'+''.join(f'<td>{html.escape(str(c))}</td>' for c in r)+'</tr>' for r in sm['rows'])
        summary=f'<h2>{html.escape(sm.get("heading","变体总表"))}</h2><div class="wrap"><table class="sum"><thead><tr>{hdr}</tr></thead><tbody>{body}</tbody></table></div>'
    pool=''.join(f'<div class="pool"><h4>{html.escape(p["name"])}</h4><pre>{html.escape(p["prompt"])}</pre>{("<p class=muted>"+html.escape(p["note"])+"</p>") if p.get("note") else ""}</div>' for p in spec.get('pool',[]))
    pool_sec=f'<section><h2>真人插片池（DIFF）</h2>{pool}<p class="muted">{html.escape(spec.get("pool_rule",""))}</p></section>' if pool else ''
    inv=''.join(f'<li>{html.escape(x)}</li>' for x in spec.get('invariants',[]))
    foot=''.join(f'<div><h3>{html.escape(k)}</h3><ul>{"".join(f"<li>{html.escape(x)}</li>" for x in v)}</ul></div>' for k,v in spec.get('footer',{}).items())
    meta=''.join(f'<span>{html.escape(m)}</span>' for m in spec.get('meta',[]))
    page=f'''<meta charset="utf-8">
<title>{html.escape(spec.get('title','Storyboard'))}</title>
<style>
:root{{--bg:#f6f5f0;--panel:#fff;--ink:#1b1f1d;--mute:#5f665f;--line:#dcdcd2;--accent:{pal.get('accent','#b9ec43')};--accent-ink:#3d5a00;--pre:#f0efe8;--var:#fbfaf3;--diff:#c9782a;--code:#2a7f74;--mix:#5b62c9;--ae:#8a4fb3;--asset:#7a7a70;--diff-bg:#fbeee0;--code-bg:#e0f2ef;--mix-bg:#e6e7fa;--ae-bg:#efe3f7;--asset-bg:#ecece6}}
@media (prefers-color-scheme: dark){{:root:not([data-theme="light"]){{--bg:#12161a;--panel:#1a2024;--ink:#eceee8;--mute:#9aa39a;--line:#2c343a;--accent-ink:{pal.get('accent','#b9ec43')};--pre:#111518;--var:#1e2620;--diff-bg:#3a2a18;--code-bg:#15302c;--mix-bg:#23253d;--ae-bg:#2f2039;--asset-bg:#2a2c2a}}}}
:root[data-theme="dark"]{{--bg:#12161a;--panel:#1a2024;--ink:#eceee8;--mute:#9aa39a;--line:#2c343a;--accent-ink:{pal.get('accent','#b9ec43')};--pre:#111518;--var:#1e2620;--diff-bg:#3a2a18;--code-bg:#15302c;--mix-bg:#23253d;--ae-bg:#2f2039;--asset-bg:#2a2c2a}}
body{{background:var(--bg);color:var(--ink);font-family:-apple-system,"PingFang SC","Helvetica Neue",Helvetica,"Noto Sans SC",sans-serif;font-size:13.5px;line-height:1.55;margin:0;padding:32px 28px 64px}}
header,section{{max-width:1440px;margin:0 auto 26px}}
h1{{font-size:26px;margin:0 0 6px}} h1 small,h2 small{{font-size:12.5px;color:var(--mute);font-weight:400;margin-left:10px}}
h2{{font-size:17px;margin:30px 0 10px;padding-left:10px;border-left:4px solid var(--accent)}}
.thesis{{border-left:4px solid var(--accent);padding:8px 14px;margin:14px 0;background:var(--panel);max-width:75ch}}
.meta{{display:flex;flex-wrap:wrap;gap:8px 22px;color:var(--mute);font-size:12.5px}}
.legend{{display:flex;flex-wrap:wrap;gap:10px 16px;margin-top:12px;align-items:center;font-size:12.5px}}
.tag{{display:inline-block;font-family:ui-monospace,Menlo,monospace;font-size:11.5px;font-weight:600;padding:2px 8px;border-radius:4px}}
.r-diff{{background:var(--diff-bg);color:var(--diff)}}.r-code{{background:var(--code-bg);color:var(--code)}}.r-mix{{background:var(--mix-bg);color:var(--mix)}}.r-ae{{background:var(--ae-bg);color:var(--ae)}}.r-asset{{background:var(--asset-bg);color:var(--asset)}}
.wrap{{overflow-x:auto;background:var(--panel);border:1px solid var(--line);border-radius:6px}}
table{{border-collapse:collapse;width:100%;min-width:1240px}}
th{{text-align:left;font-size:11.5px;letter-spacing:.06em;text-transform:uppercase;color:var(--mute);padding:10px 12px;border-bottom:1px solid var(--line);background:var(--panel)}}
td{{vertical-align:top;padding:12px;border-bottom:1px solid var(--line)}} tr.var td{{background:var(--var)}}
.tc{{width:100px}}.no{{display:block;font-family:ui-monospace,Menlo,monospace;font-size:18px;font-weight:700}}.time{{display:block;font-family:ui-monospace,Menlo,monospace;font-size:12px;color:var(--mute)}}.slot{{display:block;font-size:11.5px;color:var(--accent-ink);font-weight:600;margin-top:6px}}
.ref{{width:230px}}.ref img{{width:230px;display:block;border-radius:3px}}figure{{margin:0 0 8px}}figcaption{{font-size:11px;color:var(--mute);margin-top:3px;line-height:1.35}}
.vo{{width:150px;font-style:italic;color:var(--accent-ink)}}.vis{{width:340px}}.mot{{width:230px;color:var(--mute)}}.route{{width:190px}}.route p{{margin:6px 0 0;font-size:12px;color:var(--mute)}}.stab{{font-size:12px;margin-left:6px}}
details{{margin-top:8px}}summary{{cursor:pointer;font-size:12px;color:var(--diff);font-weight:600}}
pre{{white-space:pre-wrap;font-family:ui-monospace,Menlo,monospace;font-size:11.5px;line-height:1.5;background:var(--pre);padding:10px;border-radius:4px;margin:6px 0 0}}
.pool{{background:var(--panel);border:1px solid var(--line);border-radius:6px;padding:12px 14px;margin-bottom:12px}}.pool h4{{margin:0 0 4px;font-size:13px}}.muted{{color:var(--mute);font-size:12px;margin:6px 0 0}}
.sum td,.sum th{{padding:8px 10px;font-size:12.5px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:16px;color:var(--mute);font-size:12.5px}}.grid h3{{font-size:12.5px;margin:0 0 6px;color:var(--ink);text-transform:uppercase;letter-spacing:.06em}}.grid ul{{margin:0;padding-left:18px}}
</style>
<header>
<h1>{html.escape(spec.get('title',''))} <small>{html.escape(spec.get('subtitle',''))}</small></h1>
<div class="thesis">{spec.get('thesis','')}</div>
<div class="meta">{meta}</div>
<div class="legend"><b>生产方式：</b><span class="tag r-diff">DIFF</span> 扩散/视频生成出实拍质感 <span class="tag r-code">CODE</span> 程序化动效 <span class="tag r-mix">DIFF+CODE</span> 生成底板 + 程序化元素合成 <span class="tag r-ae">AE 一次性</span> 手搓一次母版复用 <span class="tag r-asset">素材/CODE</span> 依赖客户素材 · 稳/中/险 = 后续批量复现稳定性</div>
{('<div class="thesis"><b>全片不变量</b><ul>'+inv+'</ul></div>') if inv else ''}
{summary}
</header>
{tables}
{pool_sec}
<section class="grid">{foot}</section>
'''
    open(out,'w').write(page); print(f'wrote {out} ({len(page)//1024} KB)')

if __name__=='__main__': main()
