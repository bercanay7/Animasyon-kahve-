"""Cümle düzeyinde, Whisper'sız hizalama (hizala.py'nin düzeltilmiş hâli; plan denetimi 18 Kasım: F11 4,9 sn'ye sıkışmıştı).
hizala.py yalnız BÖLÜM (senaryo cümlesi) sınırlarını sessizliğe oturtuyordu; bölüm içindeki cümleler (". ? ! :" + büyük harf)
sessizlik sayımına girmediği için sınırlar bir iki cümle kayabiliyordu (s08: F05 bir cümle fazla, F11 iki cümle eksik).
Burada her alt cümle bir birimdir; birim sınırları sırayla sessizliklere oturtulur (dinamik programlama):
  ödül = sessizlik uzunluğu; ceza = birim öbeğinin süresinin harf sayısından beklenen süreden log sapması;
  bölüm (senaryo kimliği) sınırı atlanamaz, bölüm içi cümle sınırı sessizliksiz geçilebilir (küçük ceza).
Kelimeler birimin SESLİ karelerine harf uzunluğuyla dağıtılır (hizala.py ile aynı).
Kullanım: python3 tools/hizala_cumle.py vo/s08_b.mp3 [...] [--out KLASÖR]   (çıktı <KLASÖR>/<çekim>.words.json; varsayılan vo/oneri/,
  vo/'daki çekim hizalamasının üstüne yazmaz. Uygulamak: cp vo/oneri/s0*.words.json vo/ && python3 tools/build_vo.py)
Rapor: her birimin süresi ve sn/harf hızı (0,055–0,095 dışı şüpheli)."""
import json, re, sys, os, subprocess, numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SR = 16000
segs = {s['id']: s for s in json.load(open(os.path.join(ROOT, 'senaryo.json'), encoding='utf-8'))['segments']}
bol = {b['onek']: b for b in json.load(open(os.path.join(ROOT, 'vo', 'bolumler.json'), encoding='utf-8'))}
norm1 = lambda w: re.sub(r"[^\wçğıöşüâî]+", '', w.lower().replace('İ', 'i').replace('I', 'ı').replace("'", '').replace('’', '').replace('â', 'a').replace('î', 'i').replace('û', 'u'))
def clean(t): return re.sub(r'\[[^\]]*\]', ' ', t).replace('…', ' ')

def units(sid):
    """Senaryo cümlesini alt cümlelere böler: [.?!:] (+ kapanış tırnağı) + boşluk + büyük harf ya da açılış tırnağı."""
    raw = [x for x in clean(segs[sid]['tts']).split() if norm1(x)]
    out, cur = [], []
    for k, x in enumerate(raw):
        cur.append(x)
        nxt = raw[k + 1] if k + 1 < len(raw) else None
        if nxt and re.search(r'[.?!:]["”’]?$', x) and (nxt[0] in '“"' or nxt[0].isupper()):
            out.append(cur); cur = []
    if cur: out.append(cur)
    return out

def load(p):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True).stdout
    return np.frombuffer(raw, np.float32).copy()

