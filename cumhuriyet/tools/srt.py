"""Altyazı: senaryo 'alt' metni + kelime zamanları → cumhuriyet.tr.srt (python3 tools/srt.py)"""
import json, re, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAXL, MAXC = 42, 80  # satır / altyazı başına karakter (iki satır 42'yi aşmadan sığsın)

segs = json.load(open(os.path.join(ROOT, 'senaryo.json')))['segments']
tl = open(os.path.join(ROOT, 'timeline.js')).read()
WORDS = json.loads(re.search(r'window\.WORDS = (\[.*?\]);', tl, re.S).group(1))

def fmt(t):
    ms = int(round(t * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
    return f'{h:02d}:{m:02d}:{s:02d},{ms:03d}'

# tipografi kurulunun okuma birimleri: altyazı bu sözcükten sonra biter (CUT) ya da satır burada kırılır (LB)
# anahtar: (cümle, sözcük[, kaçıncı geçiş])
CUT = [('A02', 'der:'), ('A04', 'okullarında:'), ('B02', 'sadık,'), ('B03', 'imparatorlukta'), ('B06', 'da'), ('C02', 'fikirleri,'),
       ('C06', 'Kemal', 0), ('E04', 'çok,'), ('E05', 'yarbay,'), ('F03', 'da'), ('F04', 'seslendi,'), ('F06', 'hazırdı.'), ('G04', 'şu:')]
LB = [('A02', 'göre,'), ('A04', 'dikilecekleri'), ('B02', 'memurlar'), ('B03', 'rüşdiye,'), ('B06', 'erken'), ('C02', 'önce'), ('C06', 'çıkan'),
      ('C06', 'ihbarla'), ('E04', 'kuşağı'), ('E05', "Anafartalar'da,"), ('F03', 'İsmet'), ('F04', 'Edib'), ('F04', 'katılıp'),
      ('F06', 'birleştiren'), ('G04', 'sonrası,'), ('B04', 'idadilerde'), ('B05', 'sultan,'), ('B05', 'yalnızca'),
      ('B06', 'öğretmeni'), ('C01', 'imparatorluğun'), ('C02', 'dünyanın'), ('C03', 'olmayan'), ('C06', 'arkadaşlarıyla'),
      ('D03', 'sonra'), ('D03', 'arasında'), ('E01', 'kuşağın'), ('F02', 'biri,'), ('F05', 'siperlerde'), ('G03', 'Rauf'),
      ('G05', 'hayatınızda'), ('G06', 'Cumhuriyetimizin'), ('G01', 'akşamı,')]
def marks(sid, toks, table):
    out = set()
    for k in table:
        if k[0] != sid: continue
        hits = [i for i, x in enumerate(toks) if x == k[1]]
        if not hits: print('UYARI: işaret bulunamadı', k); continue
        out.add(hits[k[2]] if len(k) > 2 else hits[0])
    return out

def wrap(words, lb=()):
    """iki satıra dengeli böl (lb: satırın kırılacağı sözcük sırası, varsa)"""
    s = ' '.join(words)
    for i in lb:
        if 0 < i + 1 < len(words): return ' '.join(words[:i + 1]) + '\n' + ' '.join(words[i + 1:])
    if len(s) <= MAXL: return s
    best, bi = 1e9, 1
    for i in range(1, len(words)):
        a, b = ' '.join(words[:i]), ' '.join(words[i:])
        cost = abs(len(a) - len(b)) - (12 if words[i - 1][-1] in ',.:;…?!' else 0) + 100 * max(0, len(a) - MAXL, len(b) - MAXL)
        if cost < best: best, bi = cost, i
    return ' '.join(words[:bi]) + '\n' + ' '.join(words[bi:])

MERGE = {('C03', 'Kızsa,'): 2}
cues = []
for sg in segs:
    toks = sg['alt'].replace('…', '… ').split()
    toks = [x for x in toks if re.sub(r"[^\wçğıöşüâîÇĞİÖŞÜ]+", '', x)]
    # görünen sözcük, seslendirmede birden çok sözcükse ("1923") bitişi grubun son sözcüğüdür ('de', tools/fix_disp.py)
    ws = [{**w, 'e': w.get('de', w['e'])} for w in WORDS if w['id'] == sg['id'] and w['d']]
    # altyazıda tek sözcük, anlatım zamanlamasında iki sözcük olan kısaltmalar ("Kız ise" → duyulan "Kızsa,")
    for (sid, tok), k in MERGE.items():
        if sid == sg['id'] and tok in toks:
            i = toks.index(tok); ws = ws[:i] + [{**ws[i], 'e': ws[i + k - 1]['e']}] + ws[i + k:]
    if len(ws) != len(toks):
        print('UYARI: kelime sayısı uyuşmuyor', sg['id'], len(ws), len(toks))
    n = min(len(ws), len(toks))
    cut, lb = marks(sg['id'], toks, CUT), marks(sg['id'], toks, LB)
    # önce cümlelere, uzun cümleleri dengeli parçalara böl (tek kelimelik yetim altyazı kalmasın; virgül tercih edilir)
    sents, cur = [], []
    for i in range(n):
        cur.append(i)
        if i == n - 1 or i in cut or toks[i][-1] in '.?!…' or toks[i].endswith('.”') or toks[i].endswith('?”'):
            sents.append(cur); cur = []
    # çok kısa cümleleri (≤ 2 kelime) bir sonrakiyle birleştir
    merged = []
    for sn in sents:
        if merged and merged[-1][-1] not in cut and len(merged[-1]) <= 2 and len(' '.join(toks[j] for j in merged[-1] + sn)) <= MAXC: merged[-1] += sn
        else: merged.append(sn)
    for sn in merged:
        L = len(' '.join(toks[j] for j in sn))
        k = max(1, -(-L // MAXC))
        if k == 1: parts = [sn]
        else:
            # k parçaya böl: hedef uzunluklara en yakın, virgüllü sınırları ödüllendiren dinamik bölme
            import itertools
            best, parts = 1e9, None
            for cuts in itertools.combinations(range(1, len(sn)), k - 1):
                ps = [sn[a_:b_] for a_, b_ in zip((0,) + cuts, cuts + (len(sn),))]
                ls = [len(' '.join(toks[j] for j in pp)) for pp in ps]
                cost = sum(abs(l - L / k) for l in ls) + 200 * sum(max(0, l - MAXC) for l in ls) - sum(10 for pp in ps[:-1] if toks[pp[-1]][-1] in ',;:') + 100 * sum(1 for pp in ps if len(pp) < 2)
                if cost < best: best, parts = cost, ps
        for pp in parts:
            cues.append([ws[pp[0]]['s'], ws[pp[-1]]['e'], wrap([toks[j] for j in pp], [k for k, j in enumerate(pp) if j in lb]), pp[-1] in cut])

# süreleri düzenle: en az 1.0 sn, bir sonrakine 80 ms boşluk, okunabilirlik için en fazla +0.6 sn uzat
def settle_times():
    for i, c in enumerate(cues):
        nxt = cues[i + 1][0] if i + 1 < len(cues) else c[1] + 3
        c[1] = min(max(c[1] + .35, c[0] + 1.0), nxt - .08)
    # hâlâ hızlı okunan altyazı (>16,5 kr/sn), önceki boşsa en çok 0,5 sn erken belirir
    for i, c in enumerate(cues):
        L = len(c[2].replace('\n', ' '))
        if L / (c[1] - c[0]) > 16.5:
            prev = cues[i - 1][1] + .08 if i else 0
            c[0] = max(c[0] - .5, prev, c[1] - L / 16.5) if c[0] - .5 >= prev else max(prev, min(c[0], c[1] - L / 16.5))
raw = [c[:] for c in cues]
settle_times()
# okuma hızı 18 karakter/sn'yi aşan kısa altyazı, sonraki kısa altyazıyla birleşir (sığıyorsa)
i = 0
while i < len(cues) - 1:
    a_, b_ = cues[i], cues[i + 1]
    ta, tb = a_[2].replace('\n', ' '), b_[2].replace('\n', ' ')
    if not a_[3] and len(ta) / (a_[1] - a_[0]) > 18 and len(ta) + 1 + len(tb) <= MAXC and raw[i + 1][0] - raw[i][1] < 1.0:
        cues[i] = [raw[i][0], raw[i + 1][1], wrap((ta + ' ' + tb).split()), b_[3]]; raw[i] = [raw[i][0], raw[i + 1][1], '', b_[3]]
        del cues[i + 1]; del raw[i + 1]
        for k, c in enumerate(cues): c[1] = raw[k][1]
        settle_times()
    else: i += 1

# duraktan sonra açılan altyazı sesin gerçek başlangıcına oturur: Whisper ilk sözcüğü (sayılar, cümle başı) erken
# işaretleyebiliyor (teknik kurulu: 3:25, 4:51, 5:44). Başlangıç, anlatımın enerjisi (tepeye göre -45 dB) aşıldığı andan
# 0,1 sn önceye çekilir; yalnız 0,33 sn'den çok erkense ve okuma hızı 16,5 kr/sn'yi aşmıyorsa
import numpy as np, soundfile as sf
vo, sr = sf.read(os.path.join(ROOT, 'vo', 'vo.wav'), always_2d=True); vo = vo.mean(1)
hop = int(sr * .01); env = np.sqrt(np.convolve(vo ** 2, np.ones(hop) / hop, 'same')[::hop]) + 1e-9
env_db = 20 * np.log10(env / env.max())
for i, c in enumerate(cues):
    prev = cues[i - 1][1] if i else 0
    k0, k1 = int(c[0] / .01), int(min(c[0] + 1.2, c[1]) / .01)
    on = np.nonzero(env_db[k0:k1] > -45)[0]
    if not len(on): continue
    t_on = (k0 + on[0]) * .01
    L = len(c[2].replace('\n', ' '))
    if t_on - c[0] > .33 and c[0] >= prev + .15 and L / (c[1] - (t_on - .1)) <= 16.5:
        c[0] = t_on - .1

out = os.path.join(ROOT, 'cumhuriyet.tr.srt')
with open(out, 'w', encoding='utf-8') as f:
    for i, (a, b, t, _) in enumerate(cues, 1):
        f.write(f'{i}\n{fmt(a)} --> {fmt(b)}\n{t}\n\n')
print(len(cues), 'altyazı →', out)
