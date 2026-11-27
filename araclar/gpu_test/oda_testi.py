# -*- coding: utf-8 -*-
"""GPU üslup testi: Theo van Gogh'un Paris odası, gece, 1888 (Blender/Cycles).

Kullanım (depo kökünden):
  blender -b -P araclar/gpu_test/oda_testi.py -- --cikti van-gogh/gpu_test
Seçenekler:
  --mod hepsi|tek|hareket|kodla|onizleme   (varsayılan: hepsi; kodla: kareler hazırsa yalnız MP4)
  --ornek 256                         Cycles örnek sayısı (tek kare)
  --ornek_hareket 256                 hareketli kare örnek sayısı
  --kareler 1-180                     yalnız bu kareler (hareket)
  --kare 1                            tek karenin zamanı (onizleme/tek)

Önce varlıklar: python araclar/gpu_test/varlik_indir.py
Çıktılar: oda_renkli.png, oda_karma.png, oda_hareket.mp4 (+ oda_hareket_renkli.mp4), olcum.json
"""
import bpy
import bmesh
import json
import math
import os
import random
import shutil
import subprocess
import sys
import time
from mathutils import Vector, Quaternion, Matrix, Euler

# ---------------------------------------------------------------- argümanlar
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []


def arg(ad, vars_):
    if "--" + ad in argv:
        return argv[argv.index("--" + ad) + 1]
    return vars_


DEPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
CIKTI = os.path.abspath(os.path.join(DEPO, arg("cikti", "van-gogh/gpu_test")))
MOD = arg("mod", "hepsi")
ORNEK = int(arg("ornek", "256"))
ORNEK_H = int(arg("ornek_hareket", "256"))
KARELER = arg("kareler", "1-180")
TEK_KARE = int(arg("kare", "1"))
V = os.path.join(DEPO, "araclar", "gpu_test", "varlik")
PH = os.path.join(V, "polyhaven")
RB = os.path.join(V, "rocketbox", "Business_Male_03")
TABLO = os.path.join(DEPO, "van-gogh", "gorsel", "otoportre_hasir_sapka_1887_met436532.jpg")
KARE_DIZ = os.path.join(V, "kareler")
os.makedirs(CIKTI, exist_ok=True)

FPS = 30
SURE = 6.0
N_KARE = int(FPS * SURE)
random.seed(1888)

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.fps = FPS
sc.frame_start, sc.frame_end = 1, N_KARE


# ---------------------------------------------------------------- GPU
def gpu_ac():
    prefs = bpy.context.preferences.addons['cycles'].preferences
    secilen = None
    for tur in ('OPTIX', 'CUDA', 'HIP', 'ONEAPI'):
        try:
            prefs.compute_device_type = tur
            prefs.get_devices()
            if any(d.type == tur for d in prefs.devices):
                secilen = tur
                break
        except Exception:
            pass
    for d in prefs.devices:
        d.use = (d.type != 'CPU')
    sc.render.engine = 'CYCLES'
    sc.cycles.device = 'GPU'
    adlar = [d.name for d in prefs.devices if d.use]
    print("GPU:", secilen, adlar)
    return secilen, adlar


GPU_TUR, GPU_AD = gpu_ac()
sc.cycles.samples = ORNEK
sc.cycles.use_denoising = True
try:
    sc.cycles.denoiser = 'OPTIX' if GPU_TUR == 'OPTIX' else 'OPENIMAGEDENOISE'
except Exception:
    pass
sc.cycles.seed = 1888
sc.cycles.use_animated_seed = False
sc.cycles.max_bounces = 8
sc.cycles.diffuse_bounces = 4
sc.cycles.glossy_bounces = 3
sc.cycles.transparent_max_bounces = 16
sc.cycles.sample_clamp_indirect = 6.0
sc.cycles.blur_glossy = 1.0
sc.render.resolution_x, sc.render.resolution_y = 1920, 1080
sc.render.resolution_percentage = 100
sc.view_settings.view_transform = 'AgX'
try:
    sc.view_settings.look = 'AgX - Base Contrast'
except Exception:
    pass
sc.view_settings.exposure = 0.35
sc.render.image_settings.file_format = 'PNG'
sc.render.image_settings.color_mode = 'RGB'
sc.render.image_settings.color_depth = '8'


# ---------------------------------------------------------------- yardımcılar
def nodes_of(mat):
    if hasattr(mat, "use_nodes"):
        try:
            mat.use_nodes = True
        except Exception:
            pass
    return mat.node_tree.nodes, mat.node_tree.links


def bsdf_of(mat):
    nt, _ = nodes_of(mat)
    for n in nt:
        if n.type == 'BSDF_PRINCIPLED':
            return n
    return None


def img(path, renk=True):
    im = bpy.data.images.load(path, check_existing=True)
    if not renk:
        im.colorspace_settings.name = 'Non-Color'
    return im


def yeni_mat(ad):
    m = bpy.data.materials.new(ad)
    nodes_of(m)
    return m


def pbr_doku(ad, klasor, olcek=0.5, renk_carp=None, lekeli=False, puruz_ek=0.0):
    """Poly Haven dokusu, dünya (Object) koordinatına kutu izdüşümüyle."""
    m = yeni_mat(ad)
    nt, ln = nodes_of(m)
    b = bsdf_of(m)
    tc = nt.new('ShaderNodeTexCoord')
    mp = nt.new('ShaderNodeMapping')
    mp.inputs['Scale'].default_value = (olcek, olcek, olcek)
    ln.new(tc.outputs['Object'], mp.inputs['Vector'])
    d = os.path.join(PH, klasor)

    def tex(ek, renk):
        f = [x for x in os.listdir(d) if ek in x][0]
        t = nt.new('ShaderNodeTexImage')
        t.image = img(os.path.join(d, f), renk)
        t.projection = 'BOX'
        t.projection_blend = 0.25
        ln.new(mp.outputs['Vector'], t.inputs['Vector'])
        return t
    dif = tex('_diff_', True)
    rgh = tex('_rough_', False)
    nor = tex('_nor_gl_', False)
    son = dif.outputs['Color']
    if renk_carp is not None:
        mx = nt.new('ShaderNodeMix')
        mx.data_type = 'RGBA'
        mx.blend_type = 'MULTIPLY'
        mx.inputs['Factor'].default_value = 1.0
        ln.new(son, mx.inputs['A'])
        mx.inputs['B'].default_value = renk_carp
        son = mx.outputs['Result']
    if lekeli:
        # sıvada büyük ölçekli lekeler ve tabana doğru kirlenme
        nz = nt.new('ShaderNodeTexNoise')
        nz.inputs['Scale'].default_value = 1.6
        nz.inputs['Detail'].default_value = 6
        nz.inputs['Roughness'].default_value = 0.62
        ln.new(tc.outputs['Object'], nz.inputs['Vector'])
        cr = nt.new('ShaderNodeValToRGB')
        cr.color_ramp.elements[0].position = 0.45
        cr.color_ramp.elements[0].color = (1, 1, 1, 1)
        cr.color_ramp.elements[1].position = 0.75
        cr.color_ramp.elements[1].color = (0.58, 0.52, 0.44, 1)
        ln.new(nz.outputs['Fac'], cr.inputs['Fac'])
        mx2 = nt.new('ShaderNodeMix')
        mx2.data_type = 'RGBA'
        mx2.blend_type = 'MULTIPLY'
        mx2.inputs['Factor'].default_value = 1.0
        ln.new(son, mx2.inputs['A'])
        ln.new(cr.outputs['Color'], mx2.inputs['B'])
        son = mx2.outputs['Result']
        # taban kiri: z küçükken koyulaş
        sep = nt.new('ShaderNodeSeparateXYZ')
        ln.new(tc.outputs['Object'], sep.inputs['Vector'])
        mr = nt.new('ShaderNodeMapRange')
        mr.inputs['From Min'].default_value = 0.0
        mr.inputs['From Max'].default_value = 0.9
        mr.inputs['To Min'].default_value = 0.72
        mr.inputs['To Max'].default_value = 1.0
        ln.new(sep.outputs['Z'], mr.inputs['Value'])
        mx3 = nt.new('ShaderNodeMix')
        mx3.data_type = 'RGBA'
        mx3.blend_type = 'MULTIPLY'
        mx3.inputs['Factor'].default_value = 1.0
        ln.new(son, mx3.inputs['A'])
        ln.new(mr.outputs['Result'], mx3.inputs['B'])
        son = mx3.outputs['Result']
    ln.new(son, b.inputs['Base Color'])
    if puruz_ek:
        ad_ = nt.new('ShaderNodeMath')
        ad_.operation = 'ADD'
        ad_.use_clamp = True
        ln.new(rgh.outputs['Color'], ad_.inputs[0])
        ad_.inputs[1].default_value = puruz_ek
        ln.new(ad_.outputs['Value'], b.inputs['Roughness'])
    else:
        ln.new(rgh.outputs['Color'], b.inputs['Roughness'])
    nm = nt.new('ShaderNodeNormalMap')
    nm.inputs['Strength'].default_value = 2.2 if lekeli else 1.0
    ln.new(nor.outputs['Color'], nm.inputs['Color'])
    ln.new(nm.outputs['Normal'], b.inputs['Normal'])
    return m


