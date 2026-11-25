#!/usr/bin/env python3
"""Seslendirmeden önce tahmini zaman çizelgesi (timeline.js): her cümle tts karakterine göre (14,5 kr/sn), cümle arası 0,45 sn, bölüm arası 1,5 sn.
Seslendirme gelince tools/build_vo.py bu dosyayı gerçeğiyle değiştirir. Kelime kökleri Python lower() ile (build_vo ile aynı)."""
import json, re, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
segs = json.load(open(os.path.join(ROOT, 'senaryo.json')))['segments']
t = .4; cues = {}; words = []; prev = None; sec = -1
for s in segs:
    if s['bolum'] != prev: sec += 1; t += (1.5 if prev else 0); prev = s['bolum']
    txt = re.sub(r'\[[^\]]*\]\s*', '', s['tts'])
    ws = txt.split(); dur = len(txt) / 14.5; per = dur / max(1, len(txt))
    st = t
    for w in ws:
        wd = (len(w) + 1) * per
        k = re.sub(r"[^\wçğıöşü]", '', w.lower().replace('â', 'a').replace('î', 'i').replace('û', 'u'))
        if k: words.append({'id': s['id'], 'w': k, 's': round(t, 3), 'e': round(t + wd * .9, 3)})
        t += wd
    cues[s['id']] = {'s': round(st, 3), 'e': round(t, 3), 'sec': sec}
    t += .45
t += 14
open(os.path.join(ROOT, 'timeline.js'), 'w').write('// TAHMİNİ (tools/tahmini_timeline.py); seslendirmeden sonra tools/build_vo.py yazar\nwindow.CUES = ' + json.dumps(cues) + ';\nwindow.WORDS = ' + json.dumps(words, ensure_ascii=False) + ';\nwindow.DUR = ' + str(round(t, 3)) + ';\n')
print('DUR', round(t, 1))
