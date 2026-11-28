# -*- coding: utf-8 -*-
"""Van Gogh v4: Theo'nun Paris dairesi (1886–1890), kalıcı oda sahnesi.

Modül olarak:  import oda_kur as O; O.kur(dekor="bekar", isik="gece_lamba", tablo=YOL)
Tek başına (oda.blend üretir):
  blender -b -P van-gogh/blender_v4/oda_kur.py -- --dekor bekar --isik gece_lamba

Dekor: "bekar" (A01–D01) | "evli" (D06–H01). Ek: "besik" (G planları), "sandik" (H01).
Işık: "gece_lamba" | "ogle" | "sabah" | "kis_gun" | "kis_gece" (lamba söner ayrıntısı için de gece).

Testten gelen düzeltmeler (GOREV_1_oda.md §1):
- Tablo ışıktan bağımsız gerçek renginde: yayım (tablo dokusu) + yağlıboya yüzeyi karışımı.
- Pencere: iki kanatlı, küçük camlı, ince yatay ve dikey kayıtlar; koyu dikey şerit dizisi yok. İnce perde (evli).
- Maske: tablo yüzleri ve sarı zarflar nesne indeksi 1.
"""
import bpy
import bmesh
import math
import os
import random
import sys
from mathutils import Vector, Matrix, Quaternion

BURA = os.path.dirname(os.path.abspath(__file__))
DEPO = os.path.abspath(os.path.join(BURA, "..", ".."))
PH = os.path.join(BURA, "varlik", "polyhaven")
GORSEL = os.path.join(DEPO, "van-gogh", "gorsel")
OTOPORTRE = os.path.join(GORSEL, "otoportre_hasir_sapka_1887_met436532.jpg")
GULLER = os.path.join(GORSEL, "aday", "guller_1890_saintremy_met436534.jpg")
MASKE = 1

# oda ölçüleri
X0, X1 = -2.5, 2.5
Y0, Y1 = -3.8, 2.4
H = 3.1
T = 0.16
PX0, PX1, PZ0, PZ1 = -1.95, -0.75, 0.70, 2.65      # pencere (arka duvar)
KY0, KY1, KZ1 = -0.55, 0.45, 2.25                  # kapı (sol duvar)


# ================================================================ yardımcılar
def nodes(m):
    return m.node_tree.nodes, m.node_tree.links


def bsdf(m):
    return [n for n in m.node_tree.nodes if n.type == 'BSDF_PRINCIPLED'][0]


def yeni_mat(ad, renk=None, puruz=0.6):
    m = bpy.data.materials.new(ad)
    if renk is not None:
        b = bsdf(m)
        b.inputs['Base Color'].default_value = (*renk, 1)
        b.inputs['Roughness'].default_value = puruz
    return m


def img(path, renk=True):
    im = bpy.data.images.load(path, check_existing=True)
    if not renk:
        im.colorspace_settings.name = 'Non-Color'
    return im


def pbr(ad, klasor, olcek=0.5, carp=(1, 1, 1), lekeli=False, normal=1.0, puruz_ek=0.0):
    m = yeni_mat(ad)
    nt, ln = nodes(m)
    b = bsdf(m)
    tc = nt.new('ShaderNodeTexCoord')
    mp = nt.new('ShaderNodeMapping')
    mp.inputs['Scale'].default_value = (olcek,) * 3
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
    dif, rgh, nor = tex('_diff_', True), tex('_rough_', False), tex('_nor_gl_', False)
    son = dif.outputs['Color']
    mx = nt.new('ShaderNodeMix'); mx.data_type = 'RGBA'; mx.blend_type = 'MULTIPLY'
    mx.inputs['Factor'].default_value = 1.0
    ln.new(son, mx.inputs['A']); mx.inputs['B'].default_value = (*carp, 1)
    son = mx.outputs['Result']
    if lekeli:
        nz = nt.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 1.6
        nz.inputs['Detail'].default_value = 6; nz.inputs['Roughness'].default_value = 0.62
        ln.new(tc.outputs['Object'], nz.inputs['Vector'])
        cr = nt.new('ShaderNodeValToRGB')
        cr.color_ramp.elements[0].position = 0.45; cr.color_ramp.elements[0].color = (1, 1, 1, 1)
        cr.color_ramp.elements[1].position = 0.78; cr.color_ramp.elements[1].color = (0.66, 0.6, 0.52, 1)
        ln.new(nz.outputs['Fac'], cr.inputs['Fac'])
        m2 = nt.new('ShaderNodeMix'); m2.data_type = 'RGBA'; m2.blend_type = 'MULTIPLY'
        m2.inputs['Factor'].default_value = 1.0
        ln.new(son, m2.inputs['A']); ln.new(cr.outputs['Color'], m2.inputs['B']); son = m2.outputs['Result']
        sep = nt.new('ShaderNodeSeparateXYZ'); ln.new(tc.outputs['Object'], sep.inputs['Vector'])
        mr = nt.new('ShaderNodeMapRange')
        mr.inputs['From Max'].default_value = 0.9; mr.inputs['To Min'].default_value = 0.75
        ln.new(sep.outputs['Z'], mr.inputs['Value'])
        m3 = nt.new('ShaderNodeMix'); m3.data_type = 'RGBA'; m3.blend_type = 'MULTIPLY'
        m3.inputs['Factor'].default_value = 1.0
        ln.new(son, m3.inputs['A']); ln.new(mr.outputs['Result'], m3.inputs['B']); son = m3.outputs['Result']
    ln.new(son, b.inputs['Base Color'])
    if puruz_ek:
        a = nt.new('ShaderNodeMath'); a.operation = 'ADD'; a.use_clamp = True
        ln.new(rgh.outputs['Color'], a.inputs[0]); a.inputs[1].default_value = puruz_ek
        ln.new(a.outputs['Value'], b.inputs['Roughness'])
    else:
        ln.new(rgh.outputs['Color'], b.inputs['Roughness'])
    nm = nt.new('ShaderNodeNormalMap'); nm.inputs['Strength'].default_value = normal
    ln.new(nor.outputs['Color'], nm.inputs['Color']); ln.new(nm.outputs['Normal'], b.inputs['Normal'])
    return m


def kutu(ad, x0, x1, y0, y1, z0, z1, mat, bevel=0.0):
    me = bpy.data.meshes.new(ad)
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts:
        v.co = Vector((x0 + (v.co.x + .5) * (x1 - x0), y0 + (v.co.y + .5) * (y1 - y0), z0 + (v.co.z + .5) * (z1 - z0)))
    bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new(ad, me)
    bpy.context.scene.collection.objects.link(ob)
    if mat:
        ob.data.materials.append(mat)
    if bevel:
        bv = ob.modifiers.new("bevel", 'BEVEL'); bv.width = bevel; bv.segments = 2
    return ob


def kutu_l(ad, merkez, boyut, mat, parent=None, bevel=0.003):
    sx, sy, sz = boyut
    ob = kutu(ad, -sx / 2, sx / 2, -sy / 2, sy / 2, -sz / 2, sz / 2, mat, bevel=min(bevel, min(boyut) * 0.3))
    ob.location = merkez
    if parent:
        ob.parent = parent
    return ob


def cubuk(ad, a, b, kal, mat, parent=None):
    a, b = Vector(a), Vector(b)
    ob = kutu_l(ad, (a + b) / 2, (kal, kal, (b - a).length), mat, parent=parent)
    ob.rotation_mode = 'QUATERNION'
    ob.rotation_quaternion = Vector((0, 0, 1)).rotation_difference((b - a).normalized())
    return ob


