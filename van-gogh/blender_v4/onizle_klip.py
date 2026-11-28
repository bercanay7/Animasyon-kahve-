# -*- coding: utf-8 -*-
"""Y4 figür klipleri için önizleme (sistem python'u, Pillow):
  python van-gogh/blender_v4/onizle_klip.py theo_oda theo_dur vincent_goster
Çıktı: onizleme/klip_<ad>_{000,040,080}.jpg — 960 px, gri zemin (128) üstünde RGBA kare; altta normal ve kimlik şeridi.
Ayrıca klasör boyutunu yazar (sınır: klip başına 20 MB).
"""
import os
import sys

from PIL import Image

BURA = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.join(BURA, "..", "blender")
ON = os.path.join(BURA, "onizleme")
os.makedirs(ON, exist_ok=True)


def gri(yol, kirp=None):
    im = Image.open(yol).convert("RGBA")
    g = Image.new("RGBA", (960, 540), (128, 128, 128, 255))
    g.alpha_composite(im, (kirp["x"], kirp["y"]) if kirp else (0, 0))
    return g.convert("RGB")


def klip(ad):
    d = os.path.join(V3, "v4_klip_" + ad)
    import json
    kp = json.load(open(os.path.join(d, "bilgi.json"), encoding="utf-8")).get("kirpma")
    for n in (0, 40, 80):
        k = gri(os.path.join(d, "kare", "k_%04d.png" % n), kp)
        nm = gri(os.path.join(d, "normal", "n_%04d.png" % n), kp).resize((480, 270))
        km = gri(os.path.join(d, "kimlik", "i_%04d.png" % n), kp).resize((480, 270))
        S = Image.new("RGB", (960, 540 + 270), (128, 128, 128))
        S.paste(k, (0, 0)); S.paste(nm, (0, 540)); S.paste(km, (480, 540))
        S.save(os.path.join(ON, "klip_%s_%03d.jpg" % (ad, n)), quality=85)
    boy = sum(os.path.getsize(os.path.join(r, f)) for r, _, fs in os.walk(d) for f in fs)
    print(ad, "%.1f MB" % (boy / 1048576))


if __name__ == "__main__":
    for a in sys.argv[1:]:
        klip(a)
