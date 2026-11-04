#!/usr/bin/env python3
"""Kapak denetimi (küçük resim QA). Kanalın kapak test seti (CLAUDE.md) + kurul tur 1 ölçütleri (PK1 §3a/§6, TE2 Ö10) tek sayfada.

  python3 kapak_qa.py --part 1                          # yayin/studio_paketi_P1/kapak_P1_K*.jpg → out_p1/kapak/kapak_qa_P1.png + .json
  python3 kapak_qa.py a.jpg b.jpg --cikti /yol/qa       # başka kapaklar (yerleşim JSON'u yoksa yalnız piksel testleri)

Her kapak için:
  1) küçültme 246 / 168 / 120 px genişlik: kahraman ve ikincil yazının büyük harf yüksekliği (yazı tipi ölçüsü + pikselden ölçülen),
     gövde kalınlığı ve o boyda yazı/zemin kontrastı → "okunur" kararı (büyük harf ≥ 9 px, gövde ≥ 1,5 px, kontrast ≥ 4,5:1);
  2) gri ton testi: yazı–zemin gri farkı (≥ 70 düzey), odak–çevre gri farkı, "tek parlak odak" (en parlak %1'in odakta kalan payı, parlak leke sayısı);
  3) akış maketi: kanalın diğer kapaklarıyla (sisifos, orfeus, sarlken_kapak, cumhuriyet_kapak) YouTube ana sayfa ızgarası, koyu + açık tema,
     süre rozeti ve başlık satırı taklidiyle;
  4) bölge denetimi: yazı / odak / öğe kutuları ∩ süre rozeti bölgesi (x 960–1250, y 553–689) ve fare simgesi bölgesi (x ≥ 1170, y ≤ 110; yalnız yazı)
     → kesişim varsa çıkış kodu 1; ek olarak süre rozeti bölgesinde piksel düzeyinde kenar/parlaklık uyarısı;
  5) kontrast: kahraman (ve ikincil) yazı ile çevresi arasında WCAG oranı (hedef kahraman ≥ 7:1, ikincil ≥ 4,5:1).
Yerleşim bilgisi kapak_medici.py'nin yazdığı `out_pN/kapak/<ad>.yerlesim.json` dosyasından okunur (yazı maskeleri, kutular).
Çıkış kodu: 0 = bölge ihlali yok; 1 = ihlal var; 2 = dosya/ölçü hatası (1280×720 değil, 2 MB üstü vb.)."""
import argparse
import base64
import io
import json
import math
import os
import sys
import time

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
KANAL = "/home/user/sisifos-wt"
SURE_ROZETI = (960, 553, 1250, 689)
FARE_SIMGE = (1170, 0, 1280, 110)
GENISLIKLER = (246, 168, 120)
ESIK = dict(kap_px=9.0, govde_px=1.5, kontrast_kucuk=4.5, gri_fark=70, kahraman_kontrast=7.0, ikincil_kontrast=4.5, kahraman_oran=0.18, ikincil_oran=0.10,
            odak_payi=0.60, boyut_mb=2.0)
# akış maketi: kanalın kapakları (dosya, başlık, süre). Süre/görüntüleme temsilîdir.
REFERANS = [
    ("sisifos/kapak.png", "Sisifos'u Neden Mutlu Hayal Etmeliyiz? | Camus ve Absürt", "7:05"),
    ("orfeus/kapak_final_A_arkana_bakma.jpg", "Orfeus ve Evridiki: Ölüleri İkna Etti, Kendini Durduramadı", "8:41"),
    ("sarlken_kapak/kapak_yeni_1_madalyalar.jpg", "Osmanlı'nın 'İspanya Kralı' Dediği İmparator: Şarlken Neden Vazgeçti?", "21:27"),
    ("cumhuriyet_kapak/kapak_yeni_A_sultanin_ogrencisi.jpg", "Abdülhamid, Kendi Sonunu Getiren Kuşağı Nasıl Yetiştirdi?", "6:20"),
    ("sisifos/kapak_b.png", "Sisifos'u Neden Mutlu Hayal Etmeliyiz? | Camus ve Absürt", "7:05"),
    ("orfeus/kapak_final_B_neden_bakti.jpg", "Orfeus ve Evridiki: Ölüleri İkna Etti, Kendini Durduramadı", "8:41"),
]
UI_FONT = "/usr/share/fonts/opentype/inter/Inter-{}.otf"
_FC = {}


