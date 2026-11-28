# -*- coding: utf-8 -*-
"""Van Gogh v4 oda planları: Blender + GPU (görev: GOREV_1_oda.md).

Kullanım (depo kökünden):
  blender -b -P van-gogh/blender_v4/planlar.py -- --plan A01 [--mod render|olc|kare] [--fps 30|15] [--ornek 160]
    olc   : planın ortasında tek kare render edip süreyi yazar
    kare  : --t saniyesindeki tek kareyi plaka/<PLAN>/deneme.png olarak yazar
    render: plaka/<PLAN>/rgb/0000.png …, maske/0000.png …, bilgi.json
Sonra önizleme (sistem python'u): python van-gogh/blender_v4/onizle.py A01
Zaman: oda_planlari.json (sozcukler[].t, plan içi saniye). Pay: −0,5 sn … sure_sn + 0,5 sn.
"""
import bpy
import bmesh
import json
import math
import os
import shutil
import sys
import time
from mathutils import Vector, Matrix, Quaternion, Euler

BURA = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BURA)
import oda_kur as O      # noqa: E402
import karakter as K     # noqa: E402
import poz               # noqa: E402
from poz import P, UP, gecis, yumusak  # noqa: E402

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []


def arg(ad, v=None):
    return argv[argv.index("--" + ad) + 1] if "--" + ad in argv else v


PLAN = arg("plan", "A01")
MOD = arg("mod", "render")
FPS = int(arg("fps", "30"))
ORNEK = int(arg("ornek", "160"))
PAY = 0.5
VERI = {p["id"]: p for p in json.load(open(os.path.join(BURA, "oda_planlari.json"), encoding="utf-8"))}
PL = VERI[PLAN]
SURE = PL["sure_sn"]


def W(sozcuk, sira=0):
    """Sözcüğün plan içi zamanı (aynı sözcük birden çok geçerse sira)."""
    eş = [s["t"] for s in PL["sozcukler"] if s["w"].lower() == sozcuk.lower() or s.get("s", "").lower() == sozcuk.lower()]
    if not eş:
        eş = [s["t"] for s in PL["sozcukler"] if s["w"].lower().startswith(sozcuk.lower()[:4])]
    return eş[sira]


# ================================================================ ortak parçalar
def kamera(lens=35, fstop=4.0):
    sc = bpy.context.scene
    cd = bpy.data.cameras.new("kamera"); cd.lens = lens; cd.sensor_width = 36
    cd.dof.use_dof = True; cd.dof.aperture_fstop = fstop
    k = bpy.data.objects.new("kamera", cd); sc.collection.objects.link(k); sc.camera = k
    od = bpy.data.objects.new("odak", None); sc.collection.objects.link(od); cd.dof.focus_object = od
    return k, cd, od


def kamera_yerle(k, cd, od, konum, hedef, lens, odak):
    k.location = konum
    k.rotation_mode = 'QUATERNION'
    k.rotation_quaternion = (Vector(hedef) - Vector(konum)).to_track_quat('-Z', 'Y')
    cd.lens = lens
    od.location = odak


def kamera_anahtar(k, cd, od, kare):
    k.keyframe_insert("location", frame=kare); k.keyframe_insert("rotation_quaternion", frame=kare)
    cd.keyframe_insert("lens", frame=kare); od.keyframe_insert("location", frame=kare)


def iki_kemik(f, yan, hedef, kutup):
    """Basit iki kemik IK: el bileğini hedefe, dirseği kutup yönüne."""
    S = f.bas(P + yan + "Arm")
    l1 = (f.bas(P + yan + "ForeArm") - S).length
    l2 = (f.bas(P + yan + "Hand") - f.bas(P + yan + "ForeArm")).length
    T = Vector(hedef)
    d = T - S
    L = min(d.length, (l1 + l2) * 0.999)
    dn = d.normalized()
    a = (l1 * l1 + L * L - l2 * l2) / (2 * L)
    h = math.sqrt(max(0.0, l1 * l1 - a * a))
    k = (Vector(kutup) - dn * Vector(kutup).dot(dn)).normalized()
    E = S + dn * a + k * h
    f.yonelt(P + yan + "Arm", E - S)
    f.yonelt(P + yan + "ForeArm", (S + dn * L) - f.bas(P + yan + "ForeArm"))


