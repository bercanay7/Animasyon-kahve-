# 28 ve 29 Ekim Atatürk Story'leri için zemin hazırlar: python3 ataturk.py  (Pillow, numpy, opencv-python-headless)
# Kaynak: kaynak/ataturk-referans.jpg, telefon ekran görüntüsü. Görselin kendisi y 133–1806, x 0–942 arasında.
#   build/ataturk-28.png  1080x1920, alıntı ve imza olduğu gibi
#   build/ataturk-29.png  aynı zemin, "Efendiler, yarın Cumhuriyeti ilan edeceğiz." silinmiş, imza duruyor
import os
import numpy as np
import cv2
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
os.makedirs(os.path.join(HERE, 'build'), exist_ok=True)
src = np.asarray(Image.open(os.path.join(HERE, 'kaynak', 'ataturk-referans.jpg')).convert('RGB')).copy()

# Durum çubuğu ve üstteki yuvarlak köşeler dışarıda kalsın; alttaki köşeler zaten siyah zeminde
TOP, BOTTOM = 223, 1807
src[1700:BOTTOM] = 1  # alt köşelerdeki arayüz rengini sil (bu bölge zaten saf siyah)

# Alıntı yazısı: koyu takım elbisenin üstünde açık renkli harfler. Maske = çevresinden belirgin açık pikseller
x0, x1, y0, y1 = 185, 765, 1278, 1500
gray = cv2.cvtColor(src, cv2.COLOR_RGB2GRAY)
roi = gray[y0:y1, x0:x1]
local = cv2.medianBlur(roi, 31)
mask = np.zeros(gray.shape, np.uint8)
mask[y0:y1, x0:x1] = ((roi.astype(int) - local.astype(int)) > 18).astype(np.uint8) * 255
mask = cv2.dilate(mask, np.ones((5, 5), np.uint8), iterations=2)
clean = cv2.inpaint(src, mask, 7, cv2.INPAINT_TELEA)


def story(a, name):
    crop = Image.fromarray(a[TOP:BOTTOM])
    w = 1080
    h = round(crop.height * w / crop.width)
    out = Image.new('RGB', (1080, 1920), (1, 1, 1))
    out.paste(crop.resize((w, h), Image.LANCZOS), (0, 0))
    out.save(os.path.join(HERE, 'build', name))


story(src, 'ataturk-28.png')
story(clean, 'ataturk-29.png')
print('Hazır: build/ataturk-28.png, build/ataturk-29.png')
