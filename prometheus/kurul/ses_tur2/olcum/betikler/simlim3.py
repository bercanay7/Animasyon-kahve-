# Müzik veriyolu sınırlayıcısının doruklara etkisi ve konuşmaya bağlı tavan denemesi (yalnız ölçüm)
import sys, numpy as np, json, soundfile as sf
sys.path.insert(0, '/home/user/Animasyon-kahve-/prometheus/tools')
import mix as M
from common import *
vo = np.load('vo.npy'); send = np.load('send.npy'); mup = np.load('mu_preduck.npy'); d100 = np.load('duck.npy')
N = len(vo)
duck = np.interp(np.arange(N, dtype=np.float32), np.arange(len(d100), dtype=np.float32) * 480, d100).astype(np.float32)
mpre = mup * duck[None]; del mup
mcur = np.load('mu.npy', mmap_mode='r')
# mevcut müzik sınırlayıcısının kazanç azaltması (10 ms bloklar)
b = 480; nb = N // b
e_pre = (mpre[:, :nb*b].astype(np.float64) ** 2).reshape(2, nb, b).sum((0, 2)); e_post = (np.asarray(mcur[:, :nb*b], np.float64) ** 2).reshape(2, nb, b).sum((0, 2))
ok = e_pre > np.percentile(e_pre, 20)
gr = 10 * np.log10((e_post + 1e-20) / (e_pre + 1e-20))
ve = M.envelope(vo); actf = np.clip((20 * np.log10(ve + 1e-9) + 42) / 10, 0, 1); del ve
sp = actf[:nb*b].reshape(nb, b).max(1) > 0.5
res = {'music_limiter_now': dict(sec_gt1=round(float((ok & (gr < -1)).sum() * .01), 1), sec_gt3=round(float((ok & (gr < -3)).sum() * .01), 1), sec_gt6=round(float((ok & (gr < -6)).sum() * .01), 1),
       sec_gt3_in_speech=round(float((ok & (gr < -3) & sp).sum() * .01), 1), sec_gt3_in_gaps=round(float((ok & (gr < -3) & ~sp).sum() * .01), 1), worst=round(float(gr[ok].min()), 1))}
print(res, flush=True)
spots = {'A04_bosluk': (25.5, 27.0), 'C10': (178.0, 178.9), 'C18_sonrasi': (234.7, 236.9), 'J04_ozgurdur': (1081.45, 1082.8), 'J04_J05_bosluk': (1082.8, 1084.19), 'K06_bosluk': (1386.22, 1389.26), 'I10': (1166.5, 1185.0), 'bitis': (1421.64, 1435.0)}
# konuşma maskesi: ±0,25 sn genişletilmiş, 30 ms yumuşatılmış
from scipy.ndimage import maximum_filter1d, uniform_filter1d
a = maximum_filter1d((actf > 0.3).astype(np.float32), int(.5 * SR)); a = uniform_filter1d(a, int(.03 * SR)); del actf
variants = {'mevcut (-8 dBFS sabit)': np.float32(M.db(-8)), '-4 dBFS sabit': np.float32(M.db(-4)), 'konuşmada -8, boşlukta -1 dBFS': (M.db(-8) * a + M.db(-1) * (1 - a)).astype(np.float32)}
for name, ceil in variants.items():
    m = M.limiter(mpre, ceil, look=.005, rel=.15).astype(np.float32)
    pre = np.empty_like(m)
    for c in range(2): pre[c] = vo + send[c] + m[c]
    x = M.limiter(pre, .7).astype(np.float32)
    L = integrated(block_ms(kfilt(x), 0.1)); x *= np.float32(M.db(-14 - L)); x = M.limiter(x, M.db(-1.6)).astype(np.float32)
    num = (x[:, :nb*b].astype(np.float64) * pre[:, :nb*b]).reshape(2, nb, b).sum((0, 2)); den = (pre[:, :nb*b].astype(np.float64) ** 2).reshape(2, nb, b).sum((0, 2))
    g = num / (den + 1e-20); ok2 = den > np.percentile(den, 30); k = np.median(g[ok2]); g2 = 20 * np.log10(np.maximum(g, 1e-6) / k)
    r = dict(final_gr_sec_gt1=round(float((ok2 & (g2 < -1)).sum() * .01), 1), final_gr_sec_gt2=round(float((ok2 & (g2 < -2)).sum() * .01), 1), worst=round(float(g2[ok2].min()), 2),
             J04=round(float(g2[int(1081.4/.01):int(1082.8/.01)].min()), 2), D11=round(float(g2[int(326/.01):int(329.2/.01)].min()), 2), I10=round(float(g2[int(1166.5/.01):int(1185/.01)].min()), 2))
    for sname, (t0, t1) in spots.items():
        seg = x[:, int(t0*SR):int(t1*SR)]; r['mix_' + sname] = round(float(integrated(block_ms(kfilt(seg), 0.1)) if t1 - t0 > 0.5 else 0), 1)
    # J05 başı ve E10/G09 kelimeleri: konuşma/müzik oranı (1-4k yerine geniş bant K)
    res[name] = r; print(name, r, flush=True)
    del m, pre, x
json.dump(res, open('simlim3.json', 'w'), indent=1, ensure_ascii=False)
