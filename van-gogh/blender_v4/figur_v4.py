# -*- coding: utf-8 -*-
"""Van Gogh Y4: Blender yalnız figür üretir (GOREV_3_kapi.md).

v3 kliplerinin sözleşmesi korunur (van-gogh/blender/figur_bpy.py): aynı eklem verisi (eklem.json, 121 kare, 15 fps),
aynı kamera (kamera.json: konum, hedef, dikey fov), aynı eksen (bizim x, y, z → Blender x, −z, y), 960×540 saydam kare.
Figür MPFB2 (MakeHuman) insanı; eklemlere oturtulur: kök ve gövde çerçevelerden, el ve ayak iki kemik IK ile.

  blender -b -P van-gogh/blender_v4/figur_v4.py -- --klip theo_oda [--kareler 0:121]
Çıktı: van-gogh/blender/v4_klip_<ad>/kare/k_0000.png (RGBA), normal/n_0000.png (kamera uzayı, n·0.5+0.5),
       kimlik/i_0000.png (ten 255,0,0 · saç/sakal 0,255,0 · giysi 0,0,255 · yaka/gömlek 255,255,0 · şapka 255,0,255 · eldeki nesne 0,255,255),
       bilgi.json.
"""
import bpy
import bmesh
import json
import math
import os
import sys
import time
from mathutils import Vector, Matrix, Quaternion

BURA = os.path.dirname(os.path.abspath(__file__))
DEPO = os.path.abspath(os.path.join(BURA, "..", ".."))
V3 = os.path.join(DEPO, "van-gogh", "blender")
sys.path.insert(0, BURA)
import karakter as K                       # noqa: E402
import poz                                 # noqa: E402
from poz import P, UP                      # noqa: E402

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []


def arg(ad, v=None):
    return argv[argv.index("--" + ad) + 1] if "--" + ad in argv else v


KLIPLER = {
    "theo_oda": {"eklem": os.path.join(V3, "eklem_oda.json"), "kamera": os.path.join(V3, "kamera_oda.json"), "kisi": "theo", "zarf": True},
    "theo_dur": {"eklem": os.path.join(V3, "klip_theo_dur", "eklem.json"), "kamera": os.path.join(V3, "klip_theo_dur", "kamera.json"), "kisi": "theo"},
    "vincent_goster": {"eklem": os.path.join(V3, "klip_vincent_goster", "eklem.json"), "kamera": os.path.join(V3, "klip_vincent_goster", "kamera.json"),
                       "kisi": "vincent", "goster": (2.0, 3.2)},
}
AD = arg("klip", "theo_dur")
KL = KLIPLER[AD]
D = json.load(open(KL["eklem"], encoding="utf-8"))
KAM = json.load(open(KL["kamera"], encoding="utf-8"))
CIKTI = os.path.join(V3, "v4_klip_" + AD)
FPS = 15
ORNEK = int(arg("ornek", "32"))
OMUZ_ORAN = float(arg("omuz", "0.66"))   # köprücüğü eklem omzuna çevirme oranı (1: tam; omuz kalkık durursa azaltılır)

B = lambda p: Vector((p[0], -p[2], p[1]))   # bizim eksen → Blender


def cer(c):
    """Eklem çerçevesi → (köken, 3×3 döndürme: sütunlar x, y, z). x = figürün solu, y = yukarı, z = yüzün baktığı yön."""
    x, y, z = B(c['x']).normalized(), B(c['y']).normalized(), B(c['z']).normalized()
    return B(c['o']), Matrix((x, y, z)).transposed()


# ================================================================ malzeme yardımcıları
def nodes(m):
    return m.node_tree.nodes, m.node_tree.links


def bsdf_bul(m):
    b = [n for n in m.node_tree.nodes if n.type == 'BSDF_PRINCIPLED']
    return b[0] if b else None


def renk_doku(m):
    for n in m.node_tree.nodes:
        if n.type == 'TEX_IMAGE' and n.image:
            ad = n.image.name.lower()
            if not any(k in ad for k in ("norm", "nrm", "bump", "spec", "metal", "_h.", "_hn", "_s.")):
                return n
    return None


def duz_renk(obj, renk, puruz=0.75, sheen=0.3, kategori=None):
    """Malzemeyi düz renge çevir (doku parlaklığı yalnız çok hafif); alfa ve normal korunur."""
    for sl in obj.material_slots:
        m = sl.material
        if not m:
            continue
        nt, ln = nodes(m); b = bsdf_bul(m)
        t = renk_doku(m)
        if t is not None:
            bw = nt.new('ShaderNodeRGBToBW'); ln.new(t.outputs['Color'], bw.inputs['Color'])
            mr = nt.new('ShaderNodeMapRange'); mr.inputs['To Min'].default_value = 0.85; mr.inputs['To Max'].default_value = 1.1
            ln.new(bw.outputs['Val'], mr.inputs['Value'])
            mx = nt.new('ShaderNodeMix'); mx.data_type = 'RGBA'; mx.blend_type = 'MULTIPLY'; mx.inputs['Factor'].default_value = 1
            mx.inputs['A'].default_value = (*renk, 1); ln.new(mr.outputs['Result'], mx.inputs['B'])
            ln.new(mx.outputs['Result'], b.inputs['Base Color'])
        else:
            for l in list(b.inputs['Base Color'].links): ln.remove(l)
            b.inputs['Base Color'].default_value = (*renk, 1)
        b.inputs['Roughness'].default_value = puruz
        b.inputs['Sheen Weight'].default_value = sheen
        b.inputs['Metallic'].default_value = 0.0
        try:
            for l in list(b.inputs['Specular IOR Level'].links): ln.remove(l)
            b.inputs['Specular IOR Level'].default_value = 0.3
        except Exception:
            pass
    if kategori:
        obj["kimlik"] = kategori