def kutu(ad, x0, x1, y0, y1, z0, z1, mat, koleksiyon=None):
    me = bpy.data.meshes.new(ad)
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts:
        v.co.x = x0 + (v.co.x + 0.5) * (x1 - x0)
        v.co.y = y0 + (v.co.y + 0.5) * (y1 - y0)
        v.co.z = z0 + (v.co.z + 0.5) * (z1 - z0)
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(ad, me)
    (koleksiyon or sc.collection).objects.link(ob)
    if mat:
        ob.data.materials.append(mat)
    return ob


def kutu_lokal(ad, merkez, boyut, mat, parent=None, rot=None):
    """Yerel merkezli kutu (bevelli), isteğe bağlı ebeveyn."""
    sx, sy, sz = boyut
    ob = kutu(ad, -sx / 2, sx / 2, -sy / 2, sy / 2, -sz / 2, sz / 2, mat)
    ob.location = merkez
    if rot:
        ob.rotation_euler = rot
    if parent:
        ob.parent = parent
    bv = ob.modifiers.new("bevel", 'BEVEL')
    bv.width = min(0.004, min(boyut) * 0.25)
    bv.segments = 2
    return ob


def gltf_al(ad, konum=(0, 0, 0), rot_z=0.0, olcek=(1, 1, 1), sakla=None):
    """Poly Haven glTF'ini içe al; hepsini tek boş nesneye bağla."""
    yol = [os.path.join(PH, ad, f) for f in os.listdir(os.path.join(PH, ad)) if f.endswith('.gltf')][0]
    once = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=yol)
    yeni = [o for o in bpy.data.objects if o not in once]
    kok = bpy.data.objects.new(ad + "_kok", None)
    sc.collection.objects.link(kok)
    for o in yeni:
        if o.parent is None:
            o.parent = kok
    if sakla:
        sil = [o for o in yeni if not sakla(o)]
        for o in sil:
            bpy.data.objects.remove(o, do_unlink=True)
    kok.location = konum
    kok.rotation_euler = (0, 0, rot_z)
    kok.scale = olcek
    bpy.context.view_layer.update()
    return kok, [o for o in kok.children_recursive]


def dunya_bbox(objs):
    mn = Vector((1e9, 1e9, 1e9))
    mx = Vector((-1e9, -1e9, -1e9))
    for o in objs:
        if o.type != 'MESH':
            continue
        for c in o.bound_box:
            w = o.matrix_world @ Vector(c)
            mn = Vector((min(mn.x, w.x), min(mn.y, w.y), min(mn.z, w.z)))
            mx = Vector((max(mx.x, w.x), max(mx.y, w.y), max(mx.z, w.z)))
    return mn, mx


# ---------------------------------------------------------------- malzemeler
M_SIVA = pbr_doku("siva", "plastered_wall_04", olcek=0.55, renk_carp=(0.93, 0.88, 0.80, 1), lekeli=True)
M_TAVAN = pbr_doku("tavan", "plastered_wall_04", olcek=0.5, renk_carp=(0.8, 0.77, 0.72, 1))
M_DOSEME = pbr_doku("doseme", "old_wooden_floor_01", olcek=0.45, renk_carp=(0.85, 0.78, 0.70, 1), puruz_ek=0.05)
M_AHSAP = pbr_doku("ahsap", "dark_wooden_planks", olcek=1.6, renk_carp=(0.75, 0.62, 0.50, 1))
M_PERVAZ = pbr_doku("pervaz", "dark_wooden_planks", olcek=1.2, renk_carp=(0.42, 0.36, 0.30, 1))

M_PERDE = yeni_mat("perde")
b = bsdf_of(M_PERDE)
b.inputs['Base Color'].default_value = (0.10, 0.11, 0.085, 1)
b.inputs['Roughness'].default_value = 0.9
try:
    b.inputs['Sheen Weight'].default_value = 0.6
    b.inputs['Sheen Tint'].default_value = (0.5, 0.55, 0.45, 1)
except Exception:
    pass

M_CATI = yeni_mat("cati")
b = bsdf_of(M_CATI)
nt, ln = nodes_of(M_CATI)
_nz = nt.new('ShaderNodeTexNoise'); _nz.inputs['Scale'].default_value = 3.0; _nz.inputs['Detail'].default_value = 8
_cr = nt.new('ShaderNodeValToRGB')
_cr.color_ramp.elements[0].color = (0.025, 0.028, 0.035, 1)
_cr.color_ramp.elements[1].color = (0.075, 0.08, 0.095, 1)
ln.new(_nz.outputs['Fac'], _cr.inputs['Fac']); ln.new(_cr.outputs['Color'], b.inputs['Base Color'])
b.inputs['Roughness'].default_value = 0.6
b.inputs['Metallic'].default_value = 0.4  # çinko kaplama

M_CATI_DUVAR = yeni_mat("cati_duvar")
b = bsdf_of(M_CATI_DUVAR)
b.inputs['Base Color'].default_value = (0.09, 0.085, 0.08, 1)
b.inputs['Roughness'].default_value = 0.9

M_PENCERE_ISIK = yeni_mat("pencere_isik")
nt, ln = nodes_of(M_PENCERE_ISIK)
b = bsdf_of(M_PENCERE_ISIK)
b.inputs['Base Color'].default_value = (0, 0, 0, 1)
b.inputs['Emission Color'].default_value = (1.0, 0.62, 0.28, 1)
b.inputs['Emission Strength'].default_value = 1.2

M_AY = yeni_mat("ay")
b = bsdf_of(M_AY)
b.inputs['Base Color'].default_value = (0, 0, 0, 1)
b.inputs['Emission Color'].default_value = (0.92, 0.94, 1.0, 1)
b.inputs['Emission Strength'].default_value = 2.6

# cam: saydam + çok hafif yansıma (saydam gölge geçirir, ay ışığı odaya girer)
M_CAM = yeni_mat("pencere_cami")
nt, ln = nodes_of(M_CAM)
for n in list(nt):
    nt.remove(n)
o = nt.new('ShaderNodeOutputMaterial')
tr = nt.new('ShaderNodeBsdfTransparent')
gl = nt.new('ShaderNodeBsdfGlossy')
gl.inputs['Roughness'].default_value = 0.03
mx = nt.new('ShaderNodeMixShader')
mx.inputs['Fac'].default_value = 0.07
ln.new(tr.outputs[0], mx.inputs[1])
ln.new(gl.outputs[0], mx.inputs[2])
ln.new(mx.outputs[0], o.inputs['Surface'])

# kâğıt: krem, el yazısı satırları (dalga + gürültü), çok hafif yarı geçirgenlik
def kagit_mat(ad, temel=(0.86, 0.82, 0.72, 1), yazi=True, yazi_renk=(0.25, 0.17, 0.10, 1)):
    m = yeni_mat(ad)
    nt, ln = nodes_of(m)
    b = bsdf_of(m)
    b.inputs['Roughness'].default_value = 0.75
    try:
        b.inputs['Subsurface Weight'].default_value = 0.08
        b.inputs['Subsurface Radius'].default_value = (0.5, 0.45, 0.35)
        b.inputs['Subsurface Scale'].default_value = 0.002
    except Exception:
        pass
    if not yazi:
        b.inputs['Base Color'].default_value = temel
        return m
    tc = nt.new('ShaderNodeTexCoord')
    # satırlar: UV'nin v'si boyunca bantlar
    sep = nt.new('ShaderNodeSeparateXYZ')
    ln.new(tc.outputs['UV'], sep.inputs['Vector'])
    wv = nt.new('ShaderNodeTexWave')
    wv.wave_type = 'BANDS'
    wv.bands_direction = 'Y'
    wv.inputs['Scale'].default_value = 7.0
    wv.inputs['Distortion'].default_value = 1.5
    wv.inputs['Detail'].default_value = 1.0
    ln.new(tc.outputs['UV'], wv.inputs['Vector'])
    nz = nt.new('ShaderNodeTexNoise')
    nz.inputs['Scale'].default_value = 140.0
    nz.inputs['Detail'].default_value = 3.0
    ln.new(tc.outputs['UV'], nz.inputs['Vector'])
    cr1 = nt.new('ShaderNodeValToRGB')  # ince çizgi
    cr1.color_ramp.elements[0].position = 0.0
    cr1.color_ramp.elements[0].color = (0, 0, 0, 1)
    cr1.color_ramp.elements[1].position = 0.12
    cr1.color_ramp.elements[1].color = (1, 1, 1, 1)
    ln.new(wv.outputs['Fac'], cr1.inputs['Fac'])
    cr2 = nt.new('ShaderNodeValToRGB')  # kelime kırıkları
    cr2.color_ramp.elements[0].position = 0.42
    cr2.color_ramp.elements[1].position = 0.55
    ln.new(nz.outputs['Fac'], cr2.inputs['Fac'])
    # kenar boşlukları
    mr = nt.new('ShaderNodeMapRange')
    mr.inputs['From Min'].default_value = 0.08
    mr.inputs['From Max'].default_value = 0.1
    ln.new(sep.outputs['X'], mr.inputs['Value'])
    mr2 = nt.new('ShaderNodeMapRange')
    mr2.inputs['From Min'].default_value = 0.92
    mr2.inputs['From Max'].default_value = 0.9
    ln.new(sep.outputs['X'], mr2.inputs['Value'])
    m1 = nt.new('ShaderNodeMath'); m1.operation = 'MULTIPLY'
    ln.new(mr.outputs['Result'], m1.inputs[0]); ln.new(mr2.outputs['Result'], m1.inputs[1])
    inv = nt.new('ShaderNodeMath'); inv.operation = 'SUBTRACT'; inv.inputs[0].default_value = 1.0
    ln.new(cr1.outputs['Color'], inv.inputs[1])
    m2 = nt.new('ShaderNodeMath'); m2.operation = 'MULTIPLY'
    ln.new(inv.outputs['Value'], m2.inputs[0]); ln.new(cr2.outputs['Color'], m2.inputs[1])
    m3 = nt.new('ShaderNodeMath'); m3.operation = 'MULTIPLY'
    ln.new(m2.outputs['Value'], m3.inputs[0]); ln.new(m1.outputs['Value'], m3.inputs[1])
    m4 = nt.new('ShaderNodeMath'); m4.operation = 'MULTIPLY'; m4.inputs[1].default_value = 0.85
    ln.new(m3.outputs['Value'], m4.inputs[0])
    mx = nt.new('ShaderNodeMix'); mx.data_type = 'RGBA'
    mx.inputs['A'].default_value = temel
    mx.inputs['B'].default_value = yazi_renk
    ln.new(m4.outputs['Value'], mx.inputs['Factor'])
    ln.new(mx.outputs['Result'], b.inputs['Base Color'])
    return m


