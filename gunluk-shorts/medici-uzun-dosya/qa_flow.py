#!/usr/bin/env python3
"""qa_flow — MEDICI yönetmenlik kapıları (YONETMENLIK_REHBERI §10): akış denetimi.

  python3 qa_flow.py --reel                     # reel (preview_reel.py) üzerinde: statik + örnekleme analizi
  python3 qa_flow.py --reel --fast              # yalnız statik analiz (hızlı; kare çizmez)
  python3 qa_flow.py --part 2 [--fast]          # Parça 2 (c3–c5)        · --chapters c3,c4  yalnız bu bölümler · (bayraksız: tüm film)
  python3 qa_flow.py --reel --video out/reel_yonetmen.mp4   # + ffmpeg freezedetect (n=-55dB d=1 s)
  python3 qa_flow.py --calibrate                # durgunluk eşiği τ'yu ölçerek kalibre et (sabit çekim + reel)
Seçenekler: --workers 2 (≤4), --tau 0.40, --json out/qa_flow.json, --quiet. Python'dan: qa_flow.run(prog, fast=False, workers=2, spec=…) / qa_flow.main([...]).

Girdi: compose.Program(chapters=…, part=…) ya da çekim listesi (Program(shots=[…], end=T) — reel).
Çıktı: terminal tablosu + out/qa_flow.json (+ kısa özet). Kapı durumları: GEÇTİ / KALDI / UYARI (yönetmen onayı) / PAS (ölçülemedi ya da bu girdiye uygulanmaz — nedeni yazılır).

── Kapılar ──────────────────────────────────────────────────────────────
 (a) statik (çekim parametrelerinden):  kamera varlığı (+ hareket yeterliliği ≥%6 ölçek / ≥120 px) · gerekçeli geçiş (link oranı ≥%70; çıplak fade ≤%10;
     aynı geçişin üst üste ≥3 kullanımı) · çekim uzunluğu (medyan 4–6, p90 ≤12, max ≤16, longtake ≤28; <1,2 sn) · tür tekrarı (≤2, montage hariç) ·
     çapa tipi dağılımı (sözcük/cümle çapalı vs mutlak saniye; ≤%10 mutlak) · yön tutarlılığı (pan/slide/carry yönleri; bölümde yön bozma ≤1) ·
     altyazı bölgesi (tür düzen tablosundan: nominal metin altı + kamera kayması)
 (b) örnekleme (kare çizer): her 0,5 sn'de bir kare (240×135 gri) → ardışık fark (MAD; koyu karelerde parlaklıkla normalize: MAD/clamp(ort.parlaklık/150, 0,3, 1)) → DURGUNLUK (MAD<τ koşusu ≤1,5 sn) ve OLAY YOĞUNLUĞU
     (pencere başına ≥1 olay: kesme, geçiş ya da fark sıçraması; anlatı cümleleri varsa cümle penceresi, yoksa 3 sn penceresi)
 (c) video (isteğe bağlı): ffmpeg freezedetect.
 (d) ENG-B (Kasım 2026, kurul tur 1 B.9) yeni kapılar: ardışık itme ≤5 (gerçek kamera ailesi; kendi kamerası olan türlerde cams/path) · kart dizisi
     (ardışık kart ≤4 ve en geç 75 sn'de bir dünya/figür çekimi; aile haritası, p1_/pN_ öneki soyulur; shot(family=…) ya da sahne modülü AILE={tür: aile}
     ile etiketlenir) · sert kesme payı ≥%15 · geçiş süresi dağılımı σ ≥0,25 sn · ölçülen hareket (örnek karelerde kare farkı; >6 sn ve hareketsiz çekim)
     · ENG-A qa_yerlesim.py / qa_donem.py (varsa; --part modunda, alt süreçte).

── Kalibrasyon (τ) ─────────────────────────────────────────────────────
 τ = TAU. `--calibrate` ile ölçülür: (1) hiç kamera/olay içermeyen sabit çekimde MAD gürültü tabanı (toz zerreleri + tane); (2) reel'in kararlı bölümlerinde
 MAD dağılımı. τ bu ikisi arasında seçilir (sabit çekimi kesin yakalar, iyi hareketli çekimi yanlış işaretlemez). Ölçülen değerler: CALIBRATION_NOTE.
"""
import argparse
import json
import math
import multiprocessing as mp
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.chdir(HERE)

FPS = 24
STEP = 0.5                      # örnekleme adımı (sn): 2 kare/sn
TAU = 0.40                      # durgunluk eşiği (MAD, 0–255 gri düzey; 240×135) — CALIBRATION_NOTE'a bak
STILL_MAX = 1.5                 # sn
EVENT_REL = 2.2                 # olay: MAD, önceki 3 aralığın medyanının ≥2,2 katı ve ≥ 2τ  (ya da kesme/geçiş)
CALIBRATION_NOTE = ("kalibrasyon (18 Eki 2026, --calibrate + t_mad ölçümleri): sabit çekim MAD 0,03–0,04 (quote/timeline/title), 0,2 (medal: eğilme+parıltı), 0,8 (palle: yaldız parıltısı); "
                    "push %4/6 sn 0,6–1,5; push %6 0,85–1,9; varsayılan eski kamera 0,8–2,9; reel kararlı aralıklar p5=0,67 p10=1,17 medyan 4,2 → τ=0,40")
CARD_KINDS = ("chapter_card", "fresco_title", "outro", "black")
# altyazı bölgesi (SPEC y≈1250–1390 Shorts 1080×1920 koordinatıdır; 1920×1080 uzun filmde karşılığı alt şerit varsayımı): [üst, alt] px
SUB_ZONE = (938.0, 1042.0)
OK, FAIL, WARN, SKIP = "GEÇTİ", "KALDI", "UYARI", "PAS"
# ENG-B kapı eşikleri (KURUL.md B.9)
PUSH_RUN_MAX = 5                 # ardışık itme ailesi
CARD_RUN_MAX = 4                 # ardışık kart çekimi
WORLD_GAP_MAX = 75.0             # sn: en geç bu kadar sürede bir dünya/figür çekimi
CUT_SHARE_MIN = 0.15             # sert kesme payı hedefi
TR_SIGMA_MIN = 0.25              # geçiş süresi standart sapması (sn)
MOT_LONG = 6.0                   # sn: bundan uzun çekimlerde ölçülen hareket denetlenir
MOT_TAU = 1.25                   # 0,5 sn adımlı kare farkı medyanı bunun altındaysa "hareketsiz" (kalibrasyon 4 Kas: kurulun "durgun" dediği çekimler 0,78–1,23; canlı çekim medyanı ≈4,9)

