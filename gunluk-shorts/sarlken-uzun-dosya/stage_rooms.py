"""Oda laboratuvarı ilkelleri (oda-lab): perspektifli "kutu oda" + numpy ile gerçek ışıklandırma (nokta ışık, ay ışığı gobo'su,
kabartma/bump), prosedürel malzemeler (taş, tahta, kerpiç), mum/meşale, toz, demir parmaklık, ışık huzmeleri ve kendi siluet figürleri.

HEPSİ `layers()` (pişirme) içindir; yalnız `flame/motes/fig` dyn içinde ucuzdur. Ortak dosyalara dokunulmaz.
Koordinatlar: katman tuvali (-220..2140, -220..1300); `Box` tek noktalı perspektif: arka duvar dikdörtgeni + kaçış noktası.
"""
import math
from functools import lru_cache

import cv2
import numpy as np
import skia

import sk
import stage as ST
from sk import C, H, W, clamp, lerp, mix, rgb, smooth
from stage import MARGIN

M = MARGIN
CW, CH = W + 2 * M, H + 2 * M          # katman tuvali (2360 × 1520)


# ───────────────────────────── küçük yardımcılar ─────────────────────────────
def hex3(c):
    r, g, b = rgb(c)
    return np.array([r, g, b], np.float32) / 255.0


def shade(col, k):
    """k>0 beyaza, k<0 siyaha doğru karıştır."""
    return mix(col, "#FFFFFF", k) if k > 0 else mix(col, "#000000", -k)


def hash2(i, j, seed=0):
    """Tamsayı dizilerinden [0,1) float32 rastgele (deterministik)."""
    h = (np.asarray(i, np.int64) * 374761393 + np.asarray(j, np.int64) * 668265263 + int(seed) * 2147483647 + 1013904223) & 0xFFFFFFFF
    h = ((h ^ (h >> 13)) * 1274126177) & 0xFFFFFFFF
    h = h ^ (h >> 16)
    return (h & 0xFFFFFF).astype(np.float32) / float(0x1000000)