M_KAGIT = kagit_mat("kagit")
M_KAGIT_BOS = kagit_mat("kagit_bos", yazi=False)

M_ZARF = yeni_mat("zarf_sari")
b = bsdf_of(M_ZARF)
b.inputs['Base Color'].default_value = (0.86, 0.58, 0.05, 1)
b.inputs['Roughness'].default_value = 0.8

M_TUVAL_KENAR = yeni_mat("tuval_kenar")
b = bsdf_of(M_TUVAL_KENAR)
b.inputs['Base Color'].default_value = (0.62, 0.57, 0.48, 1)
b.inputs['Roughness'].default_value = 0.85

M_TABLO = yeni_mat("tablo")
nt, ln = nodes_of(M_TABLO)
b = bsdf_of(M_TABLO)
t = nt.new('ShaderNodeTexImage')
t.image = img(TABLO, True)
t.interpolation = 'Cubic'
ln.new(t.outputs['Color'], b.inputs['Base Color'])
b.inputs['Roughness'].default_value = 0.38
try:
    b.inputs['Coat Weight'].default_value = 0.15
    b.inputs['Coat Roughness'].default_value = 0.25
except Exception:
    pass
bw = nt.new('ShaderNodeRGBToBW')
ln.new(t.outputs['Color'], bw.inputs['Color'])
bp = nt.new('ShaderNodeBump')
bp.inputs['Strength'].default_value = 0.25
bp.inputs['Distance'].default_value = 0.0015
ln.new(bw.outputs['Val'], bp.inputs['Height'])
ln.new(bp.outputs['Normal'], b.inputs['Normal'])

# ---------------------------------------------------------------- oda
X0, X1 = -2.4, 2.4
Y0, Y1 = -3.6, 2.4
H = 3.05
T = 0.15
PX0, PX1, PZ0, PZ1 = -1.95, -0.75, 0.62, 2.70  # pencere açıklığı (arka duvarda)

kutu("doseme", X0 - T, X1 + T, Y0 - T, Y1 + T, -0.1, 0.0, M_DOSEME)
kutu("tavan", X0 - T, X1 + T, Y0 - T, Y1 + T, H, H + 0.1, M_TAVAN)
kutu("duvar_sol", X0 - T, X0, Y0, Y1, 0, H, M_SIVA)
kutu("duvar_sag", X1, X1 + T, Y0, Y1, 0, H, M_SIVA)
kutu("duvar_on", X0, X1, Y0 - T, Y0, 0, H, M_SIVA)
kutu("duvar_arka_sol", X0, PX0, Y1, Y1 + T, 0, H, M_SIVA)
kutu("duvar_arka_sag", PX1, X1, Y1, Y1 + T, 0, H, M_SIVA)
kutu("duvar_arka_alt", PX0, PX1, Y1, Y1 + T, 0, PZ0, M_SIVA)
kutu("duvar_arka_ust", PX0, PX1, Y1, Y1 + T, PZ1, H, M_SIVA)
# süpürgelik
SP = 0.14
kutu("supurgelik_arka1", X0, PX0, Y1 - 0.018, Y1, 0, SP, M_PERVAZ)
kutu("supurgelik_arka2", PX0, PX1, Y1 - 0.018, Y1, 0, SP, M_PERVAZ)
kutu("supurgelik_arka3", PX1, X1, Y1 - 0.018, Y1, 0, SP, M_PERVAZ)
kutu("supurgelik_sol", X0, X0 + 0.018, Y0, Y1, 0, SP, M_PERVAZ)
kutu("supurgelik_sag", X1 - 0.018, X1, Y0, Y1, 0, SP, M_PERVAZ)

# pencere: yalnız dikey kayıtlar (yatay kayıt yok: haç okunmasın)
FY0, FY1 = Y1 + 0.03, Y1 + 0.085
kutu("pencere_sol_kasa", PX0, PX0 + 0.07, FY0, FY1, PZ0, PZ1, M_PERVAZ)
kutu("pencere_sag_kasa", PX1 - 0.07, PX1, FY0, FY1, PZ0, PZ1, M_PERVAZ)
kutu("pencere_ust_kasa", PX0, PX1, FY0, FY1, PZ1 - 0.08, PZ1, M_PERVAZ)
kutu("pencere_alt_kasa", PX0, PX1, FY0, FY1, PZ0, PZ0 + 0.09, M_PERVAZ)
MX = (PX0 + PX1) / 2
kutu("pencere_orta_kayit", MX - 0.045, MX + 0.045, FY0 - 0.01, FY1, PZ0, PZ1, M_PERVAZ)
for i, (a, b_) in enumerate([(PX0 + 0.07, MX - 0.045), (MX + 0.045, PX1 - 0.07)]):
    c = (a + b_) / 2
    kutu("pencere_kanat_ic%d" % i, c - 0.018, c + 0.018, FY0 + 0.01, FY1 - 0.01, PZ0 + 0.09, PZ1 - 0.08, M_PERVAZ)
cam = kutu("pencere_cam", PX0 + 0.05, PX1 - 0.05, Y1 + 0.055, Y1 + 0.058, PZ0 + 0.05, PZ1 - 0.05, M_CAM)
kutu("pencere_esigi", PX0 - 0.08, PX1 + 0.08, Y1 - 0.09, Y1 + 0.04, PZ0 - 0.035, PZ0, M_PERVAZ)
for o_ in [o_ for o_ in sc.objects if o_.name.startswith("pencere_") and o_.name != "pencere_cam"]:
    bv = o_.modifiers.new("bevel", 'BEVEL'); bv.width = 0.006; bv.segments = 2


# perdeler: kıvrımlı yüzey
def perde(ad, x0, x1, z0, z1, y, kivrim=9, genlik=0.045, toplama=1.0):
    me = bpy.data.meshes.new(ad)
    bm = bmesh.new()
    nx, nz = 90, 40
    vs = []
    for j in range(nz + 1):
        z = z0 + (z1 - z0) * j / nz
        row = []
        for i in range(nx + 1):
            u = i / nx
            x = x0 + (x1 - x0) * u
            # aşağıda biraz toplanmış kıvrımlar
            k = genlik * (0.75 + 0.25 * (1 - j / nz) * toplama)
            dalga = (0.6 * math.sin(u * kivrim * 2 * math.pi + 0.7 * math.sin(z * 1.3))
                     + 0.4 * math.sin(u * kivrim * 1.37 * 2 * math.pi + 1.9 + 0.9 * math.sin(z * 0.8 + u * 3)))
            yy = y - k * (0.5 + 0.5 * dalga)
            row.append(bm.verts.new((x, yy, z)))
        vs.append(row)
    for j in range(nz):
        for i in range(nx):
            bm.faces.new((vs[j][i], vs[j][i + 1], vs[j + 1][i + 1], vs[j + 1][i]))
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(ad, me)
    sc.collection.objects.link(ob)
    ob.data.materials.append(M_PERDE)
    for p in ob.data.polygons:
        p.use_smooth = True
    sl = ob.modifiers.new("kalinlik", 'SOLIDIFY'); sl.thickness = 0.006
    return ob


