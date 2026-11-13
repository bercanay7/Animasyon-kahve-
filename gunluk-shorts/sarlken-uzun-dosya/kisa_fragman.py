#!/usr/bin/env python3
"""Uzun videodan dikey (9:16) Kısa fragman üretir: yayin/sarlken_kisa_fragman.mp4

  python3 kisa_fragman.py [--src out/sarlken_uzun.mp4] [--t0 0] [--t1 46.1] [--out yayin/sarlken_kisa_fragman.mp4]

Düzen: bulanık-karartılmış arka plan (aynı video, dikey kırpım) + ortada 16:9 kare (altın çerçeve) + üstte başlık
+ altta yakılmış altyazı (yayin/sarlken_tr.srt'den kesit). Ses: kaynak videonun sesi (son 0,8 sn sönüm)."""
import argparse
import os
import re
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
FONTS = os.path.join(HERE, "fonts")


def srt_slice(src, dst, t0, t1):
    def p(ts):
        h, m, rest = ts.split(":")
        s, ms = rest.split(",")
        return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000

    def f(t):
        t = max(0, t)
        return f"{int(t // 3600):02d}:{int(t % 3600 // 60):02d}:{int(t % 60):02d},{int(round((t % 1) * 1000)):03d}"

    blocks = open(src, encoding="utf-8").read().strip().split("\n\n")
    out, n = [], 0
    for b in blocks:
        L = b.split("\n")
        if len(L) < 3:
            continue
        a, c = [p(x) for x in L[1].split(" --> ")]
        if c <= t0 or a >= t1:
            continue
        a, c = max(a, t0) - t0, min(c, t1) - t0
        n += 1
        out.append(f"{n}\n{f(a)} --> {f(c)}\n" + "\n".join(L[2:]))
    open(dst, "w", encoding="utf-8").write("\n\n".join(out) + "\n")
    return n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default="out/sarlken_uzun.mp4")
    ap.add_argument("--t0", type=float, default=0.0)
    ap.add_argument("--t1", type=float, default=46.1)
    ap.add_argument("--out", default="yayin/sarlken_kisa_fragman.mp4")
    a = ap.parse_args()
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    srt = "out/_cache/kisa_altyazi.srt"
    os.makedirs("out/_cache", exist_ok=True)
    n = srt_slice("yayin/sarlken_tr.srt", srt, a.t0, a.t1)
    dur = a.t1 - a.t0
    style = "FontName=Cormorant Garamond,Fontsize=17,Bold=1,PrimaryColour=&H00C8E6F0,OutlineColour=&H00000000,BorderStyle=1,Outline=3,Shadow=1,Alignment=2,MarginV=420"
    fc = (
        "[0:v]split=2[a][b];"
        "[a]scale=-2:1920,crop=1080:1920,gblur=sigma=40,eq=brightness=0.04:saturation=1.15[bg];"
        "[b]scale=1080:-2[fg];"
        "[bg][fg]overlay=(W-w)/2:(H-h)/2-60[v1];"
        "[v1]drawbox=x=0:y=(ih-607)/2-60-3:w=iw:h=3:color=0xC9962B@0.9:t=fill,drawbox=x=0:y=(ih+607)/2-60:w=iw:h=3:color=0xC9962B@0.9:t=fill[v2];"
        f"[v2]drawtext=fontfile={FONTS}/Cinzel_700Bold.ttf:text='ŞARLKEN':fontsize=120:fontcolor=0xF0D27A:x=(w-text_w)/2:y=210:shadowcolor=black@0.8:shadowx=3:shadowy=4,"
        f"drawtext=fontfile={FONTS}/Cinzel_600SemiBold.ttf:text='DÜNYAYI TESLİM EDEN İMPARATOR':fontsize=34:fontcolor=0xE0C682:x=(w-text_w)/2:y=350:shadowcolor=black@0.8:shadowx=2:shadowy=3,"
        f"drawtext=fontfile={FONTS}/CormorantGaramond_700Bold.ttf:text='TAM VİDEO  ·  ZAMAN KURYESİ  ·  UZUN DOSYA 1':fontsize=36:fontcolor=0xD8C07A:x=(w-text_w)/2:y=1700:shadowcolor=black@0.8:shadowx=2:shadowy=3[v3];"
        f"[v3]subtitles={srt}:fontsdir={FONTS}:force_style='{style}'[v]"
    )
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-ss", str(a.t0), "-t", str(dur), "-i", a.src, "-filter_complex", fc,
           "-map", "[v]", "-map", "0:a?", "-af", f"afade=t=out:st={dur - 0.8:.2f}:d=0.8", "-c:v", "libx264", "-preset", "medium", "-crf", "19",
           "-pix_fmt", "yuv420p", "-r", "24", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", a.out]
    subprocess.run(cmd, check=True)
    print(a.out, f"{dur:.1f} sn, altyazı {n} satır", os.path.getsize(a.out) // 1000, "KB")


if __name__ == "__main__":
    main()