def sstep(x, e0, e1):
    t = np.clip((x - e0) / (e1 - e0), 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


@lru_cache(maxsize=8)
def _tile_noise(seed, size=512):
    """Döşenebilir (kesintisiz tekrarlanan) çok oktavlı gürültü, sıfır ortalama / birim varyans."""
    rs = np.random.RandomState(seed)
    out = np.zeros((size, size), np.float32)
    tot = 0.0
    for n, wgt in ((8, 1.0), (16, 0.65), (32, 0.4), (64, 0.25), (128, 0.12)):
        g = rs.rand(n, n).astype(np.float32)
        gp = np.pad(g, 2, mode="wrap")
        s = size // n
        up = cv2.resize(gp, ((n + 4) * s, (n + 4) * s), interpolation=cv2.INTER_CUBIC)
        out += up[2 * s:2 * s + size, 2 * s:2 * s + size] * wgt
        tot += wgt
    out /= tot
    return ((out - out.mean()) / (out.std() + 1e-6)).astype(np.float32)


def noise2d(a, b, fa, fb=None, seed=1):
    """Düzlem koordinatlarında (a,b) perspektif-doğru gürültü örnekle. fa/fb: birim başına tekrar sayısı."""
    fb = fa if fb is None else fb
    tex = _tile_noise(int(seed))
    mx = (np.mod(a * fa, 1.0) * 512.0).astype(np.float32)
    my = (np.mod(b * fb, 1.0) * 512.0).astype(np.float32)
    return cv2.remap(tex, mx, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_WRAP)


# ───────────────────────────── malzemeler (a,b → albedo, yükseklik) ─────────────────────────────
def mat_ashlar(base="#5b4b3d", seed=1, bw=210.0, bh=92.0, tone=0.25, joint=2.8, bevel=9.0, bevh=5.5, rough=1.0, tilt=0.3,
               hue=0.07, rowvar=0.30, colvar=0.40, stain=0.0, mortar="#16100b", moss=0.0):
    """Kesme taş duvar: satır yüksekliği ve blok genişliği değişken (sınır jitter'ı), blok başına ton/eğim, pah, derz, lekeler."""
    col = hex3(base)
    mcol = hex3(mortar)

    def fn(a, b):
        bb = b / bh
        r0 = np.floor(bb)
        jr = lambda q: (hash2(q, q * 0, seed + 21) - 0.5) * rowvar
        r = r0 - (bb < r0 + jr(r0)) + (bb >= r0 + 1 + jr(r0 + 1))
        top = r + jr(r)
        bot = r + 1 + jr(r + 1)
        fv = (bb - top) / np.maximum(bot - top, 0.2)
        hh = (bot - top) * bh
        rr = hash2(r, r * 0, seed)
        bwr = bw * (0.78 + 0.44 * rr)
        off = hash2(r, r * 0 + 1, seed + 3) * bwr
        aa = (a + off) / bwr
        c0 = np.floor(aa)
        jc = lambda q, rw: (hash2(q, rw, seed + 31) - 0.5) * colvar
        c = c0 - (aa < c0 + jc(c0, r)) + (aa >= c0 + 1 + jc(c0 + 1, r))
        left = c + jc(c, r)
        right = c + 1 + jc(c + 1, r)
        fu = (aa - left) / np.maximum(right - left, 0.2)
        wd = (right - left) * bwr
        ed = np.minimum(np.minimum(fu * wd, (1 - fu) * wd), np.minimum(fv * hh, (1 - fv) * hh))
        t = hash2(c, r, seed + 7)
        t2 = hash2(c, r, seed + 11)
        n1 = noise2d(a, b, 1 / 700.0, seed=seed)
        n2 = noise2d(a, b, 1 / 260.0, seed=seed + 1)
        n3 = noise2d(a, b, 1 / 150.0, seed=seed + 2)
        edge = sstep(ed, joint, joint + bevel)
        k = 1 + tone * (t - 0.5) * 2 + 0.08 * n1 + 0.07 * n2 + 0.05 * n3
        alb = col[None, None, :] * k[..., None]
        alb[..., 0] *= 1 + hue * (t2 - 0.5) * 2
        alb[..., 2] *= 1 - hue * (t2 - 0.5) * 2
        if stain:
            st = sstep(noise2d(a, b, 1 / 1800.0, 1 / 2400.0, seed=seed + 4), -0.2, 1.2)
            alb *= (1 - stain * st)[..., None]
        if moss:
            ms = sstep(noise2d(a, b, 1 / 500.0, seed=seed + 5), 0.8, 1.7) * sstep(ed, 0.5, 6)
            alb[..., 1] *= 1 + moss * ms
            alb[..., 0] *= 1 - 0.3 * moss * ms
        mort = sstep(ed, 0.0, joint * 1.3)[..., None]
        alb = alb * mort + mcol[None, None, :] * (1 - mort)
        slx = (hash2(c, r, seed + 13) - 0.5) * 2 * tilt
        sly = (hash2(c, r, seed + 17) - 0.5) * 2 * tilt
        h = edge * bevh + slx * (fu - 0.5) * wd * 0.06 + sly * (fv - 0.5) * hh * 0.06 + rough * (0.9 * n1 + 0.6 * n2 + 0.5 * n3)
        return alb.astype(np.float32), h.astype(np.float32)
    return fn


def mat_inca(base="#6a5d52", seed=3, bh=(46, 92), bw=(90, 240), joint=1.6, bevel=13.0, bevh=8.0, tone=0.16, rough=0.6):
    """İnka taş işçiliği: satır yükseklikleri değişken, sıkı derz, yastık gibi şişkin bloklar."""
    col = hex3(base)
    rs = np.random.RandomState(seed)
    hs = rs.uniform(bh[0], bh[1], 80).astype(np.float32)
    edges = np.concatenate([[-4000.0], -4000.0 + np.cumsum(hs)]).astype(np.float32)

    def fn(a, b):
        ri = np.clip(np.searchsorted(edges, b) - 1, 0, len(hs) - 1)
        y0 = edges[ri]
        hh = hs[ri]
        fv = (b - y0) / hh
        rr = hash2(ri, ri * 0, seed)
        bwr = bw[0] + (bw[1] - bw[0]) * rr
        off = hash2(ri, ri * 0 + 1, seed + 2) * bwr
        aa = (a + off) / bwr
        c = np.floor(aa)
        fu = aa - c
        ed = np.minimum(np.minimum(fu * bwr, (1 - fu) * bwr), np.minimum(fv * hh, (1 - fv) * hh))
        t = hash2(c, ri, seed + 7)
        n1 = noise2d(a, b, 1 / 700.0, seed=seed)
        n2 = noise2d(a, b, 1 / 260.0, seed=seed + 1)
        n3 = noise2d(a, b, 1 / 150.0, seed=seed + 2)
        edge = sstep(ed, joint, joint + bevel)
        pillow = np.sqrt(np.clip(edge, 0, 1))
        k = 1 + tone * (t - 0.5) * 2 + 0.06 * n1 + 0.05 * n2 + 0.03 * n3
        alb = col[None, None, :] * k[..., None]
        alb[..., 0] *= 1 + 0.05 * (t - 0.5)
        mort = sstep(ed, 0.0, joint * 1.6)[..., None]
        alb = alb * (0.28 + 0.72 * mort)
        h = pillow * bevh + rough * (0.8 * n1 + 0.5 * n2 + 0.3 * n3)
        return alb.astype(np.float32), h.astype(np.float32)
    return fn


def mat_planks(base="#4a3422", seed=2, pw=88.0, plen=520.0, gap=2.2, tone=0.2, grain=1.0):
    """Tahta döşeme: tahtalar b ekseni boyunca (derinlik), a ekseni genişlik."""
    col = hex3(base)

    def fn(a, b):
        c = np.floor(a / pw)
        fu = a / pw - c
        off = hash2(c, c * 0, seed) * plen
        bb = (b + off) / plen
        r = np.floor(bb)
        fv = bb - r
        ed = np.minimum(np.minimum(fu * pw, (1 - fu) * pw), np.minimum(fv * plen, (1 - fv) * plen))
        t = hash2(c, r, seed + 3)
        gr = noise2d(a, b, 1 / 120.0, 1 / 900.0, seed=seed + 1)
        gr2 = noise2d(a, b, 1 / 60.0, 1 / 400.0, seed=seed + 2)
        n1 = noise2d(a, b, 1 / 700.0, seed=seed + 4)
        k = 1 + tone * (t - 0.5) * 2 + grain * (0.10 * gr + 0.06 * gr2) + 0.06 * n1
        alb = col[None, None, :] * k[..., None]
        gp = sstep(ed, 0.0, gap * 1.4)[..., None]
        alb = alb * (0.22 + 0.78 * gp)
        h = sstep(ed, gap, gap + 5.0) * 2.0 + 0.9 * gr + 0.4 * gr2
        return alb.astype(np.float32), h.astype(np.float32)
    return fn


def mat_plaster(base="#4d4036", seed=5, rough=1.0, stain=0.5, tone=0.1):
    """Sıvalı/kerpiç duvar: lekeli, pürüzlü."""
    col = hex3(base)

    def fn(a, b):
        n1 = noise2d(a, b, 1 / 800.0, seed=seed)
        n2 = noise2d(a, b, 1 / 300.0, seed=seed + 1)
        n3 = noise2d(a, b, 1 / 150.0, seed=seed + 2)
        st = sstep(noise2d(a, b, 1 / 1500.0, 1 / 2000.0, seed=seed + 3), -0.3, 1.3)
        k = 1 + tone * n1 + 0.05 * n2 + 0.04 * n3
        alb = col[None, None, :] * k[..., None] * (1 - stain * 0.5 * st)[..., None]
        h = rough * (0.9 * n1 + 1.0 * n2 + 0.6 * n3) * 1.6
        return alb.astype(np.float32), h.astype(np.float32)
    return fn


def mat_beams(base="#2f2116", seed=7, pitch=230.0, bwid=64.0, plaster="#2a2018", axis="a"):
    """Tavan: kirişler (a boyunca aralıklı), arası sıva."""
    col = hex3(base)
    pcol = hex3(plaster)

    def fn(a, b):
        u = a if axis == "a" else b
        c = np.floor(u / pitch)
        fu = u / pitch - c
        d = np.abs(fu - 0.5) * pitch
        beam = sstep(bwid * 0.5 - d, 0.0, 6.0)
        gr = noise2d(a, b, 1 / 110.0, 1 / 1100.0, seed=seed) if axis == "a" else noise2d(a, b, 1 / 1100.0, 1 / 110.0, seed=seed)
        n1 = noise2d(a, b, 1 / 500.0, seed=seed + 1)
        k = 1 + 0.12 * gr + 0.08 * n1
        alb = (col[None, None, :] * beam[..., None] + pcol[None, None, :] * (1 - beam[..., None])) * k[..., None]
        h = beam * 14.0 + 0.8 * gr
        return alb.astype(np.float32), h.astype(np.float32)
    return fn


def mat_flags(base="#4a4038", seed=9, size=190.0, joint=3.0, tone=0.22, bevel=10.0, bevh=3.5, rough=1.0):
    """Taş döşeme plakaları (kare), yüzey yıpranmış."""
    return mat_ashlar(base, seed, bw=size, bh=size * 0.78, tone=tone, joint=joint, bevel=bevel, bevh=bevh, rough=rough, tilt=0.5, hue=0.05, stain=0.35)


def mat_marble(base="#8a7e70", seed=12, size=210.0, vein="#5a5048", tone=0.14):
    """Mermer döşeme: kare plakalar + damarlar (Aachen)."""
    col = hex3(base)
    vcol = hex3(vein)

    def fn(a, b):
        c = np.floor(a / size)
        r = np.floor(b / size)
        fu = a / size - c
        fv = b / size - r
        ed = np.minimum(np.minimum(fu, 1 - fu), np.minimum(fv, 1 - fv)) * size
        t = hash2(c, r, seed)
        n1 = noise2d(a, b, 1 / 600.0, seed=seed)
        n2 = noise2d(a, b, 1 / 200.0, seed=seed + 1)
        v = np.abs(np.sin((a * 0.012 + b * 0.007 + n1 * 2.4 + t * 9.0)))
        vm = sstep(0.06 - v * 0.06, 0.0, 0.05) * 0.0 + sstep(1.0 - v, 0.93, 1.0)
        k = 1 + tone * (t - 0.5) * 2 + 0.05 * n2
        alb = col[None, None, :] * k[..., None]
        alb = alb * (1 - 0.35 * vm[..., None]) + vcol[None, None, :] * 0.3 * vm[..., None] * 0
        gp = sstep(ed, 0.0, 2.8)[..., None]
        alb = alb * (0.3 + 0.7 * gp)
        h = sstep(ed, 2.6, 6.0) * 1.2 + 0.4 * n2
        return alb.astype(np.float32), h.astype(np.float32)
    return fn


def mat_split(upper, lower, b0, trim="#8a6a3a", tw=14.0):
    """Duvar: b<b0 üst malzeme, b>b0 alt malzeme (lambri), arada çıta. b0: düzlem 'b' koordinatında sınır (aşağı pozitif)."""
    tcol = hex3(trim)

    def fn(a, b):
        au, hu = upper(a, b)
        al, hl = lower(a, b)
        m = (b > b0)[..., None]
        alb = np.where(m, al, au)
        h = np.where(b > b0, hl, hu)
        strip = sstep(tw * 0.5 - np.abs(b - b0), 0.0, 3.0)
        alb = alb * (1 - strip[..., None]) + (tcol[None, None, :] * (0.8 + 0.3 * noise2d(a, b, 1 / 260.0, seed=3))[..., None]) * strip[..., None]
        h = h + strip * 7.0
        return alb.astype(np.float32), h.astype(np.float32)
    return fn


def mat_checker(c1="#2a2420", c2="#4b4036", size=120.0, seed=4, joint=2.0):
    """Dama taş döşeme (koyu/açık karolar)."""
    a1, a2 = hex3(c1), hex3(c2)

    def fn(a, b):
        ci, ri = np.floor(a / size), np.floor(b / size)
        fu, fv = a / size - ci, b / size - ri
        ed = np.minimum(np.minimum(fu, 1 - fu), np.minimum(fv, 1 - fv)) * size
        chk = ((ci + ri) % 2 == 0)[..., None]
        t = hash2(ci, ri, seed)
        n1 = noise2d(a, b, 1 / 420.0, seed=seed)
        n2 = noise2d(a, b, 1 / 150.0, seed=seed + 1)
        base = np.where(chk, a1[None, None, :], a2[None, None, :])
        k = 1 + 0.16 * (t - 0.5) * 2 + 0.07 * n1 + 0.05 * n2
        alb = base * k[..., None]
        gp = sstep(ed, 0.0, joint * 1.5)[..., None]
        alb = alb * (0.25 + 0.75 * gp)
        h = sstep(ed, joint, joint + 5.0) * 1.5 + 0.5 * n2
        return alb.astype(np.float32), h.astype(np.float32)
    return fn


def mat_stone_fine(base="#8a7c66", seed=3, course=46.0, tone=0.12, rough=0.7):
    """Sade kesme taş: ince sıra çizgileri + dikey derzler, yumuşak lekeler."""
    col = hex3(base)

    def fn(a, b):
        r = np.floor(b / course)
        fv = b / course - r
        off = hash2(r, r * 0, seed) * course * 3
        c = np.floor((a + off) / (course * 2.6))
        fu = (a + off) / (course * 2.6) - c
        ed = np.minimum(np.minimum(fu * course * 2.6, (1 - fu) * course * 2.6), np.minimum(fv * course, (1 - fv) * course))
        t = hash2(c, r, seed + 4)
        n1 = noise2d(a, b, 1 / 650.0, seed=seed)
        n2 = noise2d(a, b, 1 / 230.0, seed=seed + 1)
        n3 = noise2d(a, b, 1 / 130.0, seed=seed + 2)
        k = 1 + tone * (t - 0.5) * 2 + 0.07 * n1 + 0.05 * n2 + 0.03 * n3
        alb = col[None, None, :] * k[..., None]
        gp = sstep(ed, 0.0, 2.0)[..., None]
        alb = alb * (0.55 + 0.45 * gp)
        h = sstep(ed, 1.0, 5.0) * 2.0 + rough * (0.6 * n2 + 0.4 * n3)
        return alb.astype(np.float32), h.astype(np.float32)
    return fn


def mat_arcade(floor_b, stone="#b3a48a", brick="#8e3a2c", white="#d8cdb0", bay=215.0, off=0.0, lo=(150.0, 230.0, 24.0, 345.0), gal=(100.0, 520.0, 18.0, 600.0),
               top=760.0, seed=5, recess="#0c0908", base_fn=None):
    """Aachen tipi iki katlı kemerli galeri (alt: büyük kemerler; üst: galeri kemerleri), kemer taşları kırmızı/beyaz dönüşümlü.
    floor_b: duvar düzleminde zeminin 'b' koordinatı (aşağı pozitif). lo/gal=(açıklık genişliği, yay başlangıç yüksekliği, halka kalınlığı, korniş yüksekliği)."""
    st = base_fn or mat_stone_fine(stone, seed=seed)
    br, wh, rc = hex3(brick), hex3(white), hex3(recess)

    def fn(a, b):
        alb, h = st(a, b)
        hf = floor_b - b
        u = (a + off) / bay
        k = np.floor(u)
        x = (u - k - 0.5) * bay
        out_alb, out_h = alb.copy(), h.copy()
        for (ow, spring, t, cornice, ymin, ymax) in ((lo[0], lo[1], lo[2], lo[3], -1e9, lo[3] - 18.0), (gal[0], gal[1], gal[2], gal[3], lo[3] + 52.0, gal[3] - 18.0)):
            r = ow / 2
            cy = spring
            lvl = (hf > ymin) & (hf < ymax + 400)
            dist = np.sqrt(x * x + np.maximum(hf - cy, 0.0) ** 2)
            in_rect = (np.abs(x) < r) & (hf <= cy) & (hf > ymin)
            in_arch = (hf > cy) & (dist < r)
            opening = (in_rect | in_arch) & lvl
            ring_arch = (hf > cy) & (dist >= r) & (dist < r + t) & lvl
            ring_jamb = (np.abs(x) >= r) & (np.abs(x) < r + t) & (hf <= cy) & (hf > ymin) & lvl
            ang = np.arctan2(np.maximum(hf - cy, 0.0), x)
            idx_a = np.floor(ang / (math.pi / 11.0))
            idx_j = np.floor(hf / (t * 1.35))
            par = np.where(ring_arch, idx_a, idx_j) % 2 == 0
            ringm = (ring_arch | ring_jamb)
            ring_col = np.where(par[..., None], br[None, None, :], wh[None, None, :]) * (0.9 + 0.2 * hash2(np.where(ring_arch, idx_a, idx_j), k, seed + 9))[..., None]
            out_alb = np.where(ringm[..., None], ring_col, out_alb)
            out_h = np.where(ringm, h + 3.0, out_h)
            # açıklık: koyu girinti (derinlik hissi için gradyan)
            deep = np.clip((np.minimum(r - np.abs(x), 60.0)) / 60.0, 0, 1)[..., None]
            rec_alb = rc[None, None, :] * (0.6 + 0.8 * deep)
            out_alb = np.where(opening[..., None], rec_alb, out_alb)
            out_h = np.where(opening, h * 0.3 - 14.0, out_h)
        # korniş şeritleri
        for ch in (lo[3], gal[3]):
            band = sstep(11.0 - np.abs(hf - ch), 0.0, 2.5)
            out_alb = out_alb * (1 - band[..., None] * 0.35) + hex3(stone)[None, None, :] * band[..., None] * 0.35 * 1.2
            out_h = out_h + band * 6.0
        # galeri korkuluğu (bronz panel)
        par_m = (hf > lo[3] + 20) & (hf < lo[3] + 52)
        bz = hex3("#9a7a38")
        out_alb = np.where(par_m[..., None], bz[None, None, :] * (0.92 + 0.14 * noise2d(a, b, 1 / 650.0, seed=seed + 3))[..., None], out_alb)
        out_h = np.where(par_m, 1.0 + 2.0 * (np.abs(((u - k) * 8) % 1 - 0.5) < 0.1), out_h)
        return out_alb.astype(np.float32), out_h.astype(np.float32)
    return fn


def mat_mosaic(base="#c9962b", seed=2, tile=8.0, rib="#6a4a14"):
    """Altın mozaik tavan: küçük tesseralar (parlak/mat dalgalı), çok kuvvetli parıltı için yükseklik titreşimi."""
    col = hex3(base)
    rc = hex3(rib)

    def fn(a, b):
        ci, ri = np.floor(a / tile), np.floor(b / tile)
        fu, fv = a / tile - ci, b / tile - ri
        ed = np.minimum(np.minimum(fu, 1 - fu), np.minimum(fv, 1 - fv))
        t = hash2(ci, ri, seed)
        t2 = hash2(ci, ri, seed + 1)
        n1 = noise2d(a, b, 1 / 500.0, seed=seed)
        k = 0.65 + 0.7 * t * t + 0.12 * n1
        alb = col[None, None, :] * k[..., None]
        alb[..., 1] *= 0.92 + 0.14 * t2
        gp = sstep(ed, 0.0, 0.12)[..., None]
        alb = alb * (0.35 + 0.65 * gp)
        rb = sstep(24.0 - np.abs(((a / 260.0) % 1.0 - 0.5) * 260.0), 0.0, 3.0)
        alb = alb * (1 - 0.7 * rb[..., None]) + rc[None, None, :] * 0.7 * rb[..., None]
        h = (t - 0.5) * 3.0 + (t2 - 0.5) * 1.2 + sstep(ed, 0.02, 0.2) * 0.8
        return alb.astype(np.float32), h.astype(np.float32)
    return fn


def mat_flat(base="#201710", seed=1, rough=0.2):
    col = hex3(base)

    def fn(a, b):
        n = noise2d(a, b, 1 / 300.0, seed=seed)
        alb = col[None, None, :] * (1 + 0.05 * n)[..., None]
        return alb.astype(np.float32), (rough * n).astype(np.float32)
    return fn


# ───────────────────────────── ışıklar ─────────────────────────────
class Light:
    """Nokta ışık: p=(x_ekran, y_ekran, Z_derinlik); col lineer RGB; power; R yarıçap (yumuşak sönüm); spec parlaklık."""

    def __init__(self, p, col=(1.0, 0.62, 0.28), power=1.0, R=320.0, spec=0.0, far=None):
        self.p, self.col, self.power, self.R, self.spec, self.far = p, np.array(col, np.float32), power, R, spec, far


def warm(k=1.0):
    return (1.0 * k, 0.62 * k, 0.26 * k)


def cool(k=1.0):
    return (0.46 * k, 0.62 * k, 1.0 * k)


class Moon:
    """Ay/gün ışığı: paralel ışık, bir açıklıktan (gobo) süzülür.
    D: ışık yönü (kameraya doğru: z<0, aşağı: y>0). win=dict(z=Z_düzlem, rect=(x0,y0,x1,y1) EKRAN koordinatı o düzlemin
    ekran izdüşümü (Z=zb ölçeğinde), bars=dict(xs=[ekran x...], w=genişlik, ys=[ekran y...], hw=)."""

    def __init__(self, D, col=(0.42, 0.58, 1.0), power=1.0, win=None, pen=3.0, pen_k=0.012, decay=3200.0, shape=None):
        d = np.array(D, np.float32)
        self.D = d / np.linalg.norm(d)
        self.col, self.power, self.win, self.pen, self.pen_k, self.decay, self.shape = np.array(col, np.float32), power, win, pen, pen_k, decay, shape


# ───────────────────────────── perspektifli kutu oda ─────────────────────────────
class Box:
    """Tek noktalı perspektif oda. back=(x0,y0,x1,y1) arka duvar dikdörtgeni (ekran), vp kaçış noktası, zb arka duvar derinliği,
    F odak (dünya birimi = Z=F düzleminde piksel). Düzlemler: back/left/right/floor/ceil."""

    def __init__(self, back, vp=None, zb=1100.0, F=1100.0):
        self.bx0, self.by0, self.bx1, self.by1 = [float(v) for v in back]
        self.vx, self.vy = vp if vp else ((self.bx0 + self.bx1) / 2, (self.by0 + self.by1) / 2)
        self.zb, self.F = float(zb), float(F)

    def world(self, x, y, Z):
        return ((x - self.vx) * Z / self.F, (y - self.vy) * Z / self.F, float(Z))

    def screen(self, X, Yd, Z):
        return (self.vx + X * self.F / Z, self.vy + Yd * self.F / Z)

    def _planes(self, sx, sy):
        dx, dy = sx - self.vx, sy - self.vy
        nx = dx / np.where(dx < 0, self.bx0 - self.vx, self.bx1 - self.vx)
        ny = dy / np.where(dy < 0, self.by0 - self.vy, self.by1 - self.vy)
        inside = (nx <= 1.0) & (ny <= 1.0)
        out = ~inside
        side = out & (nx > ny)
        return dict(back=inside, left=side & (dx < 0), right=side & (dx >= 0),
                    ceil=out & (~(nx > ny)) & (dy < 0), floor=out & (~(nx > ny)) & (dy >= 0))

    def _geom(self, name, sx, sy):
        vx, vy, zb, F = self.vx, self.vy, self.zb, self.F
        k = zb / F
        dx, dy = sx - vx, sy - vy
        if name == "back":
            Z = np.full_like(sx, zb)
            Xw, Yw = dx * k, dy * k
            a, b = Xw, Yw
            n, ea, eb = (0.0, 0.0, -1.0), (1.0, 0.0, 0.0), (0.0, 1.0, 0.0)
        elif name in ("left", "right"):
            xe = self.bx0 if name == "left" else self.bx1
            s = np.maximum(dx / (xe - vx), 1e-3)
            Z = zb / s
            Xw = np.full_like(sx, (xe - vx) * k)
            Yw = dy * k / s
            a, b = zb - Z, Yw
            n = (1.0, 0.0, 0.0) if name == "left" else (-1.0, 0.0, 0.0)
            ea, eb = (0.0, 0.0, -1.0), (0.0, 1.0, 0.0)
        else:
            ye = self.by1 if name == "floor" else self.by0
            s = np.maximum(dy / (ye - vy), 1e-3)
            Z = zb / s
            Xw = dx * k / s
            Yw = np.full_like(sx, (ye - vy) * k)
            a, b = Xw, zb - Z
            n = (0.0, -1.0, 0.0) if name == "floor" else (0.0, 1.0, 0.0)
            ea, eb = (1.0, 0.0, 0.0), (0.0, 0.0, -1.0)
        return Xw.astype(np.float32), Yw.astype(np.float32), Z.astype(np.float32), a.astype(np.float32), b.astype(np.float32), n, ea, eb

    def hole_outer(self, rect, T=120.0, splay=0.82):
        """Arka duvardaki delik (ekran dikdörtgeni) için DIŞ açıklığın ekran dikdörtgeni (derinlik T, daralma splay)."""
        x0, y0, x1, y1 = rect
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        sc = self.zb / (self.zb + T)
        hw, hh = (x1 - x0) / 2 * splay, (y1 - y0) / 2 * splay
        ox = self.vx + (cx - self.vx) * sc
        oy = self.vy + (cy - self.vy) * sc
        return (ox - hw * sc, oy - hh * sc, ox + hw * sc, oy + hh * sc)

    def render(self, mats, lights=(), moon=None, ambient=(0.07, 0.06, 0.08), expo=1.15, ao=0.5, region=None, bump=1.0, only=None,
               tint=None, holes=()):
        """→ (rgb float32 [CH,CW,3] 0..1 sRGB, kapsama bool [CH,CW]). mats: dict(back,left,right,floor,ceil)=fn(a,b).
        holes: [dict(rect=(x0,y0,x1,y1), T=120, splay=.82, mat=fn)] arka duvarda tünel/pencere (içi şeffaf kalır)."""
        moon_in = moon
        xs = (np.arange(CW, dtype=np.float32) - M)[None, :] * np.ones((CH, 1), np.float32)
        ys = (np.arange(CH, dtype=np.float32) - M)[:, None] * np.ones((1, CW), np.float32)
        planes = self._planes(xs, ys)
        hole_m = np.zeros((CH, CW), bool)
        for hd in holes:
            x0, y0, x1, y1 = hd["rect"]
            hole_m |= (xs >= x0) & (xs <= x1) & (ys >= y0) & (ys <= y1)
        if holes:
            planes["back"] = planes["back"] & ~hole_m
        out = np.zeros((CH, CW, 3), np.float32)
        cov = np.zeros((CH, CW), bool)
        amb = np.array(ambient, np.float32)
        for name, m in planes.items():
            if only and name not in only:
                continue
            if region is not None:
                m = m & region
            if not m.any():
                continue
            rr, cc = np.where(m.any(1))[0], np.where(m.any(0))[0]
            y0, y1, x0, x1 = rr[0], rr[-1] + 1, cc[0], cc[-1] + 1
            y0, x0 = max(0, y0 - 2), max(0, x0 - 2)
            y1, x1 = min(CH, y1 + 2), min(CW, x1 + 2)
            sl = (slice(y0, y1), slice(x0, x1))
            sx, sy = xs[sl], ys[sl]
            X, Y, Z, a, b, n, ea, eb = self._geom(name, sx, sy)
            res = mats[name](a, b)
            alb, h = res[0], res[1]
            emit = res[2] if len(res) > 2 else None
            alb = alb * alb                              # sRGB → ~lineer
            # bump: ekran uzayı gradyanı → düzlem uzayı (J^-T)
            hx, hy = np.gradient(h, axis=1), np.gradient(h, axis=0)
            ax_, ay_ = np.gradient(a, axis=1), np.gradient(a, axis=0)
            bx_, by_ = np.gradient(b, axis=1), np.gradient(b, axis=0)
            det = ax_ * by_ - bx_ * ay_
            det = np.where(np.abs(det) < 1e-6, 1e-6, det)
            ha = (hx * by_ - bx_ * hy) / det
            hb = (ax_ * hy - ay_ * hx) / det
            kb = 0.55 * bump
            nxv = n[0] - kb * (ha * ea[0] + hb * eb[0])
            nyv = n[1] - kb * (ha * ea[1] + hb * eb[1])
            nzv = n[2] - kb * (ha * ea[2] + hb * eb[2])
            inv = 1.0 / np.sqrt(nxv * nxv + nyv * nyv + nzv * nzv)
            nxv, nyv, nzv = nxv * inv, nyv * inv, nzv * inv
            # ambient occlusion (köşe kararması)
            if ao:
                if name == "back":
                    e = np.minimum(np.minimum(sx - self.bx0, self.bx1 - sx), np.minimum(sy - self.by0, self.by1 - sy)) * (self.zb / self.F)
                    occ = 1 - ao * np.exp(-np.maximum(e, 0) / 70.0)
                else:
                    u = np.maximum(self.zb - Z, 0)
                    if name in ("left", "right"):
                        e2 = np.minimum(np.abs(Y - (self.by1 - self.vy) * self.zb / self.F), np.abs(Y - (self.by0 - self.vy) * self.zb / self.F))
                    else:
                        e2 = np.minimum(np.abs(X - (self.bx0 - self.vx) * self.zb / self.F), np.abs(X - (self.bx1 - self.vx) * self.zb / self.F))
                    occ = (1 - ao * np.exp(-u / 80.0)) * (1 - ao * 0.9 * np.exp(-e2 / 90.0))
                occ = occ.astype(np.float32)
            else:
                occ = 1.0
            E = np.empty(sx.shape + (3,), np.float32)
            E[...] = amb[None, None, :]
            E *= occ[..., None] if ao else 1.0
            # noktasal ışıklar
            vlen = 1.0 / np.sqrt(X * X + Y * Y + Z * Z)
            for L in lights:
                lx0, ly0, lz0 = self.world(*L.p)
                dxl, dyl, dzl = lx0 - X, ly0 - Y, lz0 - Z
                d2 = dxl * dxl + dyl * dyl + dzl * dzl + 1.0
                il = 1.0 / np.sqrt(d2)
                ndl = np.maximum((nxv * dxl + nyv * dyl + nzv * dzl) * il, 0.0)
                ndl = 0.18 + 0.82 * ndl                                   # sarılı difüz (gölge kenarı yumuşak)
                att = 1.0 / (1.0 + d2 / (L.R * L.R)) ** 1.35
                wgt = (L.power * ndl * att)
                if ao:
                    wgt = wgt * (0.55 + 0.45 * occ)
                E += wgt[..., None] * L.col[None, None, :]
                if L.far:
                    att2 = 1.0 / (1.0 + d2 / (L.far[0] * L.far[0])) ** 1.2
                    E += (L.power * L.far[2] * ndl * att2)[..., None] * np.array(L.far[1], np.float32)[None, None, :]
                if L.spec:
                    hxv, hyv, hzv = dxl * il - X * vlen, dyl * il - Y * vlen, dzl * il - Z * vlen
                    hl = 1.0 / np.sqrt(hxv * hxv + hyv * hyv + hzv * hzv + 1e-6)
                    sp = np.maximum((nxv * hxv + nyv * hyv + nzv * hzv) * hl, 0.0) ** 36
                    E += (L.spec * L.power * sp * att * (h * 0 + 1.0))[..., None] * L.col[None, None, :] * 0.8
            # ay ışığı (gobo)
            for moon in ([] if moon_in is None else (list(moon_in) if isinstance(moon_in, (list, tuple)) else [moon_in])):
                mp = moon.power
                D = moon.D
                ndm = np.maximum(-(nxv * D[0] + nyv * D[1] + nzv * D[2]), 0.0)
                win = moon.win
                lit = np.ones_like(X)
                if win is not None and win.get("axis") == "x":
                    tau = (win["x"] - X) / (-D[0] if abs(D[0]) > 1e-6 else 1e-6)
                    ok = tau > 0
                    zq = Z + tau * (-D[2])
                    yq = Y + tau * (-D[1])
                    z0, y0, z1, y1 = win["wrect"]
                    pitch, nwin = win.get("pitch", 0.0), win.get("n", 1)
                    if pitch:
                        idx = np.clip(np.floor((zq - z0) / pitch), 0, nwin - 1)
                        zl = zq - idx * pitch
                    else:
                        zl = zq
                    pen = moon.pen + moon.pen_k * np.maximum(tau, 0)
                    zc = (z0 + z1) / 2
                    hw = np.full_like(zl, (z1 - z0) / 2)
                    spr_ = win.get("spring")
                    if spr_ is not None:
                        k_ = np.clip((spr_ - yq) / max(spr_ - y0, 1e-3), 0, 1)
                        hw = hw * (1 - k_ ** 1.7)
                    lit = sstep(hw - np.abs(zl - zc), -pen, pen) * sstep(yq - y0, -pen, pen) * sstep(y1 - yq, -pen, pen) * ok
                    win = None
                    fall = 1.0
                    wgt = mp * ndm * lit * fall
                    if ao:
                        wgt = wgt * (0.7 + 0.3 * occ)
                    E += wgt[..., None] * moon.col[None, None, :]
                    continue
                if win is not None:
                    zw = win["z"]
                    tau = (zw - Z) / (-D[2])
                    ok = tau > 0
                    xw = X + tau * (-D[0])
                    yw = Y + tau * (-D[1])
                    x0, y0, x1, y1 = win["wrect"]
                    pen = moon.pen + moon.pen_k * np.maximum(tau, 0)
                    lit = sstep(xw - x0, -pen, pen) * sstep(x1 - xw, -pen, pen) * sstep(yw - y0, -pen, pen) * sstep(y1 - yw, -pen, pen)
                    bars = win.get("bars")
                    if bars:
                        for bx in bars["wxs"]:
                            lit = lit * sstep(np.abs(xw - bx) - bars["w"] * 0.5, -pen, pen)
                        for by in bars.get("wys", []):
                            lit = lit * sstep(np.abs(yw - by) - bars.get("hw", bars["w"]) * 0.5, -pen, pen)
                    lit = lit * ok
                fall = np.exp(-np.maximum(Z * 0 + (win["z"] - Z if win else 0), 0) / moon.decay)
                wgt = mp * ndm * lit * fall
                if ao:
                    wgt = wgt * (0.7 + 0.3 * occ)
                E += wgt[..., None] * moon.col[None, None, :]
            col = alb * E
            if emit is not None:
                col = col + emit
            if tint is not None:
                col = col * np.array(tint, np.float32)[None, None, :]
            col = 1.0 - np.exp(-col * expo)                # filmik omuz
            col = np.sqrt(np.clip(col, 0, 1))
            mm = m[sl]
            blk = out[sl]
            blk[mm] = col[mm]
            cov[sl] |= mm
        for hd in holes:
            x0, y0, x1, y1 = hd["rect"]
            ring = (xs >= x0) & (xs <= x1) & (ys >= y0) & (ys <= y1)
            outer = self.hole_outer(hd["rect"], hd.get("T", 120.0), hd.get("splay", 0.82))
            sub = Box(outer, vp=(self.vx, self.vy), zb=self.zb + hd.get("T", 120.0), F=self.F)
            tm = hd.get("mat") or mats["back"]
            r2, c2 = sub.render(dict(left=tm, right=tm, floor=tm, ceil=tm, back=tm), lights, moon_in, ambient, expo, ao=hd.get("ao", 0.3), region=ring, bump=bump,
                                only=("left", "right", "floor", "ceil"), tint=tint)
            out[c2] = r2[c2]
            cov |= c2
        return out, cov


def to_image(rgb_f, alpha=None):
    """float32 [CH,CW,3] (0..1) (+ alpha float/bool) → skia.Image (katman tuvali boyutu)."""
    a = np.clip(rgb_f * 255.0, 0, 255).astype(np.uint8)
    al = np.full(a.shape[:2] + (1,), 255, np.uint8) if alpha is None else (np.clip(alpha.astype(np.float32), 0, 1) * 255).astype(np.uint8)[..., None]
    return sk.np_to_image(np.concatenate([a, al], 2))


def draw_np(f, rgb_f, alpha=None):
    f.c.drawImage(to_image(rgb_f, alpha), -M, -M, skia.SamplingOptions(skia.FilterMode.kLinear), skia.Paint())


# ───────────────────────────── skia ilkelleri (pişirmede) ─────────────────────────────
def glow(f, x, y, r, col="#FFB347", a=0.5, sy=1.0, blend=True):
    """Toplamsal radyal parıltı."""
    f.c.save()
    f.c.translate(x, y)
    f.c.scale(1.0, sy)
    f.c.drawCircle(0, 0, r, skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeRadial((0, 0), r, [C(col, int(255 * a)), C(col, int(255 * a * 0.45)), C(col, 0)], [0.0, 0.35, 1.0]),
                                       BlendMode=skia.BlendMode.kPlus if blend else skia.BlendMode.kSrcOver))
    f.c.restore()


