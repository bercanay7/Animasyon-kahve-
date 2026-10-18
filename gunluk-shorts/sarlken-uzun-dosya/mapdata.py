"""Harita verisi: Natural Earth 50m (kamu malı; npm `world-atlas`) → Mercator dünya pikseli; ~1520–1556 tarihsel bölgeler (YAKLAŞIK).

Tarihsel sınırlar modern ülke çokgenlerinin birleşimi/kesişimi ve elle çizilmiş kutu/çokgenlerle kurulur; kesin sınır iddiası yoktur
(videoda haritalarda "yaklaşık sınırlar" notu bulunur). Sonuç `out/_cache/mapdata_v1.pkl` içinde önbelleğe alınır (git'e girmez).

Dünya pikseli: zoom=1'de 1 derece boylam = PPD0 piksel; (LON0, LAT0) ekran merkezi (W/2, H/2)."""
import json
import math
import os
import pickle

import numpy as np
import shapely
from shapely.geometry import MultiPolygon, Polygon, box
from shapely.ops import unary_union

from engine import H, W

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "out", "_cache", "mapdata_v2.pkl")
PPD0 = 32.0
LON0, LAT0 = 15.0, 46.0
LEVELS = [0.25, 0.5, 1.0, 2.0, 4.0]       # zoom düzeyleri (sadeleştirme)
TOL = 0.75                                  # dünya pikseli / zoom


def mer_y(lat):
    return math.degrees(math.log(math.tan(math.pi / 4 + math.radians(lat) / 2)))


Y0 = mer_y(LAT0)


def to_world(lon, lat):
    return (W / 2 + (lon - LON0) * PPD0, H / 2 - (mer_y(lat) - Y0) * PPD0)


def to_world_np(a):
    a = np.asarray(a, dtype=np.float64)
    lat = np.clip(a[..., 1], -85, 85)
    y = np.degrees(np.log(np.tan(np.pi / 4 + np.radians(lat) / 2)))
    return np.stack([W / 2 + (a[..., 0] - LON0) * PPD0, H / 2 - (y - Y0) * PPD0], axis=-1)


def from_world(x, y):
    lon = LON0 + (x - W / 2) / PPD0
    yy = Y0 - (y - H / 2) / PPD0
    lat = math.degrees(2 * math.atan(math.exp(math.radians(yy))) - math.pi / 2)
    return lon, lat


# ───────────────────────── TopoJSON ─────────────────────────
def _decode_topo(path):
    d = json.load(open(path, encoding="utf-8"))
    sx, sy = d["transform"]["scale"]
    tx, ty = d["transform"]["translate"]
    arcs = []
    for a in d["arcs"]:
        x = y = 0
        pts = []
        for dx, dy in a:
            x += dx
            y += dy
            pts.append((x * sx + tx, y * sy + ty))
        arcs.append(pts)

    def ring(idxs):
        pts = []
        for i in idxs:
            seg = arcs[i] if i >= 0 else arcs[~i][::-1]
            pts.extend(seg if not pts else seg[1:])
        return pts

    def geom(g):
        if g["type"] == "Polygon":
            return Polygon(ring(g["arcs"][0]), [ring(r) for r in g["arcs"][1:]]).buffer(0)
        polys = [Polygon(ring(p[0]), [ring(r) for r in p[1:]]) for p in g["arcs"]]
        return MultiPolygon(polys).buffer(0)

    out = {}
    for g in d["objects"]["countries"]["geometries"]:
        out[g["properties"]["name"]] = geom(g)
    return out


def _countries():
    """Ülke çokgenleri; Antarktika atılır, tarih değiştirme çizgisi yakını kırpılır (birleşimde dünyayı saran halkayı önler)."""
    C = _decode_topo(os.path.join(HERE, "data", "countries-50m.json"))
    cb = box(-179.0, -58.0, 179.0, 84.0)
    out = {}
    for k, g in C.items():
        if k == "Antarctica":
            continue
        gg = g.intersection(cb)
        if not gg.is_empty:
            out[k] = gg
    return out


