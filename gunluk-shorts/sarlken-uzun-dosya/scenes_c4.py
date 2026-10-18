"""Bölüm 4 — Worms'ta Bir Keşiş (114 sn). Ton: yargı salonu — petrol (Protestan) ↔ kırmızı (Habsburg); gerilim.
Özel çekim türleri: kinds_c4.py (c4_ önekli). Ortak yardımcılar: bw_lib.py. Simgeler: icons_b.py."""
from shots import shot
import scenes_lib  # noqa: F401  (theatre şablonu + sahne aileleri)
import kinds_c4  # noqa: F401
import icons_b  # noqa: F401
from bw_lib import anc
from sk import W, H

F = ("fade", 0.7)

SHOTS = [
    # s1 — Nisan 1521. Worms.
    shot("map", a=("c4s1", 0.0), tr=F, cams=[(0.0, (9.0, 47.5, 1.5)), (("c4s1", "1521", 0.1), (8.4, 49.6, 6.2))],
         regions=[dict(name="almanya", color="#7A6A3A", at=0.2, alpha=0.30, hatch=True)],
         cities=[dict(lon=8.36, lat=49.63, name="WORMS", kind="seat", at=("c4s1", "Worms", -0.3), side="r", size=40)],
         date=("NİSAN 1521", ("c4s1", "Nisan", 0.0)), label="worms_harita"),
    # s2a — Reichstag salonu: imparator tahtta, karşısında küçük keşiş
    shot("theatre", a=("c4s2", -0.4), tr=F, scene="reichstag", cams=[(0.0, (960, 600, 1.0)), (("c4s2", "bir", 0.2), (960, 700, 1.45))],
         p=dict(monk=True, emperor=True), label="reichstag"),
    # s2b — Karl ↔ Luther
    shot("c4_duel", a=("c4s2", "bir", -0.15), tr=("fade", 0.6),
         left=dict(key="karl_genc", name="V. KARL", role="İmparator · 21 yaşında", at=0.2, metal="gold"),
         right=dict(key="luther", name="MARTIN LUTHER", role="Keşiş", at=("c4s2", "keşiş", -0.1), plate_at=("c4s2", "Martin", -0.15), metal="teal", flip=True),
         vs_at=("c4s2", "Martin", 0.0), label="karl_luther"),
    # s3a — 95 madde
    shot("c4_theses", a=("c4s3", -0.25), tr=F, at=0.0, year_at=0.5, against_at=("c4s3", "günah", -0.1), slash_at=("c4s3", "karşı", -0.1),
         count_at=("c4s3", "doksan", -0.1), write_at=("c4s3", "maddelik", -0.2), write_dur=2.4, label="95_madde"),
    # s3b — matbaa: Wittenberg'den Almanya'ya
    shot("black", a=("c4s3", "Matbaa", -0.2), tr=F, text="[c4 matbaa-harita]", label="matbaa_yayildi"),
    # s4 — güvenli geçiş: yirmi bir gün
    shot("c4_safeconduct", a=("c4s4", -0.25), tr=F, at=0.0, seal_at=("c4s4", "sözü", 0.0), days_at=("c4s4", "yirmi", -0.05), days_dur=1.25, label="guvenli_gecis"),
    shot("black", a=("c4s5", -0.2), tr=F, text="[c4 devam]", label="devam"),
]