def giysi_bolgeli(obj, renkler, esikler):
    """Takımı bölgelere ayırıp düz renklere çevir. Bölgeler doku parlaklığı ve özgün (generated) yükseklikten:
    acik  = gömlek/yaka bölgesi (parlak doku);  kirmizi = kravat (doygun kırmızı, varsa);
    gz < esikler['etek'] → pantolon; acik ve gz < esikler['yelek'] → yelek ya da ceket (beyaz yalnız yakada kalır)."""
    for sl in obj.material_slots:
        m = sl.material
        if not m:
            continue
        nt, ln = nodes(m); b = bsdf_bul(m); t = renk_doku(m)
        tc = nt.new('ShaderNodeTexCoord'); sep = nt.new('ShaderNodeSeparateXYZ'); ln.new(tc.outputs['Generated'], sep.inputs['Vector'])
        bw = nt.new('ShaderNodeRGBToBW'); ln.new(t.outputs['Color'], bw.inputs['Color'])
        hsv = nt.new('ShaderNodeSeparateColor'); hsv.mode = 'HSV'; ln.new(t.outputs['Color'], hsv.inputs['Color'])

        def esik(sok, a, b_, ad):
            mr = nt.new('ShaderNodeMapRange'); mr.name = ad
            mr.inputs['From Min'].default_value = a; mr.inputs['From Max'].default_value = b_
            ln.new(sok, mr.inputs['Value']); return mr.outputs['Result']

        def carp(a, b_, ad=None):
            n = nt.new('ShaderNodeMath'); n.operation = 'MULTIPLY'; n.use_clamp = True
            if ad: n.name = ad
            ln.new(a, n.inputs[0]); ln.new(b_, n.inputs[1]); return n.outputs['Value']

        def ters(a):
            n = nt.new('ShaderNodeMath'); n.operation = 'SUBTRACT'; n.inputs[0].default_value = 1.0
            ln.new(a, n.inputs[1]); return n.outputs['Value']

        acik = esik(bw.outputs['Val'], esikler.get('acik', 0.45), esikler.get('acik', 0.45) + 0.12, "m_acik")
        ust = esik(sep.outputs['Z'], esikler['yelek'], esikler['yelek'] + 0.01, "m_ust")         # yaka bölgesi
        yaka = carp(acik, ust, "m_yaka")                                                            # beyaz yalnız yakada
        alt = ters(esik(sep.outputs['Z'], esikler['etek'], esikler['etek'] + 0.01, "m_ustgovde"))  # pantolon
        kir = carp(esik(hsv.outputs['Green'], 0.35, 0.55, "m_doy"), esik(bw.outputs['Val'], 0.12, 0.2, "m_kirp"))  # kravat (kırmızı)
        hue = esik(hsv.outputs['Red'], 0.08, 0.06, "m_hue")   # kırmızı tonu (0'a yakın)
        kir = carp(kir, hue, "m_kravat")
        yelek = carp(carp(acik, ters(ust)), ters(alt), "m_yelek")

        def mixc(fac, a_sok, b_renk, ad):
            mx = nt.new('ShaderNodeMix'); mx.data_type = 'RGBA'; mx.name = ad
            ln.new(fac, mx.inputs['Factor'])
            if isinstance(a_sok, tuple): mx.inputs['A'].default_value = (*a_sok, 1)
            else: ln.new(a_sok, mx.inputs['A'])
            mx.inputs['B'].default_value = (*b_renk, 1)
            return mx.outputs['Result']
        c = mixc(yelek, renkler['ceket'], renkler['yelek'], "r_yelek")
        c = mixc(kir, c, renkler['kravat'], "r_kravat")
        c = mixc(yaka, c, renkler['yaka'], "r_yaka")
        c = mixc(alt, c, renkler['pantolon'], "r_pantolon")
        # çok hafif doku değeri (kıvrım gölgesi okunsun, desen okunmasın)
        mr = nt.new('ShaderNodeMapRange'); mr.inputs['From Min'].default_value = 0.0; mr.inputs['From Max'].default_value = 1.0
        mr.inputs['To Min'].default_value = 0.9; mr.inputs['To Max'].default_value = 1.08; ln.new(bw.outputs['Val'], mr.inputs['Value'])
        mm = nt.new('ShaderNodeMix'); mm.data_type = 'RGBA'; mm.blend_type = 'MULTIPLY'; mm.inputs['Factor'].default_value = 1
        ln.new(c, mm.inputs['A']); ln.new(mr.outputs['Result'], mm.inputs['B'])
        ln.new(mm.outputs['Result'], b.inputs['Base Color'])
        b.inputs['Roughness'].default_value = 0.8; b.inputs['Sheen Weight'].default_value = 0.35
        try:
            for l in list(b.inputs['Specular IOR Level'].links): ln.remove(l)
            b.inputs['Specular IOR Level'].default_value = 0.3
        except Exception:
            pass
        m["yaka_maske"] = "m_yaka"
    obj["kimlik"] = "giysi"


