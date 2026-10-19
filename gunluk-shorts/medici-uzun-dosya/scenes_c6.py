"""c6 geçici deneme"""
from shots import shot
import cilt_medici as CM
import c6_kinds as K

SHOTS = [
    shot("skyline", ("c6s1", 0), seed=3, tod="day", cam=("pan", "r", 300), pan=300, kick="FLORANSA", label="Floransa"),
    shot("c6_valori", ("c6s1", "anlatır", 0.5), a_page=("c6s1", "anlatır", 0.5), a_med=("c6s2", "yüzü", 0.2), a_gl=("c6s2", "vakarlıydı", -0.3),
         l1=("Doğa, görünüşte ona üvey ana;", ("c6s1", "doğa", 0.3)), l2=("zihinde şefkatli bir ana.", ("c6s1", "zihne", -0.1)),
         l3=("Yüzü güzel sayılmazdı,", ("c6s2", "yüzü", 0.0)), l4=("ama saygı uyandıracak kadar vakarlıydı.", ("c6s2", "ama", -0.1)),
         cam=[(("c6s1", "anlatır", 0.5), K.look(780, 520, 1.08)), (("c6s1", "zihne", 0.0), K.look(800, 520, 1.1)), (("c6s2", "yüzü", 0.0), K.look(990, 520, 1.0)), (("c6s2", "ama", 0.0), K.look(1100, 520, 1.03)), (("c6s2", "vakarlıydı", 0.3), K.look(1200, 500, 1.1)), (("c6s3", -0.2), K.look(1340, 500, 1.18))],
         tr=("carry", 0.9, dict(strip="paper", dir="r")), link="carry", longtake=True, label="Valori sayfası + Lorenzo madalyası"),
    shot("c6_tarif", ("c6s3", -0.15), a_head=("c6s3", -0.1), a_nose=("c6s3", "basık", -0.1), a_chin=("c6s3", "öne", -0.1), a_eye=("c6s3", "zayıf", -0.1),
         a_smell=("c6s4", "koku", -0.3), a_attr=("c6s4", "Valori'ye", 0.0),
         cam=[(("c6s3", -0.15), K.look(900, 540, 1.0)), (("c6s3", "zayıf", -0.2), K.look(1000, 480, 1.1)), (("c6s4", -0.2), K.look(1060, 560, 1.0)), (("c6s5", -0.4), K.look(1120, 560, 1.07))],
         tr=("slide", 0.9, dict(dir="r")), link="dir", label="ansiklopedi tarifi, koku göstergesi"),
    shot("black", ("c6s5", -0.1), text="son", cam=("push", 0.05), label="x"),
]
