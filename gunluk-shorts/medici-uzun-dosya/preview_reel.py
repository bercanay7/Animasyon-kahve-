#!/usr/bin/env python3
"""Reel (kanıt filmi): yönetmenlik motorunun sessiz testi — ~59 sn, 1920×1080, 24 fps.

Mevcut çekim türlerini (coin, skyline, frieze, map, ledger, letter, palle, quote, tree, timeline, network, counter, medal, title) birbirine
akıtır; her yeni geçişi (iris, slide, zoomthru, carry, light, candle) ve her kamera ön ayarını (push, pull, pan r/l, crane up/down, orbit,
hand, hand2, rack, track, anahtar kareli) en az bir kez kullanır. Geçişler gerekçelidir (link=): para→güneş/iris, skyline→slide→frieze,
harita→zoomthru→defter, defter→sayfa→mektup, palle→carry→alıntı, alıntı→mum→gece …

  python3 preview_reel.py                  # video (out/reel_yonetmen.mp4) + kontak sayfaları (out/frames/reel_sheet*.png)
  python3 preview_reel.py --sheet          # yalnız kontak sayfaları (hızlı)
  python3 preview_reel.py --video          # yalnız video
  python3 preview_reel.py --range 8 20     # kısa bölüm (sn) → out/reel_part.mp4 (hata ayıklama)
  python3 preview_reel.py --qa             # + qa_flow (durgunluk, gerekçeli geçiş, çekim uzunluğu …)
Seçenekler: --workers 2 (≤2 önerilir; paylaşımlı CPU), --crf 18.
"""
import argparse
import math
import multiprocessing as mp
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.chdir(HERE)

W, H, FPS = 1920, 1080, 24
OUT = os.path.join(HERE, "out")
MP4 = os.path.join(OUT, "reel_yonetmen.mp4")
FR = os.path.join(OUT, "frames")


