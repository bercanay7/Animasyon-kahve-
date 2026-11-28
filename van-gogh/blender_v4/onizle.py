# -*- coding: utf-8 -*-
"""Plakalardan depoya girecek küçük önizlemeler (sistem python'u: Pillow + ffmpeg).

  python van-gogh/blender_v4/onizle.py A01 G02
Çıktı: onizleme/<PLAN>_{25,50,75}.jpg (960 px, JPEG 85) ve onizleme/<PLAN>.mp4 (640 px, ≤ 3 MB, BT.709).
"""
import glob
import json
import os
import shutil
import subprocess
import sys

from PIL import Image

BURA = os.path.dirname(os.path.abspath(__file__))
ON = os.path.join(BURA, "onizleme")
os.makedirs(ON, exist_ok=True)


def ffmpeg():
    f = shutil.which("ffmpeg") or os.environ.get("FFMPEG")
    if f:
        return f
    g = glob.glob(os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\WinGet\Packages\Gyan.FFmpeg*\*\bin\ffmpeg.exe"))
    return g[0]


def plan(p):
    kok = os.path.join(BURA, "plaka", p)
    kareler = sorted(glob.glob(os.path.join(kok, "rgb", "*.png")))
    bilgi = json.load(open(os.path.join(kok, "bilgi.json"), encoding="utf-8"))
    n = len(kareler)
    for yuzde in (25, 50, 75):
        im = Image.open(kareler[min(n - 1, round((n - 1) * yuzde / 100))]).convert("RGB")
        im = im.resize((960, round(960 * im.height / im.width)), Image.LANCZOS)
        im.save(os.path.join(ON, "%s_%d.jpg" % (p, yuzde)), quality=85)
    cikti = os.path.join(ON, p + ".mp4")
    for crf in (24, 27, 30, 33, 36):
        subprocess.run([ffmpeg(), "-v", "error", "-y", "-framerate", str(bilgi["fps"]), "-i", os.path.join(kok, "rgb", "%04d.png"),
                        "-vf", "scale=640:-2,setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709",
                        "-c:v", "libx264", "-crf", str(crf), "-preset", "slow", "-pix_fmt", "yuv420p",
                        "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
                        "-movflags", "+faststart", cikti], check=True)
        if os.path.getsize(cikti) <= 3 * 1024 * 1024:
            break
    print(p, n, "kare", "%.2f MB" % (os.path.getsize(cikti) / 1048576), "crf", crf)


if __name__ == "__main__":
    for p in sys.argv[1:]:
        plan(p)