def soft_poly(f, pts, col, a, blur=6.0, blend=skia.BlendMode.kPlus, shader=None):
    p = sk.poly_path(pts, True)
    pa = skia.Paint(AntiAlias=True, Color=C(col, int(255 * a)), BlendMode=blend)
    if shader is not None:
        pa.setShader(shader)
    if blur:
        pa.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, blur))
    f.c.drawPath(p, pa)


def vignette_frame(f, a=0.85, inner=0.5, col="#000000"):
    """Katman içi kenar karartması (ön plan çerçevesi)."""
    sh = skia.GradientShader.MakeRadial((W / 2, H / 2), max(W, H) * 0.82, [C(col, 0), C(col, 0), C(col, int(255 * a))], [0.0, inner, 1.0])
    f.c.drawRect(skia.Rect.MakeLTRB(-M, -M, W + M, H + M), skia.Paint(Shader=sh))


def noise_overlay(f, rect, amp=0.2, scale=60, seed=3, mode=skia.BlendMode.kSoftLight):
    """Dikdörtgen içine gürültü dokusu bindir (yalnız OPAK bölgelerde kullan)."""
    x, y, w, h = [int(v) for v in rect]
    n = sk.noise_tex(max(8, w // 2), max(8, h // 2), max(4, scale // 2), 4, seed)
    g8 = np.clip(128 + (n - 0.5) * 255 * amp * 2, 0, 255).astype(np.uint8)
    img = sk.gray_to_image(cv2.resize(g8, (w, h), interpolation=cv2.INTER_LINEAR))
    f.c.drawImage(img, x, y, skia.SamplingOptions(skia.FilterMode.kLinear), skia.Paint(BlendMode=mode))


def lit_path(f, path, base, lights=(), rim=None, rim_w=1.6, edge=None, a=1.0, bright=1.0, grad=None):
    """Bir yolu temel renkle doldur; ışık kaynaklarına (x,y,R,col,a) göre radyal aydınlat; isteğe bağlı kenar ışığı."""
    f.c.save()
    f.c.clipPath(path, skia.ClipOp.kIntersect, True)
    if grad is not None:
        f.c.drawPaint(skia.Paint(AntiAlias=True, Shader=grad))
    else:
        f.c.drawPaint(skia.Paint(AntiAlias=True, Color=C(base, int(255 * a))))
    for (lx, ly, lr, lc, la) in lights:
        f.c.drawCircle(lx, ly, lr, skia.Paint(AntiAlias=True, BlendMode=skia.BlendMode.kPlus,
                                               Shader=skia.GradientShader.MakeRadial((lx, ly), lr, [C(lc, int(255 * la * bright)), C(lc, int(255 * la * 0.35 * bright)), C(lc, 0)], [0.0, 0.45, 1.0])))
    f.c.restore()
    if rim:
        f.path(path, style="stroke", sw=rim_w, color=rim, alpha=0.8)
    if edge:
        f.path(path, style="stroke", sw=1.0, color=edge, alpha=0.7)


def rect_path(x, y, w, h):
    p = skia.Path()
    p.addRect(skia.Rect.MakeXYWH(x, y, w, h))
    return p


def rrect_path(x, y, w, h, r):
    p = skia.Path()
    p.addRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, w, h), r, r))
    return p