# ================================================================ karakterler (dönem)
def _sakal_kisalt(govde, sakal, alt_pay=0.035):
    """Viking sakalını çene altında kes: kısa, dolgun, çeneyi ve dudak altını örten sakal."""
    bpy.context.view_layer.update()
    isk = sakal.parent
    bas = isk.matrix_world @ isk.pose.bones[P + "Head"].head
    sinir = bas.z - alt_pay
    bm = bmesh.new(); bm.from_mesh(sakal.data)
    Mw = sakal.matrix_world
    sil = [v for v in bm.verts if (Mw @ v.co).z < sinir]
    bmesh.ops.delete(bm, geom=sil, context='VERTS')
    bm.to_mesh(sakal.data); bm.free()


def kisi_kur(kim):
    if kim == "theo":
        isk, gov, p = K._insan("Theo", K._fen(1.0, 31, kilo=0.38, kas=0.45, boy=0.48), "young_caucasian_male", "short01", "eyebrow006",
                               ["rehmanpolanski_beard_viking", "rehmanpolanski_moustache_viking"], ["male_elegantsuit01", "shoes02"])
        sac = (0.30, 0.20, 0.11); takim = {"ceket": (0.035, 0.033, 0.036), "yelek": (0.04, 0.038, 0.04), "kravat": (0.03, 0.028, 0.03),
                                            "yaka": (0.80, 0.79, 0.76), "pantolon": (0.03, 0.029, 0.032)}
        esik = {"yelek": 0.905, "etek": 0.47, "acik": 0.45}
        takim_ad = "elegantsuit"
    else:
        isk, gov, p = K._insan("Vincent", K._fen(1.0, 37, kilo=0.42, kas=0.55, boy=0.47, oran=0.55), "toigo_light_skin_male_ginger", "short02", "eyebrow010",
                               ["rehmanpolanski_beard_viking", "rehmanpolanski_moustache_viking"], ["toigo_male_suit_3", "shoes02"])
        sac = (0.36, 0.11, 0.03); takim = {"ceket": (0.10, 0.17, 0.32), "yelek": (0.10, 0.17, 0.32), "kravat": (0.05, 0.05, 0.06),
                                            "yaka": (0.68, 0.66, 0.60), "pantolon": (0.06, 0.055, 0.05)}
        esik = {"yelek": 0.905, "etek": 0.47, "acik": 0.5}
        takim_ad = "suit_3"
    for o in p:
        n = o.name.lower()
        if n.endswith(".body"):
            o["kimlik"] = "ten"
            for sl in o.material_slots:
                b = bsdf_bul(sl.material)
                if b:
                    try: b.inputs['Subsurface Weight'].default_value = 0.15
                    except Exception: pass
        elif any(k in n for k in ("short", "eyebrow", "eyelash", "beard", "moustache")):
            duz_renk(o, sac if "lash" not in n else (0.05, 0.04, 0.035), 0.7, 0.4, "sac")
        elif takim_ad in n:
            giysi_bolgeli(o, takim, esik)
        elif "shoes" in n:
            duz_renk(o, (0.03, 0.025, 0.022), 0.5, 0.0, "giysi")
        else:   # göz, diş, dil
            o["kimlik"] = "ten"
    sakal = [o for o in p if "beard" in o.name.lower()][0]
    _sakal_kisalt(gov, sakal)
    return isk, gov, p


def hasir_sapka():
    """Alçak tepeli, geniş ama düz kenarlı açık hasır şapka; tepe yumuşak, hafif çökük (kovboy değil: kenar kıvrık değil)."""
    prof = [(0.0, 0.080), (0.045, 0.085), (0.080, 0.084), (0.098, 0.070), (0.104, 0.035), (0.106, 0.0),
            (0.13, -0.002), (0.165, -0.006), (0.172, -0.010), (0.166, -0.013), (0.12, -0.007), (0.104, -0.004), (0.100, 0.0)]
    me = bpy.data.meshes.new("sapka"); bm = bmesh.new(); n = 48; h = []
    for i in range(n):
        a = 2 * math.pi * i / n
        h.append([bm.verts.new((r * math.cos(a) * 0.92, r * math.sin(a), z)) for r, z in prof])
    for i in range(n):
        for j in range(len(prof) - 1):
            bm.faces.new((h[i][j], h[(i + 1) % n][j], h[(i + 1) % n][j + 1], h[i][j + 1]))
    bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new("hasir_sapka", me); bpy.context.scene.collection.objects.link(ob)
    for p_ in ob.data.polygons: p_.use_smooth = True
    m = bpy.data.materials.new("hasir"); b = bsdf_bul(m); nt, ln = nodes(m)
    b.inputs['Base Color'].default_value = (0.62, 0.52, 0.32, 1); b.inputs['Roughness'].default_value = 0.85
    tc = nt.new('ShaderNodeTexCoord'); wv = nt.new('ShaderNodeTexWave'); wv.wave_type = 'RINGS'; wv.inputs['Scale'].default_value = 45
    ln.new(tc.outputs['Object'], wv.inputs['Vector'])
    bp = nt.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = 0.25
    ln.new(wv.outputs['Fac'], bp.inputs['Height']); ln.new(bp.outputs['Normal'], b.inputs['Normal'])
    ob.data.materials.append(m)
    sl = ob.modifiers.new("k", 'SOLIDIFY'); sl.thickness = 0.004
    ob["kimlik"] = "sapka"
    return ob


