# -*- coding: utf-8 -*-
"""Dönem giysileri Blender'da modellenir (GOREV_3_kapi.md, kullanıcı kararı 28 Kasım): hazır giysi şablonu yok.

Yöntem: figürün kendi MPFB gövde yüzeyinden kalıp parçaları kesilir (ağırlık ve dinlenme yüksekliğiyle seçilen bölgeler,
MakeHuman'ın yardımcı kabukları `helper-tights` / `helper-skirt`), bol pay verilerek dışa şişirilir, kalınlık ve
yumuşatma eklenir. Parçalar gövdenin kemik ağırlıklarını taşır: pozla birlikte hareket eder.
- Theo: 1880'ler ceketi (göğüste yüksek kapanan, V açıklık, kalça boyu etek), yelek, kolalı dik yaka, ince kravat,
  manşet, düz bol pantolon, deri ayakkabı.
- Vincent: bourgeron (bol, kalçayı örten, kapalı önlü mavi iş ceketi, küçük devrik yaka, yama cepler), keten gömlek
  yakası, ince boyun bağı, bol koyu pantolon, ayakkabı.
Kırışık: kumaşa özgü düşük frekanslı yer değiştirme (desen değil, değer farkı).
"""
import math
import bpy
import bmesh
from mathutils import Vector

P = "mixamorig:"


# ---------------------------------------------------------------- ortak
def _gruplar(gov):
    return {g.index: g.name for g in gov.vertex_groups}


def _agirlik(v, adlar, gi):
    t = s = 0.0
    for g in v.groups:
        n = gi.get(g.group, "")
        if n.startswith(P):
            t += g.weight
            if any(n == P + a for a in adlar):
                s += g.weight
    return s / t if t > 1e-6 else 0.0


def _grupta(v, ad, gi, esik=0.5):
    return any(gi.get(g.group) == ad and g.weight > esik for g in v.groups)


def kes(gov, ad, secici):
    """Gövdenin kopyasından yalnız `secici(v, z, x, y)` doğru olan köşeler kalır. Ağırlıklar, şekil anahtarları ve
    iskelet değiştiricisi korunur; yardımcıları gizleyen maske kaldırılır."""
    ob = gov.copy(); ob.data = gov.data.copy(); ob.name = ad
    bpy.context.scene.collection.objects.link(ob)
    ob.parent = gov.parent; ob.matrix_parent_inverse = gov.matrix_parent_inverse.copy()
    for m in list(ob.modifiers):
        if m.type in ('MASK', 'SUBSURF'):
            ob.modifiers.remove(m)
    gi = _gruplar(ob)
    Mw = ob.matrix_world
    bm = bmesh.new(); bm.from_mesh(ob.data)
    bm.verts.ensure_lookup_table()
    me = ob.data
    sil = []
    for bv in bm.verts:
        v = me.vertices[bv.index]
        w = Mw @ v.co
        if not secici(v, w.z, w.x, w.y, gi):
            sil.append(bv)
    bmesh.ops.delete(bm, geom=sil, context='VERTS')
    bm.to_mesh(me); bm.free()
    ob.data.materials.clear()
    for p in ob.data.polygons:
        p.use_smooth = True
    return ob


def bitir(ob, pay, kalin=0.004, kirisik=0.004, alt=1, pay_grubu=None, ek_pay=0.0):
    """Dışa şişir (pay, m), kırışık, kalınlık, yumuşatma. Değiştiriciler iskeletten sonra (pozlu yüzeyde sabit pay)."""
    d = ob.modifiers.new("pay", 'DISPLACE'); d.direction = 'NORMAL'; d.mid_level = 0.0; d.strength = pay
    if pay_grubu:
        d2 = ob.modifiers.new("ek_pay", 'DISPLACE'); d2.direction = 'NORMAL'; d2.mid_level = 0.0; d2.strength = ek_pay
        d2.vertex_group = pay_grubu
    if kirisik:
        tx = bpy.data.textures.get("kumas_kirisik") or bpy.data.textures.new("kumas_kirisik", 'STUCCI')
        tx.noise_scale = 0.09; tx.turbulence = 3.0
        k = ob.modifiers.new("kirisik", 'DISPLACE'); k.texture = tx; k.texture_coords = 'LOCAL'; k.strength = kirisik; k.mid_level = 0.5
    s = ob.modifiers.new("kalinlik", 'SOLIDIFY'); s.thickness = kalin; s.offset = -1.0
    sb = ob.modifiers.new("yumusat", 'SUBSURF'); sb.levels = alt; sb.render_levels = alt
    return ob


