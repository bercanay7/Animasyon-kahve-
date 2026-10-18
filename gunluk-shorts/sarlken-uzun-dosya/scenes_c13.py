"""Bölüm 13 — Hesap (≈84 sn). Ton: son — açılan altın ışık, sonra sade soru. Yazar D.
Kaynak kapısı gereği: 'BİRÇOK TARİHÇİ' damgası YOK (c13s5 artık 'Sonuçta Avrupa … dengeleyen devletlerden oluşan bir yapıya doğru gitti');
c13s3 'Şarlken'in bıraktıklarıyla … iki kola ayrıldı' (ölünce değil); c13s6 'en bilinen büyük tartışma' ('ilk' demiyoruz).
Son çekim: beş cephe + 'HANGİSİNİ BIRAKIRDIN?'; kapanış compose.py'de c13 sonrası 7 sn eklenir."""
import math

import scenes_lib  # noqa: F401
import d_common as D
import icons
import shots_c13 as S13
import shots_c9 as S9
import sk
from d_common import A, AE, icn, glow_dot
from shots import shot
from sk import W, H


def _idea(cx, x, y, size, k):
    """'Fikir': küre üstünde taç (tek adamın bütün dünyayı taşıyabileceği fikri)."""
    f = cx.f
    glow_dot(f, x, y, size * 0.75, "#E3B54A", 0.4 * k)
    D.draw_globe(f, x, y + size * 0.10, size * 0.30, rot=cx.t * 0.4, alpha=k, glow=0.25)
    icons.draw_icon(f, "imperial_crown", x, y - size * 0.28, size=size * 0.40, metal="gold", alpha=k, glow=0.35)


ATL_ROUTES = [
    [(-6.3, 37.2), (-26, 31.5), (-58, 23.5), (-76, 19.8)],        # Sevilla → Karayipler
    [(-6.3, 37.2), (-33, 25.5), (-66, 15.5), (-79.9, 9.4)],       # Sevilla → Panama
    [(-96.1, 19.2), (-82, 25.5), (-48, 35.5), (-9.5, 37.6)],      # Yeni İspanya → Sevilla (dönüş)
]


def _atl_extra(cx, cam, mv):
    f = cx.f
    for j, pts in enumerate(ATL_ROUTES):
        t0 = cx.at(A("c13s6", "Atlantik", -0.25 + 0.25 * j))
        k = sk.ease_io(sk.clamp((cx.t - t0) / 2.0))
        if k > 0:
            mv.route(f, cam, pts, prog=k, color="#F0D27A" if j < 2 else "#C9D2DA", width=4.5, arrow=False, dash=(12, 9), dash_phase=-cx.t * 30 * (1 if j < 2 else -1), alpha=0.9)
        for q in (0.0, 0.5):
            kk = (sk.clamp((cx.t - t0 - 0.5) / 2.6) + q) % 1.0
            if 0 < k <= 1.0 and cx.t - t0 > 0.5:
                (x, y), ang = mv.point_on(cam, pts, kk)
                icons.draw_icon(f, "ship", x, y - 26, size=60, metal="gold" if j < 2 else "silver", alpha=0.95, glow=0.25)
    kt = cx.amt(A("c13s6", "ticaret", -0.15), 0.7)
    D.tag(f, "TİCARET YOLU", W / 2, 150, kt, size=38, align="c")