# aile haritası (taban tür adı, p1_/pN_ öneki soyulmuş): dünya (mekân/şehir/panorama), figür (insan eylemi), kart (harita/madalya/belge/diyagram)
FAMILY_BASE = {
    **{k: "dunya" for k in ("oda", "sehir", "pano", "build", "skyline", "frieze", "procession", "deniz", "deniz_rota", "deniz_kiyi", "deniz_filo", "liman",
                            "theatre", "room", "field", "siege", "sea")},
    **{k: "kart" for k in ("map", "medal", "medals", "coin", "palle", "emblem", "counter", "bars", "stacked", "timeline", "tree", "network", "iconrow",
                           "quote", "title", "doc", "ledger", "letter", "black", "cephe")},
    # Parça 1 bölüm türleri (orta kare + kod okuması; AN2 sınıflamasıyla uyumlu)
    "c0_belge": "kart", "c0_gerekce": "kart", "c0_harita": "kart", "c0_kuyruk": "figur", "c0_sikke": "kart", "c0_takvim": "kart",
    "c1_agi": "kart", "c1_cicek": "kart", "c1_darphane": "dunya", "c1_edward": "kart", "c1_kademe": "kart", "c1_kardes": "kart", "c1_kose": "kart",
    "c1_lonca": "kart", "c1_machiavelli": "figur", "c1_okul": "figur", "c1_sokak": "dunya", "c1_toprak": "kart", "c1_yazi": "kart",
    "c2_ayrim": "kart", "c2_hediye": "kart", "c2_kalemler": "kart", "c2_kasa": "kart", "c2_katasto": "kart", "c2_mezar": "kart", "c2_nolist": "kart",
    "c2_rivayet": "kart", "c2_sadaka": "figur", "c2_borc": "kart",
}
_FAM_WORLD_TOK = ("sehir", "oda", "nef", "liman", "deniz", "pano", "saray", "sokak", "meydan", "skyline", "atolye", "galeri", "kusatma", "yuruyus",
                  "giostra", "turnuva", "akademi", "careggi", "heyet", "konsey", "sahne", "bargello", "pencere", "kule", "hucre", "sakristi", "kutuphane")
_FAM_CARD_TOK = ("map", "harita", "madalya", "medal", "doc", "defter", "ledger", "takvim", "sayac", "liste", "mektup", "_ag", "tree", "cetvel", "terazi",
                 "zaman", "yil", "plan", "tally", "fatura", "unvan", "gazete", "ferman", "kapak", "harf", "dna", "sektor", "pay", "baslik", "nota")


def base_kind(kind):
    """p1_oda → oda, p5g_pano → pano (parça sarmalayıcı öneki soyulur)."""
    import re
    return re.sub(r"^p\d+[a-z]*_", "", kind)


def family_of(s, prog=None):
    """Çekimin görsel ailesi: 'dunya' | 'figur' | 'kart' | 'belirsiz'. Öncelik: shot(family=…) → sahne modülü AILE sözlüğü → FAMILY_BASE → ad sezgisi."""
    fam = getattr(s, "family", None)
    if fam in ("dunya", "figur", "kart"):
        return fam
    bk = base_kind(s.kind)
    if prog is not None:
        for mod in getattr(prog, "_chap_mod", {}).values():
            ai = getattr(mod, "AILE", None)
            if ai and (s.kind in ai or bk in ai):
                return ai.get(s.kind, ai.get(bk))
    if bk in FAMILY_BASE:
        return FAMILY_BASE[bk]
    low = "_" + bk
    if any(t in low for t in _FAM_WORLD_TOK):
        return "dunya"
    if any(t in low for t in _FAM_CARD_TOK):
        return "kart"
    return "belirsiz"


def cam_family(s):
    """Çekimin GERÇEK kamera ailesi (qa): cam= (cilt_cam.describe; süreye bağlı miktarlar dahil); kendi kamerası olan türlerde (oda/pano/sehir/build
    ve sarmalayıcıları) cam= uygulanmaz → cams= anahtar karelerinden (zum ≥%5 ve kayma <140 px → itme/çekme; değilse kayma) ya da path adından."""
    import cilt_cam
    if s.kind in CARD_KINDS:
        return None
    if s.kind in cilt_cam.OWN_CAMERA:
        cams = s.params.get("cams")
        if cams:
            try:
                vals = [tuple(v[1]) for v in cams]
                xs, ys, zs = [v[0] for v in vals], [v[1] for v in vals], [(v[2] if len(v) > 2 else 1.0) for v in vals]
                d = dict(kind="keys", scale=max(zs) / max(1e-6, min(zs)) - 1.0, shift=max(max(xs) - min(xs), max(ys) - min(ys)),
                         h=xs[-1] - xs[0], v=-(ys[-1] - ys[0]), zdir=1 if zs[-1] > zs[0] * 1.005 else (-1 if zs[-1] < zs[0] / 1.005 else 0))
                return "own:" + cilt_cam._family_of(d)
            except Exception:
                return "own:yol"
        pth = str(s.params.get("path") or "")
        return "own:push" if pth in ("in", "push") else ("own:pull" if pth in ("out", "pull") else "own:yol")
    if s.cam is None:
        return "yok"
    try:
        return cilt_cam.family(s.cam, s.dur)
    except Exception:
        return "?"


# ───────────────────────────── yardımcılar ─────────────────────────────
def make_program(spec):
    import compose
    if spec.get("reel"):
        import preview_reel
        return preview_reel.build_program()
    if spec.get("shots") is not None:
        return compose.Program(shots=spec["shots"], end=spec.get("end"))
    return compose.Program(chapters=spec.get("chapters"), part=spec.get("part"))


def run_shots(shots, end=None, fast=False, workers=2, **kw):
    """Çekim listesi girdisi (Program(shots=…) ile kurulur; a = mutlak saniye): qa_flow.run_shots(liste, end=T). Liste/parametreler pickle edilemezse örnekleme tek işlemde yapılır."""
    spec = dict(shots=list(shots), end=end)
    return run(make_program(spec), fast=fast, workers=workers, spec=spec, title=kw.pop("title", "çekim listesi"), **kw)


def _pct(vals, q):
    if not vals:
        return 0.0
    v = sorted(vals)
    i = (len(v) - 1) * q
    lo, hi = int(math.floor(i)), int(math.ceil(i))
    return v[lo] + (v[hi] - v[lo]) * (i - lo)


def _describe(spec):
    if spec is None:
        return None
    import cilt_cam
    return cilt_cam.describe(spec)


def _anchor_type(a):
    if isinstance(a, bool):
        return None
    if isinstance(a, (int, float)):
        return "abs"
    if isinstance(a, str):
        return "sent"
    if isinstance(a, (tuple, list)) and a:
        if len(a) == 2 and isinstance(a[0], str):
            return "sent"
        if len(a) >= 3 and isinstance(a[0], str):
            return "word"
    return None


def _walk_anchors(params):
    """Çekim parametrelerinde açıkça verilmiş çapaları topla: at/*_at/strike/hl/move_at anahtarları, cams, lines/events/edges son elemanları."""
    out = []

    def keyok(k):
        return k == "at" or k.endswith("_at") or k in ("strike", "hl", "move_at")

    def walk(o, depth=0):
        if depth > 4:
            return
        if isinstance(o, dict):
            for k, v in o.items():
                if isinstance(k, str) and keyok(k):
                    t = _anchor_type(v)
                    if t:
                        out.append(t)
                else:
                    walk(v, depth + 1)
        elif isinstance(o, (list, tuple)):
            for it in o:
                walk(it, depth + 1)
    for k, v in params.items():
        if k in ("view", "cam", "size", "pos", "focus"):
            continue
        if keyok(k):
            t = _anchor_type(v)
            if t:
                out.append(t)
        elif k == "cams" and isinstance(v, (list, tuple)):
            for it in v:
                t = _anchor_type(it[0]) if isinstance(it, (list, tuple)) and it else None
                if t:
                    out.append(t)
        elif k in ("lines", "events", "edges") and isinstance(v, (list, tuple)):
            for it in v:
                if isinstance(it, (list, tuple)) and len(it) >= 2:
                    t = _anchor_type(it[-1])
                    if t:
                        out.append(t)
        else:
            walk(v, 1)
    return out


