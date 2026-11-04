"""c11 — Papa Oğulları (1512 – 1537). PARÇA 5 KAPANIŞI (bölüm kartı c10→c11 Program'dan; bitiş ekranı SIRADAKİ PARÇA). Yönetmen kartı: yonetmen_c11.md.
Renk anahtarı: duman/kül + kızıl galero + lapis (imparator) + parşömen planlar; gravür (ANEKDOT) sepya. Ağır bölüm: mizah yalnız fil (V3) ve komisyoncu (V3) — Hanno, günah affı.
KAPALI: Prato (insan yok), yağma, Muhafız (sakin sayaç), Gavinana (mürekkep çizgisi), Alessandro'nun ölümü (kapı + gölge). Kapı: «…otuz yedi yıl hüküm sürecekti. Nasıl?» → «37» ağır sessiz vuruş + bitiş ekranı.
Tüm çekimler cümle/sözcük çapalı; ekrana yalnız seslendirilen ad/tarih/sayı.
"""
import math

from shots import shot
import cilt_medici as CM
import p5_lib as L
import c10_kinds as K10
import c11_kinds as K
from sk import clamp, ease_in, ease_io, ease_out, lerp
look = L.look

OUTRO_TR = ("dip", 1.4)


def mdl(x, y, R, hat, at, out=None, fall_at=None, flip=False, beard=0.0, tilt=0.0, scale_in=0.0, alpha=1.0):
    """Zamanlı siluet madalya bindirmesi: `at`'ta belirir, `out`'ta solar, `fall_at`'ta sallanıp düşer (söner)."""
    def fn(cx):
        k = cx.amt(at, 0.8)
        if out is not None:
            k *= 1.0 - cx.amt(out, 0.6)
        if k <= 0.003:
            return
        yy, tt, al = y, tilt + 0.03 * math.sin(cx.t * 0.8), alpha
        if fall_at is not None:
            u = clamp((cx.t - cx.at(fall_at)) / 1.3)
            yy = y + 160 * ease_in(u, 2.0)
            tt += 0.9 * ease_in(u, 2.0)
            al = alpha * (1.0 - 0.75 * ease_in(u, 1.4))
        L.sil_medal(cx.f, x, yy + 3 * math.sin(cx.t * 1.3), R * (0.88 + 0.12 * ease_out(k)), hat=hat, alpha=k * al, tilt=tt, flip=flip, beard=beard, nose=1.0)
    return fn


def leaf(head, sub, x_to, x_from, at, meet_at, x_end=None, y=330, sepia=False):
    """Takvim yaprağı bindirmesi: kenardan kayarak girer (at), `meet_at`'ta orta çizgiye (x_end) kayar ve iki yaprak yan yana oturur."""
    def fn(cx):
        k = ease_out(clamp((cx.t - cx.at(at)) / 0.9), 2.4)
        if k <= 0.003:
            return
        u = ease_io(clamp((cx.t - cx.at(meet_at)) / 0.7))
        x0 = lerp(x_from, x_to, k)
        x = lerp(x0, x_end if x_end is not None else x0, u)
        L.tag(head, x, y, at, size=46, w=520, sub=sub, dur=0.01)(cx)
    return fn


