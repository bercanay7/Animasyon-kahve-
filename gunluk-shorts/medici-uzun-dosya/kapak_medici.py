#!/usr/bin/env python3
"""Medici kapakları (küçük resim): yayin/kapak_P{N}_A|B|C.jpg (1280×720, ≤2 MB). Zemin = motorun KENDİ çizimi (Program(shots=…)); üstüne Cinzel ile büyük, okunaklı yazı.

  python3 kapak_medici.py --part 1            # A: ana başlık freski · B: 1743 odası + belge · C: florin yığını
  python3 kapak_medici.py --part 1 --kontrol  # 320×180 ve 270×480-kırpma okunurluk kontrol şeridi → yayin/kapak_P1_kontrol.png

Kurallar (Anayasa §7/§12-7 ruhu): yazı ≤4–5 sözcük, ≥72 px (1280×720'de), parça numarası büyük ve her parçada aynı yerde (sağ alt), videonun söylemediğini
vaat etmez (alıntı kartı kullanılmaz; 'Hiçbir şey buradan çıkmayacak' Anna Maria Luisa'ya atfedilmez)."""
import argparse
import os
import sys

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.chdir(HERE)

import compose  # noqa: E402
import shots as SH  # noqa: E402

OUT = os.path.join(HERE, "yayin")
FONTS = os.path.join(HERE, "fonts")
os.makedirs(OUT, exist_ok=True)
GOLD = (233, 199, 112)
CREAM = (248, 235, 192)

PART_TEXT = {
    1: dict(A=("MEDİCİ", "ALTIN FLORİN"), B=("BİR SÖZLEŞME", "BİR ŞEHRİ BAĞLADI"), C=("FLORİN", "VE ÇİFTE DEFTER")),
}


def font(name, size):
    return ImageFont.truetype(os.path.join(FONTS, name), size)


def engine_frame(shot, t, fast=True):
    """Tek çekimi motorda çizip t saniyedeki kareyi (1920×1080 RGB) döndürür."""
    prog = compose.Program(shots=[shot], end=t + 1.0)
    return prog.frame(int(round(t * 24)))


def gold_text(im, xy, text, size, anchor="mm", fill=GOLD, stroke=0, track=0, shadow=6):
    d = ImageDraw.Draw(im)
    f = font("Cinzel_700Bold.ttf", size)
    if track:
        # harf aralığı: tek tek çiz
        widths = [d.textlength(ch, font=f) for ch in text]
        total = sum(widths) + track * (len(text) - 1)
        x0 = xy[0] - total / 2 if anchor[0] == "m" else xy[0]
        x = x0
        for ch, w in zip(text, widths):
            if shadow:
                d.text((x + shadow * 0.6, xy[1] + shadow), ch, font=f, fill=(10, 6, 2), anchor="lm")
            d.text((x, xy[1]), ch, font=f, fill=fill, anchor="lm", stroke_width=stroke, stroke_fill=(30, 18, 6))
            x += w + track
        return
    if shadow:
        d.text((xy[0] + shadow * 0.6, xy[1] + shadow), text, font=f, fill=(10, 6, 2), anchor=anchor)
    d.text(xy, text, font=f, fill=fill, anchor=anchor, stroke_width=stroke, stroke_fill=(30, 18, 6))


def shade(im, box, alpha=0.62, blur=40):
    """Okunurluk için yumuşak koyu bant."""
    w, h = im.size
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).rectangle(box, fill=int(255 * alpha))
    m = m.filter(ImageFilter.GaussianBlur(blur))
    dark = Image.new("RGB", (w, h), (8, 5, 2))
    return Image.composite(dark, im, m)


