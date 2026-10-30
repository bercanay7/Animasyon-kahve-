"""Seçilen seslendirme take'lerini senaryo cümlelerine böler, aralarına kurgu boşlukları koyarak
tek anlatım izi (vo.wav) ve zaman çizelgesi (timeline.js) üretir.
Kullanım: python3 tools/build_vo.py   (vo/secim.json: {bölüm: dosya})"""
import json, re, difflib, subprocess, numpy as np, sys
SR = 48000
d = json.load(open('senaryo.json'))
sel = json.load(open('vo/secim.json'))
plan = json.load(open('vo/plan.json'))  # boşluklar: {"once": sn (ilk segmentten önce), "gap": {id: sn sonra}, "secGap": sn}
MERGE = {k: v for k, v in json.load(open('tools/merge.json')).items() if not k.startswith('_')}

def load(path):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True).stdout
    return np.frombuffer(raw, np.float32).copy()

norm1 = lambda w: re.sub(r"[^\wçğıöşüâî]+", '', w.lower().replace('İ', 'i').replace('I', 'ı').replace("'", '').replace('’', '').replace('â', 'a').replace('î', 'i').replace('û', 'u'))
def words_of(text):
    return [w for w in (norm1(x) for x in re.sub(r'\[[^\]]*\]', ' ', text).replace('…', ' ').split()) if w]

secs = []
for s in d['segments']:
    if not secs or secs[-1][0] != s['bolum']: secs.append((s['bolum'], []))
    secs[-1][1].append(s)