perde("perde_sol", PX0 - 0.42, PX0 + 0.08, 0.02, PZ1 + 0.22, Y1 - 0.08)
perde("perde_sag", PX1 - 0.10, PX1 + 0.40, 0.02, PZ1 + 0.22, Y1 - 0.08)
rod = bpy.data.meshes.new("korniz")
bm = bmesh.new()
bmesh.ops.create_cone(bm, cap_ends=True, segments=16, radius1=0.014, radius2=0.014, depth=1.0)
bm.to_mesh(rod); bm.free()
ro = bpy.data.objects.new("korniz", rod); sc.collection.objects.link(ro)
ro.rotation_euler = (0, math.radians(90), 0)
ro.location = ((PX0 + PX1) / 2, Y1 - 0.07, PZ1 + 0.25)
ro.scale = (1, 1, (PX1 - PX0) + 1.0)
ro.data.materials.append(M_PERVAZ)

# ---------------------------------------------------------------- dışarısı: Paris çatıları
rnd = random.Random(7)


def bina(x, y, w, d, h, cati_h, bacalar=True):
    # gövde
    kutu("bina", x - w / 2, x + w / 2, y - d / 2, y + d / 2, -12, h, M_CATI_DUVAR)
    # mansard çatı (kesik piramit)
    me = bpy.data.meshes.new("cati")
    bm = bmesh.new()
    i = 0.22 * min(w, d)
    alt = [(x - w / 2, y - d / 2), (x + w / 2, y - d / 2), (x + w / 2, y + d / 2), (x - w / 2, y + d / 2)]
    ust = [(x - w / 2 + i, y - d / 2 + i), (x + w / 2 - i, y - d / 2 + i), (x + w / 2 - i, y + d / 2 - i), (x - w / 2 + i, y + d / 2 - i)]
    va = [bm.verts.new((a, b_, h)) for a, b_ in alt]
    vu = [bm.verts.new((a, b_, h + cati_h)) for a, b_ in ust]
    for k in range(4):
        bm.faces.new((va[k], va[(k + 1) % 4], vu[(k + 1) % 4], vu[k]))
    bm.faces.new(vu)
    bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new("cati", me); sc.collection.objects.link(ob)
    ob.data.materials.append(M_CATI)
    if bacalar:
        for _ in range(rnd.randint(1, 3)):
            bx = x + rnd.uniform(-w / 3, w / 3)
            by = y + rnd.uniform(-d / 4, d / 4)
            bh = rnd.uniform(0.8, 1.6)
            bw_ = rnd.uniform(0.5, 1.1)
            kutu("baca", bx - bw_ / 2, bx + bw_ / 2, by - 0.3, by + 0.3, h, h + cati_h + bh, M_CATI_DUVAR)
            for p_ in range(rnd.randint(2, 4)):  # baca çömlekleri
                px = bx - bw_ / 2 + 0.15 + p_ * 0.22
                if px > bx + bw_ / 2 - 0.1:
                    break
                kutu("comlek", px - 0.05, px + 0.05, by - 0.05, by + 0.05, h + cati_h + bh, h + cati_h + bh + 0.35, M_CATI_DUVAR)
    # çatı katı pencereleri (az, sıcak)
    for _ in range(rnd.randint(0, 2)):
        if rnd.random() < 0.55:
            wx = x + rnd.uniform(-w / 3, w / 3)
            kutu("isik", wx - 0.25, wx + 0.25, y - d / 2 - 0.02, y - d / 2 + 0.05, h - 1.6, h - 0.6, M_PENCERE_ISIK)


# kat yüksekliği: oda 4. katta, pencereden bakış aşağıya ve uzağa
for sira, (yy, adet) in enumerate([(9, 4), (16, 6), (26, 8), (40, 9)]):
    x = -16 + rnd.uniform(-2, 2)
    while x < 10:
        w = rnd.uniform(5, 9) * (1 + sira * 0.2)
        h = rnd.uniform(-4.5, -1.5) + sira * 1.4
        bina(x + w / 2, yy + rnd.uniform(-1.5, 1.5), w * 0.96, rnd.uniform(6, 10), h, rnd.uniform(1.5, 2.6))
        x += w

# ay
bpy.ops.mesh.primitive_uv_sphere_add(segments=48, ring_count=24, radius=1.0)
ay = bpy.context.active_object
ay.name = "ay"
ay.data.materials.append(M_AY)
for p in ay.data.polygons:
    p.use_smooth = True
ay_yon = Vector((-0.55, 2.0, 0.34)).normalized()  # odadan aya doğru
pencere_merkez = Vector(((PX0 + PX1) / 2, Y1, 1.62))
ay.location = pencere_merkez + ay_yon * 220
ay.scale = (2.3, 2.3, 2.3)
ay.visible_shadow = False

# ---------------------------------------------------------------- dünya (gece göğü)
# Koyu lacivert gradyan + ayın çevresinde hafif hale + seyrek yıldız; odaya çok az dolgu.
w = bpy.data.worlds.new("gece")
sc.world = w
nt, ln = nodes_of(w)
for n in list(nt):
    nt.remove(n)
wo = nt.new('ShaderNodeOutputWorld')
bgn = nt.new('ShaderNodeBackground')
tcw = nt.new('ShaderNodeTexCoord')
sep = nt.new('ShaderNodeSeparateXYZ')
ln.new(tcw.outputs['Generated'], sep.inputs['Vector'])
grad = nt.new('ShaderNodeValToRGB')
grad.color_ramp.elements[0].position = 0.0
grad.color_ramp.elements[0].color = (0.010, 0.013, 0.024, 1)   # ufuk
grad.color_ramp.elements[1].position = 0.35
grad.color_ramp.elements[1].color = (0.0025, 0.0035, 0.008, 1)  # tepe
ln.new(sep.outputs['Z'], grad.inputs['Fac'])
# ay halesi
dot = nt.new('ShaderNodeVectorMath'); dot.operation = 'DOT_PRODUCT'
ln.new(tcw.outputs['Generated'], dot.inputs[0])
dot.inputs[1].default_value = tuple(ay_yon)
pw = nt.new('ShaderNodeMath'); pw.operation = 'POWER'; pw.use_clamp = True
ln.new(dot.outputs['Value'], pw.inputs[0]); pw.inputs[1].default_value = 400.0
hale = nt.new('ShaderNodeMix'); hale.data_type = 'RGBA'; hale.blend_type = 'ADD'
ln.new(pw.outputs['Value'], hale.inputs['Factor'])
ln.new(grad.outputs['Color'], hale.inputs['A'])
hale.inputs['B'].default_value = (0.05, 0.06, 0.09, 1)
# yıldızlar
vor = nt.new('ShaderNodeTexVoronoi'); vor.inputs['Scale'].default_value = 300.0
ln.new(tcw.outputs['Generated'], vor.inputs['Vector'])
yr = nt.new('ShaderNodeValToRGB')
yr.color_ramp.elements[0].position = 0.0; yr.color_ramp.elements[0].color = (0.25, 0.25, 0.3, 1)
yr.color_ramp.elements[1].position = 0.035; yr.color_ramp.elements[1].color = (0, 0, 0, 1)
ln.new(vor.outputs['Distance'], yr.inputs['Fac'])
yildiz = nt.new('ShaderNodeMix'); yildiz.data_type = 'RGBA'; yildiz.blend_type = 'ADD'
yildiz.inputs['Factor'].default_value = 1.0
ln.new(hale.outputs['Result'], yildiz.inputs['A']); ln.new(yr.outputs['Color'], yildiz.inputs['B'])
ln.new(yildiz.outputs['Result'], bgn.inputs['Color'])
bgn.inputs['Strength'].default_value = 1.0
ln.new(bgn.outputs['Background'], wo.inputs['Surface'])

# ---------------------------------------------------------------- mobilya
# yazı masası (alçak masa boya ölçeklendi: 0.74 m)
masa, masa_obj = gltf_al("WoodenTable_01", konum=(X1 - 0.30, 1.25, 0), rot_z=math.radians(90), olcek=(0.78, 0.85, 1.35))
mn, mx_ = dunya_bbox(masa_obj)
MASA_Z = mx_.z
print("masa", tuple(mn), tuple(mx_))

# sandalye: masaya dönük, biraz geri çekilmiş
sand, sand_obj = gltf_al("gallinera_chair", konum=(1.42, 1.58, 0), rot_z=math.radians(-72), olcek=(0.92, 0.92, 0.92))

# lamba (masanın sol ucunda)
lamba, lamba_obj = gltf_al("vintage_oil_lamp", konum=(1.99, 1.02, MASA_Z), olcek=(0.62, 0.62, 0.62))
alev = [o for o in lamba_obj if 'flame' in o.name][0]
lamba_cam = [o for o in lamba_obj if 'glass' in o.name][0]
amn, amx = dunya_bbox([alev])
ALEV = (amn + amx) / 2
print("alev", tuple(ALEV), "boy", tuple(amx - amn))
# alev: özgün kart brülörün içinde kalıyor; yerine damla biçimli küçük bir alev gövdesi
# (dış: turuncu, iç: sarı-beyaz çekirdek), fitilin hemen üstünde.
alev.hide_render = True
lmn, lmx = dunya_bbox([o for o in lamba_obj if o.name.startswith("vintage_oil_lamp") and 'flame' not in o.name and 'glass' not in o.name])
ALEV = Vector((ALEV.x, ALEV.y, lmx.z + 0.018))


