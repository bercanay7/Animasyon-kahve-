"""Altyazı: senaryo 'alt' metni + kelime zamanları → ikaros.tr.srt (python3 tools/srt.py)"""
import json, re, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAXL, MAXC = 42, 80  # satır / altyazı başına karakter (iki satır 42'yi aşmadan sığsın)
CUEMAX = 86  # yumuşak altyazı sınırı: 81-86 karakter küçük ceza (iki satır 43'er)
CPS = 17  # okuma hızı hedefi (karakter/sn)
MAXDUR = 6.4  # bir cümle bundan uzun sürerse en az iki altyazıya bölünür (altyazı 7 sn'yi aşmasın)

segs = json.load(open(os.path.join(ROOT, 'senaryo.json')))['segments']
tl = open(os.path.join(ROOT, 'timeline.js')).read()
WORDS = json.loads(re.search(r'window\.WORDS = (\[.*?\]);', tl, re.S).group(1))

def fmt(t):
    ms = int(round(t * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
    return f'{h:02d}:{m:02d}:{s:02d},{ms:03d}'

# ---- dile duyarlı bölme cezaları (kurul/kurgu_tur1/Y-Altyazi.md, kural #2-#4) ----
SOFT = 44  # yumuşak satır sınırı: 43-44 küçük ceza, üstü büyük ceza
DANGLE = set('bir bu şu o en çok daha bütün her hiç ve ama ya da de ki için gibi kadar ile mi mı mu mü'.split())  # satır/altyazı sonunda kalmamalı
ADJNUM = set('ilk son tek aynı başka diğer kendi büyük küçük yeni eski bazı birçok birkaç hangi kaç ne hiçbir iki üç dört beş altı yedi sekiz dokuz on yirmi yüz bin'.split())  # sıfat/sayı + ad ayrılmasın
LEAD = set('kadar gibi için ile mi mı mu mü'.split())  # öncekine bağlı sözcükler satır/altyazı başında yalnız kalmasın
def _low(w): return w.replace('İ', 'i').replace('I', 'ı').lower()
def _core(w): return re.sub(r'[,;:.?!…”“"]+$|^[“"]+', '', w)
def pen_end(w):
    """w sözcüğünden sonra kesmenin cezası (negatif = ödül)"""
    if re.fullmatch(r'[“"]?[A-ZÇĞİÖŞÜ]\.', w): return 200  # "C." gibi tek harfli kısaltmadan sonra kesilmez
    if w[-1] in ',;:.?!…' or w[-2:] in ('.”', '?”', '!”', ',”'): return -25
    c = _low(_core(w)); p = 0
    if c in DANGLE: p += 60
    if c == 'belki': p += 50  # "belki de" ayrılmasın
    if re.search(r"'(n?[ıiuü]n)$", c) or (len(c) >= 6 and re.search(r'n[ıiuü]n$', c)): p += 50  # tamlayan eki
    if c in ADJNUM: p += 40
    return p
CONJ = set('ve ama ki çünkü fakat hem'.split())  # bağlaç ikinci satırı/altyazıyı açabilir
def pen_start(w):
    c = _low(_core(w))
    return 40 if c in LEAD else (-25 if c in CONJ else 0)
def pen_name(prev, nxt):
    """ad-soyad (John|Milton) ayrılmasın"""
    a, b = _core(prev[-1]), _core(nxt[0])
    return 40 if len(prev) >= 2 and a[:1].isupper() and b[:1].isupper() and prev[-1][-1] not in ',;:.?!…' else 0
def open_quote_tail(words, n=4):
    """son n sözcük içinde açılıp kapanmayan açılış tırnağı var mı"""
    tail = words[-n:]
    for i, w in enumerate(tail):
        if '“' in w and '”' not in w[w.index('“'):] and not any('”' in x for x in tail[i + 1:]): return True
    return False
def pen_quote(prev, nxt, n=4):
    """prev | nxt kesmesinde tırnak cezası"""
    p = 0
    if open_quote_tail(prev, n): p += 100  # alıntının başı önceki altyazının/satırın kuyruğuna sıkışmasın
    if '”' in nxt[0] and '“' not in nxt[0]: p += 80  # kapanış tırnağı ilk sözcükte yalnız kalmasın
    return p
def brk_pen(prev, nxt, n=4):
    return max(-30, pen_end(prev[-1]) + pen_start(nxt[0])) + pen_name(prev, nxt) + pen_quote(prev, nxt, n)  # ödüller toplamı -30'u aşmaz
def over_pen(n):
    o = n - MAXL
    return 0 if o <= 0 else 15 * min(o, SOFT - MAXL) + 100 * max(0, n - SOFT)
def wrap2(words):
    """iki satıra dil bilgisine duyarlı böl → (metin, maliyet)"""
    s = ' '.join(words)
    best, bi = (over_pen(len(s)), 0) if len(s) <= SOFT else (1e9, 0)
    if len(s) <= MAXL or len(words) < 2: return s, best
    for i in range(1, len(words)):
        a, b = ' '.join(words[:i]), ' '.join(words[i:])
        cost = abs(len(a) - len(b)) + brk_pen(words[:i], words[i:], 2) + over_pen(len(a)) + over_pen(len(b))
        if cost < best: best, bi = cost, i
    if bi == 0: return s, best
    return ' '.join(words[:bi]) + '\n' + ' '.join(words[bi:]), best
def wrap(words): return wrap2(words)[0]

MERGE = {(sid, tok): n for sid, m in json.load(open(os.path.join(ROOT, 'tools', 'merge.json'))).items() if not sid.startswith('_') for tok, n in m.items()}
cues = []
for sg in segs:
    toks = sg['alt'].split()
    ws = [w for w in WORDS if w['id'] == sg['id']]
    # altyazıda tek sözcük, anlatım zamanlamasında iki sözcük olan kısaltmalar ("Kız ise" → duyulan "Kızsa,")
    for (sid, tok), k in MERGE.items():
        nt = [re.sub(r'[^\w]', '', t_) for t_ in toks]
        if sid == sg['id'] and re.sub(r'[^\w]', '', tok) in nt:
            i = nt.index(re.sub(r'[^\w]', '', tok)); ws = ws[:i] + [{**ws[i], 'e': ws[i + k - 1]['e']}] + ws[i + k:]
    if len(ws) != len(toks):
        print('UYARI: kelime sayısı uyuşmuyor', sg['id'], len(ws), len(toks))
    n = min(len(ws), len(toks))
    # önce cümlelere, uzun cümleleri dengeli parçalara böl (tek kelimelik yetim altyazı kalmasın; virgül tercih edilir)
    sents, cur = [], []
    for i in range(n):
        cur.append(i)
        if i == n - 1 or (toks[i][-1] in '.?!…' and not re.fullmatch(r'[A-ZÇĞİÖŞÜ]\.', toks[i])) or toks[i].endswith('.”') or toks[i].endswith('?”'):
            sents.append(cur); cur = []
    # çok kısa cümleleri (≤ 2 kelime) bir sonrakiyle birleştir
    merged = []
    for sn in sents:
        closing = len(sn) <= 2 and '”' in toks[sn[-1]] and not any('“' in toks[j] for j in sn)  # alıntıyı kapatan kısa cümle ("Bağışlanmaya?”") önceki cümleyle kalır
        if merged and (len(merged[-1]) <= 2 or closing) and len(' '.join(toks[j] for j in merged[-1] + sn)) <= MAXC: merged[-1] += sn
        else: merged.append(sn)
    for sn in merged:
        L = len(' '.join(toks[j] for j in sn))
        k = max(1, -(-L // MAXC))
        dur = ws[sn[-1]]['e'] - ws[sn[0]]['s']
        if dur > MAXDUR: k = max(k, 2)  # çok uzun süren altyazı iki parçaya (":" ya da "," tercih edilir)
        def split(k):
            """k parçaya böl: uzunluk dengesi + dile duyarlı kesme cezası (brk_pen) + satır kırma maliyeti"""
            if k < 2 or len(sn) < 2 * k: return None, 0
            import itertools
            best, parts = 1e9, None
            for cuts in itertools.combinations(range(1, len(sn)), k - 1):
                ps = [sn[a_:b_] for a_, b_ in zip((0,) + cuts, cuts + (len(sn),))]
                tk = [[toks[j] for j in pp] for pp in ps]
                ls = [len(' '.join(t_)) for t_ in tk]
                cost = sum(abs(l - L / k) for l in ls) + sum(15 * (min(l, CUEMAX) - MAXC) for l in ls if l > MAXC) + 200 * sum(max(0, l - CUEMAX) for l in ls)
                cost += 100 * sum(1 for pp in ps if len(pp) < 2)
                cost += sum(brk_pen(tk[q], tk[q + 1]) for q in range(k - 1)) - 5 * sum(1 for q in range(k - 1) if tk[q][-1][-1] == ':')
                cost += sum(wrap2(t_)[1] for t_ in tk)
                cost += sum(40 * max(0, l / (ws[pp[-1]]['e'] - ws[pp[0]]['s'] + .35) - CPS) for l, pp in zip(ls, ps))  # parça okuma hızı 17 kr/sn'yi aşmasın
                if dur > MAXDUR: cost += 30 * sum(1 for pp in ps if ws[pp[-1]]['e'] - ws[pp[0]]['s'] > MAXDUR - .5)
                if cost < best: best, parts = cost, ps
            return parts, best
        parts, best = split(k)
        if parts is not None:  # bir parça fazlası daha iyi kesme veriyorsa (fazladan altyazı bedeli 40) onu seç
            p2, b2 = split(k + 1)
            if p2 is not None and b2 + 40 < best: parts = p2
        if parts is None and L > MAXL:  # tek altyazıda satır kırma bedeli yüksekse (ad-soyad, tamlayan...) ikiye bölmeyi dene
            c1 = wrap2([toks[j] for j in sn])[1]
            p2, b2 = split(2)
            if p2 is not None and b2 + 40 < c1: parts = p2
        if parts is None: parts = [sn]
        for pp in parts:
            cues.append([ws[pp[0]]['s'], ws[pp[-1]]['e'], wrap([toks[j] for j in pp])])

# süreleri düzenle: en az 1.0 sn, cümle sonunda bir sonrakine 80 ms boşluk, cümle ortasında 0 ms, okuma hızı ≤ 17 karakter/sn için
# sonundan en fazla +1,0 sn uzar; yetmezse başı en fazla 0,5 sn öne alınır (yalnız hız aşımını gidermek için; çoğu altyazıda 0) (önceki altyazıyla boşluk korunur)
def gap_after(c):
    """altyazıdan sonra bırakılacak boşluk: cümle ortasında 0 (bitiş = sonrakinin başı), cümle sonunda 80 ms"""
    return .08 if re.search(r'[.?!…]”?$', c[2].replace('\n', ' ')) else 0.0
def settle_times():
    for i, c in enumerate(cues):
        nxt = cues[i + 1][0] if i + 1 < len(cues) else c[1] + 3
        need = len(c[2].replace('\n', ' ')) / CPS
        c[1] = min(max(c[1] + .35, c[0] + 1.0, min(c[0] + need, c[1] + 1.0)), nxt - gap_after(c))
    for i, c in enumerate(cues):
        need = len(c[2].replace('\n', ' ')) / CPS
        if c[1] - c[0] < need:
            prv = cues[i - 1][1] if i else 0.0
            c[0] = max(prv + (gap_after(cues[i - 1]) if i else 0), c[0] - .5, c[1] - need)
raw = [c[:] for c in cues]
settle_times()
# okuma hızı 18 karakter/sn'yi aşan kısa altyazı, sonraki kısa altyazıyla birleşir (sığıyorsa)
i = 0
while i < len(cues) - 1:
    a_, b_ = cues[i], cues[i + 1]
    ta, tb = a_[2].replace('\n', ' '), b_[2].replace('\n', ' ')
    if len(ta) / (a_[1] - a_[0]) > 18 and len(ta) + 1 + len(tb) <= MAXC and raw[i + 1][0] - raw[i][1] < 1.0:
        cues[i] = [raw[i][0], raw[i + 1][1], wrap((ta + ' ' + tb).split())]; raw[i] = [raw[i][0], raw[i + 1][1], '']
        del cues[i + 1]; del raw[i + 1]
        for k, c in enumerate(cues): c[1] = raw[k][1]
        settle_times()
    else: i += 1

out = os.path.join(ROOT, 'ikaros.tr.srt')
with open(out, 'w', encoding='utf-8') as f:
    for i, (a, b, t) in enumerate(cues, 1):
        f.write(f'{i}\n{fmt(a)} --> {fmt(b)}\n{t}\n\n')
print(len(cues), 'altyazı →', out)