def kumas(ad, renk, puruz=0.85, sheen=0.35):
    m = bpy.data.materials.new(ad)
    b = [n for n in m.node_tree.nodes if n.type == 'BSDF_PRINCIPLED'][0]
    b.inputs['Base Color'].default_value = (*renk, 1); b.inputs['Roughness'].default_value = puruz
    b.inputs['Sheen Weight'].default_value = sheen; b.inputs['Specular IOR Level'].default_value = 0.3
    return m


def boya(ob, m, kimlik):
    ob.data.materials.clear(); ob.data.materials.append(m); ob["kimlik"] = kimlik
    return ob


def _grup_z(gov, ad):
    gi = _gruplar(gov); W = gov.matrix_world
    zs = [(W @ v.co).z for v in gov.data.vertices if any(gi.get(g.group) == ad and g.weight > 0.5 for g in v.groups)]
    return sum(zs) / len(zs)


def olc(isk, gov):
    """Dinlenme pozunda kalıp yükseklikleri (dünya z) ve gövde merkezi.
    Not: MPFB'nin Mixamo iskeletinde boyun kemiği kulak hizasında başlar; boyun dibi ve çene MakeHuman'ın eklem
    yardımcılarından (joint-neck, joint-jaw) alınır."""
    pb = isk.pose.bones; W = isk.matrix_world
    h = lambda a: (W @ pb[P + a].head)
    boyun = _grup_z(gov, "joint-neck"); cene = _grup_z(gov, "joint-jaw")
    return {
        "boyun_dip": boyun, "cene": cene,
        "bel": h("Spine").z + 0.02,
        "gogus": h("Spine2").z,
        "boyun": boyun,
        "bas": h("Head").z,
        "kasik": (h("LeftUpLeg").z + h("RightUpLeg").z) / 2 - 0.07,
        "diz": (h("LeftLeg").z + h("RightLeg").z) / 2,
        "bilek_ayak": (h("LeftFoot").z + h("RightFoot").z) / 2,
        "el_sol": h("LeftHand"), "el_sag": h("RightHand"),
        "x0": h("Hips").x, "y0": h("Hips").y,
        "on_y": -1.0,   # MPFB dinlenmede −y'ye bakar
    }


def _pay_grubu(ob, ad, f):
    """Köşe grubunu z'nin işlevi olan ağırlıkla doldur (ör. paçaya doğru artan bolluk)."""
    g = ob.vertex_groups.new(name=ad)
    Mw = ob.matrix_world
    for v in ob.data.vertices:
        w = f((Mw @ v.co).z)
        if w > 0:
            g.add([v.index], min(1.0, w), 'REPLACE')
    return ad


# ---------------------------------------------------------------- parçalar
EL = ("LeftHand", "RightHand") + tuple(s + "Hand" + f + n for s in ("Left", "Right") for f in ("Thumb", "Index", "Middle", "Ring", "Pinky") for n in "123")
BAS = ("Head", "Neck")


def ceket_ust(gov, O, ad, v_acik=None, yaka_bosluk=0.015):
    """Ceketin üstü: gövde ve kollar (bel–boyun), eller ve boyun hariç. v_acik: (düğme z'si, V genişliği/yükseklik) ön açıklık."""
    def sec(v, z, x, y, gi):
        if not _grupta(v, "body", gi):
            return False
        if z < O["bel"] - 0.11 or z > O["boyun"] - yaka_bosluk:
            return False
        if _agirlik(v, EL + BAS, gi) > 0.3:
            return False
        for e in (O["el_sol"], O["el_sag"]):   # kol ağzı bilekten 3 cm geride
            if (Vector((x, y, z)) - e).length < 0.045:
                return False
        if v_acik:
            dz, gen = v_acik
            on = (y - O["y0"]) < -0.04
            if on and z > dz and abs(x - O["x0"]) < (z - dz) * gen + 0.004:
                return False
        return True
    return kes(gov, ad, sec)


def ceket_etek(gov, O, ad, boy, on_aciklik=0.0):
    """Ceket eteği: belden kalçanın altına (helper-skirt), önde isteğe bağlı açılan kesim."""
    alt = O["kasik"] - boy
    def sec(v, z, x, y, gi):
        if not _grupta(v, "helper-skirt", gi):
            return False
        if z < alt or z > O["bel"] + 0.06:
            return False
        if on_aciklik and (y - O["y0"]) < -0.04 and abs(x - O["x0"]) < (O["bel"] - z) * on_aciklik + 0.003:
            return False
        return True
    return kes(gov, ad, sec)


def yelek(gov, O, ad, dz):
    def sec(v, z, x, y, gi):
        if not _grupta(v, "body", gi) or z < O["bel"] - 0.03 or z > O["boyun"] - 0.005:
            return False
        if _agirlik(v, EL + BAS + ("LeftArm", "RightArm", "LeftForeArm", "RightForeArm"), gi) > 0.25:
            return False
        on = (y - O["y0"]) < -0.04
        if on and z > dz and abs(x - O["x0"]) < (z - dz) * 0.35 + 0.004:
            return False
        return True
    return kes(gov, ad, sec)