def gltf(ad, konum=(0, 0, 0), rot_z=0.0, olcek=(1, 1, 1), sakla=None):
    d = os.path.join(PH, ad)
    yol = [os.path.join(d, f) for f in os.listdir(d) if f.endswith('.gltf')][0]
    once = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=yol)
    yeni = [o for o in bpy.data.objects if o not in once]
    if sakla:
        for o in [o for o in yeni if not sakla(o)]:
            yeni.remove(o); bpy.data.objects.remove(o, do_unlink=True)
    kok = bpy.data.objects.new(ad + "_kok", None)
    bpy.context.scene.collection.objects.link(kok)
    for o in yeni:
        if o.parent is None:
            o.parent = kok
    kok.location = konum; kok.rotation_euler = (0, 0, rot_z); kok.scale = olcek
    bpy.context.view_layer.update()
    return kok, list(kok.children_recursive)


def bbox(objs):
    mn = Vector((1e9,) * 3); mx = Vector((-1e9,) * 3)
    for o in objs:
        if o.type != 'MESH':
            continue
        for c in o.bound_box:
            w = o.matrix_world @ Vector(c)
            mn = Vector(map(min, mn, w)); mx = Vector(map(max, mx, w))
    return mn, mx


def yaprak(ad, merkez, boyut, rz, mat, kalin=0.0008, egim=0.0, indeks=0, rx=0.0):
    me = bpy.data.meshes.new(ad)
    bm = bmesh.new(); uvl = bm.loops.layers.uv.new()
    sx, sy = boyut; n = 12; vs = []
    for j in range(n + 1):
        row = []
        for i in range(n + 1):
            u, v = i / n, j / n
            row.append(bm.verts.new(((u - .5) * sx, (v - .5) * sy, egim * (u - .5) ** 2 + 0.0012 * math.sin(v * 3.1))))
        vs.append(row)
    for j in range(n):
        for i in range(n):
            f = bm.faces.new((vs[j][i], vs[j][i + 1], vs[j + 1][i + 1], vs[j + 1][i]))
            for lp, (ii, jj) in zip(f.loops, [(i, j), (i + 1, j), (i + 1, j + 1), (i, j + 1)]):
                lp[uvl].uv = (ii / n, jj / n)
    bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new(ad, me); bpy.context.scene.collection.objects.link(ob)
    ob.data.materials.append(mat)
    ob.location = merkez; ob.rotation_euler = (rx, 0, rz)
    sl = ob.modifiers.new("kalinlik", 'SOLIDIFY'); sl.thickness = kalin; sl.offset = 1.0
    for p in ob.data.polygons:
        p.use_smooth = True
    ob.pass_index = indeks
    return ob


def duzlem(ad, w, h, mat, parent=None, konum=(0, 0, 0)):
    """xz düzleminde, normali −y'ye bakan UV'li dikdörtgen (tablo yüzü)."""
    me = bpy.data.meshes.new(ad)
    bm = bmesh.new(); uvl = bm.loops.layers.uv.new()
    vv = [bm.verts.new((-w / 2, 0, -h / 2)), bm.verts.new((w / 2, 0, -h / 2)), bm.verts.new((w / 2, 0, h / 2)), bm.verts.new((-w / 2, 0, h / 2))]
    f = bm.faces.new(vv)
    for lp, uv in zip(f.loops, [(0, 0), (1, 0), (1, 1), (0, 1)]):
        lp[uvl].uv = uv
    bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new(ad, me); bpy.context.scene.collection.objects.link(ob)
    ob.data.materials.append(mat)
    if parent:
        ob.parent = parent
    ob.location = konum
    # normal −y olmalı
    if ob.data.polygons[0].normal.y > 0:
        ob.data.polygons[0].flip()
    return ob


# ================================================================ malzemeler
M = {}


def malzemeler():
    M['siva'] = pbr("siva", "plastered_wall_04", 0.55, (0.93, 0.89, 0.81), lekeli=True, normal=2.0)
    M['tavan'] = pbr("tavan", "plastered_wall_04", 0.5, (0.85, 0.82, 0.76))
    M['doseme'] = pbr("doseme", "old_wooden_floor_01", 0.45, (0.85, 0.78, 0.70), puruz_ek=0.05)
    M['ahsap'] = pbr("ahsap", "dark_wooden_planks", 1.6, (0.78, 0.65, 0.52))
    M['ahsap_acik'] = pbr("ahsap_acik", "dark_wooden_planks", 2.0, (1.9, 1.55, 1.15))
    M['pervaz'] = pbr("pervaz", "dark_wooden_planks", 1.2, (0.55, 0.48, 0.40))
    M['pencere_boya'] = yeni_mat("pencere_boya", (0.74, 0.72, 0.66), 0.45)  # boyalı pencere doğraması (açık)
    M['kapi'] = pbr("kapi", "dark_wooden_planks", 1.0, (0.62, 0.52, 0.42))
    M['pirinc'] = yeni_mat("pirinc", (0.72, 0.55, 0.3), 0.3); bsdf(M['pirinc']).inputs['Metallic'].default_value = 1.0
    # cam: saydam + çok hafif yansıma (gölge geçirir)
    m = bpy.data.materials.new("cam"); nt, ln = nodes(m)
    for n in list(nt): nt.remove(n)
    o = nt.new('ShaderNodeOutputMaterial'); tr = nt.new('ShaderNodeBsdfTransparent'); gl = nt.new('ShaderNodeBsdfGlossy')
    gl.inputs['Roughness'].default_value = 0.04
    mx = nt.new('ShaderNodeMixShader'); mx.inputs['Fac'].default_value = 0.08
    ln.new(tr.outputs[0], mx.inputs[1]); ln.new(gl.outputs[0], mx.inputs[2]); ln.new(mx.outputs[0], o.inputs['Surface'])
    M['cam'] = m
    # ince perde: yarı geçirgen keten
    m = bpy.data.materials.new("tul"); nt, ln = nodes(m)
    for n in list(nt): nt.remove(n)
    o = nt.new('ShaderNodeOutputMaterial'); df = nt.new('ShaderNodeBsdfDiffuse'); tl = nt.new('ShaderNodeBsdfTranslucent')
    tr = nt.new('ShaderNodeBsdfTransparent')
    df.inputs['Color'].default_value = (0.82, 0.79, 0.72, 1); tl.inputs['Color'].default_value = (0.85, 0.82, 0.74, 1)
    m1 = nt.new('ShaderNodeMixShader'); m1.inputs['Fac'].default_value = 0.5
    ln.new(df.outputs[0], m1.inputs[1]); ln.new(tl.outputs[0], m1.inputs[2])
    m2 = nt.new('ShaderNodeMixShader'); m2.inputs['Fac'].default_value = 0.45
    ln.new(m1.outputs[0], m2.inputs[1]); ln.new(tr.outputs[0], m2.inputs[2]); ln.new(m2.outputs[0], o.inputs['Surface'])
    M['tul'] = m
    M['zarf'] = yeni_mat("zarf", (0.71, 0.39, 0.07), 0.85)   # ≈ #DBA84C (sRGB), mat kâğıt
    M['tuval_kenar'] = yeni_mat("tuval_kenar", (0.62, 0.57, 0.48), 0.85)
    M['sasi'] = pbr("sasi", "worn_planks", 3.0, (1.0, 0.92, 0.78))
    M['kagit'] = kagit_mat("kagit")
    M['kagit_bos'] = yeni_mat("kagit_bos", (0.86, 0.82, 0.72), 0.75)
    M['kundak'] = kumas_mat("kundak", (0.80, 0.76, 0.66))     # krem, beyaz değil
    M['tig'] = tig_mat("tig")
    M['besik_ic'] = kumas_mat("besik_ic", (0.55, 0.50, 0.42))
    M['cati'] = yeni_mat("cati", (0.06, 0.065, 0.08), 0.55); bsdf(M['cati']).inputs['Metallic'].default_value = 0.4
    M['cephe'] = cephe_mat()
    M['pencere_isik'] = isik_mat("pencere_isik", (1.0, 0.62, 0.28), 1.2)
    M['ay'] = isik_mat("ay", (0.92, 0.94, 1.0), 2.6)


