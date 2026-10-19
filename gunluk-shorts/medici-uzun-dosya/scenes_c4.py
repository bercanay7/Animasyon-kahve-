"""c4 — Kubbe ve Kefaret (1418 – 1460'lar). Parça 2 / 2. bölüm. Çekim listesi; özel türler c4_kinds.py, ortak yardımcılar p2_lib.py."""
from shots import shot
import cilt_medici as CM
import c4_kinds as K
look = K.look
SHOTS = [
    shot("p2_skyline", ("c4s1", -0.1), mode="day", tod="day", pan=240, dir=1, cam=("pan", "r", 240), labels=[dict(on="duomo", name="KUBBE", at=("c4s1", "kubbeyi", -0.1), dy=-60)],
         link=None, label="Floransa silueti: kubbeyi Medici yaptırmadı",
         over=[dict(t="palle", x=1000, y=250, size=150, at=("c4s1", "Medici", -0.1), hold=("c4s2", -0.2)), dict(t="strike", x=1000, y=250, size=120, at=("c4s1", "yaptırmadı.", -0.2))]),
    shot("c4_lonca", ("c4s2", -0.1), mode="day", cam=[(("c4s2", 0.0), look(780, 560, 1.12)), (("c4s2", "kubbeden", -0.4), look(1380, 540, 1.05)), (("c4s2", "açtı.", -0.2), look(1060, 560, 1.0))],
         tr=("light", 0.9, dict(at=(1000, 300))), link="light", label="yün loncası: kumaştan anlar, kubbeden değil"),
]
YIL_AT = [(("c4s3", "1418'de", -0.2), 1418), (("c4s4", "1420", -0.2), 1420), (("c4s8", "1436,", -0.2), 1436)]
