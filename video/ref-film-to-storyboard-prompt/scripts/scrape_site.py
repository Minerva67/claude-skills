#!/usr/bin/env python3
"""
Pull copy, palette and asset URLs out of a marketing site — including SPAs whose
text lives only in the JS bundle (curl of the HTML shows an empty <div id="root">).

Why: brand copy on screen must be letter-for-letter from the source. Reading the
bundle beats guessing, and it also surfaces hero image sequences / game art / spec
tables that the visible page hides behind scroll animations.

Usage:
    python3 scrape_site.py https://example.com [--out workdir]

Writes to --out (default ./site_dump):
    page.html, *.js, *.css   raw
    copy.txt                 de-duplicated human-readable strings (long first)
    palette.txt              CSS custom properties with hex values + font-family decls
    assets.txt               image/video/sequence URLs found in HTML/JS/CSS
Then Read copy.txt / palette.txt; download the assets you need with curl.
"""
import re, sys, os, html, urllib.request, urllib.parse

def fetch(u):
    req=urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'})
    return urllib.request.urlopen(req,timeout=30).read().decode('utf-8','ignore')

def main():
    url=sys.argv[1]; out='site_dump'
    if '--out' in sys.argv: out=sys.argv[sys.argv.index('--out')+1]
    os.makedirs(out,exist_ok=True)
    base=url if url.endswith('/') else url+'/'
    page=fetch(url); open(f'{out}/page.html','w').write(page)
    # collect js/css
    links=set(re.findall(r'(?:src|href)="([^"]+\.(?:js|css)[^"]*)"',page))
    blobs={'html':page}
    for l in links:
        full=urllib.parse.urljoin(base,l)
        try:
            b=fetch(full); name=os.path.basename(urllib.parse.urlparse(full).path); open(f'{out}/{name}','w').write(b); blobs[name]=b
        except Exception as e: print('skip',full,e)
    # follow one level of JS imports (vite chunks)
    for name,b in list(blobs.items()):
        if name.endswith('.js'):
            for imp in set(re.findall(r'from"(\./[^"]+\.js)"|import"(\./[^"]+\.js)"',b)):
                rel=[x for x in imp if x][0]; full=urllib.parse.urljoin(base+'assets/',rel.lstrip('./'))
                n=os.path.basename(rel)
                if n in blobs: continue
                try: blobs[n]=fetch(full); open(f'{out}/{n}','w').write(blobs[n])
                except Exception as e: print('skip',full,e)
    # copy
    strs=[]
    for name,b in blobs.items():
        if name=='html':
            t=re.sub(r'<(script|style|noscript)[^>]*>.*?</\1>','',b,flags=re.S|re.I); t=re.sub(r'<[^>]+>','\n',t); t=html.unescape(t)
            strs+= [x.strip() for x in t.split('\n') if len(x.strip())>3]
        else:
            # tokenize all three JS string kinds in one pass so quote pairing stays in sync,
            # then also grab anchored JSX/props strings (robust even if pairing drifts)
            for tok in re.findall(r'"(?:[^"\\\n]|\\.)*"|\'(?:[^\'\\\n]|\\.)*\'|`(?:[^`\\]|\\.)*`',b):
                if len(tok)>=6: strs.append(tok[1:-1])
            strs+= re.findall(r'(?:children|title|label|description|subtitle|headline|text|quote|name|tagline|body|caption|answer|question|alt|placeholder):\s*"((?:[^"\\]|\\.){4,})"',b)
    seen=[]
    human=re.compile(r"^[A-Za-z0-9'’‘“”\"\-–—.,:;!?&·№()%$+×/ ]+$")
    for s in strs:
        s=s.replace('\\n',' ').replace('\\"','"').strip()
        if s in seen or len(s)<4: continue
        cjk=re.search(r'[一-鿿]',s)
        words=len(re.findall(r'[A-Za-z]{2,}',s))
        code=re.search(r'[{}<>=`\\]|\bfunction\b|\breturn\b|\bconst\b|=>|\.\w+\(',s)
        if code: continue
        if cjk or (human.match(s) and words>=2) or (human.match(s) and s[:1].isupper() and words>=1 and len(s)<=40):
            seen.append(s)
    open(f'{out}/copy.txt','w').write('\n'.join(seen))
    # palette
    css='\n'.join(b for n,b in blobs.items() if n.endswith('.css'))
    pal=sorted(set(re.findall(r'--[\w-]+:\s*#[0-9a-fA-F]{3,8}',css)))
    fonts=sorted(set(re.findall(r'font-family:[^;}]+',css)))
    open(f'{out}/palette.txt','w').write('\n'.join(pal)+'\n\n'+'\n'.join(fonts))
    # assets
    allb='\n'.join(blobs.values())
    assets=sorted(set(re.findall(r'["\'(]((?:https?://|/)[^"\'()\s]+\.(?:png|jpe?g|webp|svg|gif|mp4|webm|m3u8|mov)(?:\?[^"\'()\s]*)?)',allb)))
    seqs=sorted(set(re.findall(r'"(/assets/[^"]*(?:sequence|frames?)[^"]*)"',allb)))
    open(f'{out}/assets.txt','w').write('\n'.join(assets)+'\n\n# possible frame sequences\n'+'\n'.join(seqs))
    print(f'{out}/copy.txt: {len(seen)} strings; palette: {len(pal)} vars; assets: {len(assets)}')

if __name__=='__main__': main()
