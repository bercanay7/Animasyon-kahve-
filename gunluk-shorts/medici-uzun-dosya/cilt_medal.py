"""cilt_medal — Medici cildi: bronz Rönesans portre madalyası (Pisanello / Niccolò Fiorentino tarzı: profil + kenar yazısı).

medal.py'nin parametrik profil başı (yükseklik haritası) korunur; yüzey: dökme bronz (koyu umber → altın-bronz tepeler), çukurlarda yeşil patina,
döküm gözenekleri, kenar halkası. Gerçek kişi benzerliği iddiası yok: stilize "madalya portresi".
Önbellekli yerel biçimli görüntü + bulanık gölge. draw_medal_b(): tilt (dikey eksen dönüşü), bant sınırlı parlama.
"""
import functools
import math

import cv2
import numpy as np
import skia

import cilt_medici as CM
import cilt_wall as CW
import medal
import sk
from sk import C, clamp

# Gösterim amaçlı stilize kişiler ("m_" önekli; madalya-lab'ın gerçek anahtarlarıyla çakışmaz)
medal.PEOPLE.setdefault("m_cosimo", dict(nose=26, hook=12, brow=3, lip=0, lip2=2, chin=-2, jaw=0.9, fore=3, age=0.75, jowl=0.12, neck=0.95,
                                          hair="thin", hat="cap_black", beard=None, garment="robe", mouth_open=0.0))
medal.PEOPLE.setdefault("m_lorenzo", dict(nose=4, hook=0, brow=4, lip=3, lip2=12, chin=26, jaw=1.35, fore=1, age=0.3, jowl=0.05, neck=1.2,
                                           hair="long", hat="none", beard=None, garment="fur_doublet", mouth_open=0.0))
medal.PEOPLE.setdefault("m_giovanni", dict(nose=14, hook=2, brow=3, lip=1, lip2=3, chin=0, jaw=1.1, fore=2, age=0.8, jowl=0.4, neck=1.1,
                                            hair="none", hat="flatcap", beard=None, garment="robe", mouth_open=0.0))
medal.PEOPLE.setdefault("m_lucrezia", dict(nose=10, hook=0, brow=1, lip=2, lip2=5, chin=8, jaw=0.85, fore=3, age=0.5, jowl=0.0, neck=0.9,
                                            hair="veil", hat="widow_hood", beard=None, garment="mourning_f", mouth_open=0.0))
medal.INSCR.setdefault("m_cosimo", "COSMVS · MEDICES · PATER · PATRIAE ·")
medal.INSCR.setdefault("m_lorenzo", "LAVRENTIVS · MEDICES · FLORENTINVS ·")
medal.INSCR.setdefault("m_giovanni", "IOHANNES · DE · MEDICIS ·")
medal.INSCR.setdefault("m_lucrezia", "LVCRETIA · TORNABONA ·")


@functools.lru_cache(maxsize=32)
def medal_array_b(key, metal="bronze", inscription=None, flip=False, size=720):
    """RGBA uint8 (size²): dökme bronz + patina."""
    arr = medal.medal_array(key, metal, inscription, flip)
    a = arr[..., 3]
    rgb = arr[..., :3].astype(np.float32)
    lum = rgb.mean(-1) / 255.0
    rs = np.random.RandomState(7)
    if metal == "bronze":
        pat = np.clip((0.40 - lum) / 0.26, 0, 1)
        pc = np.array([62, 96, 82], np.float32)
        rgb = rgb * (1 - 0.34 * pat[..., None]) + pc * 0.34 * pat[..., None]
        cast = CW.gn(rs, arr.shape[0], arr.shape[1], 1.1) * 0.05 + CW.lf(rs, arr.shape[0], arr.shape[1], 30) * 0.03
        rgb *= (1 + cast)[..., None]
    out = np.dstack([np.clip(rgb, 0, 255), a]).astype(np.uint8)
    if size != out.shape[0]:
        out = cv2.resize(out, (size, size), interpolation=cv2.INTER_AREA)
    return out


@functools.lru_cache(maxsize=32)
def medal_img(key, metal="bronze", inscription=None, flip=False, size=720):
    return sk.np_to_image(medal_array_b(key, metal, inscription, flip, size))


@functools.lru_cache(maxsize=32)
def medal_shadow(key, metal="bronze", inscription=None, flip=False, size=720):
    return CM.blur_sil(medal_array_b(key, metal, inscription, flip, size)[..., 3], 16.0, (14, 8, 2))


def draw_medal_b(f, key, x, y, size, metal="bronze", flip=False, alpha=1.0, tilt=0.0, glint=None, inscription=True, shadow=0.6):
    """Madalya merkezi (x,y); tilt: -1..1 (dikey eksen); glint: 0..1 yatay parlama bandı."""
    ins = medal.INSCR.get(key) if inscription else None
    img = medal_img(key, metal, ins, flip, 720)
    s = size / 720.0
    cs = max(0.05, math.cos(tilt * 0.55))
    c = f.c
    if shadow > 0:
        c.save(); c.translate(x + size * 0.035, y + size * 0.055); c.scale(s * cs, s)
        p = skia.Paint(AntiAlias=True); p.setAlphaf(clamp(shadow * alpha))
        c.drawImage(medal_shadow(key, metal, ins, flip, 720), -360, -360, CM._LIN, p)
        c.restore()
    c.save(); c.translate(x, y); c.scale(s * cs, s)
    p = skia.Paint(AntiAlias=True); p.setAlphaf(clamp(alpha))
    c.drawImage(img, -360, -360, CM._LIN, p)
    if glint is not None:
        gx = -520 + 1040 * glint
        L_, R_ = max(-380.0, gx - 140), min(380.0, gx + 140)
        if R_ > L_:
            c.save()
            c.clipRect(skia.Rect.MakeLTRB(L_, -380, R_, 380))
            c.saveLayer(skia.Rect.MakeLTRB(L_, -380, R_, 380), None)
            c.drawImage(img, -360, -360, CM._LIN, skia.Paint(AntiAlias=True))
            sh = skia.GradientShader.MakeLinear([(gx - 120, -300), (gx + 120, 300)], [C("#FFFFFF", 0), C("#FFE6B0", int(120 * alpha)), C("#FFFFFF", 0)], [0, 0.5, 1])
            c.drawRect(skia.Rect.MakeLTRB(L_, -380, R_, 380), skia.Paint(Shader=sh, BlendMode=skia.BlendMode.kSrcATop))
            c.restore()
            c.restore()
    c.restore()
