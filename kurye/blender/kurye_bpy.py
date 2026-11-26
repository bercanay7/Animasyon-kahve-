"""Mektuplar: kurye Blender'da (bpy 5.x, Cycles, işlemci). Model indirilmez: gövde, iskeletimizin eklemlerinden deri (skin) değiştiricisiyle örülür.
Hareket kurye/tablo.html'deki kuryePoz'dan gelir (eklem_disa.js → eklem.json). Çıktı: saydam zeminli RGBA kare (960×540, sahne kamerasıyla birebir);
tablo.html bu kareyi fırça darbelerine çevirir (görüntü yine boyalı kalır).
    python kurye/blender/kurye_bpy.py [çıktı klasörü] [ilk:son]      (bpy modülü kurulu Python ile)
Eksen: bizim dünya (x sağ, y yukarı, z kameraya doğru) → Blender (x, -z, y).
"""
import bpy, json, math, sys, time
from pathlib import Path
from mathutils import Vector, Matrix
from bpy_extras.object_utils import world_to_camera_view

HERE = Path(__file__).resolve().parent
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / 'kare'
OUT.mkdir(parents=True, exist_ok=True)
D = json.loads((HERE / 'eklem.json').read_text())
if len(sys.argv) > 2: a, b = map(int, sys.argv[2].split(':')); D = D[a:b]

B = lambda p: Vector((p[0], -p[2], p[1]))
def cer(c): return B(c['o']), B(c['x']), B(c['y']), B(c['z'])

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = 12; sc.cycles.use_denoising = True
sc.render.resolution_x, sc.render.resolution_y = 960, 540; sc.render.film_transparent = True
sc.render.image_settings.file_format = 'PNG'; sc.render.image_settings.color_mode = 'RGBA'
sc.view_settings.view_transform = 'Standard'
# kamera: konum [0, 1.6, 0], ufuk y = 700 (kamera 6.15° yukarı), dikey görüş 40°
cam = bpy.data.objects.new('kamera', bpy.data.cameras.new('kamera')); sc.collection.objects.link(cam); sc.camera = cam
EGIM = math.atan((700 - 540) / (540 / math.tan(math.radians(20))))
cam.location = (0, 0, 1.6); cam.rotation_euler = (math.pi / 2 + EGIM, 0, 0)   # ufuk ortanın altında: kamera hafif yukarı bakar
cam.data.sensor_fit = 'VERTICAL'; cam.data.angle_y = math.radians(40); cam.data.clip_start = .1
# güneş: karşıdan, çok alçak (sahnedeki GUNES_IS [4, 5.2, -100]); gök: mor ortam ışığı
sun = bpy.data.objects.new('gunes', bpy.data.lights.new('gunes', 'SUN')); sc.collection.objects.link(sun)
d = Vector((4, 100, 5.2)).normalized(); sun.rotation_euler = (-d).to_track_quat('-Z', 'Y').to_euler()
sun.data.energy = 5.0; sun.data.color = (1, .68, .42); sun.data.angle = math.radians(1.5)
w = bpy.data.worlds.new('gok'); sc.world = w; w.use_nodes = True
bg = w.node_tree.nodes['Background']; bg.inputs[0].default_value = (.3, .2, .38, 1); bg.inputs[1].default_value = .22
# yerden sıcak sekme: kuryenin altında görünmez, ışık veren düzlem (tarlanın altın yansıması)
bpy.ops.mesh.primitive_plane_add(size=6); yer = bpy.context.object; yer.visible_camera = False
my = bpy.data.materials.new('yer'); my.use_nodes = True; my.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = (.5, .32, .16, 1); yer.data.materials.append(my)

def mat(ad, renk, pr=.8, sheen=0.0):
    m = bpy.data.materials.new(ad); m.use_nodes = True; n = m.node_tree.nodes['Principled BSDF']
    n.inputs['Base Color'].default_value = (*renk, 1); n.inputs['Roughness'].default_value = pr
    if sheen: n.inputs['Sheen Weight'].default_value = sheen
    return m
M = {'palto': mat('palto', (.3, .2, .14), .85, .4), 'pantolon': mat('pantolon', (.15, .12, .14), .8, .3), 'ten': mat('ten', (.5, .36, .3), .6),
     'sapka': mat('sapka', (.22, .16, .12), .7, .3), 'canta': mat('canta', (.34, .2, .14), .55), 'kayis': mat('kayis', (.2, .12, .1), .6)}

def deri(ad, noktalar, kenarlar, yaricap, malz, kok=0, sub=2):
    me = bpy.data.meshes.new(ad); me.from_pydata([tuple(p) for p in noktalar], kenarlar, []); ob = bpy.data.objects.new(ad, me); sc.collection.objects.link(ob)
    md = ob.modifiers.new('deri', 'SKIN'); md.use_smooth_shade = True; md.branch_smoothing = .6
    sv = me.skin_vertices[''].data
    for i, r in enumerate(yaricap): sv[i].radius = r if isinstance(r, tuple) else (r, r)
    sv[kok].use_root = True
    ob.modifiers.new('yumusat', 'SUBSURF').levels = sub; ob.modifiers['yumusat'].render_levels = sub
    me.materials.append(malz); return ob

