# Narkissos üslup kapısı: VAZO adayı

Kırmızı figür vazo dili, motor `prometheus/lib` (kaynağı `sisifos/lib`). Ortak sahte anlatım `../ortak/zaman.json`; olaylar `S()` / `Wd()`'ye bağlı.

## Dosyalar
- `index.html`: `?t=…&mb=…` tek kare çizer; `window.renderAt(t, mb)` ve `window.READY`. `?dikey=1` D planını 1080×1920 çizer, `?kapak=yazili|yazisiz` kapak.
- `nark.js`: beş plan (A–E), yansıma (`mirror`), analitik halka (`warpRings`, `ringLines`), telefon camı ↔ havuz biçim dönüşümü (`morphPts`), alttan ışık (`litFigure`).
- `kapak.js`: kapak taslağı (1920'de çizilir, 1280×720'ye küçültülür).
- `main.js`: kare döngüsü, hareket bulanıklığı (180° obtüratör, `mb` alt kare, plan sınırını aşmaz), doku + vinyet + gren (tohum `floor(f/2)`).
- `lib/`: `prometheus/lib`'den kopya. Değişiklikler yalnız `figure.js`'te:
  - `HAIR_MOD`: bugünün genci için kısa saç (`lk.hairPts`);
  - `lk.coatCol`, `lk.sleeveCol`: bugünün giysisi (seyreltik sır ceket, uzun kol);
  - `lk.noCurls`: alın bukleleri yok;
  - sakalsız kırmızı figürde ağız kil çizgisi çizilmez; yüz konturunu aşıp "sigara" gibi okunuyordu, yerine kazıma çizgi.
- `fonts/`: Bebas Neue (latin + latin-ext; `orfeus/fonts`'tan, OFL). `sisifos/fonts.css`'te Bebas yok.

## Komutlar
Kökü `narkissos/kapi` olan küçük bir yerel http sunucusu kullanılır (`../ortak/` erişimi için).

```
node kare.js <klasör> A_cam=1.5,4 D_benim=15.0,4        # ad=t[,mb] → PNG
node kare.js <klasör> kapak=kapak:yazili kapak0=kapak:yazisiz
node kare.js <klasör> dikey_D=dikey:14.9,4               # 1080×1920
WORKERS=3 MB=4 node render.js <çıktı.mp4>                # 19,5 sn, 30 fps, H.264 CRF 18, BT.709, sessiz
```

## Tanıma hamlesi ('benim', 14,6 sn)
'benim'e kadar yansıma kendi zamanından 0,3 sn geride çizilir (başka biri gibi geç cevap verir) ve seyreltik sırla soluktur (saydamlık 0,44). 'Sonra anladı'da genç suya doğru eğilir, yansıma bu eğilmeye geç uyar. 'benim'de:
- gecikme sıfırlanır (birebir kilit);
- genç irkilip başını geri çeker, kaşlar kalkar, ağız aralanır;
- yansıma bedenin kiline yaklaşır (0,44 → 0,84);
- iki göz arasında kısa bir noktalı kil çizgi belirip söner.