def yaka(gov, O, ad, yuk=0.045, on_bosluk=0.0):
    """Dik yaka (ya da gömlek yakası): boyun dibinde dar halka; önde isteğe bağlı küçük boşluk."""
    def sec(v, z, x, y, gi):
        if not _grupta(v, "body", gi):
            return False
        if z < O["boyun"] - 0.04 or z > min(O["boyun"] - 0.04 + yuk, O["cene"] - 0.006):
            return False
        if on_bosluk and (y - O["y0"]) < -0.03 and abs(x - O["x0"]) < on_bosluk:
            return False
        return True
    return kes(gov, ad, sec)


def kravat(gov, O, ad, ust, alt, gen=0.014):
    """İnce kravat: yakadan yeleğin açıklığına inen dar ön şerit."""
    def sec(v, z, x, y, gi):
        return (_grupta(v, "body", gi) and alt < z < ust and abs(x - O["x0"]) < gen and (y - O["y0"]) < -0.05)
    return kes(gov, ad, sec)


def mansetler(gov, O, ad):
    def sec(v, z, x, y, gi):
        if not _grupta(v, "body", gi) or _agirlik(v, EL, gi) > 0.5:
            return False
        p = Vector((x, y, z))
        return any(0.035 < (p - e).length < 0.06 for e in (O["el_sol"], O["el_sag"]))
    return kes(gov, ad, sec)


def pantolon(gov, O, ad):
    def sec(v, z, x, y, gi):
        return _grupta(v, "helper-tights", gi) and O["bilek_ayak"] - 0.02 < z < O["bel"] - 0.13   # bel ceket eteğinin içinde kalır
    return kes(gov, ad, sec)


def ayakkabi(gov, O, ad):
    def sec(v, z, x, y, gi):
        return _grupta(v, "body", gi) and z < O["bilek_ayak"] + 0.035 and _agirlik(v, ("LeftFoot", "RightFoot", "LeftToeBase", "RightToeBase"), gi) > 0.4
    return kes(gov, ad, sec)


def yama_cep(gov, O, ad, merkez_x, z0, z1, gen=0.075):
    """Bourgeron'un yama cebi: eteğin önünden kesilmiş küçük dikdörtgen (eteğin biraz dışında)."""
    def sec(v, z, x, y, gi):
        return (_grupta(v, "helper-skirt", gi) and z0 < z < z1 and abs(x - (O["x0"] + merkez_x)) < gen and (y - O["y0"]) < -0.02)
    return kes(gov, ad, sec)


# ---------------------------------------------------------------- takımlar
def theo_takim(gov, isk):
    O = olc(isk, gov)
    koyu = kumas("yun_koyu", (0.032, 0.030, 0.034), 0.8, 0.4)
    yelek_m = kumas("yelek_yun", (0.045, 0.042, 0.045), 0.75, 0.35)
    beyaz = kumas("kolali_yaka", (0.80, 0.79, 0.76), 0.45, 0.0)
    kravat_m = kumas("kravat_ipek", (0.025, 0.024, 0.028), 0.4, 0.2)
    pant = kumas("pantolon_yun", (0.03, 0.029, 0.032), 0.8, 0.4)
    deri = kumas("ayakkabi_deri", (0.022, 0.018, 0.016), 0.35, 0.0)
    dugme = O["gogus"] - 0.02
    L = []
    L.append(boya(bitir(ceket_ust(gov, O, "ceket_ust", v_acik=(dugme, 0.42)), 0.010, 0.005, 0.004), koyu, "giysi"))
    e = ceket_etek(gov, O, "ceket_etek", 0.03, on_aciklik=0.35)
    eg = _pay_grubu(e, "etek_bol", lambda z: max(0.0, min(1.0, (O["bel"] - 0.04 - z) / 0.12)))   # belde dar, aşağı bollaşır
    L.append(boya(bitir(e, 0.006, 0.005, 0.004, pay_grubu=eg, ek_pay=0.016), koyu, "giysi"))
    L.append(boya(bitir(yelek(gov, O, "yelek", dugme + 0.05), 0.008, 0.003, 0.002), yelek_m, "giysi"))
    L.append(boya(bitir(yaka(gov, O, "dik_yaka", 0.05, on_bosluk=0.008), 0.009, 0.003, 0.0), beyaz, "yaka"))
    L.append(boya(bitir(kravat(gov, O, "kravat", O["boyun"] + 0.01, dugme + 0.04), 0.012, 0.003, 0.0), kravat_m, "giysi"))
    L.append(boya(bitir(mansetler(gov, O, "manset"), 0.010, 0.003, 0.0), beyaz, "yaka"))
    p = pantolon(gov, O, "pantolon")
    pg = _pay_grubu(p, "paca", lambda z: max(0.0, (O["diz"] - z) / max(1e-3, O["diz"] - O["bilek_ayak"])) * 0.8 + max(0.0, (z - O["diz"])) * 0)
    L.append(boya(bitir(p, 0.014, 0.004, 0.004, pay_grubu=pg, ek_pay=0.012), pant, "giysi"))
    L.append(boya(bitir(ayakkabi(gov, O, "ayakkabi"), 0.008, 0.004, 0.0), deri, "giysi"))
    return L


