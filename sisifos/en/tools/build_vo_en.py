"""English dub track: splits the chosen takes (en/secim_en.json) into the 57 script segments using the
whisper word alignment, places every segment so its speech starts at the Turkish cue start, fits it
into the Turkish window (earlier start up to 0.35 s, then rubberband time compression up to 1.12x),
loudness-matches to vo/vo.wav and writes en/vo_en.wav + en/timeline_en.json + en/build_en.json.
Usage: python3 en/tools/build_vo_en.py"""
import json, os, sys, subprocess, difflib, tempfile
import numpy as np, soundfile as sf, pyloudnorm as pyln
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common_en import *

SR = 48000
GAP = 0.12            # min gap between English speech and the next cue start
EARLY = 0.35          # max earlier start
MAXF = 1.12           # max tempo factor
FADE = 0.040          # fade in / out at every cut
H04_END = 416.0
HOP = 0.01            # envelope hop
WORDS_TAG = os.environ.get('WORDS_TAG', 'mediumen')   # which transcript drives the alignment

cues, DUR = load_cues()
N = round(DUR * SR)
sel = json.load(open(os.environ.get('SECIM', os.path.join(EN, 'secim_en.json'))))
OUT = os.environ.get('OUT_DIR', EN)   # alternative output dir (take comparisons)
secs = sections()
ids = [s['id'] for s in load_script()]
assert ids == list(cues), 'script ids differ from Turkish cue ids'

def load(path):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-af', 'aresample=resampler=soxr:precision=28',
                          '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).astype(np.float64)