def kutu(ad, mrk, x, y, z, s, malz):
    me = bpy.data.meshes.new(ad); ob = bpy.data.objects.new(ad, me); sc.collection.objects.link(ob)
    import bmesh; bm = bmesh.new(); bmesh.ops.create_cube(bm, size=1); bm.to_mesh(me); bm.free()
    ob.matrix_world = Matrix(((x[0] * s[0], y[0] * s[1], z[0] * s[2], mrk[0]), (x[1] * s[0], y[1] * s[1], z[1] * s[2], mrk[1]), (x[2] * s[0], y[2] * s[1], z[2] * s[2], mrk[2]), (0, 0, 0, 1)))
    bev = ob.modifiers.new('pah', 'BEVEL'); bev.width = .012; bev.segments = 2
    me.materials.append(malz); return ob

def silindir(ad, mrk, x, y, z, r, h, malz, uz=1.0, ust=1.0, bukum=0.0):
    if ust != 1.0: bpy.ops.mesh.primitive_cone_add(vertices=40, radius1=1, radius2=ust, depth=1)
    else: bpy.ops.mesh.primitive_cylinder_add(vertices=40, radius=1, depth=1)
    ob = bpy.context.object; ob.name = ad
    if bukum:   # kenar önde ve arkada aşağı kıvrılır (yerel y ekseni = başın z'si: ön-arka)
        for v in ob.data.vertices: v.co.z -= bukum / max(h, 1e-3) * (v.co.y ** 2) * (v.co.x ** 2 + v.co.y ** 2) ** .5
    # silindirin ekseni yerel Z: başın y eksenine; x ve z başın x ve z'sine
    ob.matrix_world = Matrix(((x[0] * r, z[0] * r * uz, y[0] * h, mrk[0]), (x[1] * r, z[1] * r * uz, y[1] * h, mrk[1]), (x[2] * r, z[2] * r * uz, y[2] * h, mrk[2]), (0, 0, 0, 1)))
    bev = ob.modifiers.new('pah', 'BEVEL'); bev.width = .006; bev.segments = 2
    ob.data.materials.append(malz); bpy.ops.object.shade_smooth(); return ob

