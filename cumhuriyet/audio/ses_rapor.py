#!/usr/bin/env python3
"""Ses/miks kurulu için görsel kanıt ve ölçümler (dinlemeden değerlendirilebilsin diye).

    python3 tools/mix.py --stems      (önce: audio/mix.wav + audio/stems/{vo,music}.wav)
    python3 audio/ses_rapor.py        -> board/ses/*.png + board/ses/olcumler.txt

seviye.png              0..DUR kısa süreli ses yüksekliği (3 sn, LUFS): anlatım, müzik (miksteki seviyesiyle), miks;
                        bölümler, cümle başları ve audio/cues.md'deki vuruş anları işaretli
konusma_marji.png       her cümlede anlatımın müziğin üstünde kaldığı pay: konuşma bandı (500 Hz-4 kHz) ve LUFS
spektrogram_muzik.png   audio/music.wav tamamı (log frekans 30 Hz-16 kHz), bölüm şeridiyle
spektrogram_final.png   miks, 300 sn'den sona: G01 nefes + doruk, G02 bando, G06 ve bitiş ekranı marşı
"""
import json
import re
from pathlib import Path

import numpy as np
import soundfile as sf
from PIL import Image, ImageDraw, ImageFont
from scipy import signal

HERE = Path(__file__).resolve().parent
FILM = HERE.parent
OUT = FILM / 'board' / 'ses'
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'


def font(size):
    try:
        return ImageFont.truetype(FONT, size)
    except OSError:
        return ImageFont.load_default()


def timeline():
    txt = (FILM / 'timeline.js').read_text(encoding='utf-8')
    dec = json.JSONDecoder()
    grab = lambda n: dec.raw_decode(txt, re.search(r'window\.' + n + r'\s*=\s*', txt).end())[0]
    return float(grab('DUR')), {k: (v['s'], v['e']) for k, v in grab('CUES').items()}


DUR, CUES = timeline()
ORDER = sorted(CUES, key=lambda c: CUES[c][0])
try:
    BOLUM = {s['id']: s['bolum'] for s in json.loads((FILM / 'senaryo.json').read_text(encoding='utf-8'))['segments']}
except (OSError, ValueError, KeyError):
    BOLUM = {}
SECTIONS = []
for c in ORDER:
    if not SECTIONS or SECTIONS[-1][0] != c[0]:
        SECTIONS.append([c[0], BOLUM.get(c, c[0]), CUES[c][0], CUES[c][1]])
    SECTIONS[-1][3] = CUES[c][1]
for i, s in enumerate(SECTIONS):                     # a section lasts until the next one starts
    s[3] = SECTIONS[i + 1][2] if i + 1 < len(SECTIONS) else DUR
SECTIONS[0][2] = 0.0


def hits_from_cues_md():
    p = HERE / 'cues.md'
    if not p.exists():
        return []
    return [(float(m[1]), m[2]) for m in re.finditer(r'^- \d+:[\d.]+ \(([\d.]+)\): (.*)$', p.read_text('utf-8'), re.M)]


# ------------------------------------------------------------------------- measurement
KW = [([1.53512485958697, -2.69169618940638, 1.19839281085285], [1.0, -1.69065929318241, 0.73248077421585]),
      ([1.0, -2.0, 1.0], [1.0, -1.99004745483398, 0.99007225036621])]   # ITU-R BS.1770 K-weighting at 48 kHz


def kpower(x):
    """K-weighted power summed over channels (per sample)."""
    x = x if x.ndim == 2 else x[:, None]
    for b, a in KW:
        x = signal.lfilter(b, a, x, axis=0)
    return (x ** 2).sum(1)


def short_term(p, sr, win=3.0, hop=0.5):
    c = np.concatenate([[0.0], np.cumsum(p)])
    w, h = int(win * sr), int(hop * sr)
    starts = np.arange(0, len(p) - w, h)
    ms = (c[starts + w] - c[starts]) / w
    return starts / sr + win / 2, -0.691 + 10 * np.log10(ms + 1e-12)


def integrated(p, sr):
    """BS.1770 integrated loudness (absolute -70 and relative -10 LU gates, 400 ms blocks, 75 % overlap)."""
    c = np.concatenate([[0.0], np.cumsum(p)])
    w, h = int(0.4 * sr), int(0.1 * sr)
    st = np.arange(0, len(p) - w, h)
    z = (c[st + w] - c[st]) / w
    l = -0.691 + 10 * np.log10(z + 1e-15)
    z = z[l > -70]
    rel = -0.691 + 10 * np.log10(z.mean()) - 10
    z = z[-0.691 + 10 * np.log10(z) > rel]
    return -0.691 + 10 * np.log10(z.mean())


