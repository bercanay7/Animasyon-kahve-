"""Erdem Melih logosunu Instagram profil ekran görüntüsünden ayıklar ve büyütür.
Çıktılar: logo/em_logo_beyaz.png (şeffaf zemin, beyaz), logo/em_rozet.png (siyah daire rozet).
Kullanım: python3 tools/logo_temizle.py <ekran_goruntusu.png> <cikti_klasoru>"""
import sys
import numpy as np
from PIL import Image, ImageFilter

src, out = sys.argv[1], sys.argv[2]
im = Image.open(src).convert("L")
a = np.asarray(im).astype(np.float32)
# Siyah dairenin sınırları (koyu piksel taraması)
ys, xs = np.where(a < 9)
cy0 = a.shape[0] // 2
band = (ys > 500) & (ys < a.shape[0] - 500)
ys, xs = ys[band], xs[band]
x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
cx, cy, r = (x0 + x1) / 2, (y0 + y1) / 2, (x1 - x0) / 2
print("daire", cx, cy, r)
S = 5  # büyütme
crop = im.crop((int(cx - r), int(cy - r), int(cx + r), int(cy + r)))
big = crop.resize((crop.width * S, crop.height * S), Image.LANCZOS)
big = big.filter(ImageFilter.GaussianBlur(S * 0.55))
L = np.asarray(big).astype(np.float32) / 255.0
# Daire dışını ve kenar halkasını sil
h, w = L.shape
yy, xx = np.mgrid[0:h, 0:w]
rr = np.hypot(xx - w / 2, yy - h / 2)
L[rr > (r - 10) * S] = 0
# Kontrast eğrisi: koyu zemin 0, beyaz harfler 1, gri süsler yarı saydam kalır
lo, hi = 0.10, 0.62
A = np.clip((L - lo) / (hi - lo), 0, 1)
A = A * A * (3 - 2 * A)  # smoothstep: keskin ama kenar yumuşatmalı
alpha = (A * 255).astype(np.uint8)
white = np.full((h, w, 3), 255, np.uint8)
logo = Image.fromarray(np.dstack([white, alpha]), "RGBA")
bbox = logo.getbbox()
logo.crop(bbox).save(f"{out}/em_logo_beyaz.png")
# Rozet: siyah daire + logo
rozet = Image.new("RGBA", (w, h), (0, 0, 0, 0))
disk = Image.fromarray(((rr <= (r - 2) * S) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.5))
rozet.paste((8, 8, 8, 255), (0, 0), disk)
rozet.alpha_composite(logo)
rozet.save(f"{out}/em_rozet.png")
print("boyut", logo.crop(bbox).size, rozet.size)
