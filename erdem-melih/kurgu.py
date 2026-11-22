"""Erdem Melih Tattoo Studio: dikey Reels kurgusu (1080x1920, 30 kare/sn).
Girdi: sabitlenmiş ara kopya (1440x2560, tools/hazirla.sh), müzik (audio/muzik.py), logo (tools/logo_temizle.py).
Akış: 0–5,0 sn klip (renk, iPad'e yavaş yaklaşma, iki yazı), 4,55–5,0 zoom vuruşu → karanlık,
5,0–8,5 sn logo kartı (müzikteki vuruşla açılır, ışık süpürmesi, 'RANDEVU İÇİN DM').
Kullanım: python3 kurgu.py <stab.mov> <muzik.wav> <cikti.mp4> [--muziksiz] [--kare N:dosya.png]"""
import sys, subprocess, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = __file__.rsplit("/", 1)[0]
args = [a for a in sys.argv[1:] if not a.startswith("--")]
STAB, MUZ, OUT = args[0], args[1], args[2]
MUZIKSIZ = "--muziksiz" in sys.argv
YAZISIZ = "--yazisiz" in sys.argv  # hiç yazı yok, üstte küçük logo yok; yalnız sonda logo kartı
YZ = 0.0 if YAZISIZ else 1.0
KARE = None
for a in sys.argv:
    if a.startswith("--kare="):
        KARE = [(int(x.split(":")[0]), x.split(":")[1]) for x in a[7:].split(",")]
W, H, FPS = 1080, 1920, 30
SW, SH = 1440, 2560
HIT = 5.0
DUR = 8.5
NF = int(DUR * FPS)
rng = np.random.default_rng(3)

def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def ease_io(x): x = clamp(x); return x * x * (3 - 2 * x)
def ease_out(x): x = clamp(x); return 1 - (1 - x) ** 3
def ease_in(x): x = clamp(x); return x ** 3
def win(t, a, b, fi=0.35, fo=0.3):
    """a–b aralığında görünürlük (yumuşak giriş/çıkış)."""
    return ease_io((t - a) / fi) * (1 - ease_io((t - (b - fo)) / fo))

# ---------- renk düzeni (LUT) ----------
x = np.linspace(0, 1, 256)
s = x * x * (3 - 2 * x)
base = 0.62 * x + 0.38 * s                      # yumuşak S eğrisi
base = 0.018 + base * (0.985 - 0.018)           # siyahı hafif kaldır, beyazı yumuşat
shadow = (1 - x) ** 2.2; high = x ** 2.0
lutR = np.clip(base + 0.020 * high - 0.010 * shadow, 0, 1)
lutG = np.clip(base + 0.004 * shadow, 0, 1)
lutB = np.clip(base + 0.022 * shadow - 0.020 * high, 0, 1)
LUT = (np.stack([lutR, lutG, lutB], 1) * 255).astype(np.float32)
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
rr = np.hypot((xx - W / 2) / (W / 2), (yy - H * 0.47) / (H / 2))
VIG = (1 - 0.30 * np.clip(rr - 0.35, 0, None) ** 1.6)[..., None]
TOPGRAD = (1 - 0.55 * np.clip(1 - yy / 520, 0, 1) ** 1.8)[..., None]   # üstte logo okunurluğu
BOTGRAD = (1 - 0.35 * np.clip((yy - 1500) / 420, 0, 1) ** 1.5)[..., None]

def grade(img):
    a = np.asarray(img)
    out = np.empty(a.shape, np.float32)
    for c in range(3): out[..., c] = LUT[a[..., c], c]
    lum = out.mean(2, keepdims=True)
    out = lum + (out - lum) * 0.88                   # doygunluk %88
    return out