def bar_rod(f, x0, y0, x1, y1, w=9, col="#14100d", hl="#8aa6d8", hl_a=0.6, light=-1):
    """Demir çubuk: koyu gövde + ışık yönüne bakan ince kenar parıltısı."""
    f.line(x0, y0, x1, y1, color=col, sw=w, cap="butt")
    dx, dy = x1 - x0, y1 - y0
    L = math.hypot(dx, dy) or 1
    nx, ny = -dy / L, dx / L
    o = w * 0.34 * light
    f.line(x0 + nx * o, y0 + ny * o, x1 + nx * o, y1 + ny * o, color=hl, sw=max(1.2, w * 0.2), alpha=hl_a, cap="butt")


# ───────────────────────────── alev / mum / toz (dyn'de ucuz) ─────────────────────────────
def flicker(t, seed=0.0, k=1.0):
    """Mum titremesi 0.6..1.25 (birkaç sinüs)."""
    v = 0.5 * math.sin(t * 11.3 + seed * 2.1) + 0.3 * math.sin(t * 17.9 + seed * 5.3) + 0.2 * math.sin(t * 5.1 + seed)
    return 1.0 + 0.16 * k * v


def flame(f, x, y, s=1.0, t=0.0, seed=0.0, halo=1.0, a=1.0, col_out="#FF9A2E", col_in="#FFF3C4", halo_col="#FFB45A", hr=170.0):
    """Mum alevi: damla biçimi + parıltı. (x,y) fitilin ucu; s ölçek (1 ≈ 26 px yüksek)."""
    if a <= 0.01 or s <= 0.01:
        return
    fl = flicker(t, seed)
    sway = math.sin(t * 6.3 + seed * 1.7) * 1.8 * s + math.sin(t * 13.1 + seed) * 0.8 * s
    hh = 27.0 * s * fl
    ww = 8.2 * s * (2.0 - fl * 0.9) * 0.62
    if halo > 0:
        r = hr * s * (0.92 + 0.14 * fl) * halo
        f.c.drawCircle(x, y - hh * 0.45, r, skia.Paint(AntiAlias=True, BlendMode=skia.BlendMode.kPlus, Shader=skia.GradientShader.MakeRadial(
            (x, y - hh * 0.45), r, [C(halo_col, int(150 * a)), C(halo_col, int(48 * a)), C(halo_col, 0)], [0.0, 0.3, 1.0])))
    p = skia.Path()
    p.moveTo(x, y + 3 * s)
    p.cubicTo(x - ww * 1.25, y - hh * 0.12, x - ww * 0.55 + sway * 0.1, y - hh * 0.62, x + sway, y - hh)
    p.cubicTo(x + ww * 0.55 + sway * 0.1, y - hh * 0.62, x + ww * 1.25, y - hh * 0.12, x, y + 3 * s)
    f.c.drawPath(p, skia.Paint(AntiAlias=True, Color=C(col_out, int(235 * a))))
    p2 = skia.Path()
    p2.moveTo(x, y + 2 * s)
    p2.cubicTo(x - ww * 0.7, y - hh * 0.1, x - ww * 0.28 + sway * 0.05, y - hh * 0.5, x + sway * 0.7, y - hh * 0.72)
    p2.cubicTo(x + ww * 0.28 + sway * 0.05, y - hh * 0.5, x + ww * 0.7, y - hh * 0.1, x, y + 2 * s)
    f.c.drawPath(p2, skia.Paint(AntiAlias=True, Color=C(col_in, int(255 * a))))
    f.c.drawCircle(x, y + 0.5 * s, 2.4 * s, skia.Paint(AntiAlias=True, Color=C("#6FA0FF", int(110 * a))))


def candle_body(f, x, y, h=70, w=15, col="#D9C79A", holder=True, lit_side=1, melt=0.0):
    """Mum gövdesi (y: tabanın alt ucu). holder: pirinç dip tabaklı."""
    if holder:
        f.oval(x, y + 2, w * 1.5, w * 0.34, color="#1a120a")
        f.oval(x, y, w * 1.35, w * 0.3, color="#5b4220")
        f.oval(x, y - 1.5, w * 1.15, w * 0.22, color="#a8823e")
    f.rect(x - w / 2, y - h, w, h, shader=f.lin(x - w / 2, 0, x + w / 2, 0, [(shade(col, -0.45), 0.0), (shade(col, 0.1), 0.45 if lit_side > 0 else 0.55), (shade(col, -0.35), 1.0)]))
    f.oval(x, y - h, w / 2, w * 0.17, color=shade(col, 0.2))
    f.oval(x, y - h - 0.5, w * 0.12, w * 0.06, color="#201208")
    if melt > 0:
        for i, (dxm, ln) in enumerate(((-0.28, 0.35), (0.25, 0.22))):
            f.rect(x + dxm * w - 1.5, y - h, 3, ln * h * melt, color=shade(col, 0.08))


def motes(f, t, rect, n=34, seed=3, col="#FFE2B0", a=0.55, drift=(5, -3), size=(0.9, 2.1), mask=None):
    """Askıdaki toz zerrecikleri (kaynaşma yok, ucuz). rect=(x,y,w,h); mask(x,y)->0..1 parlaklık çarpanı."""
    rs = np.random.RandomState(seed)
    x0, y0, w, h = rect
    pa = skia.Paint(AntiAlias=True, BlendMode=skia.BlendMode.kPlus)
    for i in range(n):
        d = 0.35 + 0.65 * rs.rand()
        px = x0 + (rs.rand() * w + t * drift[0] * d + math.sin(t * 0.37 + i * 1.3) * 14 * d) % w
        py = y0 + (rs.rand() * h + t * drift[1] * d + math.cos(t * 0.29 + i * 2.1) * 12 * d) % h
        tw = 0.35 + 0.65 * abs(math.sin(t * (0.6 + 0.5 * rs.rand()) + i * 2.7))
        m = 1.0 if mask is None else mask(px, py)
        al = a * d * tw * m
        if al < 0.02:
            continue
        r = size[0] + (size[1] - size[0]) * d
        pa.setColor(C(col, int(255 * min(1.0, al))))
        f.c.drawCircle(px, py, r, pa)
        pa.setColor(C(col, int(255 * min(1.0, al) * 0.22)))
        f.c.drawCircle(px, py, r * 2.6, pa)


