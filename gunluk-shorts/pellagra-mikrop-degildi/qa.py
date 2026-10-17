"""Kalite kontrol: out/Pellagra_Mikrop_Degildi.mp4 → boş kare, HUD, yazısız seri, ilk/son kare, hareket, donma, kontak sayfaları. Çıkış kodu 0 = geçti."""
import os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw
import cues, ui
from engine import W, H, FPS

VID = "out/Pellagra_Mikrop_Degildi.mp4"
if not os.path.exists("kaynaklar.md"):
    print("HATA: kaynaklar.md yok (Kanal Anayasası, kaynak kapısı)"); sys.exit(1)
SW, SH = 180, 320
SF = 1080 / SW
NF = int(round(cues.T * FPS))


def decode_small():
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", VID, "-vf", f"scale={SW}:{SH}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, SH, SW, 3)


fr = decode_small()
print("kare sayısı:", len(fr), "(beklenen", NF, ")")
lum = np.array([f.mean() for f in fr]); sd = np.array([f.std() for f in fr])
print(f"1) BOŞ/SİYAH KARE: min parlaklık {lum.min():.0f}, min kontrast {sd.min():.1f}; parlaklık<25: {(lum<25).sum()}")
# HUD: koyu etiket (TESLİMAT #7 + 4 kapsül) — etiketin içinde koyu piksel çoğunlukta, açık yazı/kapsül oranı makul aralıkta olmalı
y0, y1, x0, x1 = int(222 / SF), int(302 / SF), int(230 / SF), int(850 / SF)
dk = np.array([(f[y0:y1, x0:x1, :].mean(axis=2) < 95).mean() for f in fr])
lt = np.array([(f[y0:y1, x0:x1, :].mean(axis=2) > 165).mean() for f in fr])
ok_h = (dk > 0.55) & (lt > 0.02) & (lt < 0.45)
hud_ok = ok_h.mean()
print(f"2) HUD (TESLİMAT #7 + KANIT kapsülleri): koyu oran min {dk.min()*100:.0f}%, açık oran {lt.min()*100:.1f}–{lt.max()*100:.1f}%; aralık dışı kare: {int((~ok_h).sum())} / {len(fr)}")


def visible(t):
    for i, p in enumerate(ui.PAGES):
        t0 = p[0]["t0"] - 0.03
        t1 = (ui.PAGES[i + 1][0]["t0"] - 0.03) if i + 1 < len(ui.PAGES) else cues.CAP_END
        if t0 + 0.02 <= t < t1:
            return True
    return False


vis = [visible(i / FPS) and (i / FPS) < cues.FINAL_T for i in range(NF)]
best = cur = 0
for v in vis + vis:
    cur = 0 if v else cur + 1
    best = max(best, cur)
best = min(best, NF)
print(f"3) EN UZUN YAZISIZ SERİ (döngü dahil): {best} kare = {best/FPS:.3f} sn (sınır 0.4 — cümle araları)")
a = fr[0].astype(np.float32); b = fr[-1].astype(np.float32)
print(f"4) İLK vs SON KARE: ort. fark {np.abs(a-b).mean():.3f}, PSNR {10*np.log10(255**2/max(1e-9,((a-b)**2).mean())):.1f} dB")
import compose
ia = np.asarray(compose.render_frame(0)); ib = np.asarray(compose.render_frame(NF - 1))
print(f"   ham render farkı max {np.abs(ia.astype(int)-ib.astype(int)).max()} (0 = birebir aynı)")
d = np.array([np.abs(fr[i + 1].astype(np.int16) - fr[i].astype(np.int16)).mean() for i in range(len(fr) - 1)])
win = int(2.0 * FPS); low = []
for s in range(0, NF - win, 6):
    if d[s:s + win].max() < 0.9:
        low.append(round(s / FPS, 1))
print(f"5) 2 sn'lik pencerede belirgin görsel değişim olmayan başlangıçlar: {low if low else 'yok'}")
print("   saniyelik hareket:", " ".join(f"{d[i*FPS:(i+1)*FPS].mean():.1f}" for i in range(int(cues.T))))

# kontak sayfaları
tw, th = 180, 320
rows = []
for g in cues.GROUPS:
    a0, b0 = cues.st(g[0]), cues.en(g[-1])
    rows += [a0 + 0.4, (a0 + b0) / 2, b0 - 0.3]
rows[0] = 0.0
cols = 6
sheet = Image.new("RGB", (cols * tw, ((len(rows) + cols - 1) // cols) * th), (20, 20, 20)); dr = ImageDraw.Draw(sheet)
for k, t in enumerate(rows):
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-ss", f"{t}", "-i", VID, "-frames:v", "1", "-vf", f"scale={tw}:{th}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                         capture_output=True).stdout
    im = Image.frombytes("RGB", (tw, th), raw)
    x, y = (k % cols) * tw, (k // cols) * th
    sheet.paste(im, (x, y)); dr.rectangle([x, y, x + 62, y + 13], fill=(0, 0, 0)); dr.text((x + 2, y + 1), f"{t:.1f}s", fill=(255, 255, 0))
sheet.save("out/kontak_sayfasi.png")
nsec = int(cues.T)
s2 = Image.new("RGB", (10 * tw, ((nsec + 9) // 10) * th), (20, 20, 20)); dr = ImageDraw.Draw(s2)
for i in range(0, nsec, 3):
    f = fr[min(i * FPS, len(fr) - 1)]
    im = Image.fromarray(f).resize((tw, th), Image.LANCZOS)
    k = i // 3
    x, y = (k % 10) * tw, (k // 10) * th
    s2.paste(im, (x, y)); dr.rectangle([x, y, x + 34, y + 13], fill=(0, 0, 0)); dr.text((x + 2, y + 1), f"{i}s", fill=(255, 255, 0))
s2.crop((0, 0, 10 * tw, ((nsec // 3 + 10) // 10) * th)).save("out/saniyelik_kareler.png"); print("sayfalar yazıldı")

# ── kapı özeti ──
first_word = cues.TL["sentences"][0]["words"][0]["t0"]
fz = subprocess.run(["ffmpeg", "-i", VID, "-vf", "freezedetect=n=-55dB:d=1.0", "-f", "null", "-"], capture_output=True, text=True).stderr
freezes = [l for l in fz.splitlines() if "freeze_start" in l]
checks = {
    "kare sayısı": len(fr) == NF,
    "boş/siyah kare yok": (lum < 25).sum() == 0 and sd.min() > 6,
    "HUD her karede": hud_ok > 0.995,
    "yazısız seri ≤0,4 sn": best / FPS <= 0.4,
    "ilk=son kare (ham render birebir)": int(np.abs(ia.astype(int) - ib.astype(int)).max()) == 0,
    "ilk ses ≤0,5 sn": first_word <= 0.5,
    "2 sn'lik durağan pencere yok": not low,
    "donma (freezedetect) yok": not freezes,
    "süre ≤ 180 sn (Shorts sınırı)": cues.T <= 180,
}
print("KAPI ÖZETİ:", "; ".join(f"{k}: {'GEÇTİ' if v else 'KALDI'}" for k, v in checks.items()))
if freezes: print("  donma:", freezes[:3])
sys.exit(0 if all(checks.values()) else 1)
