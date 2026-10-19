"""c13_kinds — c13 «İki Kraliçe» özel çekim türleri (Parça 6 sahne yazarı). `scenes_c13.py` içinde import edilir; `@CM.ckind` ile kaydolur.

Dünya koordinatı = nötr kamerada ekran koordinatı (1920×1080). Kamera: `cam=[(çapa, look(wx, wy, z)), …]` (p6_lib.look) ya da `cam=("push", …)`.
Kaynak disiplini: yüz yok (stilize madalya/siluet/simge), şiddet yok (1572, 1559, Blois, Köln'de beden/kan/ceset/oda betimi yok); ekrana yalnız script/brif sözcükleri yazılır.
Sözleşme: rivayet/mit = gravür (siyah-beyaz sepya); belge/olgu/gerçek = renk. İPLİK motifi: p6_lib.thread (ovl) ve `thread=` parametreleri.
Her tür `ovl=` kabul eder. Tüm zamanlar çapalıdır.

Türler
  c13_yetim    : Lorenzo di Piero + Madeleine → Catherine (tarih kartları; ebeveyn çizgileri solar; yalnız iplik uzar)
  c13_turnuva  : turnuva alanı (yan travelling): iki atlı birbirine koşar — çarpışma GÖSTERİLMEZ (çekim kararmayla biter)
  c13_uzlasma  : el sıkışma (uzlaşma) iki sancak arasında
  c13_1572     : gece sokak cephesi + üç tarih kartı (22·23·24 AĞUSTOS); kartlardan geçerken pencere ışıkları söner; «≈3.000 (PARİS, TAHMİN)» kartı sessiz belirir
  c13_onay     : Catherine → iki iplik: «liderler: onaylamıştı» ✓ / «katliam: büyük olasılıkla onaylamamıştı» ?; iplik çatallanır (tarihçiler ayrılır)
  c13_fatura   : mit rayı (gravür): çatal · dondurma · topuk · parfüm · zehir kartları; damgalar renkli (MİT / ANEKDOT)
  c13_balet    : Balet comique (renk = gerçek): saray balesi, dansçı siluetleri, geometrik figürler
  c13_zaman    : zaman çizgisi + vinyetler (1610–1631); iplik sağ kenardan çıkar, kamera boş kalır
  c13_galeri   : Galerie Médicis: tek noktalı perspektifte 24 çerçeve; dolly + Parklar çerçevesinde iplik parıltısı
  c13_harf     : Arapça harf kestirmek (madeni harfler damgalanır)
  c13_gok      : gece göğü: dört ışık, «MEDİCİ» göğe yazılır (kapı)
  st_vekalet   : pano=nave istasyonu: sunakta gelin + BOŞ YER (vekâlet; kral orada değildi)
"""
import math

import numpy as np
import skia

import cilt_anim as FA
import cilt_kinds2 as K2
import cilt_medal as CMD
import cilt_medici as CM
import cilt_oda as OD
import cilt_paper as PP
import cilt_pano as PN
import icons
import p6_lib as L
import sk
from cilt_medici import TH
from p6_lib import INK, P, S, look, ov
from sk import C, H, W, clamp, ease_in, ease_io, ease_out, lerp, mix, smooth

INK_BROWN = "#2A180D"


def _edge(f, p0, p1, k, col="#C8962B", sw=5.0, alpha=1.0, bow=0.0):
    """İki nokta arasında (yukarıdan aşağı eğri) altın bağ; k: ilerleme 0..1."""
    if k <= 0.003:
        return
    path = skia.Path()
    path.moveTo(*p0)
    ym = (p0[1] + p1[1]) / 2
    path.cubicTo(p0[0] + bow, ym, p1[0] + bow, ym, p1[0], p1[1])
    pm = skia.PathMeasure(path, False)
    part = skia.Path()
    pm.getSegment(0, pm.getLength() * ease_out(k, 2), part, True)
    f.path(part, style="stroke", sw=sw * 2.6, color="#000000", alpha=0.16 * alpha, blur=2.0)
    f.path(part, style="stroke", sw=sw, color=col, alpha=0.95 * alpha)


# ═════════════════════════════ c13_yetim ═════════════════════════════
@CM.ckind("c13_yetim")
def k_yetim(cx, a_l=0.0, a_m=0.0, a_c=0.0, a_el=None, a_em=None, d_m=None, d_l=None, a_die=None, seed=51, ovl=None, **_):
    """Soy: LORENZO DI PIERO · MADELEINE → CATHERINE (madalya). a_l/a_m/a_c: düğümler; a_el/a_em: bağlar; d_m/d_l: anne/baba ölüm tarihi kartları; a_die: ebeveyn düğümleri/bağları söner."""
    f, c, cam = L.begin(cx, seed=seed, dress="top")
    t = cx.t
    die = ease_io(clamp((t - cx.at(a_die)) / 1.3)) if a_die is not None else 0.0
    PLp, PMp, CCp = (620, 300), (1300, 300), (960, 610)
    col_edge = mix("#C8962B", "#6A6458", die)
    _edge(f, (PLp[0], PLp[1] + 150), (CCp[0] - 60, CCp[1] - 190), cx.amt(a_el, 0.9) if a_el is not None else 0.0, col=col_edge, bow=-30, alpha=1.0 - 0.45 * die)
    _edge(f, (PMp[0], PMp[1] + 150), (CCp[0] + 60, CCp[1] - 190), cx.amt(a_em, 0.9) if a_em is not None else 0.0, col=col_edge, bow=30, alpha=1.0 - 0.45 * die)
    for (px, py), icon, name, an, dat, dtxt in ((PLp, "shield", "LORENZO DI PIERO", a_l, d_l, "4 MAYIS"), (PMp, "fleur", "MADELEINE", a_m, d_m, "28 NİSAN")):
        k = cx.amt(an, 0.7)
        if k <= 0.003:
            continue
        al = k * (1.0 - 0.62 * die)
        f.circle(px, py, 130, shader=f.rad(px, py, 130, [("#F0D27A", 0.0, int(70 * al)), ("#F0D27A", 1.0, 0)]))
        icons.draw_icon(f, icon, px, py, size=230 * (0.85 + 0.15 * ease_out(k)), metal="gold" if die < 0.5 else "bronze", alpha=al, glow=0.0)
        CM.ink(f, name, px, py + 168, face="title_m", size=34, color=TH.fg, align="c", track=5, alpha=al, emboss=False)
        if dat is not None:
            kd = cx.amt(dat, 0.6)
            if kd > 0.003:
                wd = sk.text_width(dtxt, "title", 42, 5) + 70
                CM.tablet(f, px - wd / 2, py + 196 - (1 - kd) * 8, wd, 76, alpha=kd, corner=8)
                CM.ink(f, dtxt, px, py + 248 - (1 - kd) * 8, face="title", size=42, color=TH.fg, align="c", track=5, alpha=kd, emboss=False)
    kc = cx.amt(a_c, 0.9)
    if kc > 0.003:
        s = 330 * (0.9 + 0.1 * ease_out(kc))
        CMD.draw_medal_b(f, "m_catherine", CCp[0], CCp[1], s, "bronze", False, alpha=kc, tilt=0.12 * math.sin(t * 0.6), inscription=False, shadow=0.55)
        CM.name_plate(f, "CATHERINE", None, "13 NİSAN 1519", cx_=CCp[0], y=CCp[1] + s * 0.50, t=cx.amt(a_c, 0.7, off=0.4), w=470)
    L.end(cx, cam, motes_n=22)
    if ovl:
        ovl(cx)


# ═════════════════════════════ c13_turnuva ═════════════════════════════
def _stand(f, c, x0, x1, y, t, seed):
    """Tribün: ahşap platform + arkada renkli sancaklar; seyirci siluetleri."""
    rs = np.random.RandomState(seed)
    c.drawRect(skia.Rect.MakeLTRB(x0, y - 130, x1, y + 14), P("#6A4426", 255))
    c.drawRect(skia.Rect.MakeLTRB(x0, y - 130, x1, y + 14), S("#2A170B", 2.4, 230))
    for xx in np.arange(x0 + 20, x1, 60):
        c.drawLine(xx, y - 130, xx, y + 14, S("#4A2C16", 1.8, 160))
    for i, xx in enumerate(np.arange(x0 + 30, x1 - 20, 46)):
        h = rs.uniform(52, 74)
        sway = math.sin(t * 2.0 + i * 0.7) * 2.5
        col = ["#2A1A10", "#3A2616", "#4A3220", "#2A2A32"][i % 4]
        c.drawCircle(xx + sway, y - 130 - h * 0.62, 9.5, P(col, 255))
        c.drawRoundRect(skia.Rect.MakeLTRB(xx - 13 + sway, y - 130 - h * 0.55, xx + 13 + sway, y - 130), 7, 7, P(col, 255))
        if i % 5 == 0:
            c.drawLine(xx + sway + 12, y - 130 - h * 0.4, xx + sway + 22, y - 130 - h * 0.95 + math.sin(t * 5 + i) * 4, S(col, 4, 255))


