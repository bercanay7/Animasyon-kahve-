#!/usr/bin/env python3
"""Milliyet Gazete Arşivi (1950-2007) anahtar sözcük araması; OCR metniyle.
  python3 cernobil/tools/arsiv.py "radyasyonlu çay" --bas 1986-04-26 --son 1987-12-31 --sayfa 1-84 > cikti.jsonl
Sonuçlar tarihe göre azalan gelir. Oturum açmadan yalnız ilk sayfa (en yeni 10 sonuç) geliyor: dar sorgu kur. OCR hatalıdır (ı/i, l/ü karışır): alıntı sayfa görüntüsüyle doğrulanır.
Sayfa görüntüsü: https://gazetearsivi-api.milliyet.com.tr/api/v1/NewspaperImage<pageFolderName>
"""
import subprocess, urllib.parse, json, sys, re, time, argparse
UA={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36'}
def flight(html):
    parts=re.findall(r'self\.__next_f\.push\(\[1,"((?:[^"\\]|\\.)*)"\]\)',html)
    s=''.join(json.loads('"'+p+'"') for p in parts)
    refs={}; i=0
    # T-chunks: "id:T<hexlen>,<text>"
    for m in re.finditer(r'([0-9a-f]{1,3}):T([0-9a-f]{1,5}),',s):
        n=int(m.group(2),16); st=m.end()
        b=s[st:].encode('utf8')[:n].decode('utf8','ignore'); refs[m.group(1)]=b
    return s,refs
def sayfa(q,p):
    u='https://gazetearsivi.milliyet.com.tr/liste?basitArama='+urllib.parse.quote(q)+'&sayfaNo=%d'%p
    for k in range(3):
        r=subprocess.run(['curl','-s','-m','40','-A',UA['User-Agent'],u],capture_output=True)
        if r.returncode==0 and len(r.stdout)>1000: return r.stdout.decode('utf8','replace')
        time.sleep(2+k*3)
    return ''
ap=argparse.ArgumentParser(); ap.add_argument('q'); ap.add_argument('--bas',default='1986-04-26'); ap.add_argument('--son',default='1987-12-31'); ap.add_argument('--sayfa',default='1-5')
a=ap.parse_args(); p0,p1=map(int,a.sayfa.split('-'))
for p in range(p0,p1+1):
    h=sayfa(a.q,p); s,refs=flight(h)
    i=s.find('"result":[{"id"')
    if i<0: print('# sayfa',p,'sonuç yok (anonim erişimde yalnız ilk sayfa geliyor)',file=sys.stderr); break
    try: res=json.JSONDecoder().raw_decode(s[i+9:])[0]
    except Exception as e: print('# sayfa',p,'ayrıştırılamadı',e,file=sys.stderr); continue
    eski=False
    for r in res:
        d=r['date'][:10]
        if d<a.bas: eski=True
        if a.bas<=d<=a.son:
            ti=r.get('textInfo','');
            if isinstance(ti,str) and ti.startswith('$'): ti=refs.get(ti[1:],ti)
            print(json.dumps({'tarih':d,'sayfa':r['pageNumber'],'yayin':r.get('broadcastName'),'gorsel':r['pageFolderName'],'metin':ti},ensure_ascii=False),flush=True)
    print('# sayfa',p,res[0]['date'][:10],'…',res[-1]['date'][:10],file=sys.stderr)
    if eski: break
    time.sleep(0.5)