def ui_font(size, w="Regular"):
    key = (size, w)
    if key not in _FC:
        for p in (UI_FONT.format(w), "/usr/share/fonts/truetype/dejavu/DejaVuSans{}.ttf".format("-Bold" if w in ("Bold", "SemiBold") else "")):
            if os.path.exists(p):
                _FC[key] = ImageFont.truetype(p, size)
                break
        else:
            _FC[key] = ImageFont.load_default()
    return _FC[key]


# ───────────────────────────── ölçü yardımcıları ─────────────────────────────
def srgb_lin(c):
    c = np.asarray(c, np.float64) / 255.0
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def rel_lum(rgb):
    lin = srgb_lin(rgb)
    return 0.2126 * lin[..., 0] + 0.7152 * lin[..., 1] + 0.0722 * lin[..., 2]


def wcag(l1, l2):
    hi, lo = max(l1, l2), min(l1, l2)
    return (hi + 0.05) / (lo + 0.05)


def icc_name(icc):
    if not icc:
        return "yok (sRGB varsayılır)"
    try:
        from PIL import ImageCms
        return ImageCms.getProfileDescription(ImageCms.ImageCmsProfile(io.BytesIO(icc))).strip() or "var"
    except Exception:
        return "var"


def gray(rgb):
    return cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY).astype(np.float32)


def inter(a, b):
    """İki kutunun kesişim alanı (px²)."""
    w = min(a[2], b[2]) - max(a[0], b[0])
    h = min(a[3], b[3]) - max(a[1], b[1])
    return max(0.0, w) * max(0.0, h)


def decode_mask(b64):
    m = Image.open(io.BytesIO(base64.b64decode(b64))).convert("L")
    return np.asarray(m, np.float32) / 255.0


def load_layout(img_path, part=None):
    stem = os.path.splitext(os.path.basename(img_path))[0]
    cands = [os.path.join(os.path.dirname(img_path), stem + ".yerlesim.json")]
    if part:
        cands.insert(0, os.path.join(HERE, f"out_p{part}", "kapak", stem + ".yerlesim.json"))
    for c in cands:
        if os.path.exists(c):
            with open(c, encoding="utf-8") as fh:
                return json.load(fh), c
    return None, None


def measured_cap(mask):
    """Pikselden büyük harf yüksekliği: harf bileşenlerinin (İ noktaları ve küçük parçalar hariç) yükseklikleri → (en büyük p90, en küçük p10)."""
    m = (mask > 0.5).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(m, 8)
    if n <= 1:
        return 0.0, 0.0
    areas = st[1:, cv2.CC_STAT_AREA]
    hs = st[1:, cv2.CC_STAT_HEIGHT][areas > 0.08 * areas.max()]
    if len(hs) == 0:
        return 0.0, 0.0
    return float(np.percentile(hs, 90)), float(np.percentile(hs, 10))


def stem_width(mask):
    """Gövde kalınlığı (px): uzaklık dönüşümünün harf içi tepe değerlerinin medyanı × 2."""
    m = (mask > 0.5).astype(np.uint8)
    if m.sum() == 0:
        return 0.0
    d = cv2.distanceTransform(m, cv2.DIST_L2, 5)
    peaks = d[(d >= cv2.dilate(d, np.ones((3, 3), np.uint8))) & (d > 1.0)]
    return float(np.median(peaks) * 2.0) if peaks.size else 0.0


def text_contrast(img, mask, ring_in=6, ring_out=26):
    """Yazı pikselleri (aşınmış maske) ile çevre halkası (yazıdan ring_in…ring_out px uzak) arasında: WCAG oranı, gri farkı."""
    m = (mask > 0.5).astype(np.uint8)
    if m.sum() < 4:
        return 0.0, 0.0, None, None
    inner = cv2.erode(m, np.ones((3, 3), np.uint8)) if m.sum() > 400 else m
    k_in = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * ring_in + 1, 2 * ring_in + 1))
    k_out = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * ring_out + 1, 2 * ring_out + 1))
    ring = (cv2.dilate(m, k_out) > 0) & ~(cv2.dilate(m, k_in) > 0)
    if ring.sum() < 4:
        return 0.0, 0.0, None, None
    t_rgb = np.median(img[inner > 0], axis=0)
    b_rgb = np.median(img[ring], axis=0)
    g = gray(img)
    return wcag(float(rel_lum(t_rgb)), float(rel_lum(b_rgb))), float(np.median(g[inner > 0]) - np.median(g[ring])), t_rgb.tolist(), b_rgb.tolist()