def embers_lite(f, t, x, y, n=14, seed=5, rise=90.0, spread=26.0, col="#FFB347"):
    """Küçük kıvılcım/kor (meşale/şömine)."""
    rs = np.random.RandomState(seed)
    pa = skia.Paint(AntiAlias=True, BlendMode=skia.BlendMode.kPlus)
    for i in range(n):
        ph = (t * (0.25 + 0.35 * rs.rand()) + rs.rand()) % 1.0
        px = x + (rs.rand() - 0.5) * spread + math.sin(t * 2 + i) * 9 * ph
        py = y - ph * rise * (0.6 + 0.8 * rs.rand())
        al = (1 - ph) ** 1.4 * (0.5 + 0.5 * abs(math.sin(t * 7 + i * 2)))
        pa.setColor(C(col, int(255 * al)))
        f.c.drawCircle(px, py, 1.1 + 1.0 * rs.rand(), pa)


# ───────────────────────────── ışık huzmeleri (pişirmede) ─────────────────────────────
def beam(f, quad, col="#9FB6E6", a=0.16, blur=5.0, fade_to=None, streak=True, seed=1):
    """Hacimsel ışık huzmesi: dörtgen (pencere → zemin). quad=[(x,y)...4]; ucu sönükleşir; ince lifli çizgilerle."""
    (x0, y0), (x1, y1), (x2, y2), (x3, y3) = quad
    mid_s = ((x0 + x1) / 2, (y0 + y1) / 2)
    mid_e = ((x2 + x3) / 2, (y2 + y3) / 2)
    sh = skia.GradientShader.MakeLinear([mid_s, mid_e], [C(col, int(255 * a)), C(col, int(255 * a * 0.55)), C(col, 0 if fade_to is None else int(255 * fade_to))], [0.0, 0.55, 1.0])
    pa = skia.Paint(AntiAlias=True, Shader=sh, BlendMode=skia.BlendMode.kPlus)
    if blur:
        pa.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, blur))
    f.c.drawPath(sk.poly_path(quad, True), pa)
    if streak:
        rs = np.random.RandomState(seed)
        for i in range(5):
            u0, u1 = sorted(rs.rand(2))
            q = [lerp_pt((x0, y0), (x1, y1), u0), lerp_pt((x0, y0), (x1, y1), u1), lerp_pt((x3, y3), (x2, y2), u1), lerp_pt((x3, y3), (x2, y2), u0)]
            pa2 = skia.Paint(AntiAlias=True, Shader=sh, BlendMode=skia.BlendMode.kPlus, Alpha=int(255 * (0.25 + 0.4 * rs.rand())))
            pa2.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, blur * 0.7))
            f.c.drawPath(sk.poly_path(q, True), pa2)


def lerp_pt(p, q, u):
    return (p[0] + (q[0] - p[0]) * u, p[1] + (q[1] - p[1]) * u)


# ───────────────────────────── dış dünya (pencereden görünen) ─────────────────────────────
def night_sky(f, top="#050912", mid="#0c1a2e", hor="#1b3550", moon=None, stars=60, seed=4, clouds=True, y_h=700):
    """Gece gökyüzü: degrade + yıldızlar + ay + bulutlar (pişirmede; bulanık)."""
    f.rect(-M, -M, W + 2 * M, H + 2 * M, shader=f.lin(0, -M, 0, y_h, [(top, 0.0), (mid, 0.55), (hor, 1.0)]))
    rs = np.random.RandomState(seed)
    for i in range(stars):
        x, y = rs.uniform(-M, W + M), rs.uniform(-M, y_h * 0.8)
        a = 0.25 + 0.6 * rs.rand() * (1 - y / (y_h * 1.0)) ** 0.5
        f.circle(x, y, 0.8 + 1.1 * rs.rand(), color="#DDE8FF", alpha=max(0.05, a))
    if moon:
        mx, my, mr = moon
        glow(f, mx, my, mr * 7.0, "#7FA0D8", 0.35)
        glow(f, mx, my, mr * 3.2, "#BBD0F5", 0.45)
        f.circle(mx, my, mr, shader=f.rad(mx - mr * 0.25, my - mr * 0.25, mr * 1.3, [("#FFFFFF", 0.0), ("#E4ECFA", 0.6), ("#B7C6E2", 1.0)]))
        rm = np.random.RandomState(9)
        for i in range(7):
            ang, rad = rm.rand() * 6.28, rm.rand() * mr * 0.7
            f.circle(mx + math.cos(ang) * rad, my + math.sin(ang) * rad, mr * (0.1 + 0.16 * rm.rand()), color="#8E9DBA", alpha=0.25)
    if clouds:
        for i in range(7):
            cx_, cy_ = rs.uniform(-M, W + M), rs.uniform(y_h * 0.25, y_h * 0.9)
            w_, h_ = rs.uniform(260, 620), rs.uniform(22, 54)
            pa = skia.Paint(AntiAlias=True, Color=C("#0A1220", int(255 * rs.uniform(0.35, 0.65))))
            pa.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 22))
            f.c.drawOval(skia.Rect.MakeLTRB(cx_ - w_, cy_ - h_, cx_ + w_, cy_ + h_), pa)
            if moon:
                pa2 = skia.Paint(AntiAlias=True, Color=C("#8FA9D8", int(255 * 0.12)))
                pa2.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 14))
                f.c.drawOval(skia.Rect.MakeLTRB(cx_ - w_ * 0.9, cy_ - h_ * 1.1, cx_ + w_ * 0.8, cy_ - h_ * 0.1), pa2)


# ───────────────────────────── siluet figürler (kendi hattımız) ─────────────────────────────
ROOM_FIG = {}


def rfig(name):
    def deco(fn):
        ROOM_FIG[name] = fn
        return fn
    return deco


def _area(pts):
    return 0.5 * sum(pts[i][0] * pts[(i + 1) % len(pts)][1] - pts[(i + 1) % len(pts)][0] * pts[i][1] for i in range(len(pts)))


def _sp(pts, h, close=True, t=0.5):
    pts = [(x * h, y * h) for x, y in pts]
    if close and _area(pts) < 0:
        pts = pts[::-1]
    return sk.smooth_path(pts, close, t)


def _pp(pts, h):
    pts = [(x * h, y * h) for x, y in pts]
    if _area(pts) < 0:
        pts = pts[::-1]
    return sk.poly_path(pts, True)


def _union(*paths):
    p = skia.Path()
    for q in paths:
        p.addPath(q)
    return p


def _ellipse(cx, cy, rx, ry, h):
    p = skia.Path()
    p.addOval(skia.Rect.MakeLTRB((cx - rx) * h, (cy - ry) * h, (cx + rx) * h, (cy + ry) * h))
    return p


@lru_cache(maxsize=256)
def _rf_sprite(kind, hpx, col, rimc, rimd, rim2, rim2d, rimw, hl):
    """Siluet sprite: gövde + iç kenar ışığı (iki yönlü: sıcak/soğuk) + hafif iç degrade. Dönüş: (img, ox, oy)."""
    hpx = float(hpx)
    path, detail = ROOM_FIG[kind](hpx)
    b = path.getBounds()
    pad = max(8, int(hpx * 0.06))
    l, t = int(math.floor(b.left())) - pad, int(math.floor(b.top())) - pad
    r, bt = int(math.ceil(b.right())) + pad, int(math.ceil(b.bottom())) + pad
    s = skia.Surface(max(4, r - l), max(4, bt - t))
    c = s.getCanvas()
    c.clear(skia.ColorTRANSPARENT)
    c.translate(-l, -t)
    body = skia.Paint(AntiAlias=True, Color=C(col))
    c.drawPath(path, body)
    # kenar ışıkları: silueti ışığa doğru kaydırıp iç kenar bırak
    def rim_pass(color, d, w, alpha):
        if not color or alpha <= 0:
            return
        c.save()
        c.clipPath(path, skia.ClipOp.kIntersect, True)
        lay = skia.Paint(AntiAlias=True)
        c.saveLayer(None, lay)
        c.drawPath(path, skia.Paint(AntiAlias=True, Color=C(color, int(255 * alpha))))
        c.translate(-d[0] * w, -d[1] * w)
        c.drawPath(path, skia.Paint(AntiAlias=True, BlendMode=skia.BlendMode.kDstOut, Color=C("#000000")))
        c.restore()
        c.restore()
    rim_pass(rimc, rimd, rimw, 0.95)
    rim_pass(rim2, rim2d, rimw * 0.9, 0.75)
    if detail is not None:
        c.save()
        c.clipPath(path, skia.ClipOp.kIntersect, True)
        detail(c, col, rimc, rimd, rim2, hl)
        c.restore()
    return s.makeImageSnapshot(), -l, -t


def rfigure(f, kind, x, y, h, col="#0A0605", rim="#E0A15A", rimd=(-1.0, -0.2), rim2=None, rim2d=(1.0, -0.3), rimw=2.2, face=1, alpha=1.0, sway=0.0, bob=0.0, hl=0.0):
    """Kendi siluet figürüm. y = ayak (veya oturma zemini). face=-1 ayna (rim yönü de aynalanır)."""
    rd = (rimd[0] * face, rimd[1])
    r2 = (rim2d[0] * face, rim2d[1])
    img, ox, oy = _rf_sprite(kind, int(round(h)), col, rim, rd, rim2, r2, round(rimw, 1), round(hl, 2))
    f.c.save()
    f.c.translate(x, y + bob)
    if sway:
        f.c.rotate(math.degrees(sway))
    f.c.scale(face, 1)
    p = skia.Paint(AntiAlias=True)
    if alpha < 1:
        p.setAlphaf(alpha)
    f.c.drawImage(img, -ox, -oy, skia.SamplingOptions(skia.FilterMode.kLinear), p)
    f.c.restore()


def rfig_path(kind, h):
    return ROOM_FIG[kind](float(h))[0]


def window_gobo(box, rect, zw, xs=(), bar_w=8.0, ys=(), bar_hw=None):
    """Ay ışığı açıklığı. rect=(x0,y0,x1,y1): açıklığın, Z=zw düzleminde EKRAN izdüşümü; xs/ys: demir çubukların ekran konumları."""
    k = zw / box.F
    x0, y0, x1, y1 = rect
    wr = ((x0 - box.vx) * k, (y0 - box.vy) * k, (x1 - box.vx) * k, (y1 - box.vy) * k)
    d = dict(z=zw, wrect=wr)
    if xs or ys:
        d["bars"] = dict(wxs=[(x - box.vx) * k for x in xs], w=bar_w * k, wys=[(y - box.vy) * k for y in ys], hw=(bar_hw or bar_w) * k)
    return d


# ═════════════════════════════ FİGÜRLER: oda-lab türleri ═════════════════════════════
# Hepsi sağa bakar (face=-1 ayna). h = zeminden tepeye boy. detail(c,col,rim,rimd,rim2,hl): gövde içine kıvrım/ayrıntı.
def _fold(c, pts, col, a=0.25, w=1.4):
    p = sk.smooth_path(pts, False, 0.5)
    c.drawPath(p, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=w, Color=C(col, int(255 * a)), StrokeCap=skia.Paint.kRound_Cap))


def _rot(path, ang, cx, cy, h):
    """Yolu (cx,cy) birim koordinatı etrafında ang radyan döndür (birim = h)."""
    m = skia.Matrix()
    m.setRotate(math.degrees(ang), cx * h, cy * h)
    q = skia.Path(path)
    q.transform(m)
    return q


@rfig("woman_seated")
def _f_woman_seated(h):
    """Tordesillas: alçak tabureye oturmuş, peçeli kadın (profil, sağa bakar, başı pencereye doğru hafif kalkık)."""
    head = _sp([(0.085, -0.95), (0.135, -0.972), (0.18, -0.95), (0.197, -0.915), (0.212, -0.893), (0.197, -0.88), (0.2, -0.862), (0.185, -0.842),
                (0.155, -0.828), (0.12, -0.835), (0.088, -0.86), (0.078, -0.91)], h, True, 0.5)
    veil = _sp([(0.19, -0.962), (0.135, -1.0), (0.062, -0.99), (0.0, -0.95), (-0.06, -0.89), (-0.11, -0.80), (-0.15, -0.69), (-0.17, -0.58), (-0.135, -0.50),
                (-0.07, -0.60), (-0.02, -0.71), (0.035, -0.79), (0.07, -0.84), (0.09, -0.90)], h, True, 0.5)
    head = _rot(_union(head, veil), -0.10, 0.10, -0.80, h)
    neck = _pp([(0.07, -0.86), (0.15, -0.86), (0.165, -0.77), (0.055, -0.77)], h)
    torso = _sp([(-0.035, -0.80), (0.04, -0.815), (0.115, -0.785), (0.16, -0.735), (0.175, -0.68), (0.155, -0.60), (0.125, -0.545), (0.14, -0.50), (0.0, -0.49),
                 (-0.07, -0.54), (-0.10, -0.62), (-0.085, -0.72)], h, True, 0.4)
    skirt = _sp([(-0.24, 0.0), (-0.285, -0.20), (-0.255, -0.40), (-0.12, -0.50), (0.12, -0.52), (0.30, -0.49), (0.40, -0.40), (0.44, -0.22), (0.47, -0.03),
                 (0.45, 0.0)], h, True, 0.42)
    arm = _sp([(0.015, -0.77), (0.085, -0.73), (0.115, -0.63), (0.17, -0.565), (0.27, -0.525), (0.335, -0.51), (0.34, -0.48), (0.27, -0.475), (0.15, -0.50),
               (0.065, -0.57), (0.03, -0.66), (-0.01, -0.72)], h, True, 0.4)

    def detail(c, col, rim, rimd, rim2, hl):
        rc = rim or "#C58A44"
        for pts in (((0.03, -0.46), (0.12, -0.30), (0.20, -0.14), (0.24, -0.01)), ((0.17, -0.48), (0.31, -0.34), (0.40, -0.17), (0.44, -0.01)),
                    ((-0.12, -0.40), (-0.15, -0.24), (-0.19, -0.10), (-0.22, -0.01))):
            _fold(c, [(x * h, y * h) for x, y in pts], rc, 0.16, max(1.0, h * 0.0035))
        _fold(c, [(x * h, y * h) for x, y in ((-0.05, -0.93), (-0.09, -0.82), (-0.13, -0.70), (-0.15, -0.60))], rc, 0.14, max(1.0, h * 0.003))
    return _union(head, neck, torso, skirt, arm), detail