def hasir_sapka():
    """Hasır şapka: tepe (silindir, üstü hafif kubbe) + geniş düz kenar; doğal saman rengi, örgü dokusu."""
    prof = [(0.0, 0.110), (0.055, 0.112), (0.082, 0.104), (0.090, 0.07), (0.094, 0.02), (0.096, 0.0),
            (0.12, -0.003), (0.165, -0.010), (0.175, -0.016), (0.168, -0.020), (0.11, -0.010), (0.095, -0.006), (0.090, 0.0)]
    me = bpy.data.meshes.new("sapka"); bm = bmesh.new(); n = 48; halka = []
    for i in range(n):
        a = 2 * math.pi * i / n
        halka.append([bm.verts.new((r * math.cos(a), r * math.sin(a) * 0.9, z)) for r, z in prof])
    for i in range(n):
        for j in range(len(prof) - 1):
            bm.faces.new((halka[i][j], halka[(i + 1) % n][j], halka[(i + 1) % n][j + 1], halka[i][j + 1]))
    bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new("hasir_sapka", me); bpy.context.scene.collection.objects.link(ob)
    for p in ob.data.polygons:
        p.use_smooth = True
    m = bpy.data.materials.new("hasir"); nt, ln = m.node_tree.nodes, m.node_tree.links
    b = [x for x in nt if x.type == 'BSDF_PRINCIPLED'][0]
    tc = nt.new('ShaderNodeTexCoord')
    wv = nt.new('ShaderNodeTexWave'); wv.wave_type = 'RINGS'; wv.inputs['Scale'].default_value = 60
    wv.inputs['Distortion'].default_value = 2.0
    ln.new(tc.outputs['Object'], wv.inputs['Vector'])
    cr = nt.new('ShaderNodeValToRGB')
    cr.color_ramp.elements[0].color = (0.55, 0.42, 0.18, 1); cr.color_ramp.elements[1].color = (0.85, 0.70, 0.38, 1)
    ln.new(wv.outputs['Fac'], cr.inputs['Fac']); ln.new(cr.outputs['Color'], b.inputs['Base Color'])
    bp = nt.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = 0.4
    ln.new(wv.outputs['Fac'], bp.inputs['Height']); ln.new(bp.outputs['Normal'], b.inputs['Normal'])
    b.inputs['Roughness'].default_value = 0.8
    ob.data.materials.append(m)
    sl = ob.modifiers.new("k", 'SOLIDIFY'); sl.thickness = 0.004
    return ob


def sapka_tak(f, sapka, egim=6):
    bas = f.bas(P + "Head")
    tepe = bas + UP * 0.115 + f.on * 0.01
    M = Matrix.Translation(tepe) @ Quaternion(f.sag, math.radians(-egim)).to_matrix().to_4x4() @ \
        Quaternion(UP, math.atan2(f.on.y, f.on.x) - math.pi / 2).to_matrix().to_4x4()
    f.bagla(sapka, P + "Head", M)


def mektup_el(f, yan, mat):
    """Elde katlı mektup (avuçla başparmak arasında)."""
    n, d = f.avuc(yan)
    el = (f.bas(P + yan + "HandIndex1") + f.bas(P + yan + "HandPinky1")) / 2
    m = O.yaprak("mektup_" + yan, (0, 0, 0), (0.135, 0.20), 0.0, mat, kalin=0.0012, egim=-0.02)
    yx = d.cross(n).normalized()
    R = Matrix((yx, d, n)).transposed().to_4x4()
    f.bagla(m, P + yan + "Hand", Matrix.Translation(el + d * 0.07 + n * 0.015) @ R)
    return m


