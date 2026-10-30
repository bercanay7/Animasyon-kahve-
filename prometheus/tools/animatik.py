"""Plan listesini (animatik/planlar.json) gerçek ses zamanlamasına (timeline.js) oturtur.
Her planın başlangıcını, süresini ve bağlı olduğu sözü hesaplar; kuralları denetler:
  - 8 sn'yi geçen plan (içinde olay ya da kamera değişimi gerekir), 1,2 sn'den kısa plan (göz yetişmez);
  - bulunamayan kelime çapası; sırası bozuk plan.
Kullanım: python3 tools/animatik.py  → animatik/plan_tablosu.md + animatik/zamanli.json"""
import json, re, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
js = open(os.path.join(ROOT, 'timeline.js')).read()
grab = lambda name: json.loads(re.search(r'window\.' + name + r' = (.*?);\n', js, re.S).group(1))
CUES, WORDS, DUR = grab('CUES'), grab('WORDS'), float(re.search(r'window\.DUR = ([\d.]+)', js).group(1))
d = json.load(open(os.path.join(ROOT, 'animatik', 'planlar.json')))
segs = {s['id']: s for s in json.load(open(os.path.join(ROOT, 'senaryo.json')))['segments']}
nw = lambda w: re.sub(r'[^\wçğıöşü]', '', w.replace('İ', 'i').replace('I', 'ı').lower().replace('â', 'a').replace('î', 'i').replace('û', 'u'))

def anchor(at):
    m = re.match(r'^([A-Z]\d+[a-z]?)(?:@([^#]+)(?:#(\d+))?)?$', at)
    sid, w, n = m.group(1), m.group(2), int(m.group(3) or 0)
    if sid not in CUES: return None, f'cümle yok: {sid}'
    if not w: return CUES[sid]['s'], None
    k = 0
    for x in WORDS:
        if x['id'] == sid and x['w'].startswith(nw(w)):
            if k == n: return x['s'], None
            k += 1
    return CUES[sid]['s'], f'kelime yok: {at}'

rows, errs = [], []
for p in d['planlar']:
    t, e = anchor(p['at'])
    if e: errs.append(f"{p['id']}: {e}")
    rows.append({**p, 't': t if t is not None else 0})
# ilk plan filmin başından başlar (sessiz giriş)
rows[0]['t'] = 0.0
for i, r in enumerate(rows):
    r['bitis'] = rows[i + 1]['t'] if i + 1 < len(rows) else DUR
    r['sure'] = round(r['bitis'] - r['t'], 2)
    if r['sure'] <= 0: errs.append(f"{r['id']}: sıra bozuk ({r['at']} → {rows[i + 1]['at'] if i + 1 < len(rows) else 'son'})")
    sid = re.match(r'^([A-Z]\d+[a-z]?)', r['at']).group(1)
    # planın üstüne düşen anlatım (altyazı kelimeleri)
    r['soz'] = ' '.join(x['d'] for x in WORDS if r['t'] - 1e-3 <= x['s'] < r['bitis'] - 1e-3 and x['d'])
fmt = lambda s: f'{int(s // 60)}:{s % 60:04.1f}'
uzun = [r for r in rows if r['sure'] > 8]; kisa = [r for r in rows if r['sure'] < 1.2]
sures = sorted(r['sure'] for r in rows)
out = [f"# Animatik: zamanlı plan tablosu\n",
       f"Film süresi {fmt(DUR)} · {len(rows)} plan · ortalama {DUR / len(rows):.1f} sn · ortanca {sures[len(sures) // 2]:.1f} sn · 8 sn'yi geçen {len(uzun)} · 1,2 sn'den kısa {len(kisa)}\n"]
if errs: out += ['**Çapa hataları:**\n'] + [f'- {e}' for e in errs] + ['']
sec = None
for r in rows:
    b = segs[re.match(r'^([A-Z]\d+[a-z]?)', r['at']).group(1)]['bolum']
    if b != sec:
        sec = b; out += [f"\n## {b}\n", '| plan | başlangıç | süre | katman | set | kare | hareket | söz |', '|---|---|---|---|---|---|---|---|']
    flag = ' ⚠' if r['sure'] > 8 or r['sure'] < 1.2 else ''
    kare = r['kare'] + (f" **[yazı: {r['yazi']}]**" if r.get('yazi') else '') + (f" _(geçiş: {r['gecis']})_" if r.get('gecis') else '')
    out.append(f"| {r['id']} | {fmt(r['t'])} | {r['sure']:.1f}{flag} | {r['k']} | {r['set']} | {kare} | {r['hareket']} | {r['soz'][:140]} |")
open(os.path.join(ROOT, 'animatik', 'plan_tablosu.md'), 'w').write('\n'.join(out) + '\n')
json.dump([{k: r[k] for k in ('id', 'at', 't', 'sure', 'k', 'set')} for r in rows], open(os.path.join(ROOT, 'animatik', 'zamanli.json'), 'w'), ensure_ascii=False, indent=0)
print(out[1].strip())
for e in errs: print('  HATA', e)
for r in uzun: print(f"  uzun {r['id']} {r['sure']:.1f} sn  {r['soz'][:90]}")
for r in kisa: print(f"  kısa {r['id']} {r['sure']:.1f} sn  {r['soz'][:90]}")