def resize(img, w):
    h = round(w * 9 / 16)
    return cv2.resize(img, (w, h), interpolation=cv2.INTER_AREA)


# ───────────────────────────── testler ─────────────────────────────
def analyse(path, part=None):
    r = dict(dosya=os.path.relpath(path, HERE) if path.startswith(HERE) else path, hatalar=[], uyarilar=[])
    pil = Image.open(path)
    r["boyut"] = list(pil.size)
    r["mb"] = round(os.path.getsize(path) / 1e6, 3)
    r["mod"] = pil.mode
    r["icc"] = icc_name(pil.info.get("icc_profile"))
    if tuple(pil.size) != (1280, 720):
        r["hatalar"].append(f"boyut {pil.size} ≠ 1280×720")
    if r["mb"] >= ESIK["boyut_mb"]:
        r["hatalar"].append(f"dosya {r['mb']} MB ≥ 2 MB")
    img = np.asarray(pil.convert("RGB").resize((1280, 720), Image.LANCZOS))
    lay, lay_path = load_layout(path, part)
    r["yerlesim"] = os.path.relpath(lay_path, HERE) if lay_path else None
    g = gray(img)
    # ── 1 + 5: yazılar (boy, okunurluk, kontrast)
    yazilar = []
    masks = []
    if lay:
        for o in lay["ogeler"]:
            if o["tur"] != "yazi":
                continue
            m = decode_mask(o["maske_png"])
            masks.append(m)
            cap_metric = float(o["kap_px"])
            cap_meas, cap_meas_min = measured_cap(m)
            stem = stem_width(m)
            ratio, gfark, trgb, brgb = text_contrast(img, m)
            e = dict(ad=o["ad"], metin=o["metin"], kutu=o["kutu"], kap_px=cap_metric, kap_px_min=o.get("kap_px_min", cap_metric),
                     kap_oran=round(cap_metric / 720, 4), olculen_kap_px=round(cap_meas, 1), olculen_kap_px_min=round(cap_meas_min, 1), govde_px=round(stem, 1),
                     kontrast=round(ratio, 2), gri_fark=round(gfark, 1), yazi_rgb=trgb, zemin_rgb=brgb, boylar={})
            for w in GENISLIKLER:
                s = w / 1280.0
                sm_img = resize(img, w)
                sm_m = cv2.resize(m, sm_img.shape[1::-1], interpolation=cv2.INTER_AREA)
                rr, gf, _, _ = text_contrast(sm_img, sm_m, ring_in=1, ring_out=3)
                kp, kmin, st_ = cap_metric * s, e["kap_px_min"] * s, stem * s
                ok = (kmin >= ESIK["kap_px"] or w < 168) and kp >= ESIK["kap_px"] * (0.75 if w < 168 else 1.0) and st_ >= ESIK["govde_px"] * (0.8 if w < 168 else 1.0) \
                    and rr >= ESIK["kontrast_kucuk"]
                e["boylar"][str(w)] = dict(kap_px=round(kp, 1), kap_px_min=round(kmin, 1), govde_px=round(st_, 2), kontrast=round(rr, 2), gri_fark=round(gf, 1), okunur=bool(ok))
            hedef_oran = ESIK["kahraman_oran"] if o["ad"] == "kahraman" else ESIK["ikincil_oran"]
            hedef_k = ESIK["kahraman_kontrast"] if o["ad"] == "kahraman" else ESIK["ikincil_kontrast"]
            e["oran_tamam"] = cap_metric / 720 >= hedef_oran - 1e-4
            e["kontrast_tamam"] = ratio >= hedef_k
            e["gri_tamam"] = gfark >= ESIK["gri_fark"]
            if not e["oran_tamam"]:
                r["hatalar"].append(f"{o['ad']} büyük harf %{cap_metric / 7.2:.1f} < %{hedef_oran * 100:.0f}")
            if not e["kontrast_tamam"]:
                r["uyarilar"].append(f"{o['ad']} kontrast {ratio:.1f}:1 < {hedef_k}:1")
            if not e["gri_tamam"]:
                r["uyarilar"].append(f"{o['ad']} gri farkı {gfark:.0f} < {ESIK['gri_fark']}")
            yazilar.append(e)
    r["yazilar"] = yazilar
    tmask = np.zeros(g.shape, np.float32)
    for m in masks:
        tmask = np.maximum(tmask, m)
    tmask_d = cv2.dilate((tmask > 0.2).astype(np.uint8), np.ones((15, 15), np.uint8)) > 0
    # ── 2: gri / tek odak
    odak = None
    if lay:
        od = [o for o in lay["ogeler"] if o["tur"] == "odak"]
        if od:
            odak = od[0]["kutu"]
    excl = tmask_d.copy()
    if lay:
        for o in lay["ogeler"]:
            if o["tur"] == "rozet":
                x0, y0, x1, y1 = [int(round(v)) for v in o["kutu"]]
                excl[max(0, y0 - 4):y1 + 4, max(0, x0 - 4):x1 + 4] = True
    vals = g[~excl]
    thr = float(np.percentile(vals, 99.0))
    bright = (g >= thr) & ~excl
    gri = dict(esik_p99=round(thr, 1))
    n, lab, st, _ = cv2.connectedComponentsWithStats(cv2.dilate(bright.astype(np.uint8), np.ones((9, 9), np.uint8)), 8)
    big = [i for i in range(1, n) if st[i, cv2.CC_STAT_AREA] >= 0.0008 * g.size]
    gri["parlak_leke"] = len(big)
    if odak:
        x0, y0, x1, y1 = odak
        pad_x, pad_y = (x1 - x0) * 0.10, (y1 - y0) * 0.10
        box = np.zeros(g.shape, bool)
        box[int(max(0, y0 - pad_y)):int(min(720, y1 + pad_y)), int(max(0, x0 - pad_x)):int(min(1280, x1 + pad_x))] = True
        gri["odak_payi"] = round(float((bright & box).sum() / max(1, bright.sum())), 3)
        inside = np.zeros(g.shape, bool)
        inside[int(max(0, y0)):int(min(720, y1)), int(max(0, x0)):int(min(1280, x1))] = True
        ring = np.zeros(g.shape, bool)
        ex, ey = (x1 - x0) * 0.45, (y1 - y0) * 0.45
        ring[int(max(0, y0 - ey)):int(min(720, y1 + ey)), int(max(0, x0 - ex)):int(min(1280, x1 + ex))] = True
        ring &= ~inside & ~excl
        gri["odak_p90"] = round(float(np.percentile(g[inside & ~excl], 90)), 1)
        gri["cevre_medyan"] = round(float(np.median(g[ring])), 1) if ring.any() else None
        gri["odak_cevre_fark"] = round(gri["odak_p90"] - (gri["cevre_medyan"] or 0), 1)
        # 168 px'te bulanık en parlak nokta odakta mı (küçük boy belirginlik vekili)
        sm = cv2.GaussianBlur(resize(img, 168), (0, 0), 2.0)
        sg = gray(sm)
        sx = cv2.resize((~excl).astype(np.uint8), (168, 94), interpolation=cv2.INTER_NEAREST) > 0
        sg[~sx] = 0
        yy, xx = np.unravel_index(int(np.argmax(sg)), sg.shape)
        X, Y = xx * 1280 / 168, yy * 720 / 94
        gri["en_parlak_168"] = [round(X), round(Y)]
        gri["en_parlak_168_odakta"] = bool(x0 - pad_x * 3 <= X <= x1 + pad_x * 3 and y0 - pad_y * 3 <= Y <= y1 + pad_y * 3)
        gri["tek_odak"] = bool(gri["odak_payi"] >= ESIK["odak_payi"] and gri["en_parlak_168_odakta"])
        if not gri["tek_odak"]:
            r["uyarilar"].append(f"tek parlak odak zayıf: en parlak %1'in %{gri['odak_payi'] * 100:.0f}'i odakta; 168 px en parlak nokta odakta={gri['en_parlak_168_odakta']}")
    gri["ortalama"] = round(float(g.mean()), 1)
    gri["p95"] = round(float(np.percentile(g, 95)), 1)
    r["gri"] = gri
    # ── 4: bölge denetimi
    ihlal = []
    if lay:
        for o in lay["ogeler"]:
            b = o["kutu"]
            if o["tur"] in ("yazi", "odak", "oge", "rozet"):
                a = inter(b, SURE_ROZETI)
                if a > 0:
                    ihlal.append(dict(bolge="sure_rozeti", oge=o["ad"], alan_px=round(a)))
            if o["tur"] == "yazi":
                a = inter(b, FARE_SIMGE)
                if a > 0:
                    ihlal.append(dict(bolge="fare_simgeleri", oge=o["ad"], alan_px=round(a)))
                # maske düzeyinde de (kutu kesişse bile mürekkep girmiyor olabilir → bilgi)
    x0, y0, x1, y1 = SURE_ROZETI
    zone = g[y0:y1, x0:x1]
    edges = cv2.Canny(cv2.GaussianBlur(g.astype(np.uint8), (3, 3), 0), 60, 150)
    ed_zone = float((edges[y0:y1, x0:x1] > 0).mean())
    ed_all = float((edges > 0).mean())
    piksel = dict(sure_rozeti_kenar=round(ed_zone, 4), kare_kenar=round(ed_all, 4), sure_rozeti_parlak=round(float((zone > 170).mean()), 4),
                  sure_rozeti_ortalama=round(float(zone.mean()), 1))
    if ed_zone > 0.03 or piksel["sure_rozeti_parlak"] > 0.01:
        r["uyarilar"].append(f"süre rozeti bölgesi piksel düzeyinde dolu görünüyor (kenar %{ed_zone * 100:.1f}, parlak %{piksel['sure_rozeti_parlak'] * 100:.1f})")
    r["bolge"] = dict(ihlal=ihlal, ihlal_sayisi=len(ihlal), piksel=piksel, denetlendi=bool(lay))
    if not lay:
        r["uyarilar"].append("yerleşim JSON'u yok: yazı/odak ölçüleri ve kutu kesişimi yapılmadı (yalnız piksel testleri)")
    r["_img"] = img
    r["_mask"] = tmask
    r["_lay"] = lay
    return r