# ================================================================ planlar
def plan_A01():
    """Geniş; bekâr, gece, lamba; şövalede otoportre. Theo şövaleye bakar (sırttan ¾).
    Kamera tuvale ve lambaya doğru yavaş yaklaşır (%45 yol)."""
    N = O.kur("bekar", "gece_lamba", O.OTOPORTRE)
    isk, gov, par = K.theo(29)
    f = poz.Figur(isk)
    f.ayakta(sag_dirsek=0.45)
    tuval = N['sovale']['yuz'].matrix_world.translation.copy()
    f.yerlestir((-0.28, 0.40), tuval)
    f.kaydet()
    lamba = N['alev_konum']
    k, cd, od = kamera(38, 4.0)
    K0, K1 = Vector((0.35, -3.0, 1.58)), Vector((0.85, -1.4, 1.48))
    H0, H1 = Vector((0.70, 1.50, 1.18)), Vector((1.05, 1.55, 1.18))
    K1 = K0.lerp(K1, 1.0)  # yolun %45'i aşağıda (oran)

    def kare(t):
        f.sifirla()
        f.nefes(t)
        # "inandı"da başını hafifçe kaldırıp tuvale bakar, "yazı masası"nda lambaya döner
        f.bak(tuval + Vector((0, 0, -0.05)), oran=0.6 + 0.3 * gecis(t, W("inandı") - 0.3, 1.2))
        don = gecis(t, W("yazı") - 0.4, 1.4)
        f.dondur(P + "Head", UP, -math.radians(9) * don)
        f.dondur(P + "Neck", UP, -math.radians(4) * don)
        u = 0.45 * yumusak((t + PAY) / (SURE + 2 * PAY))
        kamera_yerle(k, cd, od, K0.lerp(K1, u), H0.lerp(H1, u), 38 + 4 * u, (tuval + lamba) / 2)
    return kare, (k, cd, od), [f]


