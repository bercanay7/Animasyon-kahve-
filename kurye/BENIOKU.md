# Mektuplar: yağlıboya canlanan resim (26 Kasım 2026)

Kullanıcı yaratıcılığı tamamen başkana bıraktı: "detaylı, güzel, gerçekten sanatsal bir iş". Gönderdiği örnekler (geyik, iskambil, merdiven ve çerçeveler, satranç, orkestra, BMW) yalnız başvuru.

## Fikir
Kanalın kimliği: "geçmişten bugüne soru taşıyan kurye". Bunun görsel şiiri:
- Gün batımında, yalnız bir meşeye uzanan buğday tarlası.
- Kurye çantasıyla patikadan yürür, durur, güneşe döner, çantasını açar.
- Rüzgâr mektupları alır; kâğıtlar havada döne döne kuşa dönüşür ve güneşin ışığına uçar.
- Anlatım yok; 25 sn. Kanal jeneriği ya da bir videonun kapanışı olabilir.

## Nasıl yapıldı
- **Resim:** `lib/tablo_ciz.js` değer planlı düz bir resim çizer: gök, uzak tepeler, tarla ve patika, meşe, ön plan otları.
  - Her katman ayrı tuvaldir.
  - Dorian'ın yağlıboya motoru (`dorian-gray/kapi/vendor/impasto.js`, `plate.js`; Lemo-Opuscar, MIT) bu resmi Hertzmann yöntemiyle kaba darbeden ince darbeye spatula ve fırça darbelerine çevirir.
  - Darbeler boya kalınlığı, sıyıran ışık ve tuval dokusuyla basılır.
  - Durağan katmanlar yüklenirken bir kez boyanır (~84 bin darbe, 1,7 sn).
- **Derinlik:** kamera meşeye ve güneşe doğru yavaşça yaklaşır. Her katman kendi derinliğinde kayar.
- **Canlı katmanlar:** her iki karede bir yeniden boyanır (15 çizim/sn; boyalı animasyonun nabzı).
  - **Kurye:** `araclar/manken` 3B mankeni resmin perspektifiyle çizilir (ufuk y = 700, dikey görüş 40°).
    - Okunan görüntü darbelere çevrilir: içte seyrek, kenarda sık.
    - Güneş karşıdan ve çok alçakta: figür karşı ışıkta siluet, gölgesi bize doğru uzanır.
    - Yürüyüş `araclar/hareket` (ayak kaymaz); çanta sarkaç.
  - **Rüzgâr:** tarlada 3200 başak darbesi; açı, ilerleyen bir rüzgâr dalgasıyla eğilir.
  - **Işık:** güneşten yayılan yarı saydam spatula darbeleri (nefes alır), havada polen.
  - **Mektuplar → kuşlar:** kâğıt döne döne uçar. Dönüşüm sırasında kâğıt darbesi incelir, iki kanat darbesi belirir ve çırpmaya başlar; renk kremden koyu siluete geçer.

## Dosyalar
- `tablo.html`: sahne (sözleşme: `window.READY`, `DUR`, `renderAt(t)`, `BITIR`).
- `lib/tablo_ciz.js`: resmin katmanları.

## Komutlar
```bash
node araclar/manken/kare.js kurye/tablo.html cikti/ 5,13,21          # tek kare + süre
node /home/user/Animasyon-kahve-/araclar/manken/render.js kurye/tablo.html mektuplar.mp4   # 4 işçi
```

## Ölçüm
- Kare başına ~7 sn (tek işçi, SwiftShader, süper örnekleme 1,5). Durağan darbeler her karede yeniden basılıyor; pahalı olan bu.
- Hızlandırma yolu: durağan katmanları bir kez dokuya basıp kamera yaklaşmasını dokudan yapmak. Kabartma ışığı sabit kalır, darbeler yeniden basılmaz.

## Hassasiyet taraması
- **Kuşlar** küçük, sürekli çırpan siluetler; açık kanatlı simetrik amblem değil.
- **Kol** mektupları bırakırken göğüs hizasında öne açılır, omuzun üstüne çıkmaz; havaya kalkmış düz kol yok.
- **Ağacın gölgesi** tarlada koyu bir kama; tümsek ya da mezar okunmuyor.
- **Patika** ağacın dibinde biter; ağaçta asılı bir şey yok.