def alev_govde(ad, r, boy, renk, guc):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=16, radius=r)
    o = bpy.context.active_object
    o.name = ad
    for v in o.data.vertices:  # damla: üstü sivri
        t = min(1.0, max(0.0, (v.co.z / r + 1) / 2))
        k = 1.0 - 0.75 * t ** 1.6
        v.co.x *= k
        v.co.y *= k
        v.co.z *= boy
    for p in o.data.polygons:
        p.use_smooth = True
    m = yeni_mat(ad)
    bb = bsdf_of(m)
    bb.inputs['Base Color'].default_value = (0, 0, 0, 1)
    bb.inputs['Emission Color'].default_value = renk
    bb.inputs['Emission Strength'].default_value = guc
    o.data.materials.append(m)
    o.location = ALEV
    o.visible_shadow = False
    return o


alev_dis = alev_govde("alev_dis", 0.0065, 2.6, (1.0, 0.45, 0.10, 1), 35.0)
alev_ic = alev_govde("alev_ic", 0.0038, 2.2, (1.0, 0.85, 0.55, 1), 80.0)
alev_ic.location.z -= 0.003
print("alev konumu", tuple(ALEV))
alev.visible_shadow = False
lamba_cam.visible_shadow = False
# lamba camı: alevin ışığını tutan hafif buzlu cam
for m_ in lamba_cam.data.materials:
    bb = bsdf_of(m_)
    if bb:
        bb.inputs['Roughness'].default_value = 0.12
        bb.inputs['Emission Color'].default_value = (1.0, 0.62, 0.30, 1)
        bb.inputs['Emission Strength'].default_value = 0.06

# kitaplar (masanın sağ ucunda, duvara yaslı)
kit, kit_obj = gltf_al("book_encyclopedia_set_01", konum=(2.27, 1.66, MASA_Z), rot_z=math.radians(90), olcek=(0.95, 0.95, 0.95),
                       sakla=lambda o: o.type != 'MESH' or any(o.name.endswith("book%02d" % k) for k in range(1, 8)))
# gözlük
goz, _ = gltf_al("round_spectacles", konum=(1.98, 1.30, MASA_Z + 0.002), rot_z=math.radians(-20), olcek=(1, 1, 1))
goz.rotation_euler = (math.radians(90), 0, math.radians(70))  # katlı yatırılmış
bpy.context.view_layer.update()
gmn, gmx = dunya_bbox(goz.children_recursive)
goz.location.z += MASA_Z + 0.001 - gmn.z

# kâğıtlar ve sarı zarflar (zarflar maskede renkli kalır)
MASKE_INDEKS = 1   # tablo
ZARF_INDEKS = 2    # sarı zarflar


def yaprak(ad, merkez, boyut, rz, mat, kalin=0.0008, egim=0.0, indeks=0):
    me = bpy.data.meshes.new(ad)
    bm = bmesh.new()
    sx, sy = boyut
    nx, ny = 12, 12
    uvl = bm.loops.layers.uv.new()
    vs = []
    for j in range(ny + 1):
        row = []
        for i in range(nx + 1):
            u, v = i / nx, j / ny
            x = (u - 0.5) * sx
            y = (v - 0.5) * sy
            z = egim * (u - 0.5) ** 2 + 0.0015 * math.sin(v * 3.1)
            row.append(bm.verts.new((x, y, z)))
        vs.append(row)
    for j in range(ny):
        for i in range(nx):
            f = bm.faces.new((vs[j][i], vs[j][i + 1], vs[j + 1][i + 1], vs[j + 1][i]))
            for lp, (ii, jj) in zip(f.loops, [(i, j), (i + 1, j), (i + 1, j + 1), (i, j + 1)]):
                lp[uvl].uv = (ii / nx, jj / ny)
    bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new(ad, me); sc.collection.objects.link(ob)
    ob.data.materials.append(mat)
    ob.location = merkez
    ob.rotation_euler = (0, 0, rz)
    sl = ob.modifiers.new("kalinlik", 'SOLIDIFY'); sl.thickness = kalin; sl.offset = 1.0
    for p in ob.data.polygons:
        p.use_smooth = True
    ob.pass_index = indeks
    return ob


z = MASA_Z + 0.0005
yaprak("kagit1", (2.06, 1.42, z), (0.21, 0.27), math.radians(98), M_KAGIT, egim=0.01)
yaprak("kagit2", (2.13, 1.18, z + 0.001), (0.21, 0.27), math.radians(76), M_KAGIT, egim=0.012)
yaprak("kagit3", (2.20, 1.36, z + 0.002), (0.21, 0.27), math.radians(87), M_KAGIT_BOS)
for k, (x, y, r) in enumerate([(2.02, 0.74, 102), (2.04, 0.72, 84), (2.00, 0.75, 115), (1.97, 1.58, 60)]):
    yaprak("zarf%d" % k, (x, y, z + 0.003 + k * 0.0025), (0.16, 0.105), math.radians(r), M_ZARF, kalin=0.0015, indeks=ZARF_INDEKS)

# ---------------------------------------------------------------- şövale ve tuval
SOV_KONUM = Vector((0.30, 1.80, 0))
SOV_ROT = math.radians(14)
sov = bpy.data.objects.new("sovale", None)
sc.collection.objects.link(sov)
sov.location = SOV_KONUM
sov.rotation_euler = (0, 0, SOV_ROT)


def cubuk(ad, a, b_, kal, mat, parent):
    """a'dan b'ye kare kesitli çubuk (yerel koordinat)."""
    a, b_ = Vector(a), Vector(b_)
    d = b_ - a
    ob = kutu_lokal(ad, (a + b_) / 2, (kal, kal, d.length), mat, parent=parent)
    ob.rotation_mode = 'QUATERNION'
    ob.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(d.normalized())
    return ob


TUV_W, TUV_H = 0.50, 0.50 * 1600 / 1286
RAF_Z = 1.00
# iki ön bacak tepede birleşir (A biçimi), arka bacak dayanak
cubuk("sov_bacak_sol", (-0.33, -0.02, 0), (-0.035, 0.03, 1.86), 0.032, M_AHSAP, sov)
cubuk("sov_bacak_sag", (0.33, -0.02, 0), (0.035, 0.03, 1.86), 0.032, M_AHSAP, sov)
cubuk("sov_bacak_arka", (0.0, 0.46, 0), (0.0, 0.06, 1.78), 0.03, M_AHSAP, sov)
# tuval rafı: yalnız iki bacak arasında, tuvalin hemen altında (tuval kenarı rafa oturur)
lx = 0.33 - (0.33 - 0.035) * RAF_Z / 1.86
kutu_lokal("sov_raf", (0, -0.045, RAF_Z), (2 * lx + 0.06, 0.07, 0.025), M_AHSAP, parent=sov)
kutu_lokal("sov_raf_dudak", (0, -0.078, RAF_Z + 0.018), (2 * lx + 0.06, 0.008, 0.03), M_AHSAP, parent=sov)
# tuval (tablo yüzü + şasi)
TUV_Z = RAF_Z + 0.0125 + TUV_H / 2
TUV_Y = -0.03
tuv_govde = kutu_lokal("tuval_sasi", (0, TUV_Y + 0.012, TUV_Z), (TUV_W, 0.022, TUV_H), M_TUVAL_KENAR, parent=sov)
me = bpy.data.meshes.new("tablo")
bm = bmesh.new()
uvl = bm.loops.layers.uv.new()
vv = [bm.verts.new((-TUV_W / 2 + 0.001, 0, -TUV_H / 2 + 0.001)), bm.verts.new((TUV_W / 2 - 0.001, 0, -TUV_H / 2 + 0.001)),
      bm.verts.new((TUV_W / 2 - 0.001, 0, TUV_H / 2 - 0.001)), bm.verts.new((-TUV_W / 2 + 0.001, 0, TUV_H / 2 - 0.001))]
f = bm.faces.new(vv)
for lp, uv in zip(f.loops, [(0, 0), (1, 0), (1, 1), (0, 1)]):
    lp[uvl].uv = uv
bm.normal_update()
bm.to_mesh(me); bm.free()
tablo = bpy.data.objects.new("tablo", me)
sc.collection.objects.link(tablo)
tablo.data.materials.append(M_TABLO)
tablo.parent = sov
tablo.location = (0, TUV_Y + 0.0005, TUV_Z)
tablo.pass_index = MASKE_INDEKS
# normalin kameraya (−y) bakması için yüz sırası kontrol
bpy.context.view_layer.update()
nrm = (tablo.matrix_world.to_3x3() @ tablo.data.polygons[0].normal)
if nrm.y > 0:
    tablo.data.flip_normals() if hasattr(tablo.data, "flip_normals") else None
    for p in tablo.data.polygons:
        p.flip()
print("tablo normal", tuple(tablo.matrix_world.to_3x3() @ tablo.data.polygons[0].normal))

# ---------------------------------------------------------------- Theo (Rocketbox Business_Male_03, MIT)
once = set(bpy.data.objects)
bpy.ops.import_scene.fbx(filepath=os.path.join(RB, "Export", "Business_Male_03.fbx"), automatic_bone_orientation=False)
yeni = [o for o in bpy.data.objects if o not in once]
arm = [o for o in yeni if o.type == 'ARMATURE'][0]
govde = [o for o in yeni if o.type == 'MESH'][0]
for o in yeni:
    if o.type == 'EMPTY':
        bpy.data.objects.remove(o, do_unlink=True)