# ───────────────────────── tarihsel bölgeler (lon/lat) ─────────────────────────
def build_regions():
    C = _countries()

    def c(*names):
        return unary_union([C[n] for n in names])

    def P(pts):
        return Polygon(pts).buffer(0)

    def clip(g, poly):
        return g.intersection(poly)

    R = {}
    # ── İspanya Tacı (Kastilya + Aragon) ──
    spain = C["Spain"]
    R["ispanya"] = clip(spain, box(-19, 26, 5, 45))
    # ── İtalya'daki Habsburg/İspanyol mülkleri ──
    italy = C["Italy"]
    south = P([(12.4, 40.9), (13.3, 41.4), (14.0, 42.4), (14.9, 43.0), (19, 43.0), (19, 35.5), (12.4, 35.5)])
    sardinia = box(8.0, 38.8, 9.95, 41.4)
    sicily = box(12.3, 36.5, 15.8, 38.4)
    R["napoli"] = unary_union([clip(italy, south), clip(italy, sardinia)])
    R["sicilya"] = clip(italy, sicily)
    R["napoli_kara"] = clip(italy, south).difference(sicily)
    R["sardunya"] = clip(italy, sardinia)
    R["milano"] = clip(italy, P([(8.4, 44.8), (10.9, 44.85), (10.8, 46.0), (9.3, 46.6), (8.4, 45.9)]))
    R["papalik"] = clip(italy, P([(11.2, 41.35), (12.5, 41.5), (13.55, 42.3), (13.7, 43.6), (12.6, 44.45), (12.3, 45.0), (11.0, 44.8), (10.55, 44.1), (11.0, 43.2)]))
    # ── Venedik ──
    ven_i = clip(italy, P([(11.4, 45.0), (13.8, 45.05), (13.95, 46.2), (12.4, 46.75), (11.6, 46.0)]))
    ven_d = clip(C["Croatia"], P([(13.4, 45.6), (14.6, 45.0), (15.7, 43.9), (16.8, 43.0), (18.3, 42.4), (18.0, 43.4), (16.2, 44.5), (14.2, 45.9)]))
    ven_c = clip(C["Greece"], box(23.4, 34.8, 26.4, 35.7))
    ven_ion = clip(C["Greece"], box(19.3, 36.6, 21.2, 39.9))
    R["venedik"] = unary_union([ven_i, ven_d, ven_c, ven_ion])
    # ── Burgonya Hollandası ──
    flanders = clip(C["France"], P([(1.6, 50.0), (4.3, 49.95), (4.3, 51.3), (1.9, 51.2)]))
    fcomte = clip(C["France"], P([(5.1, 46.4), (6.15, 46.2), (7.15, 47.6), (6.95, 48.0), (5.4, 47.95), (5.0, 47.0)]))
    R["hollanda"] = unary_union([c("Netherlands", "Belgium", "Luxembourg"), flanders, fcomte])
    R["franche_comte"] = fcomte
    # ── Savoy (1536'ya kadar bağımsız dukalık) ──
    savoy_f = clip(C["France"], P([(5.7, 45.0), (7.2, 45.1), (7.05, 46.4), (5.85, 46.2)]))
    savoy_i = clip(italy, P([(6.6, 44.1), (8.2, 44.1), (8.4, 45.4), (7.9, 45.95), (6.9, 45.9)]))
    R["savoya"] = unary_union([savoy_f, savoy_i])
    # ── Fransa (Hollanda/Franche-Comté/Savoy çıkarılmış) ──
    R["fransa"] = C["France"].difference(unary_union([flanders, fcomte, savoy_f]))
    # ── Avusturya mirası, Bohemya, Macaristan ──
    tyrol = clip(italy, P([(10.4, 45.7), (12.45, 46.6), (12.3, 47.1), (10.2, 47.0)]))
    friuli = clip(italy, box(13.1, 45.55, 13.95, 46.6))
    istria = clip(C["Croatia"], box(13.3, 44.7, 14.6, 45.6))
    R["avusturya"] = unary_union([C["Austria"], C["Slovenia"], tyrol, friuli, istria])
    R["bohemya"] = C["Czechia"]
    hun_w = clip(C["Hungary"], P([(15.5, 45.5), (19.0, 45.9), (19.4, 47.6), (19.6, 48.7), (15.5, 48.7)]))
    hun_cro = clip(C["Croatia"], box(14.5, 45.4, 17.5, 46.6))
    R["macar_habsburg"] = unary_union([C["Slovakia"], hun_w, hun_cro])
    R["macar_osmanli"] = C["Hungary"].difference(hun_w)
    R["erdel"] = clip(C["Romania"], P([(21.0, 45.2), (26.8, 45.2), (27.0, 47.6), (22.8, 48.1), (21.0, 46.4)]))
    # ── Alman prensleri (şematik: Almanya + İsviçre kuzeyi + Hollanda'yı hariç tutar) ──
    R["almanya"] = clip(C["Germany"], box(5, 46, 15.2, 56))
    R["isvicre"] = C["Switzerland"]
    # ── İngiltere / İskoçya / İrlanda ──
    R["britanya"] = C["United Kingdom"]
    R["irlanda"] = C["Ireland"]
    # ── Portekiz ──
    R["portekiz"] = C["Portugal"]
    # ── Osmanlı (c.1520) ve (c.1550) ──
    rhodes = box(27.0, 35.8, 28.3, 36.5)
    greece = C["Greece"]
    ott_greece = greece.difference(unary_union([ven_c, ven_ion]))
    ott20 = unary_union([
        C["Turkey"], ott_greece, c("Bulgaria", "Serbia", "Kosovo", "Macedonia", "Albania", "Montenegro", "Bosnia and Herz."),
        c("Syria", "Lebanon", "Israel", "Palestine", "Jordan", "Egypt"),
        clip(C["Saudi Arabia"], P([(34.5, 29.5), (36.5, 27.0), (38.0, 24.0), (39.5, 21.5), (41.0, 18.5), (42.8, 16.4), (43.5, 17.5), (42.5, 21.0), (41.0, 24.5), (38.8, 27.5), (37.0, 29.2)])),
    ]).difference(rhodes)
    R["osmanli_1520"] = ott20
    ott50 = unary_union([ott20, rhodes, R["macar_osmanli"], C["Iraq"],
                         clip(C["Algeria"], P([(-1.5, 35.0), (8.5, 36.9), (8.6, 35.5), (3.0, 34.0), (-1.5, 34.5)])),
                         clip(C["Libya"], box(10.0, 31.0, 20.0, 33.5)), clip(C["Yemen"], box(42.0, 12.5, 45.5, 17.0))])
    R["osmanli_1550"] = ott50
    R["osmanli_vassal"] = unary_union([C["Romania"].difference(R["erdel"]), C["Moldova"], clip(C["Ukraine"], box(28, 44, 36.7, 46.6))])
    # ── Kuzey Afrika ──
    R["fas"] = C["Morocco"]
    R["cezayir"] = C["Algeria"]
    R["tunus"] = C["Tunisia"]
    R["trablus"] = C["Libya"]
    R["misir"] = C["Egypt"]
    # ── Yeni Dünya ──
    mex = C["Mexico"]
    R["aztek"] = clip(mex, P([(-103.5, 17.3), (-97.0, 16.4), (-94.0, 17.6), (-95.5, 20.6), (-98.5, 22.3), (-101.5, 21.5), (-104.0, 19.5)]))
    R["yeni_ispanya"] = unary_union([mex, c("Guatemala", "Honduras", "El Salvador", "Nicaragua", "Costa Rica", "Panama", "Belize"),
                                     c("Cuba", "Dominican Rep.", "Haiti", "Puerto Rico", "Jamaica")])
    inca = unary_union([c("Peru", "Ecuador"), clip(C["Bolivia"], box(-70, -23, -64, -9)), clip(C["Chile"], box(-72, -35, -66, -17.5)),
                        clip(C["Argentina"], box(-69, -35, -64.5, -22)), clip(C["Colombia"], box(-79.5, -1.5, -74, 2.0))])
    R["inka"] = inca
    R["peru_ispanya"] = unary_union([inca, c("Colombia", "Venezuela"), clip(C["Chile"], box(-76, -41, -66, -17.5)), c("Paraguay")])
    R["brezilya"] = C["Brazil"]
    # ── Habsburg bütünü ──
    R["karl_kendi"] = unary_union([R["ispanya"], R["napoli"], R["milano"], R["hollanda"], R["yeni_ispanya"], R["peru_ispanya"]])
    R["ferdinand"] = unary_union([R["avusturya"], R["bohemya"], R["macar_habsburg"]])
    # ── zeminler ──
    R["__kara__"] = unary_union(list(C.values()))
    return R


