"""Kalite kontrol: bitmiş videodan (out/Zanzibar_Savasi.mp4) otomatik denetim + kontak sayfaları."""
import subprocess, sys
import numpy as np
from PIL import Image, ImageDraw
import ui
from engine import W, H, FPS, NF

VID = "out/Zanzibar_Savasi.mp4"
SW, SH = 270, 480   # analiz için küçültülmüş boyut (1/4)

def decode_small():
    cmd = ["ffmpeg", "-loglevel", "error", "-i", VID, "-vf", f"scale={SW}:{SH}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    raw = subprocess.run(cmd, capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, SH, SW, 3)

fr = decode_small()
print("kare sayısı:", len(fr))
lum = fr.mean(axis=(1, 2, 3)); sd = fr.std(axis=(1, 2, 3))
print(f"1) BOŞ/SİYAH KARE: min parlaklık {lum.min():.1f} (kare {lum.argmin()}), min kontrast {sd.min():.1f}; parlaklık<25 olan: {(lum<25).sum()}, kontrast<12 olan: {(sd<12).sum()}")

# 2) savaş saati her karede: HUD hap bölgesi (y 212-308, x 360-720) → /4
y0, y1, x0, x1 = 212//4, 308//4, 365//4, 715//4
reg = fr[:, y0:y1, x0:x1, :].astype(np.int32)
rstd = reg.std(axis=(1, 2, 3))
# hap rengi: lacivert (18,48,74) / koyu kırmızı / kırmızı  → bölgede baskın "hap" pikseli oranı
navy = (np.abs(reg - np.array([18, 48, 74])).sum(-1) < 60)
dkred = (np.abs(reg - np.array([43, 15, 20])).sum(-1) < 70)
red = (np.abs(reg - np.array([255, 59, 48])).sum(-1) < 90)
frac = (navy | dkred | red).mean(axis=(1, 2))
print(f"2) SAVAŞ SAATİ: hap rengi oranı min {frac.min():.2f} (kare {frac.argmin()}), <0.30 olan kare: {(frac<0.30).sum()} / {len(fr)}")

# 3) yazısız ardışık kare (altyazı kelime görünürlüğü, kod tarafı) + döngü sarması
def text_visible(t):
    for (t0, t1, text) in ui.CAPS:
        if t0 <= t < t1:
            words, lines, widths, space, px = ui._CAPLAY[text]
            n = len(words); dt = min(0.30, max(0.15, (t1 - t0) * 0.62 / n))
            if t >= t0 + 0.02 + 0.03: return True   # ilk kelime beliriyor
    return False
vis = [text_visible(i / FPS) and (i / FPS) < 41.8 for i in range(NF)]
runs, cur = [], 0
seq = vis + vis  # sarma
best = 0; cur = 0
for v in seq:
    cur = 0 if v else cur + 1
    best = max(best, cur)
print(f"3) EN UZUN YAZISIZ SERİ (döngü sarması dahil): {min(best,NF)} kare = {min(best,NF)/FPS:.3f} sn  (sınır 0.3 sn)")

# 4) ilk kare / son kare
a = fr[0].astype(np.float32); b = fr[-1].astype(np.float32)
mad = np.abs(a - b).mean(); psnr = 10*np.log10(255**2/max(1e-9, ((a-b)**2).mean()))
print(f"4) İLK vs SON KARE (video): ort. mutlak fark {mad:.3f}, PSNR {psnr:.1f} dB")
import compose
ia = np.asarray(compose.render_frame(0)); ib = np.asarray(compose.render_frame(NF-1))
print(f"   ham render farkı: max {np.abs(ia.astype(int)-ib.astype(int)).max()} (0 = birebir aynı)")

# 5) görsel değişim: her 2.5 sn'lik pencerede kareler arası ort. mutlak fark
d = np.abs(np.diff(fr.astype(np.int16), axis=0)).mean(axis=(1,2,3))
win = int(2.5*FPS); low = []
for s in range(0, NF - win, 6):
    if d[s:s+win].max() < 1.5: low.append(s/FPS)
print(f"5) 2.5 sn'lik pencerede belirgin değişim (<1.5 yoğunluk) olmayan başlangıçlar: {low if low else 'yok'}")
per_s = [d[i*FPS:(i+1)*FPS].mean() for i in range(42)]
print("   saniyelik hareket yoğunluğu:", " ".join(f"{v:.1f}" for v in per_s))

# 6) kontak sayfası: her sahneden 3 kare
scenes = [("S1",[0.4,1.5,2.7]),("S2",[3.5,4.6,5.6]),("S3",[7.0,7.6,10.0]),("S4",[11.9,13.2,15.3]),("S5",[16.2,17.6,19.3]),
          ("S6",[20.4,23.0,26.0]),("S7",[28.8,30.3,31.5]),("S8",[32.8,33.8,34.6]),("S9",[35.6,37.4,39.6]),("S10",[40.5,41.1,41.95])]
tw, th = 180, 320
sheet = Image.new("RGB", (6*tw, 5*th), (20,20,20)); dr = ImageDraw.Draw(sheet)
import subprocess as sp
k = 0
for name, ts in scenes:
    for t in ts:
        raw = sp.run(["ffmpeg","-loglevel","error","-ss",f"{t}","-i",VID,"-frames:v","1","-vf",f"scale={tw}:{th}","-f","rawvideo","-pix_fmt","rgb24","-"],capture_output=True).stdout
        im = Image.frombytes("RGB",(tw,th),raw)
        x,y = (k%6)*tw, (k//6)*th
        sheet.paste(im,(x,y)); dr.rectangle([x,y,x+78,y+13],fill=(0,0,0)); dr.text((x+2,y+1),f"{name} {t:.2f}s",fill=(255,255,0)); k+=1
sheet.save("out/kontak_sayfasi.png"); print("kontak sayfası: out/kontak_sayfasi.png")

# 7) saniyede 1 kare → 7x6 sayfa
tw, th = 180, 320
s2 = Image.new("RGB",(6*tw,7*th),(20,20,20)); dr = ImageDraw.Draw(s2)
for i in range(42):
    f = fr[min(i*FPS, len(fr)-1)]
    im = Image.fromarray(f).resize((tw,th), Image.LANCZOS)
    x,y=(i%6)*tw,(i//6)*th; s2.paste(im,(x,y)); dr.rectangle([x,y,x+30,y+13],fill=(0,0,0)); dr.text((x+2,y+1),f"{i}s",fill=(255,255,0))
s2.save("out/saniyelik_kareler.png"); print("out/saniyelik_kareler.png")
