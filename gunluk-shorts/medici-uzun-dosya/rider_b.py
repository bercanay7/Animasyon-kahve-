"""Atlı imparator siluet yolu (Tiziano'nun simgesel portresinden esinli, birebir kopya değil). Bölüm yazarı B (c5).
Yerel koordinat: ayak (0,0), yukarı −y, sağa bakar; toplam boy ≈ 500 birim. draw_rider(f, x, y, s, ...)."""
import math

import skia

import sk


def _sp(pts, close=True, t=0.5):
    return sk.smooth_path(pts, close, t)


def rider_paths(s=1.0):
    P = lambda *pts: [(x * s, y * s) for x, y in pts]  # noqa: E731
    horse = skia.Path()
    body = _sp(P((-100, -196), (-62, -208), (-14, -204), (36, -208), (70, -220), (92, -250), (110, -284), (128, -310), (130, -326), (141, -308),
                 (158, -292), (178, -262), (192, -238), (194, -224), (186, -214), (170, -220), (150, -242), (134, -256), (122, -244),
                 (116, -206), (106, -172), (84, -154), (46, -148), (0, -146), (-48, -150), (-88, -164), (-110, -184)), True, 0.42)
    horse.addPath(body)
    near_fore = _sp(P((84, -176), (102, -172), (104, -120), (100, -62), (104, -12), (108, 0), (86, 0), (88, -14), (86, -62), (82, -122)), True, 0.3)
    raised = _sp(P((100, -170), (124, -158), (154, -130), (166, -98), (152, -86), (140, -108), (118, -128), (96, -140)), True, 0.3)
    near_hind = _sp(P((-96, -176), (-68, -168), (-70, -116), (-90, -64), (-94, -12), (-90, 0), (-114, 0), (-114, -14), (-116, -66), (-130, -112), (-118, -160)), True, 0.3)
    far_hind = _sp(P((-60, -160), (-34, -156), (-30, -104), (-40, -54), (-36, -12), (-34, 0), (-58, 0), (-58, -14), (-60, -56), (-68, -104)), True, 0.3)
    for p_ in (near_fore, raised, near_hind, far_hind):
        horse.addPath(p_)
    tail = _sp(P((-104, -196), (-136, -190), (-170, -158), (-182, -112), (-172, -64), (-158, -84), (-160, -128), (-140, -166), (-108, -178)), True, 0.4)
    horse.addPath(tail)
    mane = _sp(P((92, -254), (104, -282), (122, -306), (126, -324), (110, -314), (96, -288), (86, -266)), True, 0.4)
    horse.addPath(mane)
    # binici (eğerde, dik)
    rider = skia.Path()
    rider.addPath(_sp(P((-26, -200), (-32, -250), (-26, -296), (-6, -318), (22, -316), (38, -292), (36, -250), (30, -200)), True, 0.45))
    rider.addCircle(10 * s, -344 * s, 16 * s)
    rider.addPath(_sp(P((-8, -346), (-6, -370), (10, -378), (28, -368), (30, -344), (16, -334)), True, 0.4))      # miğfer
    rider.addPath(_sp(P((28, -300), (52, -288), (78, -282), (84, -272), (72, -266), (48, -272), (26, -278)), True, 0.4))   # kol
    rider.addPath(_sp(P((8, -198), (44, -180), (54, -150), (46, -118), (32, -116), (32, -148), (4, -168)), True, 0.35))    # bacak
    lance = skia.Path()
    lance.moveTo(78 * s, -276 * s)
    lance.lineTo(176 * s, -498 * s)
    lance.lineTo(180 * s, -496 * s)
    lance.lineTo(84 * s, -274 * s)
    lance.close()
    lance.addPath(sk.poly_path(P((174, -498), (190, -530), (182, -492)), True))
    plume = _sp(P((16, -378), (4, -404), (-20, -424), (-48, -422), (-32, -402), (-18, -386)), True, 0.45)
    sash = sk.poly_path(P((-24, -300), (-6, -316), (34, -262), (24, -242), (6, -276)), True)
    return dict(horse=horse, rider=rider, lance=lance, plume=plume, sash=sash)


def draw_rider(f, x, y, s=1.0, col="#0A0604", rim="#C58A44", plume="#B0302A", sash="#8E1F26", face=1, alpha=1.0):
    ps = rider_paths(s)
    f.c.save()
    f.c.translate(x, y)
    f.c.scale(face, 1)
    for k in ("horse", "rider", "lance"):
        pr = skia.Paint(AntiAlias=True, Color=sk.C(rim, int(255 * alpha)))
        f.c.save(); f.c.translate(-2.4 * s, -2.2 * s)
        f.c.drawPath(ps[k], pr)
        f.c.restore()
    for k in ("horse", "rider", "lance"):
        f.c.drawPath(ps[k], skia.Paint(AntiAlias=True, Color=sk.C(col, int(255 * alpha))))
    f.c.drawPath(ps["plume"], skia.Paint(AntiAlias=True, Color=sk.C(plume, int(255 * alpha))))
    f.c.drawPath(ps["sash"], skia.Paint(AntiAlias=True, Color=sk.C(sash, int(255 * alpha))))
    f.c.restore()
