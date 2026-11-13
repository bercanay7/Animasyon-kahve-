import numpy as np, json
from scipy.ndimage import uniform_filter1d, maximum_filter1d
from common import *
F = np.load('frames.npz'); FR = 0.02
V = {k[2:]: F[k] for k in F if k.startswith('v_')}; Mu = {k[2:]: F[k] for k in F if k.startswith('m_')}; Pp = {k[2:]: F[k] for k in F if k.startswith('p_')}
nf = len(V['bb']); t = (np.arange(nf) + 0.5) * FR
dB = lambda p: 10 * np.log10(p + 1e-20)
# konuşma etkin kareler: kelime aralıkları içinde ve cümlenin en yüksek karesinin 25 dB altına kadar
inword = np.zeros(nf, bool); wid = np.full(nf, -1)
for i, w in enumerate(WORDS):
    a, b = int(w['s'] / FR), int(w['e'] / FR) + 1; inword[a:b] = True; wid[a:b] = i
cue_of = np.full(nf, '', object)
act = np.zeros(nf, bool)
for c, v in CUES.items():
    a, b = int(v['s'] / FR), int(v['e'] / FR) + 1
    lv = dB(V['k'][a:b]); thr = np.percentile(lv, 95) - 25
    act[a:b] = inword[a:b] & (lv > thr); cue_of[a:b] = c
IMP = {'o250': .0617, 'o500': .1671, 'o1k': .2373, 'o2k': .2648, 'o4k': .2142, 'o8k': .0549}
def smr(band, m):
    return dB(V[band][m].sum()) - dB(Mu[band][m].sum())
def sii(m):
    s = 0
    for b, w in IMP.items():
        s += w * (np.clip(smr(b, m), -15, 15) + 15) / 30
    return s
rows = []
for c, v in CUES.items():
    a, b = int(v['s'] / FR), int(v['e'] / FR) + 1
    m = np.zeros(nf, bool); m[a:b] = act[a:b]
    # kelime düzeyi 1-4k
    ws = [(i, w) for i, w in enumerate(WORDS) if w['id'] == c]
    wsm = []
    for i, w in ws:
        mm = (wid == i) & act
        if mm.sum() >= 3: wsm.append((w['w'], round(float(smr('1-4k', mm)), 1), round(w['s'], 2)))
    worst = min(wsm, key=lambda z: z[1]) if wsm else None
    rows.append(dict(id=c, s=v['s'], e=v['e'], K=round(float(smr('k', m)), 1), bb=round(float(smr('bb', m)), 1), b14=round(float(smr('1-4k', m)), 1),
                     phone=round(float(smr('phone', m)), 1), sii=round(float(sii(m)), 3), worst_word=worst,
                     words_lt6=sum(1 for z in wsm if z[1] < 6), words_lt3=sum(1 for z in wsm if z[1] < 3), nwords=len(wsm),
                     o=[round(float(smr(bn, m)), 1) for bn in IMP]))
json.dump(rows, open('intel_rows.json', 'w'), ensure_ascii=False)
out = {}
allm = act
out['film_SMR'] = {b: round(float(smr(b, allm)), 1) for b in ('k', 'bb', '1-4k', 'phone', *IMP)}
out['film_SII_proxy'] = round(float(sii(allm)), 3)
K = np.array([r['K'] for r in rows]); B = np.array([r['b14'] for r in rows]); Ph = np.array([r['phone'] for r in rows])
out['sent_K_pct'] = {p: round(float(np.percentile(K, p)), 1) for p in (0, 5, 10, 50, 90)}
out['sent_b14_pct'] = {p: round(float(np.percentile(B, p)), 1) for p in (0, 5, 10, 50, 90)}
out['sent_phone_pct'] = {p: round(float(np.percentile(Ph, p)), 1) for p in (0, 5, 10, 50, 90)}
out['worst10_b14'] = [(r['id'], fmt(r['s']), r['b14'], r['K'], r['phone'], r['sii'], r['worst_word']) for r in sorted(rows, key=lambda r: r['b14'])[:10]]
out['worst10_K'] = [(r['id'], fmt(r['s']), r['K'], r['b14']) for r in sorted(rows, key=lambda r: r['K'])[:10]]
out['worst10_phone'] = [(r['id'], fmt(r['s']), r['phone']) for r in sorted(rows, key=lambda r: r['phone'])[:10]]
out['worst10_sii'] = [(r['id'], fmt(r['s']), r['sii']) for r in sorted(rows, key=lambda r: r['sii'])[:10]]
# tüm kelimeler
wl = []
for i, w in enumerate(WORDS):
    mm = (wid == i) & act
    if mm.sum() >= 3: wl.append((round(float(smr('1-4k', mm)), 1), w['id'], w['w'], round(w['s'], 2), round(float(smr('k', mm)), 1)))
