"""Seslendirme gelmeden önce tahmini zaman çizelgesi: python3 tools/gecici_zaman.py
senaryo.json'daki 'alt' metninden kelime başına ~0,43 sn, cümle arası 0,7 sn, bölüm arası 1,4 sn. timeline.js'i yazar (GEÇİCİ işaretli).
Gerçek çizelge tools/build_vo.py ile gelir; görüntü kelimelere bağlı olduğu için kendiliğinden kayar."""
import json, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
segs = json.load(open(os.path.join(ROOT, 'senaryo.json'), encoding='utf-8'))['segments']
t, b, CUES, WORDS = .6, None, {}, []
for k, s in enumerate(segs):
    if b is not None and s['bolum'] != b: t += .7
    b = s['bolum']
    ws = s['alt'].split(); s0 = t
    for w in ws:
        d = .2 + .055 * len(re.sub(r'\W', '', w)) + (.25 if w[-1] in '.,;:?!”' else 0)
        WORDS.append({'id': s['id'], 'w': re.sub(r'[^\wçğıöşüâîû]', '', w.lower().replace('I', 'ı').replace('İ', 'i')), 's': round(t, 3), 'e': round(t + d - .04, 3)})
        t += d
    CUES[s['id']] = {'s': round(s0, 3), 'e': round(t, 3), 'sec': k}
    t += .7
DUR = round(t + 2.5, 2)
open(os.path.join(ROOT, 'timeline.js'), 'w', encoding='utf-8').write(
    '// GEÇİCİ: tools/gecici_zaman.py (seslendirme yok, tahmini)\n'
    f'window.CUES = {json.dumps(CUES, ensure_ascii=False)};\nwindow.WORDS = {json.dumps(WORDS, ensure_ascii=False)};\nwindow.DUR = {DUR};\n')
print(f'{len(segs)} cümle, {len(WORDS)} kelime, DUR {DUR} sn ({DUR/60:.1f} dk)')
