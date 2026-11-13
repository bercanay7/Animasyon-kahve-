"""Tarihî kişilikler (Uzun Dosya #1): Pellagra kuklalarının (kukla.py) Rönesans uyarlaması; büstler, eklemli kollar, ifadeler.
Orijin = boyun tabanı. Birim ≈ ekran pikseli (s=1'de baş ≈ 170 px). Eller dünya koordinatı olarak döner (sahne nesne taşır)."""
import math

from inkpaint import *  # noqa

# ───────────────────────── görünüşler ─────────────────────────
LOOKS = {}   # aşağıda doldurulur


def _look(name, **kw):
    base = dict(skin=SKIN, hair=INK_L, hair_style="side", hat=None, hat_col=INK, jacket=Hx("#4A4A58"), shirt=PARCH_L, tie=None, mustache=None,
                glasses=False, nose=1.0, ears=True, chin=0.0, cloak=None, collar=None, fleece=False, beard=None)
    base.update(kw)
    LOOKS[name] = base


# ── Habsburg ve akrabalar ──
_look("karl_genc", skin=Hx("#F0C29A"), hair=Hx("#8A6A44"), hair_style="page", hat="beret", hat_col=INK, jacket=CRIMSON_D, shirt=PARCH_L, nose=1.05, chin=22, collar="fur_light")
_look("karl", skin=Hx("#EDBE96"), hair=Hx("#6E5236"), hair_style="page", hat="beret", hat_col=INK, jacket=INK, shirt=PARCH_L, nose=1.12, chin=30, beard="short",
      mustache=Hx("#6E5236"), fleece=True, collar="fur_dark")
_look("karl_yasli", skin=Hx("#E8C6A4"), hair=Hx("#B9B2A4"), hair_style="page", hat="beret", hat_col=INK, jacket=INK, shirt=PARCH_L, nose=1.18, chin=34, beard="short",
      mustache=Hx("#B9B2A4"), fleece=True, collar="fur_dark", sick=0.0)
_look("karl_kron", skin=Hx("#EDBE96"), hair=Hx("#6E5236"), hair_style="page", hat="crown", hat_col=GOLD, jacket=CRIMSON, shirt=PARCH_L, nose=1.12, chin=30, beard="short",
      mustache=Hx("#6E5236"), fleece=True, collar="ermine")
_look("karl_zirh", skin=Hx("#EDBE96"), hair=Hx("#6E5236"), hair_style="page", hat="morion", hat_col=Hx("#A9AEB4"), jacket=Hx("#8E949C"), shirt=None, nose=1.12, chin=30,
      beard="short", mustache=Hx("#6E5236"), armor=True)
_look("juana", skin=Hx("#EFCBAA"), hair=Hx("#2E2420"), hair_style="veil", hat="veil", hat_col=INK, jacket=Hx("#3A2E3C"), shirt=PARCH_L, nose=0.95, chin=6, collar="white")
_look("filip_guzel", skin=Hx("#F2CDA6"), hair=Hx("#B88E4E"), hair_style="page", hat="beret", hat_col=Hx("#2B3A66"), jacket=Hx("#2B3A66"), shirt=PARCH_L, nose=1.0, chin=18,
      collar="fur_light")
_look("maximilian", skin=Hx("#E5BE9A"), hair=Hx("#9A8466"), hair_style="page", hat="beret", hat_col=CRIMSON_D, jacket=CRIMSON_D, shirt=PARCH_L, nose=1.5, chin=20, collar="fur_light")
_look("ferdinand_aragon", skin=Hx("#E2B58C"), hair=Hx("#6A5A4A"), hair_style="short", hat="crown", hat_col=GOLD, jacket=Hx("#7A2A24"), shirt=PARCH_L, nose=1.1, chin=8, collar="ermine")
_look("isabella_kastilya", skin=Hx("#F0CBA8"), hair=Hx("#7A4E2E"), hair_style="veil", hat="veil_crown", hat_col=GOLD, jacket=Hx("#7A2A24"), shirt=PARCH_L, nose=0.95, collar="white")
_look("isabella_portekiz", skin=Hx("#F2D0AE"), hair=Hx("#4A3226"), hair_style="veil", hat="french_hood", hat_col=Hx("#2E2A3C"), jacket=Hx("#2E2A3C"), shirt=PARCH_L, nose=0.9, collar="white")
_look("margarete", skin=Hx("#EFCBAA"), hair=Hx("#2E2420"), hair_style="veil", hat="veil", hat_col=INK, jacket=INK, shirt=PARCH_L, nose=1.0, collar="white")
_look("filip2", skin=Hx("#F0CBA6"), hair=Hx("#C7A15E"), hair_style="short", hat=None, jacket=INK, shirt=PARCH_L, nose=1.0, chin=26, beard="pointed", mustache=Hx("#C7A15E"),
      fleece=True, collar="ruff")
_look("ferdinand1", skin=Hx("#EDBE96"), hair=Hx("#6E5236"), hair_style="page", hat="beret", hat_col=CRIMSON_D, jacket=Hx("#5B2A2E"), shirt=PARCH_L, nose=1.1, chin=24, beard="short",
      mustache=Hx("#6E5236"), collar="fur_dark")
# ── Rakipler ve müttefikler ──
_look("fransuva", skin=Hx("#F0C29A"), hair=Hx("#3E2A1E"), hair_style="short", hat="beret", hat_col=ROYAL_D, jacket=ROYAL, shirt=PARCH_L, nose=1.65, chin=0, beard="short",
      mustache=Hx("#3E2A1E"), collar="fur_light")
_look("henry8", skin=Hx("#F2C9A2"), hair=Hx("#B4762E"), hair_style="short", hat="beret", hat_col=CRIMSON, jacket=Hx("#7A2A3A"), shirt=PARCH_L, nose=0.95, chin=-6, beard="full",
      mustache=Hx("#B4762E"), collar="fur_dark", wide=True)
_look("suleyman", skin=Hx("#E1B58B"), hair=Hx("#2E241E"), hair_style="short", hat="turban_tall", hat_col=PARCH_L, jacket=FOREST_D, shirt=GOLD_D, nose=1.2, chin=4, beard="pointed",
      mustache=Hx("#2E241E"), collar="gold_trim")
_look("barbaros", skin=Hx("#D8A57A"), hair=Hx("#A8402A"), hair_style="short", hat="turban_red", hat_col=CRIMSON, jacket=Hx("#2F4F6A"), shirt=PARCH_L, nose=1.25, chin=6, beard="full",
      mustache=Hx("#A8402A"), collar="gold_trim")
_look("pasa", skin=Hx("#DDB088"), hair=Hx("#3A2A22"), hair_style="short", hat="turban_tall", hat_col=Hx("#E9DFC6"), jacket=Hx("#6B3A4A"), shirt=GOLD_D, nose=1.15, chin=2, beard="pointed",
      mustache=Hx("#3A2A22"), collar="gold_trim")
