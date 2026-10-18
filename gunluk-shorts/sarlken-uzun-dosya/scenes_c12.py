"""Bölüm 12 — Bırakmak (≈96 sn). Ton: c0'ın aynası: aynı salon, ağır altın ışık, vedaya dönük. Yazar D.
Ayna motifleri: c0 tarih kartı ↔ c12 tarih+saat; c0 salon itme (geniş→yakın) ↔ c12 salon çekme (yakın→geniş) + kolonun ardından yürüyen çift;
c0 '40 YIL' sayacı ↔ c12 '1515→1555' zaman çizgisi; c0 V. KARL (altın) ↔ c12 V. KARL (oniks, 58 yaşında, kararır)."""
import math

import scenes_lib  # noqa: F401
import d_common as D
import scenes_d as SD
import shots_c12 as S12  # noqa: F401
import shots as SH
import sk
from d_common import A, AE, tag, tag_seq, icn
from shots import shot
from sk import W, H, clamp, ease_io, lerp

TL = SH.timeline()

# ─────────────── salon (s3): kamera + yürüyen çift ───────────────
_H0 = A("c12s3", -0.3)
T_H = TL.resolve(_H0)
_CAM_H = SD.keys_local([
    (_H0, (985, 604, 1.22)),                                   # c0'ın bitişinin aynası: yakından başla, geri çekil
    (A("c12s3", "toplanmış", 0.3), (960, 560, 1.0)),
    (A("c12s3", "İmparator", -0.2), (700, 600, 1.2)),          # çifti izle
    (A("c12s3", "giriyor", 1.0), (900, 640, 1.34)),
], _H0)
_T_ENTER = TL.resolve(A("c12s3", "İmparator", -0.1)) - T_H
_T_ARRIVE = TL.resolve(A("c12s3", "var", 0.2)) - T_H
_X0, _X1 = 110.0, 900.0


def _pair_state(t):
    k = clamp((t - _T_ENTER) / max(0.5, _T_ARRIVE - _T_ENTER))
    return k, lerp(_X0, _X1, ease_io(k, 1.25))


def _hall_extra(f, t):
    k, x = _pair_state(t)
    if k > 0:
        SD.draw_pair(f, x, 985, 520, t, walk=(0 < k < 0.985))


def _ov_hall(cx):
    f = cx.f
    cam = SD.cam_at(cx.t, _CAM_H)
    k1 = cx.amt(A("c12s3", "Genel", -0.15), 0.7) * (1 - cx.amt(A("c12s3", "İmparator", -0.5), 0.5))
    tag(f, "GENEL DEVLETLER", 96, 128, k1, size=36)
    k2 = cx.amt(A("c12s3", "Orange", -0.2), 0.6) * (1 - cx.amt(A("c12s3", "giriyor", 0.7), 0.6))
    if k2 > 0:
        _, px = _pair_state(cx.t)
        sx, sy = SD.scene_to_screen(px + 150, 520, cam)
        tx, ty = sx + 70, sy - 300
        f.line(tx + 10, ty + 100, sx, sy - 30, color="#C9962B", sw=2, alpha=0.8 * k2)
        f.circle(sx, sy - 30, 5, color="#F0D27A", alpha=k2)
        tag(f, "WİLLEM", tx, ty, k2, size=36, sub="Orange Prensi")


# ─────────────── s5 haritası: Hollanda → İspanya ───────────────
def _ov_devir(cx, cam, mv):
    f = cx.f
    k1 = cx.amt(A("c12s5", "Hollanda", -0.1), 0.7) * (1 - cx.amt(A("c12s5", "İspanya", -0.5), 0.5))
    tag(f, "25 EKİM 1555", 96, 150, k1, size=40, sub="bugün")
    k2 = cx.amt(A("c12s5", "Ocak", -0.25), 0.7)
    tag(f, "OCAK 1556", 96, 150, k2, size=40, sub="gelecek")
    D.cameo(f, cx, "felipe2", 1590, 520, 300, A("c12s5", "oğluna", -0.25), metal="gold", name="FELİPE", role="Oğlu", i=0, plate_dy=170)


