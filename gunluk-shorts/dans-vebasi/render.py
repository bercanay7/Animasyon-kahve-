"""Videoyu render eder: python3 render.py [--frames a:b] [--out yol] [--audio wav]
Kareler 4 süreçte çizilir, ham RGB ffmpeg'e pipe edilir (libx264, yuv420p, bt709)."""
import subprocess, sys, time
from multiprocessing import Pool
import compose
from engine import FPS, W, H
import cues
NF = int(round(cues.T * FPS))

def main():
    a, b, out, audio = 0, NF, "out/emu_noaudio.mp4", None
    for x in sys.argv[1:]:
        if x.startswith("--frames="): a, b = map(int, x.split("=")[1].split(":"))
        if x.startswith("--out="): out = x.split("=")[1]
        if x.startswith("--audio="): audio = x.split("=")[1]
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-"]
    if audio: cmd += ["-i", audio]
    cmd += ["-vf", "scale=out_color_matrix=bt709:out_range=tv,format=yuv420p", "-c:v", "libx264", "-preset", "medium", "-crf", "17",
            "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-r", str(FPS)]
    if audio: cmd += ["-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest"]
    cmd += ["-movflags", "+faststart", out]
    ff = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    t0 = time.time()
    with Pool(4) as p:
        for k, (i, data) in enumerate(p.imap(compose.frame_bytes, range(a, b), chunksize=2)):
            ff.stdin.write(data)
            if k % 48 == 0: print(f"{k}/{b-a} {time.time()-t0:.0f}s", flush=True)
    ff.stdin.close(); ff.wait()
    print("bitti", out, f"{time.time()-t0:.0f}s")

if __name__ == "__main__":
    main()
