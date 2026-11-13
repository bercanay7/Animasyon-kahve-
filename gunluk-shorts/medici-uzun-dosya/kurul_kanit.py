#!/usr/bin/env python3
"""Kurul kanıt paketi: bitmiş bir Medici parçasının mp4'ünden kurul üyelerine verilecek GÖRSEL + SAYISAL kanıtı üretir (kurullar sesi dinleyemez, videoyu oynatamaz).

  python3 kurul_kanit.py --part 1 [--src out_p1/medici_P1.mp4] [--out out_p1/kurul]

Üretir (--out altında):
  genel_NN.png        : her ≈9 sn'de bir kare, 4×4 kontak sayfaları (1920×1080; tam süre taranır)
  gecis_<ad>.png      : seçili geçişlerin çevresinde 0,125 sn adımlı 8 karelik şerit (akış/hareket kanıtı)
  tam_<ad>.png        : tam çözünürlüklü 12 kritik kare (okunurluk, çizgi kalitesi, yazı)
  hareket.json        : 0,5 sn adımlı ardışık kare farkı (gri 240×135) → durgunluk/ritim eğrisi + özet
  teknik.json         : ffprobe + kare hızı + bit hızı + (varsa) ses raporu özeti
"""
import argparse
import json
import os
import subprocess
import sys

import cv2
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)


def read_frame(cap, t, fps):
    cap.set(cv2.CAP_PROP_POS_FRAMES, int(round(t * fps)))
    ok, f = cap.read()
    return f if ok else None


def label(img, text):
    cv2.rectangle(img, (0, 0), (img.shape[1], 22), (0, 0, 0), -1)
    cv2.putText(img, text, (6, 16), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (240, 215, 140), 1, cv2.LINE_AA)
    return img


def sheet(imgs, cols, tile_w):
    tiles = []
    for im in imgs:
        h = int(im.shape[0] * tile_w / im.shape[1])
        tiles.append(cv2.resize(im, (tile_w, h), interpolation=cv2.INTER_AREA))
    th = tiles[0].shape[0]
    rows = []
    for i in range(0, len(tiles), cols):
        row = tiles[i:i + cols]
        while len(row) < cols:
            row.append(np.zeros_like(tiles[0]))
        rows.append(np.concatenate(row, axis=1))
    return np.concatenate(rows, axis=0)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--part", type=int, default=1)
    ap.add_argument("--src", default=None)
    ap.add_argument("--out", default=None)
    ap.add_argument("--gecisler", default="", help="virgüllü 'ad:sn' (örn. oda_belge:44.2,iris:107.4)")
    a = ap.parse_args()
    src = a.src or f"out_p{a.part}/medici_P{a.part}.mp4"
    out = a.out or f"out_p{a.part}/kurul"
    os.makedirs(out, exist_ok=True)
    cap = cv2.VideoCapture(src)
    fps = cap.get(cv2.CAP_PROP_FPS)
    n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    dur = n / fps
    print(f"{src}: {dur:.1f} sn, {fps:.2f} fps, {n} kare")

    # 1) genel kontak sayfaları
    step = dur / 64.0
    ts = [min(dur - 0.1, 1.0 + i * step) for i in range(64)]
    for k in range(4):
        imgs = []
        for t in ts[k * 16:(k + 1) * 16]:
            f = read_frame(cap, t, fps)
            if f is None:
                f = np.zeros((1080, 1920, 3), np.uint8)
            imgs.append(label(f.copy(), f"{int(t // 60)}:{t % 60:04.1f}"))
        cv2.imwrite(f"{out}/genel_{k + 1:02d}.png", sheet(imgs, 4, 480))

    # 2) geçiş şeritleri
    gec = [x.split(":") for x in a.gecisler.split(",") if x]
    for name, t0 in gec:
        t0 = float(t0)
        imgs = []
        for i in range(8):
            t = max(0, t0 - 0.5 + i * 0.125)
            f = read_frame(cap, t, fps)
            if f is not None:
                imgs.append(label(f.copy(), f"{name} {t:.2f}s"))
        if imgs:
            cv2.imwrite(f"{out}/gecis_{name}.png", sheet(imgs, 4, 480))

    # 3) tam çözünürlüklü kritik kareler: 12 eşit aralıklı + başlık kartı
    for i, t in enumerate(np.linspace(8, dur - 12, 12)):
        f = read_frame(cap, float(t), fps)
        if f is not None:
            cv2.imwrite(f"{out}/tam_{i + 1:02d}_{int(t)}s.png", f)

    # 4) hareket eğrisi (0,5 sn adımlı kare farkı)
    prev = None
    diffs = []
    t = 0.0
    while t < dur - 0.2:
        f = read_frame(cap, t, fps)
        if f is None:
            break
        g = cv2.cvtColor(cv2.resize(f, (240, 135), interpolation=cv2.INTER_AREA), cv2.COLOR_BGR2GRAY).astype(np.float32)
        if prev is not None:
            diffs.append(float(np.mean(np.abs(g - prev))))
        prev = g
        t += 0.5
    d = np.array(diffs)
    still = 0
    run = 0
    maxrun = 0
    for v in d:
        if v < 0.35:
            run += 1
            maxrun = max(maxrun, run)
        else:
            run = 0
    summ = dict(adim_sn=0.5, n=len(d), ort=float(d.mean()), medyan=float(np.median(d)), p10=float(np.percentile(d, 10)), p90=float(np.percentile(d, 90)),
                durgun_oran_esik_0_35=float((d < 0.35).mean()), en_uzun_durgun_koşu_sn=maxrun * 0.5)
    json.dump(dict(ozet=summ, egri=[round(x, 3) for x in diffs]), open(f"{out}/hareket.json", "w"), indent=1)
    print("hareket:", summ)

    # 5) teknik
    pr = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,codec_name,width,height,r_frame_rate,bit_rate,pix_fmt,color_space,color_primaries,color_transfer,sample_rate,channels:format=duration,size,bit_rate", "-of", "json", src],
                        capture_output=True, text=True)
    tek = json.loads(pr.stdout)
    json.dump(tek, open(f"{out}/teknik.json", "w"), indent=1)
    print(json.dumps(tek)[:600])


if __name__ == "__main__":
    main()
