import sys, json, urllib.request, urllib.parse, re, time
def search(q, n=12):
    u = "https://www.youtube.com/results?hl=tr&gl=TR&search_query=" + urllib.parse.quote(q)
    req = urllib.request.Request(u, headers={"User-Agent":"Mozilla/5.0","Accept-Language":"tr-TR,tr;q=0.9"})
    html = urllib.request.urlopen(req, timeout=20).read().decode('utf-8','replace')
    m = re.search(r'var ytInitialData = (\{.*?\});</script>', html, re.S)
    if not m: return ["(ytInitialData yok)"]
    d = json.loads(m.group(1))
    out=[]
    def walk(o):
        if isinstance(o, dict):
            if 'videoRenderer' in o:
                v=o['videoRenderer']
                t=''.join(r.get('text','') for r in v.get('title',{}).get('runs',[]))
                vc=v.get('viewCountText',{}).get('simpleText') or ''.join(r.get('text','') for r in v.get('viewCountText',{}).get('runs',[]))
                ch=''.join(r.get('text','') for r in v.get('ownerText',{}).get('runs',[]))
                ln=v.get('lengthText',{}).get('simpleText','')
                pt=v.get('publishedTimeText',{}).get('simpleText','')
                out.append(f"{vc:>22} | {ln:>8} | {pt:>14} | {ch[:28]:28} | {t[:90]}")
                return
            for x in o.values(): walk(x)
        elif isinstance(o, list):
            for x in o: walk(x)
    walk(d)
    return out[:n]
for q in sys.argv[1:]:
    try: r=search(q)
    except Exception as e: r=["HATA "+str(e)]
    print(f"### {q}"); print("\n".join(r)); time.sleep(1.0)
