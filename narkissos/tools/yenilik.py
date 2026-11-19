"""Yenilik aralıkları (CLAUDE.md kurgu önerisi: 3–5 sn'de bir yenilik): kesme ya da sözcüğe bağlı eylem olmadan geçen süreler.
python3 tools/yenilik.py [eşik=5.0] [--hepsi] [--en=15]     TL=vo/oneri/timeline_oneri.js ile başka zaman çizelgesi
İşaretler: plan başları (planlar.json 'at') + plan eylemleri ('eylem'[].at) + film sonu. Eşiği aşan aralıklar planıyla listelenir;
--en=N en uzun N aralığı (eşik altı dahil) yazar; --hepsi her planın içindeki en uzun boşluğu da yazar.
Çıkış kodu: eşiği aşan aralık varsa 1 (bitiş ekranı, DUR-20 sonrası, bilgi olarak yazılır ve sayılmaz)."""
import json, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
tl = open(os.environ.get('TL') or os.path.join(ROOT, 'timeline.js'), encoding='utf-8').read()
CUES = json.loads(re.search(r'window\.CUES = (\{.*?\});', tl, re.S).group(1))
WORDS = json.loads(re.search(r'window\.WORDS = (\[.*?\]);', tl, re.S).group(1))
DUR = float(re.search(r'window\.DUR\s*=\s*([\d.]+)', tl).group(1))
P = json.load(open(os.path.join(ROOT, 'planlar.json'), encoding='utf-8'))
args = [a for a in sys.argv[1:] if not a.startswith('--')]; ESIK = float(args[0]) if args else 5.0
EN = next((int(a.split('=')[1]) for a in sys.argv if a.startswith('--en=')), 10)
norm = lambda w: re.sub(r'[^\wçğıöşü]', '', w.lower().replace('â', 'a').replace('î', 'i').replace('û', 'u'))
def A(at):   # film.js A() ile aynı
    m = re.match(r'^([A-Z]\d+[a-z]?)(?:@([^#+-]+)(?:#(\d+))?)?([+-][\d.]+)?$', at)
    sid, w, n, off = m.group(1), m.group(2), int(m.group(3) or 0), float(m.group(4) or 0)
    t = CUES[sid]['s']
    if w:
        hits = [x for x in WORDS if x['id'] == sid and x['w'].startswith(norm(w))]
        if len(hits) > n: t = hits[n]['s']
    return round(t + off, 3)
rows = sorted((A(p['at']), pid) for pid, p in P.items())
isaret = []   # (zaman, tür, plan)
for t, pid in rows:
    isaret.append((t, 'kesme', pid))
    for e in P[pid].get('eylem', []): isaret.append((A(e['at']), 'eylem', pid))
isaret.append((DUR, 'son', None)); isaret.sort()
def plan_of(t):   # t anında süren plan (başlangıcı ≤ t olan son plan)
    q = rows[0][1]
    for s, pid in rows:
        if s <= t + 1e-6: q = pid
    return q
araliklar = []
prev = 0.0
for t, tur, pid in isaret:
    if t - prev > 1e-6: araliklar.append((prev, t, round(t - prev, 2), plan_of(prev)))
    prev = max(prev, t)
BIT = DUR - 20.0
mm = lambda t: f'{int(t // 60)}:{t % 60:04.1f}'
asan = [a for a in araliklar if a[2] > ESIK and a[0] < BIT]
bit = [a for a in araliklar if a[2] > ESIK and a[0] >= BIT]
print(f'{len(rows)} plan, {len(isaret) - 1} işaret (kesme + sözcüğe bağlı eylem), DUR {DUR}; eşik {ESIK} sn')
print(f'eşiği aşan aralık: {len(asan)}' + ('' if asan else ' (yok)'))
for a, b, d, pid in asan: print(f'  {mm(a)}–{mm(b)}  {d:5.2f} sn  {pid} {P[pid]["set"]} {P[pid]["olcek"]}  {P[pid]["at"]}')
if bit: print('bitiş ekranında (sayılmaz):', ', '.join(f'{mm(a)} {d:.2f} sn' for a, b, d, _ in bit))
print(f'en uzun {EN} aralık:')
for a, b, d, pid in sorted(araliklar, key=lambda x: -x[2])[:EN]: print(f'  {d:5.2f} sn  {mm(a)}–{mm(b)}  {pid} {P[pid]["set"]}' + ('  (bitiş ekranı)' if a >= BIT else ''))
if '--hepsi' in sys.argv:
    print('plan içi en uzun boşluk:')
    for t, pid in rows:
        ic = [d for a, b, d, q in araliklar if q == pid]; print(f'  {pid} {max(ic) if ic else 0:5.2f} sn')
sys.exit(1 if asan else 0)
