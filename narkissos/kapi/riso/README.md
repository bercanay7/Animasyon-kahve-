# Narkissos üslup kapısı: RİSOGRAF adayı

Ortak zaman çizelgesi `../ortak/zaman.json` (19,5 sn, beş plan A–E). Olaylar `S()`/`Wd()`'ye bağlı.

## Dosyalar
- `vendor/riso.js`, `vendor/draw.js`: Lemo-Opuscar (lemomo-ai/lemo-opuscar) 3a7132b, MIT (`vendor/LICENSE-MIT.txt`). Değişiklikler dosya başında yazılı:
  su/cam artık bir **maske dokusu** (R su, G piksel ızgarası, B parıltı), yansımada plaka başına kayma (`sep`), analitik gözyaşı halkası (her plaka kendi evresinde), sabit kodlu beyaz dalga kırıkları kaldırıldı (`uGap`, varsayılan 0), suyun kendi mürekkebi (`ink`), yarım ton → piksel ızgarası geçişi, `uReflX` (kapakta yazı suya yansımasın), hale damgası 8.
  Lemo'nun STYLE.md / DEMO.md metinleri (CC BY-NC) depoya alınmadı; yalnız uygulandı.
- `figur.js`: genç profil başı (alın, burun, dudak, çene, göz, kaş, kulak; antik kısa dalgalı saç / bugünün kısa saçı), yürüyen avcı, dirseklerine dayanıp yüzüstü uzanan genç.
- `sahne.js`: planlar A–E, kapak, kayıt (plaka) vuruşları.
- `main.js`, `index.html`: `window.renderAt(t, mb)`, hazır işareti `window.READY` / `window.HAZIR`. `?t=…&mb=…`, `?kapak=1|0`, `?w=1080&h=1920`.
- `render.js`: yerel http sunucusu (kök `narkissos/kapi/`, `../ortak` erişilebilir).
- `fonts/`: Bebas Neue (OFL, latin + latin-ext; `ran/fonts`'tan).

## Komutlar
```
cd narkissos/kapi/riso
node render.js kareler          # 9 anahtar kare (PNG, mb=4)
node render.js kare 12.2 4      # tek kare
node render.js kapak            # kapak.jpg + kapak_yazisiz.jpg (1280×720)
node render.js dikey 15.0       # dikey_D.png (1080×1920)
WORKERS=3 node render.js video 4  # kapi.mp4 (19,5 sn, 30 fps, sessiz, CRF 18, BT.709)
node render.js olc 4            # tek işçi kare süresi
```
Çıktılar varsayılan olarak `OUT=/tmp/…/scratchpad/kapi/riso`.

## Mürekkepler ve plakalar
R = Federal Blue (61,85,136), G = Sunflower (255,181,17), B = Teal (0,131,138); kâğıt (244,238,226). Floresan pembe yok.
Ten: yalnız Sunflower tonu. Saç: Blue + Sunflower (kahve-siyah). Pelerin: Teal. Su: yansıma + `ink`.

## Üslubun hamleleri
- **"Başkası" → "benim":** yansımanın plakaları baştan kayık (±9 px); gözyaşı halkasında kayma büyür, `Wd('S4','benim')`'de tek vuruşta yerine oturur (sönümlü salınım ~0,1 sn), dalga durur, suyun mürekkebi azalır (yansıma yüz renginde), yansıyan gözde kâğıt parıltısı belirir, bütün karede kayıt tepmesi.
- **Gözyaşı:** `Wd('S4','gözyaşı')`'de göz pınarında damla, yerçekimiyle düşer; suya değdiği an hesaplanır, analitik halka oradan yayılır.
- **Cam ↔ havuz:** A'da telefon camı (piksel ızgarası) havuza (yarım ton) döner; E'de tersi: kıyı düz kenar + yuvarlak köşeye, noktalar piksel ızgarasına, `Wd('S5','yine')`'de aynı halka siyah camda.
- Karakterler ikişerli (15 fps), kamera her karede; gren tohumu `floor(f/2)`.
- Hareket bulanıklığı: plaka ve maske tuvalleri alt karelerde çizilip ortalanır, baskı bir kez.
