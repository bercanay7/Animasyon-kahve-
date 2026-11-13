"""Bölüm 3 özel çekim türleri — c3_ önekli. Ton: kan kırmızısı, gri yağmur."""
import math

import numpy as np
import skia

import icons
import kit_a as K
import shots as SH
import sk
import stage as ST
import stage_c3  # noqa: F401  (c3_sokak sahnesi)
from sk import H, W, clamp, ease_out, lerp, mix, smooth, back_out


@SH.kind("c3_bayram")
def k_c3_bayram(cx, t_flag=0.0, t_date=0.0, t_label=0.0):
    """Villalar yıldönümü bayramı: sancak, flamalar, kıvılcımlar, '23 NİSAN'."""
    f = cx.f
    t = cx.t
    K.bg(f, "blood")
    K.rays(f, "blood", 0.32)
    # flama dizisi (zincir eğrisi)
    n = 17
    for i in range(n):
        u = i / (n - 1)
        x = lerp(-20, W + 20, u)
        y = 110 + 70 * (1 - (2 * u - 1) ** 2)
        a = smooth((t - 0.04 * i) / 0.5)
        col = ("#8E1F26", "#E3B54A", "#F2E6C4")[i % 3]
        sw = math.sin(t * 2.4 + i * 0.7) * 5
        f.poly([(x - 20, y), (x + 20, y), (x + sw, y + 62)], color=col, alpha=0.95 * a)
        f.poly([(x - 20, y), (x + 20, y), (x + sw, y + 62)], style="stroke", sw=2, color="#2A0A0C", alpha=0.7 * a)
    p = skia.Path()
    p.moveTo(-20, 110)
    for i in range(1, 25):
        u = i / 24
        p.lineTo(lerp(-20, W + 20, u), 110 + 70 * (1 - (2 * u - 1) ** 2))
    f.path(p, style="stroke", sw=3.5, color="#C9962B", alpha=0.9)
    # sancak
    fa = cx.amt(t_flag, 0.9)
    if fa > 0:
        K.glow_disc(f, 960, 480, 380, "#FF9A5A", 0.3 * fa)
        f.rect(660, 232 - 10, 600, 14, color="#B88A3A", alpha=fa)
        ST.banner(f, 960, 236, 330 * (0.9 + 0.1 * back_out(fa)), 540, color="#8E1F26", trim="#E3B54A", icon="castle", wave=math.sin(t * 2.2) * 7)
        for sx in (-1, 1):
            f.circle(960 + sx * 308, 236, 14, color="#E3B54A", alpha=fa)
    # kıvılcımlar
    sk.embers(f, t, n=70, rect=(0, 300, W, 780), color="#FFD07A")
    da = cx.amt(t_date, 0.6)
    if da > 0:
        SH.gold_flat(f, "23 NİSAN", 960, 930 + 8 * (1 - da), face="title", size=int(138 * (0.9 + 0.1 * back_out(da))), track=14, alpha=da)
    la = cx.amt(t_label, 0.6)
    if la > 0:
        K.txt(f, "BAYRAM", 960, 1012, face="title_m", size=42, color="#E7D5A0", track=22, alpha=la)
    f.vig(0.6)
