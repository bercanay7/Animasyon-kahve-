#!/usr/bin/env python3
"""Medici — PARÇA (1–7) bazlı paralel render + birleştirme + ses ekleme + denetim.

Her komut bir parçayla çalışır: `--part N` (ya da MEDICI_PART=N). Çıktılar `out_pN/` altındadır (seg/, medici_pN_noaudio.mp4, medici_P{N}.mp4).

  python3 render.py --part 3 --list                        # parça planı (segmentler)
  python3 render.py --part 3 --all [--workers 4] [--seg 1200] [--crf 19] [--segs 0-3]   # parçayı üret (kaldığı yerden devam eder)
  python3 render.py --part 3 --range 120 180 --out out_p3/prev.mp4 [--scale 1280]       # kısa önizleme (parça-içi sn; sessiz)
  python3 render.py --part 3 --concat                      # segmentleri sessiz tek dosyada birleştir → out_p3/medici_p3_noaudio.mp4
  python3 render.py --part 3 --mux [--audio out_p3/mix_audio.m4a] [--onizleme]          # video + miks → out_p3/medici_P3.mp4
  python3 render.py --part 3 --qa                          # ffprobe/blackdetect/freezedetect denetimi
  python3 render.py --part 3 --overview [--every 20]       # parçadan her N sn'de bir kare → out_p3/frames/overview_N.png
  python3 render.py --tam [--out out_tam/medici_tam_film.mp4]   # 7 final parçayı art arda birleştir (Tam Film)

GERÇEK SES KORUMASI: `--mux` (ve `--tam`) geçici (Piper) anlatım varsa DURUR (parca.assert_gercek_ses). `--onizleme` ile geçici sesle
`ONIZLEME_medici_P{N}.mp4` adıyla üretilebilir (yayına GİRMEZ). Kare hataları out_pN/seg/errors.log'a yazılır; önceki kare tekrarlanır."""
import argparse
import glob
import json
import math
import multiprocessing as mp
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.chdir(HERE)

import parca as PA  # noqa: E402

FPS = 24
MAXRATE, BUFSIZE = "9M", "18M"      # YouTube önerisi (1080p24 SDR ≈ 8 Mb/sn); film greni tepe bit hızını şişirmesin
W, H = 1920, 1080
N_PARTS = 7


def part_dirs(part):
    out = os.path.join(HERE, f"out_p{part}")
    return out, os.path.join(out, "seg")


def total_frames(part):
    import compose
    prog = compose.Program(part=part)
    return int(math.ceil(prog.total * FPS)), prog.total


def plan(nframes, seg):
    return [(i, a, min(nframes, a + seg)) for i, a in enumerate(range(0, nframes, seg))]


def ff_cmd(out, crf, preset, scale=None, threads=2):
    vf = []
    if scale:
        vf = ["-vf", f"scale={scale}:-2:flags=lanczos"]
    return ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
            *vf, "-c:v", "libx264", "-preset", preset, "-crf", str(crf), "-maxrate", MAXRATE, "-bufsize", BUFSIZE, "-pix_fmt", "yuv420p", "-color_primaries", "bt709", "-color_trc", "bt709",
            "-colorspace", "bt709", "-g", "48", "-bf", "2", "-threads", str(threads), "-an", out]