# FBX ile gelen tek karelik animasyon nesne dönüşünü ve pozu ezmesin
for o in (arm, govde):
    o.animation_data_clear()


def rb_tex(ad):
    return os.path.join(RB, "Textures", ad)


# kravatı 1880'ler boyunbağına çevir: dokuda turkuaz pikseller koyu griye
def doku_1880():
    im = bpy.data.images.load(rb_tex("m020_body_color.tga"))
    import numpy as np
    W_, H_ = im.size
    px = np.empty(W_ * H_ * 4, dtype=np.float32)
    im.pixels.foreach_get(px)
    px = px.reshape(H_, W_, 4)
    r, g, b_ = px[..., 0], px[..., 1], px[..., 2]
    # yalnız alt orta bölgede (kravat adası) turkuaz/yeşil
    yy = np.arange(H_)[:, None] / H_          # piksel dizisi alttan yukarı
    xx = np.arange(W_)[None, :] / W_
    bolge = (yy < 0.16) & (xx > 0.33) & (xx < 0.62)
    tur = bolge & ((g - r) > 0.04)
    l = (0.3 * r + 0.59 * g + 0.11 * b_)
    koyu = 0.07 + 0.25 * l
    for k in range(3):
        px[..., k] = np.where(tur, koyu * (1.0, 0.97, 0.95)[k], px[..., k])
    yeni_im = bpy.data.images.new("m020_body_1880", W_, H_, alpha=True)
    yeni_im.pixels.foreach_set(px.ravel())
    yeni_im.pack()
    print("kravat pikseli:", int(tur.sum()))
    return yeni_im


def rb_mat(mat, renk_im, normal, specular, deri=False, opak=False):
    nt, ln = nodes_of(mat)
    for n in list(nt):
        nt.remove(n)
    out = nt.new('ShaderNodeOutputMaterial')
    b = nt.new('ShaderNodeBsdfPrincipled')
    ln.new(b.outputs[0], out.inputs['Surface'])
    tc = nt.new('ShaderNodeTexImage'); tc.image = renk_im
    ln.new(tc.outputs['Color'], b.inputs['Base Color'])
    if opak:
        ln.new(tc.outputs['Alpha'], b.inputs['Alpha'])
        b.inputs['Roughness'].default_value = 0.6
        return
    tn = nt.new('ShaderNodeTexImage'); tn.image = img(normal, False)
    nm = nt.new('ShaderNodeNormalMap')
    ln.new(tn.outputs['Color'], nm.inputs['Color'])
    ln.new(nm.outputs['Normal'], b.inputs['Normal'])
    ts = nt.new('ShaderNodeTexImage'); ts.image = img(specular, False)
    bw = nt.new('ShaderNodeRGBToBW')
    ln.new(ts.outputs['Color'], bw.inputs['Color'])
    mr = nt.new('ShaderNodeMapRange')
    mr.inputs['To Min'].default_value = 0.82 if not deri else 0.62
    mr.inputs['To Max'].default_value = 0.42 if not deri else 0.38
    ln.new(bw.outputs['Val'], mr.inputs['Value'])
    ln.new(mr.outputs['Result'], b.inputs['Roughness'])
    if deri:
        b.inputs['Subsurface Weight'].default_value = 0.25
        b.inputs['Subsurface Radius'].default_value = (1.0, 0.4, 0.22)
        b.inputs['Subsurface Scale'].default_value = 0.006
    else:
        try:
            b.inputs['Sheen Weight'].default_value = 0.35
            b.inputs['Sheen Roughness'].default_value = 0.5
        except Exception:
            pass


for m in govde.data.materials:
    if m.name.startswith("m020_body"):
        rb_mat(m, doku_1880(), rb_tex("m020_body_normal.tga"), rb_tex("m020_body_specular.tga"))
    elif m.name.startswith("m020_head"):
        rb_mat(m, img(rb_tex("m020_head_color.tga")), rb_tex("m020_head_normal.tga"), rb_tex("m020_head_specular.tga"), deri=True)
    elif m.name.startswith("m020_opacity"):
        im = img(rb_tex("m020_opacity_color.tga"))
        im.alpha_mode = 'STRAIGHT'
        rb_mat(m, im, None, None, opak=True)
for p in govde.data.polygons:
    p.use_smooth = True
sub = govde.modifiers.new("yumusat", 'SUBSURF')
sub.levels = 1
sub.render_levels = 1

bpy.context.view_layer.update()
PB = arm.pose.bones
for pb in PB:
    pb.rotation_mode = 'QUATERNION'


def bas(ad):
    return arm.matrix_world @ PB[ad].head


def kuyruk(ad):
    return arm.matrix_world @ PB[ad].tail


def guncelle():
    bpy.context.view_layer.update()


def dunya_dondur(ad, eksen, aci):
    """Kemiği dünya ekseni etrafında, kendi başı çevresinde döndür."""
    pb = PB[ad]
    q_arm = arm.matrix_world.to_quaternion()
    eksen_a = (q_arm.inverted() @ Vector(eksen)).normalized()
    R = pb.matrix.to_quaternion()
    qd = R.inverted() @ Quaternion(eksen_a, aci) @ R
    pb.rotation_quaternion = pb.rotation_quaternion @ qd
    guncelle()


# Biped kemiklerinin kuyruğu uzvu göstermiyor: uzuv yönü çocuk kemiğin başından
COCUK = {}
for yan in ("L", "R"):
    COCUK["Bip01 %s UpperArm" % yan] = "Bip01 %s Forearm" % yan
    COCUK["Bip01 %s Forearm" % yan] = "Bip01 %s Hand" % yan
    COCUK["Bip01 %s Hand" % yan] = "Bip01 %s Finger2" % yan
    for fi in range(0, 5):
        COCUK["Bip01 %s Finger%d" % (yan, fi)] = "Bip01 %s Finger%d1" % (yan, fi)
        COCUK["Bip01 %s Finger%d1" % (yan, fi)] = "Bip01 %s Finger%d2" % (yan, fi)
COCUK["Bip01 Neck"] = "Bip01 Head"


def uzuv(ad):
    if ad in COCUK:
        return (bas(COCUK[ad]) - bas(ad)).normalized()
    # son parmak boğumu: bir önceki boğumun yönü
    for k, v in COCUK.items():
        if v == ad:
            return (bas(ad) - bas(k)).normalized()
    return (kuyruk(ad) - bas(ad)).normalized()


def yonelt(ad, hedef, oran=1.0):
    """Kemiğin uzuv yönünü dünya hedef yönüne çevir."""
    d = uzuv(ad)
    t = Vector(hedef).normalized()
    eks = d.cross(t)
    if eks.length < 1e-6:
        return
    aci = d.angle(t) * oran
    dunya_dondur(ad, eks.normalized(), aci)


# karakterin ön yönü (burun) ve yan yönleri, iskelet dönmeden önce
guncelle()
UP = Vector((0, 0, 1))
f = (bas("Bip01 L Toe0") + bas("Bip01 R Toe0")) - (bas("Bip01 L Foot") + bas("Bip01 R Foot"))
f.z = 0
ON = f.normalized()
print("Theo ön yönü (içe alındığında):", tuple(round(c, 3) for c in ON))


def dis(yan):  # omuzdan dışarı (yatay)
    v = bas("Bip01 %s UpperArm" % yan) - bas("Bip01 Spine2")
    v.z = 0
    return v.normalized()


# kollar aşağı: üst kol hafif dışa ve öne, ön kol dirsekte bükük
for yan in ("L", "R"):
    o = dis(yan)
    yonelt("Bip01 %s UpperArm" % yan, -UP + o * 0.17 + ON * (0.06 if yan == "L" else 0.10))
    if yan == "L":
        yonelt("Bip01 L Forearm", -UP + ON * 0.30 + o * 0.05)
    else:
        yonelt("Bip01 R Forearm", -UP * 0.75 + ON * 0.62 - o * 0.08)
    # el ön kolun devamı, bilekte hafif içe
    fa = uzuv("Bip01 %s Forearm" % yan)
    yonelt("Bip01 %s Hand" % yan, fa + (-o) * 0.15 + (ON * 0.1 if yan == "R" else Vector()))


# parmaklar: avuca doğru bük
def avuc_normali(yan):
    h = bas("Bip01 %s Hand" % yan)
    p_ = (bas("Bip01 %s Finger1" % yan) + bas("Bip01 %s Finger4" % yan)) / 2
    yan_v = bas("Bip01 %s Finger1" % yan) - bas("Bip01 %s Finger4" % yan)
    d = (p_ - h).normalized()
    n = d.cross(yan_v).normalized()
    # avuç bedene (içe) bakmalı
    if n.dot(-dis(yan)) < 0:
        n = -n
    return n, d


