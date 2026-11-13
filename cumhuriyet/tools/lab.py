"""Bölge renk ölçümü (CIE Lab, D65): python3 tools/lab.py kare.png x0 y0 x1 y1 [...] → medyan L*, C*, ton°"""
import sys, numpy as np
from PIL import Image
im = np.asarray(Image.open(sys.argv[1]).convert('RGB')).astype(float) / 255
def lab(rgb):
    c = np.where(rgb > .04045, ((rgb + .055) / 1.055) ** 2.4, rgb / 12.92)
    M = np.array([[.4124, .3576, .1805], [.2126, .7152, .0722], [.0193, .1192, .9505]])
    xyz = c @ M.T / np.array([.95047, 1, 1.08883])
    f = np.where(xyz > .008856, np.cbrt(xyz), 7.787 * xyz + 16 / 116)
    L = 116 * f[..., 1] - 16; a = 500 * (f[..., 0] - f[..., 1]); b = 200 * (f[..., 1] - f[..., 2])
    return L, a, b
a = list(map(int, sys.argv[2:]))
for k in range(0, len(a), 4):
    x0, y0, x1, y1 = a[k:k + 4]; L, A, B = lab(im[y0:y1, x0:x1])
    print(f'({x0},{y0})-({x1},{y1}): L* {np.median(L):.0f}  C* {np.median(np.hypot(A, B)):.0f}  ton {np.degrees(np.arctan2(np.median(B), np.median(A))) % 360:.0f}°')