# ───────────────────────────── çizim: kontrol sayfası ─────────────────────────────
def _txt(d, xy, s, size=15, w="Regular", fill=(230, 230, 230), anchor="la"):
    d.text(xy, s, font=ui_font(size, w), fill=fill, anchor=anchor)


def overlay(img, lay):
    pil = Image.fromarray(img).convert("RGBA")
    ov = Image.new("RGBA", pil.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    d.rectangle(SURE_ROZETI, fill=(255, 40, 40, 70), outline=(255, 60, 60, 255), width=3)
    d.rectangle(FARE_SIMGE, fill=(255, 150, 0, 70), outline=(255, 160, 0, 255), width=3)
    if lay:
        for o in lay["ogeler"]:
            col = dict(yazi=(0, 230, 255, 255), odak=(60, 255, 90, 255), oge=(255, 230, 0, 200), rozet=(200, 120, 255, 255))[o["tur"]]
            b = [max(-2, min(1282, v)) for v in o["kutu"]]
            d.rectangle(b, outline=col, width=3 if o["tur"] in ("yazi", "odak") else 2)
    return np.asarray(Image.alpha_composite(pil, ov).convert("RGB"))


def _rounded(img, r):
    h, w = img.shape[:2]
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), r, fill=255)
    return Image.fromarray(img), m


