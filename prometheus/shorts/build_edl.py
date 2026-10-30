"""Shorts kurgu listesi: filmden kesintisiz bir kesit + 9:16 kırpma anahtarları + kelime vurgulu altyazı → shorts/edl.js, edl.json
Kullanım: python3 shorts/build_edl.py [a|b]   (varsayılan a)
Anlatım ve altyazı filmin kendi zaman çizelgesinden (timeline.js WORDS, 'd' = altyazı yazımı) gelir; yeni seslendirme gerekmez."""
import json, os, re, sys
D = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(D)
src = open(os.path.join(R, 'timeline.js'), encoding='utf8').read()
WORDS = json.loads(re.search(r'window\.WORDS = (\[.*?\]);', src, re.S).group(1))
CUES = json.loads(re.search(r'window\.CUES = (\{.*?\});', src, re.S).group(1))
def wd(sid, w, n=0):
    k = 0
    for x in WORDS:
        if x['id'] == sid and x['w'].startswith(w):
            if k == n: return x
            k += 1
    raise KeyError(f'{sid}@{w}#{n}')

# Kısa A: "Asıl tutsak kim?" (IX, doruk): kanca soru ilk saniyede; cevap ZEUS · KÖLE / PROMETHEUS · ÖZGÜR; son: terazi döner
SHORTS = {
  'a': dict(
    TITLE='PROMETHEUS',
    F0=wd('J01', 'bu', 1)['s'] - .3, F1=wd('J06', 'tutsak')['e'] + .9,
    # kırpma anahtarları: (film saniyesi, kırpma merkezi x, y, yakınlık); arada yumuşak geçiş
    KEYS=[(1055.2, 1330, 540, 1.0), (1056.6, 1250, 540, 1.0), (1062.0, 1050, 520, 1.0), (1067.6, 960, 560, 1.0), (1073.8, 960, 540, 1.0),
          (1077.2, 960, 560, 1.0), (1079.3, 960, 540, 1.0), (1081.5, 960, 540, 1.05), (1082.2, 1220, 540, 1.0), (1084.2, 1220, 540, 1.0),
          (1084.3, 960, 540, 1.0), (1091.4, 960, 540, 1.0), (1091.5, 960, 600, 1.0), (1097.2, 960, 540, 1.0),
          (1097.3, 960, 560, 1.0), (1102.5, 960, 560, 1.0), (1102.6, 560, 520, 1.0), (1104.8, 560, 520, 1.0), (1106.4, 1460, 540, 1.0), (1108.8, 1460, 540, 1.0)],
    LIGHT=[(1097.3, 1102.5)],  # açık (sayfa) zeminli aralıklar: altyazı mürekkep renginde
    CAP=1235),
}
K = sys.argv[1] if len(sys.argv) > 1 else 'a'
cfg = SHORTS[K]
F0, F1 = cfg['F0'], cfg['F1']; DUR = round(F1 - F0, 3)
# altyazı sözcükleri: kesite düşen sözcükler, Shorts saatine kaydırılır
words = [{'w': x['d'] or x['w'], 's': round(x['s'] - F0, 3), 'e': round(x['e'] - F0, 3)} for x in WORDS if x['s'] >= F0 - .05 and x['e'] <= F1 + .05 and (x['d'] or '').strip()]
# gruplar: noktalama ya da en fazla 3 sözcük (cümle sonu her zaman keser)
P = '.,:?!…”'
groups, cur = [], []
for i, w in enumerate(words):
    cur.append(w)
    nxt = words[i + 1] if i + 1 < len(words) else None
    gap = nxt and nxt['s'] - w['e'] > .45
    if w['w'][-1] in P or len(cur) >= 3 or gap: groups.append({'s': cur[0]['s'], 'e': cur[-1]['e'], 'words': cur}); cur = []
if cur: groups.append({'s': cur[0]['s'], 'e': cur[-1]['e'], 'words': cur})
for i in range(len(groups) - 1): groups[i]['e'] = min(groups[i]['e'] + .25, groups[i + 1]['s'] - .02)
# kırpma anahtarlarından kesitler (film kesintisiz: f = F0 + s)
keys = [(max(F0, k[0]), *k[1:]) for k in cfg['KEYS'] if k[0] <= F1]
if keys[0][0] > F0: keys.insert(0, (F0, *keys[0][1:]))
if keys[-1][0] < F1: keys.append((F1, *keys[-1][1:]))
EDL = []
for a, b in zip(keys, keys[1:]):
    s, e = round(a[0] - F0, 3), round(b[0] - F0, 3)
    if e - s < .02: continue
    light = any(l0 <= a[0] < l1 for l0, l1 in cfg.get('LIGHT', []))
    EDL.append(dict(s=s, e=e, f=round(a[0], 3), cx0=a[1], cx1=b[1], cy0=a[2], cy1=b[2], z0=a[3], z1=b[3], capY=cfg['CAP'], light=light))
CTA = round(DUR - 2.4, 3)
out = dict(TITLE=cfg['TITLE'], F0=round(F0, 3), F1=round(F1, 3), DUR=DUR, CTA=CTA, EDL=EDL, GROUPS=groups, WORDS=words)
json.dump(out, open(os.path.join(D, 'edl.json'), 'w'), ensure_ascii=False, indent=1)
open(os.path.join(D, 'edl.js'), 'w').write('// shorts/build_edl.py tarafından üretildi\nwindow.SHORT = ' + json.dumps(out, ensure_ascii=False) + ';\n')
print(K, 'süre', DUR, 'sn,', len(EDL), 'kesit,', len(groups), 'altyazı grubu, film', round(F0, 2), '→', round(F1, 2))
