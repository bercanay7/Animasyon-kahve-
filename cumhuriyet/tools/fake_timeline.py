"""Seslendirme gelmeden önce geçici zaman çizelgesi: kelime süreleri harf sayısından tahmin edilir.
Animasyon çekimleri S()/Wd() ile cümlelere bağlı olduğu için, gerçek vo geldiğinde build_vo.py timeline.js'i
yeniden yazar ve görüntü kendiliğinden kayar.  Kullanım: python3 tools/fake_timeline.py"""
import json, re, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
d = json.load(open(os.path.join(ROOT, 'senaryo.json')))
pp = os.path.join(ROOT, 'vo', 'plan.json')
plan = json.load(open(pp)) if os.path.exists(pp) else {'once': 1.0, 'gap': {}, 'secGap': 1.2, 'sonra': 12.0}
norm1 = lambda w: re.sub(r"[^\wçğıöşüâî]+", '', w.lower().replace('İ', 'i').replace('I', 'ı').replace("'", '').replace('’', '').replace('â', 'a').replace('î', 'i').replace('û', 'u'))
CPS = 14.5  # konuşma hızı: saniyede harf (Emrullah, Sisifos ortalaması)
t = plan.get('once', 1.0); cues = {}; words = []; prev = None
for s in d['segments']:
    if prev is not None and prev != s['bolum']: t += plan.get('secGap', 1.2)
    prev = s['bolum']
    txt = re.sub(r'\[[^\]]*\]', ' ', s['tts'])
    disp = [x for x in re.sub(r'\[[^\]]*\]', ' ', s['alt']).replace('…', ' ').split() if norm1(x)]
    s0 = t
    for k, raw in enumerate(x for x in txt.replace('…', ' … ').split()):
        if raw == '…': t += .45; continue
        w = norm1(raw)
        if not w: continue
        dur = max(.16, len(w) / CPS)
        words.append({'id': s['id'], 'w': w, 'd': disp[len([x for x in words if x['id'] == s['id']])] if len([x for x in words if x['id'] == s['id']]) < len(disp) else w, 's': round(t, 3), 'e': round(t + dur, 3)})
        t += dur + .06
        if raw[-1] in '.!?:': t += .32
        elif raw[-1] in ',;': t += .16
    cues[s['id']] = {'s': round(s0, 3), 'e': round(t, 3), 'sec': 0}
    t += plan.get('gap', {}).get(s['id'], .45)
t += plan.get('sonra', 12.0)
open(os.path.join(ROOT, 'timeline.js'), 'w').write('// tools/fake_timeline.py (GEÇİCİ tahmin)\nwindow.CUES = ' + json.dumps(cues) + ';\nwindow.WORDS = ' + json.dumps(words, ensure_ascii=False) + ';\nwindow.DUR = ' + str(round(t, 3)) + ';\n')
print('tahmini süre', round(t, 1), 'sn =', f'{int(t // 60)}:{t % 60:04.1f}')
