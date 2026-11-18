import sys, json, urllib.request, urllib.parse, time, re
def ac(q):
    u = "https://suggestqueries-clients6.youtube.com/complete/search?client=youtube&ds=yt&hl=tr&gl=tr&q=" + urllib.parse.quote(q)
    raw = urllib.request.urlopen(u, timeout=15).read()
    try: s = raw.decode('utf-8')
    except UnicodeDecodeError: s = raw.decode('iso-8859-9')
    m = re.search(r'\((.*)\)\s*$', s, re.S)
    d = json.loads(m.group(1))
    return [x[0] for x in d[1]]
for q in sys.argv[1:]:
    try: r = ac(q)
    except Exception as e: r = ["HATA "+str(e)]
    print(f"## {q}\n  " + " | ".join(r))
    time.sleep(0.6)
