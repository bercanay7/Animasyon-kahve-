"""Whisper'sız hizalama (kapta Whisper yok, kurulum izni yok): metni biliyoruz; cümle sınırlarını sessizliklerden buluruz.
python3 tools/hizala.py [vo/s02_a.mp3 ...]   (argümansız: vo/s*_?.mp3 hepsi) → <çekim>.words.json + vo/hizalama_raporu.json
- Cümle sınırı: metin uzunluğundan beklenen zamana en yakın, en uzun sessizlik (dinamik programlama; sıra korunur).
- Kelime: cümlenin SESLİ karelerine harf uzunluğuyla dağıtılır (duraklamalara kelime düşmez).
Sınır: kelime zamanı tahmindir (±0,2–0,4 sn); telaffuz hatası yakalanmaz. Kulakla son onay kullanıcıda; Whisper kurulabilirse transcribe.py ile doğrulanır."""
import json, re, sys, os, glob, subprocess, numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SR = 16000
segs = {s['id']: s for s in json.load(open(os.path.join(ROOT, 'senaryo.json'), encoding='utf-8'))['segments']}
bol = {b['onek']: b for b in json.load(open(os.path.join(ROOT, 'vo', 'bolumler.json'), encoding='utf-8'))}
norm1 = lambda w: re.sub(r"[^\wçğıöşüâî]+", '', w.lower().replace('İ', 'i').replace('I', 'ı').replace("'", '').replace('’', '').replace('â', 'a').replace('î', 'i').replace('û', 'u'))
def words_of(text): return [w for w in (norm1(x) for x in re.sub(r'\[[^\]]*\]', ' ', text).replace('…', ' ').split()) if w]
def raw_words(text): return [x for x in re.sub(r'\[[^\]]*\]', ' ', text).replace('…', ' ').split() if norm1(x)]

SINIR = json.load(open(os.path.join(ROOT, 'vo', 'sinir.json'))) if os.path.exists(os.path.join(ROOT, 'vo', 'sinir.json')) else {}

def load(p):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True).stdout
    return np.frombuffer(raw, np.float32).copy()