@rfig("man_window")
def _f_man_window(h):
    """Madrid hücresi: pencereye dönük ayakta sakallı erkek (profil), bir kolu demire uzanmış, düz bere."""
    torso = _sp([(-0.075, -0.795), (-0.095, -0.66), (-0.085, -0.535), (-0.12, -0.50), (-0.10, -0.40), (-0.075, -0.26), (-0.08, -0.06), (-0.10, -0.01),
                 (0.07, -0.005), (0.115, -0.03), (0.10, -0.045), (0.045, -0.06), (0.05, -0.22), (0.08, -0.40), (0.14, -0.50), (0.125, -0.58),
                 (0.10, -0.70), (0.075, -0.775), (0.055, -0.80)], h, True, 0.4)
    head = _union(
        _sp([(0.055, -0.80), (0.06, -0.845), (0.07, -0.875), (0.065, -0.915), (0.082, -0.955), (0.12, -0.965), (0.155, -0.94), (0.165, -0.905),
             (0.185, -0.89), (0.172, -0.875), (0.178, -0.835), (0.165, -0.795), (0.135, -0.775), (0.10, -0.80), (0.085, -0.84)], h, True, 0.45),
        _sp([(0.06, -0.965), (0.10, -0.995), (0.165, -0.99), (0.20, -0.965), (0.185, -0.95), (0.14, -0.955), (0.085, -0.945)], h, True, 0.35))
    arm = _sp([(0.06, -0.785), (0.13, -0.80), (0.20, -0.86), (0.245, -0.93), (0.275, -0.955), (0.285, -0.935), (0.265, -0.90), (0.235, -0.835),
               (0.18, -0.765), (0.11, -0.73), (0.07, -0.72)], h, True, 0.4)
    back_arm = _sp([(-0.07, -0.77), (-0.115, -0.68), (-0.125, -0.56), (-0.10, -0.52), (-0.08, -0.60), (-0.055, -0.70)], h, True, 0.4)
    leg2 = _sp([(-0.04, -0.30), (0.01, -0.30), (0.03, -0.12), (0.045, -0.03), (-0.005, -0.0), (-0.05, -0.02), (-0.05, -0.12)], h, True, 0.3)
    mantle = _sp([(-0.07, -0.78), (-0.15, -0.72), (-0.19, -0.50), (-0.18, -0.30), (-0.13, -0.28), (-0.10, -0.40), (-0.09, -0.60)], h, True, 0.4)

    def detail(c, col, rim, rimd, rim2, hl):
        rc = rim or "#C58A44"
        _fold(c, [(x * h, y * h) for x, y in ((-0.12, -0.70), (-0.14, -0.55), (-0.15, -0.40), (-0.13, -0.30))], rc, 0.14, max(1.0, h * 0.003))
    return _union(torso, head, arm, back_arm, leg2, mantle), detail


def _writer_build(h, beard=True, hat=False):
    torso = _sp([(-0.06, -0.785), (-0.14, -0.72), (-0.185, -0.57), (-0.20, -0.43), (-0.15, -0.37), (0.10, -0.42), (0.19, -0.50), (0.17, -0.62),
                 (0.12, -0.73), (0.07, -0.785)], h, True, 0.45)
    thigh = _sp([(-0.14, -0.45), (0.20, -0.46), (0.38, -0.45), (0.445, -0.40), (0.44, -0.30), (0.36, -0.275), (0.0, -0.29), (-0.15, -0.30)], h, True, 0.3)
    shin = _sp([(0.35, -0.33), (0.445, -0.33), (0.455, -0.05), (0.52, -0.025), (0.525, 0.0), (0.30, 0.0), (0.315, -0.10)], h, True, 0.3)
    stool = _union(_pp([(-0.17, -0.30), (0.12, -0.30), (0.12, -0.27), (-0.17, -0.27)], h), _pp([(-0.13, -0.27), (-0.10, -0.27), (-0.11, 0.0), (-0.14, 0.0)], h),
                   _pp([(0.06, -0.27), (0.09, -0.27), (0.10, 0.0), (0.07, 0.0)], h))
    parts = [torso, thigh, shin, stool]
    hp = [(0.06, -0.935), (0.095, -0.995), (0.155, -1.02), (0.20, -0.99), (0.215, -0.945), (0.20, -0.915), (0.205, -0.87), (0.19, -0.80),
          (0.15, -0.775), (0.11, -0.80), (0.085, -0.85), (0.065, -0.88)]
    if not beard:
        hp = [(0.06, -0.935), (0.095, -0.995), (0.155, -1.02), (0.20, -0.99), (0.212, -0.945), (0.20, -0.92), (0.198, -0.895), (0.18, -0.865),
              (0.15, -0.85), (0.11, -0.86), (0.085, -0.89), (0.065, -0.91)]
    parts.append(_sp(hp, h, True, 0.45))
    parts.append(_sp([(0.12, -0.80), (0.17, -0.80), (0.20, -0.74), (0.17, -0.70), (0.13, -0.73)], h, True, 0.4) if beard else _pp([(0.10, -0.86), (0.17, -0.86), (0.18, -0.78), (0.09, -0.78)], h))
    if hat:
        parts.append(_sp([(0.05, -0.985), (0.09, -1.04), (0.17, -1.07), (0.235, -1.04), (0.245, -1.0), (0.20, -0.985), (0.12, -0.99)], h, True, 0.4))
    parts.append(_sp([(0.00, -0.78), (0.14, -0.77), (0.30, -0.69), (0.45, -0.60), (0.535, -0.585), (0.545, -0.56), (0.45, -0.55), (0.30, -0.575), (0.16, -0.64),
                      (0.05, -0.68)], h, True, 0.4))
    parts.append(_pp([(0.53, -0.585), (0.575, -0.612), (0.58, -0.604), (0.54, -0.575)], h))
    parts.append(_sp([(0.575, -0.608), (0.60, -0.66), (0.615, -0.70), (0.612, -0.655), (0.592, -0.60)], h, True, 0.5))

    def detail(c, col, rim, rimd, rim2, hl):
        rc = rim or "#C58A44"
        _fold(c, [(x * h, y * h) for x, y in ((-0.14, -0.62), (-0.17, -0.50), (-0.16, -0.40))], rc, 0.14, max(1.0, h * 0.003))
        _fold(c, [(x * h, y * h) for x, y in ((0.0, -0.44), (0.20, -0.44), (0.36, -0.43))], rc, 0.12, max(1.0, h * 0.003))
    return _union(*parts), detail


@rfig("writer_seated")
def _f_writer_seated(h):
    """Wartburg: yazı masasına eğilmiş sakallı yazar (profil), sağ elinde tüy kalem. Masa ayrı prop (tabla y=-0.58h, x>=0.3h)."""
    return _writer_build(h, True, False)


@rfig("clerk_seated")
def _f_clerk_seated(h):
    """Sayım odası katibi: berelı, sakalsız, yüksek sıraya eğilmiş (tabla y=-0.58h)."""
    return _writer_build(h, False, True)


def _head_front(h, cx, cy, rx=0.062, ry=0.074):
    return _ellipse(cx, cy, rx, ry, h)


def _headgear(h, kind, cy=-0.86):
    """Önden başlıklar: mitre | kurhut | crown | galero | cap."""
    if kind == "mitre":
        mit = _sp([(-0.078, cy - 0.045), (-0.088, cy - 0.10), (-0.058, cy - 0.185), (-0.012, cy - 0.235), (0.0, cy - 0.248), (0.012, cy - 0.235), (0.058, cy - 0.185), (0.088, cy - 0.10), (0.078, cy - 0.045)], h, True, 0.3)
        band = _pp([(-0.075, cy - 0.04), (0.075, cy - 0.04), (0.07, cy - 0.065), (-0.07, cy - 0.065)], h)
        lap = _union(_pp([(-0.06, cy - 0.04), (-0.085, cy + 0.07), (-0.065, cy + 0.075), (-0.045, cy - 0.04)], h), _pp([(0.06, cy - 0.04), (0.085, cy + 0.07), (0.065, cy + 0.075), (0.045, cy - 0.04)], h))
        return _union(mit, band, lap)
    if kind == "kurhut":
        cap = _sp([(-0.075, cy - 0.04), (-0.083, cy - 0.085), (-0.05, cy - 0.125), (0.0, cy - 0.135), (0.05, cy - 0.125), (0.083, cy - 0.085), (0.075, cy - 0.04)], h, True, 0.4)
        brim = _ellipse(0.0, cy - 0.045, 0.098, 0.028, h)
        top = _ellipse(0.0, cy - 0.14, 0.018, 0.016, h)
        return _union(cap, brim, top)
    if kind == "crown":
        return _pp([(-0.07, cy - 0.04), (-0.075, cy - 0.12), (-0.04, cy - 0.085), (-0.02, cy - 0.15), (0.0, cy - 0.095), (0.02, cy - 0.15), (0.04, cy - 0.085), (0.075, cy - 0.12), (0.07, cy - 0.04)], h)
    if kind == "galero":
        return _union(_ellipse(0.0, cy - 0.06, 0.13, 0.026, h), _sp([(-0.06, cy - 0.06), (-0.05, cy - 0.12), (0.05, cy - 0.12), (0.06, cy - 0.06)], h, True, 0.4))
    return _sp([(-0.07, cy - 0.05), (-0.065, cy - 0.10), (0.0, cy - 0.12), (0.065, cy - 0.10), (0.07, cy - 0.05)], h, True, 0.4)


def _elector(h, gear):
    robe = _sp([(-0.31, 0.0), (-0.295, -0.20), (-0.29, -0.40), (-0.285, -0.52), (-0.24, -0.66), (-0.20, -0.735), (-0.10, -0.775), (0.10, -0.775), (0.20, -0.735),
                (0.24, -0.66), (0.285, -0.52), (0.29, -0.40), (0.295, -0.20), (0.31, 0.0)], h, True, 0.35)
    neck = _pp([(-0.035, -0.81), (0.035, -0.81), (0.04, -0.76), (-0.04, -0.76)], h)
    head = _head_front(h, 0.0, -0.865)
    gearp = _headgear(h, gear)
    hands = _union(_ellipse(-0.115, -0.405, 0.045, 0.030, h), _ellipse(0.115, -0.405, 0.045, 0.030, h))
    sleeve = _union(_sp([(-0.235, -0.70), (-0.285, -0.54), (-0.27, -0.42), (-0.20, -0.40), (-0.18, -0.52), (-0.17, -0.66)], h, True, 0.4),
                    _sp([(0.235, -0.70), (0.285, -0.54), (0.27, -0.42), (0.20, -0.40), (0.18, -0.52), (0.17, -0.66)], h, True, 0.4))

    def detail(c, col, rim, rimd, rim2, hl):
        rc = rim or "#C58A44"
        for dx in (-0.10, 0.0, 0.10):
            _fold(c, [(dx * h, -0.35 * h), ((dx * 1.3) * h, -0.18 * h), ((dx * 1.5) * h, -0.01 * h)], rc, 0.14, max(1.0, h * 0.003))
        _fold(c, [(-0.07 * h, -0.76 * h), (0.0, -0.66 * h), (0.07 * h, -0.76 * h)], rc, 0.18, max(1.0, h * 0.0035))
    return _union(robe, neck, head, gearp, hands, sleeve), detail


for _g in ("mitre", "kurhut", "crown", "galero", "cap"):
    ROOM_FIG["elector_" + _g] = (lambda g: (lambda h: _elector(h, g)))(_g)


