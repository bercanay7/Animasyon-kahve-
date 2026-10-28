"""Seslendirme çekimlerini cümlelere böler, cümle başına seçilen çekimden alır, aralarına kurgu boşlukları koyar;
tek anlatım izi (vo.wav) ve zaman çizelgesi (timeline.js) üretir.
Kullanım: python3 tools/build_vo.py
  vo/secim.json        {bölüm: dosya}  bölümün varsayılan çekimi
  vo/secim_cumle.json  {cümle_id: dosya} (isteğe bağlı) cümle başına çekim (anlatım kurulu); bölüm dışı dosyalar da olabilir
  vo/takes.json        {dosya: [cümle_id...]} (isteğe bağlı) bölüm çekimi olmayan dosyaların içerdiği cümleler (ör. yeniden okumalar)
  vo/plan.json         once, secGap, sonra, gap{id: sn}, ic{id: [[sözcük, sn], ...]} (cümle içi durak)
Kesim: iki cümle arası en uzun sessizliğin ortası; kesim noktası sessiz değilse arama penceresi genişler (kopuk hece kalmaz).
CUES başlangıç/bitişi enerjiden alınır; cümleler arası ses seviyesi eşitlenir."""
import json, re, difflib, subprocess, numpy as np, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dispmap import disp_map
SR = 48000
d = json.load(open('senaryo.json'))
sel = json.load(open('vo/secim.json'))
sel_s = json.load(open('vo/secim_cumle.json')) if os.path.exists('vo/secim_cumle.json') else {}
takes = json.load(open('vo/takes.json')) if os.path.exists('vo/takes.json') else {}
plan = json.load(open('vo/plan.json'))
SEG = {s['id']: s for s in d['segments']}

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
SEC_OF = {s['id']: b for b, ss in secs for s in ss}

CACHE = {}
def analyse(f, ids):
    """bir çekim dosyası: hizalama, kelime zamanları, cümle kesimleri. ids: dosyadaki cümleler (sırasıyla)"""
    if f in CACHE: return CACHE[f]
    a = load('vo/' + f)
    hw = json.load(open('vo/' + f.rsplit('.', 1)[0] + '.words.json'))
    hyp = [norm1(w['w']) for w in hw]
    ref, owner = [], []
    for k, sid in enumerate(ids):
        ws = words_of(SEG[sid]['tts']); ref += ws; owner += [k] * len(ws)
    sm = difflib.SequenceMatcher(None, ref, hyp, autojunk=False)
    m = [None] * len(ref)
    for blk in sm.get_matching_blocks():
        for i in range(blk.size): m[blk.a + i] = blk.b + i
    st = [None] * len(ref); en = [None] * len(ref)
    for i, j in enumerate(m):
        if j is not None: st[i], en[i] = hw[j]['s'], hw[j]['e']
    for i in range(len(ref)):
        if st[i] is None:
            p = max([k for k in range(i) if st[k] is not None], default=None)
            n = min([k for k in range(i + 1, len(ref)) if st[k] is not None], default=None)
            if p is not None and n is not None: st[i] = en[p] + (st[n] - en[p]) * (i - p) / (n - p); en[i] = st[i] + .2
            elif p is not None: st[i] = en[p] + .05; en[i] = st[i] + .3
            else: st[i] = max(0, st[n] - .4); en[i] = st[i] + .3
    hop = int(.01 * SR)
    rms = np.sqrt(np.convolve(a ** 2, np.ones(hop * 3) / (hop * 3), 'same'))[::hop]
    thr = max(1e-4, np.percentile(rms, 20) * 2.2)
    def longest_quiet(lo, hi):
        lo, hi = max(0, lo), min(len(rms), hi)
        best, bi, cur, ci = 0, None, 0, None
        for i in range(lo, hi):
            if rms[i] < thr: cur += 1; ci = i if cur == 1 else ci
            else: cur = 0
            if cur > best: best, bi = cur, ci
        return None if bi is None else (bi + best / 2) * .01
    def cut_between(e0, s1):
        c = longest_quiet(int((e0 - .12) / .01), int((s1 + .12) / .01))
        ci = None if c is None else int(c / .01)
        # anlatım kurulu: kesim noktası sessiz değilse ya da ±80 ms içinde ses varsa pencere genişler
        if c is None or rms[ci] >= thr * .5 or not (rms[max(0, ci - 8):ci + 8] < thr).all():
            c2 = longest_quiet(int((e0 - .3) / .01), int((s1 + .8) / .01))
            if c2 is not None: c = c2
        return c if c is not None else (e0 + s1) / 2
    bounds = []
    for k in range(len(ids)):
        idx = [i for i, o in enumerate(owner) if o == k]
        bounds.append((st[idx[0]], en[idx[-1]]))
    cuts = [max(0, bounds[0][0] - .25)]
    for k in range(len(ids) - 1): cuts.append(cut_between(bounds[k][1], bounds[k + 1][0]))
    endt = bounds[-1][1]; j = int(endt / .01)
    while j < len(rms) and rms[j] > thr: j += 1
    cuts.append(min(len(a) / SR, j * .01 + .25))
    CACHE[f] = dict(a=a, ref=ref, owner=owner, st=st, en=en, cuts=cuts, rms=rms, thr=thr, ids=ids)
    return CACHE[f]