@CM.ckind("c13_turnuva")
def k_turnuva(cx, t_meet=4.4, seed=61, ovl=None, **_):
    """Turnuva alanı: gökyüzü, tribün, bayraklar, ahşap bariyer; iki atlı (soldan sağa / sağdan sola) birbirine dörtnala koşar. Çarpışma GÖSTERİLMEZ:
    atlılar arada ≈380 px kala çekim kesilir (kararma). t_meet: aradaki mesafenin 380 px olduğu an (yerel sn)."""
    import cilt_deniz as DN
    f, c, cam = L.begin(cx, seed=seed, dress=None, bg="clear", clear="#CFE0EC")
    t = cx.t
    f.rect(-800, -400, 4200, 1600, shader=f.lin(0, -400, 0, 760, [("#8FB0D0", 0.0), ("#EAD7B0", 1.0)]))
    for i in range(6):
        f.oval(200 + i * 520, 140 + (i % 3) * 70, 180, 34, color="#FFFFFF", alpha=0.35, blur=12)
    # uzak tepeler
    pts = [(-800, 640)]
    for xx in range(-800, 3000, 150):
        pts.append((xx, 560 + 40 * math.sin(xx / 330.0) + 18 * math.sin(xx / 110.0)))
    pts += [(3000, 700), (-800, 700)]
    c.drawPath(sk.poly_path(pts), P("#9AA880", 255))
    c.drawPath(sk.poly_path(pts, False), S("#4A5A3A", 2, 200))
    # sancak direkleri (arka)
    for i, xx in enumerate((120, 700, 1300, 1900)):
        c.drawLine(xx, 430, xx, 620, S("#4A2C16", 5, 255))
        DN.flag(c, xx + 3, 432, 130, 72, t, shape="swallow", dev=["stripes", "bands", "plain", "stripes"][i], c1=["#2F4A8E", "#B8261A", "#E8C468", "#6A8A4A"][i], c2="#F2E6C2", wind=0.7, ph=i * 1.3)
    _stand(f, c, -200, 2300, 640, t, 3)
    # alan zemini
    f.rect(-800, 640, 4200, 700, shader=f.lin(0, 640, 0, 1100, [("#D8C190", 0.0), ("#B49866", 1.0)]))
    for i in range(30):
        xx = -700 + i * 110
        c.drawLine(xx, 700 + (i * 53) % 330, xx + 40, 700 + (i * 53) % 330 + 4, S("#9A8050", 1.6, 80))
    # bariyer (uzun ahşap çit)
    c.drawRect(skia.Rect.MakeLTRB(-600, 770, 2700, 788), P("#7A5230", 255))
    c.drawRect(skia.Rect.MakeLTRB(-600, 770, 2700, 788), S("#2A170B", 2.0, 230))
    c.drawRect(skia.Rect.MakeLTRB(-600, 832, 2700, 848), P("#7A5230", 255))
    for xx in np.arange(-600, 2700, 120):
        c.drawRect(skia.Rect.MakeLTRB(xx, 760, xx + 18, 920), P("#5A3A1C", 255))
        c.drawRect(skia.Rect.MakeLTRB(xx, 760, xx + 18, 920), S("#2A170B", 1.6, 220))
    # atlılar
    tm = max(0.5, cx.at(t_meet))
    vA = (900 - (-380)) / tm
    xa = -380 + vA * t
    xb = 2300 - (2300 - 1280) / tm * t
    FA.rider(f, xb, 800, 330, t, speed=(2300 - 1280) / tm, gait="gallop", dir=-1, seed=7, prop="spear")
    FA.rider(f, xa, 932, 400, t, speed=vA, gait="gallop", dir=1, seed=3, prop="spear")
    # toz
    for i in range(14):
        ph = (t * 0.9 + i / 14.0) % 1.0
        FA._puff(c, xa - 120 - ph * 220, 930 - ph * 40 - (i % 3) * 10, 22 + 40 * ph, 0.32 * (1 - ph), "#CDB98E")
        FA._puff(c, xb + 100 + ph * 180, 800 - ph * 30, 16 + 26 * ph, 0.26 * (1 - ph), "#CDB98E")
    L.end(cx, cam, motes_n=14)
    if ovl:
        ovl(cx)


# ═════════════════════════════ c13_uzlasma ═════════════════════════════
@CM.ckind("c13_uzlasma")
def k_uzlasma(cx, t_shake=0.4, a_tag=None, seed=67, ovl=None, **_):
    """İki sancak arasında el sıkışma (uzlaşma): solda koyu lapis, sağda toprak kızılı sancak; ortada iki figür (Catherine siluet-giysisi ve bir soylu)."""
    import cilt_deniz as DN
    f, c, cam = L.begin(cx, seed=seed, dress="both")
    t = cx.t
    ts = cx.at(t_shake) if not isinstance(t_shake, (int, float)) else float(t_shake)
    # sancak direkleri
    for xx, c1, dev in ((320, "#2F4A8E", "bands"), (1600, "#A8402A", "stripes")):
        f.rect(xx - 9, 150, 18, 880, shader=f.lin(xx - 9, 0, xx + 9, 0, [("#8A5A32", 0.0), ("#C8925A", 0.5), ("#4A2C16", 1.0)]))
        f.circle(xx, 146, 18, color="#E8C468")
        DN.flag(c, xx + 8, 170, 260, 150, t, shape="rect", dev=dev, c1=c1, c2="#F2E6C2", wind=0.5, ph=xx * 0.01, flipx=1 if xx < 960 else -1)
    FA.handshake(f, "soylu_f", "soylu", 960, 900, 560, t, gap=0.62, t0=ts, seedA=11, seedB=6, robe="#1E1A22")
    L.end(cx, cam, motes_n=22)
    if ovl:
        ovl(cx)


# ═════════════════════════════ c13_1572 ═════════════════════════════
def _facade(c, x0, w, h, y_base, seed, wins, night=True):
    rs = np.random.RandomState(seed)
    col = ["#2A2A3A", "#30303F", "#262634", "#34303A"][seed % 4]
    c.drawRect(skia.Rect.MakeLTRB(x0, y_base - h, x0 + w, y_base), P(col, 255))
    c.drawRect(skia.Rect.MakeLTRB(x0, y_base - h, x0 + w, y_base), S("#14141C", 2.6, 255))
    # çatı
    pth = skia.Path()
    pth.moveTo(x0 - 10, y_base - h)
    pth.lineTo(x0 + w / 2, y_base - h - 70 - rs.randint(0, 40))
    pth.lineTo(x0 + w + 10, y_base - h)
    pth.close()
    c.drawPath(pth, P("#1C1C28", 255))
    c.drawPath(pth, S("#0E0E16", 2.4, 255))
    nx, ny = max(2, int(w // 90)), max(2, int(h // 150))
    for j in range(ny):
        for i in range(nx):
            wx = x0 + 28 + i * (w - 56) / nx + 6
            wy = y_base - h + 50 + j * (h - 120) / ny
            wins.append((wx, wy, (w - 56) / nx - 20, (h - 120) / ny - 48, seed * 100 + j * 10 + i))


@CM.ckind("c13_1572")
def k_1572(cx, cards=(), toll=None, candle=None, n_houses=14, seed=71, ovl=None, **_):
    """Gece sokak cephesi (Paris mimarisi iddiası YOK: genel cephe). cards=[dict(x, big, sub, at, dark=[çapa…])]: tarih kartları cephede asılı; dark: yakınındaki pencerelerin söneceği anlar.
    toll=dict(x, at, text): «≈3.000 (PARİS, TAHMİN)» kartı sessiz belirir. candle=dict(x, y, out): tek mum alevi küçülür ve söner. Şiddet, çan, saat, şafak YOK."""
    f, c, cam = L.begin(cx, bg="clear", clear="#0A0C1A", seed=seed)
    t = cx.t
    f.rect(-800, -400, 7600, 2000, shader=f.lin(0, -400, 0, 900, [("#0A0F2A", 0.0), ("#1A2244", 0.7), ("#241E36", 1.0)]))
    rs = np.random.RandomState(3)
    for i in range(70):
        sx, sy = rs.uniform(-400, 6400), rs.uniform(-200, 380)
        f.circle(sx, sy, rs.uniform(1.2, 2.6), color="#EFE8D0", alpha=0.35 + 0.35 * abs(math.sin(t * 0.7 + i)))
    # cepheler
    wins = []
    x = -200
    seeds = []
    for i in range(n_houses):
        w = 330 + (i * 47) % 130
        h = 560 + (i * 83) % 190
        _facade(c, x, w, h, 940, 3 + i, wins)
        x += w + 18
    # pencereler: ışık
    dark_times = []
    for cd in cards:
        for j, a in enumerate(cd.get("dark", ())):
            dark_times.append((cd["x"], cx.at(a), j))
    for (wx, wy, ww, wh, sd) in wins:
        # kapanma zamanı: en yakın kartın dark listesinden (x mesafesi) seçilir
        tt = 1e9
        for (cxp, tdk, j) in dark_times:
            if abs(wx - cxp) < 420 and (sd % 3 == j % 3 or abs(wx - cxp) < 160):
                tt = min(tt, tdk + (sd % 7) * 0.07)
        lit = 1.0 - ease_io(clamp((t - tt) / 0.6)) if t >= tt else 1.0
        base = 0.95 if (sd % 5) != 0 else 0.25
        a = base * lit
        # pencere çerçevesi
        c.drawRect(skia.Rect.MakeXYWH(wx, wy, ww, wh), P("#0E1020", 255))
        if a > 0.02:
            fl = 0.88 + 0.12 * math.sin(t * 5.3 + sd)
            c.drawRect(skia.Rect.MakeXYWH(wx + 3, wy + 3, ww - 6, wh - 6), P("#F2B35A", int(255 * a * fl)))
            f.circle(wx + ww / 2, wy + wh / 2, ww * 1.1, shader=f.rad(wx + ww / 2, wy + wh / 2, ww * 1.1, [("#F2B35A", 0.0, int(70 * a)), ("#F2B35A", 1.0, 0)]))
        c.drawLine(wx + ww / 2, wy, wx + ww / 2, wy + wh, S("#0E1020", 2.2, 255))
        c.drawLine(wx, wy + wh / 2, wx + ww, wy + wh / 2, S("#0E1020", 2.2, 255))
    # zemin: sokak taşı
    f.rect(-800, 940, 7600, 400, shader=f.lin(0, 940, 0, 1340, [("#2A2630", 0.0), ("#0E0C14", 1.0)]))
    f.line(-800, 940, 7600, 940, color="#4A4658", sw=3, alpha=0.7)
    # tarih kartları
    for cd in cards:
        k = cx.amt(cd["at"], 0.8)
        if k <= 0.003:
            continue
        xc = cd["x"]
        sway = 0.02 * math.sin(t * 1.4 + xc)
        c.save()
        c.translate(xc, 170 - (1 - ease_out(k)) * 160)
        c.rotate(math.degrees(sway))
        w = 700
        for dx in (-w / 2 + 70, w / 2 - 70):
            f.line(dx, -200, dx, 0, color="#6A5438", sw=3, alpha=k)
        CM.tablet(f, -w / 2, 0, w, 230 if cd.get("sub") else 170, alpha=k, corner=12)
        CM.ink(f, cd["big"], 0, 118, face="title", size=CM.fit_size(cd["big"], "title", 86, w - 70, 5), color=TH.fg, align="c", track=5, alpha=k, emboss=False)
        if cd.get("sub"):
            CM.ink(f, cd["sub"], 0, 186, face="cap_i", size=36, color=TH.fg2, align="c", alpha=k, emboss=False)
        c.restore()
    if toll:
        k = cx.amt(toll["at"], 1.4)
        if k > 0.003:
            xc = toll["x"]
            w = 1000
            CM.tablet(f, xc - w / 2, 420 - (1 - k) * 10, w, 190, alpha=k, corner=12)
            CM.ink(f, toll.get("text", "≈3.000"), xc, 540 - (1 - k) * 10, face="cap_b", size=CM.fit_size(toll.get("text", "≈3.000"), "cap_b", 92, w - 70, 3), color=TH.fg, align="c", track=3, alpha=k, emboss=False)
    lit_c = 0.0
    if candle:
        tout = cx.at(candle["out"])
        lit_c = 1.0 - ease_io(clamp((t - tout) / 2.2)) if t >= tout else 1.0
        kk = cx.amt(candle.get("at", 0.0), 0.8)
        if kk > 0.003:
            OD.candle(f, candle["x"], candle["y"], 230, t, seed=9, lit=lit_c, holder=True, halo=1.0)
    L.end(cx, cam, light=CM.candle_light(t, seed, base=(W / 2, 600), r=1500.0, sway=6.0), motes_n=10, k=0.9)
    if ovl:
        ovl(cx)


# ═════════════════════════════ c13_onay ═════════════════════════════
@CM.ckind("c13_onay")
def k_onay(cx, a_med=0.0, a_th1=None, a_th2=None, a_tick=None, a_q=None, a_fork=None, seed=77, ovl=None, **_):
    """Catherine madalyası (ortada) → iki iplik: SOL «LİDERLERİN ÖLDÜRÜLMESİ» ✓ (onaylamıştı), SAĞ «KATLİAM» ? (büyük olasılıkla onaylamamıştı). a_fork: tarihçiler ayrılır (? iplik ikiye çatallanır)."""
    f, c, cam = L.begin(cx, seed=seed, dress="top")
    t = cx.t
    km = cx.amt(a_med, 0.9)
    mx, my = 960, 230
    if km > 0.003:
        CMD.draw_medal_b(f, "m_catherine", mx, my, 270 * (0.9 + 0.1 * ease_out(km)), "bronze", False, alpha=km, tilt=0.10 * math.sin(t * 0.6), inscription=False, shadow=0.5)
    # paneller
    panels = [dict(x=520, y=700, w=700, title="LİDERLERİN ÖLDÜRÜLMESİ", sub="ONAYLAMIŞTI", a=a_th1, at=a_tick, sym="tick", col="#2F6B3A"),
              dict(x=1400, y=700, w=700, title="KATLİAM", sub="BÜYÜK OLASILIKLA ONAYLAMAMIŞTI", a=a_th2, at=a_q, sym="q", col="#A8321E")]
    for pnl in panels:
        kth = cx.amt(pnl["a"], 1.0) if pnl["a"] is not None else 0.0
        if kth > 0.003:
            _edge(f, (mx + (-60 if pnl["x"] < 960 else 60), my + 135), (pnl["x"], pnl["y"] - 190), kth, col="#8E3342" if TH.day else "#F4DE90", sw=4.5, bow=(-80 if pnl["x"] < 960 else 80))
        kp = cx.amt(pnl["a"], 0.7, off=0.6) if pnl["a"] is not None else 0.0
        if kp <= 0.003:
            continue
        CM.tablet(f, pnl["x"] - pnl["w"] / 2, pnl["y"] - 190 + (1 - kp) * 14, pnl["w"], 380, alpha=kp, corner=14)
        CM.ink(f, pnl["title"], pnl["x"], pnl["y"] - 120 + (1 - kp) * 14, face="title_m", size=CM.fit_size(pnl["title"], "title_m", 38, pnl["w"] - 60, 5), color=TH.fg, align="c", track=5, alpha=kp, emboss=False)
        ks = cx.amt(pnl["at"], 0.6) if pnl["at"] is not None else 0.0
        cxs, cys = pnl["x"], pnl["y"] + 10
        if ks > 0.003:
            if pnl["sym"] == "tick":
                u = ease_out(ks, 2.0)
                pts = [(cxs - 60, cys - 6), (cxs - 18, cys + 40), (cxs + 70, cys - 56)]
                f.line(pts[0][0], pts[0][1], lerp(pts[0][0], pts[1][0], clamp(u * 2)), lerp(pts[0][1], pts[1][1], clamp(u * 2)), color=pnl["col"], sw=18, alpha=0.95)
                if u > 0.5:
                    f.line(pts[1][0], pts[1][1], lerp(pts[1][0], pts[2][0], clamp(u * 2 - 1)), lerp(pts[1][1], pts[2][1], clamp(u * 2 - 1)), color=pnl["col"], sw=18, alpha=0.95)
            else:
                sp = CM.engraved("?", "title", 150, 4.0, "#8A1810")
                CM.draw_spr(f, sp, cxs, cys + 52, "c", alpha=ks * (0.85 + 0.15 * math.sin(t * 3)), scale=0.9 + 0.1 * ease_out(ks))
        CM.ink(f, pnl["sub"], pnl["x"], pnl["y"] + 140, face="cap_b", size=CM.fit_size(pnl["sub"], "cap_b", 34, pnl["w"] - 60, 2), color=pnl["col"], align="c", track=2, alpha=kp * cx.amt(pnl["at"], 0.6, off=0.2) if pnl["at"] is not None else 0.0, emboss=False)
    # çatal
    if a_fork is not None:
        k = ease_out(clamp((t - cx.at(a_fork)) / 1.2), 2.0)
        if k > 0.003:
            x0, y0 = 1400, 800
            for sgn in (-1, 1):
                p1 = (x0 + 260 * k, y0 + sgn * 170 * k)
                p2 = (x0 + 470 * k, y0 + sgn * 330 * k)
                pts = [(x0, y0 + 20), (x0 + 120 * k, y0 + sgn * 40 * k), p1, p2]
                f.path(sk.poly_path(L._catmull(pts, 10), False), style="stroke", sw=4.5, color="#8E3342" if TH.day else "#F4DE90", alpha=0.95)
    L.end(cx, cam, motes_n=18)
    if ovl:
        ovl(cx)


# ═════════════════════════════ c13_fatura (mit rayı; gravür) ═════════════════════════════
CARD_W, CARD_H = 270, 440
CARD_X = [360, 660, 960, 1260, 1560]
CARD_Y = 560


def _metal(c, path, x0, x1, a=255, edge="#1E1E22"):
    p = skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(x0, 0), (x1, 0)], [C("#E4E6EA", a), C("#9AA0AA", a), C("#5A5E68", a)], [0, 0.5, 1]))
    c.drawPath(path, p)
    c.drawPath(path, S(edge, 2.4, a))