def band_power(x, sr, lo=500, hi=4000):
    m = x.mean(1) if x.ndim == 2 else x
    return signal.sosfilt(signal.butter(4, [lo, hi], 'bandpass', fs=sr, output='sos'), m) ** 2


def true_peak(x):
    return 20 * np.log10(np.abs(signal.resample_poly(x, 4, 1, axis=0)).max() + 1e-12)


# ------------------------------------------------------------------------- drawing helpers
PAL = [(0, 0, 4), (40, 11, 84), (101, 21, 110), (159, 42, 99), (212, 72, 66), (245, 125, 21), (250, 193, 39),
       (252, 255, 164)]


def cmap(v):
    v = np.clip(v, 0, 1) * (len(PAL) - 1)
    i = np.minimum(v.astype(int), len(PAL) - 2)
    f = (v - i)[..., None]
    p = np.array(PAL, float)
    return (p[i] * (1 - f) + p[i + 1] * f).astype(np.uint8)


SEC_COL = [(238, 228, 205), (220, 207, 178)]


def spectrogram_png(x, sr, t0, t1, path, title, marks=(), width=2400, height=520, fmin=30, fmax=16000):
    m = x.mean(1) if x.ndim == 2 else x
    seg = m[int(t0 * sr):int(t1 * sr)]
    nfft = 4096
    hop = max(int(len(seg) / width), 256)
    f, tt, Z = signal.stft(seg, sr, nperseg=nfft, noverlap=nfft - hop, boundary=None, padded=False)
    S = 20 * np.log10(np.abs(Z) + 1e-9)
    ylog = np.geomspace(fmin, fmax, height)[::-1]
    img = np.empty((height, S.shape[1]))
    for j in range(S.shape[1]):
        img[:, j] = np.interp(ylog, f, S[:, j])
    top = np.percentile(img, 99.7)
    rgb = cmap((img - (top - 90)) / 90)
    im = Image.fromarray(rgb).resize((width, height), Image.BILINEAR)
    L, T, B = 70, 50, 70
    can = Image.new('RGB', (width + L + 20, height + T + B + 30), (250, 247, 240))
    can.paste(im, (L, T))
    d = ImageDraw.Draw(can)
    d.text((L, 12), title, fill=(30, 25, 20), font=font(20))
    X = lambda t: L + (t - t0) / (t1 - t0) * width
    for fr in (50, 100, 200, 500, 1000, 2000, 5000, 10000):
        y = T + (np.log(fmax) - np.log(fr)) / (np.log(fmax) - np.log(fmin)) * height
        d.line([(L - 6, y), (L, y)], fill=(30, 25, 20))
        d.text((4, y - 7), f'{fr if fr < 1000 else str(fr // 1000) + "k"} Hz', fill=(30, 25, 20), font=font(12))
    for s in SECTIONS:
        if s[3] <= t0 or s[2] >= t1:
            continue
        a, b = max(s[2], t0), min(s[3], t1)
        d.line([(X(a), T), (X(a), T + height)], fill=(255, 255, 255), width=1)
        d.text((X(a) + 4, T + height + 6), s[1], fill=(30, 25, 20), font=font(14))
    k = 0
    for t, lab in marks:
        if t0 <= t <= t1:
            dy = 14 * (k % 3)
            d.line([(X(t), T + height), (X(t), T + height + 26 + dy)], fill=(179, 51, 43), width=2)
            d.text((X(t) + 3, T + height + 24 + dy), lab, fill=(179, 51, 43), font=font(12))
            k += 1
    step = 30 if t1 - t0 > 120 else 5
    for t in np.arange(np.ceil(t0 / step) * step, t1, step):
        d.text((X(t) - 12, T - 18), f'{int(t // 60)}:{int(t % 60):02d}', fill=(90, 80, 70), font=font(12))
    can.save(path)