def feed(cards, dark=True, cols=4, tw=300):
    """YouTube ana sayfa ızgarası taklidi: kapak (yuvarlak köşe) + süre rozeti + kanal simgesi + iki satır başlık + kanal/görüntüleme."""
    bg, fg, sub = ((15, 15, 15), (241, 241, 241), (170, 170, 170)) if dark else ((255, 255, 255), (15, 15, 15), (96, 96, 96))
    th = round(tw * 9 / 16)
    pad, gap_y = 16, 104
    rows = (len(cards) + cols - 1) // cols
    W_ = pad + cols * (tw + pad)
    H_ = 44 + rows * (th + gap_y) + pad
    can = Image.new("RGB", (W_, H_), bg)
    d = ImageDraw.Draw(can)
    _txt(d, (pad, 12), "Akış maketi · " + ("koyu" if dark else "açık") + " tema (süre/görüntüleme temsilîdir)", 15, "SemiBold", sub)
    for i, (img, title, dur, mark) in enumerate(cards):
        rr, cc = divmod(i, cols)
        x, y = pad + cc * (tw + pad), 44 + rr * (th + gap_y)
        t = cv2.resize(img, (tw, th), interpolation=cv2.INTER_AREA)
        tim, m = _rounded(t, 10)
        can.paste(tim, (x, y), m)
        f = ui_font(12, "SemiBold")
        bw = d.textlength(dur, font=f) + 10
        d.rounded_rectangle((x + tw - 6 - bw, y + th - 6 - 18, x + tw - 6, y + th - 6), 4, fill=(0, 0, 0))
        d.text((x + tw - 6 - bw / 2, y + th - 6 - 9), dur, font=f, fill=(255, 255, 255), anchor="mm")
        d.ellipse((x, y + th + 10, x + 34, y + th + 44), fill=(120, 30, 30) if mark else (90, 60, 30))
        d.text((x + 17, y + th + 27), "ZK", font=ui_font(11, "Bold"), fill=(250, 235, 200), anchor="mm")
        words, lines, cur = title.split(), [], ""
        ft = ui_font(14, "SemiBold")
        for wd in words:
            tt = (cur + " " + wd).strip()
            if d.textlength(tt, font=ft) <= tw - 46 or not cur:
                cur = tt
            else:
                lines.append(cur)
                cur = wd
        lines.append(cur)
        if len(lines) > 2:
            lines = [lines[0], lines[1].rstrip() + "…"]
        for k_, ln in enumerate(lines):
            d.text((x + 44, y + th + 10 + k_ * 19), ln, font=ft, fill=fg)
        d.text((x + 44, y + th + 12 + len(lines) * 19), "Zaman Kuryesi", font=ui_font(12), fill=sub)
        d.text((x + 44, y + th + 28 + len(lines) * 19), "1,2 B görüntüleme · 2 gün önce", font=ui_font(12), fill=sub)
        if mark:
            d.rounded_rectangle((x - 3, y - 3, x + tw + 3, y + th + 3), 12, outline=(255, 200, 60), width=2)
    return np.asarray(can)