def _ic_fork(c, x, y, s=1.0, a=255):
    c.save(); c.translate(x, y); c.scale(s, s)
    h = skia.Path()
    h.addRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(-13, -20, 13, 200), 11, 11))
    _metal(c, h, -13, 13, a)
    base = skia.Path()
    base.addRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(-62, -48, 62, -14), 16, 16))
    _metal(c, base, -62, 62, a)
    for i in range(4):
        tx = -48 + i * 32
        t_ = skia.Path()
        t_.addRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(tx - 8, -170, tx + 8, -40), 8, 8))
        _metal(c, t_, tx - 8, tx + 8, a)
    c.restore()


def _ic_ice(c, x, y, s=1.0, a=255):
    c.save(); c.translate(x, y); c.scale(s, s)
    # ayak + sap
    foot = skia.Path(); foot.addOval(skia.Rect.MakeLTRB(-70, 150, 70, 178))
    c.drawPath(foot, P("#B8903A", a)); c.drawPath(foot, S("#3A2A12", 2.2, a))
    c.drawRect(skia.Rect.MakeLTRB(-11, 100, 11, 160), P("#B8903A", a))
    # kase
    bowl = skia.Path()
    bowl.moveTo(-110, 20); bowl.quadTo(-100, 120, 0, 126); bowl.quadTo(100, 120, 110, 20); bowl.close()
    c.drawPath(bowl, skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(-110, 0), (110, 0)], [C("#E8D8B0", a), C("#B8A070", a), C("#7A6840", a)], [0, 0.5, 1])))
    c.drawPath(bowl, S("#3A2A12", 2.4, a))
    for i, (cx_, cy_, r_, col) in enumerate(((-52, 6, 56, "#F6E7B6"), (52, 6, 56, "#E8A8A0"), (0, -52, 58, "#D8C8E0"))):
        c.drawCircle(cx_, cy_, r_, P(col, a)); c.drawCircle(cx_, cy_, r_, S("#5A4A30", 2.0, a))
        c.drawArc(skia.Rect.MakeLTRB(cx_ - r_ * 0.7, cy_ - r_ * 0.7, cx_ + r_ * 0.7, cy_ + r_ * 0.7), 200, 70, False, S("#FFFFFF", 4, int(a * 0.6)))
    c.drawCircle(0, -112, 14, P("#B8261A", a)); c.drawCircle(0, -112, 14, S("#3A0806", 2, a))
    c.restore()


def _ic_heel(c, x, y, s=1.0, a=255):
    c.save(); c.translate(x, y); c.scale(s, s)
    sh = sk.smooth_path([(-104, -40), (-56, -50), (-14, -22), (36, 18), (96, 46), (128, 70), (112, 92), (20, 90), (-48, 92), (-66, 158), (-96, 158), (-98, 60)], True, 0.42)
    c.drawPath(sh, skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(0, -50), (0, 160)], [C("#A8321E", a), C("#6E1810", a)], [0, 1])))
    c.drawPath(sh, S("#2A0806", 3.0, a))
    c.drawLine(-96, 92, 124, 92, S("#1A0806", 6, a))
    c.drawArc(skia.Rect.MakeLTRB(-30, -40, 80, 40), 210, 80, False, S("#E08A70", 4, int(a * 0.7)))
    c.restore()


def _ic_perfume(c, x, y, s=1.0, a=255):
    c.save(); c.translate(x, y); c.scale(s, s)
    body = sk.poly_path([(-78, -10), (-60, -34), (60, -34), (78, -10), (78, 150), (60, 170), (-60, 170), (-78, 150)])
    c.drawPath(body, skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(-78, 0), (78, 0)], [C("#CFE8E4", int(a * 0.9)), C("#7FB8B8", int(a * 0.9)), C("#3A7A86", int(a * 0.9))], [0, 0.5, 1])))
    c.drawPath(body, S("#1E3A40", 2.6, a))
    c.drawRect(skia.Rect.MakeLTRB(-70, 62, 70, 164), P("#F2E6C2", int(a * 0.35)))
    c.drawRoundRect(skia.Rect.MakeLTRB(-46, 78, 46, 128), 6, 6, P("#F6EEDA", a))
    c.drawRoundRect(skia.Rect.MakeLTRB(-46, 78, 46, 128), 6, 6, S("#5A4A30", 1.8, a))
    c.drawRect(skia.Rect.MakeLTRB(-20, -68, 20, -34), P("#B8903A", a)); c.drawRect(skia.Rect.MakeLTRB(-20, -68, 20, -34), S("#3A2A12", 2, a))
    c.drawCircle(0, -98, 34, P("#E8C468", a)); c.drawCircle(0, -98, 34, S("#3A2A12", 2.4, a))
    c.drawArc(skia.Rect.MakeLTRB(-22, -118, 18, -78), 200, 80, False, S("#FFFFFF", 4, int(a * 0.7)))
    c.restore()