def level_png(tv, lv, tm, lm, tx, lx, path, marks, width=2400, height=760):
    L, R, T, B = 70, 20, 90, 60
    can = Image.new('RGB', (width + L + R, height + T + B), (250, 247, 240))
    d = ImageDraw.Draw(can)
    lo, hi = -60.0, -5.0
    X = lambda t: L + t / DUR * width
    Y = lambda v: T + (hi - np.clip(v, lo, hi)) / (hi - lo) * height
    for i, s in enumerate(SECTIONS):
        d.rectangle([X(s[2]), T, X(s[3]), T + height], fill=SEC_COL[i % 2])
        d.text((X(s[2]) + 5, T + 4), s[1], fill=(60, 50, 40), font=font(15))
    for v in (-10, -14, -21, -30, -40, -50):
        d.line([(L, Y(v)), (L + width, Y(v))], fill=(150, 140, 125) if v in (-14, -21) else (200, 190, 175), width=1)
        d.text((8, Y(v) - 8), f'{v} LUFS', fill=(60, 50, 40), font=font(12))
    for c in ORDER:
        d.line([(X(CUES[c][0]), T + height - 14), (X(CUES[c][0]), T + height)], fill=(90, 80, 70))
        d.text((X(CUES[c][0]) + 2, T + height - 28), c, fill=(90, 80, 70), font=font(10))
    for t, lab in marks:
        d.line([(X(t), T - 6), (X(t), T + height)], fill=(179, 51, 43), width=1)
    for k, (t, lab) in enumerate(marks):
        d.text((X(t) + 2, T - 22 - 16 * (k % 3)), lab[:38], fill=(179, 51, 43), font=font(11))

    def line(t, v, col, w):
        d.line([(X(a), Y(b)) for a, b in zip(t, v)], fill=col, width=w)
    line(tv, lv, (130, 130, 130), 2)
    line(tm, lm, (230, 120, 20), 3)
    line(tx, lx, (33, 29, 27), 1)
    d.text((L, 8), 'Kısa süreli ses yüksekliği (3 sn, LUFS) - gri: anlatım  turuncu: müzik (miksteki seviyesiyle)  '
                   'siyah: miks.   Çizgiler: -14 hedef, -21 müzik entegre', fill=(30, 25, 20), font=font(18))
    for t in range(0, int(DUR) + 1, 30):
        d.text((X(t) - 12, T + height + 8), f'{t // 60}:{t % 60:02d}', fill=(60, 50, 40), font=font(13))
    can.save(path)


def margin_png(rows, path, width=2400, height=560):
    L, T, B = 70, 70, 70
    can = Image.new('RGB', (width + L + 20, height + T + B), (250, 247, 240))
    d = ImageDraw.Draw(can)
    lo, hi = 0.0, 35.0
    Y = lambda v: T + (hi - np.clip(v, lo, hi)) / (hi - lo) * height
    n = len(rows)
    bw = width / n
    for v in (5, 10, 15, 20, 25, 30):
        d.line([(L, Y(v)), (L + width, Y(v))], fill=(179, 51, 43) if v == 10 else (205, 195, 180), width=2 if v == 10 else 1)
        d.text((10, Y(v) - 8), f'{v} dB', fill=(60, 50, 40), font=font(12))
    for i, (c, sb, lu) in enumerate(rows):
        x0 = L + i * bw
        d.rectangle([x0 + 3, Y(sb), x0 + bw * 0.5, Y(0)], fill=(39, 54, 80))
        d.rectangle([x0 + bw * 0.5, Y(lu), x0 + bw - 3, Y(0)], fill=(196, 144, 63))
        d.text((x0 + 2, T + height + 8), c, fill=(30, 25, 20), font=font(12))
        d.text((x0 + 2, Y(max(sb, lu)) - 15), f'{sb:.0f}', fill=(39, 54, 80), font=font(11))
    d.text((L, 12), 'Her cümlede anlatımın müziğin üstündeki payı. Lacivert: konuşma bandı 500 Hz-4 kHz (anlaşılırlık). '
                    'Okra: LUFS farkı. Kırmızı çizgi: 10 dB', fill=(30, 25, 20), font=font(18))
    can.save(path)


