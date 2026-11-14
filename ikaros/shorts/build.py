"""İkaros Shorts: filmden kesitler (9:16) + kelime vurgulu altyazı + ses → shorts/edl.js, edl.json, mix_shorts.wav
python3 shorts/build.py ; sonra: SHORTS=1 node render.js ikaros_shorts.mp4
Kesitler cümle/kelime çapalarıyla (timeline.js); ses audio/mix.wav'dan aynı kesitler (35 ms geçiş)."""
import json, os, re, subprocess
D = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(D)
src = open(os.path.join(R, 'timeline.js'), encoding='utf8').read()
WORDS = json.loads(re.search(r'window\.WORDS = (\[.*?\]);', src, re.S).group(1))
CUES = json.loads(re.search(r'window\.CUES = (\{.*?\});', src, re.S).group(1))
def w(sid, wd, n=0, end=False):
    k = 0
    for x in WORDS:
        if x['id'] == sid and x['w'].startswith(wd):
            if k == n: return x['e'] if end else x['s']
            k += 1
    raise KeyError(f'{sid}@{wd}')
# (film başı, film sonu, kırpma merkezi x [başta, sonda], yakınlık)
SEG = [
  (CUES['A01']['s'] - .25, w('A02', 'güneşe') - .02, (900, 900), 1.0),        # P01: güneşe bakan İkaros (kapak A ile aynı kare)
  (w('A02', 'güneşe') - .02, CUES['A02']['e'] + .2, (980, 900), 1.0),       # P02: dev güneş, yükselen siluet
  (CUES['C05']['s'] - .15, CUES['C05']['e'] + .3, (700, 700), 1.0),         # P15: uyarı afişi
  (CUES['C06']['s'] - .1, 86.84, (1240, 1240), 1.0),   # 86,66–87,02 gerçek duraklama (vo.wav ölçümü)  # P16: tüy dalgada
  (277.45, CUES['G05']['e'] + .4, (900, 1000), 1.0, .5),   # 277,38–277,64 gerçek duraklama  # P47: batan tüyler
  (CUES['G09']['s'] - .15, CUES['G09']['e'] + 1.6, (720, 720), 1.0),        # P52: tek tüy yükselir; sonda kanal çağrısı
]
EDL, t, words = [], 0.0, []
for sg in SEG:
    f0, f1, (c0, c1), z = sg[:4]; tol = sg[4] if len(sg) > 4 else .02
    d = f1 - f0; EDL.append({'s': round(t, 3), 'e': round(t + d, 3), 'f': round(f0, 3), 'cx0': c0, 'cx1': c1, 'z0': z, 'z1': z})
    seg_i = len(EDL) - 1
    for x in WORDS:
        if x['s'] >= f0 - tol and x['s'] <= f1 - .3 and x['e'] <= f1 + .02: words.append({'w': x.get('d') or x['w'], 's': round(max(t, t + x['s'] - f0), 3), 'e': round(t + x['e'] - f0, 3), 'id': x['id'], 'k': seg_i})
    t += d
DUR = round(t, 3)
# altyazı grupları: cümle içinde noktalamada ya da en çok 4 kelimede bölünür
G, cur = [], []
for x in words:
    if cur and cur[-1]['k'] != x['k']: G.append(cur); cur = []
    cur.append(x)
    if len(cur) >= 4 or re.search(r'[.,;:?!”]$', x['w']): G.append(cur); cur = []
if cur: G.append(cur)
GROUPS = [{'s': g[0]['s'], 'e': g[-1]['e'], 'words': [{'w': re.sub(r'[“”]', '', x['w']), 's': x['s'], 'e': x['e']} for x in g]} for g in G]
S = {'TITLE': 'İKAROS · OVİDİUS', 'HOOK': {'l1': 'İKİ UYARI', 'l2': 'VARDI', 'e': EDL[0]['e']}, 'CTA': round(DUR - 1.5, 2), 'DUR': DUR, 'EDL': EDL, 'GROUPS': GROUPS}
json.dump(S, open(os.path.join(D, 'edl.json'), 'w'), ensure_ascii=False, indent=1)
open(os.path.join(D, 'edl.js'), 'w').write('window.SHORT = ' + json.dumps(S, ensure_ascii=False) + ';\n')
# ses
mix = os.path.join(R, 'audio', 'mix.wav'); parts = []
for i, sg in enumerate(SEG):
    f0, f1 = sg[0], sg[1]; parts.append(f"[0:a]atrim={f0:.3f}:{f1:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.035,afade=t=out:st={f1 - f0 - .035:.3f}:d=0.035[a{i}]")
fc = ';'.join(parts) + ';' + ''.join(f'[a{i}]' for i in range(len(SEG))) + f'concat=n={len(SEG)}:v=0:a=1,afade=t=out:st={DUR - 1.2:.2f}:d=1.2[o]'
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', mix, '-filter_complex', fc, '-map', '[o]', '-c:a', 'pcm_s16le', os.path.join(D, 'mix_shorts.wav')], check=True)
print(f'Shorts {DUR:.2f} sn, {len(EDL)} kesit, {len(words)} kelime, {len(GROUPS)} altyazı grubu')
