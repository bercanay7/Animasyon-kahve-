# Mektuplar: yağlıboya canlanan resim (26 Kasım 2026)

Kullanıcı yaratıcılığı tamamen başkana bıraktı: "detaylı, güzel, gerçekten sanatsal bir iş". Gönderdiği örnekler (geyik, iskambil, merdiven ve çerçeveler, satranç, orkestra, BMW) yalnız başvuru.

## Fikir (v2, 26 Kasım; bağımsız eleştiriden sonra)
Kanalın kimliği "geçmişten bugüne soru taşıyan kurye". Bunun görsel şiiri (25 sn, anlatım yok):
- 0–7 sn: gün batımında buğday tarlası, yalnız bir meşe. Kurye soldan girer, patikada durur.
- 7 sn: başını ağaca kaldırır, çantasından tek bir mektup çıkarır, göğsünde tutar.
- 11–13 sn: soldan bir rüzgâr dalgası başakları yatırarak gelir, mektubu elinden alır.
- 12–19 sn: mektup döne döne önce bize gelir, sonra meşenin tacına konar.
- 19 sn: konduğu yerden dışa doğru tacın içinde beş yapraklı açık çiçekler açılır. Ağaç cevap verir.
- 17–25 sn: güneş tepelerin ardına batar, ışık soğur.

v1'de (mektuplar → kuşlar) eleştirmen şunları buldu:
- filtre görünümü;
- güneş diskinde hedef tahtası;
- tacın köz görünümü;
- 18 sn'den sonra hiçbir şeyin olmaması;
- figürün kesik bir delik gibi okunması.

Ayrıntı ve kurallar: `araclar/tablo/KILAVUZ.md`.

## Sürümler (26 Kasım)
- **v1:** mektuplar kuşa dönüşür. Eleştiri: filtre görünümü, hedef tahtası güneş, köz taç, 18. saniyeden sonra hiçbir şey olmuyor.
- **v2:** fırça, ışık ve hikâye yeniden kuruldu (tek mektup, rüzgâr, çiçek, batış).
- **v3:** kamera koreografisi, kuryeye dönen yapraklar, özgün ezgi ve ElevenLabs efektleri, siyah-beyaz kip.
- **v4** (ikinci eleştiriden):
  - taç fırçayla boyandı;
  - çiçekler mektubun girdiği noktadan açılır;
  - şapka ve palto düzeltildi;
  - ayak sesi, varış notası; −16 LUFS.
- **v5:** kurye Blender'da (`blender/`); boyama aynı.

## Ses (`audio/`)
- `ses.py`: numpy ile özgün ezgi (soru ve cevap motifi; doruk çiçek anında).
- ElevenLabs Sound Effects v3 (`efekt/`): tarla, esinti, zarf, ayak sesi. Adımlar `adimlar.js`'in bulduğu basma anlarına konur.
- Düzey: iki geçişli doğrusal loudnorm, −16 LUFS.

## Nasıl yapıldı
- **Resim:** `lib/tablo_ciz.js` değer planlı düz bir resim çizer: gök, uzak tepeler, tarla ve patika, meşe, ön plan otları. Her katman ayrı tuvaldir.
- **Motor:** ortak tablo motoru (`araclar/tablo/`, Lemo-Opuscar impasto, MIT) resmi kaba darbeden ince darbeye fırça ve spatula darbelerine çevirir. Durağan katmanlar bir kez boyanıp önbellekten kamerayla basılır.
- **Derinlik:** kamera yavaşça yaklaşır; her katman kendi derinliğinde kayar. Meşe rüzgârda gövdesinin dibinden eğilir (döndürülmüş kamera).
- **Canlı katmanlar** (iki karede bir):
  - **Kurye:** `araclar/manken` 3B mankeni resmin perspektifiyle çizilir; okunan görüntü darbelere çevrilir. Şapka, çapraz kayışlı çanta, güneş yanında altın kenar ışığı. Yürüyüş `araclar/hareket` ile yapılır (ayak kaymaz).
  - Başaklar, rüzgâr dalgası, güneş diski ve hüzme, polen, mektup (zarf: kapak çizgisi, iki yüz), çiçekler.

## Dosyalar
- `tablo.html`: sahne (sözleşme: `window.READY`, `DUR`, `renderAt(t)`, `BITIR`).
- `lib/tablo_ciz.js`: resmin katmanları.

## Komutlar
```bash
node araclar/manken/kare.js kurye/tablo.html cikti/ 5,13,21          # tek kare + süre
node /home/user/Animasyon-kahve-/araclar/manken/render.js kurye/tablo.html mektuplar.mp4   # 4 işçi
```

## Ölçüm
- **v1:** kare 7,2 sn; 25 sn'lik film 4 işçiyle 88 dk.
- **v2:** önbellekle kare ~1 sn.

## Hassasiyet taraması (v2)
- **Güneş diski** halka ya da ışın darbesiyle çizilmez (hedef tahtası); yatay sürütme.
- **Güneş figürün başının arkasında durmaz** (hale okunur); kurye güneşin solunda durur.
- **Çiçekler** beş yapraklıdır; dört yapraklı öbek küçükte haç okunuyordu.
- **Taçta turuncu leke yok** (köz, yanan ağaç).
- **Kol** mektubu göğüs hizasında tutar ve bırakır; omuzun üstüne çıkmaz (selam okunmaz).
- **Ağacın gölgesi** yumuşak, loblu bir göldür (kama ışık konisi ya da rampa okunuyordu).
- **Ağaçta asılı nesne yok;** çiçekler tacın içinde, dalda sarkan bir şey yok (adak ağacı okunmasın).
- **Şapkanın kenarı** keskin spatula darbesiyle çizilir; boncuklu kenar kıvırcık yuvarlak baş (karikatür) okunuyordu.

### v1 notları (arşiv)
- **Kuşlar** küçük, sürekli çırpan siluetler; açık kanatlı simetrik amblem değil.
- **Kol** mektupları bırakırken göğüs hizasında öne açılır, omuzun üstüne çıkmaz; havaya kalkmış düz kol yok.
- **Ağacın gölgesi** tarlada koyu bir kama; tümsek ya da mezar okunmuyor.
- **Patika** ağacın dibinde biter; ağaçta asılı bir şey yok.