def render_segment(args):
    part, idx, n0, n1, crf, preset = args
    import numpy as np
    import cv2
    cv2.setNumThreads(1)
    _, SEG = part_dirs(part)
    os.makedirs(SEG, exist_ok=True)
    final = os.path.join(SEG, f"seg_{idx:04d}.mp4")
    if os.path.exists(final + ".done"):
        return idx, 0.0, 0
    import compose
    prog = compose.Program(part=part)
    tmp = final + ".tmp.mp4"
    ff = subprocess.Popen(ff_cmd(tmp, crf, preset), stdin=subprocess.PIPE)
    t0 = time.time()
    last = None
    errs = 0
    for n in range(n0, n1):
        try:
            img = prog.frame(n)
            last = img
        except Exception as e:  # kare hatası: önceki kareyi tekrarla, kaydet
            errs += 1
            with open(os.path.join(SEG, "errors.log"), "a", encoding="utf-8") as fh:
                fh.write(f"kare {n} (t={n / FPS:.2f}s): {type(e).__name__}: {e}\n")
            img = last if last is not None else np.zeros((H, W, 3), np.uint8)
        ff.stdin.write(np.ascontiguousarray(img).tobytes())
        k = n - n0 + 1
        if k % 120 == 0:
            el = time.time() - t0
            print(f"[P{part} seg {idx:02d}] {k}/{n1 - n0}  {el / k * 1000:.0f} ms/kare  ETA {el / k * (n1 - n0 - k) / 60:.1f} dk", flush=True)
    ff.stdin.close()
    rc = ff.wait()
    if rc != 0:
        raise RuntimeError(f"ffmpeg hata kodu {rc} (P{part} seg {idx})")
    os.replace(tmp, final)
    open(final + ".done", "w").write(f"{n0} {n1} {time.time() - t0:.1f}\n")
    return idx, time.time() - t0, errs


def cmd_list(a):
    _, SEG = part_dirs(a.part)
    nf, tot = total_frames(a.part)
    p = plan(nf, a.seg)
    print(f"PARÇA {a.part}: toplam {tot:.2f} sn = {nf} kare; {len(p)} segment × ≤{a.seg} kare")
    for i, n0, n1 in p:
        done = os.path.exists(os.path.join(SEG, f"seg_{i:04d}.mp4.done"))
        print(f"  seg {i:02d}: kare {n0}–{n1}  ({n0 / FPS:7.1f}–{n1 / FPS:7.1f} sn) {'✓' if done else ''}")


def cmd_all(a):
    _, SEG = part_dirs(a.part)
    nf, tot = total_frames(a.part)
    p = plan(nf, a.seg)
    only = None
    if a.segs:
        only = set()
        for s in a.segs.split(","):
            lo, _, hi = s.partition("-")
            only.update(range(int(lo), int(hi or lo) + 1))
    todo = [(a.part, i, n0, n1, a.crf, a.preset) for i, n0, n1 in p if not os.path.exists(os.path.join(SEG, f"seg_{i:04d}.mp4.done")) and (only is None or i in only)]
    print(f"PARÇA {a.part}: {len(p)} segmentten {len(todo)} tanesi üretilecek; {a.workers} işlem", flush=True)
    t0 = time.time()
    ctx = mp.get_context("spawn")
    errs = 0
    with ctx.Pool(a.workers, maxtasksperchild=1) as pool:
        for idx, dt, e in pool.imap_unordered(render_segment, todo):
            errs += e
            print(f"== P{a.part} seg {idx:02d} bitti ({dt / 60:.1f} dk, hata {e}); geçen {(time.time() - t0) / 60:.1f} dk", flush=True)
    print(f"tamam: {(time.time() - t0) / 60:.1f} dk; kare hatası toplam {errs}")


def cmd_range(a):
    import numpy as np
    import cv2
    import compose
    cv2.setNumThreads(2)
    OUT, _ = part_dirs(a.part)
    prog = compose.Program(part=a.part)
    n0, n1 = int(a.range[0] * FPS), int(a.range[1] * FPS)
    out = a.out or os.path.join(OUT, "prev.mp4")
    ff = subprocess.Popen(ff_cmd(out, 22, "veryfast", scale=a.scale, threads=2), stdin=subprocess.PIPE)
    t0 = time.time()
    for n in range(n0, n1):
        ff.stdin.write(np.ascontiguousarray(prog.frame(n)).tobytes())
    ff.stdin.close(); ff.wait()
    print(f"{out}  ({(n1 - n0) / FPS:.1f} sn, {(time.time() - t0) / (n1 - n0) * 1000:.0f} ms/kare)")


