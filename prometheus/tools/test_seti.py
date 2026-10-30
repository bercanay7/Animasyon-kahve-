"""Kurul test seti: bir deneme sahnesinden tam boy kare, 246×138 ve 168×94 küçültmeler, gri değer,
ayrıntı kırpıntıları ve hareket şeridi üretir.
Kullanım: python3 tools/test_seti.py <çıktı-klasörü> <sahne> <ana-zaman> <şerit zamanları,virgülle> [kırp=x0,y0,x1,y1:ad ...]"""
import sys, os, subprocess, glob
from PIL import Image, ImageOps
out, scene, t0, strip = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4].split(',')
crops = [a.split(':') for a in sys.argv[5:]]
os.makedirs(out, exist_ok=True)
tmp = os.path.join(out, '_kare'); os.makedirs(tmp, exist_ok=True)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
subprocess.run(['node', os.path.join(ROOT, 'shot.js'), tmp, t0] + strip, env={**os.environ, 'SCENE': scene, 'MB': '4'}, check=True, capture_output=True)
fn = lambda t: os.path.join(tmp, f't{float(t):.2f}'.replace('t', 't' + '0' * (7 - len(f'{float(t):.2f}'))) + '.png')
main = Image.open(fn(t0)).convert('RGB')
main.save(os.path.join(out, 'uslup_karesi.png'))
main.resize((246, 138), Image.LANCZOS).save(os.path.join(out, 'kucuk_246.png'))
main.resize((168, 94), Image.LANCZOS).save(os.path.join(out, 'kucuk_168.png'))
ImageOps.grayscale(main).save(os.path.join(out, 'gri.png'))
for box, name in crops:
    x0, y0, x1, y1 = map(int, box.split(',')); main.crop((x0, y0, x1, y1)).save(os.path.join(out, f'kirp_{name}.png'))
fr = [Image.open(fn(t)).convert('RGB').resize((640, 360), Image.LANCZOS) for t in strip]
st = Image.new('RGB', (640 * len(fr), 360))
for i, f in enumerate(fr): st.paste(f, (640 * i, 0))
st.save(os.path.join(out, 'hareket_seridi.png'))
for f in glob.glob(os.path.join(tmp, '*.png')): os.remove(f)
os.rmdir(tmp)
print('test seti →', out)