def isik_mat(ad, renk, guc):
    m = yeni_mat(ad, (0, 0, 0))
    b = bsdf(m); b.inputs['Emission Color'].default_value = (*renk, 1); b.inputs['Emission Strength'].default_value = guc
    return m


def kumas_mat(ad, renk):
    m = yeni_mat(ad, renk, 0.85)
    b = bsdf(m); nt, ln = nodes(m)
    b.inputs['Sheen Weight'].default_value = 0.5
    nz = nt.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 400; nz.inputs['Detail'].default_value = 2
    bp = nt.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = 0.15
    ln.new(nz.outputs['Fac'], bp.inputs['Height']); ln.new(bp.outputs['Normal'], b.inputs['Normal'])
    return m


def tig_mat(ad):
    """Tığ işi örtü: yumuşak yuvarlak ilmek tümsekleri (artı/haç deseni yok), krem."""
    m = yeni_mat(ad, (0.66, 0.60, 0.50), 0.9)
    b = bsdf(m); nt, ln = nodes(m)
    b.inputs['Sheen Weight'].default_value = 0.6
    tc = nt.new('ShaderNodeTexCoord')
    vo = nt.new('ShaderNodeTexVoronoi'); vo.inputs['Scale'].default_value = 90.0
    vo.feature = 'SMOOTH_F1' if hasattr(vo, 'feature') else vo.feature
    ln.new(tc.outputs['Object'], vo.inputs['Vector'])
    bp = nt.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = 0.6; bp.inputs['Distance'].default_value = 0.003
    ln.new(vo.outputs['Distance'], bp.inputs['Height']); ln.new(bp.outputs['Normal'], b.inputs['Normal'])
    return m


def kagit_mat(ad, temel=(0.86, 0.82, 0.72), yazi_renk=(0.25, 0.17, 0.10)):
    m = yeni_mat(ad, temel, 0.75)
    nt, ln = nodes(m); b = bsdf(m)
    tc = nt.new('ShaderNodeTexCoord'); sep = nt.new('ShaderNodeSeparateXYZ'); ln.new(tc.outputs['UV'], sep.inputs['Vector'])
    wv = nt.new('ShaderNodeTexWave'); wv.wave_type = 'BANDS'; wv.bands_direction = 'Y'
    wv.inputs['Scale'].default_value = 7.0; wv.inputs['Distortion'].default_value = 1.5
    ln.new(tc.outputs['UV'], wv.inputs['Vector'])
    nz = nt.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 140.0; ln.new(tc.outputs['UV'], nz.inputs['Vector'])
    c1 = nt.new('ShaderNodeValToRGB'); c1.color_ramp.elements[1].position = 0.12; ln.new(wv.outputs['Fac'], c1.inputs['Fac'])
    c2 = nt.new('ShaderNodeValToRGB'); c2.color_ramp.elements[0].position = 0.42; c2.color_ramp.elements[1].position = 0.55
    ln.new(nz.outputs['Fac'], c2.inputs['Fac'])
    r1 = nt.new('ShaderNodeMapRange'); r1.inputs['From Min'].default_value = 0.08; r1.inputs['From Max'].default_value = 0.1
    ln.new(sep.outputs['X'], r1.inputs['Value'])
    r2 = nt.new('ShaderNodeMapRange'); r2.inputs['From Min'].default_value = 0.92; r2.inputs['From Max'].default_value = 0.9
    ln.new(sep.outputs['X'], r2.inputs['Value'])

    def mt(op, a, b_=None, v=None):
        n = nt.new('ShaderNodeMath'); n.operation = op
        ln.new(a, n.inputs[0])
        if b_ is not None: ln.new(b_, n.inputs[1])
        if v is not None: n.inputs[1].default_value = v
        return n.outputs['Value']
    inv = nt.new('ShaderNodeMath'); inv.operation = 'SUBTRACT'; inv.inputs[0].default_value = 1.0
    ln.new(c1.outputs['Color'], inv.inputs[1])
    f = mt('MULTIPLY', mt('MULTIPLY', mt('MULTIPLY', inv.outputs['Value'], c2.outputs['Color']), mt('MULTIPLY', r1.outputs['Result'], r2.outputs['Result'])), None, 0.85)
    mx = nt.new('ShaderNodeMix'); mx.data_type = 'RGBA'
    mx.inputs['A'].default_value = (*temel, 1); mx.inputs['B'].default_value = (*yazi_renk, 1)
    ln.new(f, mx.inputs['Factor']); ln.new(mx.outputs['Result'], b.inputs['Base Color'])
    return m


def cephe_mat():
    """Uzak Paris cepheleri: krem kesme taş, hafif lekeli (pencereler uzakta seçilmez)."""
    m = yeni_mat("cephe", (0.45, 0.42, 0.37), 0.85)
    nt, ln = nodes(m); b = bsdf(m)
    nz = nt.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 0.8; nz.inputs['Detail'].default_value = 5
    cr = nt.new('ShaderNodeValToRGB')
    cr.color_ramp.elements[0].color = (0.30, 0.28, 0.25, 1); cr.color_ramp.elements[1].color = (0.52, 0.49, 0.43, 1)
    ln.new(nz.outputs['Fac'], cr.inputs['Fac']); ln.new(cr.outputs['Color'], b.inputs['Base Color'])
    return m


def tablo_mat(ad, yol, yayim=1.0):
    """Tablo: gerçek rengi ışıktan bağımsız (yayım) + yağlıboya yüzeyi (kabartı, vernik)."""
    m = bpy.data.materials.new(ad); nt, ln = nodes(m)
    for n in list(nt): nt.remove(n)
    o = nt.new('ShaderNodeOutputMaterial')
    t = nt.new('ShaderNodeTexImage'); t.image = img(yol); t.interpolation = 'Cubic'
    b = nt.new('ShaderNodeBsdfPrincipled')
    ln.new(t.outputs['Color'], b.inputs['Base Color'])
    b.inputs['Roughness'].default_value = 0.4
    b.inputs['Coat Weight'].default_value = 0.12; b.inputs['Coat Roughness'].default_value = 0.3
    bw = nt.new('ShaderNodeRGBToBW'); ln.new(t.outputs['Color'], bw.inputs['Color'])
    bp = nt.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = 0.25; bp.inputs['Distance'].default_value = 0.0015
    ln.new(bw.outputs['Val'], bp.inputs['Height']); ln.new(bp.outputs['Normal'], b.inputs['Normal'])
    e = nt.new('ShaderNodeEmission'); ln.new(t.outputs['Color'], e.inputs['Color'])
    e.inputs['Strength'].default_value = yayim
    ad_ = nt.new('ShaderNodeAddShader')
    ln.new(b.outputs[0], ad_.inputs[0]); ln.new(e.outputs[0], ad_.inputs[1]); ln.new(ad_.outputs[0], o.inputs['Surface'])
    m["yayim_dugumu"] = e.name
    return m


