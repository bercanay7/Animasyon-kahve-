"""Gerçek görsel aralarının kırpımları: python3 tools/gorsel_kirp.py
Girdi kaynak/gorsel/ham/ (indirme kaydı kaynak/GORSELLER.md), çıktı kaynak/gorsel/*.png|jpg.
Kırpma kutuları elle ölçüldü (Met görselleri) ya da archive.org djvu.xml kelime kutularından alındı (Ellis, Freud).
Maskelenen yerler kâğıdın kendi tonuyla (çevre medyanı) örtülür; metin uydurulmaz, yalnız dışarıda bırakılır."""
import os
from PIL import Image, ImageDraw, ImageStat
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HAM = os.path.join(ROOT, 'kaynak', 'gorsel', 'ham'); OUT = os.path.join(ROOT, 'kaynak', 'gorsel')


def kagit(im, box):  # kâğıt tonu: satır arasındaki boş şeridin kanal medyanı (yazısız bölge verilir)
    return tuple(int(v) for v in ImageStat.Stat(im.crop(box).convert('RGB')).median)


def ortu(im, rects, ton):
    d = ImageDraw.Draw(im)
    for r in rects: d.rectangle(r, fill=ton)
    return im


def kaydet(im, ad, q=92):
    fn = os.path.join(OUT, ad)
    if ad.endswith('.jpg'): im.convert('RGB').save(fn, quality=q)
    else: im.save(fn)
    print(fn, im.size)


# 1) Tempesta 1606 (Met 401131): bütün levha (yazı satırı dahil)
t = Image.open(os.path.join(HAM, 'met401131_DP864257.jpg'))
kaydet(t, 'tempesta1606.jpg')

# 2) Callot / Lux Claustri 22 (Met 419135): resim + üstündeki Fransızca satır (Latince başlık, şiir ve sayfa numarası dışarıda)
c = Image.open(os.path.join(HAM, 'met419135_DP890746.jpg'))
kaydet(c.crop((250, 360, 2060, 1590)), 'callot1646_resim_satir.jpg')
kaydet(c.crop((250, 360, 2060, 480)), 'callot1646_satir.jpg')          # P079: yalnız satır
kaydet(c.crop((520, 470, 2060, 1590)), 'callot1646_resim.jpg')          # yalnız resim (secde okunursa alt kırpma ayrıca)

# 3) Ellis 1898, Alienist and Neurologist 19, s.280 (archive.org alienistneurolog1918unse, n297)
#    djvu kutuları: 'self-admiration. This Narcissus-like tendency,' satırı y 1952–2014; 'tendency,' x 1549–1907;
#    önceki satırda 'often entirely lost in' x 1517–2194. Cinsiyetçi çerçeve (', of which the normal germ in women …') örtülür.
e = Image.open(os.path.join(HAM, 'ellis1898_an_n297.jpg')).convert('RGB')
ton = kagit(e, (300, 1932, 2150, 1948))   # iki satır arasındaki boşluk
X = 1900   # 'tendency,' virgülünden sonra (', of which' dışarıda)
a = e.crop((228, 1932, X + 16, 2032)).copy(); ortu(a, [(X - 228, 0, a.width, a.height)], ton)
kaydet(a, 'ellis1898_satir.png')
b = e.crop((228, 1846, 2212, 2032)).copy()
ortu(b, [(0, 0, 1512 - 228, 2030 - 1846 - 100), (X - 228, 2030 - 1846 - 100, b.width, b.height)], ton)   # üst satırda 'often'den öncesi, alt satırda 'tendency,'den sonrası
kaydet(b, 'ellis1898_iki_satir.png')
kaydet(e.crop((230, 250, 1500, 345)), 'ellis1898_sayfa_basi.png')         # '280 Havelock Ellis.' sayfa başlığı (künye için)

# 4) Freud 1914, Jahrbuch der Psychoanalyse VI, s.1 (archive.org jb61914, n10): başlık + ad + I + ilk paragraf
f = Image.open(os.path.join(HAM, 'freud1914_jb_n10.jpg')).convert('RGB')
kaydet(f.crop((100, 940, 2780, 2680)), 'freud1914_s1_ust.jpg')
kaydet(f.crop((100, 940, 2780, 1920)), 'freud1914_s1_baslik.jpg')        # başlık + ad + ilk üç satır ('Näcke 1899')
kaydet(f.resize((f.width // 2, f.height // 2), Image.LANCZOS), 'freud1914_s1_tam.jpg')