_look("luther", skin=Hx("#E8BE98"), hair=Hx("#4A3626"), hair_style="tonsure", hat=None, jacket=Hx("#1F1A1A"), shirt=PARCH_L, nose=1.1, chin=14, collar="white", wide=True)
_look("klemens", skin=Hx("#E3BC95"), hair=Hx("#8A8A8A"), hair_style="short", hat="tiara", hat_col=GOLD_L, jacket=PARCH_L, shirt=PARCH_L, nose=1.2, chin=6, beard="full",
      mustache=Hx("#8A8A8A"), collar="gold_trim")
_look("kortes", skin=Hx("#D8A57A"), hair=Hx("#2E241E"), hair_style="short", hat="morion", hat_col=Hx("#A9AEB4"), jacket=Hx("#8E949C"), shirt=None, nose=1.1, chin=6, beard="short",
      mustache=Hx("#2E241E"), armor=True)
_look("pizarro", skin=Hx("#D8A57A"), hair=Hx("#6A5A4A"), hair_style="short", hat="morion", hat_col=Hx("#A9AEB4"), jacket=Hx("#8E949C"), shirt=None, nose=1.15, chin=4, beard="full",
      mustache=Hx("#6A5A4A"), armor=True)
_look("montezuma", skin=Hx("#C98F5E"), hair=Hx("#1F1814"), hair_style="short", hat="feather_crown", hat_col=Hx("#2FA39A"), jacket=Hx("#2FA39A"), shirt=GOLD_L, nose=1.05, chin=0, collar="gold_trim")
_look("atahualpa", skin=Hx("#C98F5E"), hair=Hx("#1F1814"), hair_style="bowl", hat="llautu", hat_col=CRIMSON, jacket=Hx("#B5532E"), shirt=GOLD_L, nose=1.1, chin=0, collar="gold_trim")
_look("fugger", skin=Hx("#EDBE96"), hair=Hx("#8E8274"), hair_style="short", hat="cap_flat", hat_col=Hx("#2B3A66"), jacket=Hx("#4A3A2E"), shirt=PARCH_L, nose=1.2, chin=6, beard="short",
      mustache=Hx("#8E8274"), collar="fur_dark")
_look("las_casas", skin=Hx("#E8BE98"), hair=Hx("#B9B2A4"), hair_style="tonsure", hat=None, jacket=Hx("#3A302A"), shirt=PARCH_L, nose=1.1, chin=8, collar="white")
_look("elcano", skin=Hx("#DDB088"), hair=Hx("#2E241E"), hair_style="short", hat="cap_flat", hat_col=Hx("#3A2E27"), jacket=Hx("#5A3E26"), shirt=PARCH_L, nose=1.1, chin=4, beard="short",
      mustache=Hx("#2E241E"))
_look("moritz", skin=Hx("#EDBE96"), hair=Hx("#4A3626"), hair_style="short", hat="beret", hat_col=Hx("#3F6445"), jacket=Hx("#3F6445"), shirt=PARCH_L, nose=1.0, chin=4, beard="short",
      mustache=Hx("#4A3626"), collar="fur_light")
_look("doria", skin=Hx("#DDB088"), hair=Hx("#8E8E8E"), hair_style="short", hat="cap_flat", hat_col=Hx("#2B3A66"), jacket=Hx("#2B3A66"), shirt=PARCH_L, nose=1.2, chin=4, beard="full",
      mustache=Hx("#8E8E8E"), collar="gold_trim")
_look("oranje", skin=Hx("#EFC7A0"), hair=Hx("#6E4A2E"), hair_style="page", hat="beret", hat_col=INK, jacket=INK, shirt=PARCH_L, nose=1.05, chin=2, beard="short",
      mustache=Hx("#6E4A2E"), collar="ruff")
_look("sepulveda", skin=Hx("#E5BE9A"), hair=Hx("#5A4636"), hair_style="short", hat="cap_flat", hat_col=INK, jacket=INK, shirt=PARCH_L, nose=1.1, chin=6, beard="short", mustache=Hx("#5A4636"), collar="white")
_look("sekreter", skin=SKIN, hair=Hx("#4A3626"), hair_style="short", hat="cap_flat", hat_col=INK, jacket=Hx("#4A4A58"), shirt=PARCH_L, nose=1.0, chin=0, collar="white")
_look("asker", skin=Hx("#E5AE82"), hair=Hx("#4A3626"), hair_style="short", hat="morion", hat_col=Hx("#A9AEB4"), jacket=Hx("#7A5A44"), shirt=None, nose=1.05, chin=2, stubble=True)
_look("elector", skin=Hx("#EDBE96"), hair=Hx("#7A6A56"), hair_style="short", hat="cap_flat", hat_col=CRIMSON_D, jacket=Hx("#5B2A2E"), shirt=PARCH_L, nose=1.15, chin=4, beard="short",
      mustache=Hx("#7A6A56"), collar="ermine")
_look("elector_b", skin=Hx("#E2B58C"), hair=Hx("#4A3626"), hair_style="short", hat="cap_flat", hat_col=ROYAL_D, jacket=ROYAL_D, shirt=PARCH_L, nose=1.05, chin=2, beard="full",
      mustache=Hx("#4A3626"), collar="ermine")
_look("elector_c", skin=Hx("#EDBE96"), hair=Hx("#9A8E7E"), hair_style="short", hat="cap_flat", hat_col=FOREST_D, jacket=FOREST_D, shirt=PARCH_L, nose=1.25, chin=6, collar="ermine")

POSE0 = dict(tilt=0.0, lean=0.0, bob=0.0, arm_l=(8.0, 6.0), arm_r=(8.0, 6.0), mouth="flat", eyes="open", brows=0.0, face=0.0,
             sick=0.0, flip=1, sweat=0.0, jaw=0.0, breathe=0.0, look=(0.0, 0.0), blush=0.0, rash=0.0)


def _rot(pts, ang, pivot):
    c, s = math.cos(ang), math.sin(ang)
    px, py = pivot
    return [(px + (x - px) * c - (y - py) * s, py + (x - px) * s + (y - py) * c) for x, y in pts]