# ================================================================ yapı
def oda():
    kutu("doseme", X0 - T, X1 + T, Y0 - T, Y1 + T, -0.1, 0.0, M['doseme'])
    kutu("tavan", X0 - T, X1 + T, Y0 - T, Y1 + T, H, H + 0.1, M['tavan'])
    # sol duvar kapı boşluklu
    kutu("duvar_sol_on", X0 - T, X0, Y0, KY0, 0, H, M['siva'])
    kutu("duvar_sol_arka", X0 - T, X0, KY1, Y1, 0, H, M['siva'])
    kutu("duvar_sol_ust", X0 - T, X0, KY0, KY1, KZ1, H, M['siva'])
    kutu("duvar_sag", X1, X1 + T, Y0, Y1, 0, H, M['siva'])
    kutu("duvar_on", X0, X1, Y0 - T, Y0, 0, H, M['siva'])
    kutu("duvar_arka_sol", X0, PX0, Y1, Y1 + T, 0, H, M['siva'])
    kutu("duvar_arka_sag", PX1, X1, Y1, Y1 + T, 0, H, M['siva'])
    kutu("duvar_arka_alt", PX0, PX1, Y1, Y1 + T, 0, PZ0, M['siva'])
    kutu("duvar_arka_ust", PX0, PX1, Y1, Y1 + T, PZ1, H, M['siva'])
    sp = 0.15
    for ad, a in (("sup_arka1", (X0, PX0, Y1 - .02, Y1)), ("sup_arka2", (PX0, PX1, Y1 - .02, Y1)), ("sup_arka3", (PX1, X1, Y1 - .02, Y1)),
                  ("sup_sol1", (X0, X0 + .02, Y0, KY0)), ("sup_sol2", (X0, X0 + .02, KY1, Y1)), ("sup_sag", (X1 - .02, X1, Y0, Y1))):
        kutu(ad, *a, 0, sp, M['pervaz'])
    # kartonpiyer (tavan pervazı)
    for ad, a in (("korn_arka", (X0, X1, Y1 - .05, Y1)), ("korn_sol", (X0, X0 + .05, Y0, Y1)), ("korn_sag", (X1 - .05, X1, Y0, Y1))):
        kutu(ad, *a, H - 0.08, H, M['tavan'])
    kapi()
    pencere()


def kapi():
    """Sol duvarda kapı: kasa + paneli kapı kanadı (G01'de açılır). Kanat menteşesi KY1 tarafında."""
    kalin = 0.07
    kutu("kapi_kasa_on", X0 - 0.01, X0 + 0.05, KY0 - 0.08, KY0, 0, KZ1 + 0.08, M['kapi'], 0.004)
    kutu("kapi_kasa_arka", X0 - 0.01, X0 + 0.05, KY1, KY1 + 0.08, 0, KZ1 + 0.08, M['kapi'], 0.004)
    kutu("kapi_kasa_ust", X0 - 0.01, X0 + 0.05, KY0 - 0.08, KY1 + 0.08, KZ1, KZ1 + 0.08, M['kapi'], 0.004)
    mente = bpy.data.objects.new("kapi_mentese", None); bpy.context.scene.collection.objects.link(mente)
    mente.location = (X0 - 0.03, KY1, 0)
    w = KY1 - KY0
    k = kutu("kapi_kanat", -kalin / 2, kalin / 2, -w, 0, 0.005, KZ1 - 0.005, M['kapi'], 0.004)
    k.parent = mente
    # paneller (çıkıntılı çerçeve, iki dikey panel)
    for i, (y0, y1) in enumerate(((-w + 0.09, -w / 2 - 0.04), (-w / 2 + 0.04, -0.09))):
        for z0, z1 in ((0.15, 0.95), (1.1, KZ1 - 0.15)):
            p = kutu("kapi_panel_%d_%d" % (i, z0 > 1), kalin / 2, kalin / 2 + 0.012, y0, y1, z0, z1, M['kapi'], 0.006)
            p.parent = mente
    tok = bpy.ops.mesh.primitive_uv_sphere_add(radius=0.03, location=(kalin / 2 + 0.05, -w + 0.08, 1.0))
    t = bpy.context.active_object; t.name = "kapi_tokmak"; t.data.materials.append(M['pirinc']); t.parent = mente
    return mente


def pencere():
    """İki kanatlı, küçük camlı pencere; ince boyalı kayıtlar (3 sıra × 2 sütun cam / kanat)."""
    FY0, FY1 = Y1 + 0.04, Y1 + 0.09
    pb = M['pencere_boya']
    kutu("pen_kasa_sol", PX0, PX0 + 0.06, FY0, FY1, PZ0, PZ1, pb, 0.004)
    kutu("pen_kasa_sag", PX1 - 0.06, PX1, FY0, FY1, PZ0, PZ1, pb, 0.004)
    kutu("pen_kasa_ust", PX0, PX1, FY0, FY1, PZ1 - 0.07, PZ1, pb, 0.004)
    kutu("pen_kasa_alt", PX0, PX1, FY0, FY1, PZ0, PZ0 + 0.08, pb, 0.004)
    mx = (PX0 + PX1) / 2
    kutu("pen_orta", mx - 0.03, mx + 0.03, FY0 - 0.005, FY1, PZ0, PZ1, pb, 0.004)
    ic = 0.022
    for k, (a, b) in enumerate(((PX0 + 0.06, mx - 0.03), (mx + 0.03, PX1 - 0.06))):
        c = (a + b) / 2
        kutu("pen_dikey_%d" % k, c - ic / 2, c + ic / 2, FY0 + 0.012, FY1 - 0.012, PZ0 + 0.08, PZ1 - 0.07, pb, 0.003)
        for r in (1, 2):
            z = PZ0 + 0.08 + r * (PZ1 - 0.07 - PZ0 - 0.08) / 3
            kutu("pen_yatay_%d_%d" % (k, r), a, b, FY0 + 0.012, FY1 - 0.012, z - ic / 2, z + ic / 2, pb, 0.003)
    kutu("pen_cam", PX0 + 0.04, PX1 - 0.04, Y1 + 0.063, Y1 + 0.066, PZ0 + 0.05, PZ1 - 0.05, M['cam'])
    kutu("pen_esik", PX0 - 0.08, PX1 + 0.08, Y1 - 0.1, Y1 + 0.04, PZ0 - 0.035, PZ0, pb, 0.004)
    # pencere içi derinlik (iç yan yüzler duvarla aynı sıva)


def perde():
    """İnce tül perde (evli): pencerenin iki yanında hafif kıvrımlı, yarı saydam."""
    def p(ad, x0, x1):
        me = bpy.data.meshes.new(ad); bm = bmesh.new()
        nx, nz = 70, 30; vs = []
        for j in range(nz + 1):
            z = 0.25 + (PZ1 + 0.2 - 0.25) * j / nz; row = []
            for i in range(nx + 1):
                u = i / nx
                d = 0.6 * math.sin(u * 8 * 2 * math.pi + 0.6 * math.sin(z)) + 0.4 * math.sin(u * 13 * 2 * math.pi + 2)
                row.append(bm.verts.new((x0 + (x1 - x0) * u, Y1 - 0.06 - 0.02 * (0.5 + 0.5 * d), z)))
            vs.append(row)
        for j in range(nz):
            for i in range(nx):
                bm.faces.new((vs[j][i], vs[j][i + 1], vs[j + 1][i + 1], vs[j + 1][i]))
        bm.to_mesh(me); bm.free()
        ob = bpy.data.objects.new(ad, me); bpy.context.scene.collection.objects.link(ob)
        ob.data.materials.append(M['tul'])
        for f in ob.data.polygons: f.use_smooth = True
    p("perde_sol", PX0 - 0.35, PX0 + 0.22)
    p("perde_sag", PX1 - 0.22, PX1 + 0.35)
    rod = cubuk("korniz", (PX0 - 0.45, Y1 - 0.06, PZ1 + 0.24), (PX1 + 0.45, Y1 - 0.06, PZ1 + 0.24), 0.022, M['pirinc'])


