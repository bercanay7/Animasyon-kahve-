# -*- coding: utf-8 -*-
"""Van Gogh v4 varlıkları: Poly Haven (CC0) + MakeHuman asset pack'leri (CC0 / CC BY) + MPFB eklentisi.

  python van-gogh/blender_v4/varlik_indir.py
Sonra (bir kez): MPFB'yi Blender'a kur ve paketleri MPFB kullanıcı verisine aç:
  blender -c extension install-file -r user_default -e van-gogh/blender_v4/varlik/indirme/mpfb-2.0.18.zip
  blender -b --python-expr "import glob,zipfile; from bl_ext.user_default.mpfb.services import LocationService as L; [zipfile.ZipFile(z).extractall(L.get_user_data()) for z in glob.glob('van-gogh/blender_v4/varlik/indirme/*_c*.zip')]"
Hepsi .gitignore'da (blender_v4/varlik/). Kayıt: araclar/ASSETS.md.
"""
import json
import os
import urllib.request
from concurrent.futures import ThreadPoolExecutor

BURA = os.path.dirname(os.path.abspath(__file__))
KOK = os.path.join(BURA, "varlik")
UA = {"User-Agent": "zk-v4/1.0"}
MODELLER = ["WoodenTable_01", "gallinera_chair", "vintage_oil_lamp", "book_encyclopedia_set_01", "round_spectacles",
            "wicker_basket_01", "wooden_crate_01", "wooden_crate_02"]
DOKULAR = ["old_wooden_floor_01", "plastered_wall_04", "dark_wooden_planks", "worn_planks"]
MH = "https://files.makehumancommunity.org/asset_packs/"
PAKETLER = ["makehuman_system_assets/makehuman_system_assets_cc0.zip", "suits01/suits01_cc0.zip", "dress03/dress03_cc-by.zip",
            "hair01/hair01_cc0.zip", "bodyparts05/bodyparts05_cc0.zip", "skins02/skins02_cc0.zip"]
MPFB = ("https://extensions.blender.org/download/sha256:c075b3e9b94b8e5556a5f03f4653602d02ea306de08126e8f55ed6dee28a2dad/add-on-mpfb-v2.0.18.zip",
        "mpfb-2.0.18.zip")


def js(u):
    return json.load(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60))


def indir(x):
    u, y = x
    if os.path.exists(y) and os.path.getsize(y) > 0:
        return
    os.makedirs(os.path.dirname(y), exist_ok=True)
    with urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=900) as r, open(y + ".part", "wb") as f:
        while True:
            b = r.read(1 << 20)
            if not b:
                break
            f.write(b)
    os.replace(y + ".part", y)


def isler():
    out = []
    for m in MODELLER:
        f = js("https://api.polyhaven.com/files/" + m)["gltf"]["2k"]["gltf"]
        d = os.path.join(KOK, "polyhaven", m)
        out.append((f["url"], os.path.join(d, os.path.basename(f["url"]))))
        out += [(i["url"], os.path.join(d, rel)) for rel, i in f.get("include", {}).items()]
    for t in DOKULAR:
        f = js("https://api.polyhaven.com/files/" + t)
        for h in ("Diffuse", "nor_gl", "Rough"):
            u = f[h]["2k"]["jpg"]["url"]
            out.append((u, os.path.join(KOK, "polyhaven", t, os.path.basename(u))))
    out += [(MH + p, os.path.join(KOK, "indirme", os.path.basename(p))) for p in PAKETLER]
    out.append((MPFB[0], os.path.join(KOK, "indirme", MPFB[1])))
    return out


if __name__ == "__main__":
    L = isler()
    list(ThreadPoolExecutor(6).map(indir, L))
    print("tamam:", len(L), "dosya")