SHOTS = [
    # ── V1 · Prato: duman, bayrak; kamera orduya kayar ──────────────────────────────────────────────────────────
    shot("c11_prato", ("c11s1", 0), mode="day", perde=2, pan_at=("c11s1", "29", 0.0), pan_dur=6.5, med_at=("c11s1", "Medici'den", -0.1), cam=("push", 0.08),
         ovl=L.ov(L.engr("29 AĞUSTOS 1512", 960, 232, ("c11s1", "29", -0.1), size=100, track=14, dur=1.1, out=("c11s1", "İspanyol", 0.4)),
                  L.tag("PRATO", 700, 360, ("c11s1", "Prato'yu", -0.1), size=44, w=320, out=("c11s1", "ordunun", 0.0)),
                  L.tag("İSPANYOL ORDUSU", 1500, 330, ("c11s1", "ordusu", -0.1), size=34, w=520, out=("c11s1", "papalık", 0.0)),
                  L.tag("PAPALIK ELÇİSİ", 1440, 330, ("c11s1", "papalık", -0.05), size=34, w=470, out=("c11s1", "Lorenzo'nun", 0.0)),
                  L.tag("LORENZO'NUN OĞLU", 1440, 840, ("c11s1", "Lorenzo'nun", -0.1), size=32, w=470, out=("c11s1", "Giovanni.", 0.3)),
                  L.tag("GİOVANNİ", 1440, 840, ("c11s1", "Giovanni.", -0.1), size=40, w=360)),
         label="Prato: duman ve bayraklar; ordunun yanında kardinal Giovanni"),
    # ── V1b · mektup: «başkalarına örnek ve dehşet» ─────────────────────────────────────────────────────────────
    shot("c10_mektup", ("c11s2", -0.2), mode="day", perde=2, at=("c11s2", -0.2), n=6, dur=3.0, seed=9, w=900, h=800, page_xy=(900, 540), candle_xy=(1580, 720), cam=("push", 0.08),
         ovl=L.ov(L.tag("PAPA'YA MEKTUP", 900, 190, ("c11s2", "Papa'ya", -0.1), size=34, w=480, out=("c11s2", "olanları", 0.3)),
                  lambda cx: L.hand_at(cx.f, cx, "“başkalarına örnek", 560, 690, ("c11s2", "“başkalarına", -0.05), size=60, color="#6A1A12", dur=1.3, seed=3),
                  lambda cx: L.hand_at(cx.f, cx, "ve dehşet”", 640, 770, ("c11s2", "ve", -0.05), size=60, color="#6A1A12", dur=1.2, seed=5),
                  L.stamp("○ TEK KAYNAK", 1560, 250, ("c11s2", "aktarılır.", -0.2), size=48, rot=-0.07)),
         tr=("sayfa", 0.9), link="material", label="mektup: başkalarına örnek ve dehşet (○)"),
    # ── V2 · Soderini düşer, Medici döner (soldan sağa kabaran kalabalık) ──────────────────────────────────────
    shot("p5_sehir", ("c11s3", -0.2), scene="meydan", act="kalabalik", tod="day", mode="day", perde=2, dir="r", flags="medici", n=26, cam=("push", 0.08),
         ovl=L.ov(mdl(480, 560, 140, "cap", ("c11s3", "Soderini'nin", -0.1), fall_at=("c11s3", "düştü", -0.1)),
                  L.tag("SODERİNİ", 480, 760, ("c11s3", "Soderini'nin", -0.1), size=32, w=340, out=("c11s3", "ve", 0.3)),
                  mdl(1440, 560, 140, "berretto", ("c11s3", "Medici,", -0.2)),
                  L.tag("MEDİCİ", 1440, 760, ("c11s3", "Medici,", -0.1), size=32, w=280, out=("c11s3", "eylülde", 0.3)),
                  L.tag("YAKLAŞIK", 960, 200, ("c11s3", "yaklaşık", -0.1), size=30, w=300, out=("c11s3", "sonra,", 0.1)),
                  L.count_up(960, 350, ("c11s3", "on", -0.1), 18, dur=1.0, unit="YIL", size=130, unit_size=40, out=("c11s3", "eylülde", 0.1)),
                  L.tag("EYLÜL", 960, 250, ("c11s3", "eylülde", -0.1), size=44, w=320)),
         tr=("carry", 0.9, dict(strip="banner", dir="r")), link="carry", label="Soderini düşer; Medici döner (18 yıl)"),
    # ── V2b · çocuk kardinal → iki oylama → X. Leo ─────────────────────────────────────────────────────────────
    shot("c11_leo", ("c11s4", -0.2), mode="day", perde=2, child_at=("c11s4", "Giovanni", -0.1), red_at=("c11s4", "kardinal", -0.15), grow_at=("c11s4", "mart", -0.2),
         vote1_at=("c11s4", "iki", -0.3), vote2_at=("c11s4", "oylamada", -0.4), pope_at=("c11s4", "seçildi:", -0.1), cam=("push", 0.08),
         ovl=L.ov(L.tag("GİOVANNİ", 560, 800, ("c11s4", "Giovanni", -0.1), size=34, w=360, out=("c11s4", "mart", 0.0)),
                  L.stamp("○ TEK KAYNAK", 1560, 230, ("c11s4", "yazıldığına", -0.1), size=46, rot=-0.07, out=("c11s4", "mart", 0.0)),
                  L.count_up(560, 340, ("c11s4", "on", -0.1), 13, dur=0.9, unit="YAŞINDA", size=120, unit_size=34, out=("c11s4", "mart", 0.0)),
                  L.tag("KARDİNAL", 560, 880, ("c11s4", "kardinal", -0.1), size=32, w=300, out=("c11s4", "mart", 0.0)),
                  L.date_plate("MART 1513", ("c11s4", "mart", -0.1)),
                  L.count_up(1450, 290, ("c11s4", "otuz", -0.1), 37, dur=1.0, unit="YAŞINDA", size=120, unit_size=34),
                  L.tag("İKİ OYLAMA", 1450, 660, ("c11s4", "iki", -0.1), size=32, w=360),
                  L.tag("X. LEO", 900, 850, ("c11s4", "X.", -0.1), size=48, w=360)),
         tr=("zoomthru", 0.9, dict(at=(960, 560), at_b=(960, 540))), link="scale", label="çocuk kardinal; iki oylama; tiara"),
    # ── V3 · Lateran alayı: iki takvim yaprağı aynı güne oturur ─────────────────────────────────────────────────
    shot("p5_procession", ("c11s5", -0.2), dir="r", density=0.9, mix=dict(rider=0.20, noble=0.16, page=0.12, banner=0.22, guard=0.04, elder=0.08, cleric=0.16, common=0.02), cam=("pan", "r", 640), speed=110.0, seed=11, mode="day", perde=2,
         ovl=L.ov(leaf("11 NİSAN 1513", "LATERAN", 480, -520, ("c11s5", "11", -0.2), ("c11s5", "denk", -0.1), x_end=700),
                  leaf("BİR YIL ÖNCE", "RAVENNA · ESİR", 1440, 2300, ("c11s5", "bir", -0.1), ("c11s5", "denk", -0.1), x_end=1240, sepia=True),
                  L.engr("=", 960, 318, ("c11s5", "denk", 0.0), size=150, dur=0.5, style="gilt", glow=0.3),
                  L.stamp("○ TEK KAYNAK", 1600, 780, ("c11s5", "geliyordu.", -0.2), size=46, rot=-0.07)),
         tr=("carry", 0.9, dict(strip="banner", dir="r")), link="carry", label="Lateran alayı: iki yaprak aynı güne oturur (○)"),
    shot("p5_pano", ("c11s6", -0.2), pano="florence", tod="day", mode="day", perde=2, cam=("pan", "r", 500),
         cams=[(("c11s6", -0.2), (3000, 0, 1.0)), (("c11s6", "aforozlu", -0.2), (3420, 20, 1.18)), (("c11s7", -0.3), (3800, 30, 1.3))],
         stations=[dict(x=2900, at=0.0, fn=K.st_papal_horse, speed=85.0)],
         ovl=L.ov(L.tag("PAPA", 3060 * 0 + 560, 250, ("c11s6", "Papa'nın", -0.1), size=34, w=260, out=("c11s6", "aforozlu", 0.0)),
                  L.tag("ALFONSO D'ESTE", 1360, 250, ("c11s6", "Alfonso", -0.1), size=34, w=470, sub="aforozlu", out=("c11s7", -0.3)),
                  L.stamp("○ TEK KAYNAK", 1600, 780, ("c11s6", "anlatılır.", -0.3), size=46, rot=-0.07)),
         tr=("slide", 0.8, dict(dir="r")), link="dir", label="beyaz at, yedekte aforozlu Alfonso (○)"),
    # ── V3b · papası var, bankası yok; alacaklılar ──────────────────────────────────────────────────────────────
    shot("c11_seritler", ("c11s7", -0.2), mode="day", perde=2, pope_at=("c11s7", "papası", -0.5), bank_at=("c11s7", "bankası", -0.5), lock_at=("c11s7", "yoktu;", -0.3), key_at=("c11s7", "kayyumlara", -0.8), cam=("push", 0.08),
         ovl=L.ov(L.tag("MEDİCİ PAPASI", 960, 495, ("c11s7", "papası", -0.1), size=38, w=520),
                  L.tag("MEDİCİ BANKASI", 760, 880, ("c11s7", "bankası", -0.1), size=38, w=520, out=("c11s7", "ailenin", 0.0)),
                  L.date_plate("1494", ("c11s7", "1494'te", -0.15)),
                  L.tag("KAYYUM", 1340, 880, ("c11s7", "kayyumlara", -0.1), size=34, w=360)),
         tr=("zoomthru", 0.9, dict(at=(960, 540), at_b=(960, 540))), link="scale", label="iki şerit: Medici papası ↔ kayyumdaki banka"),
    shot("c11_borc", ("c11s8", -0.2), mode="day", perde=2, head_at=("c11s8", "Leo", -0.2), rows_at=[("BİNİ", ("c11s8", "Bini,", -0.1)), ("GADDİ", ("c11s8", "Gaddi,", -0.1)), ("SALVİATİ", ("c11s8", "Salviati", -0.1)), ("STROZZİ", ("c11s8", "Strozzi", -0.1))],
         none_at=("c11s8", "Medici", -0.2), strike_at=("c11s8", "geçmez.", -0.35), cam=("push", 0.08),
         ovl=L.ov(mdl(330, 560, 160, "tiara", ("c11s8", "Leo", -0.2), fall_at=("c11s8", "öldü;", -0.1)),
                  L.tag("LEO BORÇLU", 330, 800, ("c11s8", "borçlu", -0.1), size=34, w=380),
                  L.tag("ALACAKLILAR", 1060, 190, ("c11s8", "alacaklıları", -0.1), size=36, w=460),
                  L.tag("ADI GEÇMEZ", 1060, 880, ("c11s8", "adı", -0.1), size=36, w=420),
                  L.stamp("○ TEK KAYNAK", 1640, 250, ("c11s8", "geçer,", -0.2), size=46, rot=-0.07)),
         tr=("sayfa", 0.9), link="material", label="defter: alacaklılar; Medici bankasının adı yok (○)"),
    shot("black", ("c11s9", -0.2), text="[devam]", label="yer tutucu"),
]
