"""Çekimleri senaryoya karşı karakter düzeyinde karşılaştırır; Whisper'ın yazım bölmelerini (Zeus 'un, ön sözünde)
ve sayı yazımını (1967'de ↔ bin dokuz yüz altmış yedide) hata saymaz. Kalan farkları cümle kimliği ve zamanıyla listeler.
Kullanım: python3 tools/karsilastir.py  → vo/karsilastirma.json + ekrana bölüm bölüm özet"""
import json, re, difflib, glob, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
low = lambda s: s.replace('İ', 'i').replace('I', 'ı').lower().replace('â', 'a').replace('î', 'i').replace('û', 'u')
clean = lambda s: re.sub(r"[^\wçğıöşü]+", '', low(s).replace("'", '').replace('’', ''))

def merge_tokens(hw):
    """Kesme işaretiyle başlayan Whisper parçalarını önceki kelimeye ekler."""
    out = []
    for w in hw:
        if out and w['w'][:1] in "'’": out[-1] = {**out[-1], 'w': out[-1]['w'] + w['w'], 'e': w['e']}
        else: out.append(dict(w))
    return out

d = json.load(open(os.path.join(ROOT, 'senaryo.json')))
secs = {}
for s in d['segments']: secs.setdefault(s['bolum'], []).append(s)
onek = {b['onek']: b['ad'] for b in json.load(open(os.path.join(ROOT, 'vo', 'bolumler.json')))}
res = {}
for wj in sorted(glob.glob(os.path.join(ROOT, 'vo', 's[0-9][0-9]_[ab].words.json'))):
    key = os.path.basename(wj).split('.')[0]; segs = secs[onek[key[:3]]]
    hw = merge_tokens(json.load(open(wj)))
    # referans karakter dizisi ve her karakterin sahibi (cümle kimliği)
    ref, rown = '', []
    for s in segs:
        c = clean(re.sub(r'\[[^\]]*\]', ' ', s['tts'])); ref += c; rown += [s['id']] * len(c)
    hyp, hpos = '', []
    for w in hw:
        c = clean(w['w']); hyp += c; hpos += [w['s']] * len(c)
    # rakamlar: Whisper rakam yazdıysa okunuşla eşleştirmek için hata saymayacağız (aşağıda süzülür)
    sm = difflib.SequenceMatcher(None, ref, hyp, autojunk=False)
    errs, bad = [], 0
    for op, a, b, c, e in sm.get_opcodes():
        if op == 'equal': continue
        rs, hs = ref[a:b], hyp[c:e]
        if re.search(r'\d', hs): continue
        bad += max(b - a, e - c)
        sid = rown[min(a, len(rown) - 1)]
        t0 = hpos[min(c, len(hpos) - 1)] if hpos else 0
        ctxr = ref[max(0, a - 12):b + 12]; ctxh = hyp[max(0, c - 12):e + 12]
        errs.append({'id': sid, 't': round(t0, 2), 'ref': rs, 'hyp': hs, 'bag_ref': ctxr, 'bag_hyp': ctxh})
    res[key] = {'cer': round(bad / max(1, len(ref)), 4), 'sure': hw[-1]['e'] if hw else 0, 'farklar': errs}
json.dump(res, open(os.path.join(ROOT, 'vo', 'karsilastirma.json'), 'w'), ensure_ascii=False, indent=1)
for k, v in res.items():
    print(f"{k}  CER {v['cer']:.3f}  {v['sure']:.1f} sn  fark {len(v['farklar'])}")
    for e in v['farklar']: print(f"    {e['id']:5} {e['t']:7.2f}  {e['ref']!r:22} → {e['hyp']!r:22}  [{e['bag_ref']} | {e['bag_hyp']}]")
