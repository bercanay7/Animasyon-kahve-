"""Hızlı önizleme yardımcıları: tek çekimi (kind+params) belirli yerel saniyelerde çiz → PNG / kontak sayfası."""
import sys, time
import cv2, numpy as np
import shots as SH, sk
import compose  # outro kind kaydı

def render_shot(kind, params, ts, dur=8.0, post=True, tl=None):
    sh = SH.shot(kind, 0.0, **params); sh.t0 = 0.0; sh.t1 = dur; sh.i = 1
    tl = tl or SH.timeline()
    out = []
    for t in ts:
        f = sk.Frame()
        cx = SH.Ctx(f, t, sh, tl)
        SH.KINDS[kind](cx, **params)
        img = f.rgb()
        if post: img = sk.post(img, int(t*24))
        out.append(img)
    return out

def sheet(imgs, cols=3, scale=0.5, path="out/frames/sheet.png"):
    h, w = imgs[0].shape[:2]
    sw, sh_ = int(w*scale), int(h*scale)
    rows = (len(imgs)+cols-1)//cols
    S = np.zeros((rows*sh_, cols*sw, 3), np.uint8)
    for i, im in enumerate(imgs):
        r, c = divmod(i, cols)
        S[r*sh_:(r+1)*sh_, c*sw:(c+1)*sw] = cv2.resize(im, (sw, sh_), interpolation=cv2.INTER_AREA)
    cv2.imwrite(path, cv2.cvtColor(S, cv2.COLOR_RGB2BGR))
    return path