wl.sort()
arrw = np.array([z[0] for z in wl])
out['words_n'] = len(wl); out['words_frac_lt'] = {th: round(float((arrw < th).mean() * 100), 1) for th in (0, 3, 6, 10)}
out['words_worst25'] = wl[:25]
# kısma: müzik seviyesi orta bantta konuşma sırasında ve boşluklarda
mid = dB(uniform_filter1d(Mu['mid220-3800'], 5)); kmu = dB(uniform_filter1d(Mu['k'], 5)); pmid = dB(uniform_filter1d(Pp['mid220-3800'], 5))
gaps = []
for c0, c1 in zip(ORDER, ORDER[1:]):
    e, s = CUES[c0]['e'], CUES[c1]['s']
    if s - e < 0.5: continue
    sp = (t > e - 0.9) & (t < e - 0.1); gp = (t > e + 0.05) & (t < s - 0.05); nx = (t > s + 0.1) & (t < s + 0.8)
    gaps.append(dict(a=c0, b=c1, e=round(e, 2), gap=round(s - e, 2), rise_mid=round(float(mid[gp].max() - np.median(mid[sp])), 1),
                     rise_k=round(float(kmu[gp].max() - np.median(kmu[sp])), 1), drop_next=round(float(mid[gp].max() - np.median(mid[nx])), 1),
                     rise_pre=round(float(pmid[gp].max() - np.median(pmid[sp])), 1)))
json.dump(gaps, open('gaps.json', 'w'), ensure_ascii=False)
R = np.array([g['rise_mid'] for g in gaps]); Rk = np.array([g['rise_k'] for g in gaps]); Dn = np.array([g['drop_next'] for g in gaps])
out['gap_n'] = len(gaps)
out['gap_rise_mid_pct'] = {p: round(float(np.percentile(R, p)), 1) for p in (10, 50, 90, 100)}
out['gap_rise_K_pct'] = {p: round(float(np.percentile(Rk, p)), 1) for p in (10, 50, 90, 100)}
out['gap_drop_next_pct'] = {p: round(float(np.percentile(Dn, p)), 1) for p in (10, 50, 90, 100)}
out['gaps_rise_gt8'] = [(g['a'], g['b'], fmt(g['e']), g['gap'], g['rise_mid'], g['rise_k']) for g in sorted(gaps, key=lambda g: -g['rise_mid']) if g['rise_mid'] > 8][:15]
# olay kilitli ortalama: cümle sonlarına göre müzik orta bant (yalnız ≥1,0 sn boşluklar)
lags = np.arange(-50, 101)
ev = []; evp = []
for c0, c1 in zip(ORDER, ORDER[1:]):
    e, s = CUES[c0]['e'], CUES[c1]['s']
    if s - e < 1.0: continue
    i = int(e / FR)
    if i - 50 < 0 or i + 101 >= nf: continue
    ref = np.median(mid[i - 40:i - 5]); ev.append(mid[i + lags] - ref)
    refp = np.median(pmid[i - 40:i - 5]); evp.append(pmid[i + lags] - refp)
ev = np.median(np.array(ev), 0); evp = np.median(np.array(evp), 0)
out['eta_mid_dB'] = {f'{l * FR:+.2f}': round(float(ev[list(lags).index(l)]), 1) for l in (-25, 0, 5, 10, 15, 20, 25, 35, 50, 75, 100)}
out['eta_mid_scoreduck_only'] = {f'{l * FR:+.2f}': round(float(evp[list(lags).index(l)]), 1) for l in (-25, 0, 5, 10, 15, 20, 25, 35, 50, 75, 100)}
np.save('eta.npy', np.stack([lags * FR, ev, evp]))
# cümle içi duraklamalar (≥0,4 sn)
ip = []
for w0, w1 in zip(WORDS, WORDS[1:]):
    if w0['id'] == w1['id'] and w1['s'] - w0['e'] >= 0.4:
        sp = (t > w0['e'] - 0.6) & (t < w0['e']); gp = (t > w0['e']) & (t < w1['s'])
        ip.append((w0['id'], w0['w'], round(w0['e'], 2), round(w1['s'] - w0['e'], 2), round(float(mid[gp].max() - np.median(mid[sp])), 1)))
out['intra_pauses_n'] = len(ip); out['intra_pauses_rise_gt6'] = [z for z in ip if z[4] > 6]
json.dump(out, open('intel.json', 'w'), indent=1, ensure_ascii=False)
print(json.dumps(out, indent=1, ensure_ascii=False))
np.savez('curves.npz', t=t, act=act, vk=dB(V['k']), mk=dB(Mu['k']), v14=dB(V['1-4k']), m14=dB(Mu['1-4k']), mid=mid)
