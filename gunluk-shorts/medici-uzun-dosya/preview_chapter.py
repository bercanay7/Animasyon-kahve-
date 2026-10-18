#!/usr/bin/env python3
"""Bölüm önizleme / denetim aracı (sahne yazarları için) — MEDICI: parça duyarlı (c7 → Parça 2 zaman çizelgesi; `out` bağlantısına GEREK YOK).

  python3 preview_chapter.py c7 --script          # bölümün cümleleri: kimlik, bölüm içi zaman, kaynak sınıfı, metin (çapa seçmek için)
  python3 preview_chapter.py c7 --words c7s17     # cümlenin sözcükleri ve zamanları (sözcük çapası için)
  python3 preview_chapter.py c7 --check           # çekim listesi, uyarılar, kare başına ms ölçümü
  python3 preview_chapter.py c7                   # kontak sayfaları → out_pN/frames/c7_sheet_N.png (çekim başına 2 kare)
  python3 preview_chapter.py c7 --shots 2,3 -k 4  # yalnız 2. ve 3. çekim, çekim başına 4 kare
  python3 preview_chapter.py c7 --at 83.4,90      # PARÇA-İÇİ saniyelerde (prog.frame zamanı) tam çözünürlüklü kareler → out_pN/frames/c7_t83.4.png
  python3 preview_chapter.py c7 --clip 80 6       # parça-içi 80. sn'den 6 sn'lik küçük mp4 (sessiz) → out_pN/frames/c7_clip.mp4
  python3 preview_chapter.py c7 --flow            # yönetmenlik kapıları (qa_flow --part N --chapters c7 --fast): kamera/geçiş/link/çapa/olay yoğunluğu

Zamanlar: `--script`/`--check` çıktısındaki "bölüm içi" süre bölüm başından; `--at/--clip` ise PARÇA-İÇİ saniyedir (parçanın ilk karesi 0). Bölüm başlangıcı çıktıda yazar.
Ses GEÇİCİ (Piper) olabilir: zamanlar gerçek sesle DEĞİŞİR → çapaları cümle/sözcük kimliğine bağla, mutlak saniyeye değil.
Not: bölüm kartı ve (P1'de c1 öncesi) ana başlık çekimleri Program tarafından otomatik eklenir; sahne dosyası yalnız bölümün KENDİ çekimlerini içerir.
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
import script as S  # noqa: E402
import shots as SH  # noqa: E402
from sk import FPS  # noqa: E402


def mmss(t):
    return f"{int(t // 60)}:{t % 60:04.1f}"


def part_of(cid):
    if cid not in S.PART_OF:
        sys.exit(f"bilinmeyen bölüm: {cid} (c0…c16)")
    return S.PART_OF[cid]


def outdir(cid):
    d = os.path.join(HERE, f"out_p{part_of(cid)}", "frames")
    os.makedirs(d, exist_ok=True)
    return d


def tags_of(cid):
    ch = next(c for c in S.CHAPTERS if c["id"] == cid)
    out, k = {}, 0
    for para in ch["paras"]:
        for tup in para:
            k += 1
            out[f"{cid}s{k}"] = tup[2] if len(tup) > 2 else ""
    return out


def print_script(cid):
    p = part_of(cid)
    compose._use_part_timeline(p)
    tl = SH.timeline()
    c = tl.chapters[cid]
    tg = tags_of(cid)
    scratch = os.path.exists(os.path.join(HERE, f"out_p{p}", "GECICI_SES.json"))
    print(f"{cid}  Parça {p}  parça-içi {c['t0']:.2f} – {c['t1']:.2f} sn  ({c['t1'] - c['t0']:.1f} sn)  ses: {'GEÇİCİ (Piper)' if scratch else 'gerçek'}")
    for sid in tl.order:
        s = tl.sent[sid]
        if s["ch"] != cid:
            continue
        print(f"\n{sid:8s} {s['t0']:8.2f}–{s['t1']:8.2f}  (bölüm içi {s['t0'] - c['t0']:6.2f})   [{tg.get(sid, '')[:70]}]")
        print(f"   {s['disp']}")


def print_words(cid, sid):
    p = part_of(cid)
    compose._use_part_timeline(p)
    tl = SH.timeline()
    c = tl.chapters[cid]
    s = tl.sent[sid]
    print(f"{sid}  {s['t0']:.2f}–{s['t1']:.2f}  {s['disp']}")
    for w in s["words"]:
        print(f"   {w['t0']:8.2f}–{w['t1']:8.2f}  (bölüm içi {w['t0'] - c['t0']:6.2f})  {w['w']}")


def build(cid):
    try:
        return compose.Program(chapters=[cid], part=part_of(cid))
    except KeyError as e:
        print(f"\n✗ ÇAPA HATASI: {e}\n  → `--script` ile cümle kimliklerini, `--words cKsN` ile sözcükleri kontrol et. Sözcük araması aksan/harf büyüklüğüne duyarsız, alt dize eşleşir; "
              f"aynı sözcük birden çok geçiyorsa (sid, 'sözcük', nth, ofset) biçimini kullan.")
        sys.exit(2)
    except AssertionError as e:
        print(f"\n✗ ÇEKİM SÜRESİ HATASI: {e}\n  → bir çekimin çapası bir sonrakinden SONRA; çapa sırasını düzelt.")
        sys.exit(2)
    except ValueError as e:
        print(f"\n✗ GEÇERSİZ ÇEKİM PARAMETRESİ: {e}\n  → cam=/tr=/link= değerlerini notlar_yonetmen_motoru.md ile karşılaştır.")
        sys.exit(2)


def check(prog, cid):
    c = prog.tl.chapters[cid]
    print(f"\n{cid}: parça-içi {c['t0']:.1f}–{c['t1']:.1f} sn · {len(prog.shots)} çekim (bölüm kartı/bindirme dahil)")
    print(f"{'#':>3} {'tür':<12} {'başlangıç':>9} {'süre':>6}  {'cam':<22} {'geçiş':<12} etiket")
    warns = []
    prev_kind, run = None, 0
    for i, s in enumerate(prog.shots):
        cam = str(getattr(s, "cam", None) or "—")[:21]
        tr = str((getattr(s, "tr_eff", None) or (None,))[0] or "—")[:11]
        print(f"{i:3d} {s.kind:<12} {mmss(s.t0 - c['t0'] + 0):>9} {s.dur:6.1f}  {cam:<22} {tr:<12} {s.label}")
        if s.kind in ("chapter_card", "fresco_title", "outro", "black"):
            prev_kind, run = s.kind, 1
            continue
        if s.dur < 1.2:
            warns.append(f"#{i} {s.kind} '{s.label}': {s.dur:.2f} sn — çok kısa (geçişle yutulur)")
        if s.dur > 16.0 and not getattr(s, "longtake", False):
            warns.append(f"#{i} {s.kind} '{s.label}': {s.dur:.1f} sn — çok uzun; araya ek çekim/kamera hareketi/yeniden çerçeveleme koy (ya da longtake=True + gerekçe)")
        if not s.label:
            warns.append(f"#{i} {s.kind}: etiket (label=) yok")
        if getattr(s, "cam", None) is None and s.kind not in ("pano", "build"):
            warns.append(f"#{i} {s.kind} '{s.label}': cam= yok (qa_flow 'örtük' sayar; her çekimde açıkça yaz)")
        if s.kind == prev_kind:
            run += 1
            if run >= 3:
                warns.append(f"#{i}: üst üste {run} kez '{s.kind}' — görsel çeşitlilik düşük (kapı: ≤2)")
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
            imgs.append(label_img(prog.frame(int(t * FPS)), f"#{i} {s.kind} {s.label}  p={t:.1f}s"))
    if not imgs:
        print("kare yok")
        return
    per_sheet = cols * 5
    paths = []
    for k in range(0, len(imgs), per_sheet):
        p = os.path.join(outdir(cid), f"{cid}_sheet_{k // per_sheet + 1}.png")
        preview.sheet(imgs[k:k + per_sheet], cols=cols, scale=scale, path=p)
        paths.append(p)
    print("kontak sayfaları:\n  " + "\n  ".join(paths))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cid")
    ap.add_argument("--script", action="store_true")
    ap.add_argument("--words", default=None, metavar="CUMLE_ID")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--flow", action="store_true")
    ap.add_argument("--shots", default=None, help="çekim indeksleri, virgülle")
    ap.add_argument("-k", type=int, default=2, help="çekim başına kare")
    ap.add_argument("--cols", type=int, default=3)
    ap.add_argument("--scale", type=float, default=0.5)
    ap.add_argument("--at", default=None, help="PARÇA-İÇİ saniyeler, virgülle (tam çözünürlük PNG)")
    ap.add_argument("--clip", nargs=2, type=float, default=None, metavar=("T0", "SURE"))
    a = ap.parse_args()
    if a.script:
        print_script(a.cid)
        return
    if a.words:
        print_words(a.cid, a.words)
        return
    if a.flow:
        r = subprocess.run([sys.executable, os.path.join(HERE, "qa_flow.py"), "--part", str(part_of(a.cid)), "--chapters", a.cid, "--fast"])
        sys.exit(r.returncode)
    prog = build(a.cid)
    if a.check:
        check(prog, a.cid)
        return
    if a.at:
        for t in [float(x) for x in a.at.split(",")]:
            img = prog.frame(int(t * FPS))
            p = os.path.join(outdir(a.cid), f"{a.cid}_t{t:g}.png")
            cv2.imwrite(p, cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
            print(p)
        return
    if a.clip:
        t0, dur = a.clip
        n0, n = int(t0 * FPS), int(dur * FPS)
        p = os.path.join(outdir(a.cid), f"{a.cid}_clip.mp4")
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
