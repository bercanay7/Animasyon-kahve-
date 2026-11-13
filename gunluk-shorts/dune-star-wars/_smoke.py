"""Tüm zaman çizelgesinde kare örnekleyerek istisna avı (render öncesi duman testi)"""
import sys, traceback
from multiprocessing import Pool
sys.path.insert(0, ".")
import compose, cues
from engine import FPS

def one(i):
    try:
        compose.render_frame(i)
        return None
    except Exception as e:
        return (i, repr(e), traceback.format_exc().splitlines()[-4:])

if __name__ == "__main__":
    step = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    NF = int(round(cues.T * FPS))
    idx = list(range(0, NF, step)) + [NF - 1]
    # geçiş pencerelerini yoğun tara
    for tb, _ in cues.TRANS:
        c = int(tb * FPS)
        idx += list(range(max(0, c - 6), min(NF, c + 7)))
    idx = sorted(set(idx))
    with Pool(4) as p:
        res = [r for r in p.map(one, idx, chunksize=4) if r]
    print(f"{len(idx)} kare tarandı, hata: {len(res)}")
    for r in res[:8]:
        print(r)
