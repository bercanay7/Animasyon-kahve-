# -*- coding: utf-8 -*-
"""Van Gogh v4 karakterleri: MPFB2 (MakeHuman, CC0 insanlar) + MakeHuman varlık paketleri.

Blender içinden kullanılır:  from karakter import theo, vincent, jo, bebek
Her işlev (iskelet, gövde, [parçalar]) döndürür; iskelet "mixamo" (Mixamo hareketleri doğrudan uyar).
Varlıklar: MPFB kullanıcı verisi (makehuman_system_assets, suits01, dress03, hair01, bodyparts05, skins01/02).
Lisanslar ve kayıt: araclar/ASSETS.md.
"""
import math
import bpy
from mathutils import Vector

from bl_ext.user_default.mpfb.services import HumanService, ObjectService


def _ad(x):
    return "%s/%s.mhclo" % (x, x)


def _insan(isim, fenotip, deri, sac, kas, ekler, giysiler, goz="brown"):
    info = {
        "name": isim,
        "phenotype": fenotip,
        "rig": "mixamo",
        "eyes": "high-poly/high-poly.mhclo",
        "eyebrows": _ad(kas),
        "eyelashes": _ad("eyelashes01"),
        "teeth": _ad("teeth_base"),
        "tongue": _ad("tongue01"),
        "hair": _ad(sac) if sac else "",
        "proxy": "",
        "targets": [],
        "clothes": [_ad(g) for g in ekler + giysiler],
        "skin_mhmat": "%s/%s.mhmat" % (deri, deri),
        "skin_material_type": "ENHANCED_SSS",
        "eyes_material_type": "MAKESKIN",
        "eyes_material_settings": {},
        "skin_material_settings": {},
        "expressions": [],
        "alternative_materials": {},
        "color_adjustments": {},
    }
    ayar = HumanService.get_default_deserialization_settings()
    ayar["subdiv_levels"] = 1
    govde = HumanService.deserialize_from_dict(info, ayar)
    iskelet = ObjectService.find_object_of_type_amongst_nearest_relatives(govde, "Skeleton")
    parcalar = [o for o in bpy.data.objects if o.parent in (govde, iskelet) and o.type == 'MESH']
    try:  # göz rengi
        from bl_ext.user_default.mpfb.services import AssetService, MaterialService
        gozler = [o for o in parcalar if "eye" in o.name.lower() and "brow" not in o.name.lower() and "lash" not in o.name.lower()]
    except Exception:
        pass
    return iskelet, govde, parcalar


def _yas(yil):
    """MakeHuman yaş kaydırıcısı: 0→1, 0.1875→11, 0.5→25, 1→90 yaş."""
    if yil <= 25:
        return 0.1875 + (yil - 11) / 14 * 0.3125 if yil >= 11 else (yil - 1) / 10 * 0.1875
    return 0.5 + (yil - 25) / 65 * 0.5


def _fen(cins, yil, kilo=0.5, kas=0.5, boy=0.5, oran=0.6):
    return {"gender": cins, "age": _yas(yil), "muscle": kas, "weight": kilo, "proportions": oran,
            "height": boy, "cupsize": 0.5, "firmness": 0.5,
            "race": {"asian": 0.0, "caucasian": 1.0, "african": 0.0}}


# ---------------------------------------------------------------- renk ayarı
def boya(obj, renk, oran=1.0, doygunluk=None, parlaklik=None):
    """Giysi malzemesinin temel rengini çarpımla tonla (doku korunur)."""
    for sl in obj.material_slots:
        m = sl.material
        if not m or not m.node_tree:
            continue
        nt, ln = m.node_tree.nodes, m.node_tree.links
        bsdfs = [n for n in nt if n.type == 'BSDF_PRINCIPLED']
        for b in bsdfs:
            inp = b.inputs['Base Color']
            kaynak = inp.links[0].from_socket if inp.is_linked else None
            hs = nt.new('ShaderNodeHueSaturation')
            if doygunluk is not None:
                hs.inputs['Saturation'].default_value = doygunluk
            if parlaklik is not None:
                hs.inputs['Value'].default_value = parlaklik
            if kaynak:
                ln.new(kaynak, hs.inputs['Color'])
            else:
                hs.inputs['Color'].default_value = inp.default_value
            mx = nt.new('ShaderNodeMix')
            mx.data_type = 'RGBA'
            mx.blend_type = 'MULTIPLY'
            mx.inputs['Factor'].default_value = oran
            ln.new(hs.outputs['Color'], mx.inputs['A'])
            mx.inputs['B'].default_value = (*renk, 1)
            ln.new(mx.outputs['Result'], inp)