def zarf():
    me = bpy.data.meshes.new("zarf"); bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts:
        v.co = Vector((v.co.x * 0.11, v.co.y * 0.16, v.co.z * 0.003))
    bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new("zarf", me); bpy.context.scene.collection.objects.link(ob)
    m = bpy.data.materials.new("zarf"); b = bsdf_bul(m); b.inputs['Base Color'].default_value = (0.71, 0.39, 0.07, 1)  # ≈ #DBA84C
    b.inputs['Roughness'].default_value = 0.85; ob.data.materials.append(m)
    ob["kimlik"] = "nesne"
    return ob


# ================================================================ sahne: kamera ve ışık (figur_bpy.py ile aynı)
def sahne():
    sc = bpy.context.scene
    prefs = bpy.context.preferences.addons['cycles'].preferences
    prefs.compute_device_type = 'OPTIX'; prefs.get_devices()
    for d in prefs.devices: d.use = (d.type != 'CPU')
    sc.render.engine = 'CYCLES'; sc.cycles.device = 'GPU'; sc.cycles.samples = ORNEK; sc.cycles.use_denoising = True
    try: sc.cycles.denoiser = 'OPTIX'
    except Exception: pass
    sc.cycles.seed = 1888
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 960, 540, 100
    sc.render.film_transparent = True
    sc.render.image_settings.file_format = 'PNG'; sc.render.image_settings.color_mode = 'RGBA'; sc.render.image_settings.color_depth = '8'
    sc.view_settings.view_transform = 'Standard'
    cam = bpy.data.objects.new('kamera', bpy.data.cameras.new('kamera')); sc.collection.objects.link(cam); sc.camera = cam
    cam.data.sensor_fit = 'VERTICAL'; cam.data.clip_start = .1
    cam.location = B(KAM['konum']); yon = (B(KAM['hedef']) - B(KAM['konum'])).normalized()
    cam.rotation_euler = yon.to_track_quat('-Z', 'Y').to_euler(); cam.data.angle_y = math.radians(KAM['fov'])
    sun = bpy.data.objects.new('gunes', bpy.data.lights.new('gunes', 'SUN')); sc.collection.objects.link(sun)
    d = Vector((4, 100, 5.2)).normalized(); sun.rotation_euler = (-d).to_track_quat('-Z', 'Y').to_euler()
    sun.data.energy = 5.0; sun.data.color = (1, .68, .42); sun.data.angle = math.radians(1.5)
    w = bpy.data.worlds.new('gok'); sc.world = w
    bg = w.node_tree.nodes['Background']; bg.inputs[0].default_value = (.3, .2, .38, 1); bg.inputs[1].default_value = .22
    if KAM.get('dis'):
        DS = KAM['dis']; g_ = DS['gunes']; d = Vector((g_['yon'][0], -g_['yon'][2], g_['yon'][1])).normalized()
        sun.rotation_euler = (-d).to_track_quat('-Z', 'Y').to_euler(); sun.data.energy = g_['guc']; sun.data.color = tuple(g_['renk']); sun.data.angle = math.radians(8)
        bg.inputs[0].default_value = (.5, .5, .52, 1); bg.inputs[1].default_value = DS.get('ortam', .3)
    if KAM.get('isik'):
        IS = KAM['isik']; sun.data.energy = IS.get('gunes', 0.0)
        la = bpy.data.objects.new('lamba', bpy.data.lights.new('lamba', 'POINT')); sc.collection.objects.link(la)
        la.location = B(IS['konum']); la.data.energy = IS.get('guc', 120); la.data.color = tuple(IS.get('renk', (1, .78, .5)))
        la.data.shadow_soft_size = IS.get('boy', .06)
        bg.inputs[1].default_value = IS.get('ortam', .08)
    bpy.ops.mesh.primitive_plane_add(size=6); yer = bpy.context.object; yer.visible_camera = False; yer.name = "yer_sekme"
    my = bpy.data.materials.new('yer'); bsdf_bul(my).inputs['Base Color'].default_value = (.5, .32, .16, 1); yer.data.materials.append(my)
    yer["kimlik"] = "yok"
    return cam


