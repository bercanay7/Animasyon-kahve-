"""Shorts (1080×1920): ana filmden kesitler + kâğıt zemin + üstte kanca + altta kelime gruplu altyazı.
python3 shorts/yap.py  (girdi: teslim/ran_ana.mp4, audio/mix.wav; çıktı: teslim/ran_shorts.mp4)
EDL: en güçlü kare (yanan kale) ve cümle ilk saniyede; cevap ve iki soru sonda. Toplam ~28 sn."""
import json, re, subprocess, os
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); P = lambda *a: os.path.join(R, *a)
tl = open(P('timeline.js'), encoding='utf-8').read()
C = json.loads(tl.split('window.CUES = ')[1].split(';\n')[0]); WORDS = json.loads(tl.split('window.WORDS = ')[1].split(';\n')[0])
SEG = json.load(open(P('senaryo.json'), encoding='utf-8'))['segments']; ALT = {s['id']: s['alt'] for s in SEG}
# (cümleler, kırpma x0 [1440×1080 pencerenin solu])
EDL = [(['A01'], 380), (['E05'], 260), (['H08'], 400), (['H09'], 240)]
HOOK = 'YAPTIKLARIN SANA DÖNER Mİ?'
segs, t = [], 0.0
for ids, x0 in EDL:
    a = C[ids[0]]['s'] - .35; b = C[ids[-1]]['e'] + .45
    segs.append(dict(a=a, b=b, x0=x0, t0=t, ids=ids)); t += b - a
DUR = t
# altyazı: cümlenin kelimelerini ≤ 26 karakterlik gruplara böl (görünen biçim alt metinden)
cues = []
for s in segs:
    for sid in s['ids']:
        ws = [w for w in WORDS if w['id'] == sid]; disp = ALT[sid].split()
        if len(disp) != len(ws): disp = [w['d'] for w in ws]
        grp, cur = [], []
        for w, d in zip(ws, disp):
            if cur and len(' '.join(x[1] for x in cur) + ' ' + d) > 26: grp.append(cur); cur = []
            cur.append((w, d))
        if cur: grp.append(cur)
        for g in grp:
            cues.append(dict(s=g[0][0]['s'] - s['a'] + s['t0'], e=g[-1][0]['e'] - s['a'] + s['t0'] + .15, txt=' '.join(x[1] for x in g)))
for i in range(len(cues) - 1): cues[i]['e'] = min(cues[i]['e'], cues[i + 1]['s'])
json.dump(dict(DUR=DUR, segs=segs, cues=cues, hook=HOOK), open(P('shorts', 'edl.json'), 'w'), ensure_ascii=False, indent=1)
# 1) taban: kesitleri kırp, ölçekle, kâğıt zemine koy (video 1080×810, y=470)
tmp = P('shorts', '_parca'); os.makedirs(tmp, exist_ok=True); parts = []
for i, s in enumerate(segs):
    o = os.path.join(tmp, f'p{i}.mp4'); parts.append(o)
    vf = f"crop=1440:1080:{s['x0']}:0,scale=1080:810,pad=1080:1920:0:470:color=0xece4d2,fps=30"
    af = f"afade=t=in:d=.15,afade=t=out:st={s['b']-s['a']-.25:.2f}:d=.25"
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-ss', f"{s['a']:.3f}", '-t', f"{s['b']-s['a']:.3f}", '-i', P('teslim', 'ran_ana.mp4'), '-ss', f"{s['a']:.3f}", '-t', f"{s['b']-s['a']:.3f}", '-i', P('audio', 'mix.wav'),
                    '-map', '0:v', '-map', '1:a', '-vf', vf, '-af', af, '-c:v', 'libx264', '-crf', '16', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-c:a', 'pcm_s16le', '-ar', '48000', o], check=True)
open(os.path.join(tmp, 'liste.txt'), 'w').write('\n'.join(f"file '{p}'" for p in parts))
base = os.path.join(tmp, 'taban.mov')
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', os.path.join(tmp, 'liste.txt'), '-c:v', 'libx264', '-crf', '16', '-pix_fmt', 'yuv420p', '-c:a', 'pcm_s16le', base], check=True)
# 2) yazı katmanları (tarayıcıda çizilir: Türkçe karakterli fontlar) → PNG'ler
subprocess.run(['node', P('shorts', 'yazi.js')], check=True)
# 3) bindir: her PNG kendi zaman aralığında
ins, flt, last = ['-i', base], [], '[0:v]'
pngs = json.load(open(os.path.join(tmp, 'yazi.json')))
for k, (f, a, b) in enumerate(pngs):
    ins += ['-i', f]; flt.append(f"{last}[{k+1}:v]overlay=0:0:enable='between(t,{a:.3f},{b:.3f})'[v{k}]"); last = f'[v{k}]'
out = P('teslim', 'ran_shorts.mp4')
subprocess.run(['ffmpeg', '-y', '-v', 'error', *ins, '-filter_complex', ';'.join(flt), '-map', last, '-map', '0:a', '-c:v', 'libx264', '-crf', '18', '-preset', 'slow', '-pix_fmt', 'yuv420p',
                '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-af', 'loudnorm=I=-14:TP=-1.5', '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-metadata:s:a:0', 'language=tur', '-movflags', '+faststart', out], check=True)
print('Shorts:', out, round(DUR, 2), 'sn,', len(cues), 'altyazı')