# ------------------------------------------------------------------------- main
def main():
    OUT.mkdir(parents=True, exist_ok=True)
    stems = HERE / 'stems'
    if not (stems / 'vo.wav').exists() or not (HERE / 'mix.wav').exists():
        raise SystemExit('önce: python3 tools/mix.py --stems')
    mix, sr = sf.read(HERE / 'mix.wav', always_2d=True)
    vo, _ = sf.read(stems / 'vo.wav', always_2d=True)
    mu, _ = sf.read(stems / 'music.wav', always_2d=True)
    raw, _ = sf.read(HERE / 'music.wav', always_2d=True)
    pm, pv, pu = kpower(mix), kpower(vo), kpower(mu)
    tx, lx = short_term(pm, sr)
    tv, lv = short_term(pv, sr)
    tm, lm = short_term(pu, sr)
    marks = hits_from_cues_md()
    level_png(tv, lv, tm, lm, tx, lx, OUT / 'seviye.png', marks)
    bv, bu = band_power(vo, sr), band_power(mu, sr)
    rows, lines = [], []
    for c in ORDER:
        a, b = int(CUES[c][0] * sr), int(CUES[c][1] * sr)
        sb = 10 * np.log10(bv[a:b].mean() / (bu[a:b].mean() + 1e-15))
        lu = integrated(pv[a:b], sr) - integrated(pu[a:b], sr)
        rows.append((c, sb, lu))
        lines.append(f'  {c}  {CUES[c][0]:7.2f}-{CUES[c][1]:7.2f}  konuşma bandı {sb:5.1f} dB   LUFS farkı {lu:5.1f} LU')
    margin_png(rows, OUT / 'konusma_marji.png')
    spectrogram_png(raw, sr, 0, DUR, OUT / 'spektrogram_muzik.png', 'audio/music.wav - tüm film (log frekans)',
                    [(t, l.split(':')[0]) for t, l in marks])
    spectrogram_png(mix, sr, min(300.0, DUR - 60), DUR, OUT / 'spektrogram_final.png',
                    'audio/mix.wav - G01 doruk, G02, G06 ve bitiş ekranı bando marşı', [(t, l[:30]) for t, l in marks])
    sp = np.array([CUES[c] for c in ORDER])
    talking = np.zeros(len(tm), bool)
    for a, b in sp:
        talking |= (tm >= a) & (tm <= b)
    sec_rows = []
    for s in SECTIONS:
        sel = (tm >= s[2]) & (tm < s[3])
        sec_rows.append(f'  {s[0]} {s[1]:28s} {s[2]:7.2f}-{s[3]:7.2f}  müzik ortanca {np.median(lm[sel]):6.1f}  '
                        f'en yüksek {lm[sel].max():6.1f}  miks ortanca {np.median(lx[(tx >= s[2]) & (tx < s[3])]):6.1f} LUFS')
    top = np.argsort(-lx)
    picked = []
    for i in top:
        if all(abs(tx[i] - tx[j]) > 3 for j in picked):
            picked.append(i)
        if len(picked) == 6:
            break
    last = CUES[ORDER[-1]][1]
    ya = [t for t, l in marks if 'Yaşasın' in l]
    top_c = [t for t, l in marks if 'DORUK' in l]
    rep = [f'Miks (audio/mix.wav): {mix.shape[0]} örnek = {mix.shape[0] / sr:.3f} sn (timeline DUR {DUR:.3f}), '
           f'{sr} Hz, {mix.shape[1]} kanal, {sf.info(HERE / "mix.wav").subtype}',
           f'  entegre {integrated(pm, sr):.2f} LUFS   gerçek tepe {true_peak(mix):.2f} dBTP',
           f'  anlatım (stem) {integrated(pv, sr):.1f} LUFS   müzik (stem, miksteki seviyesi) {integrated(pu, sr):.1f} LUFS',
           f'  müzik, anlatım varken (ortanca kısa süreli) {np.median(lm[talking]):.1f} LUFS; boşluklarda '
           f'{np.median(lm[~talking & (tm > 1) & (tm < last)]):.1f} LUFS; bitiş ekranı {np.median(lm[tm > last + 1]):.1f} LUFS',
           '  miksin en yüksek 3 sn pencereleri: ' + ', '.join(f'{tx[i]:.0f} sn {lx[i]:.1f}' for i in picked)]
    if ya and top_c:
        a, b = int(ya[0] * sr), int(top_c[0] * sr)
        rep.append(f'  "Yaşasın Cumhuriyet!" altında müzik {integrated(pu[a:b], sr):.1f} LUFS (nefes), '
                   f'doruğun ilk 2 sn\'si {integrated(pu[b:b + 2 * sr], sr):.1f} LUFS')
    sb_all = np.array([r[1] for r in rows])
    lu_all = np.array([r[2] for r in rows])
    rep += [f'  cümle başına pay: konuşma bandı ortanca {np.median(sb_all):.1f} dB (en düşük {sb_all.min():.1f}, '
            f'{rows[int(sb_all.argmin())][0]}); LUFS farkı ortanca {np.median(lu_all):.1f} LU (en düşük {lu_all.min():.1f}, '
            f'{rows[int(lu_all.argmin())][0]})', '', 'Bölümler:'] + sec_rows + ['', 'Cümleler:'] + lines
    (OUT / 'olcumler.txt').write_text('\n'.join(rep) + '\n', encoding='utf-8')
    print('\n'.join(rep[:8]))
    print(f'yazıldı: {", ".join(p.name for p in sorted(OUT.glob("*")))}')


if __name__ == '__main__':
    main()