def envelope_db(a):
    h, w = int(HOP * SR), int(0.02 * SR)
    n = len(a) // h
    pad = np.concatenate([np.zeros(w // 2), a, np.zeros(w)])
    c = np.concatenate([[0], np.cumsum(pad ** 2)])
    e = np.array([(c[i * h + w] - c[i * h]) / w for i in range(n)])
    return 10 * np.log10(e + 1e-12)          # frame i ~ centred at i*HOP

def stretch(clip, f):
    """time-compress by factor f (>1 = shorter) with rubberband (formant preserved, high quality)"""
    with tempfile.TemporaryDirectory() as td:
        pi, po = os.path.join(td, 'i.wav'), os.path.join(td, 'o.wav')
        sf.write(pi, clip, SR, subtype='FLOAT')
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', pi, '-af',
                        f'rubberband=tempo={f:.5f}:transients=mixed:detector=soft:phase=laminar:window=standard:'
                        f'smoothing=on:formant=preserved:pitchq=quality', '-c:a', 'pcm_f32le', po], check=True)
        out, _ = sf.read(po)
    return out

def align(segs, hw):
    """script tokens -> (s, e) in take time.  Returns per-segment token lists [(display, s, e)]."""
    toks = []   # (seg k, display token, [norm words])
    for k, s in enumerate(segs):
        for d in display_words(s['tts']):
            nw = norm_words(d)
            if nw: toks.append((k, d, nw))
    ref, rown = [], []
    for ti, (_, _, nw) in enumerate(toks):
        ref += nw; rown += [ti] * len(nw)
    hyp, hs, he = [], [], []
    for w in hw:
        nw = norm_words(w['w'])
        for j, x in enumerate(nw):  # spread multi-word tokens (e.g. "1942") over the word's span
            L = (w['e'] - w['s']) / len(nw)
            hyp.append(x); hs.append(w['s'] + j * L); he.append(w['s'] + (j + 1) * L)
    st, en = [None] * len(ref), [None] * len(ref)
    sm = difflib.SequenceMatcher(None, ref, hyp, autojunk=False)
    for op, a0, a1, b0, b1 in sm.get_opcodes():
        if op == 'equal' or (op == 'replace' and a1 - a0 == b1 - b0):
            for i in range(a1 - a0): st[a0 + i], en[a0 + i] = hs[b0 + i], he[b0 + i]
        elif op == 'replace':  # spread the hyp span over the ref words by character length
            T0, T1 = hs[b0], he[b1 - 1]
            L = np.cumsum([0] + [len(ref[i]) + 1 for i in range(a0, a1)]); L = L / L[-1]
            for i in range(a1 - a0): st[a0 + i], en[a0 + i] = T0 + (T1 - T0) * L[i], T0 + (T1 - T0) * L[i + 1]
    for i in range(len(ref)):   # deletions: interpolate between neighbours
        if st[i] is None:
            p = max([k for k in range(i) if st[k] is not None], default=None)
            n = min([k for k in range(i + 1, len(ref)) if st[k] is not None], default=None)
            if p is not None and n is not None:
                st[i] = en[p] + (st[n] - en[p]) * (i - p) / (n - p + 1); en[i] = st[i] + max(.05, (st[n] - en[p]) / (n - p + 1))
            elif p is not None: st[i] = en[p] + .05; en[i] = st[i] + .3
            else: st[i] = max(0, st[n] - .35); en[i] = st[i] + .3
    out = [[] for _ in segs]
    for ti, (k, d, nw) in enumerate(toks):
        idx = [i for i, o in enumerate(rown) if o == ti]
        out[k].append([d, st[idx[0]], en[idx[-1]]])
    nmatch = sum(b.size for b in sm.get_matching_blocks())
    return out, nmatch, len(ref)

def refine(db, t_s, t_e, lw_s, lo, hi):
    """energy-based speech onset/end around whisper times. lo/hi: hard limits (take seconds)"""
    nf = len(db)
    fi = lambda t: int(np.clip(round(t / HOP), 0, nf - 1))
    # onset: first run above -42 dB (>= 40 ms) in [t_s-0.3, t_s+0.4] whose peak > -32 dB; then soft-attack walk-back
    a, b = fi(max(lo, t_s - .30)), fi(min(hi, t_s + .40))
    on = None; i = a
    while i <= b:
        if db[i] > -42:
            j = i
            while j < nf and db[j] > -42: j += 1
            if j - i >= 4 and db[i:j].max() > -32: on = i; break
            i = j
        i += 1
    if on is None: on = fi(t_s)
    k = 0
    while on > fi(lo) and db[on - 1] > -55 and k < 6: on -= 1; k += 1
    # end: from the last word (energy > -42 dB), walk forward to the first >=100 ms run below -50 dB
    f0 = fi(max(lw_s, t_e - .35))
    while f0 < nf - 1 and db[f0] <= -42 and f0 < fi(t_e + .3): f0 += 1
    j = f0; run = 0
    while j < min(nf, fi(hi)):
        run = run + 1 if db[j] < -50 else 0
        if run >= 10: break
        j += 1
    end = j - run + 1 if run else j
    return on * HOP, end * HOP

def quiet_cut(db, t0, t1):
    """quietest point between speech end t0 and next onset t1 (40 ms smoothed); slight bias towards the
    earlier side so that a breath before the next sentence stays with the next sentence"""
    nf = len(db)
    a, b = int(round(t0 / HOP)) + 4, int(round(t1 / HOP)) - 4
    if b <= a: return (t0 + t1) / 2
    sm = np.convolve(db, np.ones(4) / 4, 'same')
    seg = sm[a:b + 1]
    pos = np.linspace(0, 1, len(seg))
    cost = seg + 4.0 * pos                # dB + small position penalty
    return (a + int(np.argmin(cost))) * HOP

# ---------------------------------------------------------------- split takes
pieces = {}     # id -> dict(clip, on, end (clip-relative seconds), words [(d, s, e)] clip-relative, take)
take_info = {}
for k, L in enumerate(LET):
    f = sel[L]['take']
    a = load(os.path.join(EN, f))
    db = envelope_db(a)
    hw = json.load(open(os.path.join(EN, 'words', f.rsplit('.', 1)[0] + f'.{WORDS_TAG}.words.json')))
    segs = secs[L]
    tw, nm, nr = align(segs, hw)
    take_info[L] = {'take': f, 'matched_words': nm, 'ref_words': nr}
    T = len(a) / SR
    bounds = []
    for i in range(len(segs)):
        lo = bounds[-1][1] + .05 if bounds else 0
        hi = tw[i + 1][0][1] - .05 if i + 1 < len(segs) else T
        on, end = refine(db, tw[i][0][1], tw[i][-1][2], tw[i][-1][1], lo, hi)
        bounds.append((on, end))
    cuts = [max(0, bounds[0][0] - .30)]
    for i in range(len(segs) - 1):
        cuts.append(quiet_cut(db, bounds[i][1], bounds[i + 1][0]))
    # last cut: quietest point within 0.5 s after speech end (or end of file)
    e = bounds[-1][1]
    cuts.append(min(T, quiet_cut(db, e, min(T, e + .6)) if e + .2 < T else T))
    for i, s in enumerate(segs):
        c0, c1 = cuts[i], cuts[i + 1]
        clip = a[int(round(c0 * SR)):int(round(c1 * SR))].copy()
        on, end = bounds[i][0] - c0, bounds[i][1] - c0
        words = [[d, max(0.0, ws - c0), max(0.0, we - c0)] for d, ws, we in tw[i]]
        # clamp word times into the energy-refined speech span
        words[0][1] = on
        words[-1][2] = max(words[-1][2], end) if words[-1][2] < end else end
        for w in words:
            w[1] = min(max(w[1], on), end); w[2] = min(max(w[2], w[1] + .02), end)
        pieces[s['id']] = {'clip': clip, 'on': on, 'end': end, 'words': words, 'take': f,
                           'cut': (round(c0, 3), round(c1, 3)), 'gap_before': round(bounds[i][0] - (bounds[i - 1][1] if i else 0), 3),
                           'd_on': round(bounds[i][0] - tw[i][0][1], 3), 'd_end': round(bounds[i][1] - tw[i][-1][2], 3)}

# ---------------------------------------------------------------- place
fade_n = int(FADE * SR)
vo = np.zeros(N)
placed = {}
rows = []
prev_end = -1.0     # film time of previous English speech end
prev_clip_end = 0.0  # film sample index of previous clip end
issues = []
for n, cid in enumerate(ids):
    p = pieces[cid]
    start_tr = cues[cid]['s']
    limit = (cues[ids[n + 1]]['s'] - GAP) if n + 1 < len(ids) else H04_END
    dur = p['end'] - p['on']
    shift, f = 0.0, 1.0
    if start_tr + dur > limit:
        room = max(0.0, start_tr - (prev_end + GAP))
        shift = min(EARLY, room, start_tr + dur - limit)
        shift = round(np.ceil(shift * 1000) / 1000, 3)
        avail = limit - (start_tr - shift)
        if dur > avail:
            f = min(MAXF, dur / avail * 1.003)
            if dur / f > avail + 1e-6:
                issues.append(f'{cid}: still {dur / f - avail:.3f} s too long after {MAXF}x and {shift:.2f} s early start')
    clip, on, end, words = p['clip'], p['on'], p['end'], p['words']
    if f > 1.0:
        out = stretch(clip, f)
        r = len(out) / len(clip)          # actual length ratio
        clip, on, end = out, on * r, end * r
        words = [[d, s * r, e * r] for d, s, e in words]
    s_film = start_tr - shift
    c_start = s_film - on                 # film time where the clip begins
    i0 = int(round(c_start * SR))
    clip = clip.copy()
    # never overlap with the previous clip: trim this clip's lead (keep >= 20 ms before onset)
    if i0 < prev_clip_end:
        cut = prev_clip_end - i0
        maxcut = int((on - .02) * SR)
        if cut > maxcut:
            issues.append(f'{cid}: lead overlap with previous clip could not be fully trimmed')
            cut = maxcut
        clip = clip[cut:]; i0 += cut
    # trim tail so that it never runs into the next segment's lead (resolved when the next one is placed:
    # we cut this clip's tail at the next onset - 0.06 s or at its own end, whichever comes first)
    if n + 1 < len(ids):
        nxt_on_film = cues[ids[n + 1]]['s'] - EARLY   # conservative: next onset can move up to EARLY earlier
        nxt_lead = pieces[ids[n + 1]]['on']
        boundary = max(s_film + (end - on) + .06, nxt_on_film - nxt_lead)
        boundary = min(boundary, cues[ids[n + 1]]['s'] - .03)
        maxlen = int(round((boundary - c_start) * SR)) - (i0 - int(round(c_start * SR)))
        if len(clip) > maxlen: clip = clip[:max(maxlen, 0)]
    fi_n = min(fade_n, len(clip) // 4)
    clip[:fi_n] *= np.linspace(0, 1, fi_n) ** 2 if False else np.linspace(0, 1, fi_n)
    clip[-fade_n:] *= np.linspace(1, 0, min(fade_n, len(clip)))
    i1 = i0 + len(clip)
    assert i0 >= 0 and i1 <= N, cid
    assert i0 >= prev_clip_end, (cid, i0, prev_clip_end)
    vo[i0:i1] += clip
    prev_clip_end = i1
    e_film = s_film + (end - on)
    placed[cid] = {'s': round(s_film, 3), 'e': round(e_film, 3)}
    for d, ws, we in words:
        placed.setdefault('_w', []).append({'id': cid, 'w': d, 's': round(c_start + ws, 3), 'e': round(c_start + we, 3)})
    rows.append({'id': cid, 'en_dur': round(dur, 3), 'tr_s': start_tr, 'limit': round(limit, 3), 'win': round(limit - start_tr, 3),
                 'shift': shift, 'tempo': round(f, 4), 'en_s': round(s_film, 3), 'en_e': round(e_film, 3),
                 'slack': round(limit - e_film, 3), 'take': p['take'], 'cut': p['cut'], 'lead': round(on, 3), 'clip_len': round(len(clip) / SR, 3),
                 'd_on': p['d_on'], 'd_end': p['d_end']})
    assert e_film <= limit + 1e-3 or any(x.startswith(cid) for x in issues), (cid, e_film, limit)
    prev_end = e_film

words = placed.pop('_w')
# ---------------------------------------------------------------- loudness
ref, rsr = sf.read(os.path.join(ROOT, 'vo', 'vo.wav'))
meter = pyln.Meter(SR)
target = pyln.Meter(rsr).integrated_loudness(ref)
L0 = meter.integrated_loudness(vo)
vo *= 10 ** ((target - L0) / 20)
peak_db = 20 * np.log10(np.abs(vo).max())
limited = False
gr = np.ones(N)
for it in range(3):   # transparent peak limiter (10 ms look-ahead/hold, smooth gain), only if needed
    if 20 * np.log10(np.abs(vo).max()) <= -1.2: break
    limited = True
    thr = 10 ** (-1.25 / 20)
    g = np.minimum(1, thr / np.maximum(np.abs(vo), 1e-9))
    w = int(.010 * SR)
    from scipy.ndimage import minimum_filter1d
    g = minimum_filter1d(g, 2 * w + 1)
    hw_ = np.hanning(2 * w + 1); g = np.convolve(g, hw_ / hw_.sum(), 'same')
    g = np.minimum(g, 1)
    vo *= g; gr *= g
    vo *= 10 ** ((target - meter.integrated_loudness(vo)) / 20)
for r in rows:
    a_, b_ = int((r['en_s'] - .3) * SR), int((r['en_e'] + .3) * SR)
    r['limiter_db'] = round(float(20 * np.log10(gr[a_:b_].min())), 2)
L1 = meter.integrated_loudness(vo)
pk = 20 * np.log10(np.abs(vo).max())
# true peak (4x oversampled)
import scipy.signal as ss
tp = 20 * np.log10(np.abs(ss.resample_poly(vo, 4, 1)).max())
assert len(vo) == N
sf.write(os.path.join(OUT, 'vo_en.wav'), np.clip(vo, -1, 1), SR, subtype='PCM_16')

json.dump({'dur': DUR, 'cues': placed, 'words': words}, open(os.path.join(OUT, 'timeline_en.json'), 'w'), ensure_ascii=False, indent=0)
json.dump({'rows': rows, 'issues': issues, 'takes': take_info, 'lufs_target': round(target, 2), 'lufs': round(L1, 2),
           'gain_db': round(target - L0, 2), 'peak_dbfs': round(pk, 2), 'true_peak_dbtp': round(tp, 2), 'limited': limited,
           'samples': len(vo), 'sr': SR, 'words_tag': WORDS_TAG},
          open(os.path.join(OUT if OUT != EN else os.path.join(EN, 'tools'), 'build_en.json'), 'w'), ensure_ascii=False, indent=1)
for r in rows:
    print(f"{r['id']} dur {r['en_dur']:6.2f} win {r['win']:6.2f} shift {r['shift']:.2f} tempo {r['tempo']:.3f} slack {r['slack']:6.2f} lead {r['lead']:.2f} dOn {r['d_on']:+.2f} dEnd {r['d_end']:+.2f}")
print('issues:', issues)
print(f'gain {target - L0:+.2f} dB, peak before limiter {peak_db:.2f} dBFS')
print(f'LUFS {L1:.2f} (target {target:.2f})  peak {pk:.2f} dBFS  TP {tp:.2f} dBTP  samples {len(vo)}  limited {limited}')
