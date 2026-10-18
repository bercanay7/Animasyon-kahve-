"""Bölüm 10 — Faturayı Kim Ödedi? (1519–1557). Ton: soğuk gümüş-yeşil, defter."""
import math

import icons
import kit_a as K
import scenes_lib  # theatre şablonunu kaydeder
import shots as SH
import shots_c10  # noqa: F401  (c10_* özel çekim türleri)
import sk
from shots import shot
from sk import H, W, clamp, ease_out, lerp, smooth, back_out

VENEZUELA_C = (-66.0, 7.6)


# ───────────────────────────── kaplamalar ─────────────────────────────
def _counting_overlay(cx):
    f = cx.f
    t = cx.t
    a = smooth((t - cx.at(("c10s5", "bankerler", -0.1))) / 0.5)
    K.tag(f, "BANKERLER", W / 2, 190, alpha=a, size=50, pad=40, edge="#9FB8B4")
    b = smooth((t - cx.at(("c10s5", "1523'te", -0.1))) / 0.5)
    if b > 0:
        f.rect(0, 700, W, 380, shader=f.lin(0, 700, 0, H, [("#000000", 0.0, 0), ("#000000", 1.0, int(205 * b))]))
        SH.gold_flat(f, "1523", W / 2, 975 + 6 * (1 - b), face="title", size=int(150 * (0.92 + 0.08 * back_out(b))), track=18, alpha=b)


def _ex_venezuela(cx, cm, mv):
    f = cx.f
    t = cx.t
    a = cx.amt(("c10s7", "Welser'ler", -0.15), 0.8)
    if a > 0:
        SH.draw_medal(f, K.mkey("welser", "fugger"), 290, 520, 370 * (0.94 + 0.06 * ease_out(a)), "bronze", alpha=a, inscription=False, tilt=0.12 * math.sin(t * 0.6))
        SH.name_plate(f, "WELSER'LER", "banker ailesi", None, cx_=290, y=H * 0.725, t=cx.amt(("c10s7", "Welser'ler", 0.1), 0.5), w=500)
    va = cx.amt(("c10s7", "Venezuela'da", -0.15), 0.6)
    if va > 0:
        x, y = cm.ll(*VENEZUELA_C)
        K.beacon(f, x, y, t, amt=va, color="#5FA89A", r=15)
        K.tag(f, "VENEZUELA", x + 42, y + 16, alpha=va, size=44, align="l", pad=26, edge="#9FB8B4")
    ya = cx.amt(("c10s7", "yönetim", -0.1), 0.6)
    if ya > 0:
        wd = 640
        yy = 940 - 10 * (1 - ya)
        SH.plate(f, W / 2 - wd / 2 + 150, yy - 70, wd, 112, alpha=ya, corner=18, edge="#9FB8B4")
        icons.draw_icon(f, "scroll", W / 2 - wd / 2 + 150 + 80, yy - 14, size=88, metal="silver", alpha=ya, shadow=False)
        f.text("YÖNETİM HAKKI", W / 2 + 150 + 40, yy + 8, face="title_m", size=42, color="#DCE8E6", align="c", track=8, alpha=ya, shadow=(2, 2, 3, "#000000"))


def _ex_nisan(cx):
    """Çekim başında büyük 'NİSAN 1557' → yukarı çıkıp küçülür."""
    f = cx.f
    t = cx.t
    a = smooth((t - 0.1) / 0.6)
    k = smooth((t - cx.at(("c10s8", "oğlu", -0.55))) / 0.8)
    y = 590 + (150 - 590) * k
    size = int(150 + (60 - 150) * k)
    SH.gold_flat(f, "NİSAN 1557", W / 2, y, face="title", size=size, track=size * 0.1, alpha=a)