# ================================================================ eklemlere oturtma
class Oturt:
    def __init__(self, isk, k0):
        self.isk = isk
        self.f = poz.Figur(isk)
        f = self.f
        # karakter dinlenme çerçevesi: x = sol, y = yukarı, z = ön
        on = f.on0; sol = UP.cross(on).normalized()
        self.Cr = Matrix((sol, UP, on)).transposed()
        # ölçek: kalça yüksekliği eklem pelvisine (ayak bileği yüksekliği farkı ayakta korunur)
        kalca = f.bas(P + "Hips").z
        self.s = (B(k0['pelvis']['o']).z) / kalca
        isk.scale = (isk.scale[0] * self.s,) * 3
        f.guncelle()
        self.bilek_h = (f.bas(P + "LeftFoot").z + f.bas(P + "RightFoot").z) / 2
        # dinlenme dünya dönüşleri (karakter çerçevesine göre)
        self.Rrel = {}
        for ad in ("Hips", "Spine", "Spine1", "Spine2", "Neck", "Head", "LeftFoot", "RightFoot", "LeftHand", "RightHand"):
            self.Rrel[ad] = self.Cr.inverted() @ (isk.matrix_world.to_3x3().normalized() @ isk.pose.bones[P + ad].matrix.to_3x3().normalized())
        self.hips_dinlen = isk.matrix_world.inverted() @ f.bas(P + "Hips")
        f.kaydet()   # temel = MPFB dinlenme pozu
        # uzuv uzunlukları eklem verisine esnetilir (çocuk kemik ölçeği devralmaz: el ve ayak bozulmaz)
        for yan in ("Left", "Right"):
            for c in ("Leg", "Foot", "ForeArm", "Hand"):
                isk.data.bones[P + yan + c].inherit_scale = 'NONE'
        self.esnek = ("UpLeg", "Leg", "Arm", "ForeArm")
        self.Rarm0 = isk.matrix_world.to_3x3().normalized()
        self.sapma = 0.0

    def hizala(self, ad, F):
        """Kemiğin dünya dönüşünü F (eklem çerçevesi) × dinlenme ilişkisine getir."""
        f = self.f
        pb = self.isk.pose.bones[P + ad]
        istenen = (F @ self.Rrel[ad]).to_quaternion()
        simdi = (self.isk.matrix_world.to_3x3().normalized() @ pb.matrix.to_3x3().normalized()).to_quaternion()
        q = istenen @ simdi.inverted()
        eks, aci = q.to_axis_angle()
        if aci > math.pi: aci -= 2 * math.pi
        f.dondur(P + ad, eks, aci)

    def iki_kemik(self, ust, orta, uc, hedef, kutup_nokta):
        f = self.f
        S = f.bas(P + ust); l1 = (f.bas(P + orta) - S).length; l2 = (f.bas(P + uc) - f.bas(P + orta)).length
        T = Vector(hedef); d = T - S; L = min(d.length, (l1 + l2) * 0.9995); dn = d.normalized()
        a = (l1 * l1 + L * L - l2 * l2) / (2 * L); h = math.sqrt(max(0.0, l1 * l1 - a * a))
        kp = Vector(kutup_nokta) - S
        k = (kp - dn * kp.dot(dn))
        k = k.normalized() if k.length > 1e-6 else Vector((0, 0, 1))
        E = S + dn * a + k * h
        f.yonelt(P + ust, E - S)
        f.yonelt(P + orta, (S + dn * L) - f.bas(P + orta))

    def kare(self, k):
        f = self.f; isk = self.isk
        f.sifirla()
        po, Fp = cer(k['pelvis'])
        # kök: iskelet nesnesi pelvis çerçevesine
        R = Fp @ self.Cr.inverted() @ self.Rarm0
        M = Matrix.Translation(po) @ R.to_4x4() @ Matrix.Translation(-(self.Rarm0 @ (self.hips_dinlen * 1.0)) * 0)  # konum aşağıda düzeltilir
        isk.matrix_world = Matrix.LocRotScale(Vector(), (Fp @ self.Cr.inverted() @ self.Rarm0).to_quaternion(), Vector((self.s,) * 3) * (isk.scale[0] / self.s))
        f.guncelle()
        # kök: eklem kalçaları pelvis hizasında; MPFB'de uyluk başları pelvis kemiğinin altında → iki uyluk başının ortası pelvise
        kalca_orta = (B(k['bacak'][0]['kalca']) + B(k['bacak'][1]['kalca'])) / 2
        isk.location += kalca_orta - (f.bas(P + "LeftUpLeg") + f.bas(P + "RightUpLeg")) / 2
        f.guncelle()
        # gövde zinciri: pelvis → göğüs arası yumuşak, boyun ve baş çerçeveye
        _, Fg = cer(k['gogus']); _, Fb = cer(k['boyun']); _, Fh = cer(k['bas'])
        qp, qg = Fp.to_quaternion(), Fg.to_quaternion()
        self.hizala("Spine", qp.slerp(qg, 0.34).to_matrix())
        self.hizala("Spine1", qp.slerp(qg, 0.67).to_matrix())
        self.hizala("Spine2", Fg)
        self.hizala("Neck", Fb)
        self.hizala("Head", Fh)
        # köprücük: kol kökünü eklemdeki omuz noktasına çevir
        for yan, c in zip(("Left", "Right"), k['kol']):
            ad = P + yan + "Shoulder"
            S0 = f.bas(ad); hedef = B(c['omuz']) - S0
            simdi = f.bas(P + yan + "Arm") - S0
            e = simdi.cross(hedef)
            if e.length > 1e-6:
                f.dondur(ad, e.normalized(), simdi.angle(hedef) * OMUZ_ORAN)
        # uzuv boyları: bu karenin eklem uzaklıklarına
        pbs = isk.pose.bones
        for yan in ("Left", "Right"):
            for c_ in self.esnek: pbs[P + yan + c_].scale = (1, 1, 1)
        f.guncelle()
        for yan, bb, cc in zip(("Left", "Right"), k['bacak'], k['kol']):
            ank = B(bb['bilek']) + UP * max(0.0, self.bilek_h - B(bb['bilek']).z)
            # kök (kalça, omuz) MPFB'nin kendi noktası; boy oradan eklemin diz/dirseğine
            hedefler = {"UpLeg": (f.bas(P + yan + "UpLeg"), B(bb['diz'])), "Leg": (B(bb['diz']), ank),
                        "Arm": (f.bas(P + yan + "Arm"), B(cc['dirsek'])), "ForeArm": (B(cc['dirsek']), B(cc['bilek']))}
            for c_, (u0, u1) in hedefler.items():
                ad = P + yan + c_
                rest = (f.bas(f.cocuk[ad]) - f.bas(ad)).length
                pbs[ad].scale = (1, (u1 - u0).length / rest, 1)
        f.guncelle()
        # bacaklar (0: sol, 1: sağ)
        hata = []
        for yan, b in zip(("Left", "Right"), k['bacak']):
            hedef = B(b['bilek']); hedef.z = max(hedef.z, 0) + self.bilek_h - B(b['bilek']).z * 0 - 0.0306 * 0
            hedef = B(b['bilek']) + UP * (self.bilek_h - B(b['bilek']).z) if B(b['bilek']).z < self.bilek_h else B(b['bilek'])
            self.iki_kemik(yan + "UpLeg", yan + "Leg", yan + "Foot", hedef, B(b['diz']))
            _, Fa = cer(b['ayak']); self.hizala(yan + "Foot", Fa)
            hata += [(f.bas(P + yan + "Leg") - B(b['diz'])).length, (f.bas(P + yan + "Foot") - hedef).length]
        # kollar (0: sol, 1: sağ)
        for yan, c in zip(("Left", "Right"), k['kol']):
            self.iki_kemik(yan + "Arm", yan + "ForeArm", yan + "Hand", B(c['bilek']), B(c['dirsek']))
            _, Fe = cer(c['el'])
            f.yonelt(P + yan + "Hand", Fe @ Vector((0, 1, 0)))
            hata += [(f.bas(P + yan + "ForeArm") - B(c['dirsek'])).length, (f.bas(P + yan + "Hand") - B(c['bilek'])).length]
        self.sapma = max(self.sapma, max(hata))
        kok = [(f.bas(P + y_ + "UpLeg") - B(b_['kalca'])).length for y_, b_ in zip(("Left", "Right"), k['bacak'])] +               [(f.bas(P + y_ + "Arm") - B(c_['omuz'])).length for y_, c_ in zip(("Left", "Right"), k['kol'])]
        self.kok_sapma = max(getattr(self, "kok_sapma", 0.0), max(kok))
        self.omuz_sapma = max(getattr(self, "omuz_sapma", 0.0), max(kok[2:]))
        self.kalca_sapma = max(getattr(self, "kalca_sapma", 0.0), max(kok[:2]))
        self.bilek_yukselt = max(getattr(self, "bilek_yukselt", 0.0), max(max(0.0, self.bilek_h - B(b_['bilek']).z) for b_ in k['bacak']))
        if os.environ.get("ZK_SAPMA"):
            print("SAPMA t=%.2f diz %.3f %.3f ayak %.3f %.3f | dirsek %.3f el %.3f | dirsek %.3f el %.3f" % ((k['t'],) + tuple(hata[i] for i in (0, 2, 1, 3, 4, 5, 6, 7))))
        return hata