def _hat2(ctx, H_, hat, hcol, hy, owx, sd, tt, s, L):
    dk = shade(hcol, -0.32)
    lt = shade(hcol, 0.2)
    if hat == "beret":
        shape(ctx, H_(smooth_closed([(-92, hy - 70), (-70, hy - 118), (-10, hy - 134), (60, hy - 122), (100, hy - 92), (96, hy - 74), (30, hy - 84), (-60, hy - 78)], 6)), hcol, ow=owx, seed=sd + 120,
              t=tt, wob_amp=1.3, shade=(dk, 10 * s, 0.5), hatch=(shade(hcol, 0.12), 20 * s, 0.25))
        shape(ctx, H_([(-70, hy - 72), (78, hy - 72), (74, hy - 84), (-66, hy - 84)]), shade(hcol, -0.12), ow=owx * 0.4, seed=sd + 121, t=tt, wob_amp=0.6)
        # tüy
        shape(ctx, H_(smooth_closed([(60, hy - 112), (96, hy - 150), (132, hy - 150), (112, hy - 118), (86, hy - 96)], 5)), PARCH_L, ow=owx * 0.45, seed=sd + 122, t=tt, wob_amp=0.8)
    elif hat == "cap_flat":
        shape(ctx, H_(smooth_closed([(-80, hy - 68), (-60, hy - 108), (0, hy - 116), (62, hy - 108), (84, hy - 68), (0, hy - 78)], 6)), hcol, ow=owx, seed=sd + 123, t=tt, wob_amp=1.1,
              shade=(dk, 8 * s, 0.5), hatch=(shade(hcol, 0.12), 18 * s, 0.25))
        shape(ctx, H_(ellipse_pts(0, hy - 72, 92, 12, 20)), shade(hcol, -0.1), ow=owx * 0.6, seed=sd + 124, t=tt, wob_amp=0.8)
    elif hat == "crown":
        base = [(-62, hy - 80), (62, hy - 80), (68, hy - 134), (42, hy - 112), (22, hy - 144), (0, hy - 118), (-22, hy - 144), (-42, hy - 112), (-68, hy - 134)]
        shape(ctx, H_(base), GOLD, ow=owx, seed=sd + 125, t=tt, wob_amp=0.9, shade=(GOLD_D, 8 * s, 0.55), hatch=(GOLD_D, 16 * s, 0.25))
        shape(ctx, H_([(-64, hy - 78), (64, hy - 78), (62, hy - 94), (-62, hy - 94)]), CRIMSON, ow=owx * 0.5, seed=sd + 126, t=tt, wob_amp=0.6)
        for jx in (-40, 0, 40):
            ctx.circ(*H_([(jx, hy - 86)])[0], 5.5 * s, GOLD_L)
        for jx, jy in ((-42, hy - 116), (0, hy - 124), (42, hy - 116)):
            ctx.circ(*H_([(jx, jy)])[0], 5.0 * s, CRIMSON_L)
    elif hat == "morion":
        shape(ctx, H_(smooth_closed([(-72, hy - 60), (-62, hy - 122), (-10, hy - 150), (0, hy - 170), (10, hy - 150), (62, hy - 122), (72, hy - 60)], 6)), hcol, ow=owx, seed=sd + 127, t=tt,
              wob_amp=1.0, shade=(dk, 10 * s, 0.55), hatch=(lt, 22 * s, 0.30))
        shape(ctx, H_(smooth_closed([(-118, hy - 56), (-76, hy - 74), (0, hy - 70), (76, hy - 74), (118, hy - 56), (70, hy - 46), (0, hy - 54), (-70, hy - 46)], 6)), shade(hcol, -0.08), ow=owx, seed=sd + 128,
              t=tt, wob_amp=0.9, shade=(dk, 6 * s, 0.5))
        ctx.line(H_([(0, hy - 168), (0, hy - 64)]), 6 * s, dk, 0.8)
    elif hat in ("veil", "veil_crown"):
        veil = [(-96, hy + 96), (-98, hy - 20), (-72, hy - 104), (0, hy - 134), (72, hy - 104), (98, hy - 20), (96, hy + 96), (74, hy + 44), (68, hy - 28), (0, hy - 76), (-68, hy - 28), (-74, hy + 44)]
        shape(ctx, H_(veil), hcol, ow=owx, seed=sd + 129, t=tt, wob_amp=1.3, smooth=True, shade=(dk, 10 * s, 0.5), hatch=(lt, 22 * s, 0.22))
        if hat == "veil_crown":
            base = [(-46, hy - 112), (46, hy - 112), (50, hy - 150), (28, hy - 130), (12, hy - 158), (0, hy - 136), (-12, hy - 158), (-28, hy - 130), (-50, hy - 150)]
            shape(ctx, H_(base), GOLD, ow=owx * 0.8, seed=sd + 130, t=tt, wob_amp=0.7, shade=(GOLD_D, 6 * s, 0.5))
    elif hat == "french_hood":
        shape(ctx, H_([(-94, hy + 80), (-96, hy - 24), (-72, hy - 100), (0, hy - 128), (72, hy - 100), (96, hy - 24), (94, hy + 80), (70, hy + 40), (64, hy - 30), (0, hy - 74), (-64, hy - 30), (-70, hy + 40)]),
              hcol, ow=owx, seed=sd + 131, t=tt, wob_amp=1.2, smooth=True, shade=(dk, 10 * s, 0.5))
        arc = [(-66, hy - 28), (-46, hy - 62), (0, hy - 78), (46, hy - 62), (66, hy - 28)]
        ctx.line(H_(arc), 12 * s, GOLD_D, 1.0, cap=True)
        ctx.line(H_(arc), 6 * s, GOLD_L, 1.0, cap=True)
        for ax, ay in arc[1:-1]:
            ctx.circ(*H_([(ax, ay)])[0], 4.2 * s, PARCH_L)
    elif hat == "turban_tall":
        shape(ctx, H_(smooth_closed([(-60, hy - 68), (-54, hy - 160), (0, hy - 182), (54, hy - 160), (60, hy - 68), (0, hy - 80)], 6)), hcol, ow=owx, seed=sd + 132, t=tt, wob_amp=1.2,
              shade=(shade(hcol, -0.22), 10 * s, 0.5))
        for k in range(5):
            yy = hy - 92 - k * 20
            ctx.line(H_([(-56 + k * 2, yy), (0, yy - 14), (56 - k * 2, yy)]), 3.4 * s, shade(hcol, -0.28), 0.85, cap=True)
        shape(ctx, H_([(-62, hy - 70), (62, hy - 70), (60, hy - 86), (-60, hy - 86)]), GOLD_D, ow=owx * 0.5, seed=sd + 133, t=tt, wob_amp=0.6)
        shape(ctx, H_(smooth_closed([(-6, hy - 176), (4, hy - 214), (22, hy - 232), (14, hy - 196), (8, hy - 172)], 5)), PARCH_L, ow=owx * 0.5, seed=sd + 134, t=tt, wob_amp=0.6)
        ctx.circ(*H_([(0, hy - 92)])[0], 6.5 * s, CRIMSON_L)
    elif hat == "turban_red":
        shape(ctx, H_(smooth_closed([(-68, hy - 66), (-62, hy - 120), (0, hy - 138), (62, hy - 120), (68, hy - 66), (0, hy - 78)], 6)), hcol, ow=owx, seed=sd + 135, t=tt, wob_amp=1.2,
              shade=(shade(hcol, -0.25), 9 * s, 0.5))
        for k in range(4):
            ctx.line(H_([(-60 + k * 3, hy - 78 - k * 14), (0, hy - 90 - k * 14), (60 - k * 3, hy - 78 - k * 14)]), 3.2 * s, shade(hcol, -0.3), 0.85, cap=True)
        shape(ctx, H_(smooth_closed([(56, hy - 86), (96, hy - 76), (112, hy - 40), (86, hy - 58)], 5)), hcol, ow=owx * 0.6, seed=sd + 136, t=tt, wob_amp=0.8)
    elif hat == "tiara":
        tiers = [(0, 66, 40), (1, 52, 36), (2, 38, 34)]
        yy = hy - 74
        for i, (k, w_, h_) in enumerate(tiers):
            shape(ctx, H_([(-w_, yy), (w_, yy), (w_ * 0.84, yy - h_), (-w_ * 0.84, yy - h_)]), GOLD_L if i % 2 == 0 else GOLD, ow=owx * 0.7, seed=sd + 137 + i, t=tt, wob_amp=0.8,
                  shade=(GOLD_D, 6 * s, 0.5))
            ctx.line(H_([(-w_ * 0.9, yy - h_ * 0.5), (w_ * 0.9, yy - h_ * 0.5)]), 4 * s, CRIMSON_L, 0.9, cap=False)
            yy -= h_ - 2
        shape(ctx, H_(smooth_closed([(-30, yy), (30, yy), (16, yy - 40), (0, yy - 52), (-16, yy - 40)], 5)), GOLD, ow=owx * 0.7, seed=sd + 141, t=tt, wob_amp=0.6)
        ctx.line(H_([(0, yy - 52), (0, yy - 78)]), 5 * s, GOLD_D, 1.0)
        ctx.line(H_([(-12, yy - 66), (12, yy - 66)]), 5 * s, GOLD_D, 1.0)
    elif hat == "feather_crown":
        cols = [Hx("#2FA39A"), Hx("#C8372D"), Hx("#E9C44C"), Hx("#2F7A5A"), Hx("#C8372D"), Hx("#2FA39A")]
        for i in range(11):
            a_ = -80 + i * 16
            ar = math.radians(a_)
            bx, by = math.sin(ar) * 56, hy - 78 - math.cos(ar) * 10
            tx_, ty_ = math.sin(ar) * 150, hy - 78 - math.cos(ar) * 96 - 36
            c_ = cols[i % len(cols)]
            shape(ctx, H_(smooth_closed([(bx - 9, by), (tx_ - 12, ty_), (tx_, ty_ - 14), (tx_ + 12, ty_), (bx + 9, by)], 5)), c_, ow=owx * 0.55, seed=sd + 142 + i, t=tt, wob_amp=0.8)
        shape(ctx, H_([(-62, hy - 68), (62, hy - 68), (58, hy - 90), (-58, hy - 90)]), GOLD, ow=owx * 0.6, seed=sd + 160, t=tt, wob_amp=0.6)
    elif hat == "llautu":
        shape(ctx, H_([(-78, hy - 62), (78, hy - 62), (76, hy - 84), (-76, hy - 84)]), hcol, ow=owx * 0.8, seed=sd + 161, t=tt, wob_amp=0.8, shade=(dk, 6 * s, 0.5))
        shape(ctx, H_([(-20, hy - 62), (20, hy - 62), (24, hy - 30), (-24, hy - 30)]), CRIMSON, ow=owx * 0.5, seed=sd + 162, t=tt, wob_amp=0.6)
        for k in range(7):
            ctx.line(H_([(-18 + k * 6, hy - 30), (-18 + k * 6, hy - 14)]), 2.6 * s, CRIMSON_D, 0.9, cap=True)
        ctx.circ(*H_([(0, hy - 74)])[0], 5.0 * s, GOLD_L)


