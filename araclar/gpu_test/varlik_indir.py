# -*- coding: utf-8 -*-
"""GPU üslup testi (Theo'nun odası) için dış varlıkları indirir.

Ham dosyalar araclar/gpu_test/varlik/ altına iner; bu klasör .gitignore'dadır.
Lisanslar: Poly Haven CC0; Microsoft Rocketbox MIT (lisans metni varlik/rocketbox/LICENSE.md).
Kayıt: araclar/ASSETS.md.

Kullanım:  python araclar/gpu_test/varlik_indir.py
"""
import json
import os
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor

KOK = os.path.join(os.path.dirname(os.path.abspath(__file__)), "varlik")
UA = {"User-Agent": "zk-gpu-test/1.0"}

# Poly Haven (CC0)
MODELLER = [
    "WoodenTable_01",        # yazı masası
    "gallinera_chair",       # masa sandalyesi
    "vintage_oil_lamp",      # gaz/yağ lambası
    "book_encyclopedia_set_01",  # eski kitaplar
    "round_spectacles",      # masada gözlük
]
DOKULAR = {
    "old_wooden_floor_01": ["Diffuse", "nor_gl", "Rough"],
    "plastered_wall_04": ["Diffuse", "nor_gl", "Rough"],
    "dark_wooden_planks": ["Diffuse", "nor_gl", "Rough"],  # şövale ve pencere ahşabı
}
HDRI = []  # gece göğü prosedürel (oda_testi.py); HDRI kullanılmadı
COZ = "2k"

ROCKETBOX = "https://raw.githubusercontent.com/microsoft/Microsoft-Rocketbox/master/"
AVATAR = "Assets/Avatars/Professions/Business_Male_03/"
AVATAR_DOSYALAR = [
    "Export/Business_Male_03.fbx",
    "Textures/m020_body_color.tga",
    "Textures/m020_body_normal.tga",
    "Textures/m020_body_specular.tga",
    "Textures/m020_head_color.tga",
    "Textures/m020_head_normal.tga",
    "Textures/m020_head_specular.tga",
    "Textures/m020_opacity_color.tga",
]


def js(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
        return json.load(r)


def indir(is_):
    url, yol = is_
    if os.path.exists(yol) and os.path.getsize(yol) > 0:
        return yol, "var"
    os.makedirs(os.path.dirname(yol), exist_ok=True)
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=300) as r:
        veri = r.read()
    with open(yol + ".part", "wb") as f:
        f.write(veri)
    os.replace(yol + ".part", yol)
    return yol, len(veri)


def isler():
    out = []
    for m in MODELLER:
        f = js("https://api.polyhaven.com/files/" + m)["gltf"][COZ]["gltf"]
        d = os.path.join(KOK, "polyhaven", m)
        out.append((f["url"], os.path.join(d, os.path.basename(f["url"]))))
        for rel, inc in f.get("include", {}).items():
            out.append((inc["url"], os.path.join(d, rel)))
    for t, haritalar in DOKULAR.items():
        f = js("https://api.polyhaven.com/files/" + t)
        d = os.path.join(KOK, "polyhaven", t)
        for h in haritalar:
            u = f[h][COZ]["jpg"]["url"]
            out.append((u, os.path.join(d, os.path.basename(u))))
    for h in HDRI:
        u = js("https://api.polyhaven.com/files/" + h)["hdri"][COZ]["hdr"]["url"]
        out.append((u, os.path.join(KOK, "polyhaven", h, os.path.basename(u))))
    d = os.path.join(KOK, "rocketbox", "Business_Male_03")
    for rel in AVATAR_DOSYALAR:
        out.append((ROCKETBOX + AVATAR + rel, os.path.join(d, rel)))
    out.append((ROCKETBOX + "LICENSE.md", os.path.join(KOK, "rocketbox", "LICENSE.md")))
    return out


if __name__ == "__main__":
    liste = isler()
    with ThreadPoolExecutor(8) as ex:
        for yol, durum in ex.map(indir, liste):
            print(durum, os.path.relpath(yol, KOK))
    print("tamam:", len(liste), "dosya")
    sys.exit(0)