# ───────────────────────────── altyazı bölgesi (tür düzen tablosu) ─────────────────────────────
def _text_bottom(kind, p):
    """Kinds'ın sabit düzeninden metin taşıyan en alt nominal y (px) — yaklaşık; bilinmeyen tür → None."""
    H = 1080.0
    if kind in ("coin", "palle"):
        return H * 0.865 + 14 if p.get("caption") else (H * 0.80 + 12 if p.get("sub") else None)
    if kind == "emblem":
        return H * 0.89 + 14 if p.get("caption") else (H * 0.82 + 12 if p.get("sub") else None)
    if kind == "medal":
        if p.get("name"):
            return H * 0.775 + 104 + (40 if p.get("role") else 0) + (34 if p.get("dates") else 0)
        return H * 0.44 + 640 / 2
    if kind == "counter":
        size = p.get("size", 200)
        y = H * 0.47 + size * 0.34
        return y + (204 if p.get("sub") else (150 if p.get("label") else (82 if p.get("unit", "florin") else 0))) + 12
    if kind == "quote":
        return 780.0
    if kind == "timeline":
        return H * 0.52 + 150
    if kind in ("tree", "network"):
        ys = [n.get("y", 0.5) for n in p.get("nodes", [])]
        sz = p.get("size", 200 if kind == "tree" else 150)
        return (max(ys) * H + sz / 2 + 104) if ys else None
    if kind == "title":
        sz = p.get("size", 170)
        y = H * p.get("y", 0.50) + sz * 0.34
        return y + sz * 0.20 + 82 + 14 if p.get("sub") else y + sz * 0.2 + 20
    return None


def _cam_down_shift(spec, text_y):
    """Kamera nedeniyle içeriğin en çok AŞAĞI kayması (px): crane up (içerik aşağı), itme (pivot=merkez; alt metin aşağı iner)."""
    d = _describe(spec)
    if not d:
        return 0.0
    dn = 0.0
    if d.get("kind") == "crane" and d.get("dir") == "up":
        dn += d["shift"] / 2.0
    elif d.get("kind") in ("keys", "track"):
        dn += max(0.0, d.get("v", 0.0)) / 2.0
    dn += max(0.0, d.get("scale", 0.0)) * max(0.0, text_y - 540.0)
    return dn