def renklendir(obj, renk, alt=0.55, ust=1.25, kaynak_ust=0.35):
    """Koyu dokularda (saç, sakal, siyah elbise) rengi yerine koy: doku parlaklığı yalnız gölge-ışık
    farkı olarak kalır (renk × [alt..ust]); alfa ve normal korunur."""
    for sl in obj.material_slots:
        m = sl.material
        if not m or not m.node_tree:
            continue
        nt, ln = m.node_tree.nodes, m.node_tree.links
        for bb in [n for n in nt if n.type == 'BSDF_PRINCIPLED']:
            inp = bb.inputs['Base Color']
            tex = [n for n in nt if n.type == 'TEX_IMAGE' and n.image and 'nrm' not in n.image.name.lower()
                   and 'normal' not in n.image.name.lower() and 'bump' not in n.image.name.lower()
                   and 'spec' not in n.image.name.lower() and 'metal' not in n.image.name.lower()]
            bw = nt.new('ShaderNodeRGBToBW')
            if tex:
                ln.new(tex[0].outputs['Color'], bw.inputs['Color'])
            mr = nt.new('ShaderNodeMapRange')
            mr.inputs['From Min'].default_value = 0.0
            mr.inputs['From Max'].default_value = kaynak_ust
            mr.inputs['To Min'].default_value = alt
            mr.inputs['To Max'].default_value = ust
            ln.new(bw.outputs['Val'], mr.inputs['Value'])
            mx = nt.new('ShaderNodeMix')
            mx.data_type = 'RGBA'
            mx.blend_type = 'MULTIPLY'
            mx.inputs['Factor'].default_value = 1.0
            mx.inputs['A'].default_value = (*renk, 1)
            ln.new(mr.outputs['Result'], mx.inputs['B'])
            ln.new(mx.outputs['Result'], inp)


def bul(parcalar, *anahtar):
    return [o for o in parcalar if any(a in o.name.lower() for a in anahtar)]


# ---------------------------------------------------------------- karakterler
def theo(yil=31):
    """Theo: ince, orta boy; açık kumral saç, bıyık ve kısa sakal; koyu takım, beyaz yaka, ince kravat."""
    isk, gov, p = _insan("Theo", _fen(1.0, yil, kilo=0.38, kas=0.45, boy=0.48), "young_caucasian_male",
                         "short02", "eyebrow006", ["wdg_scruffy_beard", "rehmanpolanski_moustache_viking"],
                         ["toigo_male_suit_tie_and_jacket", "shoes02"])
    for o in bul(p, "short02"):
        renklendir(o, (0.30, 0.19, 0.10), kaynak_ust=0.5)
    for o in bul(p, "beard", "moustache"):
        renklendir(o, (0.26, 0.16, 0.08), kaynak_ust=0.3)
    for o in bul(p, "suit"):
        boya(o, (0.55, 0.53, 0.55), doygunluk=0.3)
    return isk, gov, p


def vincent(yil=34):
    """Vincent: kızıl saç ve sakal, sert yüz; mavi iş ceketi (hasır şapka sahnede ayrıca)."""
    isk, gov, p = _insan("Vincent", _fen(1.0, yil, kilo=0.42, kas=0.55, boy=0.47, oran=0.55),
                         "toigo_light_skin_male_ginger", "short04", "eyebrow010", ["wdg_scruffy_beard"],
                         ["male_casualsuit01", "shoes02"], goz="bluegreen")
    for o in bul(p, "short04"):
        renklendir(o, (0.42, 0.13, 0.035), kaynak_ust=0.5)
    for o in bul(p, "beard"):
        renklendir(o, (0.40, 0.12, 0.03), kaynak_ust=0.3)
    for o in bul(p, "casualsuit"):
        boya(o, (0.55, 0.65, 1.0), doygunluk=1.2)
    return isk, gov, p


def jo(yil=27):
    """Jo: koyu saç, ensede topuz; dik yakalı koyu lacivert elbise, etek bileğe."""
    isk, gov, p = _insan("Jo", _fen(0.0, yil, kilo=0.45, kas=0.4, boy=0.45), "young_caucasian_female",
                         "rehmanpolanski_hair_bun_brown", "eyebrow002", [], ["punkduck_medieval_dress", "shoes01"])
    for o in bul(p, "bun"):
        renklendir(o, (0.07, 0.045, 0.03), kaynak_ust=0.6)
    for o in bul(p, "dress"):
        # düz koyu lacivert-gri: dokudaki açık şerit bastırılır (koyu giysi + açık dikey şerit = haç)
        renklendir(o, (0.075, 0.085, 0.13), alt=0.85, ust=1.05, kaynak_ust=1.0)
    return isk, gov, p


def bebek():
    """Bebek (1890): MakeHuman'ın en küçük yaşı (1); kundak sahnede ayrıca, yalnız baş görünür."""
    return _insan("Bebek", _fen(0.5, 1, kilo=0.6, kas=0.3, boy=0.5, oran=0.5), "young_caucasian_male",
                  "", "eyebrow001", [], [])