def align(path, outdir):
    onek = os.path.basename(path)[:3]; ids = bol[onek]['ids']
    a = load(path); hop = SR // 100
    rms = np.sqrt(np.convolve(a ** 2, np.ones(hop * 3) / (hop * 3), 'same'))[::hop]
    thr = max(1e-4, np.percentile(rms, 20) * 2.2); v = rms > thr
    vi = np.where(v)[0]; t0, t1 = int(vi[0]), int(vi[-1] + 1)
    sil = []; i = t0
    while i < t1:
        if not v[i]:
            j = i
            while j < t1 and not v[j]: j += 1
            if j - i >= 15: sil.append((i, j))
            i = j
        else: i += 1
    U = []   # (sid, [ham kelimeler], ağırlık, bölüm sonu mu)
    for sid in ids:
        us = units(sid)
        for k, u in enumerate(us):
            w = sum(len(norm1(x)) + 1.0 for x in u) + 6 * sum(1 for x in u[:-1] if re.search(r'[,;]$', x))
            U.append((sid, u, w, k == len(us) - 1))
    W = np.array([u[2] for u in U]); span = t1 - t0
    # konuşma hızı: toplam süreden sessizlikler (sınır sayısı kadar ortalama) düşülerek
    rate = (span - 45 * (len(U) - 1)) / W.sum()
    n, M = len(U), len(sil)
    # düğümler: 0 = konuşma başı; 1..M = sessizlikler; M+1 = konuşma sonu
    st = [t0] + [e for s, e in sil] + [None]      # düğümden sonra konuşmanın başladığı kare
    en = [None] + [s for s, e in sil] + [t1]      # düğümde konuşmanın bittiği kare
    rew = [0] + [1.6 * min((e - s) / 55, 1.0) for s, e in sil] + [0]
    cum = np.concatenate([[0], np.cumsum(W)])
    INF = 1e18
    dp = np.full((n + 1, M + 2), INF); bk = {}
    dp[0][0] = 0
    for k in range(1, n + 1):
        for j in range(1, M + 2):
            if (j == M + 1) != (k == n): continue
            best, arg = INF, None
            for kp in range(k - 1, -1, -1):
                # kp..k-1 arası birimler tek öbek; arada bölüm sınırı atlanamaz
                if kp < k - 1 and U[kp][3]: break   # U[kp] bölüm sonuysa kp+1'e geçmek sınır atlamak olur
                if k - kp > 4: break
                for jp in range(0, j):
                    if dp[kp][jp] >= INF: continue
                    d = en[j] - st[jp]
                    if d <= 10: continue
                    exp = (cum[k] - cum[kp]) * rate
                    c = dp[kp][jp] + 9 * np.log(d / exp) ** 2 - rew[j] + 1.2 * (k - kp - 1)
                    if c < best: best, arg = c, (kp, jp)
            dp[k][j] = best; bk[(k, j)] = arg
    path_ = []; k, j = n, M + 1
    while k > 0:
        kp, jp = bk[(k, j)]; path_.append((kp, k, jp, j)); k, j = kp, jp
    path_.reverse()
    out, rep = [], []
    for kp, k, jp, j in path_:
        s0, s1 = st[jp], en[j]
        fr = np.where(v[s0:s1])[0] + s0
        grp = U[kp:k]
        rw = [x for u in grp for x in u[1]]; own = [u[0] for u in grp for _ in u[1]]
        L = np.array([len(norm1(x)) + 1.5 + (3 if re.search(r'[,;:.!?”]$', x) else 0) for x in rw], float)
        c = np.concatenate([[0], np.cumsum(L)]) / L.sum() * (len(fr) - 1)
        for q, x in enumerate(rw):
            fs, fe = fr[int(c[q])], fr[max(int(c[q]), int(c[q + 1]) - 1)]
            out.append({'w': norm1(x), 's': round(fs / 100, 3), 'e': round((fe + 1) / 100, 3), 'id': own[q]})
        ch = sum(len(norm1(x)) for x in rw)
        rep.append({'birim': ' '.join(rw)[:60], 'id': grp[0][0], 's': round(s0 / 100, 2), 'e': round(s1 / 100, 2),
                    'sn_harf': round((s1 - s0) / 100 / max(1, ch), 3), 'birlesik': k - kp})
    os.makedirs(outdir, exist_ok=True)
    json.dump(out, open(os.path.join(outdir, os.path.basename(path).rsplit('.', 1)[0] + '.words.json'), 'w'), ensure_ascii=False)
    return rep

args = sys.argv[1:]; outdir = os.path.join(ROOT, 'vo', 'oneri')
if '--out' in args: k = args.index('--out'); outdir = args[k + 1]; del args[k:k + 2]
for f in args:
    rep = align(f, outdir)
    print('==', os.path.basename(f))
    cid = None
    for r in rep:
        flag = '  <<< şüpheli hız' if not (0.055 <= r['sn_harf'] <= 0.095) else ''
        print(f"  {r['id'] if r['id'] != cid else '   '} {r['s']:7.2f}–{r['e']:7.2f}  {r['sn_harf']:.3f}{' (' + str(r['birlesik']) + ' cümle)' if r['birlesik'] > 1 else ''}  {r['birim']}{flag}")
        cid = r['id']
