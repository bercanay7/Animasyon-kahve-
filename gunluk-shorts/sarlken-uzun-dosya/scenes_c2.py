"""Bölüm 2 — Taç Satılık (1519–1520). Ton: para altını + koyu yeşil; entrika, sayılar."""
import math

import icons
import kit_a as K
import scenes_lib  # theatre şablonunu kaydeder
import shots as SH
import shots_c2  # noqa: F401  (c2_* özel çekim türleri)
import sk
from shots import shot
from sk import H, W, clamp, ease_out, lerp, smooth, back_out

FRANKFURT = (8.68, 50.11)
AACHEN = (6.08, 50.78)
CALPE = (-5.35, 36.13)
ABYLA = (-5.44, 35.89)
ALMANYA_C = (10.2, 51.0)

# ───────────────────────────── kaplamalar ─────────────────────────────


def _ex_ocak(cx):
    """Çekim başında büyük 'OCAK 1519' → yukarı çıkıp küçülür."""
    f = cx.f
    t = cx.t
    a = smooth((t - 0.15) / 0.6)
    k = smooth((t - cx.at(("c2s1", "dedesi", -0.5))) / 0.8)
    y = 540 + 40 + (150 - 580) * k
    size = int(150 + (62 - 150) * k)
    SH.gold_flat(f, "OCAK 1519", W / 2, y, face="title", size=size, track=size * 0.1, alpha=a)


def _ex_fugger(cx):
    a = cx.amt(("c2s7", "Augsburglu", -0.1), 0.6)
    K.tag(cx.f, "AUGSBURG", 330, 190, alpha=a, size=44, align="l", pad=30)


def _ex_frankfurt(cx, cm, mv):
    K.place(cx.f, cm, FRANKFURT[0], FRANKFURT[1], "FRANKFURT", cx.t, amt=cx.amt(("c2s8", "Frankfurt'ta", -0.25), 0.6), side="r", size=42, r=17)


def _ex_aachen_map(cx, cm, mv):
    f = cx.f
    x, y = cm.ll(*AACHEN)
    ba = cx.amt(("c2s12", "şehri", 0.0), 0.6)
    K.beacon(f, x, y, cx.t, amt=ba, color="#F0D27A", r=17)
    ta = cx.amt(("c2s12", "Aachen'de", -0.1), 0.5)
    if ta > 0:
        K.tag(f, "AACHEN", x + 44, y + 16, alpha=ta, size=42, align="l", pad=24)
    ma = cx.amt(("c2s12", "Şarlman'ın", -0.1), 0.8)
    if ma > 0:
        SH.draw_medal(f, K.mkey("sarlman", "maksimilyan"), 1500, 520, 400 * (0.94 + 0.06 * ease_out(ma)), "silver", alpha=ma, inscription=False, tilt=0.12 * math.sin(cx.t * 0.7))
        SH.name_plate(f, "ŞARLMAN", None, None, cx_=1500, y=H * 0.69, t=cx.amt(("c2s12", "Şarlman'ın", 0.2), 0.5), w=420)


def _counter_overlay(cx):
    """850.000 FLORİN sayacı (sayım odası üstünde)."""
    f = cx.f
    t = cx.t
    t_y = cx.at(("c2s6", "yaklaşık", -0.15))
    t_n = cx.at(("c2s6", "850.000", -0.1))
    a = smooth((t - t_y) / 0.5)
    if a <= 0:
        return
    f.rect(0, 640, W, 440, shader=f.lin(0, 640, 0, H, [("#000000", 0.0, 0), ("#000000", 1.0, int(205 * a))]))
    K.txt(f, "yaklaşık", W / 2, 800, face="cap_i", size=48, color="#E7D5A0", alpha=a)
    v = 850000 * ease_out(clamp((t - t_n) / 1.3), 3)
    SH.gold_flat(f, SH.fmt_int(v), W / 2, 930, face="title", size=150, track=8, alpha=a)
    ua = smooth((t - cx.at(("c2s6", "florini", -0.15))) / 0.5)
    K.txt(f, "FLORİN", W / 2, 1010, face="title_m", size=48, color="#E0C682", track=16, alpha=ua)


def _vote_overlay(cx):
    na = smooth((cx.t - cx.at(("c2s8", "verdi", -0.15))) / 0.45)
    if na > 0:
        f = cx.f
        f.rect(0, 700, W, 380, shader=f.lin(0, 700, 0, H, [("#000000", 0.0, 0), ("#000000", 1.0, int(215 * na))]))
        sc = 0.85 + 0.15 * back_out(na)
        SH.gold_flat(f, "7 / 7", W / 2, 960, face="title", size=int(170 * sc), track=14, alpha=na)