def file_for(sid):
    return sel_s.get(sid) or sel[SEC_OF[sid]]
def ids_in(f):
    if f in takes: return takes[f]
    b = [b for b, v in sel.items() if v == f] or [SEC_OF[sid] for sid in sel_s if sel_s[sid] == f]
    # bölüm çekimi (sN_a/sN_b): o bölümün bütün cümleleri
    m = re.match(r's(\d+)_[ab]\.', f)
    if m: return [s['id'] for s in secs[int(m.group(1))][1]]
    return [s['id'] for s in secs[[x[0] for x in secs].index(b[0])][1]]

# 1) her cümlenin klibi, kelimeleri, enerji sınırları
clips = {}
for bolum, segs in secs:
    for s in segs:
        sid = s['id']; f = file_for(sid); A = analyse(f, ids_in(f)); k = A['ids'].index(sid)
        c0, c1 = A['cuts'][k], A['cuts'][k + 1]
        clip = A['a'][int(c0 * SR):int(c1 * SR)].copy()
        idx = [i for i, o in enumerate(A['owner']) if o == k]
        ws = [dict(w=A['ref'][i], s=A['st'][i] - c0, e=A['en'][i] - c0) for i in idx]
        disp = disp_map(s['alt'], [w['w'] for w in ws])
        for w, dd in zip(ws, disp): w['d'] = dd
        # cümle içi durak (plan.ic): sözcükten sonraki sessizliğin ortasına
        for word, dur in plan.get('ic', {}).get(sid, []):
            nw = norm1(word); hit = [i for i, w in enumerate(ws) if w['w'].startswith(nw)]
            if not hit or hit[0] + 1 >= len(ws): print('UYARI ic bulunamadı', sid, word); continue
            i = hit[0]; e0, s1 = ws[i]['e'], ws[i + 1]['s']
            r = A['rms'][int((c0 + e0) / .01):int((c0 + s1) / .01) + 1]
            q = [n for n, v in enumerate(r) if v < A['thr']]
            at = (e0 + (q[len(q) // 2] if q else (s1 - e0) / 2 / .01) * .01) if q else (e0 + s1) / 2
            p = int(at * SR); clip = np.concatenate([clip[:p], np.zeros(int(dur * SR), np.float32), clip[p:]])
            for w in ws[i + 1:]: w['s'] += dur; w['e'] += dur
        fl = int(.012 * SR); clip[:fl] *= np.linspace(0, 1, fl); clip[-fl:] *= np.linspace(1, 0, fl)
        # enerji sınırları (CUES): ilk ve son eşik üstü kare
        hop = int(.01 * SR); rr = np.sqrt(np.convolve(clip ** 2, np.ones(hop * 3) / (hop * 3), 'same'))[::hop]
        on = np.nonzero(rr > A['thr'])[0]
        es, ee = (on[0] * .01, (on[-1] + 1) * .01) if len(on) else (ws[0]['s'], ws[-1]['e'])
        act = clip[np.repeat(rr > A['thr'], hop)[:len(clip)]] if len(on) else clip
        clips[sid] = dict(clip=clip, ws=ws, s=min(es, ws[0]['s']), e=max(ee, ws[-1]['e'] - .05) if ee < ws[-1]['e'] - .3 else ee, f=f, rms=float(np.sqrt(np.mean(act ** 2)) + 1e-9))
# 2) ses seviyesi eşitleme: etkin RMS medyana (±%40 sınırlı); yalnız seçimi bölüm çekimi olmayan ya da farklı çekim olan cümlelerde belirgin fark olur
med = float(np.median([c['rms'] for c in clips.values()]))
for sid, c in clips.items():
    g = float(np.clip(med / c['rms'], .71, 1.41)) if (c['f'] != sel[SEC_OF[sid]] or sid in sel_s) else 1.0
    c['clip'] = c['clip'] * g
# 3) birleştir
out = []; t = plan.get('once', 1.0); cues = {}; allwords = []
out.append(np.zeros(int(t * SR), np.float32))
for si, (bolum, segs) in enumerate(secs):
    for k, s in enumerate(segs):
        c = clips[s['id']]
        cues[s['id']] = {'s': round(t + c['s'], 3), 'e': round(t + c['e'], 3), 'sec': si}
        for w in c['ws']: allwords.append({'id': s['id'], 'w': w['w'], 'd': w['d'], 's': round(t + w['s'], 3), 'e': round(t + w['e'], 3)})
        out.append(c['clip'].astype(np.float32)); t += len(c['clip']) / SR
        g = plan['gap'].get(s['id'], 0)
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
for sid in sel_s: print('  ', sid, '←', sel_s[sid])
import fix_disp  # noqa: E402  görünen sözcük bitişleri (de) timeline.js'e yazılır