def _ic_vial(c, x, y, s=1.0, a=255):
    c.save(); c.translate(x, y); c.scale(s, s)
    fl = skia.Path()
    fl.moveTo(-22, -130); fl.lineTo(-22, -34); fl.cubicTo(-110, 10, -96, 150, 0, 160); fl.cubicTo(96, 150, 110, 10, 22, -34); fl.lineTo(22, -130); fl.close()
    c.drawPath(fl, P("#D8E4DC", int(a * 0.55)))
    c.save(); c.clipPath(fl, skia.ClipOp.kIntersect, True)
    c.drawRect(skia.Rect.MakeLTRB(-120, 30, 120, 170), skia.Paint(Shader=skia.GradientShader.MakeLinear([(0, 30), (0, 170)], [C("#6A9A3A", a), C("#2F5A22", a)], [0, 1])))
    c.restore()
    c.drawPath(fl, S("#1E2A1E", 2.8, a))
    c.drawRoundRect(skia.Rect.MakeLTRB(-26, -166, 26, -126), 6, 6, P("#B8903A", a)); c.drawRoundRect(skia.Rect.MakeLTRB(-26, -166, 26, -126), 6, 6, S("#3A2A12", 2.2, a))
    c.drawArc(skia.Rect.MakeLTRB(-76, 0, -20, 120), 180, 70, False, S("#FFFFFF", 4, int(a * 0.7)))
    c.restore()


ICONS13 = {"fork": _ic_fork, "ice": _ic_ice, "heel": _ic_heel, "perfume": _ic_perfume, "vial": _ic_vial}


@CM.ckind("c13_fatura")
def k_fatura(cx, items=(), a_head=None, stamps=(), mono=1.0, seed=79, ovl=None, **_):
    """Mit rayı (GRAVÜR: sepya; damgalar renkli). items=[dict(label, icon, at)] 5 kart (çatal/dondurma/topuk/parfüm/zehir); label tüy kalemle yazılır.
    stamps=[(metin, kart_i, çapa, rot, boyut, (dx, dy)|None)]: damgalar kartın üstüne/altına çarpar. a_head: «ONUN HANESİ» başlığı."""
    f = cx.f
    t = cx.t
    cam = CM.Cam(cx, push=0.0, drift=(0.0, 0.0))
    L.mono_begin(f, mono)
    CM.bgfill(f, cx, seed=seed, cam=cam, dress="top")
    cam.begin(f)
    c = f.c
    # tezgâh
    f.rect(-300, 800, 2500, 600, shader=f.lin(0, 800, 0, 1100, [("#7A5230", 0.0), ("#3A2410", 1.0)]))
    f.line(-300, 801, 2500, 801, color="#E8C78A", sw=2.4, alpha=0.8)
    if a_head is not None:
        kh = cx.amt(a_head, 0.8)
        if kh > 0.003:
            CM.ink(f, "ONUN HANESİ", 960, 150, face="title", size=64, color=TH.fg, align="c", track=14, alpha=kh, emboss=False)
            CM.flourish_rule(f, 960, 188, 620, alpha=0.8 * kh, color="#7A5A2E", grow=cx.amt(a_head, 1.0, off=0.2))
    quill = None
    for i, it in enumerate(items):
        k = cx.amt(it["at"], 0.6)
        if k <= 0.003:
            continue
        x = CARD_X[i]
        dy = (1 - ease_out(k)) * -160
        pp = PP.paper_image(CARD_W, CARD_H, 20 + i, (240, 230, 200), "deckle", (), 26, 0.7)
        pp.draw(f, x, CARD_Y + dy, rot=0.02 * ((i % 2) * 2 - 1), alpha=k, shadow=0.55)
        c.save()
        c.translate(x, CARD_Y + dy)
        ICONS13[it["icon"]](c, 0, -30, 0.95 * (0.9 + 0.1 * ease_out(k)), int(255 * k))
        c.restore()
        res = K2.write_line(f, cx, it["label"], x, CARD_Y + dy + CARD_H / 2 - 30, cx.at(it["at"]) + 0.15, "fell_i", CM.fit_size(it["label"], "fell_i", 46, CARD_W - 40), INK_BROWN, k, seed=60 + i, align="c")
        if res and 0.0 < res[0] < 1.0:
            quill = (res[1], res[2])
    if quill is not None:
        K2.draw_quill(f, quill[0] + 4, quill[1], ang=-40.0, alpha=1.0, scale=0.8)
    cam.end(f)
    CM.finish(f, cx, motes_n=22)
    L.mono_end(f)
    # damgalar (renkli)
    cam.begin(f)
    for st in stamps:
        txt, ci, at, rot, size = st[:5]
        off = st[5] if len(st) > 5 and st[5] else None
        k = cx.amt(at, 0.3)
        if k <= 0.003:
            continue
        x = CARD_X[ci] + (off[0] if off else 0)
        y = (off[1] if off else (860 if ci % 2 == 0 else 210))
        CM.stamp(f, txt, x, y, rot=rot, size=size, alpha=1.0, t=k)
    cam.end(f)
    if ovl:
        ovl(cx)


# ═════════════════════════════ c13_balet ═════════════════════════════
def _dancer(c, x, y, s, t, ph, col, col2, arms_k):
    sw = math.sin(t * 3.1 + ph)
    hem = 78 + 12 * sw
    skirt = skia.Path()
    skirt.moveTo(x - 24 * s, y - 150 * s)
    skirt.cubicTo(x - 40 * s, y - 90 * s, x - hem * s, y - 50 * s, x - hem * s * 1.05, y)
    skirt.lineTo(x + hem * s * 1.05 + 8 * sw * s, y)
    skirt.cubicTo(x + hem * s + 8 * sw * s, y - 50 * s, x + 40 * s, y - 90 * s, x + 24 * s, y - 150 * s)
    skirt.close()
    c.drawPath(skirt, skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(x, y - 150 * s), (x, y)], [C(col), C(mix(col, "#000000", 0.35))], [0, 1])))
    c.drawPath(skirt, S("#1A0E08", 2.0 * s + 0.6, 235))
    c.drawLine(x - hem * 0.5 * s, y - 6 * s, x - 18 * s, y - 130 * s, S(col2, 1.6, 150))
    c.drawLine(x + hem * 0.5 * s, y - 6 * s, x + 18 * s, y - 130 * s, S(col2, 1.6, 150))
    bod = sk.poly_path([(x - 24 * s, y - 150 * s), (x + 24 * s, y - 150 * s), (x + 18 * s, y - 208 * s), (x - 18 * s, y - 208 * s)])
    c.drawPath(bod, P(col2, 255)); c.drawPath(bod, S("#1A0E08", 1.8 * s + 0.4, 235))
    # kollar
    ang = 0.6 + 0.9 * arms_k * (0.5 + 0.5 * math.sin(t * 3.1 + ph * 0.3))
    for sg in (-1, 1):
        ex, ey = x + sg * (30 + 46 * ang) * s, y - (200 - 28 - 62 * ang) * s
        c.drawLine(x + sg * 18 * s, y - 202 * s, ex, ey, S("#1A0E08", 8 * s + 2, 255))
        c.drawLine(x + sg * 18 * s, y - 202 * s, ex, ey, S(col2, 4.5 * s + 1, 255))
    # boyun + baş (yüz YOK) + tüy
    c.drawRect(skia.Rect.MakeLTRB(x - 5 * s, y - 224 * s, x + 5 * s, y - 206 * s), P("#2A1A10", 255))
    c.drawCircle(x, y - 238 * s, 17 * s, P("#2A1A10", 255))
    pl = skia.Path(); pl.moveTo(x, y - 252 * s); pl.quadTo(x + 22 * s + 6 * sw * s, y - 290 * s, x + 10 * s, y - 318 * s)
    c.drawPath(pl, S(col2, 4 * s + 1, 255))


@CM.ckind("c13_balet")
def k_balet(cx, n=16, form_at=None, seed=91, ovl=None, **_):
    """Saray balesi: mumlu salon, sütunlar, dansçı siluetleri (yüz yok) iki sıra → halka (form_at) geometrik figürleri. Renk = gerçek (gravür değil)."""
    f, c, cam = L.begin(cx, bg="clear", clear="#1A0E12", seed=seed)
    t = cx.t
    f.rect(-600, -300, 3200, 1100, shader=f.lin(0, -300, 0, 800, [("#2A1424", 0.0), ("#4A2230", 0.6), ("#7A3A38", 1.0)]))
    for i, xx in enumerate((160, 640, 1120, 1600, 2080)):
        f.rect(xx - 36, 90, 72, 740, shader=f.lin(xx - 36, 0, xx + 36, 0, [("#C9A060", 0.0), ("#F0D890", 0.4), ("#8A6422", 1.0)]))
        f.rect(xx - 54, 70, 108, 40, color="#E8C468")
        f.rect(xx - 54, 790, 108, 36, color="#B07F22")
    # kemerler
    for xx in (400, 880, 1360, 1840):
        pth = skia.Path(); pth.moveTo(xx - 190, 140); pth.cubicTo(xx - 190, -20, xx + 190, -20, xx + 190, 140)
        c.drawPath(pth, S("#E8C468", 6, 230))
    # mumlar (tavan)
    for i in range(9):
        xx = 120 + i * 240
        PN.glow(c, xx, 150, 150 + 20 * math.sin(t * 5 + i), "#FFB454", 0.35)
        c.drawCircle(xx, 150, 6, P("#FFF1B8", 255))
    # zemin
    f.rect(-600, 800, 3200, 500, shader=f.lin(0, 800, 0, 1200, [("#D8B878", 0.0), ("#7A5230", 1.0)]))
    for i in range(14):
        yy = 800 + (i * i) * 2.4 + i * 5
        c.drawLine(-600, yy, 2600, yy, S("#8A6A3A", 1.6, 120))
    for i in range(-12, 24):
        c.drawLine(960 + i * 150, 800, 960 + i * 360 - 1700, 1200, S("#8A6A3A", 1.4, 90))
    # formasyon
    fk = smooth(clamp((t - cx.at(form_at)) / 2.2)) if form_at is not None else 0.0
    cols = [("#B07F22", "#F0D890"), ("#2F4A8E", "#9AB4E8"), ("#A8321E", "#F0A890"), ("#2F6B4A", "#A8D8A8")]
    order = []
    for i in range(n):
        row = i % 2
        j = i // 2
        xr = 280 + j * ((2000 - 560) / max(1, n / 2 - 1)) * 0.82 + (60 if row else 0)
        yr = 880 if row == 0 else 836
        sr = 1.0 if row == 0 else 0.84
        ang = 2 * math.pi * i / n + t * 0.55
        xc = 960 + math.cos(ang) * 600
        yc = 850 + math.sin(ang) * 62
        sc_ = 0.92 + 0.12 * math.sin(ang)
        x = lerp(xr, xc, fk) + (math.sin(t * 0.9 + i) * 6)
        y = lerp(yr, yc, fk)
        s_ = lerp(sr, sc_, fk)
        order.append((y, x, s_, i))
    order.sort()
    for y, x, s_, i in order:
        col, col2 = cols[i % 4]
        _dancer(c, x, y, s_ * 0.92, t, i * 0.7, col, col2, 0.6 + 0.4 * fk)
    L.end(cx, cam, motes_n=26)
    if ovl:
        ovl(cx)