def _aachen_overlay(cx):
    pass


# Almanya çevresinde yedi seçmen şapkası
def _ring(i, n=7, cx_=ALMANYA_C[0], cy=ALMANYA_C[1], rx=8.8, ry=4.6):
    a = -math.pi / 2 + i * 2 * math.pi / n
    return (cx_ + rx * math.cos(a), cy + ry * math.sin(a))


GER_HATS = [_ring(i) for i in range(7)]


def _toward(p, frac=0.74):
    return (p[0] + (ALMANYA_C[0] - p[0]) * frac, p[1] + (ALMANYA_C[1] - p[1]) * frac)


def _ex_riv(cx, cm, mv):
    f = cx.f
    SH.stamp(f, "RİVAYET", W - 330, 195, rot=-0.1, size=64, t=cx.amt(("c2s14", "Rivayete", -0.05), 0.3))
    t = cx.t
    t_p = cx.at(("c2s14", "Herkül", -0.1))
    t_z = cx.at(("c2s14", "silerek", -0.2))
    pa = smooth((t - t_p) / 0.7) * (1 - smooth((t - t_z) / 1.2))
    if pa > 0:
        for (ll, dx, dy) in ((CALPE, 170, -130), (ABYLA, -170, 130)):
            x, y = cm.ll(*ll)
            px, py = x + dx, y + dy
            f.line(x, y, px - dx * 0.25, py - dy * 0.25, color="#E3B54A", sw=2.5, alpha=0.85 * pa)
            f.circle(x, y, 7, color="#F0D27A", alpha=pa)
            K.glow_disc(f, px, py, 190, "#F0D27A", 0.3 * pa)
            icons.draw_icon(f, "c2_sutun", px, py - 18 * (1 - pa), size=270 * (0.85 + 0.15 * back_out(pa)), metal="gold", alpha=pa, glow=0.25 * pa)
    # deviz bandı: NON PLUS ULTRA → NON silinir
    ba = smooth((t - cx.at(("c2s14", "daha", -0.12))) / 0.7)
    if ba > 0:
        yb = 905
        K.ribbon(f, W / 2, yb - 14 * (1 - ba), 1180, 128, alpha=ba)
        sz = 66
        face, tr_ = "title", 14
        w_non = sk.text_width("NON ", face, sz, tr_)
        w_pu = sk.text_width("PLUS ULTRA", face, sz, tr_)
        tot = w_non + w_pu
        x0 = W / 2 - tot / 2
        kk = clamp((t - cx.at(("c2s14", "silerek", -0.1))) / 0.55)          # üstü çizilir
        gone = smooth((t - cx.at(("c2s14", "tersini", -0.15))) / 0.7)        # NON kaybolur, PLUS ULTRA ortalanır
        xp = lerp(x0 + w_non, W / 2 - w_pu / 2, gone)
        if gone < 1:
            f.text("NON", x0, yb + 24 + 2, face=face, size=sz, color="#2A1A0C", align="l", track=tr_, alpha=ba * (1 - gone))
            K.strike(f, x0 - 6, x0 + sk.text_width("NON", face, sz, tr_) + 6, yb - 2, kk, color="#B02A2A", sw=9, alpha=ba * (1 - gone))
        f.text("PLUS ULTRA", xp, yb + 24 + 2, face=face, size=sz, color="#2A1A0C", align="l", track=tr_, alpha=ba)
        if gone > 0:
            K.glow_disc(f, W / 2, yb, 420, "#F0D27A", 0.3 * gone)
        ta = ba * (1 - gone)
        K.txt(f, "DAHA ÖTESİ YOK", W / 2, yb + 108, face="cap_i", size=40, color="#D9C795", alpha=ta * smooth((t - cx.at(("c2s14", "ötesi", -0.1))) / 0.4))
        tb = smooth((t - cx.at(("c2s14", "söyledi", -0.5))) / 0.6)
        K.txt(f, "DAHA ÖTEYE", W / 2, yb + 108, face="cap_i", size=44, color="#F3DE9A", alpha=tb)


ROTA_BATI = [(-5.7, 36.0), (-9.0, 35.8), (-14.0, 35.4), (-22.0, 34.4), (-32.0, 32.8)]

