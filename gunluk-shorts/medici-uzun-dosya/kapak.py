#!/usr/bin/env python3
"""Kapak (küçük resim) üretici: yayin/kapak_A.jpg, kapak_B.jpg, kapak_C.jpg (1280×720, ≤2 MB).
  A: madalya + ŞARLKEN / 5 CEPHE · TEK ADAM     B: harita + başlık     C: salon siluet + soru
Çalıştır: python3 kapak.py"""
import os
import sys

import cv2
import numpy as np
import skia

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.chdir(HERE)

import icons  # noqa: E402
import medal  # noqa: E402
import scenes_lib  # noqa: E402,F401
import shots as SH  # noqa: E402
import sk  # noqa: E402
from sk import H, W  # noqa: E402

OUT = os.path.join(HERE, "yayin")
os.makedirs(OUT, exist_ok=True)


def save(f, name):
    img = sk.post(f.rgb(), 3, grain=0.5, bloom=0.16)
    big = os.path.join(OUT, name + ".png")
    cv2.imwrite(big, cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
    small = cv2.resize(img, (1280, 720), interpolation=cv2.INTER_AREA)
    jpg = os.path.join(OUT, name + ".jpg")
    q = 92
    while True:
        cv2.imwrite(jpg, cv2.cvtColor(small, cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, q])
        if os.path.getsize(jpg) < 1_900_000 or q <= 70:
            break
        q -= 4
    os.remove(big)
    print(jpg, os.path.getsize(jpg) // 1000, "KB")
    return img


def fronts_row(f, x0, y, size=64, gap=128):
    for i, (ic, nm) in enumerate(SH.FRONT_ICONS):
        icons.draw_icon(f, ic, x0 + i * gap, y, size=size, metal="gold", alpha=1.0, shadow=True)


def kapak_a():
    f = sk.Frame()
    f.bg("night")
    f.rays(alpha=0.9)
    f.circle(520, 560, 620, shader=f.rad(520, 560, 620, [("#F0D27A", 0.0, 120), ("#C9962B", 0.45, 45), ("#C9962B", 1.0, 0)]), blend=skia.BlendMode.kPlus)
    SH.draw_medal(f, "karl_olgun", 520, 560, 880, "gold", glint=None, tilt=0.10)
    f.gold("ŞARLKEN", 1380, 330, face="title", size=178, track=14, glow=0.5)
    f.line(1000, 392, 1770, 392, color="#C9962B", sw=3, alpha=0.9)
    f.gold("5 CEPHE", 1380, 560, face="title", size=132, track=10)
    f.text("TEK ADAM", 1380, 700, face="title", size=132, color="#E5483B", align="c", track=10, shadow=(4, 5, 6, "#000000"))
    fronts_row(f, 1130, 840, size=70, gap=125)
    f.vig(0.7)
    return save(f, "kapak_A")


def kapak_b():
    import mapsk
    f = sk.Frame()
    mv = SH.mapview()
    cam = mapsk.Cam(10, 46, 1.55)
    mv.base(f, cam, "night", mountains=True)
    for nm, col in (("ispanya", "ispanya"), ("hollanda", "burgonya"), ("franche_comte", "burgonya"), ("avusturya", "avusturya"), ("napoli", "ispanya"), ("sicilya", "ispanya"), ("sardunya", "ispanya"), ("milano", "ispanya")):
        mv.region(f, cam, nm, SH._fac(col), alpha=0.8, amt=1.0)
    f.rect(0, 0, W, H, shader=f.lin(0, 0, W, 0, [("#000000", 0.0, 240), ("#000000", 0.55, 120), ("#000000", 1.0, 0)]))
    f.gold("ŞARLKEN", 740, 470, face="title", size=200, track=16, glow=0.55)
    f.text("DÜNYAYI TESLİM EDEN İMPARATOR", 740, 585, face="title_m", size=46, color="#F0DDA0", align="c", track=9, shadow=(3, 4, 5, "#000000"))
    f.vig(0.65)
    return save(f, "kapak_B")


def kapak_c():
    f = sk.Frame()
    import scenes_lib as SL
    from shots import Ctx, Shot
    import scenes_d as SD  # c0'daki baston/kılıçsız çift (kaynak kapısı: baston iddiası doğrulanmadı)
    sh = Shot("theatre", 0.0, dict(scene="hall", cams=[(0, (1000, 660, 1.75))], p=dict(crowd=True, emperor=False, extra=lambda f, t: SD.draw_pair(f, 1010, 985, 520, 0.0)), vig=0.7, dust_n=0), None, "kapak")
    sh.t0, sh.t1, sh.i = 0.0, 8.0, 1
    cx = Ctx(f, 3.0, sh, SH.timeline())
    SH.KINDS["theatre"](cx, **sh.params)
    f.rect(0, 0, W, H, shader=f.lin(0, 0, 0, H, [("#000000", 0.0, 150), ("#000000", 0.5, 0), ("#000000", 1.0, 190)]))
    f.gold("NEDEN BIRAKTI?", W / 2, 210, face="title", size=150, track=12, glow=0.5)
    f.text("ŞARLKEN  ·  1555", W / 2, 960, face="title_m", size=64, color="#F0DDA0", align="c", track=14, shadow=(3, 4, 5, "#000000"))
    f.vig(0.6)
    return save(f, "kapak_C")


if __name__ == "__main__":
    kapak_a()
    kapak_b()
    kapak_c()
