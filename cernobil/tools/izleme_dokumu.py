"""İzleme dökümü: son mp4'ten her ADIM saniyede bir kare + o anın altyazısı ve zaman damgası → sayfa_XX.jpg (5×4 hücre).
Ayrıca her planın ortasından tam boy kare (plan_<id>.jpg, 1280 px) ve plan listesi (planlar.txt).
Kullanım: python3 tools/izleme_dokumu.py film.mp4 çıktı_klasörü [adım=2]"""
import sys, os, re, json, subprocess
from PIL import Image, ImageDraw, ImageFont
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
mp4, out = sys.argv[1], sys.argv[2]; ADIM = float(sys.argv[3]) if len(sys.argv) > 3 else 2.0
os.makedirs(out, exist_ok=True)
dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', mp4], capture_output=True, text=True).stdout)
# altyazı
srt = open(os.path.join(ROOT, 'cernobil.tr.srt'), encoding='utf-8').read().strip().split('\n\n')
def ts(x): h, m, s = x.replace(',', '.').split(':'); return int(h) * 3600 + int(m) * 60 + float(s)
subs = []
for b in srt:
    L = b.split('\n'); a, e = L[1].split(' --> '); subs.append((ts(a), ts(e), ' '.join(L[2:])))
def sub_at(t):
    for a, e, s in subs:
        if a <= t <= e + .3: return s
    return ''
# kareler: tek ffmpeg geçişi, fps=1/ADIM
tmp = os.path.join(out, '_k'); os.makedirs(tmp, exist_ok=True)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', mp4, '-vf', f'fps=1/{ADIM},scale=384:216', os.path.join(tmp, 'k%04d.jpg')], check=True)
files = sorted(os.listdir(tmp))
fn = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13); fb = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 14)
def wrap(s, n=52):
    w, L = s.split(), ['']
    for x in w:
        if len(L[-1]) + len(x) + 1 > n: L.append(x)
        else: L[-1] = (L[-1] + ' ' + x).strip()
    return L[:3]
CW, CH = 384, 216 + 62
for p in range(0, len(files), 20):
    pg = Image.new('RGB', (5 * (CW + 6), 4 * (CH + 6)), 'white'); d = ImageDraw.Draw(pg)
    for i, f in enumerate(files[p:p + 20]):
        t = (p + i) * ADIM + ADIM / 2 if False else (p + i) * ADIM
        X, Y = (i % 5) * (CW + 6), (i // 5) * (CH + 6)
        pg.paste(Image.open(os.path.join(tmp, f)), (X, Y))
        d.text((X + 4, Y + 219), '%d:%04.1f' % (int(t) // 60, t % 60), fill=(170, 0, 0), font=fb)
        for k, l in enumerate(wrap(sub_at(t))): d.text((X + 70, Y + 219 + k * 15), l, fill=(20, 20, 20), font=fn)
    pg.save(os.path.join(out, 'sayfa_%02d.jpg' % (p // 20 + 1)), quality=84)
for f in files: os.remove(os.path.join(tmp, f))
os.rmdir(tmp)
print('sayfa', (len(files) + 19) // 20, 'kare', len(files), 'süre', round(dur, 1))