# ───────────────────────────── çekim listesi ─────────────────────────────
SHOTS = [
    # s1 — "Peki bütün bu savaşları kim ödedi?"
    shot("c10_soru", a=0.0, tr=("fade", 0.9), t_q=("c10s1", "kim", -0.1), label="soru"),
    # s1b — Çoğumuz Amerika'nın gümüşünü sayarız; s2 kayıtlar başka söylüyor
    shot("c10_sandik", a=("c10s1", "Çoğumuz", -0.15), tr=("fade", 0.7), t_label=("c10s1", "Amerika'nın", -0.1), t_count=("c10s1", "hemen", 0.0), t_x=("c10s2", "Kayıtlar", -0.1), label="gumus_sandik"),
    shot("c10_defter", a=("c10s2", "başka", -0.25), tr=("fade", 0.6), t_open=0.0, t_title=0.1, label="kayitlar_defter"),
    # s3 — 35 yıl, çoğu vergi; Alçak Ülkeler / Kastilya / Napoli
    shot("c10_sayac", a=("c10s3", -0.2), tr=("fade", 0.7), t_num=("c10s3", "otuz", -0.1), t_label=("c10s3", "olağanüstü", -0.1), t_tax=("c10s3", "çoğu", -0.1), label="35_yil_vergi"),
    shot("c10_bars", a=("c10s3", "Alçak", -0.35), tr=("fade", 0.7), t_unit=("c10s3", "dükatın,", -0.1),
         items=[dict(label="ALÇAK ÜLKELER", value=10.5, color="#7B1E2B", t0=("c10s3", "Alçak", -0.1), t1=("c10s3", "milyon", -0.1), text="10+ MİLYON"),
                dict(label="KASTİLYA", value=9.3, color="#9A2430", t0=("c10s3", "Kastilya", -0.1), t1=("c10s3", "dokuz", -0.1), text="9+ MİLYON"),
                dict(label="NAPOLİ", value=5.7, color="#B8862B", t0=("c10s3", "Napoli", -0.1), t1=("c10s3", "beş", -0.1), text="5+ MİLYON")], label="uc_bolge_vergi"),
    # s4 — gümüş akışının büyük patlaması sonra; Potosí 1545
    shot("c10_egri", a=("c10s4", -0.2), tr=("fade", 0.8), t_flow=("c10s4", "gümüş", -0.1), t_boom=("c10s4", "patlamasını", -0.2), t_after=("c10s4", "sonra", -0.15),
         t_potosi=("c10s4", "Potosí", -0.1), t_year=("c10s4", "1545'te", -0.1), label="gumus_egrisi_potosi"),
    # s5 — faturayı bankerler kesiyordu; 1523 Fugger mektubu
    shot("a_theatre", a=("c10s5", -0.2), tr=("fade", 0.8), scene="counting_house", p=dict(coins=0.7, clerks=2, chandelier=True),
         cams=[(0.0, (960, 560, 1.0)), (("c10s5", "1523'te", -0.2), (960, 800, 1.6))], overlay=_counting_overlay, label="sayim_odasi_bankerler"),
    shot("a_c_medal", a=("c10s5", "Jakob", -0.35), tr=("fade", 0.8), key="fugger", metal="bronze", name="JAKOB FUGGER", role="banker", pos="c", size=620,
         at=0.0, plate_at=("c10s5", "Jakob", -0.05), label="fugger"),
    # s6 — mektup, özetle, tacın kimin parasıyla alındığını hatırlatıyordu
    shot("c10_mektup", a=("c10s6", -0.2), tr=("fade", 0.8), t_summary=("c10s6", "özetle,", -0.1), t_seal=("c10s6", "hatırlatıyordu", -0.1),
         lines=[("Alacağın ödenmesi isteniyor.", ("c10s6", "Mektup,", 0.0)), ("Tacın kimin parasıyla alındığı hatırlatılıyor.", ("c10s6", "tacını", -0.1))], label="mektup_ozeti"),
    # s7 — Welser'ler Venezuela'da yönetim hakkı
    shot("a_map", a=("c10s7", -0.2), tr=("fade", 0.8), need=("c10_venezuela",), cams=[(0.0, (-30.0, 22.0, 0.8)), (("c10s7", "Venezuela'da", -0.4), (-66.5, 7.6, 3.0))],
         regions=[dict(name="c10_venezuela", color="#2F7A8A", at=("c10s7", "Venezuela'da", -0.15), alpha=0.55)], extra=_ex_venezuela, approx=False, label="welser_venezuela"),
    # s8 — 1556'da borç uçurumda; Nisan 1557'de Felipe ödemeleri durdurdu
    shot("c10_ucurum", a=("c10s8", -0.2), tr=("fade", 0.8), t_year=("c10s8", "1556'da", -0.1), t_crown=("c10s8", "imparator", -0.1), t_debt=("c10s8", "devletin", -0.1), t_edge=("c10s8", "uçurumdaydı.", -0.2), label="borc_ucurumda"),
    shot("a_c_medal", a=("c10s8", "Nisan", -0.2), tr=("dip", 0.9), key="felipe2", metal="gold", name="FELİPE", role="Şarlken'in oğlu", pos="c", size=600,
         at=("c10s8", "oğlu", -0.45), plate_at=("c10s8", "Felipe,", -0.1), extra=_ex_nisan, stampt=("ÖDEMELER DURDU", 1380, 735, ("c10s8", "ödemeleri", -0.1), 60), label="felipe_odemeleri_durdurdu"),
    # s9 — imparatorluk altınla değil borçla ayakta duruyordu
    shot("c10_kapanis", a=("c10s9", -0.2), tr=("fade", 0.8), t_gold=("c10s9", "imparatorluk", -0.1), t_not=("c10s9", "değil,", -0.25), t_debt=("c10s9", "borçla", -0.15), label="borcla_ayakta"),
]