out = []; t = plan.get('once', 1.0); cues = {}; allwords = []
out.append(np.zeros(int(t * SR), np.float32))
for si, (bolum, segs) in enumerate(secs):
    f = sel[bolum]
    a = load('vo/' + f)
    hw = []
    for w in json.load(open('vo/' + f.rsplit('.', 1)[0] + '.words.json')):
        # Whisper "Zeus" + "'un" diye böler: kesmeyle başlayan parçayı önceki kelimeye ekle
        if hw and w['w'][:1] in "'’": hw[-1] = {**hw[-1], 'w': hw[-1]['w'] + w['w'], 'e': w['e']}
        else: hw.append(w)
    hyp = [norm1(w['w']) for w in hw]
    ref, owner, disp = [], [], []
    for k, s in enumerate(segs):
        ws = words_of(s['tts']); ref += ws; owner += [k] * len(ws)
        # altyazı sözcükleri; tools/merge.json'daki çok kelimelik karşılıklar (ör. "1967'de" = beş kelime) açılır: ilk kelime sözcüğü taşır, kalanlar boş
        at = []
        for x in re.sub(r'\[[^\]]*\]', ' ', s['alt']).replace('…', ' ').split():
            if not norm1(x): continue
            n = next((v for k_, v in MERGE.get(s['id'], {}).items() if norm1(k_) == norm1(x)), 1); at += [x] + [''] * (n - 1)
        disp += at[:len(ws)] + [''] * max(0, len(ws) - len(at))
    sm = difflib.SequenceMatcher(None, ref, hyp, autojunk=False)
    m = [None] * len(ref)
    for blk in sm.get_matching_blocks():
        for i in range(blk.size): m[blk.a + i] = blk.b + i
    # eşleşmeyenleri komşulardan doldur
    st = [None] * len(ref); en = [None] * len(ref)
    for i, j in enumerate(m):
        if j is not None: st[i], en[i] = hw[j]['s'], hw[j]['e']
    for i in range(len(ref)):
        if st[i] is None:
            p = max([k for k in range(i) if st[k] is not None], default=None)
            n = min([k for k in range(i + 1, len(ref)) if st[k] is not None], default=None)
            if p is not None and n is not None:
                st[i] = en[p] + (st[n] - en[p]) * (i - p) / (n - p); en[i] = st[i] + .2
            elif p is not None: st[i] = en[p] + .05; en[i] = st[i] + .3
            else: st[i] = max(0, st[n] - .4); en[i] = st[i] + .3
    # RMS zarfı ile kesim noktaları
    hop = int(.01 * SR)
    rms = np.sqrt(np.convolve(a ** 2, np.ones(hop * 3) / (hop * 3), 'same'))[::hop]
    thr = max(1e-4, np.percentile(rms, 20) * 2.2)
    def cut_between(e0, s1):
        lo, hi = int(max(0, e0 - .12) / .01), int(min(len(a) / SR, s1 + .12) / .01)
        if hi <= lo: return (e0 + s1) / 2
        seg = rms[lo:hi] < thr
        best, bi, cur, ci = 0, None, 0, None
        for i, q in enumerate(seg):
            if q: cur += 1; ci = i if cur == 1 else ci
            else: cur = 0
            if cur > best: best, bi = cur, ci
        c = (e0 + s1) / 2 if bi is None else (lo + bi + best / 2) * .01
        # Whisper'ın iki kelime zamanı üst üste binince (e0 ≈ s1) pencerede sessizlik yoktur ve kesim bir sesin
        # ortasına düşer ("güvenmez" → "güvenme"). Bu durumda ileriye, ilk gerçek duraklamaya (≥ 120 ms) kes.
        # Zaman çizelgesi değişmez: kesimden sonraki her örnek aynı mutlak zamanda kalır (ses kurulu tur 1).
        if rms[min(len(rms) - 1, int(c / .01))] > thr * .5:
            lo2, hi2 = int(max(0, e0 - .05) / .01), int(min(len(a) / SR, e0 + 1.2) / .01)
            run = 0
            for i in range(lo2, hi2):
                run = run + 1 if rms[i] < thr else 0
                if run >= 12: return (i - run / 2) * .01
        return c
    bounds = []
    for k in range(len(segs)):
        idx = [i for i, o in enumerate(owner) if o == k]
        bounds.append((st[idx[0]], en[idx[-1]]))
    cuts = [max(0, bounds[0][0] - .25)]
    for k in range(len(segs) - 1): cuts.append(cut_between(bounds[k][1], bounds[k + 1][0]))
    # son kesim: son kelimeden sonraki ilk sessizlik + kuyruk
    endt = bounds[-1][1]; j = int(endt / .01)
    while j < len(rms) and rms[j] > thr: j += 1
    cuts.append(min(len(a) / SR, j * .01 + .25))
    for k, s in enumerate(segs):
        c0, c1 = cuts[k], cuts[k + 1]
        clip = a[int(c0 * SR):int(c1 * SR)].copy()
        fl = int(.012 * SR); clip[:fl] *= np.linspace(0, 1, fl); clip[-fl:] *= np.linspace(1, 0, fl)
        # cümle içi duraklama (plan 'ara': {"J04@köle": 0.8}): kelimeden sonraki sessizlikte bölüp araya sessizlik koyar; sonraki kelimeler kayar
        idx = [i for i, o in enumerate(owner) if o == k]
        shift = {i: 0.0 for i in idx}; pieces = []; last = 0
        for key, dur in plan.get('ara', {}).items():
            sid, w = key.split('@'); w, n = (w.split('#') + ['0'])[:2]
            if sid != s['id']: continue
            hits = [i for i in idx if ref[i].startswith(norm1(w))]
            if len(hits) <= int(n) or hits[int(n)] == idx[-1]: print('ara bulunamadı', key); continue
            i0 = hits[int(n)]; cp = int((cut_between(en[i0], st[i0 + 1]) - c0) * SR)
            pieces.append((cp, dur))
            for i in idx:
                if i > i0: shift[i] += dur
        if pieces:
            parts = []
            for cp, dur in sorted(pieces):
                seg_ = clip[last:cp].copy(); f2 = int(.01 * SR); seg_[-f2:] *= np.linspace(1, 0, f2)
                parts += [seg_, np.zeros(int(dur * SR), np.float32)]; last = cp
            tail = clip[last:].copy(); f2 = int(.01 * SR); tail[:f2] *= np.linspace(0, 1, f2); parts.append(tail)
            clip = np.concatenate(parts)
        cues[s['id']] = {'s': round(t + (bounds[k][0] - c0), 3), 'e': round(t + (bounds[k][1] - c0) + shift[idx[-1]], 3), 'sec': si}
        for i, o in enumerate(owner):
            if o == k: allwords.append({'id': s['id'], 'w': ref[i], 'd': disp[i] if i < len(disp) else ref[i], 's': round(t + st[i] - c0 + shift[i], 3), 'e': round(t + en[i] - c0 + shift[i], 3)})
        out.append(clip); t += len(clip) / SR
        g = plan['gap'].get(s['id'], plan.get('varsayilan', 0.35))
        if k == len(segs) - 1: g += plan.get('secGap', 1.5)
        out.append(np.zeros(int(g * SR), np.float32)); t += g
t += plan.get('sonra', 0)
out.append(np.zeros(int(plan.get('sonra', 0) * SR), np.float32))
vo = np.concatenate(out)
import wave
with wave.open('vo/vo.wav', 'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.clip(vo, -1, 1) * 32767).astype(np.int16).tobytes())
open('timeline.js', 'w').write('// tools/build_vo.py tarafından üretildi\nwindow.CUES = ' + json.dumps(cues) + ';\nwindow.WORDS = ' + json.dumps(allwords, ensure_ascii=False) + ';\nwindow.DUR = ' + str(round(t, 3)) + ';\n')
print('süre', round(t, 2), 'sn =', f'{int(t // 60)}:{t % 60:04.1f}')