def disari(gunduz):
    rnd = random.Random(7)
    for sira, yy in enumerate((10, 17, 27, 41)):
        x = -18 + rnd.uniform(-2, 2)
        while x < 12:
            w = rnd.uniform(6, 10) * (1 + sira * 0.2)
            h = rnd.uniform(-4.0, -1.2) + sira * 1.4
            yb = yy + rnd.uniform(-1.5, 1.5); d = rnd.uniform(6, 10)
            kutu("bina", x, x + w * 0.97, yb - d / 2, yb + d / 2, -14, h, M['cephe'])
            # mansard
            me = bpy.data.meshes.new("cati"); bm = bmesh.new(); i = 0.22 * min(w, d); ch = rnd.uniform(1.6, 2.6)
            a = [(x, yb - d / 2), (x + w * .97, yb - d / 2), (x + w * .97, yb + d / 2), (x, yb + d / 2)]
            u = [(x + i, yb - d / 2 + i), (x + w * .97 - i, yb - d / 2 + i), (x + w * .97 - i, yb + d / 2 - i), (x + i, yb + d / 2 - i)]
            va = [bm.verts.new((p[0], p[1], h)) for p in a]; vu = [bm.verts.new((p[0], p[1], h + ch)) for p in u]
            for k in range(4):
                bm.faces.new((va[k], va[(k + 1) % 4], vu[(k + 1) % 4], vu[k]))
            bm.faces.new(vu); bm.to_mesh(me); bm.free()
            ob = bpy.data.objects.new("cati", me); bpy.context.scene.collection.objects.link(ob); ob.data.materials.append(M['cati'])
            for _ in range(rnd.randint(1, 3)):
                bx = x + w / 2 + rnd.uniform(-w / 3, w / 3); bh = rnd.uniform(0.8, 1.6); bw = rnd.uniform(0.5, 1.1)
                kutu("baca", bx - bw / 2, bx + bw / 2, yb - .3, yb + .3, h, h + ch + bh, M['cephe'])
                for q in range(rnd.randint(2, 4)):
                    px = bx - bw / 2 + 0.15 + q * 0.22
                    if px > bx + bw / 2 - 0.1: break
                    kutu("comlek", px - .05, px + .05, yb - .05, yb + .05, h + ch + bh, h + ch + bh + .35, M['cati'])
            if not gunduz and rnd.random() < 0.5:
                wx = x + rnd.uniform(1, w - 1)
                kutu("isik", wx - .25, wx + .25, yb - d / 2 - .02, yb - d / 2 + .05, h - 1.6, h - 0.6, M['pencere_isik'])
            x += w


AY_YON = Vector((-0.55, 2.0, 0.34)).normalized()


def gokyuzu(isik):
    w = bpy.data.worlds.new("gok"); bpy.context.scene.world = w
    nt, ln = nodes(w)
    for n in list(nt): nt.remove(n)
    wo = nt.new('ShaderNodeOutputWorld'); bg = nt.new('ShaderNodeBackground')
    tc = nt.new('ShaderNodeTexCoord'); sep = nt.new('ShaderNodeSeparateXYZ'); ln.new(tc.outputs['Generated'], sep.inputs['Vector'])
    gr = nt.new('ShaderNodeValToRGB'); ln.new(sep.outputs['Z'], gr.inputs['Fac'])
    e0, e1 = gr.color_ramp.elements
    if isik in ("gece_lamba", "kis_gece"):
        e0.color = (0.010, 0.013, 0.024, 1); e1.position = 0.35; e1.color = (0.0025, 0.0035, 0.008, 1); guc = 1.0
        dot = nt.new('ShaderNodeVectorMath'); dot.operation = 'DOT_PRODUCT'
        ln.new(tc.outputs['Generated'], dot.inputs[0]); dot.inputs[1].default_value = tuple(AY_YON)
        pw = nt.new('ShaderNodeMath'); pw.operation = 'POWER'; pw.use_clamp = True
        ln.new(dot.outputs['Value'], pw.inputs[0]); pw.inputs[1].default_value = 400
        hl = nt.new('ShaderNodeMix'); hl.data_type = 'RGBA'; hl.blend_type = 'ADD'
        ln.new(pw.outputs['Value'], hl.inputs['Factor']); ln.new(gr.outputs['Color'], hl.inputs['A'])
        hl.inputs['B'].default_value = (0.05, 0.06, 0.09, 1); son = hl.outputs['Result']
    elif isik == "kis_gun":
        e0.color = (0.55, 0.58, 0.62, 1); e1.position = 0.6; e1.color = (0.42, 0.46, 0.52, 1); guc = 1.0; son = gr.outputs['Color']
    elif isik == "sabah":
        e0.color = (0.75, 0.70, 0.62, 1); e1.position = 0.5; e1.color = (0.30, 0.42, 0.62, 1); guc = 0.9; son = gr.outputs['Color']
    else:  # öğle
        e0.color = (0.70, 0.74, 0.80, 1); e1.position = 0.5; e1.color = (0.25, 0.40, 0.70, 1); guc = 1.0; son = gr.outputs['Color']
    ln.new(son, bg.inputs['Color']); bg.inputs['Strength'].default_value = guc
    ln.new(bg.outputs['Background'], wo.inputs['Surface'])


# ================================================================ mobilya
NES = {}


def mobilya(dekor, tablo_yolu, yayim):
    # yazı masası (sağ duvara dik)
    k, o = gltf("WoodenTable_01", (X1 - 0.30, 1.25, 0), math.radians(90), (0.78, 0.85, 1.35))
    mn, mx = bbox(o); NES['masa_z'] = mx.z; NES['masa'] = (mn, mx)
    z = mx.z
    # sandalye (masaya dönük)
    NES['sandalye'] = gltf("gallinera_chair", (1.42, 1.48, 0), math.radians(-72), (0.92,) * 3)[0]
    # lamba
    lk, lo = gltf("vintage_oil_lamp", (1.99, 1.02, z), 0, (0.62,) * 3)
    NES['lamba'] = (lk, lo)
    kitap = gltf("book_encyclopedia_set_01", (2.27, 1.66, z), math.radians(90), (0.95,) * 3,
                 sakla=lambda ob: ob.type != 'MESH' or any(ob.name.endswith("book%02d" % i) for i in range(1, 8)))
    g, _ = gltf("round_spectacles", (1.98, 1.30, z), 0)
    g.rotation_euler = (math.radians(90), 0, math.radians(70)); bpy.context.view_layer.update()
    gmn, _ = bbox(g.children_recursive); g.location.z += z + 0.001 - gmn.z
    zz = z + 0.0005
    yaprak("kagit1", (2.06, 1.42, zz), (0.21, 0.27), math.radians(98), M['kagit'], egim=0.01)
    yaprak("kagit2", (2.13, 1.18, zz + .001), (0.21, 0.27), math.radians(76), M['kagit'], egim=0.012)
    yaprak("kagit3", (2.20, 1.36, zz + .002), (0.21, 0.27), math.radians(87), M['kagit_bos'])
    NES['zarflar'] = [yaprak("zarf%d" % i, (x, y, zz + 0.003 + i * 0.0025), (0.16, 0.105), math.radians(r), M['zarf'], 0.0015, indeks=MASKE)
                      for i, (x, y, r) in enumerate([(2.02, 0.74, 102), (2.04, 0.72, 84), (2.00, 0.75, 115), (1.97, 1.58, 60)])]
    # raf (sol duvar, kapının arkasında) ve kitaplar
    raf_kur()
    # şövale + tablo
    NES['sovale'] = sovale(Vector((0.25, 1.82, 0)), math.radians(14), tablo_yolu, yayim)
    # duvara dayalı tuvaller (sol duvar önü, raf altı): ikisi yüzü dönük (tablo), biri arkadan
    dayali(dekor)
    if dekor in ("evli",):
        sk, so = gltf("wicker_basket_01", (2.10, 1.60, z), math.radians(20), (0.55,) * 3)
        NES['sepet'] = sk


def raf_kur():
    """Sol duvarda iki raflı basit kitaplık rafı (konsollu tahta) ve eski kitaplar."""
    y0, y1 = 0.95, 2.05
    for i, z in enumerate((1.35, 1.72)):
        kutu("raf_tahta%d" % i, X0, X0 + 0.24, y0, y1, z, z + 0.025, M['ahsap'], 0.003)
        for y in (y0 + 0.08, y1 - 0.08):
            kutu("raf_konsol%d" % i, X0, X0 + 0.2, y - 0.012, y + 0.012, z - 0.16, z, M['ahsap'], 0.003)
        kk, ko = gltf("book_encyclopedia_set_01", (X0 + 0.13, y0 + 0.12 + i * 0.2, z + 0.025), math.radians(90 if i else 92), (0.9,) * 3)
    NES['raf'] = (y0, y1)