# ═════════════════════════════ c13_zaman ═════════════════════════════
def _v_clip(c, x, y, w, h, r=14):
    c.save()
    c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x - w / 2, y - h / 2, w, h), r, r), skia.ClipOp.kIntersect, True)


def _v_crown(f, c, x, y, w, h, t, k, **_):
    f.rect(x - w / 2, y - h / 2, w, h, shader=f.lin(0, y - h / 2, 0, y + h / 2, [("#1E2A5A", 0.0), ("#3A2A5A", 1.0)]), alpha=k)
    f.oval(x, y + 80, 120, 22, color="#8A1810", alpha=k)
    f.oval(x, y + 66, 120, 20, color="#B8261A", alpha=k)
    f.circle(x, y - 10, 100, shader=f.rad(x, y - 10, 100, [("#F0D27A", 0.0, int(120 * k)), ("#F0D27A", 1.0, 0)]))
    icons.draw_icon(f, "crown", x, y - 20 + 4 * math.sin(t * 1.6), size=190, metal="gold", alpha=k, glow=0.2 * k)


def _v_crowd(f, c, x, y, w, h, t, k, **_):
    f.rect(x - w / 2, y - h / 2, w, h, shader=f.lin(0, y - h / 2, 0, y + h / 2, [("#6A5A6A", 0.0), ("#2A222E", 1.0)]), alpha=k)
    rs = np.random.RandomState(5)
    for i in range(11):
        xx = x - w / 2 + 30 + i * (w - 60) / 10 + rs.uniform(-6, 6)
        hh = rs.uniform(110, 170)
        yb = y + h / 2 - 8
        sw = math.sin(t * 1.4 + i) * 2
        c.drawCircle(xx + sw, yb - hh - 14, 15, P("#14101A", int(255 * k)))
        c.drawRoundRect(skia.Rect.MakeLTRB(xx - 22 + sw, yb - hh, xx + 22 + sw, yb), 12, 12, P("#14101A", int(255 * k)))
    # yas kurdelesi
    c.drawPath(sk.poly_path([(x + w / 2 - 110, y - h / 2), (x + w / 2 - 70, y - h / 2), (x + w / 2, y - h / 2 + 90), (x + w / 2, y - h / 2 + 130)]), P("#050408", int(235 * k)))


def _v_castle(f, c, x, y, w, h, t, k, **_):
    f.rect(x - w / 2, y - h / 2, w, h, shader=f.lin(0, y - h / 2, 0, y + h / 2, [("#14183A", 0.0), ("#2A2A4A", 1.0)]), alpha=k)
    wy = y - h / 2 + 90
    c.drawRect(skia.Rect.MakeLTRB(x - w / 2, wy, x + w / 2, y + h / 2), P("#4A4A58", int(255 * k)))
    for i in range(7):
        c.drawRect(skia.Rect.MakeLTRB(x - w / 2 + 14 + i * (w - 28) / 7, wy - 30, x - w / 2 + 14 + i * (w - 28) / 7 + 34, wy), P("#4A4A58", int(255 * k)))
    for r_ in range(5):
        yy = wy + 20 + r_ * 38
        c.drawLine(x - w / 2, yy, x + w / 2, yy, S("#2A2A36", 1.6, int(200 * k)))
        for q in range(7):
            xx = x - w / 2 + (q * 62 + (31 if r_ % 2 else 0))
            c.drawLine(xx, yy, xx, yy + 38, S("#2A2A36", 1.4, int(160 * k)))
    c.drawRoundRect(skia.Rect.MakeLTRB(x - 24, y - 20, x + 24, y + 60), 20, 20, P("#0E0E18", int(255 * k)))
    fl = 0.85 + 0.15 * math.sin(t * 5)
    c.drawRoundRect(skia.Rect.MakeLTRB(x - 17, y - 12, x + 17, y + 52), 14, 14, P("#F2B35A", int(240 * k * fl)))
    f.circle(x, y + 20, 70, shader=f.rad(x, y + 20, 70, [("#F2B35A", 0.0, int(80 * k)), ("#F2B35A", 1.0, 0)]))


def _v_window(f, c, x, y, w, h, t, k, out=None, **_):
    f.rect(x - w / 2, y - h / 2, w, h, shader=f.lin(0, y - h / 2, 0, y + h / 2, [("#10142E", 0.0), ("#1E2240", 1.0)]), alpha=k)
    c.drawRect(skia.Rect.MakeLTRB(x - w / 2 + 40, y - h / 2 + 24, x + w / 2 - 40, y + h / 2), P("#3A3A4A", int(255 * k)))
    lit = 1.0 - (out if out is not None else 0.0)
    win = skia.Rect.MakeLTRB(x - 50, y - 90, x + 50, y + 70)
    c.drawRoundRect(win, 50, 50, P("#0A0A14", int(255 * k)))
    fl = (0.85 + 0.15 * math.sin(t * 6)) * lit
    c.drawRoundRect(skia.Rect.MakeLTRB(x - 42, y - 82, x + 42, y + 62), 42, 42, P("#F2B35A", int(235 * k * fl)))
    f.circle(x, y - 10, 120, shader=f.rad(x, y - 10, 120, [("#F2B35A", 0.0, int(90 * k * fl)), ("#F2B35A", 1.0, 0)]))
    c.drawLine(x, y - 82, x, y + 62, S("#0A0A14", 3, int(255 * k)))
    c.drawLine(x - 42, y - 10, x + 42, y - 10, S("#0A0A14", 3, int(255 * k)))


def _v_door(f, c, x, y, w, h, t, k, **_):
    f.rect(x - w / 2, y - h / 2, w, h, shader=f.lin(0, y - h / 2, 0, y + h / 2, [("#3A3040", 0.0), ("#1E1824", 1.0)]), alpha=k)
    arch = skia.Path()
    arch.moveTo(x - 90, y + h / 2); arch.lineTo(x - 90, y - 40); arch.cubicTo(x - 90, y - 150, x + 90, y - 150, x + 90, y - 40); arch.lineTo(x + 90, y + h / 2); arch.close()
    c.drawPath(arch, P("#F2B35A", int(210 * k)))
    c.drawPath(arch, S("#6A5A48", 8, int(255 * k)))
    for sx, hh in ((x - 30, 150), (x + 34, 168)):
        c.drawCircle(sx, y + h / 2 - hh - 14, 15, P("#14101A", int(255 * k)))
        c.drawRoundRect(skia.Rect.MakeLTRB(sx - 24, y + h / 2 - hh, sx + 24, y + h / 2), 13, 13, P("#14101A", int(255 * k)))
    # kapının dışında yalnız siluet (sırtı dönük)
    ox = x - 150 + 6 * math.sin(t * 0.8)
    c.drawCircle(ox, y + h / 2 - 134, 13, P("#0A0810", int(235 * k)))
    c.drawRoundRect(skia.Rect.MakeLTRB(ox - 20, y + h / 2 - 120, ox + 20, y + h / 2), 11, 11, P("#0A0810", int(235 * k)))


def _v_border(f, c, x, y, w, h, t, k, **_):
    f.rect(x - w / 2, y - h / 2, w, h, shader=f.lin(0, y - h / 2, 0, y + h / 2, [("#8A94A8", 0.0), ("#C8BEA0", 1.0)]), alpha=k)
    c.drawRect(skia.Rect.MakeLTRB(x - w / 2, y + 20, x + w / 2, y + h / 2), P("#8A9A6A", int(255 * k)))
    pd = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=5, Color=C("#8E1F26", int(255 * k)), StrokeCap=skia.Paint.kRound_Cap)
    pd.setPathEffect(skia.DashPathEffect.Make([16, 12], -t * 20))
    c.drawLine(x + 30, y - h / 2, x + 30, y + h / 2, pd)
    for yy in (y - 60, y + 60):
        c.drawRect(skia.Rect.MakeLTRB(x + 24, yy - 40, x + 36, yy + 20), P("#4A3A2A", int(255 * k)))
    u = clamp(((t * 0.35) % 1.6) / 1.4)
    px = lerp(x - w / 2 + 40, x + w / 2 + 40, ease_io(u))
    al = k * (1.0 - smooth(clamp((px - (x + 60)) / 80)))
    if al > 0.02:
        c.drawCircle(px, y + h / 2 - 140, 14, P("#14101A", int(255 * al)))
        c.drawRoundRect(skia.Rect.MakeLTRB(px - 20, y + h / 2 - 126, px + 20, y + h / 2 - 20), 11, 11, P("#14101A", int(255 * al)))


VIGN = {"crown": _v_crown, "crowd": _v_crowd, "castle": _v_castle, "window": _v_window, "door": _v_door, "border": _v_border}