# ───────────────────────── dünya pikseline çevir + sadeleştir ─────────────────────────
def _project(g):
    return shapely.transform(g, lambda a: to_world_np(a))


def _rings(g):
    """shapely → [(dış halka ndarray float32, [delik halkaları]), ...]"""
    out = []
    if g.is_empty:
        return out
    geoms = [g] if g.geom_type == "Polygon" else list(getattr(g, "geoms", []))
    for p in geoms:
        if p.geom_type == "Polygon" and not p.is_empty:
            out.append((np.asarray(p.exterior.coords, dtype=np.float32), [np.asarray(h.coords, dtype=np.float32) for h in p.interiors]))
        elif p.geom_type == "MultiPolygon":
            out.extend(_rings(p))
    return out


def _levels(gw):
    res = {}
    for z in LEVELS:
        s = shapely.simplify(gw, TOL / z, preserve_topology=True)
        res[z] = _rings(s)
    return res


def mountain_ranges():
    """Dağ dizileri (lon,lat çizgileri; yaklaşık)."""
    return {
        "alpler": [(6.6, 44.3), (7.0, 45.5), (8.2, 46.0), (9.6, 46.4), (11.3, 46.6), (13.0, 46.6), (14.5, 46.5), (16.0, 47.0)],
        "pireneler": [(-1.8, 43.2), (-0.3, 42.8), (1.0, 42.7), (2.4, 42.5), (3.2, 42.4)],
        "apenin": [(8.9, 44.4), (10.5, 44.1), (11.8, 43.6), (13.2, 42.4), (14.3, 41.6), (15.6, 40.4), (16.1, 39.3), (16.0, 38.2)],
        "karpatlar": [(17.5, 49.3), (19.5, 49.4), (21.5, 49.2), (23.3, 48.4), (24.8, 47.6), (25.6, 46.5), (25.9, 45.6), (24.3, 45.4), (22.5, 45.2)],
        "dinar": [(14.5, 45.6), (15.8, 44.5), (17.4, 43.4), (18.8, 42.6), (20.0, 41.5), (20.8, 40.2), (21.3, 39.3)],
        "balkan": [(22.8, 43.2), (24.8, 42.8), (26.5, 42.8), (28.0, 42.8)],
        "rodop": [(23.3, 41.8), (25.0, 41.6), (26.3, 41.4)],
        "toros": [(29.5, 37.0), (31.5, 36.9), (33.5, 36.9), (35.5, 37.3), (37.2, 37.6), (39.5, 38.0)],
        "kuzey_anadolu": [(30.5, 40.7), (33.0, 41.0), (36.0, 40.8), (39.5, 40.6), (41.5, 40.7)],
        "kafkas": [(38.0, 44.3), (40.5, 43.6), (43.0, 42.8), (45.5, 42.4), (47.5, 41.8)],
        "atlas": [(-9.5, 31.0), (-6.5, 31.8), (-3.5, 32.8), (0.0, 34.0), (3.5, 35.6), (6.5, 35.8), (9.0, 36.3), (10.5, 36.3)],
        "sierra_nevada": [(-5.8, 37.3), (-4.2, 37.0), (-2.6, 37.1)],
        "iberik": [(-5.5, 41.5), (-3.5, 41.2), (-1.7, 40.7), (-0.5, 40.4)],
        "kantabri": [(-8.0, 43.0), (-5.5, 43.0), (-3.5, 43.1)],
        "vosges_jura": [(5.8, 46.3), (6.6, 47.0), (7.1, 47.7), (7.3, 48.3)],
        "bohemya_orman": [(12.2, 49.3), (13.4, 49.0), (14.3, 48.8)],
        "sudetler": [(14.8, 50.8), (16.0, 50.7), (17.2, 50.3)],
        "andes": [(-76.5, 8.5), (-75.5, 3.5), (-78.0, -1.0), (-79.0, -6.0), (-76.0, -12.0), (-72.0, -16.0), (-69.5, -20.0), (-69.5, -26.0), (-70.0, -33.0), (-71.5, -41.0)],
        "sierra_madre": [(-107.5, 27.0), (-105.0, 22.5), (-102.5, 19.5), (-99.0, 18.3), (-96.5, 17.2)],
        "sierra_madre_or": [(-100.5, 27.5), (-99.0, 24.5), (-98.5, 20.5)],
        "cuba_sierra": [(-77.0, 20.1), (-76.0, 20.0)],
    }