def kurye(k):
    po, px, py, pz = cer(k['pelvis']); go, gx, gy, gz = cer(k['gogus']); bo, bx, by, bz = cer(k['boyun']); ho, hx, hy, hz = cer(k['bas'])
    L = []
    # gövde ve baş
    P = [po, go, go + gy * .2, bo, ho, ho + hy * .072 + hz * .028, ho + hy * .165]
    R = [(.15, .1), (.15, .1), (.17, .105), .055, .06, (.085, .1), .05]
    E = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6)]
    # bacaklar
    for b in k['bacak']:
        ka, di, bi = B(b['kalca']), B(b['diz']), B(b['bilek']); ao, ax, ay, az = cer(b['ayak'])
        i = len(P); P += [ka, di, bi, bi + az * .16 - ay * .05]; R += [.085, .06, .045, (.045, .03)]
        E += [(0, i), (i, i + 1), (i + 1, i + 2), (i + 2, i + 3)]
    # kollar
    for c in k['kol']:
        om, de, bl = B(c['omuz']), B(c['dirsek']), B(c['bilek']); uc = bl + (bl - de).normalized() * .15
        i = len(P); P += [om, de, bl, uc]; R += [.06, .046, .036, (.035, .02)]
        E += [(2, i), (i, i + 1), (i + 1, i + 2), (i + 2, i + 3)]
    L.append(deri('beden', P, E, R, M['pantolon']))
    # palto: halkalardan örülmüş A-kesim; yaka, omuz, göğüs, bel, kalça, etek (etek açık, kenarı düz kesik)
    def halka(mrk, ex, ez, rx, rz, n=28, egik=0.0):
        return [mrk + ex * (rx * math.cos(2 * math.pi * i / n)) + ez * (rz * math.sin(2 * math.pi * i / n)) - (ex.cross(ez)).normalized() * 0 for i in range(n)]
    # düz kesim sivil palto: yaka (dik, boynu saran), yuvarlak omuz, düz gövde, etek az açılır (A-kesim elbise okunuyordu)
    HR = [(bo + by * .05, gx, gz, .085, .08), (bo - by * .01, gx, gz, .1, .09), (go + gy * .19, gx, gz, .19, .12), (go + gy * .06, gx, gz, .18, .118),
          (po + py * .06, px, pz, .175, .125), (po - py * .16, px, pz, .19, .14), (po - py * .3, px, pz, .195, .145), (po - py * .4, px, pz, .2, .15)]
    V_, F_ = [], []
    for j, (m, ex, ez, rx, rz) in enumerate(HR):
        V_ += halka(m, ex, ez, rx, rz)
        if j: F_ += [((j - 1) * 28 + i, (j - 1) * 28 + (i + 1) % 28, j * 28 + (i + 1) % 28, j * 28 + i) for i in range(28)]
    me = bpy.data.meshes.new('palto'); me.from_pydata([tuple(v) for v in V_], [], F_); ob = bpy.data.objects.new('palto', me); sc.collection.objects.link(ob)
    ob.modifiers.new('kalin', 'SOLIDIFY').thickness = .012
    sb = ob.modifiers.new('yumusat', 'SUBSURF'); sb.levels = sb.render_levels = 2
    for pl in me.polygons: pl.use_smooth = True
    me.materials.append(M['palto']); L.append(ob)
    for c in k['kol']:
        om, de, bl = B(c['omuz']), B(c['dirsek']), B(c['bilek']); uc = bl + (bl - de).normalized() * .15
        i = len(P); P += [om, de, bl, uc]; R += [.06, .046, .036, (.035, .02)]
        E += [(2, i), (i, i + 1), (i + 1, i + 2), (i + 2, i + 3)]
    L.append(deri('beden', P, E, R, M['pantolon']))
    # palto: boyundan dizin üstüne genişleyen etek (kollar paltonun kolları gibi aynı renkte ayrı)
    PP = [bo, go + gy * .2, go, po + py * .05, po - py * .22, po - py * .4]
    PR = [.07, (.19, .12), (.175, .115), (.18, .13), (.21, .16), (.24, .18)]
    L.append(deri('palto', PP, [(i, i + 1) for i in range(5)], PR, M['palto']))
    for c in k['kol']:
        om, de, bl = B(c['omuz']), B(c['dirsek']), B(c['bilek'])
        om2 = om - gy * .07 + (go + gy * .2 - om) * .3          # kol paltonun içinden başlar (omuzda apolet gibi çıkıntı olmasın)
        L.append(deri('kol', [om2, de, bl], [(0, 1), (1, 2)], [.055, .05, .044], M['palto']))
        uc = bl + (bl - de).normalized() * .12
        L.append(deri('el', [bl, uc], [(0, 1)], [.032, (.03, .018)], M['ten'], sub=1))
    # baş ve boyun teni
    L.append(deri('bas', [bo, ho, ho + hy * .072 + hz * .028, ho + hy * .15], [(0, 1), (1, 2), (2, 3)], [.062, .062, (.082, .095), .06], M['ten']))
    # şapka: tepe ve kenar
    so = ho + hy * .155 + hz * .02
    # fötr: tepesi daralan, kenarı kısa, yuvarlak ve simetrik (düz tepe + geniş kenar din adamı; kıvrık uç süvari ya da asker okunur)
    L.append(silindir('tepe', so + hy * .05, hx, hy, hz, .096, .095, M['sapka'], 1.05, ust=.86))
    L.append(silindir('kenar', so + hy * .004, hx, hy, hz, .145, .014, M['sapka'], 1.0))
    # çanta ve kayış
    ck, ca = B(k['canta']['kok']), B(k['canta']['asagi']); cy = -ca; cz = px.cross(cy).normalized()
    L.append(kutu('canta', ck + ca * .15, px, cy, cz, (.08, .22, .28), M['canta']))
    om = B(k['kol'][0]['omuz']); a1 = om - gz * .01; uz = ck - a1; Lk = uz.length; yy = uz / Lk; xx = yy.cross(gz).normalized()
    L.append(kutu('kayis', (a1 + ck) / 2, xx, yy, gz, (.035, Lk, .2), M['kayis']))
    return L, P

for k in D:
    L, P = kurye(k)
    # kenar kutusu: kuryenin ekran izdüşümü (+pay); yalnız o bölge çizilir
    xs, ys = [], []
    for p in P + [p + Vector((0, 0, .25)) for p in P]:
        v = world_to_camera_view(sc, cam, p); xs.append(v.x); ys.append(v.y)
    fp = OUT / f"k_{round(k['t'] * 15):04d}.png"
    if max(xs) < -.01 or min(xs) > 1.01 or max(ys) < -.01 or min(ys) > 1.01 or min(1, max(xs) + .03) - max(0, min(xs) - .03) < .012:
        # kurye kadrajın dışında: boş saydam kare
        im = bpy.data.images.new('bos', 960, 540, alpha=True); im.pixels = [0.0] * (960 * 540 * 4); im.filepath_raw = str(fp); im.file_format = 'PNG'; im.save()
        bpy.data.images.remove(im); print(f"t={k['t']:.3f}  boş", flush=True)
        for ob in L: bpy.data.objects.remove(ob, do_unlink=True)
        continue
    sc.render.use_border = True; sc.render.use_crop_to_border = False
    sc.render.border_min_x, sc.render.border_max_x = max(0, min(xs) - .03), min(1, max(xs) + .03)
    sc.render.border_min_y, sc.render.border_max_y = max(0, min(ys) - .03), min(1, max(ys) + .03)
    sc.render.filepath = str(fp)
    t0 = time.time(); bpy.ops.render.render(write_still=True)
    print(f"t={k['t']:.3f}  {time.time() - t0:.1f} sn", flush=True)
    for ob in L: bpy.data.objects.remove(ob, do_unlink=True)