def sovale(konum, rot, tablo_yolu, yayim, ad="sov"):
    sv = bpy.data.objects.new(ad, None); bpy.context.scene.collection.objects.link(sv)
    sv.location = konum; sv.rotation_euler = (0, 0, rot)
    tw, th = 0.50, 0.50 * 1600 / 1286
    if tablo_yolu:
        im = img(tablo_yolu); w_, h_ = im.size; th = tw * h_ / w_
    raf = 1.0
    cubuk(ad + "_sol", (-0.33, -0.02, 0), (-0.035, 0.03, 1.86), 0.032, M['ahsap'], sv)
    cubuk(ad + "_sag", (0.33, -0.02, 0), (0.035, 0.03, 1.86), 0.032, M['ahsap'], sv)
    cubuk(ad + "_arka", (0.0, 0.46, 0), (0.0, 0.06, 1.78), 0.03, M['ahsap'], sv)
    lx = 0.33 - (0.33 - 0.035) * raf / 1.86
    kutu_l(ad + "_raf", (0, -0.045, raf), (2 * lx + 0.06, 0.07, 0.025), M['ahsap'], sv)
    kutu_l(ad + "_dudak", (0, -0.078, raf + 0.018), (2 * lx + 0.06, 0.008, 0.03), M['ahsap'], sv)
    tz = raf + 0.0125 + th / 2
    kutu_l(ad + "_tuval", (0, -0.018, tz), (tw, 0.022, th), M['tuval_kenar'], sv)
    yuz = None
    if tablo_yolu:
        tm = tablo_mat("tablo_" + os.path.basename(tablo_yolu)[:20], tablo_yolu, yayim)
        yuz = duzlem(ad + "_tablo", tw - 0.002, th - 0.002, tm, sv, (0, -0.0295, tz))
        yuz.pass_index = MASKE
    return {"kok": sv, "yuz": yuz, "merkez_z": tz, "boy": (tw, th)}


def dayali(dekor):
    """Duvara dayalı tuvaller: iki Vincent tuvali yüzü dönük (maske), biri arkadan (yalnız çevre çıtası)."""
    adaylar = [os.path.join(GORSEL, "aday", f) for f in ("aycicekleri_1887_met436524.jpg", "selviler_1889_met437980.jpg")]
    if dekor == "evli":
        adaylar = [os.path.join(GORSEL, "aday", f) for f in ("vazoda_irisler_1890_saintremy_met436528.jpg", "zeytin_agaclari_1889_saintremy_met437998.jpg")]
    x = X0 + 0.06
    for i, (yol, y, w) in enumerate(zip(adaylar, (0.95, 1.55), (0.55, 0.62))):
        k = bpy.data.objects.new("dayali%d" % i, None); bpy.context.scene.collection.objects.link(k)
        im = img(yol); h = w * im.size[1] / im.size[0]
        k.location = (x + 0.12, y, 0); k.rotation_euler = (math.radians(-12), 0, math.radians(90))
        kutu_l("dayali%d_sasi" % i, (0, 0.012, h / 2), (w, 0.02, h), M['tuval_kenar'], k)
        yz = duzlem("dayali%d_yuz" % i, w - 0.004, h - 0.004, tablo_mat("tablo_dayali%d" % i, yol, 0.35), k, (0, -0.0001, h / 2))
        yz.pass_index = MASKE
    # arkadan görünen tuval: yalnız çevre çıtası (çapraz ya da orta çıta yok)
    k = bpy.data.objects.new("dayali_arka", None); bpy.context.scene.collection.objects.link(k)
    w, h = 0.6, 0.75
    k.location = (x + 0.14, 2.05, 0); k.rotation_euler = (math.radians(-12), 0, math.radians(90))
    arka_tuval(k, w, h)


def arka_tuval(parent, w, h, ad="arka"):
    kutu_l(ad + "_bez", (0, 0.0, h / 2), (w, 0.004, h), M['tuval_kenar'], parent)
    c = 0.045
    for nm, (cx, cz, sx, sz) in {"alt": (0, c / 2, w, c), "ust": (0, h - c / 2, w, c),
                                 "sol": (-w / 2 + c / 2, h / 2, c, h - 2 * c), "sag": (w / 2 - c / 2, h / 2, c, h - 2 * c)}.items():
        kutu_l(ad + "_cita_" + nm, (cx, -0.014, cz), (sx, 0.022, sz), M['sasi'], parent)


def besik(konum=(-0.95, 1.05, 0), rot=math.radians(20)):
    """Beşik: açık ahşap, kavisli sallanma ayakları, baş ucunda kubbe; içinde krem kundak.
    Kapalı kutu yok: yanlar parmaklıklı (yalnız dikey çubuk), koyu renk yok."""
    k = bpy.data.objects.new("besik", None); bpy.context.scene.collection.objects.link(k)
    k.location = konum; k.rotation_euler = (0, 0, rot)
    L, W, zt, zb = 0.95, 0.52, 0.64, 0.36   # uzunluk (x), genişlik (y), üst kenar, taban (yan alçak: bebek görünür)
    A = M['ahsap_acik']
    # sallanma ayakları: kavisli (yay) iki kızak
    for s in (-1, 1):
        pts = [Vector((x, s * (W / 2 - 0.02), 0.04 + 0.10 * (x / (L * 0.58)) ** 2)) for x in [i / 10 * L * 1.16 - L * 0.58 for i in range(11)]]
        for a, b in zip(pts[:-1], pts[1:]):
            cubuk("besik_kizak", a, b, 0.035, A, k)
        for x in (-L / 2 + 0.06, L / 2 - 0.06):  # ayak dikmeleri
            cubuk("besik_dikme", (x, s * (W / 2 - 0.02), 0.04 + 0.10 * (x / (L * 0.58)) ** 2), (x, s * (W / 2 - 0.02), zt), 0.035, A, k)
    # taban
    kutu_l("besik_taban", (0, 0, zb), (L - 0.08, W - 0.06, 0.03), A, k)
    # üst kenar rayları
    for s in (-1, 1):
        kutu_l("besik_ray", (0, s * (W / 2 - 0.02), zt), (L, 0.035, 0.035), A, k)
        kutu_l("besik_ray_alt", (0, s * (W / 2 - 0.02), zb + 0.03), (L, 0.03, 0.03), A, k)
        for i in range(9):  # dikey parmaklıklar
            x = -L / 2 + 0.1 + i * (L - 0.2) / 8
            cubuk("besik_cubuk", (x, s * (W / 2 - 0.02), zb + 0.03), (x, s * (W / 2 - 0.02), zt), 0.016, A, k)
    # ayak ucu: alçak parmaklıklı pano; baş ucu: yüksek pano + kubbe (gölgelik)
    for i in range(6):
        y = -W / 2 + 0.07 + i * (W - 0.14) / 5
        cubuk("besik_ayakucu", (L / 2 - 0.02, y, zb), (L / 2 - 0.02, y, zt), 0.016, A, k)
    kutu_l("besik_bas", (-L / 2 + 0.02, 0, (zb + zt + 0.18) / 2), (0.03, W, zt + 0.18 - zb), A, k)
    # gölgelik: baş ucunda yay biçimli kumaş kubbe (yarım tünel), krem
    me = bpy.data.meshes.new("besik_kubbe"); bm = bmesh.new(); R = W / 2 + 0.01; n = 20; xs = (-L / 2 + 0.02, -L / 2 + 0.22)
    sira = []
    for x in xs:
        sira.append([bm.verts.new((x, R * math.cos(math.pi * i / n), zt + 0.02 + 0.85 * R * math.sin(math.pi * i / n))) for i in range(n + 1)])
    for i in range(n):
        bm.faces.new((sira[0][i], sira[0][i + 1], sira[1][i + 1], sira[1][i]))
    bm.to_mesh(me); bm.free()
    kb = bpy.data.objects.new("besik_kubbe", me); bpy.context.scene.collection.objects.link(kb)
    kb.data.materials.append(M['besik_ic']); kb.parent = k
    sl = kb.modifiers.new("k", 'SOLIDIFY'); sl.thickness = 0.008
    sd = kb.modifiers.new("y", 'SUBSURF'); sd.levels = 1; sd.render_levels = 2
    for f in kb.data.polygons: f.use_smooth = True
    # yatak (düz değil, yumuşak) ve kundak + tığ işi örtü
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=1.0)
    yt = bpy.context.active_object; yt.name = "besik_yatak"; yt.scale = (L / 2 - 0.06, W / 2 - 0.05, 0.08)
    yt.location = (0, 0, zb + 0.09); yt.parent = k; yt.data.materials.append(M['besik_ic'])
    for f in yt.data.polygons: f.use_smooth = True
    kundak = bpy.data.objects.new("kundak_yeri", None); bpy.context.scene.collection.objects.link(kundak)
    kundak.parent = k; kundak.location = (-0.08, 0, zb + 0.11)
    ortu = tig_ortu("tig_ortu", (0.42, W - 0.10))
    ortu.parent = k; ortu.location = (0.22, 0, zb + 0.15)
    NES['besik'] = {"kok": k, "kundak_yeri": kundak, "ortu": ortu, "boy": (L, W, zt), "zb": zb}
    return NES['besik']


