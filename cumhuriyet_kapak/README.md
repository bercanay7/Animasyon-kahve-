# Cumhuriyet videosu: yeni kapak paketi (yayın sonrası)

**Neden yeni kapak:** video yayından 2 gün sonra 14,2 B gösterimde %1,1 tıklama oranıyla durdu. İzleyici tutma (%43,5) kanalın en iyi videosu Sisifos kadar iyi; yani içerik değil paketleme sorunluydu.

## Dosyalar
| Dosya | Ne |
|---|---|
| `kapak_yeni_A_sultanin_ogrencisi.jpg` | **SULTANIN ÖĞRENCİSİ**: TO kurulu 9,1 ONAY. Testin ana adayı. |
| `kapak_yeni_B_sultanin_okulunda.jpg` | **SULTANIN OKULUNDA**: aynı görsel, yalnız yazı farklı. TO kurulu 8,4; testte yalnız kelimenin etkisini ölçmek için. |
| `kapak_d.js` | Çizim kodu; videonun kendi motorunu kullanır (`cumhuriyet/lib`). |

**Fikir:** lamba ışığında ders çalışan fesli öğrenci (Mustafa Kemal, Harbiye öncesi). Duvara düşen gölgesi 1920'lerin kalpaklı Mustafa Kemal profili. Videonun iddiasını tek karede söyler: Cumhuriyet'i kuranlar sultanın okullarında yetişti.

Üslup videonunkiyle aynıdır (`cumhuriyet/USLUP.md`): taş baskı kalıpları, yarım ton yalnız duvarda ve lamba halesinde, gradyan yok. Saygı kuralları da korunur: göz hizasında kamera, hale yok, karikatür yok. Gölge ağırbaşlı bir profildir.

## Kurul turları (5 tur)
- Sanat/üslup kurulu ve TO/paketleme kurulu ayrı ayrı değerlendirdi.
- **TO kurulunun düzeltmeleri:** ağız çizgisi yüz dışına taşıyordu (sigara gibi görünüyordu); göz altında gözyaşı gibi okunan ince kâğıt boşluğu vardı (kalıp kayması); gölge çocuktan kopuktu.
- **Sanat kurulunun düzeltmeleri:** kalpak önce silindir şapka gibi, sonra satranç kalesi ya da taç gibi okunuyordu; sonunda yumuşak köşeli kuzu postu kalpağına döndü. Ayrıca çene, lamba halesi ve eller düzeltildi.
- **Son durum:**
  - Sanat/üslup kurulu A ve B'yi 9/10 ile onayladı.
  - TO kurulu A'yı 9,1 ile onayladı; 168 px'te izleyici gölgeyi "Atatürk" diye tanıyor.
  - B 8,4'te kaldı, yalnız kelime daha zayıf olduğu için; testte kontrol amaçlı.

## Yeniden üretmek
`claude/29-ekim-animation-video-hzh7dw` dalındaki `cumhuriyet/` klasöründe:
1. `kapak_d.js`'yi `cumhuriyet/lib/` içine kopyala.
2. `film.html`'de `lib/kapak.js` satırının altına `<script src="lib/kapak_d.js"></script>` ekle.
3. Çiz:
   ```bash
   SCENE=kapakD  node shot.js cikti 0   # SULTANIN / ÖĞRENCİSİ
   SCENE=kapakD2 node shot.js cikti 0   # SULTANIN / OKULUNDA
   ```
4. Kapak test setini çıkar: `python3 tools/kapak_test.py cikti/t0000.00.png test`.

**Not:** çocuğun başı `age:16` ile çizilir. Motorun çocuk kipi (16 yaş altı) gözleri zorla tam açtığı için kitaba inmiş göz kapağı yapılamıyor. Çocuk oranları elle verildi (`jaw`, `cheek`, `HY`), bıyık yok. Başın kalıpları kaymasız basılır; ten kalıbı kayınca burun yanında gözyaşı gibi duran bir boşluk kalıyordu.

## YouTube Studio'da sıra
1. **Başlık:** `Abdülhamid, Kendi Sonunu Getiren Kuşağı Nasıl Yetiştirdi?`
   - Testi başlatmadan önce değiştir; test sürerken dokunma.
   - "29 Ekim" etiketlerde ve açıklamada kalır. Başlıktaki "| 29 Ekim" videoyu geçmiş bir bayram içeriği gibi gösteriyordu.
2. **Test ve karşılaştır** (Ayrıntılar → Küçük resim → Test ve karşılaştır), üç kapak:
   - `kapak_yeni_A_sultanin_ogrencisi.jpg`
   - `kapak_yeni_B_sultanin_okulunda.jpg`
   - mevcut "KURUCU KADRO / AYNI SIRADA" (kontrol)
3. Testi sonuna kadar (~2 hafta) beklet. Sonuç "fark yok" çıkarsa A'yı kalıcı yap.
4. Ölç: TO'nun %1,1'den yükselmesi ve izleyici tutmanın %43 civarında kalması. Kapak doğru vaadi veriyorsa tutma düşmez.

**Not:** Abdülhamid tartışmalı bir figür; yorumlarda tartışma çıkabilir. Bu bir yanıltma değil, etkileşimdir. Sert yorumlara Sisifos'taki gibi sakin ve kaynağa dayanan cevap verilir.
