"""Kalite kontrol: out/emu_savasi.mp4 → boş kare, HUD, yazısız seri, ilk/son kare, hareket, kontak sayfaları."""
import subprocess
import numpy as np
from PIL import Image, ImageDraw
import cues, ui
from engine import W, H, FPS

VID = "out/Emu_Savasi.mp4"
SW, SH = 270, 480
NF = int(round(cues.T * FPS))

def decode_small():
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", VID, "-vf", f"scale={SW}:{SH}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, SH, SW, 3)

fr = decode_small()
print("kare sayısı:", len(fr), "(beklenen", NF, ")")
lum = fr.mean(axis=(1, 2, 3)); sd = fr.std(axis=(1, 2, 3))
print(f"1) BOŞ/SİYAH KARE: min parlaklık {lum.min():.0f}, min kontrast {sd.min():.1f}; parlaklık<40: {(lum<40).sum()}")
# içerik yoğunluğu: koyu piksel oranı (kağıt zeminde çizgi/metin yoksa 'boş' sayılır)
dark = (fr.mean(axis=3) < 120).mean(axis=(1, 2))
print(f"   çizgi/yazı yoğunluğu min {dark.min()*100:.2f}% (kare {dark.argmin()}), <%0.8 olan kare: {(dark<0.008).sum()}")
# HUD: kutu bölgesi koyu çerçeve + metin
y0, y1, x0, x1 = 206//4, 318//4, 250//4, 830//4
reg = fr[:, y0:y1, x0:x1, :].mean(axis=3)
hud = (reg < 110).mean(axis=(1, 2))
print(f"2) MERMİ SAYACI (HUD) her karede: koyu piksel oranı min {hud.min()*100:.1f}% (kare {hud.argmin()}), <%1.5 olan kare: {(hud<0.015).sum()} / {len(fr)}")
# yazısız seri: sayfa süreleri
def visible(t):
    for i, p in enumerate(ui.PAGES):
        t0 = p[0]["t0"] - 0.03
        t1 = (ui.PAGES[i+1][0]["t0"] - 0.03) if i + 1 < len(ui.PAGES) else cues.CAP_END
        if t0 + 0.02 <= t < t1:
            return True
    return False
vis = [visible(i / FPS) and (i / FPS) < cues.FINAL_T for i in range(NF)]
best = cur = 0
for v in vis + vis:
    cur = 0 if v else cur + 1
    best = max(best, cur)
best = min(best, NF)
print(f"3) EN UZUN YAZISIZ SERİ (döngü dahil): {best} kare = {best/FPS:.3f} sn (sınır 0.3)")
a = fr[0].astype(np.float32); b = fr[-1].astype(np.float32)
print(f"4) İLK vs SON KARE: ort. fark {np.abs(a-b).mean():.3f}, PSNR {10*np.log10(255**2/max(1e-9,((a-b)**2).mean())):.1f} dB")
import compose
ia = np.asarray(compose.render_frame(0)); ib = np.asarray(compose.render_frame(NF - 1))
print(f"   ham render farkı max {np.abs(ia.astype(int)-ib.astype(int)).max()} (0 = birebir aynı)")
d = np.abs(np.diff(fr.astype(np.int16), axis=0)).mean(axis=(1, 2, 3))
win = int(2.0 * FPS); low = []
for s in range(0, NF - win, 6):
    if d[s:s + win].max() < 1.2:
        low.append(round(s / FPS, 1))
print(f"5) 2 sn'lik pencerede belirgin görsel değişim olmayan başlangıçlar: {low if low else 'yok'}")
print("   saniyelik hareket:", " ".join(f"{d[i*FPS:(i+1)*FPS].mean():.1f}" for i in range(int(cues.T))))
# alt güvenli alan: altyazı + içerik y<1440 (alt %25 = 1440+) → 1440 altında koyu piksel oranı
low_zone = (fr[:, int(1440/4):, :, :].mean(axis=3) < 100).mean(axis=(1, 2))
print(f"6) ALT %25 (y>1440) çizgi/yazı oranı: ort {low_zone.mean()*100:.2f}%  maks {low_zone.max()*100:.2f}% (içerik üst bölgede kalmalı)")

tw, th = 180, 320
scenes = [("A", [0.0, 1.0, 2.6]), ("B", [3.8, 4.6, 5.2]), ("C", [6.6, 7.8, 8.8]), ("D", [10.3, 11.4, 12.6]), ("E", [13.8, 14.8, 15.8]),
          ("F", [17.4, 18.6, 19.9]), ("G", [21.8, 23.0, 24.2]), ("H", [25.6, 26.4, 27.0]), ("I", [28.5, 29.8, 30.8]), ("J", [32.3, 34.0, 36.6]),
          ("K", [38.4, 39.2, 39.9])]
sheet = Image.new("RGB", (6 * tw, 6 * th), (20, 20, 20)); dr = ImageDraw.Draw(sheet)
k = 0
for name, ts in scenes:
    for t in ts:
        raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-ss", f"{t}", "-i", VID, "-frames:v", "1", "-vf", f"scale={tw}:{th}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                             capture_output=True).stdout
        im = Image.frombytes("RGB", (tw, th), raw)
        x, y = (k % 6) * tw, (k // 6) * th
        sheet.paste(im, (x, y)); dr.rectangle([x, y, x + 62, y + 13], fill=(0, 0, 0)); dr.text((x + 2, y + 1), f"{name} {t:.1f}s", fill=(255, 255, 0)); k += 1
sheet.save("out/kontak_sayfasi.png")
s2 = Image.new("RGB", (6 * tw, 7 * th), (20, 20, 20)); dr = ImageDraw.Draw(s2)
for i in range(int(cues.T)):
    f = fr[min(i * FPS, len(fr) - 1)]
    im = Image.fromarray(f).resize((tw, th), Image.LANCZOS)
    x, y = (i % 6) * tw, (i // 6) * th; s2.paste(im, (x, y)); dr.rectangle([x, y, x + 30, y + 13], fill=(0, 0, 0)); dr.text((x + 2, y + 1), f"{i}s", fill=(255, 255, 0))
s2.save("out/saniyelik_kareler.png"); print("sayfalar yazıldı")