def build():
    R = build_regions()
    out = {"regions": {}, "mount": {}, "ripples": None}
    for k, g in R.items():
        gw = _project(g)
        out["regions"][k] = _levels(gw)
    land_w = shapely.simplify(_project(R["__kara__"]), 0.5, preserve_topology=True)
    ripples = []
    for d in (7.0, 15.0, 26.0):
        b = land_w.buffer(d, resolution=3)
        geoms = [b] if b.geom_type == "Polygon" else list(b.geoms)
        rings = []
        for p in geoms:
            rings.append(np.asarray(p.exterior.coords, dtype=np.float32))
            for h in p.interiors:
                rings.append(np.asarray(h.coords, dtype=np.float32))
        ripples.append((d, rings))
    out["ripples"] = ripples
    rs = np.random.RandomState(4)
    glyphs = []
    for name, pts in mountain_ranges().items():
        wpts = to_world_np(np.array(pts))
        for a, b in zip(wpts[:-1], wpts[1:]):
            L = float(np.hypot(*(b - a)))
            n = max(1, int(L / 11.0))
            for i in range(n):
                u = (i + rs.rand() * 0.8) / n
                p = a + (b - a) * u
                p = p + rs.randn(2) * 4.0
                glyphs.append((float(p[0]), float(p[1]), 4.5 + 5.5 * rs.rand(), int(rs.randint(0, 10_000))))
    out["mount"] = np.array(glyphs, dtype=np.float32)
    os.makedirs(os.path.dirname(CACHE), exist_ok=True)
    pickle.dump(out, open(CACHE, "wb"), protocol=4)
    return out


_DATA = None


def data():
    global _DATA
    if _DATA is None:
        if os.path.exists(CACHE):
            _DATA = pickle.load(open(CACHE, "rb"))
        else:
            _DATA = build()
    return _DATA


if __name__ == "__main__":
    import time
    t0 = time.time()
    d = build()
    print("harita verisi hazır:", round(time.time() - t0, 1), "sn;", len(d["regions"]), "bölge; dağ simgesi:", len(d["mount"]))
    for k in ("__kara__", "ispanya", "osmanli_1520", "hollanda", "karl_kendi"):
        print(k, {z: len(v) for z, v in d["regions"][k].items()}, "toplam köşe(z=1):", sum(len(r[0]) for r in d["regions"][k][1.0]))
    print("ripple:", [(dd, len(r), sum(len(x) for x in r)) for dd, r in d["ripples"]])
