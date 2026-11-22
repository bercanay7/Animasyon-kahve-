#!/usr/bin/env python3
"""Türkçe boşluk taraması: aynı konu Türkçe (hl=tr, gl=TR) ve İngilizce (hl=en, gl=US) aranır.
  python3 araclar/talep/iki_dil.py "lale çılgınlığı|tulip mania" ...
Çıktı: iki dilde öneri sayısı, ilk 10 izlenme, Türkçe başlıklı sonuçların en çok izleneni. Türkçe en çok izlenen küçük, İngilizce medyan büyükse konu "dünyada yankı, Türkçede boşluk" adayıdır. Türkçe başlık tespiti kaba (harf ve sık sözcük)."""
import urllib.request, urllib.parse, json, sys, time, re
H={'User-Agent':'Mozilla/5.0'}
def get(u,lang): 
    h=dict(H); h['Accept-Language']=lang
    return urllib.request.urlopen(urllib.request.Request(u,headers=h),timeout=20).read().decode('utf-8','replace')
def oner(q,hl,gl):
    t=get('https://suggestqueries-clients6.youtube.com/complete/search?client=youtube&ds=yt&hl=%s&gl=%s&q='%(hl,gl)+urllib.parse.quote(q),hl)
    return [x[0] for x in json.loads(re.search(r'\((.*)\)\s*$',t,re.S).group(1))[1]]
def ara(q,hl,gl):
    t=get('https://www.youtube.com/results?hl=%s&gl=%s&search_query='%(hl,gl)+urllib.parse.quote(q),hl)
    m=re.search(r'var ytInitialData = (\{.*?\});</script>',t,re.S); out=[]
    if not m: return out
    def gez(o):
        if isinstance(o,dict):
            if 'videoRenderer' in o:
                v=o['videoRenderer']; n=re.sub(r'[^\d]','',v.get('viewCountText',{}).get('simpleText',''))
                ti=''.join(r.get('text','') for r in v.get('title',{}).get('runs',[]))
                out.append((int(n) if n else 0,ti))
            for x in o.values(): gez(x)
        elif isinstance(o,list):
            for x in o: gez(x)
    gez(json.loads(m.group(1))); return out[:10]
TR=re.compile(r'[çğışöüÇĞİŞÖÜ]|\b(ve|bir|nasıl|neden|nedir|depremi|tarihi)\b',re.I)
for pair in sys.argv[1:]:
    tq,eq=pair.split('|')
    try: so=oner(tq,'tr','TR')
    except Exception: so=[]
    try: r=ara(tq,'tr','TR')
    except Exception: r=[]
    trv=[v for v,t in r if TR.search(t)]
    try: se=oner(eq,'en','US')
    except Exception: se=[]
    try: re_=ara(eq,'en','US')
    except Exception: re_=[]
    ev=sorted([v for v,t in re_],reverse=True)
    trs=sorted(trv,reverse=True)
    print(f"TR {tq!r}: öneri {len(so)}, ilk10'da Türkçe başlık {len(trv)}, en çok {trs[0] if trs else 0:,}, medyan {trs[len(trs)//2] if trs else 0:,}")
    for v,t in sorted(r,reverse=True)[:4]: print(f"     {v:>10,}  {t[:80]}")
    print(f"EN {eq!r}: öneri {len(se)}, ilk10 en çok {ev[0] if ev else 0:,}, medyan {ev[len(ev)//2] if ev else 0:,} | {' / '.join(se[:4])}")
    print()
    time.sleep(0.5)
