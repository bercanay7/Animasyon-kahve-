"""img/ klasöründeki arşiv fotoğraflarını ve imzayı assets.js'e gömer (file:// altında canvas kirlenmesin diye).
Çalıştırma: python3 assets.py"""
import base64, json, re, pathlib

here = pathlib.Path(__file__).parent
photos = {k: 'data:image/jpeg;base64,' + base64.b64encode((here / 'img' / f'{k}.jpg').read_bytes()).decode()
          for k in ('cankaya', 'meclis', '1925')}
svg = (here / 'img' / 'imza.svg').read_text()
sig = re.search(r'\sd="([^"]+)"', svg).group(1)
w, h = (float(re.search(fr'\s{a}="([\d.]+)"', svg).group(1)) for a in ('width', 'height'))
(here / 'assets.js').write_text(
    '// Arşiv fotoğrafları (Wikimedia Commons, kamu malı) ve Atatürk imzası. assets.py ile üretilir.\n'
    f'window.PHOTOS = {json.dumps(photos)};\n'
    f'window.IMZA = {json.dumps({"d": sig, "w": w, "h": h})};\n')
print('assets.js yazıldı')
