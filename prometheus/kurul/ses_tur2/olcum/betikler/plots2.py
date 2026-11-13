import sys, json, numpy as np
sys.path.append('/tmp/claude-0/-home-user/c3662c9d-24be-574f-ac5d-de35ddf76b95/scratchpad/pylib')
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from common import *
OUT = P + 'kurul/ses_tur2/'; OLD = '/tmp/claude-0/-home-user/c3662c9d-24be-574f-ac5d-de35ddf76b95/scratchpad/ses/'
e0, e1 = np.load(OLD + 'eta.npy'), np.load('eta.npy')
plt.figure(figsize=(8, 4.2)); plt.plot(e0[0], e0[1], c='tab:red', label='tur 1 (önce)'); plt.plot(e1[0], e1[1], c='tab:green', label='tur 2 (sonra)')
plt.axvline(0, c='k', lw=.6); plt.axhline(0, c='gray', lw=.5); plt.grid(alpha=.3); plt.legend(fontsize=8)
plt.xlabel('cümle sonuna göre zaman (sn), boşluk ≥ 1 sn, medyan, n=87'); plt.ylabel('müzik 220–3800 Hz (dB, konuşmaya göre)')
plt.title('Pompalama: +6,3 dB → +2,3 dB (0,7 sn)'); plt.tight_layout(); plt.savefig(OUT + 'pompalama_once_sonra.png', dpi=100); plt.close()
# doruklar: son miks LUFS önce / sonra / önerilen (konuşmaya bağlı tavan, benzetim)
s3 = json.load(open('simlim3.json'))
names = [('A04 başlık sonrası', 'A04_bosluk', -10.7), ('C18 sonrası motif', 'C18_sonrasi', -11.2), ('J04→J05 doruk boşluğu', 'J04_J05_bosluk', -10.5), ('K06 doruk boşluğu', 'K06_bosluk', -9.9), ('C10 indirdi', 'C10', -11.6), ('bitiş ekranı', 'bitis', -17.9)]
x = np.arange(len(names)); w = .27
plt.figure(figsize=(10, 4.4))
plt.bar(x - w, [n[2] + 40 for n in names], w, bottom=-40, label='tur 1 (önce)', color='tab:gray')
plt.bar(x, [s3['mevcut (-8 dBFS sabit)']['mix_' + n[1]] + 40 for n in names], w, bottom=-40, label='tur 2 (şimdi, müzik tavanı −8 dBFS sabit)', color='tab:red')
plt.bar(x + w, [s3['konuşmada -8, boşlukta -1 dBFS']['mix_' + n[1]] + 40 for n in names], w, bottom=-40, label='öneri benzetimi: konuşmada −8, boşlukta −1 dBFS', color='tab:green')
plt.axhline(-14, c='k', ls='--', lw=.8); plt.xticks(x, [n[0] for n in names], fontsize=8); plt.ylim(-22, -8); plt.ylabel('son miks yükseklik (LUFS, pencere)')
plt.title('Dorukların gücü: müzik sınırlayıcısı boşluktaki dorukları 4–7 dB kırptı'); plt.legend(fontsize=7.5, loc='lower left'); plt.grid(alpha=.3, axis='y'); plt.tight_layout(); plt.savefig(OUT + 'doruklar_once_sonra.png', dpi=100); plt.close()
# yan etki yakın planları
F0, F1 = np.load(OLD + 'frames.npz'), np.load('frames.npz'); FR = .02
dB = lambda p: 10 * np.log10(p + 1e-20)
sm = lambda p: dB(np.convolve(p, np.ones(5) / 5, 'same'))
t = (np.arange(len(F1['v_bb'])) + .5) * FR
zooms = [('J04 → J05: motif "Ona göre Zeus bütün"ün üstünde', 1080.5, 1087.0), ('G08 → G09: motif "Erhat burada sorar"ın üstünde', 756.5, 761.5), ('E10: motif "Hesiodos\'un deyişiyle uzaktan"ın üstünde', 404.5, 409.5), ('F01 → F02: aulos F02\'nin ilk 2,3 sn\'sinde', 493.0, 499.5)]
fig, ax = plt.subplots(len(zooms), 1, figsize=(13, 2.9 * len(zooms)))
for a, (name, t0, t1) in zip(ax, zooms):
    m = (t >= t0) & (t <= t1)
    a.plot(t[m], sm(F1['v_1-4k'])[m], c='tab:blue', lw=.9, label='anlatım 1–4 kHz')
    a.plot(t[m], sm(F0['m_1-4k'])[m], c='tab:gray', lw=.8, ls='--', label='müzik 1–4 kHz, tur 1')
    a.plot(t[m], sm(F1['m_1-4k'])[m], c='tab:orange', lw=.9, label='müzik 1–4 kHz, tur 2')
    for w_ in WORDS:
        if t0 <= w_['s'] <= t1: a.annotate(w_['w'], (w_['s'], -22), fontsize=6.5, rotation=60)
    a.set_ylim(-95, -15); a.set_title(name, fontsize=9); a.legend(fontsize=7, loc='lower right'); a.grid(alpha=.3)
plt.tight_layout(); plt.savefig(OUT + 'yan_etki_yakin_plan.png', dpi=90); plt.close()
print('ok')