def tig_ortu(ad, boyut):
    """Tığ işi örtü: yumuşak kıvrımlı, kenarı yuvarlak fistolu; deseni ilmek tümseği (haç yok)."""
    me = bpy.data.meshes.new(ad); bm = bmesh.new(); uvl = bm.loops.layers.uv.new()
    sx, sy = boyut; n = 30; vs = []
    for j in range(n + 1):
        row = []
        for i in range(n + 1):
            u, v = i / n, j / n
            z = 0.04 * math.sin(math.pi * v) * (0.7 + 0.3 * math.sin(u * 3)) - 0.03 * (1 - math.sin(math.pi * v)) ** 2
            row.append(bm.verts.new(((u - .5) * sx, (v - .5) * sy, z)))
        vs.append(row)
    for j in range(n):
        for i in range(n):
            f = bm.faces.new((vs[j][i], vs[j][i + 1], vs[j + 1][i + 1], vs[j + 1][i]))
            for lp, (ii, jj) in zip(f.loops, [(i, j), (i + 1, j), (i + 1, j + 1), (i, j + 1)]):
                lp[uvl].uv = (ii / n, jj / n)
    bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new(ad, me); bpy.context.scene.collection.objects.link(ob)
    ob.data.materials.append(M['tig'])
    sl = ob.modifiers.new("k", 'SOLIDIFY'); sl.thickness = 0.006
    sd = ob.modifiers.new("y", 'SUBSURF'); sd.levels = 1; sd.render_levels = 1
    for f in ob.data.polygons: f.use_smooth = True
    return ob


def kundak(parent, bebek_bas=None):
    """Kundak: krem (beyaz değil) yumuşak sarılı bez; baş ucu açık, yüz görünür."""
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=20, radius=1.0)
    k = bpy.context.active_object; k.name = "kundak"
    for v in k.data.vertices:
        x, y, z = v.co
        v.co = Vector((x * 0.22 * (1 - 0.15 * (x > 0.6)), y * 0.12, z * 0.095))
    dsp = k.modifiers.new("kivrim", 'DISPLACE')
    tx = bpy.data.textures.new("kundak_kivrim", 'WOOD'); tx.wood_type = 'BANDNOISE'; tx.noise_scale = 0.08; tx.turbulence = 4
    dsp.texture = tx; dsp.strength = 0.012
    for f in k.data.polygons: f.use_smooth = True
    sd = k.modifiers.new("y", 'SUBSURF'); sd.levels = 1; sd.render_levels = 2
    k.data.materials.append(kumas_mat("kundak", (0.58, 0.53, 0.44)))  # krem; MPFB sahipsiz malzemeleri temizlediği için taze
    k.parent = parent
    return k


def sandiklar():
    """H01: taşınma sandıkları; birinin üstünde sarı zarf destesi."""
    a, _ = gltf("wooden_crate_01", (-0.95, 0.70, 0), math.radians(12), (1.0,) * 3)
    b, bo = gltf("wooden_crate_02", (-0.15, 1.35, 0), math.radians(-8), (1.0,) * 3)
    c, co = gltf("wooden_crate_01", (-0.95, 0.70, 0), math.radians(5), (0.8,) * 3)
    bpy.context.view_layer.update()
    amn, amx = bbox(a.children_recursive); c.location.z = amx.z + 0.001
    bpy.context.view_layer.update()
    cmn, cmx = bbox(c.children_recursive)
    ust = cmx.z
    zx, zy = (cmn.x + cmx.x) / 2, (cmn.y + cmx.y) / 2
    NES['deste'] = [yaprak("deste%d" % i, (zx + random.Random(i).uniform(-.02, .02), zy + random.Random(i + 9).uniform(-.02, .02), ust + 0.002 + i * 0.0032),
                           (0.16, 0.105), math.radians(10 + random.Random(i).uniform(-12, 12)), M['zarf'], 0.0018, indeks=MASKE) for i in range(14)]
    # duvara dayalı tuvaller arkadan (yalnız çevre çıtası)
    for i, (y, w, h) in enumerate(((1.95, 0.7, 0.9), (2.05, 0.55, 0.7), (2.15, 0.8, 0.65))):
        k = bpy.data.objects.new("h_arka%d" % i, None); bpy.context.scene.collection.objects.link(k)
        k.location = (-1.6 + i * 0.45, Y1 - 0.12 - i * 0.04, 0); k.rotation_euler = (math.radians(12), 0, 0)
        arka_tuval(k, w, h, "h_arka%d" % i)
    NES['sandik_ust'] = (zx, zy, ust)