# ─────────────── s10: yatak odası kaplaması ───────────────
_B0 = A("c12s10", -0.2)
T_B = TL.resolve(_B0)
_T_OUT = TL.resolve(A("c12s10", "öldü", -0.15)) - T_B


def _ov_bed(cx):
    f = cx.f
    tag_seq(cx, [("31 AĞUSTOS 1558", None, A("c12s10", "31", -0.1), A("c12s10", "Büyük", -0.3)),
                 ("BÜYÜK OLASILIKLA", "sıtma", A("c12s10", "Büyük", -0.1), A("c12s10", "21", -0.3)),
                 ("21 EYLÜL 1558", None, A("c12s10", "21", -0.1), None)], x=W - 96, y=H - 230, size=40, align="r")
    # ateş: sıcak kırmızı nabız
    kf = cx.amt(A("c12s10", "ateşi", -0.1), 0.8) * (1 - cx.amt(A("c12s10", "sıtmaydı", 0.1), 1.0))
    if kf > 0:
        pulse = 0.55 + 0.45 * math.sin(cx.t * 4.2)
        f.rect(0, 0, W, H, shader=f.rad(W / 2, H / 2, 1100, [("#C0392B", 0.0, 0), ("#C0392B", 0.7, int(30 * kf * pulse)), ("#7A1210", 1.0, int(130 * kf * pulse))]))


def _ov_chapel(txt, anchor, y=905):
    def ov(cx):
        SH.stamp(cx.f, txt, W / 2, y, rot=-0.06, size=64, t=cx.amt(anchor, 0.3))
    return ov


def _ov_tower(cx):
    k = cx.amt(A("c12s2", "Altı", -0.1), 0.7)
    tag(cx.f, "ALTI AY ÖNCE", 96, 128, k, size=38)
    k2 = cx.amt(A("c12s2", "Juana", -0.15), 0.7)
    tag(cx.f, "JUANA", 96, 238, k2, size=36, sub="annesi")