# ───────────────────────────── statik analiz ─────────────────────────────
def static_analysis(prog):
    import cilt_cam
    shots = prog.shots
    chap_mode = bool(getattr(prog, "hud", False))

    def ckey(s):
        if s.kind in CARD_KINDS:
            return "kart"
        if not chap_mode:
            return "reel"
        cid = prog._chapter_of(s.t0 + 0.01)
        return cid or "?"
    rows = []
    by_ch = {}
    for s in shots:
        r = dict(i=s.i, kind=s.kind, label=s.label, t0=round(s.t0, 2), dur=round(s.dur, 2), cam=repr(s.cam) if s.cam is not None else None, link=s.link,
                 tr=(list(s.tr_eff[:2]) if getattr(s, "tr_eff", None) else None), longtake=s.longtake, montage=s.montage, ch=ckey(s), card=s.kind in CARD_KINDS,
                 cut_explicit=bool(s.tr) and not getattr(s, "tr_eff", None), cam_auto=bool(getattr(s, "cam_auto", False)),
                 aile=family_of(s, prog) if s.kind not in CARD_KINDS else "kart*", camfam=cam_family(s))
        rows.append(r)
        by_ch.setdefault(r["ch"], []).append(r)
    gates = []
    real = [r for r in rows if not r["card"]]

    # 1) kamera varlığı (cam= verilmemiş çekimlere Program tohumlu hareket seçer: cam_auto)
    own = set(cilt_cam.OWN_CAMERA)                      # kendi kamera yolu olan türler (pano/build): yerleşik kamera sayılır
    missing = [r for r in real if r["cam"] is None and r["kind"] not in own]
    autos = [s for s in shots if getattr(s, "cam_auto", False)]
    weak, bad = [], []
    for s in shots:
        if s.kind in CARD_KINDS or s.cam is None or s.kind in own:
            continue
        try:
            if not cilt_cam.motion_ok(s.cam, s.dur):
                weak.append(f"#{s.i} {s.kind} '{s.label}': {s.cam!r} (%6 ölçek / 120 px altında)")
        except Exception as e:
            bad.append(f"#{s.i} {s.kind}: cam={s.cam!r} ayrıştırılamadı ({e})")
    n_real = max(1, len(real))
    st = SKIP if not real else (OK if (not missing and not bad) else FAIL)
    gates.append(dict(name="Kamera varlığı", status=st, value=f"{len(real) - len(missing)}/{len(real)} çekimde kamera var (%{100 * (len(real) - len(missing)) / n_real:.0f}); otomatik seçilen {len(autos)}",
                      thr="%100 (cam= yoksa Program tohumlu seçer)", detail=[f"cam= YOK: #{r['i']} {r['kind']} '{r['label']}'" for r in missing[:30]] + bad +
                      [f"otomatik: #{s.i} {s.kind} '{s.label}' → {s.cam!r}" for s in autos[:30]]))
    gates.append(dict(name="Kamera hareket yeterliliği", status=OK if not weak else WARN, value=f"{len(weak)} çekim zayıf", thr="≥%6 ölçek ya da ≥120 px kayma", detail=weak[:30]))

    # 2) gerekçeli geçiş
    cand = []
    for ch, lst in by_ch.items():
        rr = [r for r in lst if not r["card"]]
        cand += rr[1:]                                   # bölümün ilk çekimi karttan/açılıştan gelir
    n_c = max(1, len(cand))
    unj = [r for r in cand if r["link"] in (None, "", "none") and not r["cut_explicit"]]        # tr="cut" birinci sınıf kesmedir: gerekçesi kendisi
    linked = len(cand) - len(unj)
    fade_bare = [r for r in cand if r["tr"] and r["tr"][0] == "fade" and r["link"] in (None, "", "none")]
    hard_bare = [r for r in cand if not r["tr"] and r["link"] in (None, "", "none") and not r["cut_explicit"]]
    ratio = linked / n_c
    fr = len(fade_bare) / n_c
    trs = {}
    for r in cand:
        k = r["tr"][0] if r["tr"] else "kesme"
        trs[k] = trs.get(k, 0) + 1
    runs3, prev, run = [], None, 0
    for r in rows:
        k = r["tr"][0] if r["tr"] else None
        run = run + 1 if (k and k == prev) else 1
        if k and run >= 3:
            runs3.append(f"#{r['i']} '{k}' üst üste {run}. kez")
        prev = k if k else None
    vocab = {"shape", "color", "dir", "cam", "scale", "carry", "light", "material", "audio"}
    odd = sorted({str(r["link"]) for r in cand if r["link"] not in (None, "", "none") and r["link"] not in vocab})
    st = SKIP if not cand else (OK if (ratio >= 0.70 and fr <= 0.10 and not runs3) else (FAIL if (ratio < 0.70 or fr > 0.10) else WARN))
    gates.append(dict(name="Gerekçeli geçiş", status=st, value=f"link≠none %{100 * ratio:.0f} ({linked}/{len(cand)}); çıplak fade %{100 * fr:.0f}; çıplak kesme {len(hard_bare)}",
                      thr="link ≥%70 · çıplak fade ≤%10 · aynı geçiş ≥3 üst üste yok",
                      detail=[f"dağılım: {trs}"] + ([f"sözlük dışı link değerleri: {odd} (beklenen: {sorted(vocab)})"] if odd else []) + [f"gerekçesiz: #{r['i']} {r['kind']} '{r['label']}' tr={r['tr']}" for r in unj[:25]] + runs3))

    # 3) çekim uzunluğu
    det, worst = [], OK
    for ch, lst in by_ch.items():
        rr = [r for r in lst if not r["card"]]
        if not rr:
            continue
        norm = [r["dur"] for r in rr if not r["longtake"]]
        med, p90, mx = _pct(norm, 0.5), _pct(norm, 0.9), (max(norm) if norm else 0)
        bad_ = []
        if norm and not (4.0 <= med <= 6.0):
            bad_.append(f"medyan {med:.1f} (4–6 dışı)")
        if p90 > 12.0:
            bad_.append(f"p90 {p90:.1f} > 12")
        if mx > 16.0:
            bad_.append(f"max {mx:.1f} > 16")
        lt = [r for r in rr if r["longtake"] and r["dur"] > 28.0]
        if lt:
            bad_.append(f"longtake > 28 sn: {[r['i'] for r in lt]}")
        short = [r for r in rr if r["dur"] < 1.2]
        if short:
            bad_.append(f"<1,2 sn: {[r['i'] for r in short]}")
        if bad_:
            worst = WARN
        det.append(f"{ch}: {len(rr)} çekim · medyan {med:.1f} · p90 {p90:.1f} · max {mx:.1f}" + (("  ⚠ " + "; ".join(bad_)) if bad_ else ""))
    gates.append(dict(name="Çekim uzunluğu", status=worst, value=f"{len(real)} çekim", thr="medyan 4–6 · p90 ≤12 · max ≤16 (longtake ≤28) · ≥1,2 sn (ağır/mizah bölümde bant kayar → UYARI)", detail=det))

    # 4) tür tekrarı
    rep, run, prev = [], 0, None
    for s in shots:
        if s.kind in CARD_KINDS:
            prev, run = None, 0
            continue
        run = run + 1 if (s.kind == prev and not s.montage) else 1
        prev = s.kind
        if run >= 3:
            rep.append(f"#{s.i} '{s.kind}' üst üste {run}. çekim ({s.label})")
    gates.append(dict(name="Tür tekrarı", status=OK if not rep else FAIL, value=f"{len(rep)} ihlal", thr="aynı kind üst üste ≤2 (montage=True hariç)", detail=rep))

    # 5) çapa denetimi
    cnt = {"abs": 0, "sent": 0, "word": 0}
    for s in shots:
        if s.kind in CARD_KINDS:
            continue
        t = _anchor_type(s.a)
        if t:
            cnt[t] += 1
        for t in _walk_anchors(s.params):
            cnt[t] += 1
    tot = sum(cnt.values())
    if tot == 0:
        gates.append(dict(name="Çapa denetimi", status=SKIP, value="çapa bulunamadı (çekim yok / yer tutucu)", thr="mutlak ≤%10; çapalı ≥%90", detail=[]))
    elif not chap_mode:
        gates.append(dict(name="Çapa denetimi", status=SKIP, value=f"mutlak {cnt['abs']} / cümle {cnt['sent']} / sözcük {cnt['word']}", thr="mutlak ≤%10; çapalı ≥%90",
                          detail=["reel çapasız (mutlak saniye) çalışır; kapı sahne dosyalarında (Program(chapters=…)) uygulanır"]))
    else:
        ab = cnt["abs"] / max(1, tot)
        gates.append(dict(name="Çapa denetimi", status=OK if ab <= 0.10 else FAIL, value=f"sözcük {cnt['word']} · cümle {cnt['sent']} · mutlak {cnt['abs']} (mutlak %{100 * ab:.0f})", thr="mutlak ≤%10 (çapalı ≥%90)",
                          detail=["kapsam: çekim başlangıç çapası + at/*_at/strike/hl/move_at/cams/lines/events/edges anahtarları"]))

    # 6) yön denetimi
    dirs = []
    for s in shots:
        if s.kind in CARD_KINDS:
            continue
        d = _describe(s.cam) if s.cam is not None else None
        sg = 0
        if d:
            hh = d.get("h", 0.0)
            sg = 1 if hh > 20 else (-1 if hh < -20 else 0)
        te = getattr(s, "tr_eff", None)
        tg = 0
        if te:
            o = te[2]
            if te[0] in ("slide", "carry"):
                tg = 1 if o.get("dir", "r") in ("r", "u") else -1
            elif te[0] == "whip":
                tg = 1
        dirs.append((s.i, s.kind, sg, tg, ckey(s)))
    wd, perch = [], {}
    for i, k, sg, tg, ch in dirs:
        if sg:
            perch.setdefault(ch, []).append(sg)
    info = []
    for ch, v in perch.items():
        pos, neg = v.count(1), v.count(-1)
        if pos and neg:
            if min(pos, neg) > 1:
                wd.append(f"{ch}: yatay kamera yönleri karışık (sağ {pos}, sol {neg}) — yön bozma bölümde ≤1 olmalı (§1-6)")
            else:
                info.append(f"{ch}: bilinçli yön bozma 1 (sağ {pos}, sol {neg}) — dramatik gerekçe yönetmen kartında yazılı olmalı")
    for (i, k, sg, tg, ch), (i2, k2, sg2, tg2, ch2) in zip(dirs[:-1], dirs[1:]):
        if sg and tg2 and sg * (1 if tg2 > 0 else -1) < 0:
            wd.append(f"#{i2} {k2}: giriş geçişi yönü ({'r' if tg2 > 0 else 'l'}) önceki çekim kamerasıyla ({'sağ' if sg > 0 else 'sol'}) çelişiyor")

    def head(c):
        return c if isinstance(c, str) else (c[0] if isinstance(c, tuple) and c and isinstance(c[0], str) else None)
    for s0, s1 in zip(shots[:-1], shots[1:]):
        if {head(s0.cam), head(s1.cam)} == {"push", "pull"} and s1.link in (None, "", "none"):
            wd.append(f"#{s1.i}: push↔pull art arda ve aralarında gerekçe (link) yok")
    gates.append(dict(name="Yön denetimi", status=OK if not wd else WARN, value=f"{len(wd)} uyarı" + (f" · {len(info)} bilinçli yön bozma" if info else ""), thr="pan/slide yönleri §1-6 ile çelişmesin; yön bozma ≤1/bölüm (uyarı listesi → yönetmen onayı)", detail=wd + info))

    # 7) altyazı bölgesi (parametre tabanlı)
    zn, notmeas, hits = SUB_ZONE, [], []
    for s in shots:
        if s.kind in CARD_KINDS:
            continue
        tb = _text_bottom(s.kind, s.params)
        if tb is None:
            if s.kind in ("ledger", "letter", "doc", "map", "frieze", "skyline", "bars", "stacked", "iconrow", "medals"):
                notmeas.append(s.kind)
            continue
        shift = _cam_down_shift(s.cam, tb)
        if tb + shift > zn[0]:
            hits.append(f"#{s.i} {s.kind} '{s.label}': metin altı ≈{tb:.0f}px" + (f" + kamera kayması {shift:.0f}px" if shift > 1 else "") + f" > bölge üstü {zn[0]:.0f}px")
    nm = sorted(set(notmeas))
    gates.append(dict(name="Altyazı bölgesi", status=OK if not hits else WARN, value=f"{len(hits)} çekimde nominal metin/kamera kayması bölgeye giriyor",
                      thr="bölge dışı (SPEC y≈1250–1390 → 1080p varsayımı: alt şerit y≈%d–%d)" % (zn[0], zn[1]),
                      detail=hits + ([f"ölçülemedi (tür düzen tablosu yok / serbest çizim): {', '.join(nm)}"] if nm else []) + ["not: SPEC koordinatı 1080×1920 Shorts düzenine ait; uzun filmde altyazı varsayımı alt şerit"]))
    gates.append(_card_gate(prog, by_ch, chap_mode))
    gates += _engb_static_gates(prog, rows, cand)
    return dict(rows=rows, gates=gates)


