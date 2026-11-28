# -*- coding: utf-8 -*-
"""Y4 klip karelerini figürün kutusuna kırp (depo boyu: klip başına ≤ 20 MB). Sistem python'u, Pillow.
  python van-gogh/blender_v4/kirp_klip.py theo_oda theo_dur vincent_goster
Kutu: bütün RGBA karelerin alfa birleşimi + 6 px pay; normal ve kimlik kareleri aynı kutuya kırpılır.
bilgi.json'a yazılır: "kirpma": {"x", "y", "w", "h", "tam": [960, 540]} (x, y: tam karedeki sol üst köşe, piksel).
Motor kareyi tam kareye (x, y) ofsetiyle basar; kırpılmamış kareyle piksel piksel aynıdır.
"""
import json
import os
import sys

from PIL import Image

V3 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "blender")
PAY = 6


def klip(ad):
    d = os.path.join(V3, "v4_klip_" + ad)
    bilgi_yol = os.path.join(d, "bilgi.json")
    bilgi = json.load(open(bilgi_yol, encoding="utf-8"))
    if bilgi.get("kirpma"):
        print(ad, "zaten kırpılmış", bilgi["kirpma"]); return
    kareler = sorted(os.listdir(os.path.join(d, "kare")))
    x0, y0, x1, y1 = 10 ** 9, 10 ** 9, -1, -1
    for f in kareler:
        bb = Image.open(os.path.join(d, "kare", f)).getchannel("A").getbbox()
        if bb:
            x0, y0, x1, y1 = min(x0, bb[0]), min(y0, bb[1]), max(x1, bb[2]), max(y1, bb[3])
    W, H = 960, 540
    x0, y0, x1, y1 = max(0, x0 - PAY), max(0, y0 - PAY), min(W, x1 + PAY), min(H, y1 + PAY)
    for kl in ("kare", "normal", "kimlik"):
        for f in sorted(os.listdir(os.path.join(d, kl))):
            yol = os.path.join(d, kl, f)
            im = Image.open(yol)
            im.crop((x0, y0, x1, y1)).save(yol, optimize=True)
    bilgi["kirpma"] = {"x": x0, "y": y0, "w": x1 - x0, "h": y1 - y0, "tam": [W, H]}
    json.dump(bilgi, open(bilgi_yol, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    boy = sum(os.path.getsize(os.path.join(r, f)) for r, _, fs in os.walk(d) for f in fs)
    print(ad, bilgi["kirpma"], "%.1f MB" % (boy / 1048576))


if __name__ == "__main__":
    for a in sys.argv[1:]:
        klip(a)