@CM.ckind("c13_zaman")
def k_zaman(cx, events=(), y_line=470, head_lead=1100.0, x_exit=None, tail_at=None, tail_speed=900.0, seed=93, ovl=None, **_):
    """Zaman çizgisi + vinyetler. events=[dict(x, date, sub, at, kind, out=çapa|None)]; kind: crown|crowd|castle|window|door|border. İPLİK çizgisi kameranın önünde uzar; tail_at'ten
    sonra çizginin kuyruğu sağa çekilir ve sağ kenardan çıkar, kamera boş kalır. Kamera `cam=[(çapa, look(x,…))]` ile olayları izler."""
    f, c, cam = L.begin(cx, seed=seed, dress=None)
    t = cx.t
    st = getattr(cx, "cam_state", None)
    cen = 960.0 + (st.x / max(0.2, st.zoom) if st is not None else 0.0)
    x_last = max(e["x"] for e in events) if events else 960
    x_exit = x_exit or (x_last + 2600)
    x0 = events[0]["x"] - 900 if events else 200
    head = min(x_exit, cen + head_lead)
    if tail_at is not None and t > cx.at(tail_at):
        x0 = x0 + (t - cx.at(tail_at)) * tail_speed
    if head > x0:
        pts = [(x, y_line + 14 * math.sin(x / 210.0)) for x in np.arange(x0, head + 40, 40)]
        cc = "#F4DE90" if not TH.day else "#8E3342"
        path = sk.poly_path(pts, False)
        c.drawPath(path, S(cc, 16, 36))
        c.drawPath(path, S(cc, 5.2, 245))
    for ev in events:
        k = cx.amt(ev["at"], 0.8, off=-0.6)
        if k <= 0.003:
            continue
        x = ev["x"]
        CM.tablet(f, x - 300, y_line - 330 - (1 - k) * 20, 600, 100, alpha=k, corner=10)
        CM.ink(f, ev["date"], x, y_line - 258 - (1 - k) * 20, face="title", size=CM.fit_size(ev["date"], "title", 50, 540, 5), color=TH.fg, align="c", track=5, alpha=k, emboss=False)
        c.drawLine(x, y_line - 230, x, y_line + 70, S("#6A5A48", 3, int(200 * k)))
        f.circle(x, y_line + 14 * math.sin(x / 210.0), 12, color="#F4DE90", alpha=k)
        vy = y_line + 290
        w, h = 400, 290
        CM.tablet(f, x - w / 2 - 14, vy - h / 2 - 14 + (1 - k) * 24, w + 28, h + 28, alpha=k, corner=14)
        _v_clip(c, x, vy + (1 - k) * 24, w, h)
        outk = ease_io(clamp((t - cx.at(ev["out"])) / 1.6)) if ev.get("out") is not None else 0.0
        VIGN[ev["kind"]](f, c, x, vy + (1 - k) * 24, w, h, t, k, out=outk)
        c.restore()
        if ev.get("sub"):
            sz = CM.fit_size(ev["sub"], "cap_b", 34, 560, 2)
            CM.ink(f, ev["sub"], x, vy + h / 2 + 62, face="cap_b", size=sz, color=TH.fg, align="c", track=2, alpha=k, emboss=False)
    L.end(cx, cam, motes_n=16)
    if ovl:
        ovl(cx)


# ═════════════════════════════ c13_galeri ═════════════════════════════
FOC = 760.0
XW = 430.0
Y_TOP, Y_BOT = -420.0, 310.0
ZEND = 3700.0
VPX, VPY = 960.0, 470.0


def _pj(X, Y, Z, cam):
    cz, cxo, fov = cam
    z = max(60.0, Z - cz)
    k = FOC * fov / z
    return (VPX + (X - cxo) * k, VPY + Y * k)


def _quad(c, pts3, cam, paint):
    pts = [_pj(X, Y, Z, cam) for (X, Y, Z) in pts3]
    c.drawPath(sk.poly_path(pts), paint)
    return pts


def _plane_map(side, z0, z1, y0, y1):
    """Duvar düzlemi: (u,v) → 3B. side: -1 sol duvar, +1 sağ duvar."""
    return lambda u, v: (side * XW, lerp(y0, y1, v), lerp(z0, z1, u))


def _paint_prims(kind, seed):
    """Küçük kompozisyon: (poly(u,v), renk) listesi. Birebir kopya YOK: kodla üretilmiş temsil."""
    rs = np.random.RandomState(seed)
    pal = [("#E8C8A0", "#8A5A38", "#B8402A"), ("#C8D8E0", "#5A7A6A", "#2F4A8E"), ("#F0D890", "#7A6A3A", "#8E1F26"), ("#D8C8D8", "#6A5A6A", "#C8962B"), ("#E0B898", "#5A4A38", "#2F6B4A")][seed % 5]
    prims = []
    if kind == "night":
        prims.append(([(0, 0), (1, 0), (1, 1), (0, 1)], "#10162E"))
        prims.append(([(0.36, 0.16), (0.64, 0.16), (0.64, 0.72), (0.36, 0.72)], "#0A0C18"))
        prims.append(([(0.40, 0.20), (0.60, 0.20), (0.60, 0.68), (0.40, 0.68)], "#F2B35A"))
        prims.append(([(0.48, 0.20), (0.52, 0.20), (0.52, 0.68), (0.48, 0.68)], "#0A0C18"))
        prims.append(([(0.1, 0.8), (0.3, 0.8), (0.28, 1), (0.12, 1)], "#14101A"))
        return prims
    if kind == "sea":
        prims.append(([(0, 0), (1, 0), (1, 0.55), (0, 0.55)], "#BFD8E8"))
        prims.append(([(0, 0.55), (1, 0.55), (1, 1), (0, 1)], "#2F5A8E"))
        prims.append(([(0.15, 0.62), (0.7, 0.62), (0.62, 0.74), (0.2, 0.74)], "#6A4426"))
        prims.append(([(0.42, 0.18), (0.44, 0.18), (0.44, 0.62), (0.42, 0.62)], "#2A170B"))
        prims.append(([(0.44, 0.2), (0.7, 0.34), (0.44, 0.5)], "#F6EEDA"))
        prims.append(([(0.78, 0.5), (1.0, 0.5), (1.0, 0.56), (0.78, 0.56)], "#C8A878"))
        return prims
    if kind == "parcae":
        prims.append(([(0, 0), (1, 0), (1, 1), (0, 1)], "#3A2A4A"))
        prims.append(([(0, 0.0), (1, 0.0), (1, 0.38), (0, 0.38)], "#5A4A6A"))
        for i, x in enumerate((0.22, 0.5, 0.78)):
            prims.append(([(x - 0.12, 1), (x - 0.07, 0.42), (x + 0.07, 0.42), (x + 0.12, 1)], ["#E8E0D0", "#C8B8A0", "#D8D0E0"][i]))
            ang = np.linspace(0, 2 * math.pi, 12)
            prims.append(([(x + 0.05 * math.cos(a), 0.34 + 0.06 * math.sin(a) * 1.4) for a in ang], "#E8C8A0"))
        return prims
    # genel kompozisyon
    prims.append(([(0, 0), (1, 0), (1, 0.6), (0, 0.6)], pal[0]))
    prims.append(([(0, 0.6), (1, 0.6), (1, 1), (0, 1)], pal[1]))
    ang = np.linspace(0, 2 * math.pi, 14)
    sx, sy = rs.uniform(0.2, 0.8), rs.uniform(0.14, 0.3)
    prims.append(([(sx + 0.09 * math.cos(a), sy + 0.06 * math.sin(a)) for a in ang], "#FFF1B8"))
    for j in range(rs.randint(2, 4)):
        x = rs.uniform(0.18, 0.82)
        hgt = rs.uniform(0.34, 0.5)
        prims.append(([(x - 0.11, 0.98), (x - 0.05, 1 - hgt), (x + 0.05, 1 - hgt), (x + 0.11, 0.98)], pal[2] if j % 2 == 0 else pal[1]))
        prims.append(([(x + 0.045 * math.cos(a), 1 - hgt - 0.05 + 0.045 * math.sin(a) * 1.5) for a in ang], "#E8C8A0"))
    return prims


def _draw_painting(c, pmap, prims, cam, alpha=1.0, glow_col=None):
    for poly, col in prims:
        pts = [_pj(*pmap(u, v), cam) for (u, v) in poly]
        c.drawPath(sk.poly_path(pts), P(col, int(255 * alpha)))


def _frame3d(c, pmap, cam, m=0.045, alpha=1.0, dark=0.0, pulse=1.0):
    """Altın çerçeve: dış dörtgen + iç boşluk (tablo ayrı çizilir)."""
    outer = [_pj(*pmap(-m * 0.6, -m), cam), _pj(*pmap(1 + m * 0.6, -m), cam), _pj(*pmap(1 + m * 0.6, 1 + m), cam), _pj(*pmap(-m * 0.6, 1 + m), cam)]
    c.drawPath(sk.poly_path(outer), P("#C79A3C", int(255 * alpha)))
    c.drawPath(sk.poly_path(outer), S("#4A3410", 2.4, int(255 * alpha)))


def _interp_keys(cx, keys, t):
    ks = sorted(((cx.at(a), v) for a, v in keys), key=lambda kv: kv[0])
    if t <= ks[0][0]:
        return ks[0][1]
    if t >= ks[-1][0]:
        return ks[-1][1]
    for (ta, va), (tb, vb) in zip(ks[:-1], ks[1:]):
        if ta <= t <= tb:
            u = ease_io((t - ta) / max(1e-6, tb - ta), 1.6)
            return tuple(lerp(a, b, u) for a, b in zip(va, vb))
    return ks[-1][1]