def sheet(results, out_png, part):
    rows = []
    for r in results:
        img, lay = r["_img"], r["_lay"]
        Wr, Hr = 2240, 560
        can = Image.new("RGB", (Wr, Hr), (26, 26, 28))
        d = ImageDraw.Draw(can)
        ov = cv2.resize(overlay(img, lay), (640, 360), interpolation=cv2.INTER_AREA)
        can.paste(Image.fromarray(ov), (16, 44))
        ad = os.path.basename(r["dosya"])
        _txt(d, (16, 12), f"{ad}  ·  {r['boyut'][0]}×{r['boyut'][1]}  ·  {r['mb']} MB  ·  ICC {r['icc']}", 17, "SemiBold", (255, 214, 120))
        _txt(d, (16, 410), "kırmızı: süre rozeti bölgesi · turuncu: fare simgeleri · camgöbeği: yazı · yeşil: odak · sarı: öğe · mor: parça rozeti", 12, "Regular", (170, 170, 170))
        x = 672
        for w in GENISLIKLER:
            t = resize(img, w)
            can.paste(Image.fromarray(t), (x, 44))
            _txt(d, (x, 44 + t.shape[0] + 4), f"{w} px", 12, "Regular", (190, 190, 190))
            x += w + 14
        g246 = cv2.cvtColor(cv2.cvtColor(resize(img, 246), cv2.COLOR_RGB2GRAY), cv2.COLOR_GRAY2RGB)
        can.paste(Image.fromarray(g246), (x, 44))
        _txt(d, (x, 44 + g246.shape[0] + 4), "gri 246", 12, "Regular", (190, 190, 190))
        x2 = 672
        for w in (168, 120):
            t = resize(img, w)
            u = cv2.resize(t, (w * 2, t.shape[0] * 2), interpolation=cv2.INTER_NEAREST)
            can.paste(Image.fromarray(u), (x2, 214))
            _txt(d, (x2, 214 + u.shape[0] + 4), f"{w} px (2× piksel)", 12, "Regular", (190, 190, 190))
            x2 += u.shape[1] + 14
        g168 = cv2.cvtColor(cv2.cvtColor(resize(img, 168), cv2.COLOR_RGB2GRAY), cv2.COLOR_GRAY2RGB)
        can.paste(Image.fromarray(g168), (x2, 214))
        bl = cv2.GaussianBlur(resize(img, 168), (0, 0), 3.0)
        can.paste(Image.fromarray(bl), (x2, 330))
        _txt(d, (x2, 330 + 98), "gri 168 · bulanık 168", 12, "Regular", (190, 190, 190))
        # ölçüm metni
        tx, ty = 1520, 44
        lines = []
        for e in r["yazilar"]:
            b = e["boylar"]
            lines.append((f"{'KAHRAMAN' if e['ad'] == 'kahraman' else 'İKİNCİL'} \"{e['metin']}\"", "SemiBold", (255, 255, 255)))
            mn = f" (\"SON\" {e['kap_px_min']:.0f})" if e["kap_px_min"] != e["kap_px"] else ""
            lines.append((f"büyük harf {e['kap_px']:.0f} px = %{e['kap_oran'] * 100:.1f}{mn} · ölçülen {e['olculen_kap_px']:.0f} · gövde {e['govde_px']:.0f} px",
                          "Regular", (120, 230, 120) if e["oran_tamam"] else (255, 110, 110)))
            lines.append(("  " + " · ".join(f"{w}: {b[str(w)]['kap_px']:.1f} px {'✓' if b[str(w)]['okunur'] else '✗'}" for w in GENISLIKLER), "Regular", (220, 220, 220)))
            lines.append((f"  kontrast {e['kontrast']:.1f}:1 · gri farkı {e['gri_fark']:.0f} · 168'de {b['168']['kontrast']:.1f}:1",
                          "Regular", (120, 230, 120) if (e["kontrast_tamam"] and e["gri_tamam"]) else (255, 190, 90)))
        gr = r["gri"]
        if "odak_payi" in gr:
            lines.append(("ODAK / GRİ", "SemiBold", (255, 255, 255)))
            lines.append((f"en parlak %1'in %{gr['odak_payi'] * 100:.0f}'i odakta · parlak leke {gr['parlak_leke']}", "Regular",
                          (120, 230, 120) if gr["tek_odak"] else (255, 190, 90)))
            lines.append((f"odak p90 {gr['odak_p90']:.0f} − çevre {gr['cevre_medyan']:.0f} = {gr['odak_cevre_fark']:.0f} · 168'de en parlak: {'odakta' if gr['en_parlak_168_odakta'] else 'ODAK DIŞI'}",
                          "Regular", (220, 220, 220)))
        bz = r["bolge"]
        lines.append(("BÖLGE", "SemiBold", (255, 255, 255)))
        lines.append((f"ihlal {bz['ihlal_sayisi']}" + ("" if not bz["ihlal"] else ": " + ", ".join(f"{i['oge']}∩{i['bolge']}" for i in bz["ihlal"])),
                      "Regular", (120, 230, 120) if bz["ihlal_sayisi"] == 0 else (255, 110, 110)))
        lines.append((f"süre rozeti pikseli: kenar %{bz['piksel']['sure_rozeti_kenar'] * 100:.1f} · parlak %{bz['piksel']['sure_rozeti_parlak'] * 100:.1f} · ort. gri {bz['piksel']['sure_rozeti_ortalama']:.0f}",
                      "Regular", (220, 220, 220)))
        for h in r["hatalar"]:
            lines.append(("HATA: " + h, "SemiBold", (255, 110, 110)))
        for u in r["uyarilar"]:
            lines.append(("uyarı: " + u, "Regular", (255, 190, 90)))
        for s, w, col in lines:
            _txt(d, (tx, ty), s, 14 if w == "Regular" else 15, w, col)
            ty += 21 if w == "Regular" else 24
        rows.append(np.asarray(can))
    # akış maketi
    cards = []
    for r in results:
        cards.append((r["_img"], "Medici Ailesi (1/7): Faiz Yasakken Nasıl Zengin Oldular?", "10:02", True))
    for rel, title, dur in REFERANS:
        p = os.path.join(KANAL, rel)
        if os.path.exists(p):
            im = np.asarray(Image.open(p).convert("RGB").resize((1280, 720), Image.LANCZOS))
            cards.append((im, title, dur, False))
    order = []
    refs = [c for c in cards if not c[3]]
    ours = [c for c in cards if c[3]]
    while refs or ours:                          # bizimkiler ızgaraya serpiştirilir (1., 6. …)
        if ours:
            order.append(ours.pop(0))
        for _ in range(4 if ours else len(refs)):
            if refs:
                order.append(refs.pop(0))
    fd = feed(order, True)
    fl = feed(order, False)
    W_ = max(max(r_.shape[1] for r_ in rows), fd.shape[1] + fl.shape[1] + 16)
    parts = []
    head = Image.new("RGB", (W_, 48), (18, 18, 20))
    _txt(ImageDraw.Draw(head), (16, 12), f"Kapak QA · Parça {part} · {time.strftime('%Y-%m-%d %H:%M')} · kapak_qa.py (246/168/120 · gri · akış · bölge · kontrast)", 20, "SemiBold", (255, 214, 120))
    parts.append(np.asarray(head))
    for r_ in rows:
        parts.append(np.pad(r_, ((0, 0), (0, W_ - r_.shape[1]), (0, 0)), constant_values=26))
    hh = max(fd.shape[0], fl.shape[0])
    fd = np.pad(fd, ((0, hh - fd.shape[0]), (0, 0), (0, 0)), constant_values=15)
    fl = np.pad(fl, ((0, hh - fl.shape[0]), (0, 0), (0, 0)), constant_values=255)
    strip = np.concatenate([fd, np.full((hh, 16, 3), 26, np.uint8), fl], 1)
    parts.append(np.pad(strip, ((0, 0), (0, W_ - strip.shape[1]), (0, 0)), constant_values=26))
    out = np.concatenate(parts, 0)
    Image.fromarray(out).save(out_png, optimize=True)
    return out_png