# ───────────────────────────── çekim listesi ─────────────────────────────
def build_shots():
    """Reel çekimleri: a = mutlak saniye (çapa yok). Gerekçe `link=`, giriş geçişi `tr=(ad, süre, opts)`.
    Yerel saat notu: geçişli (lead'li) girişte çekimin yerel saati kesme anından `lead` sn ÖNCE başlar → içerik zamanları `c = lead` ile kesmeye göre verilir (c + 0.4 = kesmeden 0,4 sn sonra)."""
    import cilt_fx as FX
    import shots as SH
    shot = SH.shot

    def LD(tr):
        return FX.lead_for(*FX.norm_tr(tr))

    # --- iris, slide ... geçişleri (gelen çekimden önce tanımlanır ki içerik zamanları kesmeye göre yazılabilsin)
    T2 = ("iris", 0.9, dict(at=(960, 508), obj="florin", r=252))
    T3 = ("slide", 0.9, dict(dir="r"))
    T4 = ("giornata", 0.9, dict(lead=True))
    T5 = ("zoomthru", 1.0, dict(at=(890, 510)))
    T6 = ("sayfa", 0.9, dict(lead=True))
    T7 = ("light", 0.9, dict(at=(W / 2, H * 0.60)))
    T8 = ("carry", 0.95, dict(dir="r", strip="banner"))
    T9 = ("candle", 1.0, dict(at=(1730, 600)))
    T10 = ("yikama", 0.9, dict(lead=True))
    T11 = ("whip", 0.6)
    T12 = ("carry", 0.9, dict(dir="l", strip="ink"))
    T13 = ("slide", 0.9, dict(dir="l"))
    T14 = ("candle", 1.0, dict(at=(1730, 560)))
    c4, c5, c6, c10 = LD(T4), LD(T5), LD(T6), LD(T10)
    c2, c7, c9, c12, c13, c14 = LD(T2), LD(T7), LD(T9), LD(T12), LD(T13), LD(T14)
    LED_L = [dict(text="Per lana di Francia", amt=(412, 6, 8), at=c5 + 0.4), dict(text="Per seta di Lucca", amt=(180, 0, 0), at=c5 + 1.3),
             dict(text="A messer Cosimo", amt=(1500, 0, 0), at=c5 + 2.2, hl=c5 + 3.4), dict(text="Per cambio di Bruggia", amt=(96, 3, 4), at=c5 + 3.1)]
    LED_R = [dict(text="Da Giovanni di Bicci", amt=(1500, 0, 0), at=c5 + 0.9), dict(text="Da Vieri di Cambio", amt=(640, 2, 0), at=c5 + 1.8)]
    MAP = dict(view=(11.25, 43.77, 2.3),
               regions=[dict(name="floransa", color="floransa", at=c4 + 0.2, alpha=0.62), dict(name="papalik", color="papalik", at=c4 + 0.5, alpha=0.5),
                        dict(name="venedik", color="azurite", at=c4 + 0.8, alpha=0.5), dict(name="milano", color="terra", at=c4 + 1.1, alpha=0.5)],
               cities=[dict(lon=11.25, lat=43.77, name="FLORANSA", kind="capital", at=c4 + 0.4, side="b", size=36), dict(lon=12.5, lat=41.9, name="Roma", at=c4 + 1.0, size=32),
                       dict(lon=12.33, lat=45.44, name="Venedik", at=c4 + 1.3, size=32, side="r"), dict(lon=9.19, lat=45.46, name="Milano", at=c4 + 1.6, size=32, side="t")],
               routes=[dict(pts=[(11.25, 43.77), (12.33, 45.44)], at=c4 + 1.8, dur=1.5, width=6)], date=("1434", c4 + 0.3), approx=False)
    TREE = dict(title="BİR HANEDANIN ÜÇ KUŞAĞI", size=210, nodes=[
        dict(id="g", key="m_giovanni", name="GIOVANNI", dates="1360 – 1429", x=0.5, y=0.26, at=0.2), dict(id="c", key="m_cosimo", name="COSIMO", dates="1389 – 1464", x=0.34, y=0.60, at=0.5),
        dict(id="l", key="m_lorenzo", name="LORENZO", dates="1449 – 1492", x=0.66, y=0.60, at=0.8)], edges=[("g", "c", 0.7), ("g", "l", 1.0)])
    TL = dict(a0=1390, a1=1500, step=10, title="PARA — İTİBAR — İKTİDAR",
              events=[(1397, "Orsanmichele köşesi", c10 + 0.1), (1429, "Giovanni ölür", c10 + 0.6), (1434, "Cosimo döner", c10 + 1.1), (1464, "Cosimo ölür", c10 + 1.6),
                      (1478, "Pazzi", c10 + 2.1), (1494, "Sürgün", c10 + 2.6)], hl=(1434, 1464, "30 YIL", c10 + 1.8))
    NET = dict(title="PAZZİ: EVLİLİK, ORTAKLIK, REKABET", nodes=[
        dict(id="m", name="MEDICI", key="m_cosimo", x=0.50, y=0.42, size=190, at=0.2), dict(id="b", name="BARDI", initials="B", x=0.22, y=0.30, at=0.5, color="lapis"),
        dict(id="t", name="TORNABUONI", initials="T", x=0.27, y=0.62, at=0.7, color="terra"), dict(id="o", name="ORSINI", initials="O", x=0.78, y=0.30, at=0.9, color="madder"),
        dict(id="p", name="PAZZI", initials="P", x=0.76, y=0.62, at=1.1, color="umber"), dict(id="s", name="SFORZA", initials="S", x=0.50, y=0.78, at=1.3, color="azurite")],
        edges=[("m", "b", "evlilik", 0.8), ("m", "t", "evlilik", 1.0), ("m", "o", "evlilik", 1.2), ("m", "p", "rakip", 1.4), ("m", "s", "ittifak", 1.6), ("b", "t", "ortaklik", 1.8)])
    L = [
        shot("coin", 0.0, kick="1252", sub="Florin", at=0.2, n=1, mode="day", perde=1, cam=("push", 0.09), label="florin", link=None),
        shot("skyline", 4.6, tr=T2, link="shape", seed=1, pan=170, kick="FLORANSA, 1434", labels=[dict(on="duomo", at=c2 + 0.9), dict(on="pv", at=c2 + 1.6)], perde=1,
             cam=("crane", "up", 130), label="Floransa şafakta"),
        shot("frieze", 9.6, tr=T3, link="dir", seed=3, speed=40.0, kick="MAGİ ALAYI TARZI", perde=1, cam="hand", label="alay"),
        shot("map", 14.0, tr=T4, link="material", perde=1, label="harita: Floransa", **MAP,
             cam=[(0.0, (0, 0, 1.0, 0)), (c4 + 2.2, (40, 18, 1.25, 0)), (c4 + 5.0, (70, 30, 1.5, 0))]),
        shot("ledger", 19.0, tr=T5, link="scale", left=LED_L, right=LED_R, head="MCCCXCVII", focus=(900, 420), perde=1, cam=("push", 0.09), label="defter satırı"),
        shot("letter", 23.6, tr=T6, link="material", addr=("Al Magnifico Signore", "Lorenzo de' Medici", "in Firenze"), seal_at=0.2, open_at=c6 + 0.4,
             lines=[("Magnifico et honorando padre,", c6 + 1.1), ("ho ricevuto la vostra lettera", c6 + 1.8), ("et subito ho dato ordine.", c6 + 2.5)], sig=("Il vostro Piero", c6 + 3.1),
             date="a dì 12 d'aprile", perde=1, cam=("crane", "down", 130), label="mektup"),
        shot("palle", 27.8, tr=T7, link="light", kick="ALTI TOP", at=0.3, perde=2, cam=("orbit", 10), label="arma (orbit)"),
        shot("quote", 31.8, tr=T8, link="carry", text="Hiçbir şey buradan çıkmayacak.", who="ANNA MARIA LUISA", src="Aile Antlaşması, 1737", at=0.2, perde=2, cam="pull", label="alıntı"),
        shot("tree", 35.4, tr=T9, link="light", mode="night", perde=2, cam=("track", "sweep_r"), label="soy ağacı (gece)", **TREE),
        shot("timeline", 39.4, tr=T10, link="material", mode="day", perde=2, cam=("pan", "r", 150), label="zaman çizgisi", **TL),
        shot("network", 43.2, tr=T11, link="dir", mode="night", perde=2, cam="hand2", label="Pazzi ağı", **NET),
        shot("counter", 47.2, tr=T12, link="carry", value=1500, unit="florin", label="Piccarda'nın çeyizi", coin=True, at=1.0, mode="day", perde=2, cam=("pan", "l", 160)),
        shot("medal", 51.0, tr=T13, link="dir", key="m_cosimo", name="COSIMO DE' MEDICI", role="şehrin sessiz efendisi", dates="1389 – 1464", at=0.2, plate_at=c13 + 0.3,
             mode="day", perde=2, cam=("rack", (960, 470), (960, 925), dict(at=c13 + 0.6, dur=1.4, r=340, sigma=6.0)), label="Cosimo (rack: madalya → levha)"),
        shot("title", 55.0, tr=T14, link="light", text="MEDİCİ", sub="ZAMAN KURYESİ", kick="FLORANSA", at=1.1, mode="night", perde=3, cam=("push", 0.07), label="kapanış"),
    ]
    return L