def plan_G02():
    """Yakın; evli, sabah; şövalede Güller. İki kardeş beşiğin başında ayakta, beşik ön planda.
    "tığ"da Vincent tığ işi örtünün ucunu kaldırıp gösterir, Theo hafif güler. Aynı anda iki eğilme yok."""
    N = O.kur("evli", "sabah", O.GULLER, besik_var=True)
    B = N['besik']; bk = B['kok']; L, Wb, zt = B['boy']
    bpy.context.view_layer.update()
    Mb = bk.matrix_world
    # bebek: kundakta, sırtüstü; yalnız baş görünür
    bi, bg, bp = K.bebek()
    bi.scale = (0.55,) * 3
    bi.rotation_euler = (math.radians(-90), 0, 0)
    bpy.context.view_layer.update()
    bf = poz.Figur(bi)
    for yan in ("Left", "Right"):
        bf.yonelt(P + yan + "Arm", -bf.uzuv(P + "Spine") + bf.dis(yan) * 0.15)   # kollar kundak içinde, yanlarda
    bf.kaydet()
    eks = (Mb.to_3x3() @ Vector((-1, 0, 0))).normalized()      # beşiğin baş ucu yönü
    yuk = (bf.bas(P + "Head") - bf.bas(P + "Hips")).normalized()
    a = math.atan2(yuk.cross(eks).z, yuk.dot(eks))
    bi.rotation_euler = (math.radians(-90), 0, a)
    bpy.context.view_layer.update()
    bas_yer = Mb @ Vector((-L / 2 + 0.33, 0, B['zb'] + 0.20))
    bi.location += bas_yer - bf.bas(P + "Head")
    bpy.context.view_layer.update()
    kd = O.kundak(None)
    kmer = (bf.bas(P + "Spine1") + bf.bas(P + "LeftUpLeg")) / 2
    kd.location = kmer - eks * 0.09; kd.rotation_euler = (0, 0, math.atan2(eks.y, eks.x))
    # örtü: Vincent'e yakın köşesi "tığ"da kalkar (şekil anahtarı)
    ortu = B['ortu']
    # kardeşler: beşiğin arkasında ayakta (pencere tarafı)
    vi, vg, vp = K.vincent(37)
    ti, tg, tp = K.theo(33)
    vf, tf = poz.Figur(vi), poz.Figur(ti)
    merkez = Mb @ Vector((0, 0, 0))
    yan_v = (Mb.to_3x3() @ Vector((0, 1, 0))).normalized()
    vk = merkez + yan_v * 0.55 + eks * 0.05
    tk = merkez + yan_v * 0.55 - eks * 0.62
    vf.ayakta(sag_dirsek=0.35); tf.ayakta(sol_dirsek=0.3, sag_dirsek=0.3)
    vf.yerlestir((vk.x, vk.y), merkez + eks * 0.1)
    tf.yerlestir((tk.x, tk.y), merkez + eks * 0.15)
    vf.kaydet(); tf.kaydet()
    sapka = hasir_sapka(); sapka_tak(vf, sapka, egim=-12)
    # örtü: Vincent'e en yakın köşesinden tutulur; "kalk" şekli = elden sarkan kumaş (dünya koordinatında)
    bpy.context.view_layer.update()
    for md in list(ortu.modifiers):
        if md.type == 'SUBSURF':
            ortu.modifiers.remove(md)
    Mo = ortu.matrix_world.copy()
    ortu.parent = None
    ortu.matrix_world = Mo
    me = ortu.data
    for v in me.vertices:                      # örtüyü dünya koordinatına göm
        v.co = Mo @ v.co
    ortu.matrix_world = Matrix.Identity(4)
    vel = vf.bas(P + "RightHand")
    ki = min(range(len(me.vertices)), key=lambda i: (me.vertices[i].co - vel).length)
    kose = me.vertices[ki].co.copy()
    uv0 = {}
    n_ = int(round(math.sqrt(len(me.vertices)))) - 1
    for i in range(len(me.vertices)):
        uv0[i] = (i % (n_ + 1), i // (n_ + 1))
    ku, kv = uv0[ki]
    ortu.shape_key_add(name="temel")
    sk = ortu.shape_key_add(name="kalk")
    gosterme = (vf.bas(P + "Spine2") + vf.on * 0.38 + (tf.bas(P + "Spine2") - vf.bas(P + "Spine2")).normalized() * 0.12)
    gosterme.z = 1.12
    yanv = (tf.bas(P + "Spine2") - vf.bas(P + "Spine2")); yanv.z = 0; yanv.normalize()
    sx, sy = 0.42, 0.42
    for i in range(len(me.vertices)):
        u, v = uv0[i]
        du, dv = abs(u - ku) / n_ * sx, abs(v - kv) / n_ * sy
        d = math.hypot(du, dv)
        yayil = (du - dv) * 0.55
        sk.data[i].co = gosterme + Vector((0, 0, -d * 0.92)) + yanv * yayil + vf.on * (0.03 * math.sin(d * 9) + 0.04 * d)
    bas_bebek = bf.bas(P + "Head")
    k, cd, od = kamera(36, 3.5)
    K0, K1 = merkez - yan_v * 2.55 + eks * 0.2 + UP * 1.92, merkez - yan_v * 2.2 + eks * 0.25 + UP * 1.86
    H = merkez + yan_v * 0.3 + UP * 0.98
    t_tig = W("tığ")

    def kare(t):
        for f_ in (vf, tf):
            f_.sifirla()
        vf.nefes(t, 0.0); tf.nefes(t, 0.37)
        # ikisi de bebeğe bakar; "gözleri yaşlıydı"da Theo başını hafif eğer (gövde dik)
        tf.bak(bas_bebek, oran=0.75 + 0.15 * gecis(t, W("gözleri") - 0.2, 1.0))
        # "tığ": Vincent örtünün ucuna uzanır (8.64), kaldırır, gösterir ("gösterip" 9.76), bırakır
        uz = gecis(t, t_tig - 0.5, 0.6) * (1 - gecis(t, W("gösterip") + 0.9, 0.8))
        kal = gecis(t, t_tig + 0.1, 0.6) * (1 - gecis(t, W("gösterip") + 0.9, 0.8))
        sk.value = kal
        vf.dondur(P + "Spine1", vf.sag, -math.radians(10) * (uz - kal * 0.8))   # yalnız Vincent; uzanırken hafif öne
        vf.dondur(P + "Spine2", vf.sag, -math.radians(6) * (uz - kal * 0.8))
        if uz > 0.001:
            uc = kose.lerp(gosterme, kal)
            dinlen = vf.bas(P + "RightHand")
            iki_kemik(vf, "Right", dinlen.lerp(uc + UP * 0.02, uz), -UP + vf.dis("Right") * 0.7 - vf.on * 0.2)
        vf.bak(bas_bebek if t < W("gösterip") - 0.2 else tf.bas(P + "Head"), oran=0.5)
        # "şaka yapar": Theo hafif güler: başını kaldırıp kardeşine döner, küçük baş sallama
        gul = gecis(t, W("şaka") - 0.2, 0.7)
        tf.dondur(P + "Head", tf.sag, math.radians(10) * gul)
        tf.dondur(P + "Head", UP, math.radians(18) * gul)
        tf.dondur(P + "Head", tf.sag, math.radians(2.5) * math.sin(2 * math.pi * 2.2 * max(0, t - W("şaka"))) * gul)
        u = yumusak((t + PAY) / (SURE + 2 * PAY))
        kamera_yerle(k, cd, od, K0.lerp(K1, u), H, 36, bas_bebek.lerp(vf.bas(P + "Head"), 0.4))
    return kare, (k, cd, od), [vf, tf], [(sk, "value")]


PLAN_FN = {"A01": plan_A01, "G02": plan_G02}


# ================================================================ çalıştırma
def hazirla():
    r = PLAN_FN[PLAN]()
    kare_fn, kam, figurler = r[0], r[1], r[2]
    ekler = r[3] if len(r) > 3 else []
    n = int(round((SURE + 2 * PAY) * FPS)) + 1
    sc = bpy.context.scene
    sc.render.fps = FPS
    sc.frame_start, sc.frame_end = 1, n
    for i in range(n):
        t = -PAY + i / FPS
        kare_fn(t)
        for f in figurler:
            f.anahtarla(i + 1)
        kamera_anahtar(*kam, i + 1)
        for nesne, ozellik in ekler:
            nesne.keyframe_insert(ozellik, frame=i + 1)
    return n, kam


def main():
    t0 = time.time()
    n, kam = hazirla()
    print("HAZIR %s: %d kare, %.1f sn" % (PLAN, n, time.time() - t0))
    sc = bpy.context.scene
    sc.cycles.samples = ORNEK
    kok = os.path.join(BURA, "plaka", PLAN)
    tmp = os.path.join(kok, "_maske_tmp")
    os.makedirs(tmp, exist_ok=True)
    fo = O.maske_kur(tmp)

    def tek(i, yol):
        fo.file_name = "%04d_" % i
        sc.frame_set(i + 1)
        sc.render.filepath = yol
        s = time.time()
        bpy.ops.render.render(write_still=True)
        return time.time() - s

    if MOD in ("olc", "kare"):
        tt = float(arg("t", str(SURE / 2)))
        i = int(round((tt + PAY) * FPS))
        s = tek(i, os.path.join(kok, "deneme.png"))
        print("OLC %s kare %d (t=%.2f): %.1f sn, %d örnek" % (PLAN, i, tt, s, ORNEK))
        return
    os.makedirs(os.path.join(kok, "rgb"), exist_ok=True)
    os.makedirs(os.path.join(kok, "maske"), exist_ok=True)
    bas_i = int(arg("bas", "0")); son_i = int(arg("son", str(n - 1)))
    sureler = []
    for i in range(bas_i, son_i + 1):
        s = tek(i, os.path.join(kok, "rgb", "%04d.png" % i))
        for f in os.listdir(tmp):
            if f.startswith("%04d_" % i):
                shutil.move(os.path.join(tmp, f), os.path.join(kok, "maske", "%04d.png" % i))
        sureler.append(s)
        print("KARE %s %d/%d %.1f sn" % (PLAN, i, n - 1, s), flush=True)
    k, cd, od = kam
    bilgi_yol = os.path.join(kok, "bilgi.json")
    bilgi = json.load(open(bilgi_yol, encoding="utf-8")) if os.path.exists(bilgi_yol) else {}
    sl = bilgi.get("kare_sureleri", {})
    for i, s in zip(range(bas_i, son_i + 1), sureler):
        sl[str(i)] = round(s, 2)
    sc.frame_set(1)
    bilgi.update({
        "plan": PLAN, "fps": FPS, "kare_sayisi": n, "pay_sn": PAY, "sure_sn": SURE,
        "ilk_kare_zamani_sn": -PAY, "baslangic_sn_filmde": PL.get("baslangic_sn"),
        "cozunurluk": [1920, 1080], "ornek": ORNEK,
        "kamera": {"lens_mm_bas": cd.lens, "sensor_mm": cd.sensor_width, "konum_bas": list(k.location)},
        "kare_sureleri": sl, "ort_kare_sn": round(sum(sl.values()) / max(1, len(sl)), 2),
        "maske": "beyaz = şövaledeki tablo, duvara dayalı Vincent tuvallerinin yüzü, sarı zarflar (nesne indeksi 1)",
    })
    json.dump(bilgi, open(bilgi_yol, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("BİTTİ", PLAN)


main()
