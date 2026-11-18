"""Seslendirme yaması: birkaç cümleyi yeniden okunmuş çekimle değiştirir, filmin geri kalanının zamanı değişmez.
Çekim (vo/yama/<ID>_<a|b>.mp3) önde bir bağlam cümlesiyle okunur (doğal tonlama için); bağlam kesilip atılır.
Yeni cümle eski klibin yerine, konuşma başı eski cümle başına (CUES[id].s) gelecek biçimde oturtulur;
sonraki klibe taşarsa önceki sessizlikten pay alınır, yine sığmazsa hata verir (zaman kaydırılmaz).
Kelime zamanları hizala.py'deki gibi: cümlenin sesli karelerine harf uzunluğuyla dağıtılır.
Kullanım:
  python3 tools/yama_vo.py analiz             → iki çekimi karşılaştırır (hız, düzey, tını), öneri yazar
  python3 tools/yama_vo.py uygula F02=a:durak.25 L17=a:komsu1 L20=b
      → vo/vo.wav ve timeline.js yamanır (eskileri vo/yama/eski_* olarak saklanır).
      durakX: cümle içindeki ≥ 150 ms duraklamalar en çok X sn'ye kısaltılır (sessizlikte kesilir; hız değişmez).
      komsuX: düzey eski cümleye değil, komşu iki cümlenin ortalamasının X dB üstüne eşitlenir
      (eski okuma bilerek farklıysa, ör. haykırış; varsayılan: eski cümlenin düzeyi).
Metin: vo/yama/istemler.json ({id: {baglam, cumle}}); senaryo.json'daki tts/alt elle güncellenir."""
import json, re, sys, os, subprocess, wave, shutil, numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
SR = 48000; HOP = SR // 100
IST = json.load(open('vo/yama/istemler.json'))
SEG = {s['id']: s for s in json.load(open('senaryo.json'))['segments']}
MERGE = {k: v for k, v in json.load(open('tools/merge.json')).items() if not k.startswith('_')}
TL = open('timeline.js').read()
CUES = json.loads(re.search(r'window\.CUES = (\{.*?\});', TL, re.S).group(1))
WORDS = json.loads(re.search(r'window\.WORDS = (\[.*?\]);', TL, re.S).group(1))
DUR = float(re.search(r'window\.DUR = ([\d.]+)', TL).group(1))
IDS = list(CUES.keys())
norm1 = lambda w: re.sub(r"[^\wçğıöşüâî]+", '', w.lower().replace('İ', 'i').replace('I', 'ı').replace("'", '').replace('’', '').replace('â', 'a').replace('î', 'i').replace('û', 'u'))
def words_of(t): return [w for w in (norm1(x) for x in re.sub(r'\[[^\]]*\]', ' ', t).replace('…', ' ').split()) if w]

def load(p):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True).stdout
    return np.frombuffer(raw, np.float32).copy()
def zarf(a):
    rms = np.sqrt(np.convolve(a ** 2, np.ones(HOP * 3) / (HOP * 3), 'same'))[::HOP]
    return rms, max(1e-4, np.percentile(rms, 20) * 2.2)
def db(x): return 20 * np.log10(max(1e-9, x))
def sesli_rms(a, thr):
    rms, _ = zarf(a); v = rms[rms > thr]; return float(np.sqrt(np.mean(v ** 2))) if len(v) else 1e-9
