"""Kontak sayfası: python3 contact.py out/sheet.png t1 t2 ... (6 sütun). --scale=0.25 ile boyut."""
import sys
from multiprocessing import Pool
from PIL import Image, ImageDraw
import compose
from engine import FPS

def one(t):
    return compose.render_frame(int(round(t*FPS)))

if __name__=="__main__":
    args=[a for a in sys.argv[1:] if not a.startswith("--")]
    sc=0.3
    for a in sys.argv[1:]:
        if a.startswith("--scale="): sc=float(a.split("=")[1])
    out=args[0]; ts=[float(a) for a in args[1:]]
    with Pool(4) as p: imgs=p.map(one, ts)
    tw,th=int(1080*sc),int(1920*sc); cols=6
    rows=(len(ts)+cols-1)//cols
    sheet=Image.new("RGB",(cols*tw,rows*(th+0)),(20,20,20))
    d=ImageDraw.Draw(sheet)
    for k,(t,im) in enumerate(zip(ts,imgs)):
        x,y=(k%cols)*tw,(k//cols)*th
        sheet.paste(im.resize((tw,th),Image.LANCZOS),(x,y))
        d.rectangle([x,y,x+60,y+16],fill=(0,0,0)); d.text((x+3,y+2),f"{t:.2f}s",fill=(255,255,0))
    sheet.save(out); print(out, sheet.size)
