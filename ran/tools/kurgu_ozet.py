"""Bütün planlardan kare alıp etiketli özet sayfaları yapar (kurgu kurulu için).
python3 tools/kurgu_ozet.py <çıktı klasörü> [oran=0.5] [set ...]
Her plandan bir kare (plan süresinin `oran` yerinde); sayfa başına 4×5 kare, 640×360."""
import json, re, sys, os, subprocess
from PIL import Image, ImageDraw, ImageFont
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
out = sys.argv[1]; oran = float(sys.argv[2]) if len(sys.argv) > 2 else .5; sets = [a.upper() for a in sys.argv[3:]]
os.makedirs(out, exist_ok=True)
rows = subprocess.run([sys.executable, os.path.join(ROOT, 'tools', 'plan_zaman.py')], capture_output=True, text=True).stdout.strip().split('\n')
P = []
for r in rows:
    m = re.match(r'^(\S+)\s+([\d.]+)\s+([\d.]+) sn\s+(\S+)\s+(\S+)', r)
    if not m: continue
    pid, t, d, st, at = m.group(1), float(m.group(2)), float(m.group(3)), m.group(4), m.group(5)
    if sets and st not in sets: continue
    P.append((pid, t, d, st, at, round(t + d * oran, 2)))
kare = os.path.join(out, 'kare'); os.makedirs(kare, exist_ok=True)
for i in range(0, len(P), 40):
    subprocess.run(['node', 'shot.js', kare] + [f'{p[5]:.2f}' for p in P[i:i + 40]], cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
W, H, C, R = 640, 360, 4, 5
try: f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 20)
except Exception: f = ImageFont.load_default()
for s in range(0, len(P), C * R):
    grp = P[s:s + C * R]
    im = Image.new('RGB', (W * C, (H + 30) * ((len(grp) + C - 1) // C)), (20, 18, 16)); dr = ImageDraw.Draw(im)
    for i, (pid, t, d, st, at, tk) in enumerate(grp):
        x, y = (i % C) * W, (i // C) * (H + 30)
        fn = os.path.join(kare, 't%s.png' % f'{tk:.2f}'.rjust(7, '0'))
        im.paste(Image.open(fn).convert('RGB').resize((W, H), Image.LANCZOS), (x, y + 30))
        dr.text((x + 8, y + 4), f'{pid} {st} {at}  {int(tk // 60)}:{tk % 60:05.2f}  ({d:.1f} sn)', fill=(240, 220, 150), font=f)
    fn = os.path.join(out, f'sayfa{s // (C * R) + 1:02d}.jpg'); im.save(fn, quality=86); print(fn)