def main(argv=None):
    ap = argparse.ArgumentParser(description="Kapak QA (küçük resim denetimi)")
    ap.add_argument("kapaklar", nargs="*", help="kapak dosyaları (varsayılan: yayin/studio_paketi_P<part>/kapak_P<part>_K*.jpg)")
    ap.add_argument("--part", type=int, default=1)
    ap.add_argument("--cikti", default=None, help="çıktı kökü (uzantısız); varsayılan out_p<part>/kapak/kapak_qa_P<part>")
    a = ap.parse_args(argv)
    paths = a.kapaklar
    if not paths:
        import glob
        paths = sorted(glob.glob(os.path.join(HERE, "yayin", f"studio_paketi_P{a.part}", f"kapak_P{a.part}_K*.jpg")))
    if not paths:
        print("kapak bulunamadı", file=sys.stderr)
        return 2
    base = a.cikti or os.path.join(HERE, f"out_p{a.part}", "kapak", f"kapak_qa_P{a.part}")
    os.makedirs(os.path.dirname(base), exist_ok=True)
    results = [analyse(os.path.abspath(p), a.part) for p in paths]
    png = sheet(results, base + ".png", a.part)
    js = dict(tarih=time.strftime("%Y-%m-%d %H:%M"), parca=a.part, esikler=ESIK, sure_rozeti=SURE_ROZETI, fare_simgeleri=FARE_SIMGE,
              kapaklar=[{k: v for k, v in r.items() if not k.startswith("_")} for r in results])
    with open(base + ".json", "w", encoding="utf-8") as fh:
        json.dump(js, fh, ensure_ascii=False, indent=1)
    ihlal = sum(r["bolge"]["ihlal_sayisi"] for r in results)
    hata = sum(len(r["hatalar"]) for r in results)
    for r in results:
        y = {e["ad"]: e for e in r["yazilar"]}
        k_ = y.get("kahraman")
        s = f"{os.path.basename(r['dosya'])}: "
        if k_:
            s += f"kahraman {k_['kap_px']:.0f}px (%{k_['kap_oran'] * 100:.1f}) 168={k_['boylar']['168']['kap_px']:.1f}px 120={k_['boylar']['120']['kap_px']:.1f}px kontrast {k_['kontrast']:.1f}:1 gri {k_['gri_fark']:.0f}; "
        if "odak_payi" in r["gri"]:
            s += f"odak payı %{r['gri']['odak_payi'] * 100:.0f}; "
        s += f"bölge ihlali {r['bolge']['ihlal_sayisi']}; hata {len(r['hatalar'])}; uyarı {len(r['uyarilar'])}"
        print(s)
        for u in r["uyarilar"]:
            print("   uyarı:", u)
        for h in r["hatalar"]:
            print("   HATA:", h)
    print(png)
    print(base + ".json")
    if hata:
        return 2
    return 1 if ihlal else 0


if __name__ == "__main__":
    sys.exit(main())