def _runs(seq, pred):
    """seq içinde pred'i sağlayan ardışık koşular → [(baş, son)] (indeksler)."""
    out, i = [], 0
    while i < len(seq):
        if pred(seq[i]):
            j = i
            while j + 1 < len(seq) and pred(seq[j + 1]):
                j += 1
            out.append((i, j))
            i = j + 1
        else:
            i += 1
    return out


def _engb_static_gates(prog, rows, cand):
    """KURUL B.9 (ENG-B): ardışık itme, kart dizisi + dünya aralığı, sert kesme payı, geçiş süresi dağılımı."""
    gates = []
    real = [r for r in rows if not r["card"]]
    # (a) ardışık itme: gerçek kamera ailesi (kart türleri diziyi böler)
    seq = [r for r in rows]
    pr = _runs(seq, lambda r: (not r["card"]) and (r["camfam"] in ("push", "own:push")))
    longest = max([b - a + 1 for a, b in pr], default=0)
    bad = [(a, b) for a, b in pr if b - a + 1 > PUSH_RUN_MAX]
    fams = {}
    for r in real:
        fams[r["camfam"]] = fams.get(r["camfam"], 0) + 1
    gates.append(dict(name="Ardışık itme", status=OK if not bad else FAIL, value=f"en uzun itme dizisi {longest}; {len(bad)} dizi > {PUSH_RUN_MAX}",
                      thr=f"≤{PUSH_RUN_MAX} ardışık itme (kendi kameralı türlerde cams/path)",
                      detail=[f"aile dağılımı: {dict(sorted(fams.items(), key=lambda kv: -kv[1]))}"] +
                             [f"#{seq[a]['i']}–#{seq[b]['i']} ({seq[a]['t0']:.1f}–{seq[b]['t0'] + seq[b]['dur']:.1f} sn): {b - a + 1} itme" for a, b in bad]))
    # (b) kart dizisi + dünya/figür aralığı
    if not real:
        gates.append(dict(name="Kart dizisi", status=SKIP, value="çekim yok", thr="", detail=[]))
    else:
        kr = _runs(seq, lambda r: (not r["card"]) and r["aile"] in ("kart", "belirsiz"))
        klong = max([b - a + 1 for a, b in kr], default=0)
        kbad = [(a, b) for a, b in kr if b - a + 1 > CARD_RUN_MAX]
        t_start = prog.t_off
        t_end = max((r["t0"] + r["dur"] for r in real), default=t_start)
        worlds = [(r["t0"], r["t0"] + r["dur"]) for r in real if r["aile"] in ("dunya", "figur")]
        gaps, prev_end = [], t_start
        for (a_, b_) in worlds:
            if a_ - prev_end > 0:
                gaps.append((prev_end, a_))
            prev_end = max(prev_end, b_)
        if t_end - prev_end > 0:
            gaps.append((prev_end, t_end))
        gmax = max([b_ - a_ for a_, b_ in gaps], default=0.0)
        gbad = [(a_, b_) for a_, b_ in gaps if b_ - a_ > WORLD_GAP_MAX]
        unk = sorted({r["kind"] for r in real if r["aile"] == "belirsiz"})
        st = OK if (not kbad and not gbad) else FAIL
        share = sum(r["dur"] for r in real if r["aile"] in ("dunya", "figur")) / max(1e-6, sum(r["dur"] for r in real))
        gates.append(dict(name="Kart dizisi", status=st,
                          value=f"kart dizisi en uzun {klong} ({len(kbad)} > {CARD_RUN_MAX}); dünyasız en uzun {gmax:.0f} sn; dünya/figür %{100 * share:.0f}",
                          thr=f"ardışık kart ≤{CARD_RUN_MAX} · ≤{WORLD_GAP_MAX:.0f} sn'de bir dünya/figür",
                          detail=[f"#{seq[a]['i']}–#{seq[b]['i']} ({seq[a]['t0']:.1f}–{seq[b]['t0'] + seq[b]['dur']:.1f} sn): {b - a + 1} kart üst üste" for a, b in kbad] +
                                 [f"dünyasız aralık {a_:.1f}–{b_:.1f} sn ({b_ - a_:.0f} sn)" for a_, b_ in gbad] +
                                 ([f"ailesi belirsiz türler (kart sayıldı; shot(family=…) ya da sahne modülünde AILE={{tür: aile}}): {unk}"] if unk else [])))
    # (c) sert kesme payı (bölüm içi çekim sınırları; kart girişleri hariç)
    cuts = [r for r in cand if not r["tr"]]
    n = max(1, len(cand))
    cs = len(cuts) / n
    gates.append(dict(name="Sert kesme payı", status=SKIP if not cand else (OK if cs >= CUT_SHARE_MIN else FAIL),
                      value=f"%{100 * cs:.0f} ({len(cuts)}/{len(cand)} sınır; açık tr=\"cut\" {sum(1 for r in cuts if r['cut_explicit'])})",
                      thr=f"≥%{100 * CUT_SHARE_MIN:.0f} (tr=\"cut\" / None)", detail=[f"kesmeler: {[r['i'] for r in cuts]}"]))
    # (d) geçiş süresi dağılımı (tasarlı geçişler; kart girişleri hariç)
    durs = [float(r["tr"][1]) for r in cand if r["tr"]]
    if len(durs) >= 3:
        mu = sum(durs) / len(durs)
        sd = (sum((d - mu) ** 2 for d in durs) / len(durs)) ** 0.5
        hist = {}
        for d in durs:
            b_ = "≤0,4" if d <= 0.4 else ("0,4–0,8" if d < 0.8 else ("0,8–1,2" if d <= 1.2 else ("1,2–1,8" if d <= 1.8 else ">1,8")))
            hist[b_] = hist.get(b_, 0) + 1
        gates.append(dict(name="Geçiş süresi dağılımı", status=OK if sd >= TR_SIGMA_MIN else FAIL, value=f"σ {sd:.2f} sn (ort. {mu:.2f}, {len(durs)} geçiş) {hist}",
                          thr=f"σ ≥ {TR_SIGMA_MIN} sn (aralık 0,25–2,4)", detail=[]))
    else:
        gates.append(dict(name="Geçiş süresi dağılımı", status=SKIP, value=f"{len(durs)} geçiş (≥3 gerekli)", thr=f"σ ≥ {TR_SIGMA_MIN} sn", detail=[]))
    return gates