def eller(f, yan, tur):
    """Dinlenme: 20–40° kademeli bükük, başparmak içe; tut: kâğıt kavrama; isaret: işaret parmağı düz, diğerleri kıvrık."""
    if tur == "dinlen":
        f.parmak(yan, (0.35, 0.55, 0.40), (0.25, 0.25, 0.2))
    elif tur == "tut":
        f.parmak(yan, (0.55, 0.85, 0.6), (0.45, 0.45, 0.3))
    elif tur == "isaret":
        n, _ = f.avuc(yan)
        for i, fn in enumerate(("Middle", "Ring", "Pinky")):
            for seg, aci in zip("123", (0.9, 1.2, 0.8)):
                ad = P + yan + "Hand" + fn + seg; e = f.uzuv(ad).cross(n)
                if e.length > 1e-6: f.dondur(ad, e.normalized(), aci)
        for seg, aci in zip("123", (0.05, 0.05, 0.05)):
            ad = P + yan + "HandIndex" + seg; e = f.uzuv(ad).cross(n)
            if e.length > 1e-6: f.dondur(ad, e.normalized(), aci)
        for seg, aci in zip("123", (0.5, 0.5, 0.3)):
            ad = P + yan + "HandThumb" + seg; e = f.uzuv(ad).cross(n)
            if e.length > 1e-6: f.dondur(ad, e.normalized(), aci)


# ================================================================ geçişler (RGBA, normal, kimlik)
KIMLIK_RENK = {"ten": (1, 0, 0), "sac": (0, 1, 0), "giysi": (0, 0, 1), "yaka": (1, 1, 0), "sapka": (1, 0, 1), "nesne": (0, 1, 1)}


def alfa_kaynagi(m):
    b = bsdf_bul(m)
    if not b:
        return None, 1.0
    a = b.inputs['Alpha']
    return (a.links[0].from_socket if a.is_linked else None), a.default_value