def _collar(ctx, WP, W_, L, owx, sd, tt, s, tw):
    kind = L.get("collar")
    if not kind:
        return
    if kind == "white":
        col = PARCH_L
        shape(ctx, WP([(-40, -12), (-4, 10), (-26, 30), (-52, 2)]), col, ow=owx * 0.5, seed=sd + 8, t=tt, wob_amp=0.8)
        shape(ctx, WP([(40, -12), (4, 10), (26, 30), (52, 2)]), col, ow=owx * 0.5, seed=sd + 9, t=tt, wob_amp=0.8)
    elif kind in ("fur_light", "fur_dark", "ermine"):
        base = {"fur_light": Hx("#CDB58A"), "fur_dark": Hx("#5A4636"), "ermine": PARCH_L}[kind]
        band = [(-tw * 0.98, 6), (-tw * 0.62, -16), (-30, -22), (0, -14), (30, -22), (tw * 0.62, -16), (tw * 0.98, 6), (tw * 0.84, 46), (tw * 0.34, 78), (0, 118),
                (-tw * 0.34, 78), (-tw * 0.84, 46)]
        inner = [(-tw * 0.70, 10), (-30, -8), (0, 0), (30, -8), (tw * 0.70, 10), (tw * 0.50, 44), (0, 102), (-tw * 0.50, 44)]
        P_ = shape(ctx, WP(band), base, ow=owx * 0.7, seed=sd + 8, t=tt, wob_amp=1.6, smooth=True, hatch=(shade(base, -0.28), 12 * s, 0.55))
        shape(ctx, WP(inner), L["jacket"], ow=owx * 0.5, seed=sd + 9, t=tt, wob_amp=1.0, smooth=True)
        if kind == "ermine":
            for i in range(16):
                a_ = i / 15.0
                bx = -tw * 0.86 + a_ * tw * 1.72
                by = 10 + 40 * (1 - abs(2 * a_ - 1)) ** 0.8 * 0.9
                ctx.poly([(bx, by), (bx + 5, by + 20), (bx - 5, by + 20)] and WP([(bx, by), (bx + 5, by + 22), (bx - 5, by + 22)]), INK, 0.9)
    elif kind == "ruff":
        pts = []
        n = 36
        for i in range(n + 1):
            a_ = math.pi * i / n
            r = 88 + 7 * math.sin(i * 1.7)
            pts.append((math.cos(a_ + math.pi) * r, -14 + math.sin(a_ + math.pi) * 26 * -1))
        pts2 = [(x, y + 34) for x, y in reversed(pts)]
        shape(ctx, WP(pts + pts2), PARCH_L, ow=owx * 0.55, seed=sd + 8, t=tt, wob_amp=0.8, smooth=True, hatch=(PARCH_DD, 10 * s, 0.35))
    elif kind == "gold_trim":
        for sx_ in (-1, 1):
            ctx.line(WP([(sx_ * 34, -10), (sx_ * 6, 112)]), 10 * s, GOLD_D, 1.0, cap=True)
            ctx.line(WP([(sx_ * 34, -10), (sx_ * 6, 112)]), 5 * s, GOLD_L, 1.0, cap=True)