def align(path):
    onek = os.path.basename(path)[:3]; b = bol[onek]; ids = b['ids']
    a = load(path); hop = SR // 100
    rms = np.sqrt(np.convolve(a ** 2, np.ones(hop * 3) / (hop * 3), 'same'))[::hop]
    thr = max(1e-4, np.percentile(rms, 20) * 2.2); v = rms > thr
    vi = np.where(v)[0]; t0, t1 = vi[0], vi[-1] + 1
    sil = []; i = t0
    while i < t1:
        if not v[i]:
            j = i
            while j < t1 and not v[j]: j += 1
            if j - i >= 12: sil.append((i, j))
            i = j
        else: i += 1
    # Birimler: her satır, içindeki cümle sonlarından (. ? ! … ve kapanan tırnak) alt cümlelere bölünür (Mary Stuart düzeltmesi:
    # iki cümleli satırlarda iç duraklama satır sınırı sanılıyordu). Hizalama birimler üzerinde yapılır; satır = birimlerinin birleşimi.
    units = []   # (satır sırası k, birim metni)
    for k, sid in enumerate(ids):
        t = re.sub(r'\[[^\]]*\]', ' ', segs[sid]['tts']).strip()
        parts = [x for x in re.split(r'(?<=[.!?…])["”]?\s+|(?<=:)\s+(?=["“])', t) if x.strip()]
        for x in parts: units.append((k, x))
    wgt = np.array([len(re.sub(r'\s', '', x)) + 6 * len(re.findall(r'[,;:]', x)) + 4 for _, x in units], float)
    cum = np.cumsum(wgt) / wgt.sum(); span = t1 - t0
    exp = [t0 + cum[k] * span for k in range(len(units) - 1)]
    cand = [(s, e) for s, e in sil if e - s >= 18]
    N, M = len(exp), len(cand)
    # elle zorlanan satır sınırları (vo/sinir.json: {"s03_b": {"D10": 52.5}} → D10'dan önceki sınır, bu anı içeren sessizlik)
    zor = {}
    for sid, tt in SINIR.get(os.path.basename(path).rsplit('.', 1)[0], {}).items():
        if sid.startswith('_'): continue
        k = ids.index(sid); u = min(n for n, (kk, _) in enumerate(units) if kk == k) - 1
        zor[u] = next(j for j, (s, e) in enumerate(cand) if s <= tt * 100 <= e)
    if N:
        sc0 = lambda k, j: 2.5 * min((cand[j][1] - cand[j][0]) / 100, 1.0) - (((cand[j][0] + cand[j][1]) / 2 - exp[k]) / (0.07 * span)) ** 2
        sc = lambda k, j: sc0(k, j) if k not in zor or zor[k] == j else -1e6
        dp = np.full((N, M), -1e9); bk = np.zeros((N, M), int)
        for j in range(M): dp[0][j] = sc(0, j)
        for k in range(1, N):
            best, bj = -1e9, -1
            for j in range(M):
                if j > 0 and dp[k - 1][j - 1] > best: best, bj = dp[k - 1][j - 1], j - 1
                if bj >= 0: dp[k][j] = best + sc(k, j); bk[k][j] = bj
        j = int(np.argmax(dp[N - 1])); pick = [j]
        for k in range(N - 1, 0, -1): j = bk[k][j]; pick.append(j)
        pick = pick[::-1]; bnd = [cand[j] for j in pick]
    else: bnd = []
    uedges = [(t0, None)] + [(e, s) for s, e in bnd] + [(None, t1)]
    # birim kenarları → kelimeler (her birimin sesli karelerine harf uzunluğuyla)
    out, rep, useg = [], [], {}
    for u, (k, txt) in enumerate(units):
        s0 = uedges[u][0]; s1 = uedges[u + 1][1]; sid = ids[k]
        useg.setdefault(k, [s0, s1]); useg[k][1] = s1
        fr = np.where(v[s0:s1])[0] + s0
        if len(fr) < 2: fr = np.arange(s0, max(s0 + 2, s1))
        ws, rw = words_of(txt), raw_words(txt)
        if not ws: continue
        L = np.array([len(norm1(x)) + 1.5 + (3 if re.search(r'[,;:.!?”]$', x) else 0) for x in rw], float)
        c = np.concatenate([[0], np.cumsum(L)]) / L.sum() * (len(fr) - 1)
        for n, w in enumerate(ws):
            fs, fe = fr[int(c[n])], fr[max(int(c[n]), int(c[n + 1]) - 1)]
            out.append({'w': w, 's': round(fs / 100, 3), 'e': round((fe + 1) / 100, 3), 'id': sid})
    # satır sınırındaki birim kenarı → rapor
    ub = {}
    for u in range(len(units) - 1):
        if units[u][0] != units[u + 1][0]: ub[units[u][0]] = (u, bnd[u] if u < len(bnd) else None)
    for k, sid in enumerate(ids):
        s0, s1 = useg[k]; x = ub.get(k)
        gapl = (x[1][1] - x[1][0]) if x and x[1] else None
        rep.append({'id': sid, 's': round(s0 / 100, 2), 'e': round(s1 / 100, 2), 'sinir_sessizlik': round(gapl / 100, 2) if gapl else None,
                    'beklenen_sapma': round((((x[1][0] + x[1][1]) / 2) - exp[x[0]]) / 100, 2) if x and x[1] else None})
    json.dump(out, open(path.rsplit('.', 1)[0] + '.words.json', 'w'), ensure_ascii=False)
    longsil = [round((e - s) / 100, 2) for s, e in sil if e - s > 140]
    return {'dosya': os.path.basename(path), 'sure': round(len(a) / SR, 2), 'konusma': round(span / 100, 2), 'uzun_sessizlik': longsil,
            'tepe_dB': float(round(20 * np.log10(float(np.abs(a).max()) + 1e-9), 1)), 'cumleler': rep}

files = sys.argv[1:] or sorted(glob.glob(os.path.join(ROOT, 'vo', 's*_?.mp3')))
R = [align(f) for f in files]
json.dump(R, open(os.path.join(ROOT, 'vo', 'hizalama_raporu.json'), 'w'), ensure_ascii=False, indent=1, default=float)
for r in R:
    zayif = [c['id'] for c in r['cumleler'] if c['sinir_sessizlik'] is not None and (c['sinir_sessizlik'] < .25 or abs(c['beklenen_sapma']) > 2.5)]
    print(f"{r['dosya']}: {r['sure']} sn, tepe {r['tepe_dB']} dB, uzun sessizlik {r['uzun_sessizlik']}, şüpheli sınır {zayif}")