REEL_END = 59.0


def build_program():
    import compose
    return compose.Program(shots=build_shots(), end=REEL_END)


# ───────────────────────────── video ─────────────────────────────
def _ff(out, crf, threads=1):
    return ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", str(crf), "-pix_fmt", "yuv420p", "-color_primaries", "bt709", "-color_trc", "bt709",
            "-colorspace", "bt709", "-threads", str(threads), "-an", out]


def render_chunk(args):
    n0, n1, path, crf = args
    import cv2
    import numpy as np
    cv2.setNumThreads(1)
    prog = build_program()
    ff = subprocess.Popen(_ff(path, crf), stdin=subprocess.PIPE)
    t0 = time.time()
    errs = []
    last = None
    for n in range(n0, n1):
        try:
            img = prog.frame(n)
            last = img
        except Exception as e:                      # kare hatası: önceki kareyi tekrarla ve raporla
            errs.append((n, f"{type(e).__name__}: {e}"))
            img = last if last is not None else np.zeros((H, W, 3), np.uint8)
        ff.stdin.write(np.ascontiguousarray(img).tobytes())
    ff.stdin.close()
    rc = ff.wait()
    return n0, n1, time.time() - t0, errs, rc


def render_video(workers=2, crf=18, rng=None, out=None):
    prog = build_program()
    n_all = int(math.ceil(prog.total * FPS))
    n0, n1 = (0, n_all) if rng is None else (int(rng[0] * FPS), min(n_all, int(rng[1] * FPS)))
    out = out or (MP4 if rng is None else os.path.join(OUT, "reel_part.mp4"))
    os.makedirs(OUT, exist_ok=True)
    nchunk = max(workers * 2, 2)
    size = int(math.ceil((n1 - n0) / nchunk))
    chunks = []
    for i in range(nchunk):
        a, b = n0 + i * size, min(n1, n0 + (i + 1) * size)
        if b > a:
            chunks.append((a, b, os.path.join(OUT, f"_reel_seg{i}.mp4"), crf))
    print(f"reel: {prog.total:.1f} sn, {n1 - n0} kare, {len(chunks)} parça, {workers} işlem", flush=True)
    t0 = time.time()
    ctx = mp.get_context("spawn")
    errs = []
    with ctx.Pool(workers) as pool:
        for a, b, dt, e, rc in pool.imap(render_chunk, chunks):
            errs += e
            print(f"  kare {a}–{b}: {dt:.0f} sn ({dt / max(1, b - a) * 1000:.0f} ms/kare){' HATA ' + str(len(e)) if e else ''}{' ffmpeg rc=' + str(rc) if rc else ''}", flush=True)
    lst = os.path.join(OUT, "_reel_concat.txt")
    open(lst, "w").write("".join(f"file '{c[2]}'\n" for c in chunks))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", "-movflags", "+faststart", out], check=True)
    for p_ in [c[2] for c in chunks] + [lst]:
        try:
            os.remove(p_)
        except OSError:
            pass
    print(f"{out}  ({(time.time() - t0):.0f} sn)", flush=True)
    for n, m in errs[:10]:
        print(f"  KARE HATASI {n}: {m}")
    return out, errs