@CM.ckind("c13_galeri")
def k_galeri(cx, cams=(), a_spark=None, spark_idx=0, dark_at=None, seed=97, ovl=None, **_):
    """Galerie Médicis (temsil): tek noktalı perspektif; iki yan duvarda 10+10 çerçeve, uç duvarda büyük çerçeve. Kamera cams=[(çapa,(z, xoff, fov))] ile dolly.
    a_spark: ilk çerçevede (Parklar) iplik parlaması; dark_at: karanlığa gömülür (çerçeveler yalnız parıltılı kenar). Tablolar kodla üretilmiş küçük kompozisyonlardır (kopya YOK)."""
    f = cx.f
    c = f.c
    t = cx.t
    cam = _interp_keys(cx, cams, t) if cams else (0.0, 0.0, 1.0)
    cz = cam[0]
    f.clear("#1A0E10")
    # tavan
    _quad(c, [(-XW, Y_TOP, cz + 120), (XW, Y_TOP, cz + 120), (XW, Y_TOP, ZEND), (-XW, Y_TOP, ZEND)], cam, P("#3A1E1A", 255))
    for z in np.arange(math.ceil((cz + 120) / 300) * 300, ZEND, 300):
        a_ = _pj(-XW, Y_TOP, z, cam); b_ = _pj(XW, Y_TOP, z, cam)
        c.drawLine(a_[0], a_[1], b_[0], b_[1], S("#6A4426", max(2, 26 * FOC / max(100, z - cz) * 0.05), 230))
    # yan duvarlar
    for side in (-1, 1):
        _quad(c, [(side * XW, Y_TOP, cz + 120), (side * XW, Y_TOP, ZEND), (side * XW, Y_BOT, ZEND), (side * XW, Y_BOT, cz + 120)], cam,
              skia.Paint(AntiAlias=True, Color=C("#8A3E30")))
        _quad(c, [(side * XW, 120, cz + 120), (side * XW, 120, ZEND), (side * XW, Y_BOT, ZEND), (side * XW, Y_BOT, cz + 120)], cam, P("#5A2A20", 255))
    # uç duvar
    _quad(c, [(-XW, Y_TOP, ZEND), (XW, Y_TOP, ZEND), (XW, Y_BOT, ZEND), (-XW, Y_BOT, ZEND)], cam, P("#7A3828", 255))
    # zemin (parke)
    zi = 0
    for z in np.arange(math.floor((cz + 60) / 260) * 260, ZEND, 260):
        for j in range(5):
            x0 = -XW + j * (2 * XW / 5)
            col = "#B89060" if (zi + j) % 2 == 0 else "#8A6A44"
            _quad(c, [(x0, Y_BOT, max(z, cz + 70)), (x0 + 2 * XW / 5, Y_BOT, max(z, cz + 70)), (x0 + 2 * XW / 5, Y_BOT, z + 260), (x0, Y_BOT, z + 260)], cam, P(col, 255)) if z + 260 > cz + 70 else None
        zi += 1
    # çerçeveler: uzaktan yakına
    items = []
    for side in (-1, 1):
        for k in range(10):
            z0 = 280 + k * 340
            items.append((z0, side, k))
    items.sort(reverse=True)
    sp_k = clamp((t - cx.at(a_spark)) / 1.4) if a_spark is not None else 0.0
    for z0, side, k in items:
        if z0 + 210 < cz + 100:
            continue
        pmap = _plane_map(side, z0, z0 + 210, -200, 90)
        kind = "gen"
        seedk = k * 3 + (0 if side < 0 else 11)
        if side < 0 and k == 0:
            kind = "parcae"
        elif side < 0 and k == 4:
            kind = "sea"
        elif side > 0 and k == 5:
            kind = "night"
        _frame3d(c, pmap, cam)
        _draw_painting(c, pmap, _paint_prims(kind, seedk), cam)
        if kind == "parcae" and sp_k > 0:
            # Parklar'ın ipliği: ortadaki figürden köşeye parlayan iplik
            pa = _pj(*pmap(0.52, 0.52), cam)
            pb = _pj(*pmap(0.98, 0.2), cam)
            pc_ = _pj(*pmap(0.76, 0.08), cam)
            path = sk.smooth_path([pa, pc_, pb], False, 0.5)
            pulse = 0.6 + 0.4 * math.sin(t * 8.0)
            c.drawPath(path, S("#F4DE90", 12, int(110 * sp_k * pulse)))
            c.drawPath(path, S("#FFF1B8", 4, int(255 * sp_k)))
            f.circle(pa[0], pa[1], 40 * sp_k, shader=f.rad(pa[0], pa[1], 40 * sp_k, [("#FFF1B8", 0.0, int(200 * sp_k * pulse)), ("#FFF1B8", 1.0, 0)]))
    # uç duvardaki büyük çerçeve
    pm_end = lambda u, v: (lerp(-300, 300, u), lerp(-250, 130, v), ZEND)
    _frame3d(c, pm_end, cam, m=0.05)
    prims = [([(0, 0), (1, 0), (1, 1), (0, 1)], "#E8C474"), ([(0.1, 0.5), (0.9, 0.5), (0.9, 1), (0.1, 1)], "#8A5A38")]
    ang = np.linspace(0, 2 * math.pi, 16)
    prims.append(([(0.5 + 0.22 * math.cos(a), 0.34 + 0.16 * math.sin(a) * 1.3) for a in ang], "#FFF1B8"))
    for x in (0.25, 0.4, 0.55, 0.7):
        prims.append(([(x - 0.07, 0.98), (x - 0.02, 0.58), (x + 0.04, 0.58), (x + 0.08, 0.98)], "#8E1F26" if x < 0.5 else "#2F4A8E"))
    _draw_painting(c, pm_end, prims, cam)
    # karanlık
    dk = ease_io(clamp((t - cx.at(dark_at)) / 2.4)) if dark_at is not None else 0.0
    if dk > 0.003:
        f.rect(0, 0, W, H, color="#04030A", alpha=0.90 * dk)
        pulse = 0.55 + 0.35 * math.sin(t * 2.0)
        for z0, side, k in items:
            if z0 + 210 < cz + 100:
                continue
            pmap = _plane_map(side, z0, z0 + 210, -200, 90)
            pts = [_pj(*pmap(u, v), cam) for (u, v) in ((0, 0), (1, 0), (1, 1), (0, 1))]
            pth = sk.poly_path(pts)
            c.drawPath(pth, S("#E8C468", 6, int(120 * dk * pulse)))
            c.drawPath(pth, S("#FFF1B8", 2.2, int(230 * dk * pulse)))
        pts = [_pj(*pm_end(u, v), cam) for (u, v) in ((0, 0), (1, 0), (1, 1), (0, 1))]
        c.drawPath(sk.poly_path(pts), S("#FFF1B8", 3, int(255 * dk)))
    CM.vig(f, 0.8)
    CM.motes(f, t, n=14, seed=3)
    if ovl:
        ovl(cx)


def frames24(at, x=960, y=880, n=24, n_port=3, step=0.07, out=None):
    """«24 TABLO = 21 + 3»: 24 küçük çerçeve sırayla dolar; 21'i altın, 3'ü bronz (portre)."""
    def fn(cx):
        k0 = L._kk(cx, at, 0.5, out, 0.5)
        if k0 <= 0.003:
            return
        f = cx.f
        gap = 52
        x0 = x - gap * (n - 1) / 2
        for i in range(n):
            k = clamp((cx.t - (cx.at(at) + i * step)) / 0.3)
            if k <= 0.003:
                continue
            port = i >= n - n_port
            xx = x0 + i * gap + (18 if port else 0)
            f.rrect(xx - 17, y - 24 * k, 34, 48 * k, 4, color="#B07F22" if port else "#E8C468", alpha=0.95 * k0)
            f.rrect(xx - 17, y - 24 * k, 34, 48 * k, 4, style="stroke", sw=2, color="#3A2610", alpha=0.9 * k0)
            if port:
                f.circle(xx, y - 4, 7 * k, color="#3A2610", alpha=0.7 * k0)
    return fn


# ═════════════════════════════ c13_harf ═════════════════════════════
_AR_FONT = None


def _ar_font(size):
    global _AR_FONT
    if _AR_FONT is None:
        _AR_FONT = skia.Typeface.MakeFromFile("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
    return skia.Font(_AR_FONT, size)


@CM.ckind("c13_harf")
def k_harf(cx, a_start=0.0, step=0.38, letters="ابتثجحخ", seed=83, ovl=None, **_):
    """Arapça harf kestirmek: tezgâhta madeni harf blokları sırayla damgalanır (kalıp çarpar, kıvılcım); harfler madeni kabartma."""
    f, c, cam = L.begin(cx, seed=seed, dress="both")
    t = cx.t
    t0 = cx.at(a_start)
    f.rect(-300, 760, 2500, 500, shader=f.lin(0, 760, 0, 1100, [("#7A5230", 0.0), ("#3A2410", 1.0)]))
    f.line(-300, 761, 2500, 761, color="#E8C78A", sw=2.4, alpha=0.8)
    n = len(letters)
    bw, bh = 190, 240
    gap = 230
    x0 = 960 - gap * (n - 1) / 2
    for i, ch in enumerate(letters):
        ti = t0 + i * step
        u = clamp((t - ti) / 0.3)
        if t < ti - 0.35:
            continue
        x = x0 + i * gap
        yb = 640
        drop = (1 - ease_out(clamp((t - (ti - 0.35)) / 0.35))) * -220
        # blok
        c.save()
        c.translate(x, yb + drop)
        blk = skia.Path()
        blk.addRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(-bw / 2, -bh / 2, bw / 2, bh / 2), 8, 8))
        c.drawPath(blk, skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(-bw / 2, 0), (bw / 2, 0)], [C("#D8DCE2"), C("#9AA0AA"), C("#5A5E68")], [0, 0.5, 1])))
        c.drawPath(blk, S("#1E1E22", 2.6, 255))
        # kabartma harf
        if u > 0.02:
            fnt = _ar_font(150)
            blob = skia.TextBlob.MakeFromString(ch, fnt)
            wd = fnt.measureText(ch)
            c.drawTextBlob(blob, -wd / 2 + 4, 48 + 5, skia.Paint(AntiAlias=True, Color=C("#0A0A0E", int(200 * u))))
            c.drawTextBlob(blob, -wd / 2, 48, skia.Paint(AntiAlias=True, Color=C("#F4F1E8", int(255 * u))))
            c.drawTextBlob(blob, -wd / 2 - 1.5, 46.5, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.2, Color=C("#5A5E68", int(200 * u))))
        c.restore()
        # kalıp (punch) + kıvılcım
        d = (t - ti)
        if -0.2 < d < 0.18:
            ky = lerp(-220, 0, ease_in(clamp((d + 0.2) / 0.2), 2.0)) if d < 0 else lerp(0, -160, ease_out(clamp(d / 0.18), 2.0))
            c.drawRect(skia.Rect.MakeLTRB(x - 20, yb - 70 + ky - 330, x + 20, yb - 70 + ky), P("#4A4E58", 255))
            c.drawRect(skia.Rect.MakeLTRB(x - 20, yb - 70 + ky - 330, x + 20, yb - 70 + ky), S("#14141A", 2.4, 255))
            c.drawRect(skia.Rect.MakeLTRB(x - 36, yb - 70 + ky - 360, x + 36, yb - 70 + ky - 322), P("#2A2C34", 255))
        if 0.0 <= d < 0.5:
            for q in range(8):
                a = q * 0.785 + i
                r_ = 20 + 150 * d
                c.drawCircle(x + math.cos(a) * r_, yb - 70 + math.sin(a) * r_ * 0.6 - 40 * d, 3.2 * (1 - d * 2), P("#FFD890", int(255 * (1 - d * 2))))
    L.end(cx, cam, motes_n=18)
    if ovl:
        ovl(cx)


