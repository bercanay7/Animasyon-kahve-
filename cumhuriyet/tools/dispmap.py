"""Altyazı sözcüklerini (alt) seslendirme sözcüklerine (tts) eşler. Rakamla yazılan sayılar ("1923")
seslendirmede birkaç sözcüktür ("bin dokuz yüz yirmi üç"); görünen sözcük grubun ilk sözcüğüne yazılır,
grubun öbür sözcüklerine '' düşer. disp_map(alt, tts_sozcukleri) → tts ile aynı uzunlukta liste."""
import re, difflib
U = ['', 'bir', 'iki', 'üç', 'dört', 'beş', 'altı', 'yedi', 'sekiz', 'dokuz']
T = ['', 'on', 'yirmi', 'otuz', 'kırk', 'elli', 'altmış', 'yetmiş', 'seksen', 'doksan']
def tr_num(n):
    if n == 0: return ['sıfır']
    w = []
    if n >= 1000:
        k = n // 1000; w += (['bin'] if k == 1 else tr_num(k) + ['bin']); n %= 1000
    if n >= 100:
        h = n // 100; w += (['yüz'] if h == 1 else [U[h], 'yüz']); n %= 100
    if n >= 10: w.append(T[n // 10]); n %= 10
    if n: w.append(U[n])
    return w
norm1 = lambda w: re.sub(r"[^\wçğıöşüâî]+", '', w.lower().replace('İ', 'i').replace('I', 'ı').replace("'", '').replace('’', '').replace('â', 'a').replace('î', 'i').replace('û', 'u'))
def alt_tokens(alt):
    return [x for x in re.sub(r'\[[^\]]*\]', ' ', alt).replace('…', '… ').split() if norm1(x)]
def disp_map(alt, ref):
    toks = alt_tokens(alt)
    ex, own = [], []
    for k, tk in enumerate(toks):
        m = re.match(r'^\D*?(\d+)', tk)
        ws = tr_num(int(m.group(1))) if m else [norm1(tk)]
        ex += ws; own += [k] * len(ws)
    o = [None] * len(ref)
    for tag, a0, a1, b0, b1 in difflib.SequenceMatcher(None, ex, ref, autojunk=False).get_opcodes():
        if tag in ('equal', 'replace'):
            for j in range(b0, b1):
                o[j] = own[a0 + min(a1 - a0 - 1, (j - b0) * (a1 - a0) // max(1, b1 - b0))]
    for j in range(len(ref)):  # fazladan seslendirme sözcüğü: önceki gruba katılır
        if o[j] is None: o[j] = o[j - 1] if j else 0
    for j in range(1, len(ref)):  # gruplar geri gitmez
        o[j] = max(o[j], o[j - 1])
    out, seen = [], set()
    for j in range(len(ref)):
        if o[j] in seen: out.append('')
        else: seen.add(o[j]); out.append(toks[o[j]] if o[j] < len(toks) else '')
    # eşlenemeyen alt sözcükleri bir öncekine eklenir (kaybolmasın)
    missing = [k for k in range(len(toks)) if k not in seen]
    for k in missing:
        j = max([i for i in range(len(ref)) if out[i] and toks.index(out[i]) < k] or [0])
        out[j] = (out[j] + ' ' + toks[k]).strip()
    return out