def parmak_buk(yan, acilar, basparmak=(0.15, 0.2, 0.15)):
    n, _ = avuc_normali(yan)
    for fi in range(1, 5):
        for seg, aci in zip(("", "1", "2"), acilar):
            ad = "Bip01 %s Finger%d%s" % (yan, fi, seg)
            d = uzuv(ad)
            eks = d.cross(n)
            if eks.length > 1e-6:
                dunya_dondur(ad, eks.normalized(), aci * (1.0 + 0.12 * (fi - 1)))
    for seg, aci in zip(("", "1", "2"), basparmak):
        ad = "Bip01 %s Finger0%s" % (yan, seg)
        d = uzuv(ad)
        eks = d.cross(n)
        if eks.length > 1e-6:
            dunya_dondur(ad, eks.normalized(), aci)


parmak_buk("L", (0.30, 0.45, 0.30))
parmak_buk("R", (0.45, 0.65, 0.45), basparmak=(0.25, 0.35, 0.2))
# baş: hafif öne eğik (bakış tuvale)
dunya_dondur("Bip01 Head", ON.cross(UP).normalized(), math.radians(6))

# temel pozu sakla
TEMEL = {pb.name: pb.rotation_quaternion.copy() for pb in PB}
TEMEL_LOC = {pb.name: pb.location.copy() for pb in PB}

# mektup: sağ ele bağlı katlanmış kâğıt
guncelle()
n_av, d_par = avuc_normali("R")
el = (bas("Bip01 R Finger1") + bas("Bip01 R Finger4")) / 2
bp_ = bas("Bip01 R Finger01")
mektup_merkez = el * 0.6 + bp_ * 0.4 + d_par * 0.085 + n_av * 0.012
mek = yaprak("mektup", (0, 0, 0), (0.135, 0.20), 0.0, M_KAGIT, kalin=0.0012, egim=-0.02)
# yaprak düzlemi: x ekseni parmak yönüne dik yan, y ekseni parmak yönü, normal avuç normali
yx = d_par.cross(n_av).normalized()
Mrot = Matrix((yx, d_par, n_av)).transposed()
guncelle()
mek.parent = arm
mek.parent_type = 'BONE'
mek.parent_bone = "Bip01 R Hand"
guncelle()
mek.matrix_world = Matrix.Translation(mektup_merkez) @ Mrot.to_4x4()
guncelle()

# Theo'yu yerleştir: tuvale dönük, kameraya ¾ sırtı
THEO_KONUM = Vector((-0.50, 0.40, 0))
hedef_bakis = (SOV_KONUM + Vector((0.05, 0, 0)) - THEO_KONUM)
hedef_bakis.z = 0
hedef_bakis.normalize()
aci_on = math.atan2(ON.y, ON.x)
aci_hedef = math.atan2(hedef_bakis.y, hedef_bakis.x)
arm.rotation_mode = 'XYZ'
arm.rotation_euler.z += (aci_hedef - aci_on)
# boy: 1,82 → 1,76 m (Theo ince ve orta boylu)
arm.scale = arm.scale * (1.76 / 1.82)
guncelle()
ayak = min(bas("Bip01 L Toe0").z, bas("Bip01 R Toe0").z)
gmn, gmx = dunya_bbox([govde])
arm.location += THEO_KONUM - Vector((arm.location.x, arm.location.y, 0)) * 0 - Vector((0, 0, gmn.z))
arm.location.x, arm.location.y = THEO_KONUM.x, THEO_KONUM.y
guncelle()
gmn, gmx = dunya_bbox([govde])
arm.location.z -= gmn.z
guncelle()
print("Theo bbox", tuple(dunya_bbox([govde])[0]), tuple(dunya_bbox([govde])[1]))

# ---------------------------------------------------------------- canlandırma (Theo)
# nefes: 4,2 sn'lik döngü (göğüs ve omuz), baş: 2,2–4,4 sn arasında lambaya doğru ~11° döner
ON_D = (arm.matrix_world.to_quaternion() @ (arm.matrix_world.to_quaternion().inverted() @ Vector((math.cos(aci_hedef), math.sin(aci_hedef), 0)))).normalized()
YAN_D = ON_D.cross(UP).normalized()