def gecis_malzemeleri(nesneler):
    """Her malzemenin normal ve kimlik kopyası (alfa korunur). Döndürür: {nesne: [(özgün, normal, kimlik), …]}."""
    tablo = {}
    for o in nesneler:
        kat = o.get("kimlik", "ten")
        lst = []
        for sl in o.material_slots:
            m = sl.material
            if not m:
                lst.append((None, None, None)); continue
            out = []
            for tur in ("normal", "kimlik"):
                c = m.copy(); c.name = m.name + "_" + tur
                nt, ln = nodes(c)
                cikis = [n for n in nt if n.type == 'OUTPUT_MATERIAL'][0]
                kaynak, aval = alfa_kaynagi(c)
                em = nt.new('ShaderNodeEmission'); em.inputs['Strength'].default_value = 1.0
                if tur == "normal":
                    g = nt.new('ShaderNodeNewGeometry')
                    vt = nt.new('ShaderNodeVectorTransform'); vt.vector_type = 'NORMAL'; vt.convert_from = 'WORLD'; vt.convert_to = 'CAMERA'
                    ln.new(g.outputs['Normal'], vt.inputs['Vector'])
                    # Blender kamera uzayı: x sağ, y yukarı, z kameradan ileri (−). Kameraya bakan yüz z = +: n.z'yi çevir
                    sp = nt.new('ShaderNodeSeparateXYZ'); ln.new(vt.outputs['Vector'], sp.inputs['Vector'])
                    ng = nt.new('ShaderNodeMath'); ng.operation = 'MULTIPLY'; ng.inputs[1].default_value = -1.0
                    ln.new(sp.outputs['Z'], ng.inputs[0])
                    cb = nt.new('ShaderNodeCombineXYZ')
                    ln.new(sp.outputs['X'], cb.inputs['X']); ln.new(sp.outputs['Y'], cb.inputs['Y']); ln.new(ng.outputs['Value'], cb.inputs['Z'])
                    vm = nt.new('ShaderNodeVectorMath'); vm.operation = 'MULTIPLY_ADD'
                    ln.new(cb.outputs['Vector'], vm.inputs[0]); vm.inputs[1].default_value = (0.5, 0.5, 0.5); vm.inputs[2].default_value = (0.5, 0.5, 0.5)
                    ln.new(vm.outputs['Vector'], em.inputs['Color'])
                else:
                    if kat == "giysi" and "yaka_maske" in m:
                        mk = nt.get(m["yaka_maske"])
                        mx = nt.new('ShaderNodeMix'); mx.data_type = 'RGBA'
                        mx.inputs['A'].default_value = (*KIMLIK_RENK["giysi"], 1); mx.inputs['B'].default_value = (*KIMLIK_RENK["yaka"], 1)
                        ln.new(mk.outputs[0], mx.inputs['Factor'])
                        # ikili: yaka maskesi 0,5'te eşiklenir (düz renk)
                        st = nt.new('ShaderNodeMath'); st.operation = 'GREATER_THAN'; st.inputs[1].default_value = 0.5
                        ln.new(mk.outputs[0], st.inputs[0]); ln.new(st.outputs['Value'], mx.inputs['Factor'])
                        ln.new(mx.outputs['Result'], em.inputs['Color'])
                    else:
                        em.inputs['Color'].default_value = (*KIMLIK_RENK.get(kat, (1, 0, 0)), 1)
                tr = nt.new('ShaderNodeBsdfTransparent'); ms = nt.new('ShaderNodeMixShader')
                if kaynak is not None:
                    if tur == "kimlik":
                        st2 = nt.new('ShaderNodeMath'); st2.operation = 'GREATER_THAN'; st2.inputs[1].default_value = 0.5
                        ln.new(kaynak, st2.inputs[0]); ln.new(st2.outputs['Value'], ms.inputs['Fac'])
                    else:
                        ln.new(kaynak, ms.inputs['Fac'])
                else:
                    ms.inputs['Fac'].default_value = aval
                ln.new(tr.outputs[0], ms.inputs[1]); ln.new(em.outputs[0], ms.inputs[2])
                for l in list(cikis.inputs['Surface'].links): ln.remove(l)
                ln.new(ms.outputs[0], cikis.inputs['Surface'])
                out.append(c)
            lst.append((m, out[0], out[1]))
        tablo[o] = lst
    return tablo


def gecise_gec(tablo, tur):
    i = {"rgba": 0, "normal": 1, "kimlik": 2}[tur]
    for o, lst in tablo.items():
        for sl, ucl in zip(o.material_slots, lst):
            if ucl[0] is not None:
                sl.link = 'OBJECT' if False else sl.link
                sl.material = ucl[i]
    sc = bpy.context.scene
    if tur == "rgba":
        sc.view_settings.view_transform = 'Standard'; sc.cycles.samples = ORNEK; sc.cycles.use_denoising = True
        sc.cycles.filter_width = 1.5
    else:
        sc.view_settings.view_transform = 'Raw' if 'Raw' in [e.identifier for e in sc.view_settings.bl_rna.properties['view_transform'].enum_items] else 'Standard'
        sc.view_settings.look = 'None' if hasattr(sc.view_settings, 'look') else None
        sc.cycles.use_denoising = False
        sc.cycles.samples = 16 if tur == "normal" else 1
        sc.cycles.filter_width = 1.5 if tur == "normal" else 0.01
    for L in bpy.data.lights:
        pass


