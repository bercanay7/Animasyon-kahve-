# Öneri denemesi: müzik veriyoluna ayrı tepe sınırlayıcı (proje dosyası değişmez; yalnız ölçüm)
import sys, numpy as np, json
sys.path.insert(0, '/home/user/Animasyon-kahve-/prometheus/tools')
import mix as M
from common import *
vo = np.load('vo.npy'); send = np.load('send.npy'); mu = np.load('mu.npy')
res = {}
for ceil_db in (None, -6.0):
    m = mu.copy()
    if ceil_db is not None: m = M.limiter(m, M.db(ceil_db), look=.005, rel=.15).astype(np.float32)
    pre = np.empty_like(m)
    for c in range(2): pre[c] = vo + send[c] + m[c]
    x = M.limiter(pre, .7).astype(np.float32)
    ms = block_ms(kfilt(x), 0.1); L = integrated(ms)
    x *= np.float32(M.db(-14 - L))
    x = M.limiter(x, M.db(-1.6)).astype(np.float32)
    b = 480; nb = x.shape[1] // b
    num = (x[:, :nb*b].astype(np.float64) * pre[:, :nb*b]).reshape(2, nb, b).sum((0, 2)); den = (pre[:, :nb*b].astype(np.float64) ** 2).reshape(2, nb, b).sum((0, 2))
    g = num / (den + 1e-20); ok = den > np.percentile(den, 30); k = np.median(g[ok]); gr = 20 * np.log10(np.maximum(g, 1e-6) / k)
    tag = 'mevcut' if ceil_db is None else f'müzik sınırlayıcı {ceil_db} dBFS'
    res[tag] = dict(sec_lt_1=round(float((gr[ok] < -1).sum() * .01), 1), sec_lt_2=round(float((gr[ok] < -2).sum() * .01), 1), min=round(float(gr[ok].min()), 2),
                    J04=round(float(gr[int(1081.4/.01):int(1082.8/.01)].min()), 2), D11=round(float(gr[int(326/.01):int(329.2/.01)].min()), 2), I10=round(float(gr[int(1166.5/.01):int(1185/.01)].min()), 2),
                    music_gr_peak_sec=None)
    if ceil_db is not None:
        # müzik veriyolundaki sınırlamanın ne kadar sürdüğü
        a = np.abs(mu).max(0); n = len(a) // 480; pk = a[:n*480].reshape(n, 480).max(1)
        res[tag]['music_limited_sec'] = round(float((pk > M.db(ceil_db)).sum() * .01), 1)
    print(tag, res[tag], flush=True)
    del x, pre, m
json.dump(res, open('simlim.json', 'w'), indent=1, ensure_ascii=False)