SHOTS = [
    # s1 — beşinci cephe en sessiz olanıydı: miras
    shot("c13_open", a=A("c13s1", -0.2), at_kick=A("c13s1", "Beşinci", -0.1), at_icon=A("c13s1", "cephe", -0.1), at_word=A("c13s1", "miras", -0.15), label="besinci_cephe"),
    # s2 — dört büyük taht, tek adam; bir ülke gibi değil, akrabalık ağı gibi
    shot("c13_network", a=A("c13s2", -0.3), tr=("fade", 0.8),
         at_thrones=(A("c13s2", "Dört", -0.1), A("c13s2", "büyük", -0.05), A("c13s2", "taht", -0.05), A("c13s2", "tek", -0.4)),
         at_karl=A("c13s2", "adama", -0.3), at_mesh=A("c13s2", "birbirine", -0.1), at_blob=A("c13s2", "ülke", -0.25), at_blob_off=A("c13s2", "değil", -0.1), at_net=A("c13s2", "akrabalık", -0.2), label="akrabalik_agi"),
    # s3a — Şarlken'in bıraktıklarıyla Habsburg hanedanı iki kola ayrıldı (kartal ikiye)
    shot("c13_split", a=A("c13s3", -0.3), tr=("fade", 0.8), at_karl=0.1, at_eagle=A("c13s3", "Habsburg", -0.3), at_word=A("c13s3", "hanedanı", -0.1),
         at_crack=A("c13s3", "kola", -0.2), at_split=A("c13s3", "ayrıldı", -0.25), at_color=A("c13s3", "İspanya", -0.3), label="kartal_ikiye"),
    # s3b — İspanya kolu Felipe'ye, Avusturya kolu Ferdinand'a (harita rengi ikiye ayrılır)
    shot("map", a=A("c13s3", "İspanya", 0.0), tr=("fade", 0.7), cams=[(0.0, (8.5, 46.4, 1.38)), (AE("c13s3", 0.6), (9.0, 46.2, 1.5))],
         regions=[dict(name="ispanya", color="ispanya", at=A("c13s3", "İspanya", 0.1)), dict(name="napoli", color="ispanya", at=A("c13s3", "İspanya", 0.25)),
                  dict(name="milano", color="ispanya", at=A("c13s3", "İspanya", 0.35)), dict(name="hollanda", color="ispanya", at=A("c13s3", "İspanya", 0.45)),
                  dict(name="avusturya", color="#D98A2B", at=A("c13s3", "Avusturya", 0.0)), dict(name="bohemya", color="#D98A2B", at=A("c13s3", "Avusturya", 0.15)),
                  dict(name="macar_habsburg", color="#D98A2B", at=A("c13s3", "Avusturya", 0.3))],
         extra=S13.branches_extra(A("c13s3", "İspanya", 0.1), A("c13s3", "Felipe'ye", -0.3), A("c13s3", "Avusturya", 0.1), A("c13s3", "Ferdinand'a", -0.5)), label="iki_kol_harita"),
    # s4a — evrensel Hıristiyan imparatorluk hayali gerçekleşmedi (taç çatlar)
    shot("c13_crown", a=A("c13s4", -0.3), tr=("fade", 0.8), at_kick=A("c13s4", "Evrensel", -0.1), at_crown=A("c13s4", "Evrensel", 0.0), at_crack=A("c13s4", "gerçekleşmedi", -0.05), label="taç_çatlar"),
    # s4b — Reform durmadı; Augsburg Barışı Lutherciliği tanıdı
    shot("map", a=A("c13s4", "Reform", -0.35), tr=("fade", 0.7), cams=[(0.0, (11.0, 50.2, 3.1)), (AE("c13s4", 0.4), (11.0, 49.6, 3.3))],
         regions=[dict(name="almanya", color="protestan", at=A("c13s4", "Reform", 0.0), alpha=0.6)],
         extra=S13.reform_extra(A("c13s4", "Reform", -0.1), A("c13s4", "Augsburg", -0.15), A("c13s4", "Barışı", -0.2), A("c13s4", "Lutherciliği", -0.1)), label="reform_yayilir"),
    # s5 — sonuçta Avrupa tek imparatorluk yerine birbirini dengeleyen devletlerden oluşan bir yapıya doğru gitti
    shot("c13_balance", a=A("c13s5", -0.25), tr=("fade", 0.8), at_av=A("c13s5", "Avrupa", -0.15), at_crown=A("c13s5", "tek", -0.15), at_crown_off=A("c13s5", "yerine", -0.1),
         at_shields=A("c13s5", "birbirini", -0.1), step=0.38, at_word=A("c13s5", "yapıya", -0.1), label="denge_terazi"),
    # s6a — dünya küçüldü: ilk dünya turu tamamlandı
    shot("map", a=A("c13s6", -0.2), tr=("fade", 0.8), cams=[(0.0, (8, 26, 0.5)), (A("c13s6", "küçüldü", 0.5), (0, -7, 0.165))], compass=(1790, 930, 56), mountains=False,
         extra=S9.circum_extra(A("c13s6", "ilk", -0.2), dur_a=1.1, dur_b=1.2, flag_at=None), date=("1519 – 1522", A("c13s6", "turu", -0.1)), label="dunya_kuculdu"),
    # s6b — Atlantik bir ticaret yolu oldu
    shot("map", a=A("c13s6", "Atlantik", -0.25), tr=("fade", 0.7), cams=[(0.0, (-38, 27, 0.62)), (AE("c13s6", -2.5), (-40, 26, 0.7))], compass=(1790, 930, 56),
         labels=[dict(text="ATLANTİK OKYANUSU", lon=-40, lat=33.5, size=32, color="#9FB8C8", at=A("c13s6", "Atlantik", 0.0), track=12)],
         cities=[dict(lon=-6.0, lat=37.4, name="SEVİLLA", kind="town", at=A("c13s6", "Atlantik", 0.3), side="t", size=26)],
         extra=_atl_extra, label="atlantik_ticaret"),
    # s6c — sömürgeciliğin ahlâkı üzerine en bilinen büyük tartışma
    shot("wd_vs", a=A("c13s6", "sömürgeciliğin", -0.3), tr=("fade", 0.8), size=420, gap=620, y=H * 0.47, title="SÖMÜRGECİLİĞİN AHLÂKI", title_at=A("c13s6", "sömürgeciliğin", -0.1), ring_at=A("c13s6", "sömürgeciliğin", 0.0),
         left=dict(key="sepulveda", metal="silver", name="SEPÚLVEDA", at=A("c13s6", "bilinen", -0.2, alt=("büyük",))),
         right=dict(key="lascasas", metal="ivory", name="LAS CASAS", flip=True, at=A("c13s6", "bilinen", 0.0, alt=("büyük",))),
         center=dict(icon="scales", at=A("c13s6", "ahlâkı", -0.1), sway=True, size=150), label="tartisma_hatirla"),
    # s7a — strateji oyunlarında 'kişisel birlik': tek hükümdar, birçok devlet
    shot("c13_game", a=A("c13s7", -0.2), tr=("fade", 0.8), at_ui=0.1, at_tip=A("c13s7", "kişisel", -0.3), at_one=A("c13s7", "hükümdar", -0.4), at_many=A("c13s7", "birçok", -0.2), step=0.3, label="oyun_paneli"),
    # s7b — oyun olarak değil, ömür olarak yaşadı
    shot("c13_life", a=A("c13s7", "Şarlken", -0.15), tr=("fade", 0.8), at_game=0.0, at_life=A("c13s7", "ömür", -0.3), label="oyun_degil_omur"),
    # s8 — kaybeden kim? o mu, yoksa tek adamın bütün dünyayı taşıyabileceği fikri mi?
    shot("wd_vs", a=A("c13s8", -0.25), tr=("fade", 0.9), size=500, gap=700, y=H * 0.45, ring_at=A("c13s8", "kaybeden", -0.1),
         left=dict(key="karl_yasli", metal="gold", name="ŞARLKEN", role="O mu?", at=A("c13s8", "mu", -0.4)),
         right=dict(draw=_idea, name="FİKİR", role="Tek adam, bütün dünya?", at=A("c13s8", "fikri", -0.2)),
         center=dict(icon="question", metal="gold", at=A("c13s8", "kaybeden", -0.1), size=220, dy=-10), label="kaybeden_kim"),
    # s9–s10 — beş cepheden birini bırakmak zorunda olsaydınız… (son çekim; kapanış compose'da)
    shot("c13_final", a=A("c13s9", -0.3), tr=("fade", 0.9), at_first=A("c13s9", "Beş", -0.05), step=0.42, at_q=A("c13s9", "hangisini", -0.2), at_comment=A("c13s9", "Yorumlarda", -0.1), at_cycle=A("c13s9", "Yorumlarda", 0.6), label="hangisini_birakirdin"),
]
