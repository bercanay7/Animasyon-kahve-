"""Kapak ve kapak kurulu test seti.
Kullanım: python3 tools/kapak_seti.py <çıktı-klasörü>
- prometheus/kapak.jpg (A) ve kapak_b.jpg (B): 1280×720 JPG, < 2 MB
- test seti (her kapak için): tam boy, 246×138 ve 168×94 küçültmeler, bulanık (odak noktası), gri değer,
  sağ altta süre rozeti, mobil akış taklidi (kanalın Sisifos ve Orfeus kapaklarıyla yan yana)"""
import sys, os, subprocess
from PIL import Image, ImageOps, ImageFilter, ImageDraw, ImageFont
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); ROOT = os.path.dirname(R)
out = sys.argv[1]; os.makedirs(out, exist_ok=True)
tmp = os.path.join(out, '_kare'); os.makedirs(tmp, exist_ok=True)
FONT = os.path.join(R, 'fonts')
def font(sz, bold=True):
    for f in ['/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf' if bold else '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']:
        if os.path.exists(f): return ImageFont.truetype(f, sz)
    return ImageFont.load_default()
covers = {}
for key, scene, fn in [('A', 'kapakA', 'kapak.jpg'), ('B', 'kapakB', 'kapak_b.jpg')]:
    d = os.path.join(tmp, key); os.makedirs(d, exist_ok=True)
    subprocess.run(['node', os.path.join(R, 'shot.js'), d, '2'], env={**os.environ, 'SCENE': scene, 'MB': '1'}, check=True, capture_output=True)
    im = Image.open(os.path.join(d, 't0002.00.png')).convert('RGB').resize((1280, 720), Image.LANCZOS)
    path = os.path.join(R, fn); im.save(path, quality=92, optimize=True)
    print(fn, round(os.path.getsize(path) / 1e6, 2), 'MB')
    covers[key] = im
    im.save(os.path.join(out, f'{key}_1280.jpg'), quality=92)
    im.resize((246, 138), Image.LANCZOS).save(os.path.join(out, f'{key}_246.png'))
    im.resize((168, 94), Image.LANCZOS).save(os.path.join(out, f'{key}_168.png'))
    im.resize((320, 180), Image.LANCZOS).filter(ImageFilter.GaussianBlur(6)).resize((640, 360)).save(os.path.join(out, f'{key}_bulanik.png'))
    ImageOps.grayscale(im).save(os.path.join(out, f'{key}_gri.png'))
    # süre rozeti (YouTube sağ alt): rozet bölgesi boş mu?
    b = im.copy(); dr = ImageDraw.Draw(b); dr.rounded_rectangle((1168, 668, 1266, 706), 6, fill=(0, 0, 0)); dr.text((1180, 672), '23:55', fill='white', font=font(28))
    b.save(os.path.join(out, f'{key}_rozet.jpg'), quality=88)
# mobil akış taklidi: 390 px genişlikte telefon, üç video alt alta (kapak 358×201, başlık iki satır)
others = [('Sisifos', os.path.join(ROOT, 'sisifos', 'kapak.png'), "Sisifos'u Neden Mutlu Hayal Etmeliyiz? | Camus ve Absürt"),
          ('Orfeus', os.path.join(ROOT, 'orfeus', 'kapak_final_A_arkana_bakma.jpg'), 'Orfeus ve Evridiki: Ölüleri İkna Etti, Kendini Durduramadı')]
for key, im in covers.items():
    W, item = 390, 201 + 86
    feed = Image.new('RGB', (W, 16 + item * 3), (15, 15, 15)); dr = ImageDraw.Draw(feed)
    rows = [(others[0][1], others[0][2]), (None, 'Prometheus: Asıl Tutsak Kimdi? | Aiskhylos ve Azra Erhat'), (others[1][1], others[1][2])]
    for i, (p, title) in enumerate(rows):
        y = 8 + i * item
        th = (im if p is None else Image.open(p).convert('RGB')).resize((358, 201), Image.LANCZOS)
        feed.paste(th, (16, y)); dr.rounded_rectangle((16 + 358 - 54, y + 201 - 26, 16 + 358 - 6, y + 201 - 6), 4, fill=(0, 0, 0))
        dr.ellipse((16, y + 212, 52, y + 248), fill=(90, 60, 40)); dr.text((62, y + 210), title[:38], fill=(240, 240, 240), font=font(15)); dr.text((62, y + 232), title[38:76], fill=(240, 240, 240), font=font(15))
        dr.text((62, y + 256), 'Zaman Kuryesi · 1 B görüntüleme', fill=(170, 170, 170), font=font(13))
    feed.save(os.path.join(out, f'{key}_akis.png'))
# yan yana karşılaştırma
cmp = Image.new('RGB', (1280, 360)); cmp.paste(covers['A'].resize((640, 360)), (0, 0)); cmp.paste(covers['B'].resize((640, 360)), (640, 0)); cmp.save(os.path.join(out, 'AB.jpg'), quality=88)
print('test seti →', out)