@rfig("bishop_standing")
def _f_bishop(h):
    """Önden ayakta piskopos: pelerin (cope), mitre, asa (crozier) tutan kol."""
    cope = _sp([(-0.19, 0.0), (-0.175, -0.25), (-0.165, -0.50), (-0.18, -0.705), (-0.095, -0.775), (0.095, -0.775), (0.18, -0.705), (0.165, -0.50), (0.175, -0.25), (0.19, 0.0)], h, True, 0.35)
    neck = _pp([(-0.03, -0.81), (0.03, -0.81), (0.035, -0.76), (-0.035, -0.76)], h)
    head = _head_front(h, 0.0, -0.845, 0.05, 0.06)
    mit = _headgear(h, "mitre", -0.845)
    staff = _union(_pp([(0.285, 0.0), (0.30, 0.0), (0.30, -1.0), (0.285, -1.0)], h), _sp([(0.285, -1.0), (0.286, -1.06), (0.33, -1.095), (0.375, -1.06), (0.37, -1.00), (0.34, -1.0), (0.345, -1.03), (0.33, -1.045), (0.31, -1.03), (0.30, -1.0)], h, True, 0.5))
    arm = _sp([(0.15, -0.70), (0.26, -0.63), (0.31, -0.58), (0.30, -0.54), (0.23, -0.57), (0.14, -0.62)], h, True, 0.4)
    arm2 = _sp([(-0.15, -0.70), (-0.20, -0.58), (-0.15, -0.50), (-0.11, -0.52), (-0.12, -0.60)], h, True, 0.4)

    def detail(c, col, rim, rimd, rim2, hl):
        rc = rim or "#C58A44"
        for dx in (-0.09, 0.0, 0.09):
            _fold(c, [(dx * h, -0.55 * h), (dx * 1.25 * h, -0.30 * h), (dx * 1.4 * h, -0.02 * h)], rc, 0.14, max(1.0, h * 0.003))
        f_ = max(1.0, h * 0.004)
        c.drawLine(-0.012 * h, -0.76 * h, -0.012 * h, -0.05 * h, skia.Paint(AntiAlias=True, Color=C("#c9962b", 40), StrokeWidth=f_ * 1.6, Style=skia.Paint.kStroke_Style))
        c.drawLine(0.012 * h, -0.76 * h, 0.012 * h, -0.05 * h, skia.Paint(AntiAlias=True, Color=C("#c9962b", 40), StrokeWidth=f_ * 1.6, Style=skia.Paint.kStroke_Style))
    return _union(cope, neck, head, mit, staff, arm, arm2), detail


@rfig("king_kneel")
def _f_king_kneel(h):
    """Diz çökmüş genç kral (profil, sağa bakar, başı hafif eğik; arkada yere yayılan manto)."""
    cloak = _sp([(-0.07, -0.60), (-0.16, -0.50), (-0.30, -0.28), (-0.52, -0.06), (-0.66, 0.0), (-0.10, 0.0), (-0.12, -0.20), (-0.06, -0.40)], h, True, 0.4)
    shin = _sp([(-0.12, -0.06), (0.06, -0.075), (0.10, -0.03), (0.09, 0.0), (-0.30, 0.0), (-0.34, -0.03), (-0.28, -0.07)], h, True, 0.3)
    thigh = _sp([(-0.10, -0.30), (0.06, -0.28), (0.11, -0.12), (0.10, -0.01), (0.02, -0.01), (-0.06, -0.10)], h, True, 0.4)
    torso = _sp([(-0.09, -0.62), (0.0, -0.64), (0.08, -0.60), (0.115, -0.50), (0.10, -0.38), (0.06, -0.29), (-0.10, -0.29), (-0.13, -0.42), (-0.12, -0.55)], h, True, 0.4)
    head = _sp([(-0.01, -0.725), (0.02, -0.775), (0.085, -0.785), (0.13, -0.745), (0.14, -0.71), (0.158, -0.697), (0.14, -0.685), (0.135, -0.65), (0.105, -0.625), (0.055, -0.63), (0.015, -0.66), (-0.015, -0.69)], h, True, 0.45)
    hair = _sp([(-0.025, -0.70), (-0.005, -0.765), (0.045, -0.80), (0.108, -0.795), (0.105, -0.75), (0.04, -0.74), (-0.005, -0.70)], h, True, 0.4)
    neck = _pp([(0.01, -0.67), (0.07, -0.67), (0.08, -0.60), (0.0, -0.60)], h)
    arm = _sp([(0.04, -0.60), (0.12, -0.55), (0.185, -0.49), (0.215, -0.47), (0.215, -0.445), (0.17, -0.45), (0.10, -0.48), (0.03, -0.53)], h, True, 0.4)

    def detail(c, col, rim, rimd, rim2, hl):
        rc = rim or "#C58A44"
        _fold(c, [(-0.12 * h, -0.50 * h), (-0.24 * h, -0.30 * h), (-0.42 * h, -0.10 * h)], rc, 0.18, max(1.0, h * 0.0035))
        _fold(c, [(-0.10 * h, -0.40 * h), (-0.18 * h, -0.20 * h), (-0.34 * h, -0.04 * h)], rc, 0.14, max(1.0, h * 0.003))
    return _union(cloak, shin, thigh, torso, neck, head, hair, arm), detail


def crown_path(h, cx=0.0, cy=0.0, w=0.14, ht=0.08):
    """Sekizgen (Şarlman) tacı: ön görünüm — taban bandı + 5 yaprak/ haç."""
    pts = [(cx - w / 2, cy), (cx - w / 2, cy - ht * 0.55), (cx - w * 0.30, cy - ht * 0.30), (cx - w * 0.22, cy - ht), (cx - w * 0.10, cy - ht * 0.42), (cx, cy - ht * 1.12),
           (cx + w * 0.10, cy - ht * 0.42), (cx + w * 0.22, cy - ht), (cx + w * 0.30, cy - ht * 0.30), (cx + w / 2, cy - ht * 0.55), (cx + w / 2, cy)]
    return _pp(pts, h)


def shaft_polys(box, outer, zw, D, bars_x=(), bar_w=8.0):
    """Pencere açıklığından zemine uzanan ışık demetleri: çubuk aralığı başına bir ekran çokgeni (dışbükey zarf)."""
    k = zw / box.F
    x0, y0, x1, y1 = outer
    X0, Y0, X1, Y1 = (x0 - box.vx) * k, (y0 - box.vy) * k, (x1 - box.vx) * k, (y1 - box.vy) * k
    d = np.array(D, np.float32)
    d = d / np.linalg.norm(d)
    YF = (box.by1 - box.vy) * box.zb / box.F
    cuts = [X0]
    for bx in sorted(bars_x):
        bxw = (bx - box.vx) * k
        cuts += [bxw - bar_w * k / 2, bxw + bar_w * k / 2]
    cuts.append(X1)
    polys = []
    for i in range(0, len(cuts), 2):
        ga, gb = cuts[i], cuts[i + 1]
        if gb - ga < 1.0:
            continue
        pts = []
        for (Xw, Yw) in ((ga, Y0), (gb, Y0), (gb, Y1), (ga, Y1)):
            pts.append(box.screen(Xw, Yw, zw))
            tau = (YF - Yw) / d[1]
            pts.append(box.screen(Xw + tau * d[0], YF, zw + tau * d[2]))
        hull = cv2.convexHull(np.array(pts, np.float32)).reshape(-1, 2)
        polys.append([tuple(map(float, q)) for q in hull])
    return polys


def mat_stripe(base, strip, half_width, edge="#c9962b", ew=5.0):
    """Zemin: |a|<half_width şerit (halı) başka malzeme, kenarında altın bant."""
    ecol = hex3(edge)

    def fn(a, b):
        ab, hb = base(a, b)
        asr, hs = strip(a, b)
        m = (np.abs(a) < half_width)[..., None]
        alb = np.where(m, asr, ab)
        h = np.where(np.abs(a) < half_width, hs, hb)
        band = sstep(ew * 0.5 - np.abs(np.abs(a) - half_width + ew * 1.6), 0.0, 1.5)
        alb = alb * (1 - band[..., None]) + ecol[None, None, :] * band[..., None] * 0.9
        return alb.astype(np.float32), h.astype(np.float32)
    return fn


def mat_carpet(base="#6a1a20", seed=9, pat="#c9962b"):
    col = hex3(base)
    pc = hex3(pat)

    def fn(a, b):
        n1 = noise2d(a, b, 1 / 500.0, seed=seed)
        n2 = noise2d(a, b, 1 / 140.0, seed=seed + 1)
        k = 1 + 0.10 * n1 + 0.06 * n2
        alb = col[None, None, :] * k[..., None]
        rp = (np.abs(((b / 90.0) % 1.0) - 0.5) < 0.05) & (np.abs(a) < 70)
        alb = np.where(rp[..., None], pc[None, None, :] * 0.7, alb)
        h = 0.7 * n2 + 0.4 * n1
        return alb.astype(np.float32), h.astype(np.float32)
    return fn


def mat_hallwall(floor_b, stone="#6c5e4c", pitch=330.0, a0=720.0, nwin=5, w=170.0, h1=250.0, spring=600.0, h3=760.0, seed=4, glow=(1.0, 0.86, 0.60), power=2.2,
                 course=56.0):
    """Yan duvar: kesme taş + periyodik sivri pencereler (emisyonlu cam, çıta). a = duvar boyunca derinlik, b = yükseklik (aşağı +)."""
    st = mat_stone_fine(stone, seed=seed, course=course)
    g = np.array(glow, np.float32)

    def fn(a, b):
        alb, h = st(a, b)
        hf = floor_b - b
        idx = np.floor((a - a0) / pitch)
        valid = (idx >= 0) & (idx < nwin)
        al = (a - a0) - idx * pitch
        x = al - w / 2
        hw = np.full_like(x, w / 2)
        k_ = np.clip((hf - spring) / max(h3 - spring, 1e-3), 0, 1)
        hw = hw * (1 - k_ ** 1.7)
        inside = valid & (np.abs(x) < hw) & (hf > h1) & (hf < h3)
        frame = valid & (np.abs(x) < hw + 16) & (hf > h1 - 16) & (hf < h3 + 12) & ~inside
        mull = inside & ((np.abs(x) < 4.0) | (np.abs(hf - (h1 + spring) / 2) < 3.5) | (np.abs(hf - spring) < 3.5))
        glass = inside & ~mull
        alb = np.where(frame[..., None], alb * 0.55, alb)
        alb = np.where(inside[..., None], np.array([0.05, 0.04, 0.03], np.float32)[None, None, :], alb)
        h = np.where(inside, h - 18.0, np.where(frame, h + 6.0, h))
        shim = 0.82 + 0.18 * noise2d(a, b, 1 / 90.0, seed=seed + 7)
        emit = glass[..., None] * (g[None, None, :] * power * shim[..., None])
        return alb.astype(np.float32), h.astype(np.float32), emit.astype(np.float32)
    return fn


def shaft_polys_x(box, xw, wrect, D, pitch=0.0, n=1):
    """Yan duvardaki pencerelerden (düzlem X=xw) zemine uzanan huzme çokgenleri (her pencere için bir dışbükey zarf)."""
    z0, y0, z1, y1 = wrect
    d = np.array(D, np.float32)
    d = d / np.linalg.norm(d)
    YF = (box.by1 - box.vy) * box.zb / box.F
    polys = []
    for i in range(n):
        pts = []
        for (Zq, Yq) in ((z0 + i * pitch, y0), (z1 + i * pitch, y0), (z1 + i * pitch, y1), (z0 + i * pitch, y1)):
            pts.append(box.screen(xw, Yq, Zq))
            tau = (YF - Yq) / d[1]
            pts.append(box.screen(xw + tau * d[0], YF, Zq + tau * d[2]))
        hull = cv2.convexHull(np.array(pts, np.float32)).reshape(-1, 2)
        polys.append([tuple(map(float, q)) for q in hull])
    return polys