def vincent_takim(gov, isk):
    O = olc(isk, gov)
    mavi = kumas("bourgeron_pamuk", (0.09, 0.16, 0.30), 0.9, 0.25)
    mavi_k = kumas("bourgeron_yaka", (0.075, 0.13, 0.25), 0.9, 0.25)
    keten = kumas("keten_gomlek", (0.62, 0.60, 0.53), 0.8, 0.2)
    bag = kumas("boyun_bagi", (0.05, 0.05, 0.06), 0.6, 0.2)
    pant = kumas("pantolon_kadife", (0.06, 0.052, 0.045), 0.9, 0.5)
    deri = kumas("ayakkabi_deri", (0.03, 0.022, 0.018), 0.4, 0.0)
    L = []
    # bol: ceket üstü daha geniş pay; etek kalçayı örter, önü kapalı
    L.append(boya(bitir(ceket_ust(gov, O, "bourgeron_ust", v_acik=(O["boyun"] - 0.07, 0.25)), 0.016, 0.004, 0.006), mavi, "giysi"))
    e = ceket_etek(gov, O, "bourgeron_etek", 0.07, on_aciklik=0.0)
    eg = _pay_grubu(e, "etek_bol", lambda z: max(0.0, min(1.0, (O["bel"] - 0.04 - z) / 0.12)))
    L.append(boya(bitir(e, 0.012, 0.004, 0.006, pay_grubu=eg, ek_pay=0.022), mavi, "giysi"))
    for i, mx in enumerate((-0.115, 0.115)):   # iki yama cep (kalçada, ayrık)
        L.append(boya(bitir(yama_cep(gov, O, "cep%d" % i, mx, O["kasik"] + 0.0, O["kasik"] + 0.10, gen=0.045), 0.040, 0.003, 0.0), mavi_k, "giysi"))
    L.append(boya(bitir(yaka(gov, O, "devrik_yaka", 0.03, on_bosluk=0.03), 0.019, 0.004, 0.002), mavi_k, "giysi"))
    L.append(boya(bitir(yaka(gov, O, "gomlek_yaka", 0.045, on_bosluk=0.012), 0.012, 0.003, 0.0), keten, "yaka"))
    L.append(boya(bitir(kravat(gov, O, "boyun_bagi", O["boyun"] - 0.005, O["boyun"] - 0.06, 0.010), 0.016, 0.003, 0.0), bag, "giysi"))
    p = pantolon(gov, O, "pantolon")
    pg = _pay_grubu(p, "paca", lambda z: max(0.0, (O["diz"] + 0.15 - z) / max(1e-3, O["diz"] + 0.15 - O["bilek_ayak"])))
    L.append(boya(bitir(p, 0.014, 0.004, 0.005, pay_grubu=pg, ek_pay=0.008), pant, "giysi"))
    L.append(boya(bitir(ayakkabi(gov, O, "ayakkabi"), 0.009, 0.004, 0.0), deri, "giysi"))
    return L


# ---------------------------------------------------------------- yüz (kaynağa göre)
def yuz_ayari(gov, kim):
    """Yüz oranları kamu malı kaynağa göre (otoportre / fotoğraf); yaşayan birine benzetilmez."""
    try:
        from bl_ext.user_default.mpfb.services import TargetService
    except Exception:
        return
    ayar = {
        "vincent": {"cheek/l-cheek-bones-incr": 0.7, "cheek/r-cheek-bones-incr": 0.7, "cheek/l-cheek-volume-decr": 0.6,
                    "cheek/r-cheek-volume-decr": 0.6, "chin/chin-jutting-incr": 0.3, "nose/nose-hump-incr": 0.3},
        "theo": {"cheek/l-cheek-volume-decr": 0.25, "cheek/r-cheek-volume-decr": 0.25, "head/head-oval": 0.4},
    }.get(kim, {})
    for ad, w in ayar.items():
        try:
            yol = TargetService.target_full_path(ad)
            if yol:
                TargetService.load_target(gov, yol, weight=w, name=ad.replace("/", "-"))
        except Exception as e:
            print("yüz hedefi yok:", ad, e)
