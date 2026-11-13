"""python3 preview.py 0.5 7.4 ... → out/prev_<t>.png"""
import sys, time
import compose
from engine import FPS
for a in sys.argv[1:]:
    t=float(a); t0=time.time()
    img=compose.render_frame(int(round(t*FPS)))
    img.save(f"out/prev_{a}.png"); print(a, round(time.time()-t0,2),"s")