def bust(ctx, x, y, s, look, pose=None, t=0.0, seed=0, ow=8.0):
    """Büst çizer. Dönüş: dict(handL, handR, head) dünya koordinatları (nesne taşımak için)."""
    L = LOOKS[look] if isinstance(look, str) else look
    P = dict(POSE0)
    if pose:
        P.update(pose)
    fl = P["flip"]
    kid = L.get("kid", False)
    tt = tq(t)
    br = 1.0 + 0.012 * math.sin(tt * 2.6 + seed) + P["breathe"]
    bob = P["bob"] + 2.0 * math.sin(tt * 2.2 + seed * 1.7)
    ox, oy = x + P["lean"] * s, y + bob * s

    def W_(px, py):      # yerel → dünya (yatay çevirme + ölçek)
        return (ox + px * s * fl, oy + py * s)

    def WP(pts):
        return [W_(a, b) for a, b in pts]

    sk = L["skin"]
    skd = shade(sk, -0.16)
    sick = clamp(P["sick"])
    if sick > 0:
        sk = mix(sk, SKIN_SICK, 0.75 * sick)
        skd = shade(sk, -0.16)
    sd = seed * 13 + 5
    owx = ow * s * (0.85 if kid else 1.0)
    scale_t = 0.92 if kid else 1.0

    # ── gövde ──
    tw = 118 * scale_t * (1.12 if L.get('wide') else 1.0)
    tor = [(-26, -10), (26, -10), (tw * 0.86, 2), (tw * 1.16, 34), (tw * 1.14, 110), (tw * 0.98, 250), (-tw * 0.98, 250),
           (-tw * 1.14, 110), (-tw * 1.16, 34), (-tw * 0.86, 2)]
    jac = L["jacket"]
    torP = shape(ctx, WP([(a * 1, b * br if b > 0 else b) for a, b in tor]), jac, ow=owx, seed=sd, t=tt, wob_amp=1.5, smooth=True,
                 shade=(shade(jac, -0.30), 14 * s, 0.55), hatch=(shade(jac, -0.22), 24 * s, 0.35))
    if L.get("stripe"):                     # mahkûm çizgileri
        c = Clip(ctx, torP)
        if c.ok:
            yy = -10.0
            while yy < 260:
                c.poly(WP([(-200, yy), (200, yy), (200, yy + 17), (-200, yy + 17)]), L["stripe"], 0.92)
                yy += 36
            c.done()
    if L.get("apron"):
        ap = WP([(-tw * 0.66, 70), (tw * 0.66, 70), (tw * 0.8, 250), (-tw * 0.8, 250)])
        shape(ctx, ap, L["apron"], ow=owx * 0.7, seed=sd + 1, t=tt, wob_amp=1.2, hatch=(shade(L["apron"], -0.15), 26 * s, 0.30))
    # gömlek V + yaka + kravat
    if L.get("shirt") is not None and not L.get("stripe") and not L.get("apron"):
        v = WP([(-30, -8), (30, -8), (0, 112)])
        shape(ctx, v, L["shirt"], ow=owx * 0.6, seed=sd + 2, t=tt, wob_amp=1.0)
        shape(ctx, WP([(-34, -10), (-6, 8), (-30, 26)]), shade(L["shirt"], -0.05), ow=owx * 0.5, seed=sd + 3, t=tt, wob_amp=0.8)
        shape(ctx, WP([(34, -10), (6, 8), (30, 26)]), shade(L["shirt"], -0.05), ow=owx * 0.5, seed=sd + 4, t=tt, wob_amp=0.8)
        if L.get("tie") == "bow":
            tc = L["tie_col"]
            shape(ctx, WP([(0, 14), (-34, 0), (-34, 30)]), tc, ow=owx * 0.55, seed=sd + 5, t=tt, wob_amp=0.8)
            shape(ctx, WP([(0, 14), (34, 0), (34, 30)]), tc, ow=owx * 0.55, seed=sd + 6, t=tt, wob_amp=0.8)
            shape(ctx, WP(ellipse_pts(0, 15, 9, 11, 12)), shade(tc, -0.2), ow=owx * 0.4, seed=sd + 7, t=tt, wob_amp=0.5)
        elif L.get("tie") == "long":
            tc = L["tie_col"]
            shape(ctx, WP([(-9, 10), (9, 10), (14, 100), (0, 118), (-14, 100)]), tc, ow=owx * 0.55, seed=sd + 5, t=tt, wob_amp=0.8,
                  hatch=(shade(tc, -0.25), 14 * s, 0.4))
    if L.get("armor"):                       # göğüs zırhı: çelik parlaklık bantları + orta sırt
        c = Clip(ctx, torP)
        if c.ok:
            c.poly(WP([(-80, 0), (-30, 0), (-46, 250), (-110, 250)]), shade(jac, 0.30), 0.55)
            c.poly(WP([(30, 0), (80, 0), (110, 250), (46, 250)]), shade(jac, -0.25), 0.55)
            c.line(WP([(0, 6), (0, 250)]), 7 * s, shade(jac, -0.40), 0.8)
            c.done()
        for rx_ in (-62, 62):
            for ry_ in (60, 140):
                ctx.circ(*W_(rx_, ry_), 4.2 * s, shade(jac, 0.35))
    _collar(ctx, WP, W_, L, owx, sd, tt, s, tw)
    if L.get("fleece"):                       # Altın Post Nişanı zinciri + koç kolye
        ch = [(-70, -2), (-52, 40), (-30, 80), (-10, 110), (0, 126)]
        chain = ch + [(-x, y) for x, y in reversed(ch[:-1])]
        for i in range(len(chain) - 1):
            a_, b_ = W_(*chain[i]), W_(*chain[i + 1])
            ctx.line([a_, b_], 9 * s, GOLD_D, 1.0, cap=True)
            ctx.line([a_, b_], 5 * s, GOLD_L, 1.0, cap=True)
        px_, py_ = W_(0, 146)
        shape(ctx, WP(ellipse_pts(0, 146, 17, 19, 12)), GOLD_L, ow=owx * 0.5, seed=sd + 41, t=tt, wob_amp=0.5)
        ctx.circ(px_, py_, 5.5 * s, CRIMSON_D)

    # ── kollar ──
    hands = {}
    for side, key in ((-1, "arm_l"), (1, "arm_r")):
        a1, a2 = P[key]
        sh_x = side * tw * 0.96
        sh_y = 36.0
        upper, fore = 112.0 * scale_t, 104.0 * scale_t
        d1 = (math.sin(math.radians(a1)) * side, math.cos(math.radians(a1)))
        e = (sh_x + d1[0] * upper, sh_y + d1[1] * upper)
        d2 = (math.sin(math.radians(a1 + a2)) * side, math.cos(math.radians(a1 + a2)))
        h = (e[0] + d2[0] * fore, e[1] + d2[1] * fore)
        rU, rF = 27 * scale_t, 22 * scale_t
        shape(ctx, WP(capsule((sh_x, sh_y), e, rU, rF)), jac, ow=owx, seed=sd + 20 + side, t=tt, wob_amp=1.3,
              shade=(shade(jac, -0.30), 8 * s, 0.5))
        shape(ctx, WP(capsule(e, h, rF, rF * 0.92)), shade(jac, -0.06), ow=owx, seed=sd + 24 + side, t=tt, wob_amp=1.3,
              shade=(shade(jac, -0.30), 7 * s, 0.5))
        hp = (h[0] + d2[0] * 14, h[1] + d2[1] * 14)
        hsk = sk
        shape(ctx, WP(ellipse_pts(hp[0], hp[1], 25 * scale_t, 25 * scale_t, 16)), hsk, ow=owx * 0.85, seed=sd + 28 + side, t=tt, wob_amp=1.0,
              shade=(skd, 6 * s, 0.55))
        if P["rash"] > 0 or sick > 0.4:
            rr = max(P["rash"], sick * 0.8)
            for i in range(5):
                rx = hp[0] + (rng_hash(sd, i, side + 3) - 0.5) * 30
                ry = hp[1] + (rng_hash(sd, i, side + 9) - 0.5) * 30
                ctx.poly(blob(*W_(rx, ry), (5 + 3 * rng_hash(sd, i, 4)) * s, (4 + 3 * rng_hash(sd, i, 6)) * s, 8, 0.25, sd + i), BRICK, 0.85 * rr)
        hands[key] = W_(hp[0], hp[1])

    # ── boyun + kafa (kafa boyun tabanı çevresinde eğilir) ──
    shape(ctx, WP([(-20, -46), (20, -46), (24, 4), (-24, 4)]), skd, ow=owx * 0.8, seed=sd + 30, t=tt, wob_amp=1.0)
    hs = 0.86 if kid else 1.0
    hy = -122 * (0.9 if kid else 1.0)
    hr = 82.0                          # ölçekleme H_ içinde yapılır
    piv = (0, -30)
    ang = math.radians(P["tilt"])

    def H_(pts):
        q = [(px * hs, (py - hy) * hs + hy) for px, py in pts]
        return WP(_rot(q, ang, piv))

    fx = P["face"]
    ear_l = ellipse_pts(-hr * 0.98, hy + 6, 14, 22, 12)
    ear_r = ellipse_pts(hr * 0.98, hy + 6, 14, 22, 12)
    if L.get("ears", True):
        shape(ctx, H_(ear_l), sk, ow=owx * 0.7, seed=sd + 31, t=tt, wob_amp=0.8)
        shape(ctx, H_(ear_r), sk, ow=owx * 0.7, seed=sd + 32, t=tt, wob_amp=0.8)
    chn = L.get("chin", 0.0)
    head = smooth_closed([(0, hy - 94), (62, hy - 74), (80, hy - 8), (62, hy + 56 + chn * 0.4), (0, hy + 84 + chn), (-62, hy + 56 + chn * 0.4), (-80, hy - 8), (-62, hy - 74)], 6)
    headP = shape(ctx, H_(head), sk, ow=owx * 1.05, seed=sd + 33, t=tt, wob_amp=1.4,
                  shade=(skd, 12 * s, 0.50), wash=(shade(sk, 0.08), shade(sk, -0.05), 0.40))
    # yanak kızarıklığı / döküntü
    if P["blush"] > 0 or sick > 0:
        bl = P["blush"]
        for sx_ in (-1, 1):
            ctx.poly(wob(H_(ellipse_pts(sx_ * 46 + fx * 8, hy + 34, 17, 12, 12)), 0.6, sd + 40 + sx_, tt), mix(sk, BRICK, 0.55), 0.55 * bl)
    if sick > 0.35 or P["rash"] > 0:
        rr = max(P["rash"], sick * 0.9)
        for i in range(7):
            rx = (rng_hash(sd, i, 21) - 0.5) * 100 + fx * 6
            ry = hy + 6 + rng_hash(sd, i, 22) * 70
            cx_, cy_ = H_([(rx, ry)])[0]
            ctx.poly(blob(cx_, cy_, (6 + 4 * rng_hash(sd, i, 4)) * s, (5 + 3 * rng_hash(sd, i, 6)) * s, 8, 0.25, sd + i), BRICK, 0.85 * rr)

    # ── burun, gözler, kaşlar, ağız ──
    nz = L.get("nose", 1.0)
    nose_c = (fx * 16, hy + 20)
    nP = shape(ctx, H_(ellipse_pts(nose_c[0], nose_c[1], 17 * nz, 22 * nz, 16)), mix(sk, BRICK, 0.10 + 0.25 * P["blush"]), ow=owx * 0.8,
               seed=sd + 50, t=tt, wob_amp=0.8, shade=(skd, 6 * s, 0.5))
    eye_y = hy - 14
    gx, gy = P["look"]
    for sx_ in (-1, 1):
        ex = sx_ * 32 + fx * 10
        e = P["eyes"]
        if e == "blink" or (e == "open" and (rng_hash(seed, int(tt * 3.0), 77) > 0.965)):
            pts = H_([(ex - 15, eye_y), (ex, eye_y + 6), (ex + 15, eye_y)])
            ink_line(ctx, pts, 6.5 * s, INK, sd + 60 + sx_, tt, 0.4, smooth=True)
        elif e == "wide":
            shape(ctx, H_(ellipse_pts(ex, eye_y, 18, 21, 14)), CREAM, ow=owx * 0.5, seed=sd + 61 + sx_, t=tt, wob_amp=0.5)
            ctx.poly(H_(ellipse_pts(ex + gx * 6, eye_y + gy * 6, 7, 7, 10)), INK)
        elif e == "squint":
            ink_line(ctx, H_([(ex - 15, eye_y + 3), (ex + 15, eye_y - 3 * sx_)]), 6.5 * s, INK, sd + 62 + sx_, tt, 0.4)
        elif e == "spiral":
            pts = []
            for k in range(26):
                a = k * 0.55
                r = 2.5 + k * 0.62
                pts.append((ex + r * math.cos(a), eye_y + r * math.sin(a)))
            ink_line(ctx, H_(pts), 4.2 * s, INK, sd + 63 + sx_, tt, 0.2)
        elif e == "sad":
            shape(ctx, H_(ellipse_pts(ex, eye_y + 3, 12, 14, 12)), CREAM, ow=owx * 0.4, seed=sd + 64 + sx_, t=tt, wob_amp=0.4)
            ctx.poly(H_(ellipse_pts(ex + gx * 4, eye_y + 5 + gy * 4, 6.5, 7.5, 10)), INK)
        else:
            ctx.poly(H_(ellipse_pts(ex + gx * 3, eye_y + gy * 3, 8.5, 10.5, 12)), INK)
            ctx.poly(H_(ellipse_pts(ex + gx * 3 - 3, eye_y + gy * 3 - 4, 2.8, 2.8, 8)), CREAM)
        # kaşlar: brows>0 kaldır, <0 çat/üzgün (iç uç yukarı)
        b = P["brows"]                      # >0 yukarı (şaşkın), <0 üzgün/endişeli (iç uçlar yukarı)
        by = eye_y - 30 - 9 * max(0.0, b)
        w_ = 10.0 * max(0.0, -b)
        k_ = 1 if sx_ == -1 else -1         # sol kaş: dış uç aşağı; sağ kaş: dış uç aşağı (iç uçlar yukarı)
        pa = (ex - 19, by + w_ * k_)
        pb = (ex + 19, by - w_ * k_)
        ink_line(ctx, H_([pa, ((pa[0] + pb[0]) / 2, (pa[1] + pb[1]) / 2 - 5), pb]), 9 * s * (1.2 if not kid else 1.0), L["hair"] if L.get("hair") else INK,
                 sd + 66 + sx_, tt, 0.4, smooth=True)
    # gözlük
    if L.get("glasses"):
        for sx_ in (-1, 1):
            ex = sx_ * 32 + fx * 10
            ring = ellipse_pts(ex, eye_y, 27, 27, 22)
            ink_line(ctx, H_(ring + [ring[0]]), 6.5 * s, INK, sd + 70 + sx_, tt, 0.4)
        ink_line(ctx, H_([(-6 + fx * 10, eye_y), (6 + fx * 10, eye_y)]), 6 * s, INK, sd + 72, tt, 0.2)
    # ağız
    my = hy + 56 + chn * 0.45
    mo = P["mouth"]
    mx = fx * 10
    jaw = P["jaw"]
    if mo == "open":
        mp = H_(ellipse_pts(mx, my + 4 + jaw * 6, 22, 12 + 16 * jaw, 14))
        shape(ctx, mp, Hx("#4A1F18"), ow=owx * 0.55, seed=sd + 80, t=tt, wob_amp=0.6)
        ctx.poly(H_(ellipse_pts(mx, my + 14 + jaw * 12, 12, 6, 10)), BRICK_D, 0.8)
    elif mo == "oh":
        shape(ctx, H_(ellipse_pts(mx, my + 6, 11, 14, 12)), Hx("#4A1F18"), ow=owx * 0.5, seed=sd + 80, t=tt, wob_amp=0.5)
    elif mo == "smile":
        ink_line(ctx, H_([(mx - 26, my - 2), (mx, my + 14), (mx + 26, my - 2)]), 6.5 * s, INK, sd + 81, tt, 0.4, smooth=True)
    elif mo == "worry":
        ink_line(ctx, H_([(mx - 24, my + 10), (mx, my - 3), (mx + 24, my + 10)]), 6.5 * s, INK, sd + 82, tt, 0.4, smooth=True)
    elif mo == "chew":
        k = math.sin(tt * 14.0)
        shape(ctx, H_(ellipse_pts(mx, my + 5, 20, 5 + 6 * (0.5 + 0.5 * k), 12)), Hx("#4A1F18"), ow=owx * 0.5, seed=sd + 83, t=tt, wob_amp=0.5)
    elif mo == "gulp":
        ink_line(ctx, H_([(mx - 20, my + 4), (mx, my + 8), (mx + 20, my + 4)]), 7 * s, INK, sd + 84, tt, 0.4, smooth=True)
        ctx.poly(H_(ellipse_pts(mx + 22, my - 6, 11, 11, 10)), skd, 0.55)
        ctx.poly(H_(ellipse_pts(mx - 22, my - 6, 11, 11, 10)), skd, 0.55)
    else:
        ink_line(ctx, H_([(mx - 20, my + 4), (mx + 20, my + 4)]), 6.5 * s, INK, sd + 85, tt, 0.4)
    # bıyık / sakal
    L_m = L.get("mustache")
    if L_m is not None and not kid:
        for sx_ in (-1, 1):
            pm = H_([(mx + sx_ * 2, my - 12), (mx + sx_ * 30, my - 18), (mx + sx_ * 52, my - 4), (mx + sx_ * 30, my - 6)])
            shape(ctx, pm, L_m, ow=owx * 0.35, seed=sd + 90 + sx_, t=tt, wob_amp=0.8, smooth=True)
    bd = L.get("beard")
    if bd == "short":
        shape(ctx, H_([(-66, hy + 26), (-46, my + 6), (0, my + 18 + chn * 0.2), (46, my + 6), (66, hy + 26), (54, hy + 72 + chn), (0, hy + 96 + chn), (-54, hy + 72 + chn)]),
              L["hair"], ow=owx * 0.5, seed=sd + 95, t=tt, wob_amp=1.0, smooth=True, hatch=(shade(L["hair"], -0.2), 9 * s, 0.4))
        ink_line(ctx, H_([(mx - 18, my + 8), (mx + 18, my + 8)]), 6 * s, PARCH_L if mo == "flat" else INK, sd + 97, tt, 0.3)
    elif bd == "pointed":
        shape(ctx, H_([(-26, my + 10), (26, my + 10), (14, hy + 100 + chn), (0, hy + 128 + chn), (-14, hy + 100 + chn)]), L["hair"], ow=owx * 0.45, seed=sd + 95, t=tt,
              wob_amp=0.8, smooth=True, hatch=(shade(L["hair"], -0.2), 8 * s, 0.4))
    elif bd == "goatee":
        shape(ctx, H_([(-20, my + 12), (20, my + 12), (14, my + 52), (-14, my + 52)]), L["hair"], ow=owx * 0.4, seed=sd + 95, t=tt, wob_amp=0.8, smooth=True)
    elif bd == "full":
        shape(ctx, H_([(-70, hy + 18), (-40, my + 4), (0, my + 22), (40, my + 4), (70, hy + 18), (58, hy + 76), (0, hy + 104), (-58, hy + 76)]),
              L["hair"], ow=owx * 0.5, seed=sd + 96, t=tt, wob_amp=1.0, smooth=True)
        # ağzı sakalın üstüne yeniden çiz
        ink_line(ctx, H_([(mx - 18, my + 8), (mx + 18, my + 8)]), 6 * s, CREAM if mo == "flat" else INK, sd + 97, tt, 0.3)
    if L.get("stubble"):
        for i in range(34):
            sx_ = (rng_hash(sd, i, 31) - 0.5) * 100
            sy_ = hy + 40 + rng_hash(sd, i, 32) * 44
            if abs(sx_) < 54:
                ctx.circ(*H_([(sx_, sy_)])[0], 2.4 * s, INK_L, 0.55)

    # ── saç / şapka ──
    hs_ = L.get("hair_style")
    hc = L["hair"]
    top = hy - 94
    if hs_ in ("side", "short", "kid", "kid_long", "curly", "bald_sides", "bun", "braid"):
        if hs_ == "side":
            hp_ = [(-82, hy - 8), (-70, hy - 70), (-20, top - 6), (50, top - 4), (80, hy - 40), (78, hy - 4), (60, hy - 50), (-4, hy - 56), (-56, hy - 40)]
        elif hs_ == "short":
            hp_ = [(-80, hy - 6), (-70, hy - 72), (-10, top - 4), (60, top + 2), (82, hy - 16), (66, hy - 54), (0, hy - 62), (-60, hy - 52)]
        elif hs_ == "kid":
            hp_ = [(-80, hy - 10), (-68, hy - 74), (-4, top - 8), (64, hy - 72), (82, hy - 10), (60, hy - 46), (4, hy - 58), (-58, hy - 46)]
        elif hs_ == "kid_long":
            hp_ = [(-84, hy + 40), (-80, hy - 40), (-64, hy - 78), (0, top - 10), (66, hy - 78), (82, hy - 40), (86, hy + 40), (66, hy - 34), (4, hy - 58), (-62, hy - 34)]
        elif hs_ == "curly":
            hp_ = [(-84, hy - 6), (-78, hy - 62), (-50, top - 10), (0, top - 22), (52, top - 10), (80, hy - 62), (86, hy - 6), (66, hy - 48), (0, hy - 60), (-66, hy - 48)]
        elif hs_ == "bald_sides":
            hp_ = [(-84, hy - 2), (-76, hy - 36), (-60, hy - 30), (-66, hy + 14), (-80, hy + 14)]
        elif hs_ == "bun":
            hp_ = [(-82, hy - 4), (-70, hy - 74), (-4, top - 8), (66, hy - 74), (82, hy - 4), (62, hy - 48), (0, hy - 60), (-60, hy - 48)]
            shape(ctx, H_(ellipse_pts(0, top - 22, 30, 26, 14)), hc, ow=owx * 0.8, seed=sd + 100, t=tt, wob_amp=0.8)
        else:  # braid
            hp_ = [(-82, hy - 4), (-70, hy - 74), (-4, top - 8), (66, hy - 74), (82, hy - 4), (62, hy - 48), (0, hy - 60), (-60, hy - 48)]
            shape(ctx, H_([(-72, hy + 10), (-92, hy + 70), (-76, hy + 160), (-58, hy + 150), (-66, hy + 70)]), hc, ow=owx * 0.8, seed=sd + 101, t=tt, wob_amp=1.0, smooth=True)
        shape(ctx, H_(hp_), hc, ow=owx * 0.9, seed=sd + 102, t=tt, wob_amp=1.2, smooth=True, shade=(shade(hc, -0.25), 7 * s, 0.4))
        if hs_ == "bald_sides" and L.get("hat") is None:      # tepe kel: ışık yansıması
            ctx.poly(wob(H_(ellipse_pts(-18, top + 12, 18, 9, 10, -0.5)), 0.4, sd, tt), CREAM, 0.30)
    if hs_ in ("page", "tonsure", "veil", "bowl"):
        if hs_ == "page":
            hp_ = [(-88, hy + 24), (-86, hy - 44), (-66, hy - 88), (0, top - 10), (66, hy - 88), (86, hy - 44), (88, hy + 24), (72, hy + 4), (64, hy - 40), (0, hy - 62), (-64, hy - 40), (-72, hy + 4)]
            shape(ctx, H_(hp_), hc, ow=owx * 0.9, seed=sd + 102, t=tt, wob_amp=1.2, smooth=True, shade=(shade(hc, -0.25), 7 * s, 0.4))
        elif hs_ == "bowl":
            hp_ = [(-86, hy + 30), (-84, hy - 40), (-64, hy - 86), (0, top - 8), (64, hy - 86), (84, hy - 40), (86, hy + 30), (70, hy + 10), (62, hy - 44), (0, hy - 66), (-62, hy - 44), (-70, hy + 10)]
            shape(ctx, H_(hp_), hc, ow=owx * 0.9, seed=sd + 102, t=tt, wob_amp=1.0, smooth=True, shade=(shade(hc, -0.25), 7 * s, 0.4))
        elif hs_ == "tonsure":
            for sx_ in (-1, 1):
                shape(ctx, H_([(sx_ * 84, hy + 14), (sx_ * 83, hy - 22), (sx_ * 72, hy - 42), (sx_ * 67, hy - 16), (sx_ * 72, hy + 10)]), hc, ow=owx * 0.7, seed=sd + 102 + sx_, t=tt,
                      wob_amp=0.8, smooth=True, shade=(shade(hc, -0.25), 4 * s, 0.4))
            ctx.poly(wob(H_(ellipse_pts(-16, top + 16, 20, 9, 10, -0.4)), 0.4, sd, tt), PARCH_L, 0.30)
        else:  # veil altı saç
            for sx_ in (-1, 1):
                shape(ctx, H_([(sx_ * 80, hy - 40), (sx_ * 88, hy + 52), (sx_ * 66, hy + 62), (sx_ * 60, hy - 20)]), hc, ow=owx * 0.7, seed=sd + 102 + sx_, t=tt, wob_amp=0.8, smooth=True)
    hat = L.get("hat")
    hcol = L.get("hat_col", INK)
    if hat in ("beret", "cap_flat", "crown", "morion", "veil", "veil_crown", "french_hood", "turban_tall", "turban_red", "tiara", "feather_crown", "llautu"):
        _hat2(ctx, H_, hat, hcol, hy, owx, sd, tt, s, L)
    if hat == "bowler":
        shape(ctx, H_(smooth_closed([(-70, hy - 70), (-60, hy - 130), (-26, hy - 158), (30, hy - 158), (62, hy - 130), (72, hy - 70)], 6)), hcol, ow=owx, seed=sd + 110, t=tt,
              wob_amp=1.2, shade=(shade(hcol, -0.3), 10 * s, 0.5), hatch=(shade(hcol, 0.12), 22 * s, 0.25))
        shape(ctx, H_(ellipse_pts(0, hy - 70, 104, 17, 22)), shade(hcol, -0.05), ow=owx, seed=sd + 111, t=tt, wob_amp=1.0, shade=(shade(hcol, -0.3), 6 * s, 0.5))
        shape(ctx, H_([(-68, hy - 82), (68, hy - 82), (66, hy - 96), (-66, hy - 96)]), INK_L, ow=owx * 0.3, seed=sd + 112, t=tt, wob_amp=0.6)
    elif hat == "straw":
        shape(ctx, H_(smooth_closed([(-56, hy - 74), (-48, hy - 128), (0, hy - 138), (48, hy - 128), (56, hy - 74)], 6)), hcol, ow=owx, seed=sd + 113, t=tt, wob_amp=1.2,
              hatch=(shade(hcol, -0.2), 16 * s, 0.35))
        shape(ctx, H_(ellipse_pts(0, hy - 72, 128, 22, 24)), shade(hcol, 0.04), ow=owx, seed=sd + 114, t=tt, wob_amp=1.0, hatch=(shade(hcol, -0.2), 16 * s, 0.30))
        shape(ctx, H_([(-54, hy - 84), (54, hy - 84), (53, hy - 98), (-53, hy - 98)]), BRICK, ow=owx * 0.3, seed=sd + 115, t=tt, wob_amp=0.6)
    elif hat == "cap":
        shape(ctx, H_(smooth_closed([(-74, hy - 62), (-60, hy - 116), (0, hy - 130), (62, hy - 116), (76, hy - 62)], 6)), hcol, ow=owx, seed=sd + 116, t=tt, wob_amp=1.1,
              shade=(shade(hcol, -0.3), 8 * s, 0.5), hatch=(shade(hcol, -0.2), 18 * s, 0.30))
        shape(ctx, H_([(-10, hy - 66), (96, hy - 60), (86, hy - 48), (-10, hy - 54)]), shade(hcol, -0.12), ow=owx * 0.7, seed=sd + 117, t=tt, wob_amp=0.8)
    elif hat == "nurse":
        shape(ctx, H_(smooth_closed([(-62, hy - 70), (-52, hy - 118), (0, hy - 130), (52, hy - 118), (62, hy - 70), (0, hy - 82)], 6)), hcol, ow=owx, seed=sd + 118, t=tt, wob_amp=1.0,
              shade=(shade(hcol, -0.12), 8 * s, 0.5))
        if L.get("collar") or L.get("apron"):
            shape(ctx, H_([(-6, hy - 118), (6, hy - 118), (6, hy - 100), (-6, hy - 100)]), BRICK, ow=owx * 0.2, seed=sd + 119, t=tt, wob_amp=0.3)

    # ter damlaları
    if P["sweat"] > 0:
        for i in range(3):
            u = (tt * 1.8 + i * 0.33) % 1.0
            sx_ = (-1 if i % 2 else 1) * (72 + 6 * i)
            sy_ = hy - 40 + u * 70
            dp = H_([(sx_, sy_ - 14), (sx_ + 8, sy_ + 2), (sx_, sy_ + 10), (sx_ - 8, sy_ + 2)])
            ctx.poly(smooth_closed(dp, 4), (150, 205, 235), 0.9 * P["sweat"] * (1 - u * 0.6))
    hx_, hy_ = W_(0, hy)
    return dict(handL=hands.get("arm_l"), handR=hands.get("arm_r"), head=(hx_, hy_), tor=P)
