#!/usr/bin/env python3
"""Talep kontrolü (CLAUDE.md, iş akışı 1a): YouTube Türkçe otomatik tamamlama + aramadaki ilk 10 videonun izlenmeleri.
  python3 araclar/talep/talep.py "sisifos" "dönüşüm kafka" ...
Not: ilk 10 içinde konu dışı videolar (şarkı, ürün, oyun) olabilir; öneri listesine bakarak yorumla. Ölçü kaba bir vekildir.
"""
import urllib.request, urllib.parse, json, sys, time, re
H={'User-Agent':'Mozilla/5.0','Accept-Language':'tr-TR,tr;q=0.9'}
def oner(q):
    u='https://suggestqueries-clients6.youtube.com/complete/search?client=youtube&ds=yt&hl=tr&gl=tr&q='+urllib.parse.quote(q)
    t=urllib.request.urlopen(urllib.request.Request(u,headers=H),timeout=15).read().decode('utf-8','replace')
    m=re.search(r'\((.*)\)\s*$',t,re.S); d=json.loads(m.group(1))
    return [x[0] for x in d[1]]
def ara(q):
    u='https://www.youtube.com/results?hl=tr&gl=TR&search_query='+urllib.parse.quote(q)
    t=urllib.request.urlopen(urllib.request.Request(u,headers=H),timeout=20).read().decode('utf-8','replace')
    m=re.search(r'var ytInitialData = (\{.*?\});</script>',t,re.S)
    if not m: return []
    d=json.loads(m.group(1)); out=[]
    def gez(o):
        if isinstance(o,dict):
            if 'videoRenderer' in o:
                v=o['videoRenderer']; vc=v.get('viewCountText',{}).get('simpleText','')
                n=re.sub(r'[^\d]','',vc); out.append(int(n) if n else 0)
            for x in o.values(): gez(x)
        elif isinstance(o,list):
            for x in o: gez(x)
    gez(d); return out[:10]
for q in sys.argv[1:]:
    try: s=oner(q)
    except Exception as e: s=['HATA '+str(e)[:40]]
    try: v=ara(q)
    except Exception as e: v=[]
    v=sorted(v,reverse=True); med=v[len(v)//2] if v else 0
    print(f"{q:22s} öneri {len(s):2d} | ilk10 en çok {v[0] if v else 0:>10,} medyan {med:>9,} | {' / '.join(s[:6])}")
    time.sleep(0.6)