# ================================================================ ana
def main():
    t0 = time.time()
    bpy.ops.wm.read_factory_settings(use_empty=True)
    isk, gov, par = kisi_kur(KL["kisi"])
    cam = sahne()
    ot = Oturt(isk, D[0])
    f = ot.f
    # elde zarf (theo_oda: sağ el) ve şapka (Vincent)
    ek = []
    sapka = hasir_sapka() if KL["kisi"] == "vincent" else None
    zf = zarf() if KL.get("zarf") else None
    for o in par:
        if o.name.lower().split(".")[-1].startswith("short") and sapka is not None:
            d = o.modifiers.new("sapka_alti", 'DISPLACE'); d.strength = -0.007; d.mid_level = 0.0
    a, b_ = [int(x) for x in arg("kareler", "0:%d" % len(D)).split(":")]
    sc = bpy.context.scene
    sc.frame_start, sc.frame_end = 1, len(D)
    # 1) pozları anahtarla
    for i, k in enumerate(D):
        ot.kare(k)
        t = k['t']
        eller(f, "Left", "dinlen")
        if KL.get("goster"):
            g0, g1 = KL["goster"]
            if t >= g0 - 0.3:
                eller(f, "Left", "isaret")   # Vincent sol eliyle aşağıyı gösterir (parmaklar doğal)
        eller(f, "Right", "tut" if zf else "dinlen")
        isk.keyframe_insert("location", frame=i + 1); isk.keyframe_insert("rotation_quaternion" if isk.rotation_mode == 'QUATERNION' else "rotation_euler", frame=i + 1)
        isk.keyframe_insert("scale", frame=i + 1)
        f.anahtarla(i + 1)
        for yan in ("Left", "Right"):
            for c_ in ot.esnek:
                isk.pose.bones[P + yan + c_].keyframe_insert("scale", frame=i + 1)
        if i == 0:
            if sapka is not None:
                bas = f.bas(P + "Head"); on = f.on
                tepe = bas + UP * 0.115 * ot.s + on * 0.02
                Mh = Matrix.Translation(tepe) @ Quaternion(UP, math.atan2(on.y, on.x) - math.pi / 2).to_matrix().to_4x4() @ Matrix.Scale(ot.s, 4)
                f.bagla(sapka, P + "Head", Mh)
            if zf is not None:
                n, dd = f.avuc("Right")
                el = (f.bas(P + "RightHandIndex1") + f.bas(P + "RightHandPinky1")) / 2
                yx = dd.cross(n).normalized()
                R = Matrix((yx, dd, n)).transposed().to_4x4()
                f.bagla(zf, P + "RightHand", Matrix.Translation(el + dd * 0.05 + n * 0.012) @ R)
    print("POZ %s: %d kare, %.1f sn; en büyük eklem sapması %.3f m; kalça %.3f, omuz %.3f" % (AD, len(D), time.time() - t0, ot.sapma, ot.kalca_sapma, ot.omuz_sapma))
    nesneler = [o for o in bpy.data.objects if o.type == 'MESH' and o.name != "yer_sekme"]
    tablo = gecis_malzemeleri(nesneler)
    sureler = {}
    for tur, kl, on_ek in (("rgba", "kare", "k"), ("normal", "normal", "n"), ("kimlik", "kimlik", "i")):
        os.makedirs(os.path.join(CIKTI, kl), exist_ok=True)
        gecise_gec(tablo, tur)
        bpy.data.objects["yer_sekme"].hide_render = (tur != "rgba")
        for L in [o for o in bpy.data.objects if o.type == 'LIGHT']:
            L.hide_render = (tur != "rgba")
        s0 = time.time()
        for i in range(a, b_):
            k = D[i]
            sc.frame_set(i + 1)
            sc.render.filepath = os.path.join(CIKTI, kl, "%s_%04d.png" % (on_ek, round(k['t'] * FPS)))
            bpy.ops.render.render(write_still=True)
        sureler[tur] = round((time.time() - s0) / max(1, b_ - a), 2)
        print("GECIS %s %s: %.2f sn/kare" % (AD, tur, sureler[tur]), flush=True)
    bilgi = {
        "klip": AD, "kisi": KL["kisi"], "fps": FPS, "kare_sayisi": len(D), "t_son": D[-1]['t'],
        "eklem": os.path.relpath(KL["eklem"], DEPO).replace("\\", "/"), "kamera": KAM,
        "kamera_dosyasi": os.path.relpath(KL["kamera"], DEPO).replace("\\", "/"),
        "cozunurluk": [960, 540], "eksen": "bizim (x sağ, y yukarı, z kameraya) → Blender (x, −z, y)",
        "ornek": ORNEK, "gurultu_giderme": "OptiX (yalnız RGBA)", "renk_donusumu": "Standard (RGBA), Raw (normal, kimlik)",
        "normal": "kamera uzayı: x sağ, y yukarı, z kameraya doğru; RGB = n·0.5+0.5",
        "kimlik": {k_: [round(c * 255) for c in v] for k_, v in KIMLIK_RENK.items()},
        "eklem_sapmasi_en_buyuk_m": round(ot.sapma, 4),
        "eklem_sapmasi_not": "diz, dirsek, el bileği, ayak bileği hedefte (uzuvlar eklem boyuna esnetildi); kalça ve omuz kökü MPFB'nin kendi noktası",
        "kok_sapmasi_en_buyuk_m": round(ot.kok_sapma, 4), "kalca_sapmasi_m": round(ot.kalca_sapma, 4), "omuz_sapmasi_m": round(ot.omuz_sapma, 4), "omuz_orani": OMUZ_ORAN, "ayak_bilegi_yukseltme_m": round(ot.bilek_yukselt, 4), "kare_suresi_sn": sureler, "olcek": round(ot.s, 4),
        "kirpma": None,
        "varliklar": "MPFB2 (MakeHuman) gövde ve CC0 giysiler; ayrıntı RAPOR_3.md ve araclar/ASSETS.md",
    }
    json.dump(bilgi, open(os.path.join(CIKTI, "bilgi.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("BİTTİ", AD)


main()
