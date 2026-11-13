#!/usr/bin/env python3
"""Bölüm önizleme / denetim aracı (sahne yazarları için).

  python3 preview_chapter.py c3 --script          # bölümün cümleleri: kimlik, zaman, metin (çapa seçmek için)
  python3 preview_chapter.py c3 --check           # çekim listesi, uyarılar, kare başına ms ölçümü
  python3 preview_chapter.py c3                   # kontak sayfaları → out/frames/c3_sheet_N.png (çekim başına 2 kare)
  python3 preview_chapter.py c3 --shots 2,3 -k 4  # yalnız 2. ve 3. çekim, çekim başına 4 kare
  python3 preview_chapter.py c3 --at 283.4,290    # verilen GLOBAL saniyelerde tam çözünürlüklü kareler → out/frames/c3_t283.4.png
  python3 preview_chapter.py c3 --clip 280 6      # global 280. sn'den 6 sn'lik kısa mp4 (sessiz) → out/frames/c3_clip.mp4

Not: bölüm kartı ve (c1 için) ana başlık çekimleri Program tarafından otomatik eklenir; sahne dosyası yalnız bölümün KENDİ çekimlerini içerir.
"""
import argparse
import os
import subprocess
import sys
import time

import cv2
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.chdir(HERE)

import compose  # noqa: E402
import preview  # noqa: E402
import shots as SH  # noqa: E402
from sk import FPS  # noqa: E402


def mmss(t):
    return f"{int(t // 60)}:{t % 60:04.1f}"


def print_script(cid):
    tl = SH.timeline()
    c = tl.chapters[cid]
    print(f"{cid}  global {c['t0']:.2f} – {c['t1']:.2f} sn  ({c['t1'] - c['t0']:.1f} sn)")
    for sid in tl.order:
        s = tl.sent[sid]
        if s["ch"] != cid:
            continue
        print(f"\n{sid:8s} {s['t0']:8.2f}–{s['t1']:8.2f}  (bölüm içi {s['t0'] - c['t0']:6.2f})")
        print(f"   {s['disp']}")


def build(cid):
    try:
        return compose.Program(chapters=[cid])
    except KeyError as e:
        print(f"\n✗ ÇAPA HATASI: {e}\n  → `--script` ile cümle kimliklerini ve sözcükleri kontrol et. Sözcük araması aksan/harf büyüklüğüne duyarsız, alt dize eşleşir; "
              f"aynı sözcük birden çok geçiyorsa (sid, 'sözcük', nth, ofset) biçimini kullan.")
        sys.exit(2)
    except AssertionError as e:
        print(f"\n✗ ÇEKİM SÜRESİ HATASI: {e}\n  → bir çekimin çapası bir sonrakinden SONRA; çapa sırasını düzelt.")
        sys.exit(2)


def check(prog, cid):
    c = prog.tl.chapters[cid]
    print(f"\n{cid}: global {c['t0']:.1f}–{c['t1']:.1f} sn · {len(prog.shots)} çekim (bölüm kartı dahil)")
    print(f"{'#':>3} {'tür':<12} {'başlangıç':>9} {'süre':>6}  etiket")
    warns = []
    prev_kind, run = None, 0
    for i, s in enumerate(prog.shots):
        print(f"{i:3d} {s.kind:<12} {mmss(s.t0 - c['t0'] + 0):>9} {s.dur:6.1f}  {s.label}")
        if s.kind in ("chapter_card", "title", "outro", "black"):
            prev_kind, run = s.kind, 1
            continue
        if s.dur < 1.2:
            warns.append(f"#{i} {s.kind} '{s.label}': {s.dur:.2f} sn — çok kısa (geçişle yutulur)")
        if s.dur > 16.0:
            warns.append(f"#{i} {s.kind} '{s.label}': {s.dur:.1f} sn — çok uzun; araya ek çekim/kamera hareketi/yeniden çerçeveleme koy")
        if not s.label:
            warns.append(f"#{i} {s.kind}: etiket (label=) yok")
        if s.kind == prev_kind:
            run += 1
            if run >= 4:
                warns.append(f"#{i}: üst üste {run} kez '{s.kind}' — görsel çeşitlilik düşük")
        else:
            prev_kind, run = s.kind, 1
    # ms/kare ölçümü
    print("\nkare başına süre (önbellek ısındıktan sonra, post dahil):")
    tot = 0.0
    for i, s in enumerate(prog.shots):
        nfr = int(s.dur * FPS)
        if nfr < 4:
            continue
        pts = [int(s.t0 * FPS) + 1 + int((nfr - 3) * q) for q in (0.15, 0.5, 0.85)]
        for n in pts:
            prog.frame(n)
        t = time.process_time()                      # CPU süresi: makine yükü (başka işlemler) sahte uyarı üretmesin
        for n in pts:
            prog.frame(n + 1)
        ms = (time.process_time() - t) / len(pts) * 1000
        tot += ms * nfr
        flag = "  ← YAVAŞ (>450 ms): dyn() içinde bulanıklık/degrade/ışık huzmesi çiziyor olabilirsin; statik katmana pişir" if ms > 450 else ""
        print(f"  #{i:2d} {s.kind:<12} {ms:6.0f} ms{flag}")
        if ms > 450:
            warns.append(f"#{i} {s.kind} '{s.label}': {ms:.0f} ms/kare")
    nf = int((c['t1'] - c['t0']) * FPS)
    print(f"\nbölüm ortalaması ≈ {tot / max(1, nf):.0f} ms/kare, tahmini render ≈ {tot / 1000 / 60:.1f} dk (tek çekirdek)")
    if warns:
        print("\nUYARILAR:")
        for w in warns:
            print("  ⚠", w)
    else:
        print("\nuyarı yok ✓")