# ---------- yazı katmanları ----------
FONT_DIR = f"{HERE}/fonts"
def text_layer(lines, sizes, weights, tracking, gap=18, color=(255, 255, 255)):
    fonts = [ImageFont.truetype(f"{FONT_DIR}/Cinzel_{w}.ttf", sz) for sz, w in zip(sizes, weights)]
    widths = []
    for ln, f, tr in zip(lines, fonts, tracking):
        widths.append(sum(f.getlength(c) for c in ln) + tr * (len(ln) - 1))
    hts = [f.getbbox("ÇİĞŞHg")[3] for f in fonts]
    Wl = int(max(widths)) + 80; Hl = sum(hts) + gap * (len(lines) - 1) + 80
    lay = Image.new("RGBA", (Wl, Hl), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    y = 40
    for ln, f, tr, wd, ht in zip(lines, fonts, tracking, widths, hts):
        xx_ = (Wl - wd) / 2
        for c in ln:
            d.text((xx_, y), c, font=f, fill=color + (255,)); xx_ += f.getlength(c) + tr
        y += ht + gap
    a = np.asarray(lay).astype(np.float32) / 255
    sh = np.asarray(lay.split()[3].filter(ImageFilter.GaussianBlur(14))).astype(np.float32) / 255
    return a, np.clip(sh * 1.6, 0, 1)

def ornament(width=420):
    lay = Image.new("RGBA", (width, 40), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    c = width / 2
    d.line([(10, 20), (c - 22, 20)], fill=(255, 255, 255, 200), width=2)
    d.line([(c + 22, 20), (width - 10, 20)], fill=(255, 255, 255, 200), width=2)
    d.polygon([(c, 6), (c + 7, 20), (c, 34), (c - 7, 20)], fill=(255, 255, 255, 255))
    return np.asarray(lay).astype(np.float32) / 255

T1 = text_layer(["HER DÖVME", "BİR SOHBETLE BAŞLAR"], [64, 46], ["700Bold", "400Regular"], [14, 7])
T2 = text_layer(["FİKRİN", "BURADA ŞEKİLLENİR"], [64, 46], ["700Bold", "400Regular"], [14, 7])
ORN = ornament()
CTA = text_layer(["RANDEVU İÇİN DM"], [40], ["600SemiBold"], [10])

def blit(dst, layer, cx, cy, alpha, shadow=None, sh_alpha=0.75, scale=1.0):
    """layer: HxWx4 (0..1). dst: float 0..255."""
    if alpha <= 0.002: return
    if scale != 1.0:
        im = Image.fromarray((layer * 255).astype(np.uint8), "RGBA")
        im = im.resize((max(1, int(im.width * scale)), max(1, int(im.height * scale))), Image.LANCZOS)
        layer = np.asarray(im).astype(np.float32) / 255
        if shadow is not None:
            shadow = np.asarray(Image.fromarray((shadow * 255).astype(np.uint8)).resize(im.size, Image.LANCZOS)).astype(np.float32) / 255
    h, w = layer.shape[:2]
    x0, y0 = int(round(cx - w / 2)), int(round(cy - h / 2))
    xa, ya, xb, yb = max(0, x0), max(0, y0), min(W, x0 + w), min(H, y0 + h)
    if xa >= xb or ya >= yb: return
    sub = dst[ya:yb, xa:xb]
    L = layer[ya - y0:yb - y0, xa - x0:xb - x0]
    if shadow is not None:
        S = shadow[ya - y0:yb - y0, xa - x0:xb - x0][..., None] * sh_alpha * alpha
        sub *= (1 - S)
    A = L[..., 3:4] * alpha
    sub[:] = sub * (1 - A) + L[..., :3] * 255 * A

# ---------- logo ----------
LOGO = Image.open(f"{HERE}/logo/em_logo_beyaz.png")
def logo_arr(width, tint=1.0):
    im = LOGO.resize((width, int(LOGO.height * width / LOGO.width)), Image.LANCZOS)
    a = np.asarray(im).astype(np.float32) / 255
    a[..., :3] *= tint
    return a
LOGO_SMALL = logo_arr(190)
LOGO_SMALL_SH = np.clip(np.asarray(Image.fromarray((LOGO_SMALL[..., 3] * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(10))).astype(np.float32) / 255 * 1.5, 0, 1)
LOGO_BIG = logo_arr(780)
LH, LW = LOGO_BIG.shape[:2]
LOGO_GLOW = np.asarray(Image.fromarray((LOGO_BIG[..., 3] * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(28))).astype(np.float32) / 255

# ---------- iPad izi (stab.mov koordinatı) ----------
KEYS = [(0, 885, 1290), (75, 945, 1200), (150, 840, 1185)]
def ipad(fr):
    for (f0, x0, y0), (f1, x1, y1) in zip(KEYS, KEYS[1:]):
        if fr <= f1:
            u = ease_io((fr - f0) / (f1 - f0)); return x0 + (x1 - x0) * u, y0 + (y1 - y0) * u
    return KEYS[-1][1:]

def sample(src, cx, cy, z):
    s = (SW / W) / z
    cx = clamp(cx, W / 2 * s, SW - W / 2 * s); cy = clamp(cy, H / 2 * s, SH - H / 2 * s)
    return src.transform((W, H), Image.AFFINE, (s, 0, cx - W / 2 * s, 0, s, cy - H / 2 * s), resample=Image.BICUBIC)

# ---------- kaynak kareler ----------
dec = subprocess.Popen(["ffmpeg", "-v", "error", "-i", STAB, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
frames = []
while True:
    b = dec.stdout.read(SW * SH * 3)
    if len(b) < SW * SH * 3: break
    frames.append(Image.frombuffer("RGB", (SW, SH), b, "raw", "RGB", 0, 1))
dec.wait()
print("kaynak kare:", len(frames))

def render(i):
    t = i / FPS
    if t < HIT:
        fr = min(len(frames) - 1, i)
        src = frames[fr]
        u = t / HIT
        z = 1.0 + 0.16 * ease_io(u)
        ix, iy = ipad(fr)
        w_ = 0.25 + 0.6 * ease_io(u)
        cx = SW / 2 + (ix - SW / 2) * w_; cy = SH / 2 + (iy - SH / 2) * w_
        punch = clamp((t - 4.40) / 0.60) ** 2
        if punch > 0:
            zp = z * (1 + 0.55 * punch)
            # radyal (zoom) bulanıklık: birkaç ölçeğin ortalaması
            n = 5; acc = None
            for k in range(n):
                im = sample(src, ix, iy, zp * (1 + 0.06 * punch * k / (n - 1)))
                a = np.asarray(im).astype(np.float32)
                acc = a if acc is None else acc + a
            img = Image.fromarray((acc / n).astype(np.uint8))
            cx, cy = ix, iy
        else:
            img = sample(src, cx, cy, z)
        f = grade(img) * VIG * (TOPGRAD if YZ else 1.0) * BOTGRAD
        # açılış: siyahtan 0,35 sn
        f *= ease_out(t / 0.35)
        # kapanış: vuruşa doğru karart
        f *= 1 - ease_in((t - 4.62) / 0.38) * 0.97
        # küçük logo (üstte)
        blit(f, LOGO_SMALL, W / 2, 245, YZ * win(t, 0.25, 4.6, 0.5, 0.25), LOGO_SMALL_SH, 0.6)
        # yazılar (koyu gömlek bölgesi; Instagram alt arayüzünün üstünde)
        for lay, a0, b0 in ((T1, 0.55, 2.55), (T2, 2.70, 4.55)):
            al = YZ * win(t, a0, b0, 0.45, 0.30)
            if al > 0:
                rise = 26 * (1 - ease_out((t - a0) / 0.6))
                blit(f, lay[0], W / 2, 1335 + rise, al, lay[1], 0.85)
                blit(f, ORN, W / 2, 1335 + rise + lay[0].shape[0] / 2 + 6, al * 0.9)
    else:
        tl = t - HIT
        # zemin: koyu, merkezde hafif ışık
        g = 6 + 22 * np.clip(1 - rr * 0.95, 0, 1) ** 2
        f = np.repeat(g[..., None], 3, 2).astype(np.float32)
        f[..., 0] *= 1.02; f[..., 2] *= 0.98
        # logo: vuruşla açılır (ölçek 1,10 → 1,0), sonra çok yavaş büyür
        ap = ease_out(tl / 0.55)
        sc = 1.10 - 0.10 * ap + 0.025 * ease_io(tl / 3.5)
        cyL = 880
        # parıltı (glow)
        glow = np.zeros((LH, LW, 4), np.float32); glow[..., :3] = 1; glow[..., 3] = LOGO_GLOW * 0.35 * (0.6 + 0.4 * math.exp(-tl * 2.5))
        blit(f, glow, W / 2, cyL, ap, scale=sc)
        # ışık süpürmesi: gümüş tondan beyaza geçen çapraz bant
        lg = LOGO_BIG.copy()
        base = 0.80
        sweep_t = (tl - 0.75) / 0.9
        gy, gx = np.mgrid[0:LH, 0:LW].astype(np.float32)
        pos = -0.3 + 1.6 * clamp(sweep_t)
        d = (gx / LW + 0.45 * gy / LH) / 1.45 - pos
        band = np.exp(-(d / 0.07) ** 2) if 0 <= sweep_t <= 1.05 else 0.0
        lg[..., :3] = np.clip(base + (1 - base) * 1.0 * band + 0.0, 0, 1)[..., None] if np.ndim(band) else base
        blit(f, lg, W / 2, cyL, ap, scale=sc)
        # alt yazı
        ac = YZ * ease_io((tl - 1.2) / 0.5)
        blit(f, ORN, W / 2, 1395, ac * 0.85)
        blit(f, CTA[0], W / 2, 1462 + 14 * (1 - ease_out((tl - 1.2) / 0.6)), ac, CTA[1], 0.5)
        # vuruş anı: kısa beyaz flaş
        f += 30 * math.exp(-tl * 22) * (tl < 0.3)
    # film greni (2 karede bir değişir: dosya boyu)
    gr = np.random.default_rng(i // 2).standard_normal((H // 2, W // 2)).astype(np.float32)
    gr = np.repeat(np.repeat(gr, 2, 0), 2, 1)[..., None] * 3.2
    f = f + gr
    return np.clip(f, 0, 255).astype(np.uint8)

if KARE:
    for i, p in KARE:
        Image.fromarray(render(i)).save(p); print("kare", i, p)
    sys.exit()

enc_cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-"]
if MUZIKSIZ:
    enc_cmd += ["-i", STAB, "-filter_complex",
                f"[1:a]volume=1.6,afade=t=in:d=0.3,afade=t=out:st={HIT-0.25}:d=0.25,apad,atrim=0:{DUR}[a]", "-map", "0:v", "-map", "[a]"]
else:
    # müzik + odanın kendi sesi (hafif), -14 LUFS
    enc_cmd += ["-i", MUZ, "-i", STAB, "-filter_complex",
                f"[2:a]volume=0.55,afade=t=in:d=0.3,afade=t=out:st={HIT-0.3}:d=0.3,apad[amb];"
                f"[1:a][amb]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.0:LRA=11,aresample=48000[a]",
                "-map", "0:v", "-map", "[a]"]
enc_cmd += ["-t", str(DUR), "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-profile:v", "high", "-pix_fmt", "yuv420p",
            "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", "-movflags", "+faststart",
            "-c:a", "aac", "-b:a", "256k", OUT]
enc = subprocess.Popen(enc_cmd, stdin=subprocess.PIPE)
for i in range(NF):
    enc.stdin.write(render(i).tobytes())
    if i % 30 == 0: print("kare", i, "/", NF, flush=True)
enc.stdin.close(); enc.wait()
print("bitti", OUT)