def part_badge(im, part, n=7):
    """Parça numarası: sağ altta, her kapakta aynı yerde ve büyük."""
    w, h = im.size
    d = ImageDraw.Draw(im)
    bw, bh = 330, 150
    x1, y1 = w - 36, h - 34
    x0, y0 = x1 - bw, y1 - bh
    d.rounded_rectangle((x0, y0, x1, y1), 18, fill=(14, 22, 62), outline=GOLD, width=5)
    f = font("Cinzel_700Bold.ttf", 118)
    d.text((x0 + 36, (y0 + y1) / 2 + 4), str(part), font=f, fill=CREAM, anchor="lm")
    f2 = font("Cinzel_700Bold.ttf", 60)
    d.text((x0 + 36 + 84, (y0 + y1) / 2 + 30), f"/ {n}", font=f2, fill=GOLD, anchor="lm")
    f3 = font("Cinzel_600SemiBold.ttf", 28)
    d.text((x0 + 36 + 84, (y0 + y1) / 2 - 38), "PARÇA", font=f3, fill=GOLD, anchor="lm")


def save(im, name):
    small = im.resize((1280, 720), Image.LANCZOS)
    path = os.path.join(OUT, name + ".jpg")
    q = 93
    while True:
        small.save(path, "JPEG", quality=q, optimize=True)
        if os.path.getsize(path) < 1_900_000 or q <= 70:
            break
        q -= 4
    print(path, os.path.getsize(path) // 1000, "KB")
    return small


def cover_A(part):
    top, sub = PART_TEXT[part]["A"]
    # ana başlık freski (sub ayrı satır); fresk tam açılmış an
    shot = SH.shot("fresco_title", 0.0, text=top, sub=f"PARÇA {part}/7 · {sub}", mode="night", perde=1)
    arr = engine_frame(shot, 6.4)
    im = Image.fromarray(arr).convert("RGB")
    part_badge(im, part)
    return save(im, f"kapak_P{part}_A")


def cover_B(part):
    l1, l2 = PART_TEXT[part]["B"]
    shot = SH.shot("oda", 0.0, room="oda1743", figure="seated", tod="dusk", mode="night", perde=1, path="in", seal_at=1.0, seed=3)
    arr = engine_frame(shot, 9.6)
    im = Image.fromarray(arr).convert("RGB")
    im = shade(im, (0, 60, 1920, 470), 0.78)
    gold_text(im, (960, 150), l1, 150, stroke=2, track=6)
    gold_text(im, (960, 330), l2, 112, fill=CREAM, stroke=2, track=4)
    part_badge(im, part)
    return save(im, f"kapak_P{part}_B")


def cover_C(part):
    l1, l2 = PART_TEXT[part]["C"]
    shot = SH.shot("coin", 0.0, n=7, size=640, mode="night", perde=1, pos=(560, 560), seed=5)
    arr = engine_frame(shot, 3.2)
    im = Image.fromarray(arr).convert("RGB")
    im = shade(im, (940, 120, 1920, 960), 0.80, blur=60)
    gold_text(im, (1450, 330), l1, 200, stroke=2, track=4)
    gold_text(im, (1450, 530), l2, 78, fill=CREAM, stroke=1, track=3)
    part_badge(im, part)
    return save(im, f"kapak_P{part}_C")


def kontrol(part):
    tiles = []
    for k in "ABC":
        p = os.path.join(OUT, f"kapak_P{part}_{k}.jpg")
        im = cv2.imread(p)
        tiles.append(cv2.resize(im, (320, 180), interpolation=cv2.INTER_AREA))
    row = np.concatenate(tiles, axis=1)
    cv2.imwrite(os.path.join(OUT, f"kapak_P{part}_kontrol.png"), row)
    print("kontrol şeridi:", os.path.join(OUT, f"kapak_P{part}_kontrol.png"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--part", type=int, default=1)
    ap.add_argument("--kontrol", action="store_true")
    a = ap.parse_args()
    if a.kontrol:
        return kontrol(a.part)
    cover_A(a.part)
    cover_B(a.part)
    cover_C(a.part)
    kontrol(a.part)


if __name__ == "__main__":
    main()
