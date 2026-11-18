"""Seçilen Met CC0 görsellerini depoya alır ve kaynak/GORSELLER.md'yi yazar.
Kullanım: python3 -I tools/gorsel_kaydet.py <met/tam klasörü> <clouet resmi>"""
import json, os, sys
from PIL import Image
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC, CLOUET = sys.argv[1], sys.argv[2]
G = os.path.join(R, 'kaynak', 'gorsel'); os.makedirs(G, exist_ok=True)
meta = json.load(open(os.path.join(SRC, 'meta.json')))
for m in meta:
    Image.open(os.path.join(SRC, m['dosya'])).save(os.path.join(G, m['dosya']), quality=85)
im = Image.open(CLOUET).convert('RGB'); im.thumbnail((2000, 2000)); im.save(os.path.join(G, 'mary_clouet_beyazyas_resim.jpg'), quality=85)
L = ['# Gerçek görseller (yalnız CC0 / kamu malı)', '',
     'Erişim: 18 Kasım 2026. Met Open Access nesneleri API ile doğrulandı (`isPublicDomain: true` → CC0). Dosyalar uzun kenar ≤ 2400 px, JPG.',
     'Kullanım: `silent-film` yeniden çizim geçişinden geçer ya da `archive-lighttable` arasında masada gösterilir. 18.–19. yüzyıl tarih baskıları "sonraki yüzyılların hayal ettiği" diye anlatılır, belge gibi sunulmaz.', '',
     '| Dosya | Eser | Sanatçı | Tarih | Kurum ve no | Lisans | Teknik |', '|---|---|---|---|---|---|---|']
for m in meta:
    L.append(f"| `{m['dosya']}` | {m['baslik']} | {m['sanatci'] or '–'} | {m['tarih']} | The Met {m['id']} ([sayfa]({m['url']})) | CC0 (Met Open Access) | {m['teknik']} |")
L.append('| `mary_clouet_beyazyas_resim.jpg` | Mary, Queen of Scots (in white mourning), Clouet\'den sonra | bilinmiyor (François Clouet\'den sonra) | 16. yy | Scottish National Portrait Gallery; Wikimedia Commons "Unknown after Francois Clouet - Mary, Queen of Scots, 1542 - 1587. Reigned 1542 - 1567 (In white mourning) - Google Art Project.jpg" | Kamu malı (PD-Art; 16. yy eseri) | Commons sayfasındaki şablon elle denetlenecek (API oran sınırı) |')
L += ['', '## Hassasiyet notları',
      '- `idam_gardiner_1790.jpg`, `idam_iln_1861.jpg`: baltayı ve cellatı gösterir; yalnız kırpılmış ayrıntı (salon, seyirciler) kullanılır, darbe anı gösterilmez.',
      '- `rizzio_cinayeti_*`: şiddet sahnesi; yalnız gölgeli genel plan, kan yok.',
      '- `hayali_bulusma_currier.jpg` (1868): iki kraliçenin karşılaşması **kurgudur** (Schiller); anlatımda "böyle bir buluşma hiç olmadı" diye kullanılır.',
      '- `elizabeth_kameo_yuzuk.jpg`: Elizabeth portreli bir yüzük; anlatıdaki dostluk elmasının kendisi değildir, öyle sunulmaz.']
open(os.path.join(R, 'kaynak', 'GORSELLER.md'), 'w').write('\n'.join(L) + '\n')
print(len(meta) + 1, 'görsel')