def _sitter(h, hat="beret"):
    torso = _sp([(-0.07, -0.80), (-0.15, -0.70), (-0.18, -0.55), (-0.17, -0.42), (-0.10, -0.38), (0.10, -0.42), (0.16, -0.52), (0.15, -0.64), (0.11, -0.74),
                 (0.06, -0.80)], h, True, 0.45)
    thigh = _sp([(-0.14, -0.46), (0.2, -0.46), (0.38, -0.45), (0.44, -0.40), (0.435, -0.31), (0.36, -0.285), (0.0, -0.30), (-0.14, -0.31)], h, True, 0.3)
    shin = _sp([(0.34, -0.33), (0.435, -0.33), (0.445, -0.05), (0.51, -0.025), (0.515, 0.0), (0.30, 0.0), (0.315, -0.10)], h, True, 0.3)
    head = _sp([(0.03, -0.87), (0.06, -0.93), (0.115, -0.955), (0.165, -0.93), (0.18, -0.89), (0.195, -0.875), (0.18, -0.86), (0.175, -0.83), (0.14, -0.805), (0.09, -0.81),
                (0.05, -0.84)], h, True, 0.45)
    neck = _pp([(0.07, -0.84), (0.14, -0.84), (0.15, -0.77), (0.06, -0.77)], h)
    arm = _sp([(0.05, -0.74), (0.13, -0.62), (0.22, -0.50), (0.245, -0.47), (0.16, -0.47), (0.06, -0.60)], h, True, 0.4)
    parts = [torso, thigh, shin, head, neck, arm]
    if hat == "beret":
        parts.append(_sp([(0.02, -0.915), (0.05, -0.975), (0.14, -0.995), (0.205, -0.955), (0.185, -0.925), (0.10, -0.935)], h, True, 0.4))
    elif hat == "galero":
        parts.append(_union(_ellipse(0.11, -0.94, 0.15, 0.022, h), _sp([(0.05, -0.94), (0.06, -0.99), (0.16, -0.99), (0.17, -0.94)], h, True, 0.4)))
    elif hat == "mitre":
        parts.append(_sp([(0.03, -0.925), (0.05, -1.01), (0.095, -1.085), (0.14, -1.01), (0.175, -0.925)], h, True, 0.25))
    elif hat == "cap":
        parts.append(_sp([(0.04, -0.915), (0.06, -0.975), (0.15, -0.98), (0.185, -0.93)], h, True, 0.4))
    elif hat == "hood":
        parts.append(_sp([(0.0, -0.80), (0.0, -0.93), (0.06, -0.985), (0.14, -0.975), (0.10, -0.90), (0.06, -0.80)], h, True, 0.4))

    def detail(c, col, rim, rimd, rim2, hl):
        rc = rim or "#C58A44"
        _fold(c, [(-0.10 * h, -0.62 * h), (-0.13 * h, -0.50 * h), (-0.11 * h, -0.40 * h)], rc, 0.12, max(1.0, h * 0.003))
    return _union(*parts), detail


for _hn in ("beret", "galero", "mitre", "cap", "hood"):
    ROOM_FIG["sit_" + _hn] = (lambda hn: (lambda h: _sitter(h, hn)))(_hn)


# ═════════════ yol/at/sedye figürleri (road_night) ═════════════
def _limb(pts, w0, w1, h):
    """Çizgi eklemli (omuz-diz-bilek) uzuv: noktalar arası daralan kalınlıkta çokgen. pts birim koordinat."""
    P_ = [(x * h, y * h) for x, y in pts]
    n = len(P_)
    left, right = [], []
    for i in range(n):
        if i == 0:
            dx, dy = P_[1][0] - P_[0][0], P_[1][1] - P_[0][1]
        elif i == n - 1:
            dx, dy = P_[-1][0] - P_[-2][0], P_[-1][1] - P_[-2][1]
        else:
            dx, dy = P_[i + 1][0] - P_[i - 1][0], P_[i + 1][1] - P_[i - 1][1]
        L = math.hypot(dx, dy) or 1.0
        nx, ny = -dy / L, dx / L
        w = (w0 + (w1 - w0) * i / (n - 1)) * h * 0.5
        left.append((P_[i][0] + nx * w, P_[i][1] + ny * w))
        right.append((P_[i][0] - nx * w, P_[i][1] - ny * w))
    pts2 = left + right[::-1]
    if _area(pts2) < 0:
        pts2 = pts2[::-1]
    return sk.smooth_path(pts2, True, 0.25)


@rfig("horse_rider")
def _f_horse_rider(h):
    """Yan görünüş yürüyen at + binici (sağa). h: binicinin tepesine kadar toplam boy."""
    body = _sp([(-0.34, -0.60), (-0.29, -0.655), (-0.10, -0.645), (0.10, -0.62), (0.22, -0.64), (0.30, -0.585), (0.315, -0.47), (0.23, -0.375), (0.0, -0.36),
                (-0.20, -0.38), (-0.325, -0.47)], h, True, 0.45)
    neck = _sp([(0.19, -0.63), (0.26, -0.72), (0.34, -0.83), (0.42, -0.885), (0.455, -0.925), (0.48, -0.88), (0.555, -0.805), (0.605, -0.725), (0.59, -0.685),
                (0.525, -0.695), (0.47, -0.745), (0.41, -0.70), (0.34, -0.60), (0.30, -0.50)], h, True, 0.4)
    legs = _union(
        _limb([(0.27, -0.46), (0.375, -0.28), (0.40, -0.12), (0.43, 0.0)], 0.075, 0.032, h),
        _limb([(0.24, -0.46), (0.225, -0.27), (0.185, -0.11), (0.15, 0.0)], 0.07, 0.03, h),
        _limb([(-0.26, -0.47), (-0.22, -0.31), (-0.34, -0.18), (-0.335, -0.07), (-0.32, 0.0)], 0.085, 0.032, h),
        _limb([(-0.23, -0.47), (-0.16, -0.29), (-0.12, -0.15), (-0.10, -0.04), (-0.07, 0.0)], 0.08, 0.03, h))
    tail = _limb([(-0.33, -0.62), (-0.43, -0.57), (-0.48, -0.42), (-0.47, -0.27)], 0.06, 0.018, h)
    rider = _union(
        _sp([(-0.07, -0.64), (-0.075, -0.78), (-0.03, -0.90), (0.03, -0.935), (0.075, -0.90), (0.085, -0.78), (0.07, -0.65)], h, True, 0.45),
        _ellipse(0.04, -0.975, 0.045, 0.052, h),
        _sp([(-0.04, -0.995), (0.0, -1.03), (0.07, -1.035), (0.12, -1.0), (0.10, -0.985), (0.03, -0.99)], h, True, 0.4),
        _limb([(0.02, -0.66), (0.12, -0.58), (0.115, -0.46), (0.105, -0.38)], 0.07, 0.04, h),
        _limb([(0.04, -0.86), (0.13, -0.80), (0.20, -0.75)], 0.045, 0.03, h),
        _sp([(-0.03, -0.90), (-0.17, -0.82), (-0.30, -0.66), (-0.27, -0.58), (-0.09, -0.68)], h, True, 0.4))

    def detail(c, col, rim, rimd, rim2, hl):
        rc = rim or "#C58A44"
        _fold(c, [(0.27 * h, -0.64 * h), (0.34 * h, -0.78 * h), (0.43 * h, -0.88 * h)], rc, 0.22, max(1.0, h * 0.004))
        _fold(c, [(-0.10 * h, -0.64 * h), (0.05 * h, -0.62 * h), (0.2 * h, -0.62 * h)], rc, 0.16, max(1.0, h * 0.003))
    return _union(body, neck, legs, tail, rider), detail


@rfig("torchbearer")
def _f_torchbearer(h):
    """Yürüyen meşaleci (sağa): pelerin, yükseltilmiş kolda meşale. Meşale ucu: TORCH_TIP."""
    cloak = _sp([(-0.09, -0.80), (0.10, -0.80), (0.14, -0.62), (0.15, -0.42), (0.145, -0.30), (-0.17, -0.30), (-0.16, -0.46), (-0.13, -0.66)], h, True, 0.4)
    head = _union(_ellipse(0.015, -0.875, 0.055, 0.064, h), _sp([(-0.05, -0.86), (-0.04, -0.935), (0.03, -0.955), (0.09, -0.92), (0.05, -0.90), (-0.01, -0.85)], h, True, 0.4))
    neck = _pp([(-0.02, -0.83), (0.05, -0.83), (0.055, -0.78), (-0.03, -0.78)], h)
    legs = _union(_limb([(-0.02, -0.34), (0.08, -0.18), (0.16, -0.02)], 0.09, 0.05, h), _limb([(-0.04, -0.34), (-0.10, -0.18), (-0.15, -0.01)], 0.09, 0.05, h))
    arm = _limb([(0.06, -0.78), (0.17, -0.90), (0.23, -1.00)], 0.07, 0.04, h)
    back_arm = _limb([(-0.08, -0.76), (-0.14, -0.60), (-0.11, -0.46)], 0.07, 0.04, h)
    stick = _union(_pp([(0.225, -0.98), (0.24, -0.98), (0.265, -1.24), (0.25, -1.24)], h), _ellipse(0.258, -1.255, 0.032, 0.04, h))

    def detail(c, col, rim, rimd, rim2, hl):
        rc = rim or "#C58A44"
        _fold(c, [(-0.10 * h, -0.70 * h), (-0.14 * h, -0.50 * h), (-0.15 * h, -0.32 * h)], rc, 0.14, max(1.0, h * 0.003))
    return _union(cloak, head, neck, legs, arm, back_arm, stick), detail


TORCH_TIP = {"torchbearer": (0.262, -1.285)}


@rfig("bearer")
def _f_bearer(h):
    """Sedye taşıyıcısı (sağa): omzunda direk, iki eli direkte, hafif öne eğik."""
    body = _sp([(-0.10, -0.79), (0.10, -0.79), (0.15, -0.60), (0.15, -0.40), (0.13, -0.30), (-0.16, -0.30), (-0.16, -0.46), (-0.14, -0.66)], h, True, 0.4)
    head = _union(_ellipse(0.04, -0.865, 0.055, 0.064, h), _sp([(-0.015, -0.855), (-0.005, -0.93), (0.07, -0.95), (0.115, -0.905), (0.08, -0.89), (0.02, -0.84)], h, True, 0.4))
    neck = _pp([(0.0, -0.82), (0.07, -0.82), (0.075, -0.78), (-0.01, -0.78)], h)
    legs = _union(_limb([(-0.02, -0.34), (0.07, -0.18), (0.14, -0.02)], 0.09, 0.05, h), _limb([(-0.04, -0.34), (-0.09, -0.18), (-0.14, -0.01)], 0.09, 0.05, h))
    arms = _union(_limb([(0.07, -0.76), (0.16, -0.78), (0.21, -0.82)], 0.065, 0.04, h), _limb([(-0.05, -0.76), (0.04, -0.80), (0.10, -0.83)], 0.065, 0.04, h))
    pad = _pp([(-0.13, -0.835), (0.30, -0.835), (0.30, -0.805), (-0.13, -0.805)], h)
    return _union(body, head, neck, legs, arms, pad), None


@rfig("litter")
def _f_litter(h):
    """Kapalı sedye (yandan): iki direk + perdeli kabin + kubbe. h: taşıyıcı boyu; ön/arka taşıyıcılar x=±1.0h."""
    poles = _pp([(-1.12, -0.822), (1.12, -0.822), (1.12, -0.795), (-1.12, -0.795)], h)
    cabin = _sp([(-0.56, -0.78), (-0.56, -0.28), (-0.50, -0.20), (0.50, -0.20), (0.56, -0.28), (0.56, -0.78), (0.0, -0.80)], h, True, 0.18)
    roof = _sp([(-0.62, -0.74), (-0.46, -0.93), (0.0, -0.99), (0.46, -0.93), (0.62, -0.74)], h, True, 0.35)
    hang = _union(_pp([(-0.40, -0.80), (-0.37, -0.80), (-0.37, -0.79), (-0.40, -0.79)], h), _pp([(0.37, -0.80), (0.40, -0.80), (0.40, -0.79), (0.37, -0.79)], h))

    def detail(c, col, rim, rimd, rim2, hl):
        rc = rim or "#C58A44"
        for k in range(8):
            x = (-0.48 + k * 0.137) * h
            c.drawLine(x, -0.74 * h, x + 0.01 * h, -0.30 * h, skia.Paint(AntiAlias=True, Color=C(rc, 60), StrokeWidth=max(1.0, h * 0.004), Style=skia.Paint.kStroke_Style))
        c.drawLine(-0.58 * h, -0.28 * h, 0.58 * h, -0.28 * h, skia.Paint(AntiAlias=True, Color=C("#c9962b", 120), StrokeWidth=max(1.2, h * 0.006), Style=skia.Paint.kStroke_Style))
        c.drawLine(-0.62 * h, -0.74 * h, 0.62 * h, -0.74 * h, skia.Paint(AntiAlias=True, Color=C("#c9962b", 110), StrokeWidth=max(1.2, h * 0.006), Style=skia.Paint.kStroke_Style))
        # püskül
        for k in range(12):
            x = (-0.52 + k * 0.095) * h
            c.drawLine(x, -0.20 * h, x, -0.14 * h, skia.Paint(AntiAlias=True, Color=C("#c9962b", 130), StrokeWidth=max(1.2, h * 0.006), Style=skia.Paint.kStroke_Style))
    return _union(poles, cabin, roof, hang), detail