# ═════════════════════════════ c13_gok ═════════════════════════════
@CM.ckind("c13_gok")
def k_gok(cx, a_moons=0.0, a_name=None, seed=89, ovl=None, **_):
    """Gece göğü: yıldızlar; ışık yayan disk ve çevresinde dönen dört nokta (dört ışık); `a_name`'de «MEDİCİ» yaldızla göğe yazılır (kapı)."""
    f, c, cam = L.begin(cx, bg="clear", clear="#04050E", seed=seed)
    t = cx.t
    f.rect(-800, -400, 3600, 1800, shader=f.lin(0, -400, 0, 1200, [("#04050E", 0.0), ("#0E1636", 0.65), ("#1E2850", 1.0)]))
    rs = np.random.RandomState(9)
    for i in range(190):
        x, y = rs.uniform(-600, 2500), rs.uniform(-300, 1200)
        r = rs.uniform(0.9, 2.8)
        a = 0.35 + 0.6 * abs(math.sin(t * rs.uniform(0.4, 1.4) + i))
        f.circle(x, y, r, color="#F2ECD6", alpha=a * 0.9)
        if r > 2.3:
            f.line(x - r * 3.4, y, x + r * 3.4, y, color="#F2ECD6", sw=1.0, alpha=0.4 * a)
            f.line(x, y - r * 3.4, x, y + r * 3.4, color="#F2ECD6", sw=1.0, alpha=0.4 * a)
    # disk (bantlı)
    px, py, pr = 700, 460, 120
    km = cx.amt(a_moons, 1.2)
    f.circle(px, py, pr * 2.6, shader=f.rad(px, py, pr * 2.6, [("#F0D890", 0.0, int(60 * km)), ("#F0D890", 1.0, 0)]))
    c.save()
    c.clipPath(skia.Path().addCircle(px, py, pr), skia.ClipOp.kIntersect, True)
    for j, col in enumerate(("#D8B88A", "#B8885A", "#E8D0A0", "#A8785A", "#D8B88A", "#C89868")):
        f.rect(px - pr, py - pr + j * pr / 3, 2 * pr, pr / 3 + 2, color=col)
    f.circle(px - 40, py - 40, pr * 1.2, shader=f.rad(px - 40, py - 40, pr * 1.2, [("#FFFFFF", 0.0, 60), ("#000000", 1.0, 120)]))
    c.restore()
    c.drawCircle(px, py, pr, S("#2A1A0C", 2, 160))
    # dört ışık
    for i, (rr, sp, ph) in enumerate(((220, 1.5, 0.3), (310, 1.0, 2.2), (410, 0.7, 4.0), (520, 0.45, 5.4))):
        ang = ph + t * sp * 0.6
        x = px + math.cos(ang) * rr
        y = py + math.sin(ang) * rr * 0.17
        a = km * clamp((cx.t - cx.at(a_moons) - i * 0.35) / 0.6)
        if a > 0.003:
            f.circle(x, y, 36, shader=f.rad(x, y, 36, [("#FFF1B8", 0.0, int(220 * a)), ("#FFF1B8", 1.0, 0)]))
            f.circle(x, y, 7.5, color="#FFF9E0", alpha=a)
    # MEDİCİ yaldız yazı
    if a_name is not None:
        kn = cx.amt(a_name, 2.2)
        if kn > 0.003:
            sp = CM.gilt("MEDİCİ", "title", 170, 26)
            CM.draw_spr(f, sp, 1210, 820, "c", alpha=min(1.0, kn * 2.0), reveal=clamp(kn * 1.1), glow=0.35 * kn, shadow=0.6)
    L.end(cx, cam, motes_n=10)
    if ovl:
        ovl(cx)


# ═════════════════════════════ st_vekalet (pano=nave istasyonu) ═════════════════════════════
def st_vekalet(ctx, st):
    """Katedral nefi, sunak önü: gelin ve rahip; yanında BOŞ YER (diz minderi, ışık lekesi): kral orada değildi (vekâlet). Yüz iddiası yok (stilize figür)."""
    f, c, t = ctx.f, ctx.c, ctx.t
    x = st["x"]
    yg = 836
    k = clamp((t - ctx.t0) / 1.0) if hasattr(ctx, "t0") else 1.0
    # boş yerin ışık lekesi (nefe vuran huzme)
    pul = 0.8 + 0.2 * math.sin(t * 1.3)
    c.drawOval(skia.Rect.MakeLTRB(x - 330, yg - 34, x - 30, yg + 24), P("#FFE9A8", int(120 * pul)))
    PN.glow(c, x - 180, yg - 40, 260, "#FFE9A8", 0.30 * pul)
    # diz minderi (boş)
    c.drawRoundRect(skia.Rect.MakeLTRB(x - 250, yg - 22, x - 110, yg + 6), 10, 10, P("#8E1F26", 255))
    c.drawRoundRect(skia.Rect.MakeLTRB(x - 250, yg - 22, x - 110, yg + 6), 10, 10, S("#3A0806", 2, 255))
    # gelin + rahip
    FA.actor(f, "soylu_f", x + 40, yg, 262, t, action="idle", dir=-1, seed=14, robe="#F2EAD8", robe2="#D8C8A0")
    FA.actor(f, "rahip", x + 190, yg + 4, 262, t, action="talk", dir=-1, seed=18, prop="book")


# ═════════════════════════════ c13 yardımcı bindirmeler (ovl) ═════════════════════════════
def medal_ovl(key, x, y, size, at, out=None, out_dur=2.4, metal="bronze", name=None, dates=None, alpha=1.0, in_dur=0.8):
    """Madalyayı bindirme olarak çizer (at'ta belirir; out'ta solar). name: isim levhası."""
    def fn(cx):
        k = cx.amt(at, in_dur)
        if out is not None:
            k *= 1.0 - cx.amt(out, out_dur)
        if k <= 0.003:
            return
        CMD.draw_medal_b(cx.f, key, x, y, size * (0.94 + 0.06 * ease_out(k)), metal, False, alpha=alpha * k, tilt=0.10 * math.sin(cx.t * 0.6), inscription=False, shadow=0.5)
        if name:
            CM.name_plate(cx.f, name, None, dates, cx_=x, y=y + size * 0.52, t=k, w=470)
    return fn


def voice_arcs(x, y, at, n=3, out=None, col="#2A180D", size=1.0):
    """Sesler: soldan duvara doğru yayılan yay dizileri (ANEKDOT; kim söylediği bilinmiyor)."""
    def fn(cx):
        k = cx.amt(at, 0.8)
        if out is not None:
            k *= 1.0 - cx.amt(out, 0.6)
        if k <= 0.003:
            return
        c = cx.f.c
        for j in range(n):
            ph = (cx.t * 0.55 + j / n) % 1.0
            r = (70 + 260 * ph) * size
            a = (1.0 - ph) ** 1.2 * k
            p = S(col, 5.0 * size, int(235 * a))
            c.drawArc(skia.Rect.MakeLTRB(x - r, y - r, x + r, y + r), -42, 84, False, p)
            p2 = S("#F4E8C8", 2.0 * size, int(160 * a))
            c.drawArc(skia.Rect.MakeLTRB(x - r, y - r, x + r, y + r), -42, 84, False, p2)
    return fn


def year_run(x, y, at, v0, v1, dur=6.0, size=120, unit=None, out=None, face="title"):
    """Yıl sayacı v0 → v1 (ease_in_out; kayıt: 1533 → 1543)."""
    def fn(cx):
        k0 = cx.amt(at, 0.4)
        if out is not None:
            k0 *= 1.0 - cx.amt(out, 0.5)
        if k0 <= 0.003:
            return
        u = ease_io(clamp((cx.t - cx.at(at)) / dur), 1.8)
        v = int(round(lerp(v0, v1, u)))
        txt = str(v)
        sp = CM.gilt(txt, face, int(size), 6.0) if not TH.day else CM.engraved(txt, face, int(size), 6.0, TH.fg)
        CM.draw_spr(cx.f, sp, x, y, "c", alpha=k0, shadow=0.5)
        if unit:
            CM.ink(cx.f, unit, x, y + 70, face="title_m", size=34, color=TH.acc, align="c", track=12, alpha=k0, emboss=False)
    return fn


def dot_grid(x0, y0, cols, rows, at, step=0.07, r=17, gx=50, gy=50, col="#B33620", out=None, ring="#7A3A24"):
    """Çok sayıda küçük yuvarlak (sayı söylenmez: «çok»): sırayla dolar."""
    def fn(cx):
        base = cx.at(at)
        ko = 1.0 - (cx.amt(out, 0.5) if out is not None else 0.0)
        n = 0
        for j in range(rows):
            for i in range(cols):
                k = clamp((cx.t - (base + n * step)) / 0.35)
                n += 1
                if k <= 0.003:
                    continue
                xx, yy = x0 + i * gx + (gx / 2 if j % 2 else 0), y0 + j * gy
                rr = r * (0.2 + 0.8 * sk.back_out(k))
                cx.f.circle(xx, yy, rr, color=col, alpha=0.92 * ko)
                cx.f.circle(xx, yy, rr, style="stroke", sw=2, color=ring, alpha=0.8 * ko)
                cx.f.circle(xx - rr * 0.28, yy - rr * 0.30, rr * 0.28, color="#FFFFFF", alpha=0.25 * ko)
    return fn


def span13(x0, x1, y, at, l0, l1, at1=None, dur=2.2, size=38, w=360):
    """İki tarihli ince cetvel (23 ARALIK 1588 → 5 OCAK 1589): geniş etiket levhaları."""
    def fn(cx):
        k = ease_io(clamp((cx.t - cx.at(at)) / dur), 1.6)
        if k <= 0.003:
            return
        f = cx.f
        xe = lerp(x0, x1, k)
        f.line(x0, y, xe, y, color="#7A5A2E", sw=7, alpha=0.95)
        f.line(x0, y, xe, y, color="#E8C468", sw=3, alpha=0.95)
        f.line(x0, y - 22, x0, y + 22, color="#7A5A2E", sw=6, alpha=0.95)
        CM.tablet(f, x0 - w / 2, y - 118, w, 74, alpha=min(1.0, k * 6), corner=8)
        CM.ink(f, l0, x0, y - 66, face="title", size=CM.fit_size(l0, "title", size, w - 36, 4), color=TH.fg, align="c", track=4, alpha=min(1.0, k * 6), emboss=False)
        k1 = cx.amt(at1, 0.5) if at1 is not None else clamp((k - 0.95) * 20)
        if k1 > 0.003:
            f.line(x1, y - 22, x1, y + 22, color="#7A5A2E", sw=6, alpha=0.95 * k1)
            CM.tablet(f, x1 - w / 2, y - 118, w, 74, alpha=k1, corner=8)
            CM.ink(f, l1, x1, y - 66, face="title", size=CM.fit_size(l1, "title", size, w - 36, 4), color=TH.fg, align="c", track=4, alpha=k1, emboss=False)
        if k > 0.02:
            f.circle(xe, y, 9, color="#FFF1B8", alpha=0.95 if k < 0.99 else 0.0)
    return fn