def label_img(img, text):
    im = img.copy()
    cv2.rectangle(im, (0, 0), (im.shape[1], 46), (0, 0, 0), -1)
    cv2.putText(im, text, (12, 33), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (240, 215, 140), 2, cv2.LINE_AA)
    return im


def contact(prog, cid, which, per, cols, scale):
    imgs, labs = [], []
    for i, s in enumerate(prog.shots):
        if which is not None and i not in which:
            continue
        if per == 1 or s.dur < 2.5:
            qs = [0.55]
        else:
            qs = [0.12 + 0.76 * k / (per - 1) for k in range(per)]
        for q in qs:
            t = s.t0 + q * s.dur
            imgs.append(label_img(prog.frame(int(t * FPS)), f"#{i} {s.kind} {s.label}  g={t:.1f}s"))
    if not imgs:
        print("kare yok")
        return
    per_sheet = cols * 5
    paths = []
    for k in range(0, len(imgs), per_sheet):
        p = os.path.join("out", "frames", f"{cid}_sheet_{k // per_sheet + 1}.png")
        os.makedirs(os.path.dirname(p), exist_ok=True)
        preview.sheet(imgs[k:k + per_sheet], cols=cols, scale=scale, path=p)
        paths.append(p)
    print("kontak sayfaları:\n  " + "\n  ".join(paths))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cid")
    ap.add_argument("--script", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--shots", default=None, help="çekim indeksleri, virgülle")
    ap.add_argument("-k", type=int, default=2, help="çekim başına kare")
    ap.add_argument("--cols", type=int, default=3)
    ap.add_argument("--scale", type=float, default=0.5)
    ap.add_argument("--at", default=None, help="global saniyeler, virgülle (tam çözünürlük PNG)")
    ap.add_argument("--clip", nargs=2, type=float, default=None, metavar=("T0", "SURE"))
    a = ap.parse_args()
    if a.script:
        print_script(a.cid)
        return
    prog = build(a.cid)
    if a.check:
        check(prog, a.cid)
        return
    if a.at:
        os.makedirs("out/frames", exist_ok=True)
        for t in [float(x) for x in a.at.split(",")]:
            img = prog.frame(int(t * FPS))
            p = f"out/frames/{a.cid}_t{t:g}.png"
            cv2.imwrite(p, cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
            print(p)
        return
    if a.clip:
        t0, dur = a.clip
        n0, n = int(t0 * FPS), int(dur * FPS)
        p = f"out/frames/{a.cid}_clip.mp4"
        os.makedirs("out/frames", exist_ok=True)
        ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "1920x1080", "-r", str(FPS), "-i", "-",
                               "-vf", "scale=1280:720", "-c:v", "libx264", "-crf", "24", "-preset", "veryfast", "-pix_fmt", "yuv420p", p], stdin=subprocess.PIPE)
        for k in range(n):
            ff.stdin.write(np.ascontiguousarray(prog.frame(n0 + k)).tobytes())
        ff.stdin.close(); ff.wait()
        print(p)
        return
    which = None if a.shots is None else {int(x) for x in a.shots.split(",")}
    contact(prog, a.cid, which, a.k, a.cols, a.scale)


if __name__ == "__main__":
    main()