# ───────────────────────────── çekim listesi ─────────────────────────────
SHOTS = [
    # s1 — Ocak 1519, Maksimilian ölür
    shot("a_g_medal", a=0.0, tr=("fade", 0.9), key="maksimilyan", metal="onyx", name="MAKSİMİLYAN", role="Şarlken'in dedesi", pos="c", size=640,
         at=("c2s1", "dedesi", -0.4), plate_at=("c2s1", "Maksimilian", -0.1), extra=_ex_ocak, label="maksimilyan_oldu"),
    # s2 — taç kalıtsal değil; yedi seçmen
    shot("c2_yedi_koltuk", a=("c2s2", -0.2), tr=("fade", 0.8), mode="intro", t_crown=("c2s2", "İmparatorluğun", -0.1), t_fam=("c2s2", "kalıtsal", -0.2), t_cross=("c2s2", "değildi", -0.15),
         t_hats=("c2s2", "Yedi", -0.1), t_label=("c2s2", "Yedi", -0.05), t_pulse=("c2s2", "karar", -0.05), label="yedi_secmen"),
    # s3 — rakip: I. François
    shot("a_medals", a=("c2s3", -0.2), tr=("fade", 0.8), size=470, y=H * 0.44, gap=660, bgname="green", vs=("c2s3", "François", -0.15),
         items=[dict(key="karl_genc", name="ŞARLKEN", role="Kastilya ve Aragon Kralı", at=0.1, pw=620),
                dict(key="fransuva", name="I. FRANÇOIS", role="Fransa Kralı", metal="royal", at=("c2s3", "Fransa", -0.15), pw=620)], label="karl_fransuva"),
    # s4 — VIII. Henry: gösteri
    shot("c2_gosteri", a=("c2s4", -0.2), tr=("fade", 0.8), t_h=("c2s4", "İngiltere", -0.1), t_plate=("c2s4", "Henry", -0.1), t_show=("c2s4", "gösteriydi", -0.15), label="henry_gosteri"),
    # s5 — oylar pazarlık konusu
    shot("c2_terazi", a=("c2s5", -0.2), tr=("fade", 0.7), t_scale=0.1, t_votes=("c2s5", "Oylar", -0.05), t_coins=("c2s5", "açıkça", -0.15), label="terazi_pazarlik"),
    # s6 — 850.000 florin: sayım odası
    shot("a_theatre", a=("c2s6", -0.2), tr=("fade", 0.8), scene="counting_house",
         p=dict(coins=0.95, coins_t=(K.rel(("c2s6", "yaklaşık", 0.0), ("c2s6", -0.2)), K.rel(("c2s6", "florini", 0.0), ("c2s6", -0.2))), clerks=3, chandelier=True),
         cams=[(0.0, (960, 560, 1.0)), (("c2s6", "yaklaşık", 0.0), (960, 740, 1.45))], overlay=_counter_overlay, label="sayim_odasi_850bin"),
    # s7 — yaklaşık 543.000 florin Fugger'den
    shot("c2_pay", a=("c2s7", -0.2), tr=("fade", 0.8), t_bar=0.2, t_third=("c2s7", "üçte", -0.1), t_lab=("c2s7", "yaklaşık", -0.15), t_num=("c2s7", "543.000", -0.1), t_unit=("c2s7", "florin", -0.1), label="fugger_payi"),
    shot("a_g_medal", a=("c2s7", "Augsburglu", -0.35), tr=("fade", 0.8), key="fugger", metal="bronze", name="JAKOB FUGGER", role="bankacı", pos="c", size=640,
         at=0.0, plate_at=("c2s7", "Jakob", -0.1), extra=_ex_fugger, label="fugger"),
    # s8 — 28 Haziran 1519, Frankfurt: 7/7
    shot("a_map", a=("c2s8", -0.2), tr=("fade", 0.8), cams=[(0.0, (9.5, 50.8, 2.6)), (("c2s8", "Frankfurt'ta", -0.1), (8.68, 50.11, 9.0))],
         regions=[dict(name="almanya", color="#C9962B", at=0.2, alpha=0.15)], date=("28 HAZİRAN 1519", ("c2s8", "28", -0.1)), extra=_ex_frankfurt, label="frankfurt_harita"),
    shot("a_theatre", a=("c2s8", "yedi", -0.3), tr=("fade", 0.7), scene="electors_hall",
         p=dict(seats=7, occupied=True, light_t=(K.rel(("c2s8", "yedi", -0.1), ("c2s8", "yedi", -0.3)), K.rel(("c2s8", "verdi", 0.1), ("c2s8", "yedi", -0.3)))),
         cams=[(0.0, (960, 540, 1.0)), (("c2s8", "ona", -0.2), (960, 620, 1.45))], overlay=_vote_overlay, label="yedi_oy"),
    # s9 — bazı tarihçilere göre: parayı aldı ama kararı Almanya için en iyi yönde verdi
    shot("c2_para", a=("c2s9", -0.2), tr=("fade", 0.8), t_stamp=("c2s9", "Bazı", -0.05), t_coins=("c2s9", "seçmenler", 0.0), t_take=("c2s9", "aldı", -0.1), label="parayi_aldi"),
    shot("a_map", a=("c2s9", "ama", -0.3), tr=("fade", 0.8), cams=[(0.0, (ALMANYA_C[0], ALMANYA_C[1], 1.8)), (("c2s9", "verdi", 0.3), (ALMANYA_C[0], ALMANYA_C[1], 1.95))],
         regions=[dict(name="almanya", color="#9A7222", at=("c2s9", "Almanya", -0.2), alpha=0.6)],
         labels=[dict(text="ALMANYA", lon=ALMANYA_C[0], lat=ALMANYA_C[1], size=76, track=26, color="#F8EBC0", at=("c2s9", "Almanya", -0.1))],
         icons_=[dict(kind="c2_kurhut", lon=GER_HATS[i][0], lat=GER_HATS[i][1], size=124, at=("c2s9", "ama", -0.2 + 0.07 * i), metal="crimson", glow=0.45) for i in range(7)],
         routes=[dict(pts=[GER_HATS[i], _toward(GER_HATS[i])], at=("c2s9", "yönde", -0.15 + 0.09 * i), dur=0.8, color="#F0D27A", width=5) for i in range(7)],
         approx=False, label="almanya_icin_en_iyi"),
    # s10 — rüşvet tartışmalı, borç gerçekti
    shot("c2_borc_terazi", a=("c2s10", -0.2), tr=("fade", 0.8), t_scale=0.1, t_rus=("c2s10", "Rüşvetin", -0.1), t_tart=("c2s10", "tartışmalı", -0.1), t_borc=("c2s10", "borç", -0.15),
         t_gercek=("c2s10", "gerçekti", -0.15), t_crown=("c2s10", "imparator,", -0.1), t_chain=("c2s10", "takmadan", 0.0), label="rusvet_borc"),
    # s11 — yazılı söz
    shot("a_g_doc", a=("c2s11", -0.2), tr=("fade", 0.8), title="YAZILI SÖZ · 1519", w=1240, h=520, size=54, head_size=62, at=0.0, align="c", tone="#CDB886",
         lines=[("Prenslerin ayrıcalıklarına saygı gösterilecek.", ("c2s11", "prenslerin", -0.1)), ("Birlikte yönetecek bir konsey kurulacak.", ("c2s11", "imparatorluğu", -0.1))],
         seal=True, seal_at=("c2s11", "kuracaktı", 0.0), label="yazili_soz"),
    # s12 — 23 Ekim 1520, Aachen
    shot("a_map", a=("c2s12", -0.2), tr=("fade", 0.8), cams=[(0.0, (6.5, 50.4, 3.6)), (("c2s12", "Şarlman'ın", 0.3), (6.08, 50.78, 7.2))],
         regions=[dict(name="almanya", color="#C9962B", at=0.3, alpha=0.2)], date=("23 EKİM 1520", ("c2s12", "23", -0.1)), extra=_ex_aachen_map, label="aachen_harita"),
    shot("a_theatre", a=("c2s12", "tacını", -0.2), tr=("zoom", 0.8), scene="aachen",
         p=dict(crown_t=(0.15, 2.2), crown_show=True, figure=True, bishops=True, attend=True),
         cams=[(0.0, (960, 560, 1.0)), (("c2s12", "taktı", -0.3), (980, 720, 1.8))], label="aachen_taç"),
    # s13 — Plus ultra
    shot("c2_plus_ultra", a=("c2s13", "Plus", -0.3), tr=("fade", 0.7), t_pillars=0.0, t_motto=("c2s13", "Plus", -0.1), t_sub=("c2s13", "Daha", -0.1), label="plus_ultra"),
    # s14 — Herkül Sütunları'nda "non plus ultra" → "non" silinir
    shot("a_map", a=("c2s14", -0.2), tr=("fade", 0.8),
         cams=[(0.0, (-5.4, 36.1, 7.0)), (("c2s14", "silerek", -0.2), (-5.4, 36.1, 7.0)), (("c2s14", "söyledi", 0.35), (-14.5, 35.2, 3.0))],
         routes=[dict(pts=ROTA_BATI, at=("c2s14", "silerek", 0.3), dur=1.4, color="#F0D27A", width=7)],
         icons_=[dict(kind="ship", lon=-5.7, lat=36.0, size=84, at=("c2s14", "silerek", 0.3), route=ROTA_BATI, move_at=("c2s14", "silerek", 0.3), move_dur=1.4, metal="gold")],
         extra=_ex_riv, approx=False, label="herkul_sutunlari"),
]