SHOTS = [
    # s1 — 25 Ekim 1555, öğleden sonra saat üç sularında (c0 tarih kartının aynası)
    shot("c12_clock", a=A("c12s1", -0.05), at_city=A("c12s1", 0.0), at_date=A("c12s1", "25", -0.15), at_clock=A("c12s1", "Öğleden", -0.3), at_hand=A("c12s1", "saat", -0.1), at_three=A("c12s1", "üç", 0.0), label="saat_uc"),
    # s2a — altı ay önce annesi Juana (Tordesillas kulesi; pencereye yaklaşma)
    shot("theatre", a=A("c12s2", -0.3), tr=("fade", 0.9), scene="tower", cams=[(0.0, (960, 540, 1.0)), (A("c12s2", "kırk", 0.0), (985, 400, 1.5))],
         p=dict(variant="tordesillas", candle=1.0), overlay=_ov_tower, label="kule_juana"),
    # s2b — kırk altı yıllık tutsaklığın ardından
    shot("wd_counter", a=A("c12s2", "kırk", -0.3), tr=("fade", 0.8), value=46, unit="YIL", size=300, pos=(W * 0.69, H * 0.44), at=A("c12s2", "kırk", -0.1), dur=1.1,
         lab="Tordesillas", lab_at=A("c12s2", "tutsaklığın", -0.1),
         medal_=dict(key="juana", metal="onyx", x=W * 0.28, y=H * 0.45, size=540, at=0.0, name="JUANA", role="Kastilya Kraliçesi"), label="juana_46"),
    # s3a — salonda Genel Devletler; imparator, Willem'in omzuna yaslanarak giriyor (aynı hall; altın ışık)
    shot("theatre", a=_H0, tr=("fade", 0.9), scene="d_hall_gold", cams=[(t, v) for t, v in _CAM_H], tint=("#E08A1E", 0.07), dust_n=110,
         p=dict(emperor=False, glow0="#FFE2A8", glow1="#E27A18", extra=_hall_extra), overlay=_ov_hall, label="salon_ikinci"),
    # s3b — arkasında oğlu Felipe ve kız kardeşi Mary
    shot("wd_medals", a=A("c12s3", "oğlu", -0.3), tr=("fade", 0.8), size=470, y=H * 0.43,
         items=[dict(key="felipe2", name="FELİPE", role="Oğlu", metal="gold", at=A("c12s3", "Felipe", -0.35)),
                dict(key="mary_macar", name="MARY", role="Kız kardeşi", metal="gold", at=A("c12s3", "Mary", -0.35))], label="felipe_mary"),
    # s4 — tam kırk yıl önce, on beş yaşında (1515 → 1555)
    shot("c12_forty", a=A("c12s4", -0.2), tr=("fade", 0.8), at_old=A("c12s4", 0.0), at_back=A("c12s4", "tam", -0.1), at_young=A("c12s4", "beş", -0.4), at_crown=A("c12s4", "hükmetmeye", -0.1), label="kirk_yil"),
    # s5a — Hollanda oğluna (bugün) → İspanya Ocak 1556'da
    shot("map", a=A("c12s5", -0.25), tr=("fade", 0.8),
         cams=[(0.0, (4.8, 51.3, 4.3)), (A("c12s5", "İspanya", -0.5), (4.8, 51.3, 4.4)), (A("c12s5", "İspanya", 1.1), (-3.4, 40.6, 2.6))],
         regions=[dict(name="hollanda", color="burgonya", at=A("c12s5", "Hollanda", -0.1), alpha=0.6), dict(name="ispanya", color="ispanya", at=A("c12s5", "İspanya", -0.1), alpha=0.6)],
         labels=[dict(text="HOLLANDA", lon=4.9, lat=52.45, size=40, at=A("c12s5", "Hollanda", -0.05)), dict(text="İSPANYA", lon=-3.7, lat=40.4, size=46, at=A("c12s5", "İspanya", 0.0))],
         extra=_ov_devir, label="devir_harita"),
    # s5b — imparatorluk unvanı ise kardeşi Ferdinand'a (devir şeması)
    shot("c12_transfer", a=A("c12s5", "İmparatorluk", -0.45), tr=("fade", 0.7), at_r1=0.15, at_r2=0.5, at_r3=A("c12s5", "unvanı", -0.3),
         at_dates=(0.75, 1.05, A("c12s5", "1556", -0.1, 1)), at_who3=A("c12s5", "kardeşi", -0.2), label="devir_semasi"),
    # s6a — nedenler: gut ve yorgunluk
    shot("c12_reason", a=A("c12s6", -0.35), tr=("fade", 0.8), which="gut", at_kick=A("c12s6", "Tarihçilerin", -0.1), at_stamp=A("c12s6", "nedenler", -0.05),
         at_icon=A("c12s6", "şunlar", 0.0), at_w1=A("c12s6", "gut", 0.0), at_w2=A("c12s6", "yorgunluk", -0.1), label="neden_gut"),
    # s6b — evrensel Hıristiyan imparatorluğunun gerçekleşmeyeceği
    shot("c12_reason", a=A("c12s6", "evrensel", -0.45), tr=("fade", 0.7), which="empire", at_kick=A("c12s6", "evrensel", -0.4), at_icon=A("c12s6", "evrensel", -0.4), at_w1=A("c12s6", "evrensel", 0.0),
         at_crack=A("c12s6", "gerçekleşmeyeceğinin", 0.0), label="neden_evrensel"),
    # s7 — Felipe İspanya'yı savaşta ve iflasa yakın devralacaktı
    shot("c12_crackcoin", a=A("c12s7", -0.2), tr=("fade", 0.8), at_med=A("c12s7", "Felipe", -0.25), at_war=A("c12s7", "savaşta", -0.2), at_crack=A("c12s7", "iflasa", -0.1), at_broke=A("c12s7", "yakın", 0.0), label="felipe_iflas"),
    # s8a — Eylül 1556'da İspanya'ya döndü
    shot("map", a=A("c12s8", -0.2), tr=("fade", 0.8), cams=[(0.0, (-0.6, 46.6, 2.15)), (A("c12s8", "döndü", 0.2), (-1.4, 45.4, 2.3))],
         regions=[dict(name="hollanda", color="burgonya", at=0.2, alpha=0.55), dict(name="ispanya", color="ispanya", at=0.4, alpha=0.55)],
         labels=[dict(text="HOLLANDA", lon=4.6, lat=52.4, size=34, at=0.5), dict(text="İSPANYA", lon=-2.6, lat=42.4, size=38, at=A("c12s8", "İspanya'ya", -0.1))],
         routes=[dict(pts=[(3.6, 51.45), (1.0, 50.3), (-3.5, 48.9), (-6.0, 46.6), (-3.8, 43.45)], at=A("c12s8", "Eylül", -0.25), dur=2.6, color="#F0D27A", width=5)],
         icons_=[dict(kind="ship", lon=3.6, lat=51.45, size=70, at=A("c12s8", "Eylül", -0.25), route=[(3.6, 51.45), (1.0, 50.3), (-3.5, 48.9), (-6.0, 46.6), (-3.8, 43.45)], move_at=A("c12s8", "Eylül", -0.25), move_dur=2.6, bob=3, glow=0.3)],
         date=("EYLÜL 1556", A("c12s8", "Eylül", -0.1)), label="donus_1556"),
    # s8b — Şubat 1557, Yuste
    shot("map", a=A("c12s8", "Şubat", -0.45), tr=("fade", 0.7), cams=[(0.0, (-4.2, 42.4, 2.8)), (A("c12s8", "Yuste", -0.3), (-5.75, 40.14, 6.6))],
         regions=[dict(name="ispanya", color="ispanya", at=0.0, alpha=0.5)],
         routes=[dict(pts=[(-3.8, 43.45), (-4.8, 41.9), (-5.75, 40.14)], at=A("c12s8", "Şubat", -0.3), dur=1.9, color="#F0D27A", width=5, dash=(12, 9), arrow=False)],
         cities=[dict(lon=-5.75, lat=40.14, name="YUSTE", kind="seat", at=A("c12s8", "Yuste", -0.1), side="r", size=40)],
         date=("ŞUBAT 1557", A("c12s8", "Şubat", -0.1)), label="yuste_harita"),
    # s8c — manastırın yanındaki küçük konut (cloister — oda-lab)
    shot("theatre", a=A("c12s8", "küçük", -0.35), tr=("fade", 0.8), scene="cloister", cams=[(0.0, (960, 560, 1.0)), (A("c12s9", -0.3), (990, 600, 1.3))], p=dict(time="dusk"), label="yuste_avlu"),
    # s9a — kendi adına okunan ayine katıldığını yazıyor (bir çalışma)
    shot("theatre", a=A("c12s9", -0.25), tr=("fade", 0.9), scene="chapel", cams=[(0.0, (960, 580, 1.0)), (A("c12s9", "yazıyor", 0.5), (960, 620, 1.3))], p=dict(coffin=False),
         overlay=_ov_chapel("ÇALIŞMAYA GÖRE", A("c12s9", "çalışma", -0.1)), label="ayin"),
    # s9b — tabutuna yatıp cenazesini prova etti: yalnızca rivayet (soğuk, kesik çizgili hayalet tabut)
    shot("c12_rumor", a=A("c12s9", "Tabutuna", -0.35), tr=("fade", 0.9), at_coffin=A("c12s9", "Tabutuna", -0.3), at_fig=A("c12s9", "yatıp", -0.1), at_stamp=A("c12s9", "rivayet", -0.15), label="tabut_rivayet"),
    # s10a — 31 Ağustos 1558, ateş; büyük olasılıkla sıtma; 21 Eylül'de öldü (mum söner)
    shot("theatre", a=_B0, tr=("dip", 0.85), scene="bedroom", cams=[(0.0, (960, 540, 1.0)), (A("c12s10", "öldü", -0.3), (905, 600, 1.28))], p=dict(candle=1.0, fade_candle_t=(_T_OUT, _T_OUT + 1.0)),
         overlay=_ov_bed, label="yatak_odasi"),
    # s10b — elli sekiz yaşındaydı (oniks madalya, siyaha)
    shot("wd_medal_swap", a=A("c12s10", "Elli", -0.45), tr=("fade", 0.9), key="karl_yasli", metal_a="onyx", metal_b="onyx", swap_at=99.0, name="V. KARL", role="58 yaşında  ·  1500 – 1558", size=620, at=0.1, plate_at=A("c12s10", "sekiz", -0.2), fade_out=1.0, label="elli_sekiz"),
]