def noaudio_path(part):
    return os.path.join(part_dirs(part)[0], f"medici_p{part}_noaudio.mp4")


def cmd_concat(a):
    _, SEG = part_dirs(a.part)
    nf, tot = total_frames(a.part)
    p = plan(nf, a.seg)
    files = [os.path.join(SEG, f"seg_{i:04d}.mp4") for i, _, _ in p]
    missing = [f for f in files if not os.path.exists(f + ".done")]
    if missing:
        raise SystemExit(f"eksik segment: {len(missing)} (ör. {os.path.basename(missing[0])}); önce --all")
    lst = os.path.join(SEG, "concat.txt")
    open(lst, "w").write("".join(f"file '{f}'\n" for f in files))
    out = noaudio_path(a.part)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", out], check=True)
    print(out, os.path.getsize(out) // 1_000_000, "MB")


def find_audio(part, explicit=None):
    OUT, _ = part_dirs(part)
    if explicit:
        return explicit
    cands = [os.path.join(OUT, n) for n in ("mix_audio.m4a", "mix_audio.wav")] + sorted(glob.glob(os.path.join(OUT, "mix_audio*ONIZLEME*.m4a")) + glob.glob(os.path.join(OUT, "ONIZLEME*.m4a")))
    return next((p for p in cands if os.path.exists(p)), None)


def cmd_mux(a):
    OUT, _ = part_dirs(a.part)
    if not a.onizleme:
        PA.assert_gercek_ses(OUT)              # geçici (Piper) anlatım varsa DURUR
    vid = noaudio_path(a.part)
    if not os.path.exists(vid):
        cmd_concat(a)
    audio = find_audio(a.part, a.audio)
    if not audio:
        raise SystemExit(f"ses dosyası yok (miks): önce MEDICI_PART={a.part} python3 miks_kur.py")
    if (not a.onizleme) and "ONIZLEME" in os.path.basename(audio).upper():
        raise SystemExit("önizleme miksi final mux'a girmez; gerçek sesle yeniden miksleyin")
    name = f"ONIZLEME_medici_P{a.part}.mp4" if a.onizleme else f"medici_P{a.part}.mp4"
    out = a.out or os.path.join(OUT, name)
    vd = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", vid]).decode().strip())
    ad = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", audio]).decode().strip())
    print(f"PARÇA {a.part}: video {vd:.2f} sn, ses {ad:.2f} sn (fark {vd - ad:+.2f})")
    acodec = ["-c:a", "copy"] if audio.endswith(".m4a") else ["-c:a", "aac", "-b:a", "256k"]
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", vid, "-i", audio, "-map", "0:v", "-map", "1:a", "-c:v", "copy", *acodec,
                    "-shortest", "-movflags", "+faststart", out], check=True)
    print(out, os.path.getsize(out) // 1_000_000, "MB")


def cmd_tam(a):
    """7 final parçayı art arda (kodek kopyası) birleştirir → Tam Film. Yalnız gerçek sesli final parçalar."""
    files = []
    for n in range(1, N_PARTS + 1):
        OUT, _ = part_dirs(n)
        PA.assert_gercek_ses(OUT)
        f = os.path.join(OUT, f"medici_P{n}.mp4")
        if not os.path.exists(f):
            raise SystemExit(f"eksik final parça: {f}")
        files.append(f)
    out = a.out or os.path.join(HERE, "out_tam", "medici_tam_film.mp4")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    lst = os.path.join(os.path.dirname(out), "concat.txt")
    open(lst, "w").write("".join(f"file '{f}'\n" for f in files))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", "-movflags", "+faststart", out], check=True)
    print(out, os.path.getsize(out) // 1_000_000, "MB")


def cmd_qa(a):
    OUT, SEG = part_dirs(a.part)
    cands = [a.out] if a.out else [os.path.join(OUT, f"medici_P{a.part}.mp4"), os.path.join(OUT, f"ONIZLEME_medici_P{a.part}.mp4"), noaudio_path(a.part)]
    vid = next((c for c in cands if c and os.path.exists(c)), None)
    if not vid:
        raise SystemExit("denetlenecek dosya yok")
    print("denetlenen:", vid)
    info = subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,codec_name,width,height,r_frame_rate,duration,nb_frames", "-of", "json", vid]).decode()
    for s in json.loads(info)["streams"]:
        print("  ", s)
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", vid, "-vf", "blackdetect=d=0.4:pix_th=0.06,freezedetect=n=-60dB:d=2.5", "-an", "-f", "null", "-"],
                       capture_output=True, text=True)
    lines = [l for l in r.stderr.splitlines() if "blackdetect" in l or "freeze_" in l]
    print(f"  siyah/donuk bölge satırı: {len(lines)}")
    for l in lines[:60]:
        print("   ", l.strip())
    el = os.path.join(SEG, "errors.log")
    if os.path.exists(el):
        print("  KARE HATALARI:")
        print("   ", open(el, encoding="utf-8").read().strip().replace("\n", "\n    "))
    else:
        print("  kare hatası yok ✓")


def cmd_overview(a):
    import cv2
    import numpy as np
    import compose
    import preview
    cv2.setNumThreads(2)
    OUT, _ = part_dirs(a.part)
    prog = compose.Program(part=a.part)
    ts = [t for t in np.arange(2.0, prog.total - 1.0, a.every)]
    imgs = []
    for t in ts:
        im = prog.frame(int(t * FPS))
        cv2.rectangle(im, (0, 0), (260, 40), (0, 0, 0), -1)
        cv2.putText(im, f"{int(t // 60)}:{int(t % 60):02d}", (10, 31), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (240, 215, 140), 2, cv2.LINE_AA)
        imgs.append(im)
    os.makedirs(os.path.join(OUT, "frames"), exist_ok=True)
    per = 16
    for k in range(0, len(imgs), per):
        p = os.path.join(OUT, "frames", f"overview_{k // per + 1}.png")
        preview.sheet(imgs[k:k + per], cols=4, scale=0.38, path=p)
        print(p)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--part", type=int, default=PA.PART, help="1–7 (ya da MEDICI_PART)")
    ap.add_argument("--overview", action="store_true")
    ap.add_argument("--every", type=float, default=20.0)
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--range", nargs=2, type=float)
    ap.add_argument("--concat", action="store_true")
    ap.add_argument("--mux", action="store_true")
    ap.add_argument("--tam", action="store_true")
    ap.add_argument("--qa", action="store_true")
    ap.add_argument("--onizleme", action="store_true", help="geçici sesle önizleme muxu (ONIZLEME_ adıyla; yayına girmez)")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--segs", default=None, help="yalnız bu segmentler, ör. 0-3 veya 1,3,5-6")
    ap.add_argument("--seg", type=int, default=1200)
    ap.add_argument("--crf", type=int, default=19)
    ap.add_argument("--preset", default="medium")
    ap.add_argument("--scale", default=None)
    ap.add_argument("--out", default=None)
    ap.add_argument("--audio", default=None)
    a = ap.parse_args()
    if a.tam:
        return cmd_tam(a)
    if not a.part:
        print(__doc__)
        raise SystemExit("--part N (1–7) gerekli")
    if not 1 <= a.part <= N_PARTS:
        raise SystemExit("part 1–7 olmalı")
    if a.list:
        cmd_list(a)
    elif a.all:
        cmd_all(a)
    elif a.range:
        cmd_range(a)
    elif a.concat:
        cmd_concat(a)
    elif a.mux:
        cmd_mux(a)
    elif a.qa:
        cmd_qa(a)
    elif a.overview:
        cmd_overview(a)
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