def tini(a, thr):   # sesli karelerin ortalama log-bant spektrumu (24 bant, 80 Hz–8 kHz)
    n = 2048; rms, _ = zarf(a); out = []
    edges = np.geomspace(80, 8000, 25); f = np.fft.rfftfreq(n, 1 / SR)
    for i in np.where(rms > thr)[0][::3]:
        c = i * HOP; fr = a[max(0, c - n // 2):c + n // 2]
        if len(fr) < n: continue
        m = np.abs(np.fft.rfft(fr * np.hanning(n)))
        out.append([np.log10(np.mean(m[(f >= edges[k]) & (f < edges[k + 1])] ** 2) + 1e-12) for k in range(24)])
    s = np.mean(out, 0); return s - s.mean()

VO = None
def vo():
    global VO
    if VO is None:
        w = wave.open('vo/vo.wav'); VO = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32767
    return VO
def klip_sinir(t):   # t anını içeren klibin [baş, son) (klipler arası dijital sıfır ≥ 50 ms)
    a = vo(); i = int(t * SR); z = a == 0; n = int(.05 * SR)
    j = i
    while j > 0 and not z[j - n:j].all(): j -= 1
    k = i
    while k < len(a) and not z[k:k + n].all(): k += 1
    return j / SR, k / SR
def baglam_suresi(sid, metin):   # bağlam cümlesinin özgün okumadaki süresi (kelime zamanlarından)
    ws = words_of(metin); prev = IDS[IDS.index(sid) - 1]; pw = [w for w in WORDS if w['id'] == prev]
    tail = pw[-len(ws):]
    return (tail[-1]['e'] - tail[0]['s']) if [w['w'] for w in tail] == ws else None, prev, tail

def ayir(a, sid):   # bağlam | hedef sınırı: harf payına en yakın, ≥ 150 ms sessizlik
    rms, thr = zarf(a); v = rms > thr
    bt, ht = IST[sid]['baglam'], IST[sid]['cumle']
    pay = len(re.sub(r'\W', '', bt)) / len(re.sub(r'\W', '', bt + ht))
    cum = np.cumsum(v) / max(1, v.sum())
    runs, i = [], 0
    while i < len(v):
        if not v[i]:
            j = i
            while j < len(v) and not v[j]: j += 1
            if j - i >= 15 and i > 0 and j < len(v): runs.append((i, j))
            i = j
        else: i += 1
    r = min(runs, key=lambda r: abs(cum[r[0]] - pay))
    on = r[1]; off = len(v) - 1
    while off > on and not v[off]: off -= 1
    return r, on * .01, (off + 1) * .01, thr, (np.where(v)[0][0] * .01, r[0] * .01)

def analiz():
    a0 = vo(); _, thr0 = zarf(a0[int(300 * SR):int(400 * SR)])
    rapor = {}
    for sid in IST:
        c = CUES[sid]; eski = a0[int(c['s'] * SR):int(c['e'] * SR)]
        bsure, prev, tail = baglam_suresi(sid, IST[sid]['baglam'])
        eski_b = a0[int(tail[0]['s'] * SR):int(tail[-1]['e'] * SR)] if tail else None
        nxt = IDS[IDS.index(sid) + 1] if IDS.index(sid) + 1 < len(IDS) else None
        k0, k1 = klip_sinir((c['s'] + c['e']) / 2)
        sonraki = klip_sinir(CUES[nxt]['s'])[0] if nxt else DUR
        print(f"\n{sid}: eski {c['e'] - c['s']:.2f} sn, klip {k0:.2f}–{k1:.2f}, sonraki klip {sonraki:.2f} (yer {sonraki - c['s'] - .1:.2f} sn)")
        for tk in 'ab':
            p = f'vo/yama/{sid}_{tk}.mp3'; a = load(p)
            r, on, off, thr, (b0, b1) = ayir(a, sid)
            hedef, bag = a[int(on * SR):int(off * SR)], a[int(b0 * SR):int(b1 * SR)]
            g = db(sesli_rms(eski, thr0)) - db(sesli_rms(hedef, thr))
            dt = np.sqrt(np.mean((tini(hedef * 10 ** (g / 20), thr * 10 ** (g / 20)) - tini(eski, thr0)) ** 2))
            db_ = np.sqrt(np.mean((tini(bag, thr) - tini(eski_b, thr0)) ** 2)) if eski_b is not None else float('nan')
            hiz = (off - on) / (c['e'] - c['s']); bh = (b1 - b0) / bsure if bsure else float('nan')
            sig = c['s'] + (off - on) + .1 <= sonraki
            print(f"  {tk}: hedef {off - on:.2f} sn (eskinin ×{hiz:.2f}), bağlam ×{bh:.2f}, kazanç {g:+.1f} dB, tını farkı {dt:.3f} (bağlamda {db_:.3f}), sığar {sig}")
            rapor.setdefault(sid, {})[tk] = {'sure': off - on, 'hiz': hiz, 'baglam_hiz': bh, 'kazanc_db': g, 'tini': dt, 'tini_baglam': db_, 'sigar': bool(sig)}
    json.dump(rapor, open('vo/yama/analiz.json', 'w'), indent=1)

def uygula(secim):
    a0 = vo().copy(); _, thr0 = zarf(a0[int(300 * SR):int(400 * SR)])
    shutil.copy('vo/vo.wav', 'vo/yama/eski_vo.wav'); shutil.copy('timeline.js', 'vo/yama/eski_timeline.js')
    global WORDS
    for sid, tk in secim.items():
        c = CUES[sid]; eski = a0[int(c['s'] * SR):int(c['e'] * SR)]
        tk, *ops = tk.split(':'); ops = {o.rstrip('0123456789.'): float(o[len(o.rstrip('0123456789.')):]) for o in ops}
        a = load(f'vo/yama/{sid}_{tk}.mp3'); r, on, off, thr, _ = ayir(a, sid)
        if 'durak' in ops:   # iç duraklamaları kısalt (sessiz karelerin ortasından kes, 10 ms geçiş)
            rms, _ = zarf(a[int(on * SR):int(off * SR)]); v = rms > thr; i = 0; kes = []
            while i < len(v):
                if not v[i]:
                    j = i
                    while j < len(v) and not v[j]: j += 1
                    if j - i >= 15 and i > 0 and j < len(v) and (j - i) * .01 > ops['durak']: kes.append((on + i * .01, on + j * .01))
                    i = j
                else: i += 1
            for t0, t1 in reversed(kes):
                fazla = (t1 - t0) - ops['durak']; m0 = (t0 + t1) / 2 - fazla / 2; m1 = m0 + fazla
                x0, x1 = int(m0 * SR), int(m1 * SR); f2 = int(.01 * SR)
                bas, son = a[:x0].copy(), a[x1:].copy(); bas[-f2:] *= np.linspace(1, 0, f2); son[:f2] *= np.linspace(0, 1, f2)
                a = np.concatenate([bas, son]); off -= fazla
                print(f'  {sid}: {t1 - t0:.2f} sn duraklama → {ops["durak"]:.2f} sn')
        hedef_db = db(sesli_rms(eski, thr0))
        if 'komsu' in ops:
            kom = [IDS[IDS.index(sid) - 1]] + ([IDS[IDS.index(sid) + 1]] if IDS.index(sid) + 1 < len(IDS) else [])
            hedef_db = np.mean([db(sesli_rms(a0[int(CUES[k]['s'] * SR):int(CUES[k]['e'] * SR)], thr0)) for k in kom]) + ops['komsu']
        g = 10 ** ((hedef_db - db(sesli_rms(a[int(on * SR):int(off * SR)], thr))) / 20)
        k0, k1 = klip_sinir((c['s'] + c['e']) / 2)
        i = IDS.index(sid); nxt = IDS[i + 1] if i + 1 < len(IDS) else None
        sonraki = klip_sinir(CUES[nxt]['s'])[0] if nxt else DUR
        onceki_son = klip_sinir(CUES[IDS[i - 1]]['e'])[1]
        bas_pay = min(c['s'] - k0, on - r[0] * .01)          # konuşmadan önceki sessizlik (eski klipteki kadar)
        kuyruk = min(k1 - c['e'], len(a) / SR - off, .45)     # konuşmadan sonraki kuyruk
        s_yeni = c['s']
        son = s_yeni + (off - on) + kuyruk
        if son > sonraki - .03:   # sığmıyor: önce kuyruğu kısalt, sonra öne kaydır (önceki sessizlikten pay al)
            kuyruk = max(.1, kuyruk - (son - sonraki + .03)); son = s_yeni + (off - on) + kuyruk
        if son > sonraki - .03:
            s_yeni -= son - sonraki + .03; son = sonraki - .03
            if s_yeni - bas_pay < onceki_son + .05: sys.exit(f'{sid}: sığmıyor (yer yok); metni kısalt ya da başka çekim seç')
        klip = a[int((on - bas_pay) * SR):int((off + kuyruk) * SR)] * g
        fl = int(.012 * SR); klip[:fl] *= np.linspace(0, 1, fl); klip[-fl:] *= np.linspace(1, 0, fl)
        a0[int(k0 * SR):int(k1 * SR)] = 0
        b = int((s_yeni - bas_pay) * SR); a0[b:b + len(klip)] = klip
        # kelime zamanları: sesli karelere harf uzunluğuyla
        rms, _ = zarf(a[int(on * SR):int(off * SR)] * g); v = np.where(rms > thr * g)[0]
        ws = words_of(SEG[sid]['tts']); ln = np.array([len(w) for w in ws], float); cs = np.concatenate([[0], np.cumsum(ln)]) / ln.sum()
        def zt(q): return s_yeni + v[min(len(v) - 1, int(q * len(v)))] * .01
        at = []
        for x in re.sub(r'\[[^\]]*\]', ' ', SEG[sid]['alt']).replace('…', ' ').split():
            if not norm1(x): continue
            n = next((vv for kk, vv in MERGE.get(sid, {}).items() if norm1(kk) == norm1(x)), 1); at += [x] + [''] * (n - 1)
        yeni = [{'id': sid, 'w': w, 'd': at[k] if k < len(at) else w, 's': round(zt(cs[k]), 3), 'e': round(min(zt(cs[k + 1]) + .01, s_yeni + off - on), 3)} for k, w in enumerate(ws)]
        yeni[0]['s'] = round(s_yeni, 3); yeni[-1]['e'] = round(s_yeni + off - on, 3)
        j = next(k for k, w in enumerate(WORDS) if w['id'] == sid)
        WORDS = WORDS[:j] + yeni + [w for w in WORDS[j:] if w['id'] != sid]
        CUES[sid] = {**c, 's': round(s_yeni, 3), 'e': round(s_yeni + off - on, 3)}
        print(f"{sid}={tk}: {c['s']:.2f}–{c['e']:.2f} → {CUES[sid]['s']:.2f}–{CUES[sid]['e']:.2f}, kazanç {db(g):+.1f} dB, sonraki klibe {sonraki - son:.2f} sn")
    with wave.open('vo/vo.wav', 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(a0, -1, 1) * 32767).astype(np.int16).tobytes())
    open('timeline.js', 'w').write('// tools/build_vo.py tarafından üretildi; ' + ', '.join(secim) + ' cümleleri tools/yama_vo.py ile yamandı\nwindow.CUES = ' + json.dumps(CUES) + ';\nwindow.WORDS = ' + json.dumps(WORDS, ensure_ascii=False) + ';\nwindow.DUR = ' + str(DUR) + ';\n')
    json.dump(secim, open('vo/yama/secim.json', 'w'), indent=1)

if __name__ == '__main__':
    if sys.argv[1] == 'analiz': analiz()
    else: uygula(dict(x.split('=') for x in sys.argv[2:]))
