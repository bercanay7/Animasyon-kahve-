import sys, json, numpy as np
sys.path.append('/tmp/claude-0/-home-user/c3662c9d-24be-574f-ac5d-de35ddf76b95/scratchpad/pylib')
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from common import *
OUT = P + 'kurul/ses_tur3/'
F = np.load('frames.npz'); FR = .02
dB = lambda p: 10 * np.log10(p + 1e-20)
def st(p, k):  # k kare kayan ortalama → LUFS benzeri
    c = np.concatenate([[0], np.cumsum(p)]); w = (c[k:] - c[:-k]) / k; return -0.691 + dB(w)
k3 = int(3 / FR)
vS = st(F['v_k'], k3); mS = st(F['m_k'], k3); tt = (np.arange(len(vS)) + k3 / 2) * FR
mixS = np.load('mix_short.npy'); gr = np.load('gr.npy')
rows = json.load(open('intel_rows.json'))
secs = {}
for c, v in CUES.items(): secs.setdefault(v['sec'], [v['s'], v['e']]); secs[v['sec']][1] = v['e']
key = {'A01 açılış': 0.7, 'C07/C10 taht': 154, 'D11 sessizlik': 331, 'E10 rezene': 405, 'F14 fısıltı': 651, 'J04 doruk': 1081, 'I10 fırtına': 1177, 'L06': 1280, 'K06': 1385, 'bitiş ekranı': 1422}
fig, ax = plt.subplots(4, 1, figsize=(18, 13), sharex=True, gridspec_kw=dict(height_ratios=[1.2, 1.2, 1, .7]))
ax[0].plot(mixS[0], mixS[1], lw=.6, c='k'); ax[0].axhline(-14, c='r', lw=.8, ls='--'); ax[0].set_ylim(-35, -5); ax[0].set_ylabel('Miks kısa süreli (3 sn) LUFS')
ax[0].set_title('Prometheus son miks: yükseklik, anlatım/müzik, cümle bazında SMR ve sınırlayıcı (ses kurulu tur 3)')
ax[1].plot(tt, vS, lw=.6, c='tab:blue', label='anlatım (K, 3 sn)'); ax[1].plot(tt, mS, lw=.6, c='tab:orange', label='müzik+efekt (K, 3 sn, kısma sonrası)')
ax[1].set_ylim(-60, -5); ax[1].set_ylabel('LUFS benzeri (miks öncesi ölçek)'); ax[1].legend(loc='lower left', fontsize=8)
x = [(r['s'] + r['e']) / 2 for r in rows]; y = [r['b14'] for r in rows]; yk = [r['K'] for r in rows]
cols = ['tab:red' if v < 10 else 'tab:green' for v in y]
ax[2].scatter(x, y, s=14, c=cols, label='1–4 kHz SMR (kırmızı < 10 dB)'); ax[2].scatter(x, yk, s=8, c='tab:purple', marker='x', label='K-ağırlıklı SMR')
for r in sorted(rows, key=lambda r: r['b14'])[:10]: ax[2].annotate(r['id'], ((r['s'] + r['e']) / 2, r['b14']), fontsize=7, xytext=(2, -9), textcoords='offset points')
ax[2].axhline(10, c='gray', lw=.6, ls='--'); ax[2].set_ylim(-5, 50); ax[2].set_ylabel('Cümle SMR (dB)'); ax[2].legend(loc='upper right', fontsize=8)
msk = np.load('mix_ms100.npy'); rr = np.repeat(msk, 10); n2 = min(len(rr), gr.shape[1]); lv = -0.691 + 10*np.log10(rr[:n2] + 1e-20); g2 = np.where(lv > -35, gr[1][:n2], 0)
from scipy.ndimage import minimum_filter1d
ax[3].plot(gr[0][:len(g2)], minimum_filter1d(g2, 50), lw=.6, c='tab:red'); ax[3].set_ylim(-7, .5); ax[3].set_ylabel('Son sınırlayıcı GR (dB, 0,5 sn en derin)')
for a in ax:
    for k, (s, e) in secs.items(): a.axvline(s, c='gray', lw=.4, alpha=.5)
for n, tk in key.items(): ax[0].annotate(n, (tk, -7), fontsize=7, rotation=90, va='top')
for k, (s, e) in secs.items(): ax[3].annotate(SECS[k], (s + 2, -6.8), fontsize=6.5, rotation=90, va='bottom')
ax[3].set_xlabel('film zamanı (sn)'); ax[3].set_xlim(0, DUR)
plt.tight_layout(); plt.savefig(OUT + 'genel_zaman_cizelgesi.png', dpi=90); plt.close()
# pompalama: olay kilitli ortalama
e = np.load('eta.npy')
NG = sum(1 for c0, c1 in zip(ORDER, ORDER[1:]) if CUES[c1]['s'] - CUES[c0]['e'] >= 1.0)
plt.figure(figsize=(8, 4.2)); plt.plot(e[0], e[1], label='son miks (score.py spektral + mix.py −3 dB kısma)'); plt.plot(e[0], e[2], label='yalnız score.py kısması')
plt.axvline(0, c='k', lw=.6); plt.axhline(0, c='gray', lw=.5); plt.xlabel('cümle sonuna göre zaman (sn), boşluk ≥ 1 sn, medyan, n=%d' % NG); plt.ylabel('müzik 220–3800 Hz seviyesi (dB, konuşmaya göre)')
plt.title('Cümle aralarında müzik "nefes alıyor": +6,3 dB / 0,7 sn'); plt.legend(fontsize=8); plt.grid(alpha=.3); plt.tight_layout(); plt.savefig(OUT + 'pompalama_olay_ortalamasi.png', dpi=100); plt.close()
# yakın plan anlar
C = np.load('curves.npz'); t = C['t']
def sm(p, k=5): return dB(np.convolve(p, np.ones(k) / k, 'same'))
zooms = [('Açılış A01–A02 (0–12 sn)', 0, 12), ('E10 rezene: "insanlara götürür"', 403, 409), ('J04 doruk', 1076.5, 1084.5), ('I10–I12 fırtına ve "Son söz onundur"', 1176, 1209), ('L06 meşale koşusu', 1279, 1287.5), ('C10 / C18 taht ve "Prometheus"', 176, 180), ]
fig, ax = plt.subplots(len(zooms), 1, figsize=(14, 3.0 * len(zooms)))
for a, (name, t0, t1) in zip(ax, zooms):
    m = (t >= t0) & (t <= t1)
    a.plot(t[m], sm(F['v_1-4k'])[m], c='tab:blue', lw=.8, label='anlatım 1–4 kHz'); a.plot(t[m], sm(F['m_1-4k'])[m], c='tab:orange', lw=.8, label='müzik+efekt 1–4 kHz')
    for w in WORDS:
        if t0 <= w['s'] <= t1: a.annotate(w['w'], (w['s'], a.get_ylim()[1] if False else -25), fontsize=6.5, rotation=60)
    a.set_title(name, fontsize=9); a.set_ylim(-95, -15); a.legend(fontsize=7, loc='lower right'); a.grid(alpha=.3)
plt.tight_layout(); plt.savefig(OUT + 'yakin_plan_maskeleme.png', dpi=90); plt.close()
print('ok')
