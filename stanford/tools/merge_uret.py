"""tools/merge.json'u üretir: altyazıda tek sözcük, seslendirmede birden çok sözcük (rakamlar yazıyla okunur; 'sarı-kırmızı').
Kullanım: python3 tools/merge_uret.py"""
import json, re, difflib
d = json.load(open('senaryo.json'))
norm = lambda w: re.sub(r"[^\wçğıöşüâîû]+", '', w.lower())
tok = lambda t: [x for x in re.sub(r'\[[^\]]*\]', ' ', t).replace('…', ' ').split() if norm(x)]
out = {"_not": "Altyazıda tek sözcük, seslendirmede birden çok sözcük (tools/merge_uret.py ile üretildi)"}
for s in d['segments']:
    A, T = tok(s['alt']), tok(s['tts'])
    if len(A) == len(T): continue
    sm = difflib.SequenceMatcher(a=[norm(x) for x in A], b=[norm(x) for x in T], autojunk=False)
    m = {}
    for op, a0, a1, b0, b1 in sm.get_opcodes():
        if op == 'equal': continue
        na, nb = a1 - a0, b1 - b0
        if na == nb: continue
        if na == 1: m[A[a0]] = nb
        elif na >= 1 and nb > na:   # birden çok alt sözcük: ilk n-1'i 1'e 1, son sözcük kalanı alır
            for k in range(na - 1): m.setdefault(A[a0 + k], 1)
            m[A[a1 - 1]] = nb - (na - 1)
        else: print('UYARI', s['id'], op, A[a0:a1], T[b0:b1])
    if m: out[s['id']] = m
json.dump(out, open('tools/merge.json', 'w'), ensure_ascii=False, indent=1)
print(json.dumps(out, ensure_ascii=False)[:1500])
