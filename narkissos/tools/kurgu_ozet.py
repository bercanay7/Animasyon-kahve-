"""Kurgu özeti: her plandan bir kare, yanında plan kimliği, ölçek, set, zaman ve süre (milton/tools/kurgu_ozet.py'nin Narkissos sürümü).
python3 tools/kurgu_ozet.py <çıktı klasörü> [oran=0.5] [--notext] [--sec=P001,P049|regex] [--rs=0.5] [--mb=1]
Sayfa başına 4×5 kare (640×360) → <klasör>/sayfa01.jpg …; ayrıca tek sayfalık 8 sütunlu genel bakış <klasör>/genel.jpg.
--notext: ekran yazısız kareler (sessiz okuma testi; kareler plan listesini görmemiş bir okura verilir, etiketsiz kopyalar <klasör>/kor/)."""
import json, os, subprocess, sys, shutil
from PIL import Image, ImageDraw, ImageFont
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
args = [a for a in sys.argv[1:] if not a.startswith('--')]; flags = [a for a in sys.argv[1:] if a.startswith('--')]
out = os.path.abspath(args[0]); oran = args[1] if len(args) > 1 else '0.5'
kare = os.path.join(out, 'kare'); os.makedirs(kare, exist_ok=True)
subprocess.run(['node', os.path.join(ROOT, 'tools', 'ozet_kare.js'), kare, oran] + flags, cwd=ROOT, check=True)
L = json.load(open(os.path.join(kare, 'liste.json'), encoding='utf-8'))
try:
    f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 19); fs_ = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 15)
except Exception:
    f = fs_ = ImageFont.load_default()
mm = lambda t: f'{int(t // 60)}:{t % 60:04.1f}'
W, H, C, R = 640, 360, 4, 5
for s in range(0, len(L), C * R):
    grp = L[s:s + C * R]
    im = Image.new('RGB', (W * C, (H + 30) * ((len(grp) + C - 1) // C)), (20, 18, 16)); dr = ImageDraw.Draw(im)
    for i, e in enumerate(grp):
        x, y = (i % C) * W, (i // C) * (H + 30)
        im.paste(Image.open(e['dosya']).convert('RGB').resize((W, H), Image.LANCZOS), (x, y + 30))
        dr.text((x + 8, y + 5), f"{e['id']} {e['olcek'] or ''} · {e['set'] or ''}", fill=(240, 220, 150), font=f)
        dr.text((x + W - 8, y + 8), f"{mm(e['t'])} ({e['end'] - e['at']:.1f} sn) {e['tr'] if e['tr'] != 'cut' else ''}", fill=(200, 190, 170), font=fs_, anchor='ra')
    fn = os.path.join(out, f'sayfa{s // (C * R) + 1:02d}.jpg'); im.save(fn, quality=86); print(fn)
# genel bakış: 8 sütun, 240×135
w, h, c = 240, 135, 8; r = (len(L) + c - 1) // c
g = Image.new('RGB', (w * c, (h + 18) * r), (20, 18, 16)); dg = ImageDraw.Draw(g)
for i, e in enumerate(L):
    x, y = (i % c) * w, (i // c) * (h + 18)
    g.paste(Image.open(e['dosya']).convert('RGB').resize((w, h), Image.LANCZOS), (x, y + 18)); dg.text((x + 4, y + 2), f"{e['id']} {e['olcek'] or ''}", fill=(240, 220, 150), font=fs_)
g.save(os.path.join(out, 'genel.jpg'), quality=84); print(os.path.join(out, 'genel.jpg'))
if '--notext' in flags:   # kör okur için etiketsiz, sırası karışık olmayan kopyalar (yalnız sıra numarası)
    kor = os.path.join(out, 'kor'); os.makedirs(kor, exist_ok=True)
    for i, e in enumerate(L): shutil.copy(e['dosya'], os.path.join(kor, f'{i + 1:03d}.jpg'))
    json.dump({f'{i + 1:03d}': e['id'] for i, e in enumerate(L)}, open(os.path.join(out, 'kor_anahtar.json'), 'w'), indent=1); print('kör okur kareleri:', kor)
