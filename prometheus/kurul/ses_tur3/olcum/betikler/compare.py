import numpy as np, json
from common import *
OLD = '/tmp/claude-0/-home-user/c3662c9d-24be-574f-ac5d-de35ddf76b95/scratchpad/ses2/frames.npz'
F0, F1 = np.load(OLD), np.load('frames.npz'); FR = .02
dB = lambda p: 10 * np.log10(p + 1e-20)
def Wx(i, w, n=0):
    k = 0
    for x in WORDS:
        if x['id'] == i and x['w'].startswith(w):
            if k == n: return x
            k += 1
def smr(F, a, b, band):
    i, j = int(a / FR), int(b / FR) + 1
    return round(float(dB(F['v_' + band][i:j].sum()) - dB(F['m_' + band][i:j].sum())), 1)
words = [('A01', 'bile', 0), ('A01', 'bile', 1), ('A02', 'kayaya', 0), ('A02', 'mıhlatan', 0), ('A04', 'prometeus', 0), ('A06', 'bu', 0), ('C10', 'indirdi', 0), ('C17', 'kapatıldı', 0),
         ('C18', 'prometeus', 0), ('D11', 'uranos', 0), ('D11', 'kronos', 0), ('E10', 'insanlara', 0), ('E10', 'götürür', 0), ('E10', 'hesiodosun', 0), ('E10', 'deyişiyle', 0), ('E14', 'umut', 0), ('E16b', 'durduğunu', 0),
         ('F01', 'neden', 0), ('F07', 'gücü', 0), ('F10b', 'indi', 0), ('F10b', 'indi', 1), ('G07b', 'görülmedim', 0), ('G08', 'verdi', 0), ('I10', 'gök', 1), ('I10', 'denize', 0), ('I10', 'karıştı', 0),
         ('I11', 'musun', 0), ('I12', 'son', 0), ('I12', 'söz', 0), ('I12', 'onundur', 0), ('J04', 'prometeus', 0), ('J04', 'özgürdür', 0), ('L06', 'o', 0), ('M02', 'olsan', 0)]
rows = []
for c, w, n in words:
    x = Wx(c, w, n)
    rows.append((c, w, n, round(x['s'], 2), smr(F0, x['s'], x['e'], '1-4k'), smr(F1, x['s'], x['e'], '1-4k'), smr(F0, x['s'], x['e'], 'k'), smr(F1, x['s'], x['e'], 'k')))
print('kelime  zaman  1-4k önce→sonra  K önce→sonra')
for r in rows: print(f'{r[0]:5s} {r[1]:11s}#{r[2]} {r[3]:8.2f}  {r[4]:6.1f} → {r[5]:6.1f}   {r[6]:6.1f} → {r[7]:6.1f}')
# yan etki: taşınan motiflerin düştüğü kelimeler
def S_(i): return CUES[i]['s']
def E_(i): return CUES[i]['e']
mv = [('A04', E_('A04') + .05, 1.8), ('C18', E_('C18') + .05, 1.84), ('E10', Wx('E10', 'götürür')['e'] + .05, 1.68), ('F01', E_('F01') + .05, 3.4), ('G08', E_('G08') + .05, 1.36),
      ('J04', Wx('J04', 'özgürdür')['e'] + .05, 2.5), ('I12', Wx('I12', 'onundur')['e'] + .05, 1.76), ('L06', E_('L06') + .05, 1.04), ('M02', E_('M02') + .05, 1.4)]
side = []
print('\nyan etki: taşınan motifin süresi içinde başlayan kelimeler (1-4k SMR önce→sonra, K önce→sonra)')
for c, t0, d in mv:
    ws = [x for x in WORDS if t0 - .02 <= x['s'] <= t0 + d + .3]
    out = [(x['id'], x['w'], round(x['s'], 2), smr(F0, x['s'], x['e'], '1-4k'), smr(F1, x['s'], x['e'], '1-4k'), smr(F0, x['s'], x['e'], 'k'), smr(F1, x['s'], x['e'], 'k')) for x in ws]
    side.append((c, round(t0, 2), d, out))
    print(f'{c} motif {t0:.2f}–{t0 + d:.2f}:', '; '.join(f'{o[0]} {o[1]} {o[3]}→{o[4]} (K {o[5]}→{o[6]})' for o in out) if out else 'kelime yok (boşlukta)')
json.dump(dict(words=rows, side=side), open('compare_words.json', 'w'), ensure_ascii=False, indent=1)