# ================================================================ ışık
def isiklar(isik, lamba_acik=True):
    sc = bpy.context.scene
    lk, lo = NES['lamba']
    alev_kart = [o for o in lo if 'flame' in o.name][0]
    cam = [o for o in lo if 'glass' in o.name][0]
    govde = [o for o in lo if 'flame' not in o.name and 'glass' not in o.name and o.type == 'MESH']
    alev_kart.hide_render = True
    cam.visible_shadow = False
    for m_ in cam.data.materials:
        bb = bsdf(m_); bb.inputs['Roughness'].default_value = 0.12
    mn, mx = bbox(govde); amn, amx = bbox([alev_kart])
    alev = Vector(((amn.x + amx.x) / 2, (amn.y + amx.y) / 2, mx.z + 0.018))
    NES['alev_konum'] = alev
    alevler = []
    for ad, r, boy, renk, guc, dz in (("alev_dis", 0.0065, 2.6, (1.0, 0.45, 0.10), 35.0, 0), ("alev_ic", 0.0038, 2.2, (1.0, 0.85, 0.55), 80.0, -0.003)):
        bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=16, radius=r)
        o = bpy.context.active_object; o.name = ad
        for v in o.data.vertices:
            t = min(1.0, max(0.0, (v.co.z / r + 1) / 2)); k = 1 - 0.75 * t ** 1.6
            v.co.x *= k; v.co.y *= k; v.co.z *= boy
        for p in o.data.polygons: p.use_smooth = True
        m = isik_mat(ad, renk, guc); o.data.materials.append(m)
        o.location = alev + Vector((0, 0, dz)); o.visible_shadow = False
        alevler.append(o)
    L = bpy.data.lights.new("lamba", 'POINT'); L.shadow_soft_size = 0.012
    L.use_temperature = True; L.temperature = 2700
    lo_ = bpy.data.objects.new("lamba_isik", L); sc.collection.objects.link(lo_); lo_.location = alev + Vector((0, 0, 0.005))
    L2 = bpy.data.lights.new("lamba_cam", 'POINT'); L2.shadow_soft_size = 0.05; L2.use_temperature = True; L2.temperature = 2800
    lo2 = bpy.data.objects.new("lamba_cam_isik", L2); sc.collection.objects.link(lo2); lo2.location = alev + Vector((0, 0, 0.035))
    NES['lamba_isiklar'] = (L, L2, alevler)
    gece = isik in ("gece_lamba", "kis_gece")
    if gece and lamba_acik:
        L.energy, L2.energy = 20.0, 5.0
    else:
        L.energy, L2.energy = 0.0, 0.0
        for a in alevler: a.hide_render = True
    # gök cismi ve güneş/ay
    if gece:
        bpy.ops.mesh.primitive_uv_sphere_add(segments=48, ring_count=24, radius=1.0)
        ay = bpy.context.active_object; ay.name = "ay"; ay.data.materials.append(M['ay'])
        ay.location = Vector(((PX0 + PX1) / 2, Y1, 1.62)) + AY_YON * 220; ay.scale = (2.3,) * 3; ay.visible_shadow = False
        S = bpy.data.lights.new("ay", 'SUN'); S.energy = 0.55 if isik == "gece_lamba" else 0.35
        S.angle = math.radians(0.8); S.color = (0.62, 0.72, 1.0); yon = AY_YON
    else:
        S = bpy.data.lights.new("gunes", 'SUN')
        if isik == "ogle":
            S.energy, S.angle, yon = 6.0, math.radians(1.0), Vector((-0.35, 1.0, 1.05))
            S.color = (1.0, 0.96, 0.9)
        elif isik == "sabah":
            S.energy, S.angle, yon = 5.0, math.radians(1.2), Vector((-0.75, 1.0, 0.45))
            S.color = (1.0, 0.88, 0.72)
        else:  # kış günü: güneş yok, bulutlu gök
            S.energy, S.angle, yon = 0.0, math.radians(5), Vector((0, 1, 1))
        # pencereden içeri bakan alan ışığı: gök dolgusu (pencere boşluğu kadar)
        A = bpy.data.lights.new("gok_dolgu", 'AREA'); A.shape = 'RECTANGLE'
        A.size, A.size_y = PX1 - PX0, PZ1 - PZ0
        A.energy = {"ogle": 500, "sabah": 420, "kis_gun": 700}[isik]
        A.color = {"ogle": (0.9, 0.95, 1.0), "sabah": (0.95, 0.92, 0.9), "kis_gun": (0.82, 0.88, 1.0)}[isik]
        ao = bpy.data.objects.new("gok_dolgu", A); sc.collection.objects.link(ao)
        ao.location = ((PX0 + PX1) / 2, Y1 + 0.12, (PZ0 + PZ1) / 2)
        ao.rotation_euler = (math.radians(-90), 0, 0)  # −y'ye (odaya) bakar
        ao.visible_camera = False; ao.visible_glossy = False
    so = bpy.data.objects.new(S.name + "_isik", S); sc.collection.objects.link(so)
    so.rotation_mode = 'QUATERNION'; so.rotation_quaternion = Vector((0, 0, -1)).rotation_difference(-yon.normalized())
    return NES


# ================================================================ render ayarı ve maske
def render_ayar(ornek=192):
    sc = bpy.context.scene
    prefs = bpy.context.preferences.addons['cycles'].preferences
    for tur in ('OPTIX', 'CUDA'):
        try:
            prefs.compute_device_type = tur; prefs.get_devices()
            if any(d.type == tur for d in prefs.devices): break
        except Exception:
            pass
    for d in prefs.devices: d.use = (d.type != 'CPU')
    sc.render.engine = 'CYCLES'; sc.cycles.device = 'GPU'
    sc.cycles.samples = ornek; sc.cycles.use_denoising = True
    try: sc.cycles.denoiser = 'OPTIX'
    except Exception: pass
    sc.cycles.seed = 1888; sc.cycles.use_animated_seed = False
    sc.cycles.max_bounces = 8; sc.cycles.diffuse_bounces = 4; sc.cycles.glossy_bounces = 3
    sc.cycles.transparent_max_bounces = 24; sc.cycles.sample_clamp_indirect = 6.0; sc.cycles.blur_glossy = 1.0
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 1920, 1080, 100
    sc.view_settings.view_transform = 'AgX'
    try: sc.view_settings.look = 'AgX - Base Contrast'
    except Exception: pass
    sc.render.image_settings.file_format = 'PNG'; sc.render.image_settings.color_mode = 'RGB'; sc.render.image_settings.color_depth = '8'


def maske_kur(dizin):
    """Compositor: görüntü (hafif parıltı) + nesne indeksi 1'den kenarı yumuşatılmış maske PNG'si."""
    sc = bpy.context.scene
    bpy.context.view_layer.use_pass_object_index = True
    ng = bpy.data.node_groups.new("bilesim", "CompositorNodeTree"); sc.compositing_node_group = ng
    rl = ng.nodes.new("CompositorNodeRLayers"); go = ng.nodes.new("NodeGroupOutput")
    ng.interface.new_socket(name="Image", in_out='OUTPUT', socket_type='NodeSocketColor')
    bpy.context.view_layer.update()
    cikis = rl.outputs['Image']
    gl = ng.nodes.new("CompositorNodeGlare")
    for a, d in (("Type", 'Fog Glow'), ("Quality", 'High'), ("Threshold", 2.5), ("Strength", 0.3), ("Size", 0.6)):
        if a in gl.inputs: gl.inputs[a].default_value = d
    ng.links.new(cikis, gl.inputs[0]); ng.links.new(gl.outputs[0], go.inputs[0])
    idm = ng.nodes.new("CompositorNodeIDMask"); idm.inputs['Index'].default_value = MASKE
    idm.inputs['Anti-Alias'].default_value = True
    ng.links.new([s for s in rl.outputs if s.name in ("Object Index", "IndexOB")][0], idm.inputs[0])
    fo = ng.nodes.new("CompositorNodeOutputFile")
    fo.directory = dizin + os.sep; fo.file_name = "m_"
    fo.format.media_type = 'IMAGE'; fo.format.file_format = 'PNG'; fo.format.color_mode = 'BW'; fo.format.color_depth = '8'
    fo.file_output_items.new('FLOAT', 'maske')
    ng.links.new(idm.outputs['Alpha'], fo.inputs['maske'])
    return fo


# ================================================================ ana giriş
def kur(dekor="bekar", isik="gece_lamba", tablo=OTOPORTRE, besik_var=False, sandik_var=False, perde_var=None,
        lamba_acik=True, yayim=None):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    NES.clear(); M.clear()
    malzemeler()
    oda()
    if perde_var is None:
        perde_var = dekor == "evli"
    if perde_var:
        perde()
    disari(gunduz=isik not in ("gece_lamba", "kis_gece"))
    gokyuzu(isik)
    if yayim is None:  # tablo yayımı: gece lambayla, gündüz pencereyle dengeli
        yayim = {"gece_lamba": 0.9, "kis_gece": 0.9, "ogle": 1.6, "sabah": 1.4, "kis_gun": 1.4}[isik]
    mobilya(dekor, tablo, yayim)
    if besik_var:
        besik()
    if sandik_var:
        sandiklar()
    isiklar(isik, lamba_acik)
    render_ayar()
    bpy.context.scene.view_settings.exposure = {"gece_lamba": 0.35, "kis_gece": 0.35, "ogle": 0.6, "sabah": 0.8, "kis_gun": 1.0}[isik]
    return NES


if __name__ == "__main__":
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    def a(ad, v):
        return argv[argv.index("--" + ad) + 1] if "--" + ad in argv else v
    kur(a("dekor", "bekar"), a("isik", "gece_lamba"), besik_var="--besik" in argv, sandik_var="--sandik" in argv)
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(BURA, "oda.blend"))
    print("oda.blend kaydedildi")