# ───────────────────────────── kontak sayfaları ─────────────────────────────
NEW_TR_NAMES = ("iris", "slide", "zoomthru", "carry", "light", "candle")


def _label(img, text, h=34):
    import cv2
    import numpy as np
    strip = np.zeros((h, img.shape[1], 3), np.uint8)
    cv2.putText(strip, text, (8, h - 9), cv2.FONT_HERSHEY_SIMPLEX, 0.62 if img.shape[1] > 700 else 0.5, (240, 215, 140), 1, cv2.LINE_AA)
    return np.vstack([strip, img])


def _grid(tiles, cols, tw):
    import cv2
    import numpy as np
    th = int(tw * 9 / 16) + 34
    rows = (len(tiles) + cols - 1) // cols
    S = np.zeros((rows * th, cols * tw, 3), np.uint8)
    for i, t in enumerate(tiles):
        r, c = divmod(i, cols)
        S[r * th:(r + 1) * th, c * tw:(c + 1) * tw] = cv2.resize(t, (tw, th), interpolation=cv2.INTER_AREA)
    return S


def make_sheets(prog=None):
    """Geçiş sayfası (her yeni geçiş için 4 kare) + kamera sayfası (her ön ayar için 3 kare) + birleşik reel_sheet.png."""
    import cv2
    import numpy as np
    prog = prog or build_program()
    os.makedirs(FR, exist_ok=True)

    def grab(g, text):
        n = int(round((g - prog.t_off) * FPS))
        return _label(prog.frame(n), text)

    tr_tiles, seen = [], set()
    for s in prog.shots:
        if not s.tr_eff or s.tr_eff[0] not in NEW_TR_NAMES:
            continue
        name, d, o = s.tr_eff
        sty = o.get("strip") or o.get("obj") or o.get("dir") or ""
        key = (name, o.get("strip"))
        if key in seen:
            continue
        seen.add(key)
        for k in (0.15, 0.40, 0.65, 0.90):
            tr_tiles.append(grab(s.t0 - d + d * k, f"{name} {sty} k={k:.2f}  ({prog.shots[s.i - 1].kind}->{s.kind})"))
    cam_tiles = []
    seen = set()
    for s in prog.shots:
        if s.cam is None:
            continue
        spec = s.cam
        nm = spec if isinstance(spec, str) else (spec[0] if isinstance(spec[0], str) else "keys")
        if isinstance(spec, tuple) and spec[0] in ("pan", "crane"):
            nm = f"{spec[0]} {spec[1]}"
        if nm in seen:
            continue
        seen.add(nm)
        lo = s.t0 + (s.tr_eff[1] if (s.tr_eff and s.tr_eff[2].get("place") != "after") else 0.0) + 0.25
        nxt = prog.shots[s.i + 1] if s.i + 1 < len(prog.shots) else None
        hi = s.t1 - ((nxt.tr_eff[1] if (nxt and nxt.tr_eff) else 0.0)) - 0.15
        for q in (0.05, 0.5, 0.95):
            cam_tiles.append(grab(lo + (hi - lo) * q, f"{nm} [{s.kind}] {q:.2f}"))
    p_tr = os.path.join(FR, "reel_sheet_tr.png")
    p_cam = os.path.join(FR, "reel_sheet_cam.png")
    S1 = _grid(tr_tiles, 4, 480)
    S2 = _grid(cam_tiles, 3, 576)
    cv2.imwrite(p_tr, cv2.cvtColor(S1, cv2.COLOR_RGB2BGR))
    cv2.imwrite(p_cam, cv2.cvtColor(S2, cv2.COLOR_RGB2BGR))
    # birleşik (geçişler üstte; kamera kareleri küçük)
    S3 = _grid(cam_tiles, 6, 320)
    wmax = max(S1.shape[1], S3.shape[1])
    pad = lambda a: np.pad(a, ((0, 0), (0, wmax - a.shape[1]), (0, 0)))
    comb = np.vstack([pad(S1), pad(S3)])
    cv2.imwrite(os.path.join(FR, "reel_sheet.png"), cv2.cvtColor(comb, cv2.COLOR_RGB2BGR))
    print(os.path.join(FR, "reel_sheet.png"), "|", p_tr, "|", p_cam)
    return p_tr, p_cam


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sheet", action="store_true")
    ap.add_argument("--video", action="store_true")
    ap.add_argument("--range", nargs=2, type=float)
    ap.add_argument("--workers", type=int, default=2)
    ap.add_argument("--crf", type=int, default=18)
    ap.add_argument("--qa", action="store_true")
    a = ap.parse_args()
    if a.range:
        render_video(a.workers, a.crf, a.range)
        return
    do_video = a.video or not a.sheet
    do_sheet = a.sheet or not a.video
    if do_video:
        render_video(a.workers, a.crf)
    if do_sheet:
        make_sheets()
    if a.qa:
        import qa_flow
        args = ["--reel", "--workers", str(a.workers)]
        if os.path.exists(MP4):
            args += ["--video", MP4]
        qa_flow.main(args)


if __name__ == "__main__":
    main()