def yumusak(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


def poz_kur(kare):
    t = (kare - 1) / FPS
    for pb in PB:
        pb.rotation_quaternion = TEMEL[pb.name].copy()
    guncelle()
    nefes = math.sin(2 * math.pi * t / 4.2)
    dunya_dondur("Bip01 Spine1", YAN_D, math.radians(0.9) * nefes)
    dunya_dondur("Bip01 Spine2", YAN_D, math.radians(1.1) * nefes)
    for yan, s in (("L", 1), ("R", -1)):
        dunya_dondur("Bip01 %s Clavicle" % yan, ON_D, s * math.radians(0.8) * nefes)
    # ağırlık kayması (çok az)
    dunya_dondur("Bip01 Pelvis", ON_D, math.radians(0.6) * math.sin(2 * math.pi * t / 6.0))
    # baş çevirme: lambaya doğru (sağa), sonra hafif geri
    cev = yumusak((t - 2.2) / 2.2) - 0.35 * yumusak((t - 4.8) / 1.2)
    dunya_dondur("Bip01 Neck", UP, -math.radians(4.5) * cev)
    dunya_dondur("Bip01 Head", UP, -math.radians(7.0) * cev)
    dunya_dondur("Bip01 Head", YAN_D, math.radians(2.0) * cev)
    # mektuplu el: hafifçe yukarı
    kal = yumusak((t - 0.8) / 2.5)
    dunya_dondur("Bip01 R Forearm", YAN_D, -math.radians(6) * kal)


def poz_anahtarla():
    for k in range(1, N_KARE + 1):
        poz_kur(k)
        for pb in PB:
            pb.keyframe_insert("rotation_quaternion", frame=k)
    for pb in PB:
        pb.rotation_quaternion = TEMEL[pb.name].copy()


# ---------------------------------------------------------------- ışıklar
# lamba: küçük yarıçaplı nokta ışık (alev), sıcak
L = bpy.data.lights.new("lamba", 'POINT')
L.energy = 20.0
L.shadow_soft_size = 0.012
try:
    L.use_temperature = True
    L.temperature = 2700
except Exception:
    L.color = (1.0, 0.55, 0.22)
lo = bpy.data.objects.new("lamba_isik", L)
sc.collection.objects.link(lo)
lo.location = ALEV + Vector((0, 0, 0.005))
# camın içinden alev parıltısını taşıyan ikinci, daha geniş kaynak (camın yumuşak ışıması)
L2 = bpy.data.lights.new("lamba_cam", 'POINT')
L2.energy = 5.0
L2.shadow_soft_size = 0.05
try:
    L2.use_temperature = True
    L2.temperature = 2800
except Exception:
    L2.color = (1.0, 0.6, 0.3)
lo2 = bpy.data.objects.new("lamba_cam_isik", L2)
sc.collection.objects.link(lo2)
lo2.location = ALEV + Vector((0, 0, 0.035))

# ay ışığı: zayıf, soğuk, pencereden
S = bpy.data.lights.new("ay", 'SUN')
S.energy = 0.55
S.angle = math.radians(0.8)
S.color = (0.62, 0.72, 1.0)
so = bpy.data.objects.new("ay_isik", S)
sc.collection.objects.link(so)
so.rotation_mode = 'QUATERNION'
so.rotation_quaternion = Vector((0, 0, -1)).rotation_difference(-ay_yon)

# ---------------------------------------------------------------- kamera
cd = bpy.data.cameras.new("kamera")
cd.lens = 38
cd.sensor_width = 36
cd.dof.use_dof = True
cd.dof.aperture_fstop = 4.0
kam = bpy.data.objects.new("kamera", cd)
sc.collection.objects.link(kam)
sc.camera = kam
odak = bpy.data.objects.new("odak", None)
sc.collection.objects.link(odak)
cd.dof.focus_object = odak
hedef = bpy.data.objects.new("hedef", None)
sc.collection.objects.link(hedef)
tr = kam.constraints.new('TRACK_TO')
tr.target = hedef
tr.track_axis = 'TRACK_NEGATIVE_Z'
tr.up_axis = 'UP_Y'

tablo_merkez = tablo.matrix_world.translation.copy()
K0 = Vector((0.35, -3.00, 1.58))
K1 = Vector((0.75, -1.65, 1.48))
H0 = Vector((0.65, 1.50, 1.18))
H1 = Vector((1.00, 1.60, 1.18))
O0 = (tablo_merkez + ALEV) / 2
kam.location = K0
hedef.location = H0
odak.location = O0


def kamera_anahtarla():
    for k in range(1, N_KARE + 1):
        t = yumusak((k - 1) / (N_KARE - 1))
        kam.location = K0.lerp(K1, t)
        hedef.location = H0.lerp(H1, t)
        cd.lens = 38 + 4 * t
        kam.keyframe_insert("location", frame=k)
        hedef.keyframe_insert("location", frame=k)
        cd.keyframe_insert("lens", frame=k)


# ---------------------------------------------------------------- maske (compositor)
vl = bpy.context.view_layer
vl.use_pass_object_index = True
ng = bpy.data.node_groups.new("bilesim", "CompositorNodeTree")
sc.compositing_node_group = ng
rl = ng.nodes.new("CompositorNodeRLayers")
go = ng.nodes.new("NodeGroupOutput")
try:
    ng.interface.new_socket(name="Image", in_out='OUTPUT', socket_type='NodeSocketColor')
except Exception as e:
    print("arayüz soketi:", e)
guncelle()
cikis = [s for s in rl.outputs if s.name == 'Image'][0]
try:
    gl_ = ng.nodes.new("CompositorNodeGlare")
    for ad_, d_ in (("Type", 'Fog Glow'), ("Quality", 'High')):
        if ad_ in gl_.inputs:
            gl_.inputs[ad_].default_value = d_
    for ad_, d_ in (("Threshold", 2.5), ("Strength", 0.35), ("Size", 0.6)):
        if ad_ in gl_.inputs:
            gl_.inputs[ad_].default_value = d_
    print("Glare girişleri:", [(i.name, getattr(i, 'default_value', None)) for i in gl_.inputs])
    ng.links.new(cikis, gl_.inputs[0])
    cikis = gl_.outputs[0]
except Exception as e:
    print("glare yok:", e)
ng.links.new(cikis, go.inputs[0])
idx_out = None
for s_ in rl.outputs:
    if s_.name in ("IndexOB", "Object Index", "Index OB"):
        idx_out = s_
print("RL çıkışları:", [s_.name for s_ in rl.outputs])
fo = ng.nodes.new("CompositorNodeOutputFile")
fo.directory = KARE_DIZ + os.sep
fo.file_name = "maske_"
try:
    fo.format.media_type = 'IMAGE'
    fo.format.file_format = 'PNG'
    fo.format.color_mode = 'BW'
    fo.format.color_depth = '8'
except Exception as e:
    print("fo biçim:", e)
# iki maske: tablo (indeks 1, beyaz dengeli) ve zarflar (indeks 2, ham renk)
for ad_, ind_ in (("tablo", MASKE_INDEKS), ("zarf", ZARF_INDEKS)):
    idm = ng.nodes.new("CompositorNodeIDMask")
    idm.inputs['Index'].default_value = ind_
    try:
        idm.inputs['Anti-Alias'].default_value = True
    except Exception:
        pass
    ng.links.new(idx_out, idm.inputs[0])
    fo.file_output_items.new('FLOAT', ad_)
    ng.links.new(idm.outputs['Alpha'], fo.inputs[ad_])
print("FileOutput girişleri:", [s_.name for s_ in fo.inputs])


# ---------------------------------------------------------------- karma (grisaille + renkli tablo ve zarflar)
NOTR = 0.7  # tablodaki beyaz dengesi oranı (0: yok, 1: tam)
SIYAH = (0x0b / 255, 0x0a / 255, 0x0a / 255)
BEYAZ = (0xf7 / 255, 0xf0 / 255, 0xe1 / 255)


def png_oku(yol):
    import numpy as np
    im = bpy.data.images.load(yol, check_existing=False)
    im.colorspace_settings.name = 'Non-Color'  # ham sRGB değerleri olduğu gibi
    W_, H_ = im.size
    px = np.empty(W_ * H_ * 4, dtype=np.float32)
    im.pixels.foreach_get(px)
    bpy.data.images.remove(im)
    return px.reshape(H_, W_, 4), W_, H_


def png_yaz(yol, px, W_, H_):
    im = bpy.data.images.new("yaz", W_, H_, alpha=False)
    im.colorspace_settings.name = 'Non-Color'
    im.pixels.foreach_set(px.ravel())
    im.filepath_raw = yol
    im.file_format = 'PNG'
    im.save()
    bpy.data.images.remove(im)


def karma(renkli_yol, kare, cikti_yol):
    import numpy as np
    c, W_, H_ = png_oku(renkli_yol)
    a = np.clip(png_oku(maske_bul(kare, "tablo"))[0][..., 0:1], 0, 1)
    z = np.clip(png_oku(maske_bul(kare, "zarf"))[0][..., 0:1], 0, 1)
    l = 0.2126 * c[..., 0:1] + 0.7152 * c[..., 1:2] + 0.0722 * c[..., 2:3]
    g = np.concatenate([SIYAH[k] + l * (BEYAZ[k] - SIYAH[k]) for k in range(3)], axis=-1)
    # Tablo ve zarflar kendi renkleriyle okunsun: maskeli bölgede lambanın sıcak dökümünü
    # kısmen nötrle (gri dünya kazancı, maske dışındaki orta tonlardan; parlaklık korunur).
    dis_ = (a[..., 0] < 0.01) & (z[..., 0] < 0.01) & (l[..., 0] > 0.08) & (l[..., 0] < 0.8)
    ort = c[..., :3][dis_].mean(axis=0) + 1e-4
    kaz = np.clip((ort.mean() / ort) ** NOTR, 0.75, 1.7)
    cc = c[..., :3] * kaz
    lc = 0.2126 * cc[..., 0:1] + 0.7152 * cc[..., 1:2] + 0.0722 * cc[..., 2:3]
    cc = np.clip(cc * (l / np.maximum(lc, 1e-4)), 0, 1)
    out = c.copy()
    out[..., :3] = g * (1 - a - z).clip(0, 1) + cc * a + c[..., :3] * z
    out[..., 3] = 1.0
    png_yaz(cikti_yol, out, W_, H_)


def maske_bul(kare, tur):
    for f in sorted(os.listdir(KARE_DIZ)):
        if f.startswith("maske_%04d_" % kare) and f.endswith(tur + ".png"):
            return os.path.join(KARE_DIZ, f)
    raise FileNotFoundError("maske %d %s" % (kare, tur))


# ---------------------------------------------------------------- render
os.makedirs(KARE_DIZ, exist_ok=True)
olcum_yol = os.path.join(CIKTI, "olcum.json")
olcum = json.load(open(olcum_yol, encoding="utf-8")) if os.path.exists(olcum_yol) else {}
olcum["gpu"] = GPU_AD
olcum["cihaz_turu"] = GPU_TUR
olcum["blender"] = bpy.app.version_string

kamera_anahtarla()
poz_anahtarla()


def tek_render(kare, yol, ornek, yuzde=100):
    fo.file_name = "maske_%04d_" % kare
    sc.frame_set(kare)
    sc.cycles.samples = ornek
    sc.render.resolution_percentage = yuzde
    sc.render.filepath = yol
    t0 = time.time()
    bpy.ops.render.render(write_still=True)
    return time.time() - t0


if MOD == "onizleme":
    yol = os.path.join(KARE_DIZ, "onizleme.png")
    s = tek_render(TEK_KARE, yol, ORNEK, 50)
    print("ÖNİZLEME", yol, "%.1f sn" % s)

if MOD in ("tek", "hepsi"):
    yol = os.path.join(CIKTI, "oda_renkli.png")
    s = tek_render(TEK_KARE, yol, ORNEK)
    olcum["tek_kare_sn"] = round(s, 2)
    olcum["tek_kare_ornek"] = ORNEK
    karma(yol, TEK_KARE, os.path.join(CIKTI, "oda_karma.png"))
    print("TEK KARE %.1f sn" % s)

if MOD == "kodla":
    KARELER = "%d-%d" % (N_KARE + 1, N_KARE)  # render yok, yalnız mevcut karelerden kodla

if MOD in ("hareket", "hepsi", "kodla"):
    a, b_ = [int(x) for x in KARELER.split("-")]
    sureler = []
    for k in range(a, b_ + 1):
        ry = os.path.join(KARE_DIZ, "renkli_%04d.png" % k)
        s = tek_render(k, ry, ORNEK_H)
        karma(ry, k, os.path.join(KARE_DIZ, "karma_%04d.png" % k))
        sureler.append(s)
        print("KARE %d/%d %.1f sn" % (k, b_, s), flush=True)
    onceki = olcum.get("hareket_sureleri", {})
    for k, s in zip(range(a, b_ + 1), sureler):
        onceki[str(k)] = round(s, 2)
    olcum["hareket_sureleri"] = onceki
    if sureler:
        olcum["hareket_ornek"] = ORNEK_H
    tum = list(onceki.values())
    if tum:
        olcum["hareket_ort_sn"] = round(sum(tum) / len(tum), 2)
    # hepsi hazırsa kodla
    if all(os.path.exists(os.path.join(KARE_DIZ, "karma_%04d.png" % k)) for k in range(1, N_KARE + 1)):
        ff = shutil.which("ffmpeg") or os.environ.get("FFMPEG", "ffmpeg")
        for desen, ad in (("karma_%04d.png", "oda_hareket.mp4"), ("renkli_%04d.png", "oda_hareket_renkli.mp4")):
            cmd = [ff, "-y", "-framerate", str(FPS), "-i", os.path.join(KARE_DIZ, desen),
                   # ffmpeg 9 PNG'nin sRGB (iec61966-2-1) etiketini kaba taşıyor: kare etiketini BT.709'a çevir
                   "-vf", "setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709",
                   "-c:v", "libx264", "-crf", "18",
                   "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
                   "-movflags", "+faststart", os.path.join(CIKTI, ad)]
            print(" ".join(cmd))
            subprocess.run(cmd, check=True)

json.dump(olcum, open(olcum_yol, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("BİTTİ")