def motion_gate(prog, ns, mads):
    """Ölçülen hareket: 0,5 sn adımlı örnek kare farkı (MAD, parlaklık normalize) çekim içinde (geçiş pencereleri hariç) → MOT_LONG sn'den uzun ve
    medyanı MOT_TAU altında kalan çekimler "hareketsiz" (nominal cam= ne derse desin). Dönüş: (kapı, çekim başı ölçüm listesi)."""
    per = {}
    for i in range(len(mads)):
        g0, g1 = ns[i] / FPS + prog.t_off, ns[i + 1] / FPS + prog.t_off
        a, b = prog.shot_at(g0), prog.shot_at(g1)
        if a != b or prog._trans_at(g0, a) is not None or prog._trans_at(g1, b) is not None:
            continue
        per.setdefault(a, []).append(mads[i])
    rows, flagged = [], []
    for si, vals in per.items():
        s = prog.shots[si]
        if s.kind in CARD_KINDS or not vals:
            continue
        med = sorted(vals)[len(vals) // 2]
        rows.append(dict(i=si, kind=s.kind, label=s.label, t0=round(s.t0, 1), dur=round(s.dur, 1), mad_med=round(med, 3), n=len(vals)))
        if s.dur > MOT_LONG and med < MOT_TAU:
            flagged.append(rows[-1])
    st = OK if not flagged else FAIL
    return dict(name="Ölçülen hareket", status=st, value=f"{len(flagged)} çekim >{MOT_LONG:.0f} sn ve hareketsiz (medyan MAD<{MOT_TAU})",
                thr=f">{MOT_LONG:.0f} sn çekimde medyan kare farkı ≥{MOT_TAU} (0,5 sn adım; geçişler hariç)",
                detail=[f"#{r['i']} {r['kind']} '{r['label']}' {r['t0']}s ({r['dur']} sn): medyan {r['mad_med']}" for r in flagged]), rows


def eng_a_gates(part, timeout=1800):
    """ENG-A denetimleri (varsa): qa_yerlesim.py, qa_donem.py — alt süreçte (kendi argparse'ları ve kayıt bayrakları ile), çıkış kodu → kapı."""
    import subprocess
    out = []
    for fn, name in (("qa_yerlesim.py", "Yerleşim (ENG-A)"), ("qa_donem.py", "Dönem (ENG-A)")):
        path = os.path.join(HERE, fn)
        if not os.path.exists(path):
            continue
        try:
            r = subprocess.run([sys.executable, path, "--part", str(part)], capture_output=True, text=True, timeout=timeout, cwd=HERE)
            lines = [l for l in r.stdout.splitlines() if l.strip() and "Fontconfig" not in l]
            summ = next((l for l in lines if l.startswith(fn.split(".")[0])), lines[0] if lines else "(çıktı yok)")
            st = OK if r.returncode == 0 else (FAIL if r.returncode == 1 else SKIP)
            det = [l.strip() for l in lines if l.lstrip().startswith("✗")][:20]
            if st == SKIP:
                det.append((r.stderr or "").strip().splitlines()[-1] if r.stderr.strip() else f"çıkış kodu {r.returncode}")
            out.append(dict(name=name, status=st, value=summ[:180], thr=f"{fn} çıkış kodu 0", detail=det))
        except Exception as e:                                                    # noqa
            out.append(dict(name=name, status=SKIP, value=f"çalıştırılamadı: {type(e).__name__}: {e}"[:180], thr=f"{fn}", detail=[]))
    return out


def _card_gate(prog, by_ch, chap_mode):
    """Yönetmen kartı (yonetmen_cK.md, REHBER §11) ↔ shots çapraz denetimi: tablo satır sayısı ve tür sırası."""
    if not chap_mode:
        return dict(name="Yönetmen kartı", status=SKIP, value="reel/çekim listesi: kart yok", thr="her bölümde yonetmen_cK.md", detail=[])
    det, bad = [], 0
    for ch, lst in by_ch.items():
        if ch in ("kart", "?"):
            continue
        rr = [r for r in lst if not r["card"]]
        if not rr:
            continue
        path = os.path.join(HERE, f"yonetmen_{ch}.md")
        if not os.path.exists(path):
            det.append(f"{ch}: yonetmen_{ch}.md YOK ({len(rr)} çekim)")
            bad += 1
            continue
        rows_md = []
        for ln in open(path, encoding="utf-8"):
            cells = [c.strip() for c in ln.strip().strip("|").split("|")]
            if ln.lstrip().startswith("|") and len(cells) >= 5 and not set(ln.strip()) <= set("|-: "):
                rows_md.append(cells)
        rows_md = [c for c in rows_md if c[0].lower() not in ("çekim", "cekim")]
        kinds_md = [c[2].lower() for c in rows_md]
        kinds_sh = [r["kind"].lower() for r in rr]
        if len(rows_md) != len(rr):
            det.append(f"{ch}: kartta {len(rows_md)} satır, shots'ta {len(rr)} çekim")
            bad += 1
        elif kinds_md != kinds_sh:
            k = next(i for i, (a, b) in enumerate(zip(kinds_md, kinds_sh)) if a != b)
            det.append(f"{ch}: {k + 1}. çekimde tür farkı (kart '{kinds_md[k]}', shots '{kinds_sh[k]}')")
            bad += 1
    return dict(name="Yönetmen kartı", status=OK if not bad else WARN, value=f"{bad} bölümde kart eksik/uyumsuz", thr="her bölümde yonetmen_cK.md ve shots ile uyumlu", detail=det[:30])


# ───────────────────────────── örnekleme analizi ─────────────────────────────
def _sample_worker(args):
    spec, ns = args
    import cv2
    import numpy as np
    cv2.setNumThreads(1)
    prog = make_program(spec)
    prev = None
    first = last = None
    mads, chgs, ms, lums = [], [], [], []
    for n in ns:
        t0 = time.perf_counter()
        img = prog.frame(n, post=False)
        ms.append((time.perf_counter() - t0) * 1000)
        gray = cv2.cvtColor(cv2.resize(img, (240, 135), interpolation=cv2.INTER_AREA), cv2.COLOR_RGB2GRAY)
        if first is None:
            first = gray
        if prev is not None:
            d = np.abs(gray.astype(np.int16) - prev.astype(np.int16))
            mads.append(float(d.mean()))
            chgs.append(float((d > 8).mean()))
            lums.append(0.5 * (float(gray.mean()) + float(prev.mean())))
        prev = gray
        last = gray
    return ns, mads, chgs, first, last, ms, lums


def sample_series(spec, prog, workers=2, verbose=True):
    """Programı 2 kare/sn örnekle → (ns, mad[i] = i. ve i+1. örnek arası fark, chg, ms)."""
    import numpy as np
    n_end = int(math.floor(prog.total * FPS))
    step = int(round(STEP * FPS))
    ns = list(range(0, n_end, step))
    if len(ns) < 2:
        return ns, [], [], []
    k = max(1, min(workers, 4))
    blocks = [ns[i * len(ns) // k:(i + 1) * len(ns) // k] for i in range(k)]
    blocks = [b for b in blocks if b]
    t0 = time.time()
    try:
        import pickle
        pickle.dumps(spec)
        picklable = True
    except Exception:
        picklable = False
    if picklable and len(blocks) > 1:
        ctx = mp.get_context("spawn")
        with ctx.Pool(len(blocks)) as pool:
            res = pool.map(_sample_worker, [(spec, b) for b in blocks])
    else:                                                    # pickle edilemeyen çekim listesi (lambda vb.) ya da tek işlem
        res = [_sample_worker((spec, b)) for b in blocks]
    mads, chgs, ms, lums = [], [], [], []
    for i, (b, m, c, first, last, ts, lu) in enumerate(res):
        mads += m
        chgs += c
        ms += ts
        lums += lu
        if i + 1 < len(res):                                   # blok sınırı: son örnek ↔ sonraki bloğun ilk örneği
            nf = res[i + 1][3]
            d = np.abs(last.astype(np.int16) - nf.astype(np.int16))
            mads.append(float(d.mean()))
            chgs.append(float((d > 8).mean()))
            lums.append(0.5 * (float(last.mean()) + float(nf.mean())))
    if verbose:
        print(f"  örnekleme: {len(ns)} kare, {len(blocks)} işlem, {time.time() - t0:.0f} sn (ortalama {np.mean(ms):.0f} ms/kare)", flush=True)
    # parlaklık normalizasyonu: koyu (gece) karelerde mutlak fark küçük kalır → MAD / clamp(ort. parlaklık/150, 0,3, 1)
    mads = [m / min(1.0, max(0.30, lu / 150.0)) for m, lu in zip(mads, lums)]
    return ns, mads, chgs, ms


def analyze_series(prog, ns, mads, chgs, tau, chap_mode):
    """Durgunluk koşuları + olay yoğunluğu."""
    gates = []
    if not mads:
        return dict(gates=gates, runs=[], intervals=[])
    mids = [((ns[i] + ns[i + 1]) / 2.0) / FPS + prog.t_off for i in range(len(mads))]
    cut_in = []                                              # aralığın içinde kesme ya da geçiş var mı
    for i in range(len(mads)):
        g0, g1 = ns[i] / FPS + prog.t_off, ns[i + 1] / FPS + prog.t_off
        a, b = prog.shot_at(g0), prog.shot_at(g1)
        cut_in.append(a != b or prog._trans_at(g0, a) is not None or prog._trans_at(g1, b) is not None)
    still = [m < tau for m in mads]
    runs, i = [], 0
    while i < len(still):
        if still[i]:
            j = i
            while j + 1 < len(still) and still[j + 1]:
                j += 1
            runs.append((i, j))
            i = j + 1
        else:
            i += 1
    long_runs, worst = [], 0.0
    for (a, b) in runs:
        dur = (b - a + 1) * STEP
        worst = max(worst, dur)
        si = prog.shot_at(mids[a])
        s = prog.shots[si]
        if dur > STILL_MAX + 1e-6:
            long_runs.append(dict(shot=si, kind=s.kind, label=s.label, t=round(ns[a] / FPS + prog.t_off, 1), dur=dur, mad_med=round(float(sorted(mads[a:b + 1])[(b - a) // 2]), 3)))
    gates.append(dict(name="Durgunluk", status=OK if worst <= STILL_MAX + 1e-6 else FAIL,
                      value=f"en uzun durgun koşu {worst:.1f} sn (MAD<{tau}); durgun aralık %{100 * sum(still) / len(still):.0f}", thr=f"≤{STILL_MAX} sn (τ={tau}; {CALIBRATION_NOTE})",
                      detail=[f"#{r['shot']} {r['kind']} '{r['label']}' t={r['t']}s: {r['dur']:.1f} sn durgun (medyan MAD {r['mad_med']})" for r in long_runs[:30]]))
    events = []
    for i, m in enumerate(mads):
        ev = cut_in[i]
        if not ev and i >= 1:
            base = sorted(mads[max(0, i - 3):i])
            ev = (m >= EVENT_REL * max(base[len(base) // 2], 1e-6)) and m >= 2 * tau
        if not ev and i == 0:
            ev = m >= 2 * tau
        events.append(ev)
    if chap_mode and prog.tl.sent:
        wins = [(se["t0"], se["t1"], sid) for sid, se in ((s_, prog.tl.sent[s_]) for s_ in prog.tl.order) if prog.t_off - 1e-6 <= se["t0"] <= prog.t_off + prog.total]
        kind_w = "cümle"
    else:
        wins = [(prog.t_off + k * 3.0, prog.t_off + (k + 1) * 3.0, f"w{k}") for k in range(int(prog.total // 3.0))]
        kind_w = "3 sn penceresi (anlatı cümleleri yok)"
    miss = []
    for (a, b, sid) in wins:
        idx = [i for i in range(len(mads)) if a - STEP <= mids[i] <= b + STEP]
        if idx and not any(events[i] for i in idx):
            miss.append((sid, round(a, 1)))
    tot = max(1, len(wins))
    frac = 1.0 - len(miss) / tot
    gates.append(dict(name="Olay yoğunluğu", status=OK if frac >= 0.95 else FAIL, value=f"%{100 * frac:.0f} {kind_w} ≥1 olay ({tot - len(miss)}/{tot})", thr="≥%95",
                      detail=[f"olaysız: {sid} (t={t}s)" for sid, t in miss[:25]]))
    return dict(gates=gates, runs=long_runs, intervals=[dict(g=round(ns[i] / FPS + prog.t_off, 2), mad=round(mads[i], 3), chg=round(chgs[i], 4), ev=bool(events[i]), cut=bool(cut_in[i])) for i in range(len(mads))])


def freeze_check(video):
    import re
    import subprocess
    if not video or not os.path.exists(video):
        return dict(name="Donma (ffmpeg)", status=SKIP, value="video yok", thr="0 olay", detail=[f"video bulunamadı: {video}"])
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", video, "-vf", "freezedetect=n=-55dB:d=1", "-an", "-f", "null", "-"], capture_output=True, text=True)
    starts = re.findall(r"freeze_start: ([0-9.]+)", r.stderr)
    durs = re.findall(r"freeze_duration: ([0-9.]+)", r.stderr)
    return dict(name="Donma (ffmpeg)", status=OK if not starts else FAIL, value=f"{len(starts)} olay", thr="0 olay (n=−55 dB, d=1 s)", detail=[f"t={s}s süre {d}s" for s, d in zip(starts, durs)])


# ───────────────────────────── çıktı ─────────────────────────────
def print_report(title, gates, rows=None, quiet=False):
    sym = {OK: "✓", FAIL: "✗", WARN: "⚠", SKIP: "·"}
    print(f"\n══ qa_flow — {title} ══")
    print(f"  {'KAPI':<28}{'SONUÇ':<8} {'ÖLÇÜLEN':<92}EŞİK")
    for g in gates:
        print(f"{sym[g['status']]} {g['name']:<28}{g['status']:<8} {g['value'][:90]:<92}{g['thr'][:80]}")
    if not quiet:
        for g in gates:
            if g["detail"] and g["status"] != OK:
                print(f"\n  [{g['name']}]")
                for d in g["detail"]:
                    if d:
                        print(f"    - {d}")
    if rows is not None and not quiet:
        print(f"\n{'#':>3} {'tür':<9}{'t0':>7}{'süre':>6}  {'cam':<36}{'kamera ailesi':<14}{'aile':<9}{'giriş geçişi':<16}{'link':<9}etiket")
        for r in rows:
            cam = (("auto " if r.get("cam_auto") else "") + (r["cam"] or "—"))[:34]
            tr = (f"{r['tr'][0]} {r['tr'][1]:.2f}" if r["tr"] else ("kesme" if r.get("cut_explicit") else "—"))
            print(f"{r['i']:>3} {r['kind']:<9}{r['t0']:>7.1f}{r['dur']:>6.1f}  {cam:<36}{str(r.get('camfam') or '—'):<14}{str(r.get('aile') or ''):<9}{tr:<16}{str(r['link'] or '—'):<9}{r['label']}")
    print(f"\nÖZET: {sum(1 for g in gates if g['status'] == OK)} GEÇTİ · {sum(1 for g in gates if g['status'] == FAIL)} KALDI · "
          f"{sum(1 for g in gates if g['status'] == WARN)} UYARI · {sum(1 for g in gates if g['status'] == SKIP)} PAS")


def run(prog, fast=False, workers=2, tau=None, spec=None, video=None, json_path=None, title="", quiet=False, verbose=True, eng_a=None):
    """prog: compose.Program. spec: işçilerin Program'ı yeniden kurması için dict(reel=True | part=…, chapters=…)."""
    tau = TAU if tau is None else tau
    if eng_a is None:
        eng_a = not fast
    t0 = time.time()
    st = static_analysis(prog)
    gates = list(st["gates"])
    samp = None
    motion_rows = None
    if not fast:
        if spec is None:
            raise ValueError("örnekleme için spec gerekli (işçiler Program'ı yeniden kurar)")
        ns, mads, chgs, ms = sample_series(spec, prog, workers, verbose)
        samp = analyze_series(prog, ns, mads, chgs, tau, bool(getattr(prog, "hud", False)))
        mg, motion_rows = motion_gate(prog, ns, mads)
        gates = samp["gates"][:1] + gates + samp["gates"][1:] + [mg]
    else:
        gates.append(dict(name="Durgunluk", status=SKIP, value="ölçülmedi (--fast)", thr=f"≤{STILL_MAX} sn", detail=["örnekleme analizi için --fast olmadan çalıştır"]))
        gates.append(dict(name="Olay yoğunluğu", status=SKIP, value="ölçülmedi (--fast)", thr="≥%95", detail=[]))
        gates.append(dict(name="Ölçülen hareket", status=SKIP, value="ölçülmedi (--fast)", thr=f">{MOT_LONG:.0f} sn çekimde medyan MAD ≥{MOT_TAU}", detail=[]))
    gates.append(freeze_check(video) if video else dict(name="Donma (ffmpeg)", status=SKIP, value="video verilmedi (--video yol.mp4)", thr="0 olay", detail=[]))
    if eng_a and (spec or {}).get("part") and not (spec or {}).get("chapters"):
        gates += eng_a_gates(spec["part"])
    print_report(title or "çekim listesi", gates, st["rows"], quiet)
    out = dict(title=title, tau=tau, still_max=STILL_MAX, step=STEP, elapsed=round(time.time() - t0, 1), gates=gates, shots=st["rows"],
               sampling=dict(runs=samp["runs"], intervals=samp["intervals"], motion=motion_rows) if samp else None, sub_zone=SUB_ZONE, calibration=CALIBRATION_NOTE)
    if json_path:
        os.makedirs(os.path.dirname(os.path.abspath(json_path)), exist_ok=True)
        json.dump(out, open(json_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"→ {json_path}")
    return out


# ───────────────────────────── kalibrasyon ─────────────────────────────
def calibrate(workers=2):
    """τ ölçümü: (1) hiç kamera/olay içermeyen sabit çekim (gürültü tabanı: toz + tane) (2) reel'in kararlı kısımlarında MAD dağılımı."""
    import cv2
    import numpy as np
    import compose
    import shots as SH
    print("kalibrasyon: sabit çekim (kamera hareketsiz, giriş animasyonları bitmiş) ölçülüyor …", flush=True)
    still = SH.shot("quote", 0.0, text="Hiçbir şey buradan çıkmayacak.", who="ANNA", at=0.0, mode="day", perde=2, cam=[(0.0, (0, 0, 1.0, 0)), (12.0, (0, 0, 1.0, 0))])
    prog = compose.Program(shots=[still], end=12.0)
    vals, prev = [], None
    for n in range(int(3.0 * FPS), int(11.0 * FPS), int(STEP * FPS)):
        g = cv2.cvtColor(cv2.resize(prog.frame(n, post=False), (240, 135), interpolation=cv2.INTER_AREA), cv2.COLOR_RGB2GRAY).astype(np.int16)
        if prev is not None:
            vals.append(float(np.abs(g - prev).mean()))
        prev = g
    print(f"  sabit çekim MAD: ort {np.mean(vals):.3f}  maks {max(vals):.3f}  (n={len(vals)})")
    print("kalibrasyon: reel örnekleniyor …", flush=True)
    spec = dict(reel=True)
    rp = make_program(spec)
    ns, mads, chgs, ms = sample_series(spec, rp, workers)
    steady = []
    for i, m in enumerate(mads):
        g0, g1 = ns[i] / FPS, ns[i + 1] / FPS
        a, b = rp.shot_at(g0), rp.shot_at(g1)
        if a != b or rp._trans_at(g0, a) or rp._trans_at(g1, b):
            continue
        steady.append(m)
    print(f"  reel kararlı aralıklar (n={len(steady)}): p5 {_pct(steady, 0.05):.2f}  p10 {_pct(steady, 0.10):.2f}  p25 {_pct(steady, 0.25):.2f}  medyan {_pct(steady, 0.5):.2f}  p90 {_pct(steady, 0.9):.2f}")
    cand = math.sqrt(max(max(vals), 0.02) * max(_pct(steady, 0.10), 0.1))
    print(f"  öneri: τ ≈ √(sabit_maks × reel_p10) = {cand:.2f}   (kodda TAU={TAU})")
    return dict(still_mean=float(np.mean(vals)), still_max=max(vals), steady_p10=_pct(steady, 0.10), steady_p50=_pct(steady, 0.5), tau_suggest=cand)


def main(argv=None):
    ap = argparse.ArgumentParser(description="MEDICI yönetmenlik kapıları (qa_flow)")
    ap.add_argument("--reel", action="store_true")
    ap.add_argument("--part", type=int, choices=tuple(range(1, 8)))
    ap.add_argument("--chapters", default=None)
    ap.add_argument("--fast", action="store_true")
    ap.add_argument("--workers", type=int, default=2)
    ap.add_argument("--tau", type=float, default=None)
    ap.add_argument("--video", default=None)
    ap.add_argument("--json", default=os.path.join("out", "qa_flow.json"))
    ap.add_argument("--quiet", action="store_true")
    ap.add_argument("--calibrate", action="store_true")
    ap.add_argument("--no-eng-a", action="store_true", help="ENG-A denetimlerini (qa_yerlesim/qa_donem) çalıştırma")
    ap.add_argument("--eng-a", action="store_true", help="--fast'ta da ENG-A denetimlerini çalıştır")
    a = ap.parse_args(argv)
    if a.calibrate:
        calibrate(a.workers)
        return 0
    if a.reel:
        spec, title = dict(reel=True), "reel (preview_reel)"
    else:
        chs = a.chapters.split(",") if a.chapters else None
        spec = dict(part=a.part, chapters=chs)
        title = f"Parça {a.part}" if a.part else (f"bölümler {a.chapters}" if a.chapters else "tüm film")
    prog = make_program(spec)
    eng = False if a.no_eng_a else (True if a.eng_a else None)
    out = run(prog, fast=a.fast, workers=min(max(a.workers, 1), 4), tau=a.tau, spec=spec, video=a.video, json_path=a.json, title=title, quiet=a.quiet, eng_a=eng)
    return 1 if any(g["status"] == FAIL for g in out["gates"]) else 0


if __name__ == "__main__":
    sys.exit(main())
