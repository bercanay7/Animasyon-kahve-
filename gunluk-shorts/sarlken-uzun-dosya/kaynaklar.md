# Şarlken (V. Karl) — Kaynak Kapısı

**Denetlenen metin:** `script.py` — 14 bölüm (c0…c13), 174 cümle, 1.913 gösterim sözcüğü (2.138 okunuş sözcüğü), süre 20:58 (video zaman ekseni: `out/timeline.json`).
**Girdiler:** `arastirma/A1_dogum_miras_secim.md` (A1), `arastirma/A2_reform.md` (A2), `arastirma/_ham_olgu_taslak.md` (A3: Osmanlı/Akdeniz), `arastirma/_ham_olgu_sayfasi.md` (A4: Yeni Dünya/finans), `arastirma/A5_fransa_kisisel_abdikasyon.md` (A5).
**Tarih:** 2026-10-18. **Durum:** `script.py` DEĞİŞTİRİLMEDİ; bu belge yalnız denetim çıktısıdır.
**Sürüm damgası (bayatlama kontrolü):** `script.py` sha256 5146ad40e058 (dosya saati 01:00:40 UTC), `out/timeline.json` sha256 ae653495b42f. `script.py` bu damgadan sonra değişirse tablolar yeniden gözden geçirilmeli.

> **Kapı kararı: ŞARTLI GEÇER.** (1) c6s10 düzeltilmeden yayınlanmamalı; (2) öncelik-1 beş madde (H1 baston, H9 Cohn parafrazı, H21 sedye, H26 Catherine/hala, H37 'birçok tarihçi') ya çözülmeli ya da §5'teki yumuşatma uygulanmalı; (3) kalan HAFIZA maddeleri bu oturumda arama özetiyle büyük ölçüde doğrulandı, yayın öncesi sayfa düzeyinde bir kez teyit edilmesi yeterli.

> **Uygulanan düzeltmeler (18 Ekim 2026, ana ajan):** §5'teki KRİTİK/YÜKSEK maddelerin tamamı ve seçili ORTA/DÜŞÜK maddeler (27 cümle) `script.py`'de düzeltildi ve **cümle düzeyinde yeniden seslendirildi** (ElevenLabs eleven_v4, aynı ses; `ses_yama.py` ile voice.wav'a yamalandı, seviye bölüm ortalamasına eşitlendi, `out/timeline.json` güncellendi). Ayrıntı ve eski→yeni metin: `METIN_DEGISIKLIKLERI.md`. Düzeltilenler: c6s10 (teyze, 'sıkça anlatıldığına göre'), c0s4 (baston kalktı), c2s9 (Cohn parafrazı), c5s12 (sedye kalktı), c13s5 ('birçok tarihçi' kalktı), c0s11, c1s4, c1s12, c2s7, c3s2, c5s3, c5s10, c6s1, c6s3, c6s4, c7s11, c8s5, c8s8, c8s9, c8s11, c9s10, c10s3 (dükat), c11s5, c11s7, c12s1, c13s3, c13s6. Açık kalanlar: §7 HAFIZA listesindeki öncelik-2/3 maddelerin sayfa düzeyinde teyidi (yayın sonrası da yapılabilir) ve `ses_kontrol_listesi.md` kulak denetimi (kullanıcıya bırakıldı).

> **Bir bakışta:** 87 cümle CONFIRMED, 40 NİTELİKLİ, 3 RİVAYET, 25 YORUM, 19 HAFIZA. Doğrulama bekleyen 39 madde var (öncelik-1: 5). **Yayından önce düzeltilmesi gereken tek kesin hata:** c6s10 (Aragonlu Catherine imparatorun *teyzesi*, halası değil). Ayrıntı: §5 Riskli cümleler.

## 1. Yöntem notu

1. 174 cümlenin her biri `script.py`'deki gösterim metniyle okundu ve araştırma dosyalarındaki satırlarla (satır numarası = tablodaki `#`) elle eşleştirildi. Eşleşmeyen her olgusal iddia (ad, tarih, sayı, ilişki, olay) HAFIZA olarak ayrıldı.
2. **Sınıf cümlenin kendi iddiasına göre verildi, araştırma satırının toplu sınıfına göre değil.** Bir satır NİTELİKLİ olsa bile cümlenin kullandığı kısım o niteliği taşımıyorsa (örn. A3 #12'deki Tunus günü tutarsızlığı, metinde yalnız yıl geçtiği için) CONFIRMED yazıldı ve gerekçesi `Not` sütununa eklendi. Tersine, cümle satırın NİTELİKLİ kısmına dayanıyorsa (aralık, tek kaynak, çelişki) NİTELİKLİ yazıldı.
3. Bir cümlede birden çok iddia varsa **en zayıf dayanaklı ana iddia** belirleyicidir. Ana iddiayı etkilemeyen küçük, araştırmada bulunmayan ayrıntılar `+Hn` işaretiyle belirtildi (sınıfı değiştirmez, §7 listesine düşer).
4. İsteğe bağlı olarak WebSearch denendi: bu oturumda **çalıştı** (arama özeti döndürdü), WebFetch ise `getaddrinfo ENOTFOUND` ile **başarısız** oldu. Bu yüzden HAFIZA maddeleri için yapılan ek doğrulama yalnızca arama özeti düzeyindedir; hiçbir sayfa açılıp okunmadı. Sonuçlar §7'de ayrı sütunda, yalnız arama sonuçlarında gerçekten görülen URL'lerle verildi. Araştırma dosyalarında bulunmayan hiçbir kaynak, `Dayanak` sütununa yazılmadı.
5. Ses tarafı (telaffuz) ayrı belgede: `ses_kontrol_listesi.md`.

## 2. Sınıf tanımları

| Sınıf | Anlamı | Videoda beklenen davranış |
|---|---|---|
| **CONFIRMED** | Araştırma dosyalarında doğrulanmış (çoğunlukla ikincil/ansiklopedik kaynak, ≥1 sağlam özet) | Kesin kip kullanılabilir |
| **NİTELİKLİ** | Tek kaynak, kaynaklar arası çelişki, aralıklı sayı ya da popüler kaynak | Hedge gerekir: yaklaşık, aralık, 'anlatılır', 'yazılır' |
| **RİVAYET** | Araştırmada ANEKDOT diye işaretli; metinde 'rivayet' olarak anlatılıyor | 'Rivayete göre / büyük ihtimalle' şart |
| **YORUM** | Anlatıcı yorumu, özet, retorik soru, geçiş, betimleme; tek tek kaynağa bağlanmaz | Olgu gibi sunulmamalı |
| **HAFIZA** | Araştırma dosyalarında YOK; model hafızasına dayanıyor | Yayından önce doğrulanmalı (§7) |
| `+Hn` | Cümlede araştırmada bulunmayan küçük ayrıntı var (§7'deki n. madde) | Düşük öncelik |

## 3. Dürüst sınır notu

- Araştırma dosyalarının hepsi **arama ÖZETLERİne** dayanır (dosyaların kendi başlık notları: sayfa metni okunmadı; ortak WebSearch kotası bitmişti, WebFetch DNS hatası vermişti). **Birincil kaynak ve akademik monografi taranmadı** (Parker 2019, Brandi, Tracy, Carande, Hamilton, Cohn 2001, Ágoston vb. yalnızca araştırma dosyalarında *öneri* ya da dolaylı atıf olarak geçiyor).
- Dolayısıyla **CONFIRMED = 'araştırma dosyasında doğrulanmış'** demektir, 'birincil kaynağa kadar doğrulandı' demek değildir. Kaynakların büyük kısmı Wikipedia, Britannica, EBSCO, TDV İA gibi ikincil/ansiklopedik kaynaklardır.
- Bu oturumdaki ek arama (§7) de özet düzeyindedir. 'DOĞRULANDI' = en az iki ayrı arama sonucu özetinde uyumlu; 'KISMEN' = bir kısmı görüldü; 'DOĞRULANAMADI' = özetlerde çıkmadı (yanlış olduğu anlamına gelmez).
- A1 ile A4 arasında çelişki var: seçim masrafı 850.000 florin A1 #12'de NİTELİKLİ (aralık 825-852 bin), A4 #12'de CONFIRMED. Bu belge A1'in temkinli sınıfını esas aldı.
- A2 başlığındaki 'TAHMİN' notları (Interim 15 Mayıs 1548; Innsbruck 19-20 Mayıs 1552; Passau 2 Ağustos 1552; Trento 13 Aralık 1545) hafıza tahminidir; videoda yalnız Innsbruck geçiyor (H21).

## 4. Sayım özeti

| Sınıf | Cümle | Oran |
|---|---:|---:|
| CONFIRMED | 87 | %50,0 |
| NİTELİKLİ | 40 | %23,0 |
| RİVAYET | 3 | %1,7 |
| YORUM | 25 | %14,4 |
| HAFIZA | 19 | %10,9 |
| **Toplam** | **174** | %100 |

`+Hn` işaretli (ana iddiası kaynaklı ama küçük ayrıntısı HAFIZA) cümle sayısı: **21**. Bir ya da daha çok HAFIZA bileşeni olan toplam cümle: **40**.

**Bölüm bazında dağılım**

| Bölüm | Cümle | CONFIRMED | NİTELİKLİ | RİVAYET | YORUM | HAFIZA | +Hn |
|---|---:|---:|---:|---:|---:|---:|---:|
| c0 Brüksel, 25 Ekim 1555 | 12 | 4 | 2 | 0 | 5 | 1 | 0 |
| c1 Dört Tahtın Çocuğu | 16 | 9 | 4 | 1 | 1 | 1 | 3 |
| c2 Taç Satılık | 14 | 7 | 5 | 1 | 0 | 1 | 3 |
| c3 Şehirlerin İsyanı | 9 | 5 | 1 | 0 | 1 | 2 | 1 |
| c4 Worms'ta Bir Keşiş | 16 | 12 | 1 | 1 | 1 | 1 | 2 |
| c5 İmparator Hep Başka Yerde | 15 | 3 | 3 | 0 | 0 | 9 | 0 |
| c6 Kral, Esir, Düello | 14 | 8 | 2 | 0 | 3 | 1 | 2 |
| c7 Sultan: Hiç Karşılaşmadılar | 15 | 9 | 6 | 0 | 0 | 0 | 0 |
| c8 Akdeniz'de Barbaros | 11 | 6 | 2 | 0 | 1 | 2 | 1 |
| c9 Yeni Dünya: Altın, Gümüş ve Vicdan | 14 | 11 | 3 | 0 | 0 | 0 | 2 |
| c10 Faturayı Kim Ödedi? | 9 | 3 | 3 | 0 | 3 | 0 | 0 |
| c11 Adamın Kendisi | 9 | 2 | 4 | 0 | 3 | 0 | 3 |
| c12 Bırakmak | 10 | 6 | 4 | 0 | 0 | 0 | 2 |
| c13 Hesap | 10 | 2 | 0 | 0 | 7 | 1 | 2 |

**Doğrulama bekleyenler (§7):** 39 madde; öncelik-1: 5, öncelik-2: 17, öncelik-3 (düşük): 17. Bu oturumdaki arama sonucu: DOĞRULANDI 20, KISMEN 9, DOĞRULANAMADI 2, ARANMADI 8.

RİVAYET çerçevesi toplam 5 cümlede kullanılıyor: c1s11, c2s14, c4s7 (sınıf RİVAYET) ve c6s4 ile c12s9 (ikinci yarısı rivayet diye anlatılan, sınıfı NİTELİKLİ olan cümleler).

**ANEKDOT uyumu:** araştırmadaki 9 ANEKDOT satırından 4'ü videoda var ve dördü de 'rivayet' diliyle anlatılıyor; 5'i hiç kullanılmamış (Ek A). **'Yaygın yanlış' denetimi:** araştırma dosyalarında sayılan 37 yaygın yanlıştan hiçbiri videoda yinelenmiyor (Ek B). Bu belgenin bulduğu yeni sorunlar araştırma dosyalarının öngörmediği yerlerde: c6s10 (hala/teyze), c2s9 (Cohn parafrazı), c0s4 (baston).

## 5. Riskli cümleler (kaynaksız / zayıf / kaynaktan güçlü ifade)

Seviye anlamı: **KRİTİK** = kesin olgusal hata, düzeltmeden yayınlama; **YÜKSEK** = kaynaksız ve doğrulanamadı ya da kaynakla uyuşmuyor, doğrula ya da yumuşat; **ORTA** = kaynaksız ama arama özetiyle doğrulandı (sayfa düzeyinde bir kez teyit edin) ya da ifade kaynaktan güçlü; **DÜŞÜK** = tek/popüler kaynak, küçük ifade iyileştirmesi. `Yumuşatma / düzeltme önerisi` sütunu `script.py` için yeni gösterim metnidir; **dosya değiştirilmedi**. `Ses` sütunu, metin değişirse yeniden üretilecek bölümü gösterir.

Toplam işaretli cümle: 38 (KRİTİK 1, YÜKSEK 4, ORTA 19, DÜŞÜK 14); ayrıca c5 zinciri tek grup olarak aşağıda.

| Seviye | Cümle | Mevcut metin | Sorun | Yumuşatma / düzeltme önerisi | Ses |
|---|---|---|---|---|---|
| **KRİTİK** | c6s10 · 10:05 | Çoğu tarihçiye göre bunun uzak bir sonucu İngiltere'de görüldü: papa, imparatorun halası Aragonlu Catherine'in boşanmasını onaylayamadı. Henry, Roma'dan koptu. | Akrabalık yanlış: Catherine = annesinin kız kardeşi = TEYZE. (Hala = babanın kız kardeşi; Margaret için c6s12'de doğru kullanılmış.) Zincir ve 'çoğu tarihçi' kaynaksız. | Sıkça anlatıldığına göre bunun uzak bir sonucu İngiltere'de görüldü: papa, imparatorun teyzesi Aragonlu Catherine'in boşanmasını onaylayamadı. Henry, Roma'dan koptu. | c6 |
| **YÜKSEK** | c0s4 · 00:11 | Bir elinde baston, öbür kolu genç bir prensin omzunda. | Bastonun kaynağı yok; web özetinde de çıkmadı. Açılış sahnesi videonun en görünür cümlelerinden biri. | Kolunu genç bir prensin omzuna dayamış. | c0 (46,5 sn) |
| **YÜKSEK** | c2s9 · 03:31 | Bazı tarihçilere göre seçmenler iki taraftan da parayı aldı, sonra kendilerine en uygun adayı seçti. | Parafraz kaynağın tezini değiştiriyor (Almanya için en iyisi → kendilerine en uygun); 'iki taraftan' kaynaksız. | Bazı tarihçilere göre seçmenler parayı aldı, ama kararı yine de Almanya için en iyi saydıkları yönde verdi. | c2 |
| **YÜKSEK** | c5s12 · 08:33 | Hasta imparator, bir gece Innsbruck'tan sedyeyle kaçmak zorunda kaldı. | 'Sedyeyle' ayrıntısı kaynaksız ve web özetinde doğrulanamadı; ses de belirsiz ('Sedia'yla'). | Hasta imparator, bir gece Innsbruck'tan kaçmak zorunda kaldı. | c5 |
| **YÜKSEK** | c13s5 · 20:09 | Birçok tarihçi, Avrupa'nın tek imparatorluk yerine birbirini dengeleyen devletlerden oluşmasını da bu başarısızlığa bağlar. | Nicelik belirten atıf ('birçok tarihçi') kaynaksız; araştırma açıkça 'kaynaklanamadı' diyor. | Sonuçta Avrupa, tek imparatorluk yerine birbirini dengeleyen devletlerden oluşan bir yapıya doğru gitti. | c13 |
| **ORTA** | c0s11 · 00:38 | İlk kanıt, taç daha takılmadan ortaya çıkıyor: o taç, borçla alındı. | Gövdedeki hedge ile çelişen kesin nedensellik ('borçla alındı'). | İlk kanıt, taç daha takılmadan ortaya çıkıyor: o taç, büyük ölçüde borçla finanse edildi. | c0 |
| **ORTA** | c1s4 · 01:12 | O doğduğunda İspanya tahtı çok uzaktı. Beş ay sonra, kuzeni olan küçük bir bebek öldü ve yol açıldı. | Araştırma dosyalarında yok; tarih doğru ama 'bebek' sözcüğü ~22 aylık çocuk için gevşek. | O doğduğunda İspanya tahtı çok uzaktı. Beş ay sonra, henüz iki yaşına basmamış kuzeni öldü ve yol açıldı. | c1 (116,9 sn) |
| **ORTA** | c3s2 · 04:23 | Kastilya şehirleri bunu ihanet saydı. Yabancı danışmanlara ve vergilere öfkeliydiler. | Neden cümlesi kaynaksız; 'ihanet saydı' yorum. (c3s1 ile birlikte okuyun) | Bu ayrılış, yabancı danışmanlara ve vergilere öfkeli Kastilya şehirlerinde tepkiyle karşılandı. | c3 |
| **ORTA** | c5s10 · 08:18 | Tiziano o anı resmetti: zırhlı imparator, atının üstünde, tek başına. | 'O anı resmetti' fazla kesin: eser zaferden bir yıl sonra, siparişle yapılmış simgesel bir portre. | Tiziano, bir yıl sonra imparatoru o zaferin simgesi olarak resmetti: zırhlı, atının üstünde, tek başına. | c5 |
| **ORTA** | c6s3 · 09:12 | 24 Şubat 1525'te, Pavia'da, François ordusuyla birlikte esir düştü. | Ordu esir düşmedi; bozguna uğradı ('virtually annihilated'). | 24 Şubat 1525'te, Pavia'da, Fransız ordusu yok edildi; François esir düştü. | c6 |
| **ORTA** | c6s4 · 09:18 | Annesine yazdığı mektupta, “bana şeref ve canım kaldı” diyordu. Meşhur “şeref dışında her şey kayıp” sözü, sonradan yaygınlaştı. | Mektup alıntısı tek kaynakta, el yazması görülmedi; kesin kipte. | Annesine yazdığı mektupta, aktarıldığına göre, “bana şeref ve canım kaldı” diyordu. Meşhur “şeref dışında her şey kayıp” sözü ise sonradan yaygınlaştı. | c6 |
| **ORTA** | c7s11 · 12:01 | Yolda küçük bir kale, Güns, yedi sekiz yüz kişiyle orduyu yirmi beş gün oyaladı. | 'Yedi sekiz yüz' kulaktan '7.800' gibi anlaşılabiliyor (Whisper öyle yazdı). | Yolda küçük bir kale, Güns, yedi yüz ile sekiz yüz arası bir garnizonla orduyu yirmi beş gün oyaladı. | c7 |
| **ORTA** | c8s5 · 13:08 | Hıristiyan Avrupa bunu büyük bir zafer olarak kutladı. | 'Hıristiyan Avrupa' genellemesi kaynaksız. | Habsburg çevresinde bu büyük bir zafer olarak kutlandı. | c8 (70,7 sn) |
| **ORTA** | c8s8 · 13:27 | Sonraki otuz yıl boyunca, Akdeniz'in doğusunda Osmanlı donanması üstün kaldı. | 'Otuz yıl' sayısı kaynaksız; Preveze'nin sonucu tartışmalı. | Sonraki yıllarda Akdeniz'in doğusunda Osmanlı donanması üstün kaldı. | c8 |
| **ORTA** | c11s7 · 17:33 | Gut hastalığı onu yatağa bağladı. Doktorlar perhiz önerdi; yemeği bol severdi diye yazılır. | 'Yatağa bağladı' abartı olabilir; kaynak 'günlük işleri yönetemez' diyor. | Gut atakları onu çoğu zaman hareketsiz bıraktı. Doktorlar perhiz önerdi; yemeği bol severdi diye yazılır. | c11 |
| **ORTA** | c13s3 · 19:50 | Şarlken ölünce Habsburg hanedanı ikiye ayrıldı: İspanya kolu oğlu Felipe'ye, Avusturya kolu kardeşi Ferdinand'a. | Bölünme ölümle değil, 1556-58 feragatleriyle gerçekleşti. | Şarlken'in bıraktıklarıyla Habsburg hanedanı iki kola ayrıldı: İspanya kolu oğlu Felipe'ye, Avusturya kolu kardeşi Ferdinand'a. | c13 (80,2 sn) |
| **ORTA** | c13s6 · 20:18 | Ama onun döneminde dünya küçüldü: ilk dünya turu tamamlandı, Atlantik bir ticaret yolu oldu, sömürgeciliğin ahlâkı üzerine ilk büyük tartışma yapıldı. | 'İlk' üstünlüğü (Montesinos 1511 öncül). | …sömürgeciliğin ahlâkı üzerine en bilinen büyük tartışma yapıldı. | c13 |
| **DÜŞÜK** | c0s5 · 00:15 | Bu adam, kırk yıldır Avrupa'nın büyük bölümünü yönetiyor. | Retorik abartı: ilk beş yıl yalnız Hollanda'ydı. | Bu adam, kırk yıldır hükmediyor. | c0 |
| **DÜŞÜK** | c1s12 · 02:03 | Oysa bu söz, ilk kez ölümünden kırk üç yıl sonra yazıldı. Ona ait olduğunu gösteren bir belge yok. | Olumsuz/mutlak iddia ('ilk kez', 'belge yok') yalnız arama özetine dayanıyor. | Oysa bu söz, bilinen en eski hâliyle, ölümünden yaklaşık kırk üç yıl sonra yazıya geçti. Ona ait olduğunu gösteren bir belge bilinmiyor. | c1 |
| **DÜŞÜK** | c1s13 · 02:11 | 1516'da dedesi, Aragonlu Fernando öldü. Şarlken, tutsak annesiyle birlikte, Kastilya ve Aragon'un kralı oldu. | 'Tutsak' yüklü sözcük: c1s9'da delilik/siyaset tartışması var, c12s2'de 'tutsaklık' tekrar ediyor. | Şarlken, kapatılmış annesiyle birlikte, Kastilya ve Aragon'un kralı oldu. | c1 |
| **DÜŞÜK** | c2s7 · 03:17 | Bunun üçte ikisine yakını, 543.000 florin, Augsburglu bankacı Jakob Fugger'den geldi. | Aralıklı rakam (500-550 bin) tam sayı gibi söylenmiş. | Bunun üçte ikisine yakını, yaklaşık 543 bin florin, Augsburglu bankacı Jakob Fugger'den geldi. | c2 (86,6 sn) |
| **DÜŞÜK** | c5s3 · 07:19 | O yokken Luther'in fikirleri yayıldı. 1524'te başlayan Köylü Savaşı'nda yetmiş ile yüz bin kişi öldü. | Köylü Savaşı'nı Luther'in fikirlerine bağlıyor gibi okunabilir; A2 #11: Luther isyana karşıydı. | O yokken Luther'in fikirleri yayıldı. 1524'te başlayan Köylü Savaşı'nı Luther istememişti; yetmiş ile yüz bin kişi öldü. | c5 |
| **DÜŞÜK** | c6s1 · 08:56 | Şarlken'in en uzun soluklu düşmanı, Fransa Kralı I. François'ydı. | Üstünlük iddiası öznel. | Şarlken'in en kalıcı düşmanlarından biri, Fransa Kralı I. François'ydı. | c6 (115,0 sn) |
| **DÜŞÜK** | c7s7 · 11:33 | Osmanlı ordusu, modern tahminlere göre, yetmiş beş ile yüz bin arasındaydı. | Üst sınır Britannica'da '>100 bin'. | Osmanlı ordusu, modern tahminlere göre, yetmiş beş bin ile yüz bin, hatta biraz fazlası arasındaydı. | c7 (105,1 sn) |
| **DÜŞÜK** | c8s9 · 13:33 | 1541'de Şarlken, Cezayir'e çıktı: beş yüz yelkenli, yaklaşık yirmi dört bin asker. | Gemi sayısı hedge'siz; kaynaklar 300-500 arası. | 1541'de Şarlken, Cezayir'e çıktı: beş yüz kadar yelkenli, yaklaşık yirmi dört bin asker. | c8 |
| **DÜŞÜK** | c8s11 · 13:47 | Meksika'nın fatihi Hernán Cortés de oradaydı. Savaş konseyine çağrılmadı. | Kaynak Cortés'e yakın (Gómara). | Meksika'nın fatihi Hernán Cortés de oradaydı; savaş konseyine çağrılmadığı anlatılır. | c8 |
| **DÜŞÜK** | c9s10 · 15:02 | 1550'de, Valladolid'de, imparator fetihleri durdurdu ve iki adamı karşı karşıya getirdi: Sepúlveda ve Las Casas. | 'Askıya aldı' → 'durdurdu' kesinleşmiş. | 1550'de, Valladolid'de, imparator fetihleri geçici olarak durdurdu ve iki adamı karşı karşıya getirdi: Sepúlveda ve Las Casas. | c9 (108,3 sn) |
| **DÜŞÜK** | c10s3 · 15:55 | Şarlken'in otuz beş yıllık olağanüstü gelirlerinin çoğu vergiydi. Alçak Ülkeler on milyonun, Kastilya dokuz milyonun üzerinde katkı yaptı; Napoli beş milyondan fazla. | Birim eksik; 'on milyon ne?' belirsiz. | Alçak Ülkeler on milyon dükatın, Kastilya dokuz milyon dükatın üzerinde katkı yaptı; Napoli beş milyon dükattan fazla. | c10 (63,9 sn) |
| **DÜŞÜK** | c11s5 · 17:20 | 1539'da İsabel, otuz beş yaşında öldü. Şarlken iki ay bir manastıra kapandı, bir daha evlenmedi. | Popüler kaynak, kesin kipte. | 1539'da İsabel, otuz beş yaşında öldü. Şarlken yaklaşık iki ay bir manastıra çekildi, bir daha evlenmedi diye anlatılır. | c11 (63,2 sn) |
| **DÜŞÜK** | c12s1 · 18:00 | Brüksel, 25 Ekim 1555. Öğleden sonra saat üç. | 19. yy anlatısı, kesin saat. | Brüksel, 25 Ekim 1555. Öğleden sonra, saat üç sularında. | c12 (95,3 sn) |
| **DÜŞÜK** | c12s2 · 18:06 | Altı ay önce annesi Juana, kırk altı yıllık tutsaklığın ardından ölmüştü. | 'Tutsaklık' yüklü sözcük (bkz. c1s13). | Altı ay önce annesi Juana, kırk altı yıllık kapatılmanın ardından ölmüştü. | c12 |
| **ORTA** (grup) | c5 zinciri: c5s1 (07:08), c5s7 (07:54), c5s8 (08:00), c5s11 (08:25), c5s13 (08:38), c5s14 (08:46), c5s15 (08:49) | (c5s1, c5s7, c5s8, c5s11, c5s13, c5s14, c5s15) | Araştırma dosyalarında karşılığı olmayan 1521-1555 olay zinciri (dokuz yıl, Şmalkalden Birliği, 1546, Moritz 1552, Augsburg Barışı Eylül 1555, Ferdinand, 'tam bir ay'). Arama özetleriyle doğrulandı; bir kez sayfa düzeyinde teyit edilmeli. | Metin değişikliği gerekmez; yalnız c5s12'deki 'sedyeyle' çıkarılmalı (yukarıda). | c5 yalnız c5s12 için |

**Not (c3s1):** 'Tacı almak için İspanya'dan ayrılması gerekti' aynen kalabilir; asıl yumuşatma c3s2'de.

**Çapraz not (görsel plan):** `YONETMEN_NOTLARI.md` şu çekimleri bu riskli iddialara bağlamış: c0 s4 'baston + genç prensin omzu' (H1), c2 s9 'iki para akımı' (H9), c5 s12 'sedye taşıyan meşaleli kafile' (H21), c6 s10 'ÇOĞU TARİHÇİYE GÖRE' damgası ve zincir (H26). Metinde yumuşatma yapılırsa bu çekimler de aynı kararla güncellenmeli (örn. baston çizilmesin, 'ÇOĞU TARİHÇİYE GÖRE' damgası 'SIKÇA ANLATILIR' olsun).

**Hedge'siz NİTELİKLİ cümleler (17 adet; yumuşatma adayları):** c0s3, c0s11, c1s10, c1s12, c1s16, c2s5, c4s12, c5s2, c6s11, c7s5, c7s14, c7s15, c9s8, c10s5, c11s5, c12s1, c12s3. Bunların çoğunda sorun küçüktür (kaynak kesin bir olguyu söylüyor ama tek/popüler kaynaktır); yukarıdaki tabloda yer alanlar öncelikli.

## 6. Bölüm bölüm denetim tabloları

Sütunlar: cümle kimliği · video zamanı; videoda söylenen iddia (kısa); sınıf; dayanak (araştırma dosyası + satır `#` + kaynak adı; URL'ler en sondaki listede aynı adlarla); metindeki ihtiyat/ifade; not/risk.

### c0 — Brüksel, 25 Ekim 1555 (1555)

*Video: 00:00–00:46 · c0s1–c0s12 · 12 cümle*

| Cümle · süre | Videoda söylenen iddia | Sınıf | Dayanak | İhtiyat/ifade | Not / risk |
|---|---|---|---|---|---|
| c0s1 · 00:00 | Tören günü: 25 Ekim 1555 | CONFIRMED | A5 #16 (Motley/Gutenberg; GHDI) | — | Tarih kesin. O gün yalnız Hollanda devrediliyor (A5 #19); c0s7 'başlıyor' ile uyumlu. |
| c0s2 · 00:03 | Brüksel sarayının büyük salonu, kalabalık | YORUM | A5 #16 (yer: Brüksel sarayı büyük salonu; Genel Devletler toplanmış) | — | Yer doğrulanmış; 'tıklım tıklım dolu' betimleme. |
| c0s3 · 00:07 | 55 yaşında, ayakta güçlükle duran imparator | NİTELİKLİ | A1 #1 (doğum 24.02.1500, yaş hesaplandı); A5 #17 (omza yaslanarak girdi; Motley, 19. yy); A5 #13 (gut) | — | Yaş: 55 yıl 8 ay. 'Ayakta zor duruyor' araştırmadan çıkarım; sahne kaynağı 19. yy anlatısı. |
| c0s4 · 00:11 | Bir elinde baston, öbür kolu genç prensin omzunda | HAFIZA (H1, H2) | A5 #17 yalnız 'omzuna yaslanarak girdi' (NİTELİKLİ); 'baston' araştırmada YOK | — | Baston H1: bu oturumdaki aramada doğrulanamadı (Motley'de yalnız omuz). 'Genç prens' = Willem, 22 yaşında (H2). **[Risk: YÜKSEK]** |
| c0s5 · 00:15 | Kırk yıldır Avrupa'nın büyük bölümünü yönetiyor | YORUM | A5 #16 (tam 40 yıl önce, 15 yaşında devraldım); A1 #6 (Ocak 1515, NİTELİKLİ) | — | 40 yıl konuşmadan. Ama 'Avrupa'nın büyük bölümü' 40 yıl boyunca değil, yaklaşık 1519-20'den beri. **[Risk: DÜŞÜK]** |
| c0s6 · 00:19 | Yeni Dünya fetihleri onun (Kastilya Kralı) adına | CONFIRMED | A4 #2 (Cartas de relación Charles'a); A4 #5 (Capitulación de Toledo); A1 #2 (Isabella: Kastilya + Batı Hint Adaları) | — | 'Adına' = Kastilya Tacı adına; girişimlerin çoğu özel (A4 #1: Cortés Velázquez'in izni olmadan çıktı). |
| c0s7 · 00:23 | Feragat bugün başlıyor | CONFIRMED | A5 #19 (Hollanda 25 Eki 1555; İspanya 16 Oca 1556; imparatorluk 1556-58); A5 'yaygın yanlışlar' | 'başlıyor' | 'Hepsini bıraktı' denmediği için doğru. Ayrıntı c12s5'te. |
| c0s8 · 00:26 | Kimse onu tahttan indirmedi (gönüllü feragat) | CONFIRMED | A5 #16; A5 #18 (gut/yorgunluk; evrensel imparatorluğun uygulanamazlığı) | — | Hukuken gönüllü. Baskı etkenleri (A5 #18: Protestan-Osmanlı-Fransa) bu cümlede yok. |
| c0s9 · 00:28 | Retorik soru | YORUM | — | — |  |
| c0s10 · 00:29 | Beş cephe: bankacı, keşiş, kral, sultan, miras | YORUM | — (anlatı çerçevesi; A5 #18 nedenleriyle gevşek uyumlu) | — | Çerçeve yazarın kurgusu; 'tarihçilere göre' denmiyor (doğru). Tarihçilerin saydığı nedenler c12s6'da. |
| c0s11 · 00:38 | Taç borçla alındı | NİTELİKLİ | A1 #12-#14; A4 #12-#13 (seçim masrafı, Fugger payı, 1523 mektubu) | — | Nedensellik kesin söylenmiş; c2s10 ise 'rüşvetin belirleyiciliği tartışmalı' diyor. Soğuk açılış gövdeden daha kesin. **[Risk: ORTA]** |
| c0s12 · 00:44 | Başlık geçişi; 'Şarlken' adı | YORUM | A3 #1 (ad: Kitapyurdu/Parker çevirisi; Selçuk Üniv. tezi; TDV İA İspanya) | — | 'Şarlken' Türkçe tarih yazımında yerleşik (CONFIRMED); Türkçeye giriş yolu bulunamadı. |

### c1 — I. Dört Tahtın Çocuğu (1500–1518)

*Video: 00:49–02:46 · c1s1–c1s16 · 16 cümle*

| Cümle · süre | Videoda söylenen iddia | Sınıf | Dayanak | İhtiyat/ifade | Not / risk |
|---|---|---|---|---|---|
| c1s1 · 00:49 | Doğum: 24 Şubat 1500, Gent | CONFIRMED | A1 #1 (Anne Boleyn Files; WorldHistory.org) | — | 'Flandre' Fransızca yazım; Türkçe yerleşik biçim 'Flandra'. Scribe ve Whisper sesi 'Flandra' çözdü (ekran/kulak farkı). |
| c1s2 · 00:55 | Anne Juana, baba Yakışıklı Filip | CONFIRMED +H3 | A1 #1 (Anne Boleyn Files; WorldHistory.org) | — | Doğum anında Juana henüz kraliçe değildi (26 Kas 1504); cümle kimlik tanımı olarak okunur (H3). |
| c1s3 · 01:02 | Dört büyükanne-büyükbaba, dört miras | CONFIRMED | A1 #1; A1 #2 (WorldHistoryEdu; WesternCiv) | 'bırakacaktı' | Avusturya payı 1521-22'de Ferdinand'a gitti (A1 #19); cümle bunu iddia etmiyor. |
| c1s4 · 01:12 | Beş ay sonra bebek kuzen öldü, yol açıldı (Miguel da Paz) | HAFIZA (H4) | — (araştırmada YOK) | — | H4: Miguel da Paz, 19 Tem 1500, ~22 aylık (web özeti doğruladı). 'Bebek' yerine 'iki yaşına basmamış'. **[Risk: ORTA]** |
| c1s5 · 01:20 | Habsburglar evlilik ve ölümle taht topladı | YORUM | A1 #2 (genel örüntü) | — | Özet. |
| c1s6 · 01:26 | 6 yaşında, babası Burgos'ta aniden öldü | CONFIRMED | A1 #3 (Wikipedia; Royal Collections: 25.09.1506) | — | Yaş hesaplanmış (6 yıl 7 ay). |
| c1s7 · 01:30 | Juana 1509'dan sonra Tordesillas'ta tutuldu | CONFIRMED +H5 | A1 #3; A5 #12 | — | 'Bir sarayda' ayrıntısı araştırmada yok (H5, düşük). |
| c1s8 · 01:36 | 46 yıl; oğlu kapatmayı kaldırmadı | CONFIRMED | A1 #3 (≈46 yıl; Charles hapsi sürdürdü); A5 #12 (12 Nis 1555; tecrit) | 'hiç' (mutlak) | Araştırmayla uyumlu. |
| c1s9 · 01:41 | Delilik mi siyaset mi tartışması | CONFIRMED | A1 #3 notu; A5 #12 notu | 'hâlâ tartışıyor' |  |
| c1s10 · 01:47 | Mechelen'de halasının sarayında büyüdü; ana dili Fransızca | NİTELİKLİ | A1 #4 (Britannica; HNA; Catholic Encyclopedia - Mechelen yılları net değil); A1 #5 (Royal Collections: ilk dil Fransızca) | — | Hala doğru (Margaret = Philip'in kız kardeşi). |
| c1s11 · 01:54 | 'Tanrı'yla İspanyolca...' sözü | RİVAYET | A1 #23 (ANEKDOT; Wikiquote; Oxford Reference; The Low Countries) | 'Rivayete göre' | Doğru çerçeve. |
| c1s12 · 02:03 | Söz ilk kez 43 yıl sonra yazıldı; belge yok | NİTELİKLİ | A1 #23 (ilk kayıt 1601 ≈ ölümünden 43 yıl) | — | 'Belge yok' olumsuz iddia, arama özetine dayanır; 'ilk kez' kesin söylenmiş. **[Risk: DÜŞÜK]** |
| c1s13 · 02:11 | 1516: Fernando öldü; Charles anneyle birlikte kral | CONFIRMED | A1 #7 (23.01.1516, Wikipedia); A1 #8 (13.03.1516 ilan, Boydell - NİTELİKLİ) | — | Tarih verilmiyor; ortak hükümdarlık A1 #8. 'Tutsak' sözcüğü için c1s9 ile gerilim (bkz. §5). **[Risk: DÜŞÜK]** |
| c1s14 · 02:21 | Eylül 1517 fırtına; Santander yerine Tazones | CONFIRMED +H6 | A1 #9 (Turismo Asturias; Council of Europe) | — | 'Balıkçı köyü' araştırmada yok (yalnız 'küçük köy'; H6). A1 #9: iskele olası, kesin değil. |
| c1s15 · 02:33 | 17 yaşında Kastilyacayı iyi konuşamıyordu | NİTELİKLİ | A1 #5 notu (tek popüler kaynak: 'tek kelime İspanyolca bilmiyordu') | 'henüz iyi' | Yumuşatılmış ifade doğru. |
| c1s16 · 02:38 | Valladolid Cortes'i 1518: Kastilyaca öğren, yabancıları gönder | NİTELİKLİ | A1 #10 (Wikipedia/Sauvage; Brainscape; akademik doğrulama yok) | — | 'Kortes' (parlamento) ve 'Kortes' (Cortés) ses olarak aynı; bağlam ayırt ediyor. |

### c2 — II. Taç Satılık (1519–1520)

*Video: 02:49–04:16 · c2s1–c2s14 · 14 cümle*

| Cümle · süre | Videoda söylenen iddia | Sınıf | Dayanak | İhtiyat/ifade | Not / risk |
|---|---|---|---|---|---|
| c2s1 · 02:49 | Maximilian Ocak 1519'da öldü | HAFIZA (H7) | — (araştırmada YOK) | — | H7: 12 Ocak 1519, Wels (web özeti doğruladı). |
| c2s2 · 02:54 | Taç kalıtsal değil; yedi seçmen | CONFIRMED | A1 #11 (DHM; Wikipedia) | — |  |
| c2s3 · 02:59 | Başlıca rakip I. François | CONFIRMED | A1 #11 | — |  |
| c2s4 · 03:02 | Henry VIII adını ortaya attı; sembolik | CONFIRMED | A1 #11 (Henry VIII 'geç, sembolik') | 'daha çok bir gösteriydi' |  |
| c2s5 · 03:09 | Oylar açıkça pazarlık konusuydu | NİTELİKLİ | A1 #14 (Cohn 2001; DHM); A1 #12-#13 | — | 'Açıkça' A1'de yok; makul. |
| c2s6 · 03:12 | Seçim masrafı ≈850.000 florin | NİTELİKLİ | A1 #12 (DHM 850.000; Britannica 852.000; aralık 825-852 bin; uç iddia ~1,5 milyon); A4 #12 (Swiss National Museum; Wikipedia 'Fugger family'; DHM: 851.585) | 'yaklaşık' | Dosyalar arası fark: A1 NİTELİKLİ, A4 CONFIRMED yazıyor. Birim: florin. |
| c2s7 · 03:17 | Fugger payı 543.000 florin (≈üçte iki) | NİTELİKLİ +H8 | A1 #13 (Wikipedia; Britannica; EBSCO - 543-544 bin; 500-550 bin aralığı); A4 #12 (543.385) | 'üçte ikisine yakını' | 543.000 kesin söylenmiş. 'Augsburglu' araştırmada yok (H8). **[Risk: DÜŞÜK]** |
| c2s8 · 03:24 | 28 Haziran 1519 Frankfurt; 7/7 oy | CONFIRMED | A1 #11 (DHM; Wikipedia) | — |  |
| c2s9 · 03:31 | Seçmenler iki taraftan da parayı aldı, kendilerine en uygun adayı seçti | NİTELİKLİ +H9 | A1 #14 (Cohn 2001: parayı alıp 'Almanya için en iyisini' yaptı) | 'Bazı tarihçilere göre' | Metin 'kendilerine en uygun' diyor; araştırma 'Almanya için en iyisi'. 'İki taraftan da' araştırmada yok (H9). **[Risk: YÜKSEK]** |
| c2s10 · 03:38 | Rüşvetin belirleyiciliği tartışmalı; borç gerçekti | NİTELİKLİ | A1 #14; A1 #12-#13; A4 #12-#13 | 'tartışmalı' | İyi hedge. |
| c2s11 · 03:46 | Seçim kapitülasyonu: ayrıcalıklara saygı, konsey | CONFIRMED | A1 #15 (Wikisource; CHI; bpb; 3.07.1519; Reichsregiment) | — | Madde sayısı (34) söylenmiyor. |
| c2s12 · 03:57 | 23 Ekim 1520 Aachen'de taç | CONFIRMED +H10 | A1 #16 (Centre Charlemagne; Wikipedia) | — | 'Şarlman'ın şehri' ayrıntısı araştırmada yok (H10, düşük). Bu taç Alman-Roma Kralı tacı; imparatorluk tacı Bologna 24.02.1530 (A1 #16 notu). |
| c2s13 · 04:02 | Deviz: Plus ultra | CONFIRMED | A1 #21 (Wikipedia; Boydell) | — | Özgün biçim Fransızca 'Plus oultre' (1516); Latince biçim sonradan (A1 #21). |
| c2s14 · 04:06 | Herkül Sütunları yazısı; deviz 'non'u atıyor | RİVAYET | A1 #21 ('non plus ultra'dan 'non' atılmış) | 'Rivayete göre' | Sütunlardaki yazı efsane; devizin tersine çevrilmesi A1 #21'de CONFIRMED. |

### c3 — III. Şehirlerin İsyanı (1520–1522)

*Video: 04:19–05:08 · c3s1–c3s9 · 9 cümle*

| Cümle · süre | Videoda söylenen iddia | Sınıf | Dayanak | İhtiyat/ifade | Not / risk |
|---|---|---|---|---|---|
| c3s1 · 04:19 | Tacı almak için İspanya'dan ayrılması gerekti | HAFIZA (H11) | — (araştırmada YOK) | — | H11: Mayıs 1520, Cortes'in vergi oyundan sonra (web: sıra doğrulandı, tam gün doğrulanamadı). |
| c3s2 · 04:23 | Şehirler ihanet saydı; yabancı danışman ve vergi öfkesi | HAFIZA (H11) | A1 #10 (yabancıların uzaklaştırılması; 600.000 dukat servicio) kısmen | 'ihanet saydı' (yorum) | Yabancı danışman öfkesi A1 #10'da; 'vergi' ve 'ihanet algısı' yok (H11). **[Risk: ORTA]** |
| c3s3 · 04:29 | 1520 Komünero İsyanı | CONFIRMED | A1 #17 (Wikipedia; Univ. of Valladolid) | — |  |
| c3s4 · 04:33 | 23 Nisan 1521 Villalar | CONFIRMED | A1 #17 | — |  |
| c3s5 · 04:39 | Ertesi gün üç önder idam | CONFIRMED | A1 #17 (Padilla-Bravo-Maldonado) | — |  |
| c3s6 · 04:45 | Toledo'da María Pacheco direndi | CONFIRMED +H12 | A1 #17 | 'aylarca' | 'Padilla'nın dul eşi' ilişkisi araştırmada yok (H12). |
| c3s7 · 04:51 | Valensiya Germanía isyanı | NİTELİKLİ | A1 #18 (Wikipedia; yıllar kaynağa göre değişir 1519-1523) | 'Aynı yıllarda' |  |
| c3s8 · 04:57 | Castilla y León bayramı = Villalar yıldönümü | CONFIRMED | A1 #17 notu; A1 canlı detay #4 | — |  |
| c3s9 · 05:04 | 'İlk ders' sonucu | YORUM | — | — |  |

### c4 — IV. Worms'ta Bir Keşiş (1517–1522)

*Video: 05:11–07:05 · c4s1–c4s16 · 16 cümle*

| Cümle · süre | Videoda söylenen iddia | Sınıf | Dayanak | İhtiyat/ifade | Not / risk |
|---|---|---|---|---|---|
| c4s1 · 05:11 | Nisan 1521, Worms | CONFIRMED | A2 #2 (17-18 Nisan 1521) | — |  |
| c4s2 · 05:15 | 21 yaşındaki imparator; keşiş Luther | CONFIRMED | A1 #1 (doğum); A2 #5 ('keşiş': çeviriler monk/friar diye ayrışıyor) | — | Yaş: 21 yıl 2 ay. |
| c4s3 · 05:22 | 95 madde; matbaa Almanya'ya yaydı | HAFIZA (H13) | — (A2 tablosunda YOK) | 'kısa sürede' | H13: 1517 (web: doğrulandı; yayılma hızı kaynağa göre iki hafta-iki ay). |
| c4s4 · 05:32 | 21 gün güvenli geçiş | CONFIRMED | A2 #1 (k-state.edu; Catholic Textbook Project) | — |  |
| c4s5 · 05:37 | Kitapları sordular | CONFIRMED +H14 | A2 #2; A2 #3 (soran: Trier yetkilisi, adı verilmemiş) | — | 'Önüne koydular' ayrıntısı araştırmada yok (H14, düşük). |
| c4s6 · 05:44 | Bir gün süre; Almanca, sonra Latince | CONFIRMED | A2 #2 (worldhistory.org; Lutheran Quarterly) | — |  |
| c4s7 · 05:52 | 'Hier stehe ich' büyük ihtimalle söylenmedi | RİVAYET | A2 #4 (ANEKDOT; Christianity Today; Lutheran Quarterly/Young 2022) | 'büyük ihtimalle' | Doğru çerçeve. |
| c4s8 · 06:03 | Ertesi sabah yazılı bildiri okundu | CONFIRMED | A2 #5 (19 Nisan 1521 08:00; CHI; GHDI); A2 #6 (dil/okuyan belirsiz) | — | Dil belirtilmiyor (doğru). |
| c4s9 · 06:07 | Atalarını saydı | CONFIRMED | A2 #5 | — | Çeviri adı verilmeli (A2 notu). |
| c4s10 · 06:16 | Tek keşiş bin yıllık Hıristiyanlığa karşı yanılıyor olmalı | CONFIRMED | A2 #5 | — | Çeviriye bağlı ('monk/friar'). |
| c4s11 · 06:22 | Krallıklar, dostlar, beden, kan, can, ruh | CONFIRMED | A2 #5 | — | Kelimesi kelimesine alıntı değil, çeviri. |
| c4s12 · 06:31 | Ferman Luther ayrıldıktan sonra imzalandı, geriye dönük tarihli | NİTELİKLİ | A2 #8 (Schaff; Presbyterian Mission; Lutheran Sentinel - metin 8 Mayıs, imza 25/26 Mayıs) | — | Gün verilmediği için 25/26 farkı etkisiz. |
| c4s13 · 06:38 | Kanun dışı; yazıları yasak | CONFIRMED | A2 #9 (NWE; Berkley Center; EBSCO) | — |  |
| c4s14 · 06:44 | Dönüşte 'kaçırıldı' (Saksonya Seçmeni'nin adamları) | CONFIRMED | A2 #10 (4 Mayıs 1521; Ligonier; Lutheran Reformation) | tırnaklı “kaçırıldı” |  |
| c4s15 · 06:52 | Wartburg, sakal, 'Şövalye Jörg'; Yeni Ahit çevirisi | CONFIRMED +H15 | A2 #10 (Junker Jörg; sakal; Mart 1522'ye dek) | — | Yeni Ahit çevirisi araştırmada yok (H15). Ses: Scribe/Whisper 'York/Yörk' duydu. 'Şövalye' = Junker (genç soylu). |
| c4s16 · 07:01 | Ferman yazdırıldı ama fikir durdurulamadı | YORUM | A2 #9 ('hiç tam uygulanmadı'); A2 #8 | — | Özet. |

### c5 — V. İmparator Hep Başka Yerde (1521–1555)

*Video: 07:08–08:52 · c5s1–c5s15 · 15 cümle*

| Cümle · süre | Videoda söylenen iddia | Sınıf | Dayanak | İhtiyat/ifade | Not / risk |
|---|---|---|---|---|---|
| c5s1 · 07:08 | Worms sonrası Almanya'dan ayrıldı; dokuz yıl dönemedi | HAFIZA (H16) | A2 #15 yalnız 'Almanya'dan uzun yokluk' | — | H16: 1521-1530 (web: 'after nine years' absence'; Augsburg'a giriş 15 Haziran 1530). **[Risk: ORTA]** |
| c5s2 · 07:14 | İspanya karışık, Fransa saldırıyor, Osmanlı | NİTELİKLİ | A2 #15 (biblicaltraining.org; ellopos) | — | Popüler/eğitim kaynakları. |
| c5s3 · 07:19 | Luther'in fikirleri yayıldı; Köylü Savaşı 70-100 bin ölü | NİTELİKLİ | A2 #11 (worldhistory.org; NWE; 1517.org) | 'yetmiş ile yüz bin' | Luther isyana karşıydı (A2 #11); cümle sıralaması nedensellik ima edebilir. **[Risk: DÜŞÜK]** |
| c5s4 · 07:28 | Speyer 1529: Worms Fermanı yeniden yürürlüğe | CONFIRMED | A2 #9; A2 #13 (CHI; PRCA) | — |  |
| c5s5 · 07:35 | Birkaç prens + 14 şehir protesto; 'Protestan' adı | NİTELİKLİ | A2 #13 (5-6 prens + 14 şehir - NİTELİKLİ; ad kökeni ortak) | 'Birkaç prens' | 14 şehir kesin söylenmiş. |
| c5s6 · 07:43 | 1530 Augsburg İtirafı; ana yazar Melanchthon | CONFIRMED | A2 #14 (Wikipedia; Schaff; ELS - 25 Haziran 1530) | — |  |
| c5s7 · 07:54 | Dinledi ama kabul etmedi; Şmalkalden Birliği kuruldu | HAFIZA (H17) | A2 #14 (okundu) kısmen; A2 başlık notu: Birlik 'aranamadı' | — | H17: Confutatio 3 Ağu 1530, Birlik Şubat 1531 (web: doğrulandı). **[Risk: ORTA]** |
| c5s8 · 08:00 | 1546'da savaş açabildi (Fransa ve Osmanlı yatışınca) | HAFIZA (H18) | A2 #15 (genel); A5 #7 (Crépy 1544); A3 #18 (1547 ateşkesi) | 'ancak' | H18: 1546 araştırmada yok; web: Britannica Crépy özeti 1545 Osmanlı mütarekesini anıyor. **[Risk: ORTA]** |
| c5s9 · 08:07 | 24 Nisan 1547 Mühlberg; sisli sabah; Saksonya Seçmeni esir | CONFIRMED | A2 #16 (Wikipedia; War History; Nobility.org; bir müze 25 Nisan diyor); A2 #17-#18 (sayılar çelişkili, metin sayı vermiyor) | 'sisli bir sabah' |  |
| c5s10 · 08:18 | Tiziano zırhlı, atlı, tek başına imparatoru resmetti | HAFIZA (H19) | — (araştırmada YOK) | — | H19: 1548, Prado; Mary of Hungary siparişi, Augsburg'da yapıldı (web). 'O anı' = alegorik anma, anlık betimleme değil. **[Risk: ORTA]** |
| c5s11 · 08:25 | 1552'de Saksonyalı Moritz ayaklandı | HAFIZA (H20) | A2 başlık notu: '1552 isyanı' aranamadı (tahmin) | — | H20: Mart-Ağustos 1552 (web: doğrulandı). **[Risk: ORTA]** |
| c5s12 · 08:33 | Hasta imparator bir gece Innsbruck'tan sedyeyle kaçtı | HAFIZA (H21) | A2 başlık notu: 'Innsbruck kaçışı 19-20 Mayıs 1552 gecesi' (tahmin) | — | H21: gece kaçış doğrulandı; 'sedye' doğrulanamadı. Whisper 'Sedia'yla' duydu. **[Risk: YÜKSEK]** |
| c5s13 · 08:38 | Eylül 1555'te Augsburg Barışı; Lutherciliğe yer açıldı | HAFIZA (H22) | A5 #24 (Augsburg Lutherciliği tanıdı) - içerik; tarih araştırmada YOK | — | H22: 25 Eylül 1555 (web: doğrulandı). **[Risk: ORTA]** |
| c5s14 · 08:46 | Barışı Ferdinand yürüttü | HAFIZA (H23) | A2 #12 (1526'da Ferdinand başkan - benzer örüntü) | — | H23: Diet Şubat 1555'te Ferdinand başkanlığında; Şarlken katılmadı (web: doğrulandı). **[Risk: ORTA]** |
| c5s15 · 08:49 | Tam bir ay sonra o salonda | HAFIZA (H24) | A5 #16 (25 Eki 1555); 25 Eylül araştırmada YOK | 'Tam bir ay' | H24: H22'ye bağımlı (25 Eylül → 25 Ekim). **[Risk: ORTA]** |

### c6 — VI. Kral, Esir, Düello (1521–1544)

*Video: 08:55–10:50 · c6s1–c6s14 · 14 cümle*

| Cümle · süre | Videoda söylenen iddia | Sınıf | Dayanak | İhtiyat/ifade | Not / risk |
|---|---|---|---|---|---|
| c6s1 · 08:56 | En uzun soluklu düşman I. François | YORUM | A5 (genel Habsburg-Valois çerçevesi) | 'en uzun soluklu' | Öznel; Süleyman da aday (1526-58). **[Risk: DÜŞÜK]** |
| c6s2 · 09:01 | Fransa Habsburg topraklarıyla kuşatılmıştı | YORUM +H25 | A1 #2 (Burgonya Hollandası + Franche-Comté; Aragon + Napoli) | — | Bileşenler CONFIRMED; 'Burgonya' = Franche-Comté (Dükalık 1477'de Fransa'ya geçmişti; H25). |
| c6s3 · 09:12 | 24 Şubat 1525 Pavia; François esir | CONFIRMED | A5 #1 (Britannica; Herodote.net) | — | 'Ordusuyla birlikte esir düştü' fazla güçlü: ordu esir alınmadı, yok edildi (Britannica özeti). **[Risk: ORTA]** |
| c6s4 · 09:18 | Anneye mektup: 'şeref ve canım kaldı'; slogan sonradan | NİTELİKLİ | A5 #2 (ANEKDOT slogan; mektup alıntısı Herodote.net; el yazması görülmedi) | 'sonradan yaygınlaştı' | Mektup alıntısı tek kaynak; slogan debunk'ı doğru. **[Risk: ORTA]** |
| c6s5 · 09:29 | Madrid antlaşması; iki oğlu rehin | CONFIRMED | A5 #3 (Britannica; 14 Oca 1526) | — |  |
| c6s6 · 09:38 | Serbest kalınca reddetti: esirin sözü geçersiz | CONFIRMED | A5 #3 | — |  |
| c6s7 · 09:44 | 6 Mayıs 1527 Roma | CONFIRMED | A5 #4 (Britannica; EBSCO) | — |  |
| c6s8 · 09:51 | Castel Sant'Angelo; 189 muhafızdan 147 ölü | CONFIRMED | A5 #5 (Britannica 'Swiss Guards'; Wikipedia; Smarthistory) | — | A5 #5 satır sınıfı NİTELİKLİ (6-12 bin ölü tahmini ve 400.000 fidye nedeniyle); 189/147 Britannica kaynaklı. |
| c6s9 · 09:59 | İmparator emir vermemişti; papa aylarca tutsak | CONFIRMED | A5 #4 (Charles emretmedi); A5 #5 (6 Ara 1527'ye dek) | 'aylarca' |  |
| c6s10 · 10:05 | Roma Yağması → papa Catherine'in boşanmasını onaylayamadı → Henry koptu; Catherine 'halası' | HAFIZA (H26) | — (araştırmada YOK) | 'Çoğu tarihçiye göre ... uzak bir sonucu' | KESİN HATA: Aragonlu Catherine imparatorun TEYZESİ (annesi Juana'nın kız kardeşi), halası değil. 'Çoğu tarihçi' kaynaksız. H26. **[Risk: KRİTİK]** |
| c6s11 · 10:19 | 1528 karşılıklı 'yalan' + düello çağrısı, yapılmadı | NİTELİKLİ | A5 #8 (Gutenberg/Guizot; British History Online) | — | Çağrı karşılıklı (A5 'yaygın yanlışlar'). |
| c6s12 · 10:28 | 1529 Cambrai; Hanımlar Barışı | CONFIRMED | A5 #6 (Britannica; EBSCO; 3 Ağu 1529) | — | 'Şarlken'in halası' = Margaret (doğru hala). |
| c6s13 · 10:39 | François iki milyon altın ecü ödedi | CONFIRMED | A5 #6 | — |  |
| c6s14 · 10:44 | Savaş ömrünün sonuna dek kesintilerle sürdü | YORUM +H27 | A5 #7 (Crépy 1544 çöktü - NİTELİKLİ) | 'kesintilerle' | 1551-59 savaşı araştırmada yok (H27; web doğruladı). |

### c7 — VII. Sultan: Hiç Karşılaşmadılar (1526–1547)

*Video: 10:53–12:38 · c7s1–c7s15 · 15 cümle*

| Cümle · süre | Videoda söylenen iddia | Sınıf | Dayanak | İhtiyat/ifade | Not / risk |
|---|---|---|---|---|---|
| c7s1 · 10:54 | Kanuni Sultan Süleyman, doğudaki imparator | CONFIRMED | A3 #20 (Süleyman 1520'den); A3 #2 ('imparator yalnız sultandır' Osmanlı görüşü) | — | 'İmparator' Osmanlı bakışıyla. |
| c7s2 · 10:58 | Aynı yıllarda hüküm; hiç yüz yüze gelmediler | NİTELİKLİ | A3 #20 (Selçuk tezi; Encyclopedia.com; 'doğrudan bulunamadı; 1532 kaynaklarından çıkarım') | 'Bildiğimiz kadarıyla' | İyi hedge. |
| c7s3 · 11:05 | 29 Ağustos 1526 Mohaç; Lajos boğuldu | CONFIRMED | A3 #3 (TDV İA Mohaç; NWE); A1 #20 | — |  |
| c7s4 · 11:14 | Çocuksuz; Ferdinand öne çıktı; soylular ikiye bölündü | CONFIRMED | A3 #3 (1515 çifte evlilik; Zápolya 10.11, Ferdinand 17.12.1526); A1 #20 | — |  |
| c7s5 · 11:23 | Zapolya Osmanlı vasalı oldu | NİTELİKLİ | A3 #4 (Wikipedia 'Siege of Buda (1529)'; TDV İA Macaristan; vasallik şartları bulunamadı) | — |  |
| c7s6 · 11:27 | 1529 Viyana; kuşatma 27 Eylül | CONFIRMED | A3 #5-#6 (Britannica; TDV İA Süleyman I: 27 Eylül'de önüne geldi) | — |  |
| c7s7 · 11:33 | Osmanlı ordusu 75-100 bin | NİTELİKLİ | A3 #5 (Britannica '>100 bin'; modern 75-100 bin; eski kronikler 120-300 bin) | 'modern tahminlere göre ... arasında' | Britannica '>100 bin' üst sınırı aşıyor. **[Risk: DÜŞÜK]** |
| c7s8 · 11:39 | Yağmur, çamur, erken kar; Ekim ortası çekilme | CONFIRMED | A3 #6 (Britannica; TDV İA) | — |  |
| c7s9 · 11:45 | Şarlken o hafta İtalya'da; tacı almaya | CONFIRMED | A3 #7 (Clarke; Wikipedia 'Coronation of Charles V': Bologna 5.11.1529; taç 24.2.1530) | 'o hafta' | A3 açık uç: kuşatma haftalarındaki tam konum bulunamadı; İtalya'da olduğu kesin. |
| c7s10 · 11:51 | 1532 Süleyman; hedef 'İspanya kralı' | CONFIRMED | A3 #8 (TDV İA); A3 #2 (Yelçe, Sabancı Üniv.) | — | A3 #2 satır sınıfı NİTELİKLİ (kançılarya terminolojisi genellemesi); sefer günlüğü alıntısı A3 özetinde 'doğrulanmış' sayılıyor. |
| c7s11 · 12:01 | Güns: 700-800 kişi, 25 gün | CONFIRMED | A3 #8 (Jurišić; 5-30.8.1532; TDV İA; Wikipedia 'Siege of Kőszeg') | 'yedi sekiz yüz' | Ses: 'yedi sekiz yüz' Whisper'da '7800' çözüldü (belirsiz). **[Risk: ORTA]** |
| c7s12 · 12:07 | İmparatorluk ordusu Viyana yakınında bekledi; karşılaşmadılar | CONFIRMED | A3 #8 (Brigittenau); A3 #9 (Charles orduda mıydı? çelişkili) | — | Cümle Charles'ın bizzat orada olduğunu iddia etmiyor (doğru). |
| c7s13 · 12:13 | Osmanlı belgeleri 'İspanya kralı' derdi | NİTELİKLİ | A3 #2 (Yelçe; Wikipedia 'Truce of Constantinople (1533)', 'Peace of Zsitvatorok') | 'genellikle' |  |
| c7s14 · 12:22 | 1547'de 5 yıllık ateşkes; Ferdinand yılda 30.000 altın | NİTELİKLİ | A3 #18 (Wikipedia 'Truce of Adrianople'; Szeged; GHDI) | — | Birim/taraf/imza yeri kaynağa göre değişir; 'haraç/hediye' ayrımı yapılmıyor. |
| c7s15 · 12:30 | Viyana tutuldu, Macaristan kaybedildi; yükü Ferdinand taşıdı | NİTELİKLİ | A3 #19 (Universalis; Britannica); A3 #4; A3 #18 | — | Değerlendirme; adı geçen tarihçi (Parker, Ágoston) bulunamadı. |

### c8 — VIII. Akdeniz'de Barbaros (1534–1541)

*Video: 12:41–13:52 · c8s1–c8s11 · 11 cümle*

| Cümle · süre | Videoda söylenen iddia | Sınıf | Dayanak | İhtiyat/ifade | Not / risk |
|---|---|---|---|---|---|
| c8s1 · 12:42 | Barbaros Hayreddin Paşa, sultanın amirali | CONFIRMED | A3 #12 (TDV İA) | — |  |
| c8s2 · 12:47 | 1534 kaptan-ı derya + Tunus | CONFIRMED | A3 #12 (TDV: 6 Nisan 1534; Tunus günü tutarsız) | — | Yıl tutarlı; gün farkı metni etkilemiyor. |
| c8s3 · 12:53 | 1535: Doria ile bizzat Tunus | CONFIRMED +H28 | A3 #13 (Wikipedia 'Conquest of Tunis (1535)'; War History; TDV İA Halkulvadi) | 'Ertesi yıl' | 'Bizzat' araştırmada açık yazılı değil (H28; web doğruladı). |
| c8s4 · 12:59 | Temmuz 1535 Halkulvadi/Tunus; ~20 bin esir | CONFIRMED | A3 #13 (Goletta 14.7; 16.6-21.7.1535; ~20 bin köle) | 'Yaklaşık' |  |
| c8s5 · 13:08 | Hıristiyan Avrupa zaferi büyük zafer diye kutladı | HAFIZA (H29) | — (araştırmada YOK) | — | H29 (web: kısmen - Sicilya girişleri, Vermeyen halıları). **[Risk: ORTA]** |
| c8s6 · 13:11 | Barbaros hâlâ ortadaydı | YORUM | — | — | Köprü. |
| c8s7 · 13:16 | 28 Eylül 1538 Preveze; birleşik filo geri çekildi | CONFIRMED | A3 #14 (Wikipedia 'Battle of Preveza', 'Holy League (1538)'; TDV İA Barbaros; EBSCO 'büyük ölçüde sonuçsuz') | — | Sonuç yorumları ayrışıyor; 'geri çekildi' nötr. |
| c8s8 · 13:27 | Sonraki otuz yıl Osmanlı deniz üstünlüğü | HAFIZA (H30) | A3 #14 (TDV 'dönüm noktası'); A3 #19 (Preveze/Cezayir Habsburg yenilgisi) | — | H30: 1571 İnebahtı'ya dek (web: kısmen; EBSCO Preveze'yi 'sonuçsuz' sayar). **[Risk: ORTA]** |
| c8s9 · 13:33 | 1541 Cezayir; ~500 yelkenli; ~24 bin asker | NİTELİKLİ | A3 #15 (Wikipedia 'Algiers expedition (1541)'; Academia-Lab; Hispanopedia - >500 yelken/24 bin; diğer: 300 gemi/40 bin) | 'yaklaşık' (asker); gemi sayısı kesin | **[Risk: DÜŞÜK]** |
| c8s10 · 13:40 | Fırtına, barut, ~150 gemi battı | NİTELİKLİ | A3 #15 (24-25 Ekim; ~150 gemi) | 'yaklaşık' |  |
| c8s11 · 13:47 | Cortés oradaydı; savaş konseyine çağrılmadı | CONFIRMED | A3 #16 (Academia-Lab; Molina Villeta/Studia Historica; Gómara taraflı olabilir) | — | Kaynak Gómara hattı; A3 notu taraflılık uyarısı yapıyor. **[Risk: DÜŞÜK]** |

### c9 — IX. Yeni Dünya: Altın, Gümüş ve Vicdan (1519–1552)

*Video: 13:55–15:43 · c9s1–c9s14 · 14 cümle*

| Cümle · süre | Videoda söylenen iddia | Sınıf | Dayanak | İhtiyat/ifade | Not / risk |
|---|---|---|---|---|---|
| c9s1 · 13:55 | Yeni Dünya'yı hiç görmedi; onun adına fethedildi | CONFIRMED +H31 | A4 #2; A4 #5 | — | 'Hiç görmedi' araştırmada yok (H31, çok yüksek güven). |
| c9s2 · 14:01 | 1519 Cortés izinsiz çıktı; 13 Ağustos 1521 Tenochtitlan | CONFIRMED | A4 #1 (Redalyc; NWE) | — |  |
| c9s3 · 14:13 | Cortés'in mektupları savunma metni | CONFIRMED | A4 #2 (EADA; UNAM) | — |  |
| c9s4 · 14:21 | Dürer ≈100.000 florin tahmin etti | NİTELİKLİ | A4 #3 (Archive.org/Saville; tarihler tek kaynak) | 'yaklaşık ... tahmin etti' |  |
| c9s5 · 14:29 | 1532 Cajamarca: Pizarro Atahualpa'yı esir aldı | CONFIRMED | A4 #6 (Biografías y Vidas; History.co.uk - 16 Kasım 1532) | — |  |
| c9s6 · 14:36 | Fidye 1.326.539 peso | CONFIRMED | A4 #7 (PUCP/Jerez, Loredo; WHE) | — | Gümüş kısmı anlatılmıyor. |
| c9s7 · 14:44 | Atahualpa idam edildi | CONFIRMED | A4 #9 (tarih 26 Tem/29 Ağu - NİTELİKLİ) | — | Tarih verilmiyor. |
| c9s8 · 14:47 | Kraliyet payı beşte bir | NİTELİKLİ | A4 #8 (Wikipedia 'Hernando Pizarro'; tek kaynak) | — |  |
| c9s9 · 14:51 | 1542 Yeni Yasalar; vali öldürüldü | CONFIRMED | A4 #20 (Wikipedia 'New Laws'; PUCP) | — | Encomienda kalkmadı (cümle bunu iddia etmiyor). |
| c9s10 · 15:02 | 1550 Valladolid; fetihleri durdurdu; Sepúlveda-Las Casas | CONFIRMED | A4 #21 (Wikipedia 'Valladolid debate'; UNCuyo) | — | Kaynak 'askıya aldı' diyor; metin 'durdurdu'. **[Risk: DÜŞÜK]** |
| c9s11 · 15:12 | Görüşler; resmî kazanan çıkmadı | CONFIRMED +H32 | A4 #21 | — | Görüşlerin içeriği araştırmada yok (H32; web doğruladı). |
| c9s12 · 15:21 | İlk dünya turu onun desteğiyle, bayrağı altında | CONFIRMED | A4 #17 (İspanya Savunma Bak.; CSIC) | — | 'Bu arada': anlatı 1550'den 1519-22'ye dönüyor (kronolojik atlama). |
| c9s13 · 15:27 | Magellan öldü; Elcano; 18 Avrupalı | NİTELİKLİ | A4 #18 (Guinness; Wikipedia 'Victoria (ship)'); A4 #19 | 'on sekiz Avrupalı' | 18/22 çelişkisi; 'Avrupalı' diyerek güvenli. |
| c9s14 · 15:34 | Elcano'ya arma: küre + Primus circumdedisti me | CONFIRMED | A4 #19 (Hispanopedia; Fundación Elkano) | — | 'Primus' iddiası tartışmalı (A4 #19 notu). |

### c10 — X. Faturayı Kim Ödedi? (1519–1557)

*Video: 15:46–16:50 · c10s1–c10s9 · 9 cümle*

| Cümle · süre | Videoda söylenen iddia | Sınıf | Dayanak | İhtiyat/ifade | Not / risk |
|---|---|---|---|---|---|
| c10s1 · 15:47 | Çoğumuz Amerika gümüşünü sayarız | YORUM | A4 'yaygın yanlışlar' (Tracy) | — |  |
| c10s2 · 15:52 | Kayıtlar başka bir şey söylüyor | YORUM | — | — |  |
| c10s3 · 15:55 | Olağanüstü gelirler: AÜ >10 M, Kastilya >9 M, Napoli >5 M | NİTELİKLİ | A4 #16 (H-Net/Tracy kitap eleştirisi: 10,5 / 9,3 / 5,7 M dükat) | 'üzerinde', 'fazla' | Birim (dükat) söylenmiyor; tek kitap eleştirisi. **[Risk: DÜŞÜK]** |
| c10s4 · 16:07 | Potosí 1545; büyük patlama sonra | CONFIRMED | A4 #10 (Encyclopedia.com; WHE); A4 #11 | — | 1545 (bir kaynak 1544). |
| c10s5 · 16:16 | 1523 Fugger mektubu | NİTELİKLİ | A4 #13 (Financial History Magazine); A1 #14 | — | Tarih 'bahar 1523 (tahmin: 24 Nisan)'; özgün metin doğrulanamadı. |
| c10s6 · 16:24 | Mektup tacı kimin parasıyla aldığını hatırlatıyordu | NİTELİKLİ | A4 #13 | 'özetle' | İyi hedge (kelimesi kelimesine değil). |
| c10s7 · 16:29 | Welser'ler Venezuela'da yönetim hakkı | CONFIRMED | A4 #14 (Binghamton Üniv.; Wikipedia 'Klein-Venedig') | — | 'Borç karşılığı' yorumu yapılmıyor (doğru). |
| c10s8 · 16:35 | 1556 borç uçurum; Nisan 1557 Felipe ödemeleri durdurdu | CONFIRMED | A4 #15 (EHR/Álvarez-Nogal-Chamley; Banco de España: 17 Nisan 1557; ≈7,5 M dükat asiento) | 'uçurumdaydı' (yorum) | II. Felipe'ye atfedilmiş (doğru). |
| c10s9 · 16:46 | İmparatorluk borçla ayakta | YORUM | A4 #15-#16 | — |  |

### c11 — XI. Adamın Kendisi (1526–1558)

*Video: 16:53–17:57 · c11s1–c11s9 · 9 cümle*

| Cümle · süre | Videoda söylenen iddia | Sınıf | Dayanak | İhtiyat/ifade | Not / risk |
|---|---|---|---|---|---|
| c11s1 · 16:54 | Retorik soru | YORUM | — | — |  |
| c11s2 · 16:57 | Habsburg çenesi: ağzını kapatamama, çiğneme | NİTELİKLİ | A5 #14 (NBC; Hektoen; Substack); A1 #22 | 'yazılır' |  |
| c11s3 · 17:04 | 2019 çalışması: küçük, kesin değil | CONFIRMED | A1 #22 (Annals of Human Biology; Smithsonian) | 'küçüktü; kesin bir şey söylemiyor' |  |
| c11s4 · 17:15 | 26 yaşında Portekizli kuzeni İsabel'le evlendi | CONFIRMED +H33 | A5 #10 (10/11 Mar 1526; Wikipedia; Galería de las Colecciones Reales) | — | 'Kuzeni' araştırmada yok (H33; web doğruladı). |
| c11s5 · 17:20 | 1539 İsabel öldü; 2 ay manastır; evlenmedi | NİTELİKLİ | A5 #10 (1 May 1539; 35 yaş); A5 #11 (popüler kaynak; akademik teyit yok) | — | 'İki ay' popüler kaynakta. **[Risk: DÜŞÜK]** |
| c11s6 · 17:30 | Ömür boyu siyah giydi | NİTELİKLİ | A5 #11 | 'anlatılır' |  |
| c11s7 · 17:33 | Gut onu yatağa bağladı; perhiz; yemeği bol severdi | NİTELİKLİ +H34 | A5 #13 (NBC; PMC10810993; Hektoen); A5 #14 | 'diye yazılır' | 'Yatağa bağladı' şiddeti araştırmada yok (H34). **[Risk: ORTA]** |
| c11s8 · 17:41 | Bizzat dolaşarak yönetti (ülke listesi) | YORUM +H35 | A4 #23 (seyahat sayıları bulunamadı; hafıza tahmini); A3 #13, #15 (Tunus, Cezayir) | — | Fransa seyahati araştırmada yok (H35). |
| c11s9 · 17:53 | Yollarda taşıdı | YORUM | — | — |  |

### c12 — XII. Bırakmak (1555–1558)

*Video: 18:00–19:35 · c12s1–c12s10 · 10 cümle*

| Cümle · süre | Videoda söylenen iddia | Sınıf | Dayanak | İhtiyat/ifade | Not / risk |
|---|---|---|---|---|---|
| c12s1 · 18:00 | Brüksel, 25 Ekim 1555, saat üç | NİTELİKLİ | A5 #17 (Motley/Gutenberg, 19. yy: saat 15:00); A5 #16 | — | Web: Motley 'as the clock struck three'. **[Risk: DÜŞÜK]** |
| c12s2 · 18:06 | Altı ay önce Juana öldü; 46 yıllık tutsaklık | CONFIRMED | A5 #12 (12 Nis 1555); A1 #3 | — | 'Tutsaklık' sözcüğü c1s9'daki tartışmayla gerilimli. **[Risk: DÜŞÜK]** |
| c12s3 · 18:12 | Genel Devletler; Willem'in omzu; Felipe ve Mary arkada | NİTELİKLİ +H2 | A5 #16-#17 (Motley/Gutenberg) | — | 'Ağlama/Altın Post doğrulanamadı' (A5 #17); anlatılmıyor. Willem'in 'genç' olması H2. |
| c12s4 · 18:25 | 40 yıl önce, 15 yaşında | CONFIRMED | A5 #16 (Motley/GHDI) | — |  |
| c12s5 · 18:32 | Hollanda oğluna; İspanya Ocak 1556; unvan 1556-58 | NİTELİKLİ | A5 #19 (EBSCO; Wikipedia - 25 Eki 1555; 16 Oca 1556; 27 Ağu 1556; 14 Mar 1558; Britannica: unvanı ölümüne dek korudu) | 'ancak 1556 ile 1558 arasında' |  |
| c12s6 · 18:48 | Nedenler: gut/yorgunluk; evrensel imparatorluğun gerçekleşmemesi | CONFIRMED | A5 #18 (Britannica; habsburger.net; Fundación Yuste) | 'Tarihçilerin saydığı' | A5 #18'in üçüncü nedeni (Protestan-Osmanlı-Fransa baskısı) listede yok. |
| c12s7 · 18:57 | Felipe İspanya'yı savaşta ve iflasa yakın devraldı | CONFIRMED | A5 #18 | — |  |
| c12s8 · 19:03 | Eylül 1556 İspanya; Şubat 1557 Yuste | CONFIRMED +H36 | A5 #20 (Britannica; Fundación Yuste - 3 Şub 1557) | — | 'Küçük konut' ayrıntısı araştırmada yok (H36, düşük). |
| c12s9 · 19:14 | Requiem'e katıldı (bir çalışma); tabut yalnızca rivayet | NİTELİKLİ | A5 #22 (Boletín de Arte/UMA - tek akademik özet); A5 #23 (ANEKDOT) | 'Bir çalışma ... yazıyor'; 'yalnızca rivayet' | İyi hedge. |
| c12s10 · 19:25 | 31 Ağustos 1558 ateş; sıtma; 21 Eylül; 58 yaş | CONFIRMED | A5 #21 (Britannica; PMC; NBC); A1 #1 (yaş) | 'Büyük olasılıkla' |  |

### c13 — XIII. Hesap (1558–)

*Video: 19:38–20:58 · c13s1–c13s10 · 10 cümle*

| Cümle · süre | Videoda söylenen iddia | Sınıf | Dayanak | İhtiyat/ifade | Not / risk |
|---|---|---|---|---|---|
| c13s1 · 19:38 | Beşinci cephe: miras | YORUM | — | — |  |
| c13s2 · 19:42 | Dört taht; akrabalık ağı | YORUM | A1 #2 | — |  |
| c13s3 · 19:50 | Habsburg ikiye ayrıldı | CONFIRMED | A5 #24 (Britannica; habsburger.net) | — | 'Ölünce' zamanlaması gevşek: bölünme 1556-58 feragatleriyle (Avusturya payı 1521-22'de, A1 #19). **[Risk: ORTA]** |
| c13s4 · 20:00 | Evrensel imparatorluk gerçekleşmedi; Reform durmadı; Augsburg | CONFIRMED | A5 #24 | — |  |
| c13s5 · 20:09 | Birçok tarihçi: denge devletleri bu başarısızlığa bağlanır | HAFIZA (H37) | A5 #24 notu: 'Tarihçi değerlendirmeleri kaynaklanamadı' | 'Birçok tarihçi' | H37: web de doğrulayamadı. **[Risk: YÜKSEK]** |
| c13s6 · 20:18 | Dünya küçüldü: dünya turu, Atlantik, ilk büyük tartışma | YORUM +H38 | A4 #17-#19, #11, #21 | — | 'İlk büyük tartışma' üstünlük (H38; Wikipedia 'Avrupa'da ilk kamusal tartışma' diyor). **[Risk: ORTA]** |
| c13s7 · 20:30 | Oyunlarda 'kişisel birlik' denir | YORUM +H39 | — | — | Oyun terimi H39 (düşük). |
| c13s8 · 20:41 | Retorik soru | YORUM | — | — |  |
| c13s9 · 20:48 | Etkileşim çağrısı | YORUM | — | — |  |
| c13s10 · 20:54 | Kanal imzası | YORUM | — | — |  |

## 7. Doğrulama bekleyenler (HAFIZA) listesi

Araştırma dosyalarında karşılığı olmayan olgusal iddialar: **39 madde**. Öncelik: **1** = web'de doğrulanamadı ya da kaynakla uyuşmuyor, yayından önce çöz; **2** = sonuç taşıyan olgu, arama özetiyle doğrulandı, sayfa düzeyinde teyit et; **3** = önemsiz ayrıntı. `Güven` = bu belgenin yazarının (model hafızası) kendi güveni. `Web teyidi` = bu oturumda WebSearch özetleri (sayfa açılmadı); URL'ler arama sonuçlarında gerçekten görülenlerdir.

| # | Cümle(ler) | İddia | Tarih / sayı | Güven | Öncelik | Nasıl doğrulanır | Web teyidi (bu oturum, özet düzeyi) |
|---|---|---|---|---|---:|---|---|
| H1 | c0s4 (00:11) | Abdikasyon töreninde imparatorun bir elinde baston tutması | 25 Ekim 1555 | orta | 1 | Motley, The Rise of the Dutch Republic (Project Gutenberg #4803) ve Gachard'ın 'Retraite et mort de Charles-Quint' anlatısında 'baston/asa/koltuk değneği' geçiyor mu bak. | DOĞRULANAMADI: Sahne (büyük salon, saat üç, Willem'in omzuna yaslanma) doğrulandı; baston/sopa hiçbir özette geçmedi. Önerim: 'baston'u çıkar. — https://gutenberg.org/cache/epub/4803/pg4803-images.html; https://www.americanpresbyterianchurch.org/reformation-history/rise-of-the-dutch-republic/advent-of-philip-ii/ |
| H9 | c2s9 (03:31) | Seçmenlerin 'iki taraftan da' para alması (ve 'kendilerine en uygun adayı' seçmeleri) | 1519 | orta | 1 | Cohn (2001, German History 19) makalesinin kendisi; Wikipedia '1519 imperial election'. DİKKAT: A1 #14'e göre tez 'Almanya için en iyisini yaptılar'; metin 'kendilerine en uygun' diyor. | KISMEN: Seçmenlerin (Frederick hariç) iki adaya birden destek sözü verdiği bir kaynakta var; Cohn'un makalesi doğrudan bulunamadı. 'Kendilerine en uygun' ifadesi doğrulanamadı. — https://en.wikipedia.org/wiki/1519_imperial_election; https://www.the-low-countries.com/article/charles-v-the-man-who-bought-the-emperorship/ |
| H21 | c5s12 (08:33) | Hasta imparatorun bir gece Innsbruck'tan sedyeyle kaçması | 19-20 Mayıs 1552 (A2 başlığında 'tahmin') | yüksek (olay); orta (sedye) | 1 | Parker, Emperor (2019) 1552 bölümü; Brandi; 'Innsbruck 1552 Flucht Karl V. Sänfte'. | KISMEN: Gece kaçışı ve Villach'a gidiş doğrulandı; 'sedye/tahtırevan' hiçbir özette geçmedi (bir 19. yy kaynak genel olarak seyahatte sedyeyle taşındığını söylüyor). — https://en.wikipedia.org/wiki/Second_Schmalkaldic_War; https://www.coingallery.de/KarlV/Moritz_E.htm |
| H26 | c6s10 (10:05) | Roma Yağması -> papa imparatorun etkisinde -> Aragonlu Catherine'in boşanması onaylanmadı -> Henry Roma'dan koptu; 'çoğu tarihçiye göre'; Catherine imparatorun TEYZESİ | 1527-1534 | yüksek (zincir); orta ('çoğu tarihçi'); kesin (teyze) | 1 | Britannica 'Clement VII', 'Catherine of Aragon'; Scarisbrick, Henry VIII; Parker, Emperor (2019). | DOĞRULANDI: Catherine = Isabel/Fernando'nun kızı, Juana'nın kız kardeşi = imparatorun teyzesi; Şarlken'in baskısı belirleyici etkenlerden biri; zamanlama kaynaklarda ayrışıyor. — https://newworldencyclopedia.org/entry/Catherine_of_Aragon; https://www.ebsco.com/research-starters/history/clement-vii/; https://blog.nationalarchives.gov.uk/anglo-papal-relations-henry-viii-break-with-rome/; https://blog.oup.com/2012/05/the-sack-of-rome/ |
| H37 | c13s5 (20:09) | 'Birçok tarihçi': Avrupa'nın dengeleyen devletlerden oluşması evrensel monarşinin başarısızlığına bağlanır | - | orta | 1 | Parker, Emperor (2019) sonuç bölümü; Kennedy, Rise and Fall of the Great Powers; Brandi. A5 #24: 'Tarihçi değerlendirmeleri kaynaklanamadı'. | DOĞRULANAMADI: Arama özetleri bu çerçeveyi doğrudan vermedi (genel 'evrensel monarşi başarısız' anlatısı var). — https://www.habsburger.net/en/chapter/charles-v-and-dream-universal-monarchy |
| H4 | c1s4 (01:12) | Beş ay sonra kuzeni küçük bir bebeğin ölümüyle İspanya tahtına yol açıldı (Miguel da Paz) | Miguel d. 23 Ağu 1498, ö. 19 Tem 1500 (~22 aylık); Charles d. 24 Şub 1500 | yüksek | 2 | Real Academia de la Historia (Diccionario Biográfico) maddesi; Britannica 'Charles V'; kuzenlik soy ağacından (Miguel'in annesi Isabel = Juana'nın kız kardeşi). | DOĞRULANDI: Tarih ve yaş doğrulandı; 'kuzen' arama özetinde açık yazılmadı, soy ağacından çıkarım. — https://en.wikipedia.org/wiki/Miguel_da_Paz,_Prince_of_Portugal; https://dbe.rah.es/biografias/miguel-de-la-paz |
| H7 | c2s1 (02:49) | Maximilian'ın ölümü | 12 Ocak 1519 (Wels) | yüksek | 2 | Britannica / Habsburger.net 'Maximilian I'. | DOĞRULANDI: 12 Ocak 1519, Wels; birden çok kaynak uyumlu. — https://en.wikipedia.org/wiki/Maximilian_I,_Holy_Roman_Emperor; https://www.encyclopedia.com/people/history/german-history-biographies/maximilian-i-holy-roman-empire; https://www.habsburger.net/en/persons/habsburg-emperor/maximilian-i-last-knight |
| H11 | c3s1 (04:19), c3s2 (04:23) | Şarlken'in taç için İspanya'dan ayrılması (Cortes'ten vergi alındıktan sonra), şehirlerin tepkisi ('ihanet saydı', vergi öfkesi) | Mayıs 1520 | yüksek (sıra); orta (tam gün, 'ihanet') | 2 | Pérez, Los Comuneros; Haliczer, The Comuneros of Castile (1981); EBSCO 'Comunero Revolt'. | KISMEN: Sıra doğrulandı: Santiago/La Coruña Cortes'i dar çoğunlukla vergi verdi, kral ayrıldı, isyan başladı; isyancılar yabancı yönetimi ve kralın Almanya için İspanya'yı terk etmesini eleştirdi. Tam gün doğrulanamadı; bir kaynak 'Santander' diyor. — https://www.ebsco.com/research-starters/history/comunero-revolt/; https://warhistory.org/de/article/imperial-spain-i |
| H13 | c4s3 (05:22) | 95 Tez: günah affı (endüljans) satışına karşı; matbaanın kısa sürede yayması | 1517 (gelenek: 31 Ekim) | yüksek | 2 | Britannica 'Ninety-five Theses'; Pettegree, Brand Luther (2015). | DOĞRULANDI: Tarih gelenekseldir (31 Ekim 1517); yayılma hızı kaynağa göre iki hafta ile iki ay arası anlatılıyor. — https://en.wikipedia.org/wiki/History_of_Lutheranism; https://faculty.uml.edu/ethan_Spanier/Teaching/documents/21Reformation.pdf |
| H15 | c4s15 (06:52) | Luther'in Wartburg'da Yeni Ahit'i Almancaya çevirmesi | Aralık 1521-Mart 1522 (~11 hafta); basım 20 Eylül 1522 | çok yüksek | 2 | Wartburg-Stiftung; Lutherhaus Eisenach. | DOĞRULANDI: Aralık 1521'de başladı, Mart 1522'de bitti; Eylül Testamenti 20 Eylül 1522. — https://en.wikipedia.org/wiki/Lutherhaus_Eisenach; https://www.ligonier.org/podcasts/5-minutes-in-church-history-with-stephen-nichols/junker-jorg; https://witness.lcms.org/2022/junker-jorge-translates-the-bible/ |
| H16 | c5s1 (07:08) | Şarlken Worms'tan sonra Almanya'dan 'dokuz yıl' uzak kaldı | 1521-1530 (Augsburg'a giriş 15 Haziran 1530) | yüksek | 2 | Britannica 'Charles V' itinerary; Brandi; Parker, Emperor (2019). | DOĞRULANDI: 'Dokuz yıllık yokluktan sonra' ifadesi ve Augsburg'a 15 Haziran 1530 girişi görüldü (eski Protestan tarih kaynakları). — https://www.biblicaltraining.org/library/charles-v; https://ghdi.ghi-dc.org/pdf/eng/Doc.65-ENG-Augsburg-1530_eng.pdf |
| H17 | c5s7 (07:54) | Şarlken'in Augsburg İtirafı'nı kabul etmemesi (Confutatio) ve Şmalkalden Birliği'nin kurulması | Confutatio 3 Ağu 1530; Recess 19 Kas 1530; Birlik Şubat 1531 (27 Şubat) | yüksek | 2 | Britannica 'Schmalkaldic League'; GHDI Doc. 65. | DOĞRULANDI: Üç tarih de arama özetinde görüldü. — https://en.wikipedia.org/wiki/Schmalkaldic_League; https://britannica.com/print/article/527721; https://ghdi.ghi-dc.org/pdf/eng/Doc.65-ENG-Augsburg-1530_eng.pdf; https://www.worldhistory.org/Augsburg_Confession/ |
| H18 | c5s8 (08:00) | Şmalkalden Savaşı'nın 1546'da başlaması; Fransa (Crépy) ve Osmanlı cephesinin yatışması | Crépy 18 Eylül 1544; Osmanlı mütarekesi 1545 (Britannica özeti); savaş 1546-47 | yüksek (1546); orta (yatışma sırası) | 2 | Britannica 'Peace of Crépy', 'Schmalkaldic War'. | DOĞRULANDI: Britannica Crépy özeti 1545 Osmanlı mütarekesini anıyor; başka bir kaynak Edirne ateşkesini 1547'ye koyuyor (A3 #18 ile uyumlu). — https://www.britannica.com/topic/Peace-of-Crepy; https://en.wikipedia.org/wiki/Schmalkaldic_League; https://www.historyofwar.org/articles/wars_fourth_hapsburg_valois.html |
| H19 | c5s10 (08:18) | Tiziano'nun Mühlberg'de atlı Şarlken portresi; 'o anı resmetti' | 1548 (Prado); Mary of Hungary siparişi; Augsburg'da Nisan-Eylül 1548 | yüksek (eser); orta ('o anı') | 2 | Museo del Prado kataloğu 'El emperador Carlos V, a caballo, en Mühlberg'. | DOĞRULANDI: Eser ve tarih doğrulandı; zaferi anan simgesel portre (anlık betimleme değil). — https://en.wikipedia.org/wiki/Equestrian_Portrait_of_Charles_V; https://www.worldhistory.org/image/15184 |
| H20 | c5s11 (08:25) | Saksonyalı Moritz'in 1552'de Şarlken'e karşı ayaklanması | Mart-Ağustos 1552 | yüksek | 2 | Britannica 'Maurice, elector of Saxony'; Wikipedia 'Second Schmalkaldic War'. | DOĞRULANDI: Eski müttefik, 1552 savaşı doğrulandı. — https://en.wikipedia.org/wiki/Second_Schmalkaldic_War; https://www.historyofwar.org/articles/people_saxony_maurice_of.html |
| H22 | c5s13 (08:38) | Augsburg Barışı'nın Eylül 1555'te imzalanması | 25 Eylül 1555 | yüksek | 2 | Britannica 'Peace of Augsburg'; GHDI Doc. 67. | DOĞRULANDI: 25 Eylül 1555 birden çok kaynakta. — https://www.britannica.com/print/article/42767; https://www.ebsco.com/research-starters/history/peace-augsburg/; https://www.catholictextbookproject.com/post/the-imperial-diet-proclaims-the-religious-peace-of-augsburg-september-25-1555; https://germanhistorydocs.ghi-dc.org/pdf/eng/Doc.67-ENG-ReligPeace-1555_en.pdf |
| H23 | c5s14 (08:46) | Barışı Ferdinand'ın yürütmesi, Şarlken'in katılmaması | Diet Şubat 1555'te Ferdinand başkanlığında | yüksek | 2 | Britannica 'Peace of Augsburg'; GHDI Doc. 67. | DOĞRULANDI: Şarlken hastalık ve Hollanda sorunları nedeniyle katılmadı; Ferdinand'a tam yetki verdi; barışı resmen onaylamadı. — https://www.britannica.com/print/article/42767; https://germanhistorydocs.ghi-dc.org/pdf/eng/Doc.67-ENG-ReligPeace-1555_en.pdf |
| H24 | c5s15 (08:49) | 'Tam bir ay sonra' (Augsburg Barışı - abdikasyon) | 25 Eylül → 25 Ekim 1555 | yüksek (H22'ye bağlı) | 2 | H22 doğrulanınca otomatik. | DOĞRULANDI: 25 Eylül ile 25 Ekim tam bir ay. |
| H29 | c8s5 (13:08) | Tunus zaferinin 'Hıristiyan Avrupa'da büyük zafer olarak kutlanması | 1535 | orta-yüksek | 2 | Kunsthistorisches Museum 'Tunis' sergisi; Vermeyen halıları literatürü. | KISMEN: Sicilya'da törenli girişler (Palermo, 13 Eylül 1535) ve 12 halı (1543) kutlamanın somut örnekleri; 'Avrupa çapında' genellemesi hafif destekli. — https://khm.at/en/visit/exhibitions/2015/emperor-charles-v-captures-tunis; https://en.wikipedia.org/wiki/Porta_Nuova_(Palermo) |
| H30 | c8s8 (13:27) | Preveze'den sonra 'otuz yıl' Osmanlı deniz üstünlüğü | 1538-1571 (İnebahtı) | orta | 2 | Wikipedia 'Battle of Preveza'; Guilmartin, Gunpowder and Galleys. | KISMEN: Bir kaynak 1571'e dek 'tartışmasız üstünlük' diyor; başka kaynaklar Preveze'yi 'sonuçsuz' sayıyor. — https://en.wikipedia.org/wiki/Battle_of_Preveza; https://www.ebsco.com/research-starters/history/battle-preveza |
| H34 | c11s7 (17:33) | Gut'un onu 'yatağa bağlaması' (şiddet derecesi) | - | orta | 2 | Frontiers in Medicine 2023 makalesi (A5 #13 ile aynı literatür); Parker, Emperor. | KISMEN: 2023 makalesi atakların günlük işleri yönetemez hale getirdiğini söylüyor; 19. yy kaynak seyahatte sedyeyle taşındığını yazıyor. — https://www.frontiersin.org/journals/medicine/articles/10.3389/fmed.2023.1287041/pdf; https://www.habsburger.net/en/chapter/charles-v-resignation-and-abdication |
| H38 | c13s6 (20:18) | Valladolid'in 'sömürgeciliğin ahlâkı üzerine ilk büyük tartışma' olması | 1550-51 | orta | 2 | Wikipedia 'Valladolid debate'; Montesinos 1511 vaazı literatürü. | KISMEN: Wikipedia 'Avrupa tarihinin ilk kamusal tartışması' diyor; Montesinos'un 1511 vaazı öncül sayılıyor. — https://en.wikipedia.org/wiki/Valladolid_debate |
| H2 | c0s4 (00:11), c12s3 (18:12) | Orange Prensi Willem'in 'genç' olması | d. 24 Nisan 1533 (1555'te 22 yaşında) | yüksek | 3 | Herhangi bir Willem biyografisi (Rijksmuseum, EBSCO, Encyclopedia.com). | DOĞRULANDI: Doğum 24 Nisan 1533; 22 yaşında ordu komutanı. — https://www.ebsco.com/research-starters/history/william-silent; https://www.encyclopedia.com/people/history/benelux-history-biographies/william-silent |
| H3 | c1s2 (00:55) | Annesi 'Kastilya Kraliçesi' Juana (doğum anında henüz kraliçe değildi) | Kraliçelik: 26 Kasım 1504 | yüksek | 3 | Juana I maddesi (Britannica; Galería de las Colecciones Reales). | DOĞRULANDI: Taht 26 Kasım 1504'te annesi Isabel'in ölümüyle geçti. — https://en.wikipedia.org/wiki/Joanna_of_Castile |
| H5 | c1s7 (01:30) | Juana'nın Tordesillas'ta 'bir sarayda' tutulması | 1509-1555 | yüksek | 3 | Tordesillas Real Casa / Santa Clara manastırı kaynakları. | ARANMADI |
| H6 | c1s14 (02:21) | Tazones'un 'küçük bir balıkçı köyü' olması | 19 Eylül 1517 | yüksek | 3 | Turismo Asturias; Tazones belediye sayfası. | KISMEN: İniş 19 Eylül 1517 doğrulandı; yerel turizm sayfası iniş anlatısının bir kısmını 'efsaneye yakın' bulanlar olduğunu belirtiyor; 'balıkçı' nitelemesi limana dair anlatılarda geçiyor. — https://www.turismoasturias.es/en/descubre/fiestas-de-interes-turistico/primer-desembarco-de-carlos-v; https://lospueblosmasbonitosdeespana.org/en/pueblos/tazones/experiencias/carlos-v-el-primer-viaje-del-rey |
| H8 | c2s7 (03:17) | Fugger'in 'Augsburglu' olması | - | yüksek | 3 | Herhangi bir Fugger biyografisi. | ARANMADI |
| H10 | c2s12 (03:57) | Aachen'in 'Şarlman'ın şehri' olması | - | yüksek | 3 | Aachen maddesi (Centre Charlemagne; A1 #16'daki kaynak). | ARANMADI |
| H12 | c3s6 (04:45) | María Pacheco'nun Juan de Padilla'nın eşi (dul) olması | - | çok yüksek | 3 | Herhangi bir Comuneros kaynağı. | ARANMADI |
| H14 | c4s5 (05:37) | Luther'in kitaplarının önüne konulması | 18 Nisan 1521 | yüksek | 3 | A2 #2'deki kaynaklar (worldhistory.org; Lutheran Quarterly). | ARANMADI |
| H25 | c6s2 (09:01) | Burgonya Dükalığı'nın 1477'de Fransa'ya geçmesi; Şarlken'in elindeki 'Burgonya' = Franche-Comté + Hollanda | 1477 (Franche-Comté: 1493 Senlis ile iade) | yüksek | 3 | Wikipedia 'House of Valois-Burgundy'; EBSCO 'Mary of Burgundy'. | DOĞRULANDI: Dükalık Fransa'ya, Hollanda ve diğer topraklar Habsburglara geçti. — https://en.wikipedia.org/wiki/House_of_Valois-Burgundy; https://www.ebsco.com/research-starters/history/mary-burgundy |
| H27 | c6s14 (10:44) | Savaşın II. Henri döneminde 1551-59 sürmesi (Cateau-Cambrésis 1559) | 1551-1559 | yüksek | 3 | Wikipedia 'Italian War of 1551-1559'. | DOĞRULANDI: Barış Philip II ile yapıldı; Şarlken 1558'de öldüğünde savaş sürüyordu. — https://en.wikipedia.org/wiki/Italian_War_of_1551%E2%80%931559; https://en.wikipedia.org/wiki/Treaty_of_Cateau-Cambr%C3%A9sis |
| H28 | c8s3 (12:53) | Şarlken'in Tunus seferine bizzat katılması | Barselona'dan 30 Mayıs 1535 | yüksek | 3 | A3 #13 kaynakları; War History Online. | DOĞRULANDI: Seferi bizzat yönettiği belirtiliyor. — https://warhistory.org/article/amphibious-warfare-i?amp=0; https://www.historynet.com/emperor-vs-pirate-tunis-1535.htm |
| H31 | c9s1 (13:55) | Şarlken'in Amerika'ya hiç gitmemesi | - | çok yüksek | 3 | Herhangi bir biyografi. | ARANMADI |
| H32 | c9s11 (15:12) | Sepúlveda ve Las Casas'ın savunduğu görüşler (doğal kölelik / fetih suçtur) | 1550-1551 | çok yüksek | 3 | Wikipedia 'Valladolid debate'; History Today. | DOĞRULANDI: Sepúlveda Aristoteles'in 'doğal kölelik' fikrine dayandı; Las Casas beş gün yanıt verdi. — https://www.historytoday.com/archive/months-past/valladolid-debate-rights-indigenous-people; https://academic.oup.com/book/46077/chapter/404575095 |
| H33 | c11s4 (17:15) | İsabel'in Şarlken'in kuzeni olması | Evlilik 10/11 Mart 1526 | çok yüksek | 3 | Wikipedia 'Isabella of Portugal'. | DOĞRULANDI: Annesi Maria of Aragon (Juana'nın kız kardeşi): ilk kuzen. — https://en.wikipedia.org/wiki/Isabella_of_Portugal |
| H35 | c11s8 (17:41) | Şarlken'in Fransa'ya yolculukları (1539-40 Paris ziyareti; 1544 seferi) | 1539-1544 | yüksek | 3 | Parker, Emperor (2019) seyahat çizelgesi; A4 #23'ün 'bulunamadı' notu. | ARANMADI |
| H36 | c12s8 (19:03) | Yuste'de manastıra bitişik 'küçük konut' | Şubat 1557 | yüksek | 3 | Fundación Yuste. | ARANMADI |
| H39 | c13s7 (20:30) | Strateji oyunlarında 'kişisel birlik' (personal union) denmesi | - | orta-yüksek | 3 | Paradox Wiki 'Personal union'. | KISMEN: EU4'te 'personal union' mekaniği var; Türkçe terim topluluk forumlarında geçiyor, resmî kaynak bulunamadı. — https://steamcommunity.com/app/236850/discussions/0/619569608569911239?l=turkish |

**Görev tarifindeki örnek listeyle eşleşme:** Maximilian'ın ölümü = H7; Şmalkalden Savaşı 1546 = H18 (Birlik: H17); Innsbruck sedyeyle kaçış = H21; Augsburg Barışı ve Ferdinand = H22-H23; 'dokuz yıl' = H16; Titian = H19; Henry VIII-Catherine-Roma Yağması = H26. **Güns/1532 HAFIZA değildir:** A3 #8 (CONFIRMED) Güns'ü (Jurišić, 700-800 kişi, 25 gün, 5-30.8.1532, Brigittenau) ve A3 #2 Osmanlı sefer günlüğünün 'İspanya kralı' ifadesini zaten içeriyor; c7s10-c7s13 bu yüzden CONFIRMED/NİTELİKLİ.

## Ek A. ANEKDOT uyum denetimi

| Araştırma satırı | Anekdot | Videoda | Cümle | Çerçeve |
|---|---|---|---|---|
| A1 #23 | 'Tanrı'yla İspanyolca, kadınlarla İtalyanca...' | VAR | c1s11-c1s12 | 'Rivayete göre'; ilk kayıt 43 yıl sonra, belge yok (doğru) |
| A1 #24 | 'Güneş batmayan imparatorluk' | YOK | — | — (doğru) |
| A2 #4 | 'Hier stehe ich, ich kann nicht anders' | VAR | c4s7 | 'büyük ihtimalle orada söylenmedi' (doğru) |
| A2 #7 | 'Bu adam beni asla sapkın yapamaz' | YOK | — | — (doğru) |
| A3 #17 | Cortés'in zümrütleri / tavsiyesinin reddi | YOK | — | Araştırma 'Videoya koymayın' diyordu; konmamış (doğru) |
| A4 #22 | 'Güneş batmaz' (Charles/Felipe) | YOK | — | — (doğru) |
| A5 #2 | 'Tout est perdu, fors l'honneur' | VAR | c6s4 | 'sonradan yaygınlaştı' (doğru); anne mektubu alıntısı ayrıca tek kaynak (NİTELİKLİ) |
| A5 #15 | Saat tutkusu / 'iki saati aynı çalıştıramam' | YOK | — | — (doğru) |
| A5 #23 | Tabutuna yatıp cenazesini prova | VAR | c12s9 | 'yalnızca rivayet' (doğru) |

Ayrıca c2s14'teki 'Herkül Sütunları'nda yazı' efsanesi 'Rivayete göre' ile anlatılıyor (araştırmada numaralı ANEKDOT satırı değil; A1 #21 yalnız devizin 'non'u atmasını doğruluyor).

## Ek B. Araştırmadaki 'yaygın yanlış' maddelerine karşı denetim

| Dosya | Yaygın yanlış | Videoda | Cümle |
|---|---|---|---|
| A1 | 543.000 florin Welser'indir | Fugger olarak verilmiş (doğru) | c2s7 |
| A1 | 1519'da taç giydi | Seçim 28.06.1519, taç 23.10.1520 ayrılmış (doğru) | c2s8, c2s12 |
| A1 | Ana dili İspanyolcaydı | Fransızca (doğru) | c1s10 |
| A1 | Frederick tek rüşvet almayan seçmen; seçimi yalnız rüşvet belirledi | Anlatılmıyor; 'belirleyiciliği tartışmalı' | c2s10 |
| A1 | Avusturya toprakları Charles'ta kaldı | İddia edilmiyor (miras kaynağı olarak anılıyor; Avusturya kolu Ferdinand'a) | c1s3, c13s3 |
| A1 | Habsburg çenesi kanıtlanmış gerçek, en ağır Charles V'de | Hedge'li; küçük çalışma vurgusu | c11s2-c11s3 |
| A1 | 'Tanrı'ya İspanyolca' / 'güneş batmaz' belgeli söz | İlki rivayet, ikincisi yok | c1s11-c1s12 |
| A1 | Villalar tüm isyanı bitirdi | Toledo direnişi ve Germanía ayrı anlatılıyor | c3s6-c3s7 |
| A2 | 'Hier stehe ich' kesin söylendi | Büyük ihtimalle söylenmedi | c4s7 |
| A2 | Soruyu Johann Eck sordu | Soranın adı verilmiyor | c4s5 |
| A2 | Ferman duruşmanın hemen ardından çıktı | Luther ayrıldıktan sonra, geriye dönük | c4s12 |
| A2 | Ferman uygulandı | 'fikri durduramadı' | c4s16 |
| A2 | Köylü Savaşı'nda tam 100.000 ölü | 70-100 bin | c5s3 |
| A2 | 'Protestan' adı 1517'de doğdu | 1529 Speyer | c5s4-c5s5 |
| A2 | Augsburg İtirafı'nı Luther yazdı | Ana yazar Melanchthon | c5s6 |
| A2 | Mühlberg'de kesin asker sayıları | Sayı verilmiyor | c5s9 |
| A2 | İspanyollar Elbe'yi yüzdü | 'Elbe nehrini geçti' (yüzme iddiası yok) | c5s9 |
| A3 | Şarlken Viyana önünde Kanuni ile savaştı | 1529'da İtalya'daydı; 1532'de ordular karşılaşmadı | c7s9, c7s12 |
| A3 | Viyana'da 200-300 bin Türk | Modern tahmin 75-100 bin | c7s7 |
| A3 | 1536'da imzalı Fransız kapitülasyonu | Anlatılmıyor | — |
| A3 | Kanuni Charles'a imparator dedi | Tersi anlatılıyor | c7s13 |
| A3 | Cortés zümrütlerini Cezayir'de kaybetti | Yalnız 'konseye çağrılmadı' | c8s11 |
| A3 | Barbaros 1533'te kaptan-ı derya oldu | 1534 | c8s2 |
| A4 | Charles 1557'de iflas etti | 'oğlu Felipe, ödemeleri durdurdu' | c10s8 |
| A4 | Capitulación'ı Isabel la Católica imzaladı | Anlatılmıyor | — |
| A4 | Atahualpa'nın idam tarihi tek | Tarih verilmiyor | c9s7 |
| A4 | Magellan dünyayı dolaştı; dönen '18 kişi' | 'Magellan yolda öldü'; 'on sekiz Avrupalı' | c9s13 |
| A4 | Yeni Yasalar encomienda'yı bitirdi | İddia edilmiyor | c9s9 |
| A4 | 'Güneş batmaz' Charles/Felipe sözü | Yok | — |
| A4 | Fugger mektubu kelimesi kelimesine | 'özetle' | c10s6 |
| A4 | Savaşları Amerikan gümüşü finanse etti | Tersi anlatılıyor (vergiler, bankerler) | c10s1-c10s4 |
| A5 | 'Şeref hariç her şey kayıp' birebir kral sözü | 'sonradan yaygınlaştı' | c6s4 |
| A5 | Charles Roma'nın yağmasını emretti | 'emir vermemişti' | c6s9 |
| A5 | 1528 düellosunu Charles teklif etti (tek yönlü) | 'iki hükümdar ... davet etti' | c6s11 |
| A5 | 25 Ekim 1555'te her şeyi bıraktı | 'bırakmaya başlıyor'; devir ayrıntısı | c0s7, c12s5 |
| A5 | Eylül 1556'da Yuste'ye taşındı | Eylül 1556 İspanya, Şubat 1557 Yuste | c12s8 |
| A5 | Tabuta yatma, iki saat, Borja yemini kesin | Tabut 'yalnızca rivayet'; diğerleri yok | c12s9 |

Toplam 37 madde: ihlal 0.

## Kullanılan kaynaklar

Yalnız araştırma dosyalarında geçen URL ve yayıncılar, tekrarsız. Parantezde ilgili araştırma satırı. Bu oturumda arama sonuçlarında görülen ek sayfalar burada yinelenmedi; yalnız §7 tablosunda ilgili satırda verildi.

### A3 — `_ham_olgu_taslak.md` (Osmanlı/Akdeniz)

- Kitapyurdu (Parker çevirisi) — https://www.kitapyurdu.com/kitap/imparator-sarlken-ciltli/764183.html (A3 #1)
- Selçuk Üniv. tezi — https://acikerisim.selcuk.edu.tr/items/9b1c1741-3c71-4d53-8f2b-72bdcac3a5f5 (A3 #1)
- TDV İA — İspanya — https://islamansiklopedisi.org.tr/ispanya (A3 #1)
- Yelçe, Sabancı Üniv. — https://research.sabanciuniv.edu/id/eprint/32484/1/9-_Zeynep_Yelçe.pdf (A3 #2)
- Wikipedia — Truce of Constantinople (1533) — https://en.wikipedia.org/wiki/Truce_of_Constantinople_(1533) (A3 #2)
- Wikipedia — Peace of Zsitvatorok — https://en.wikipedia.org/wiki/Peace_of_Zsitvatorok (A3 #2)
- TDV İA — Mohaç Muharebesi — https://islamansiklopedisi.org.tr/mohac-muharebesi (A3 #3)
- TDV İA — Macaristan — https://islamansiklopedisi.org.tr/macaristan (A3 #3)
- New World Encyclopedia — Battle of Mohacs — https://www.newworldencyclopedia.org/entry/Battle_of_Mohacs (A3 #3)
- Wikipedia — Siege of Buda (1529) — https://en.wikipedia.org/wiki/Siege_of_Buda_(1529) (A3 #4)
- Britannica — Siege of Vienna (1529) — https://www.britannica.com/event/Siege-of-Vienna-1529 (A3 #5)
- Wikipedia — Siege of Vienna (1529) — https://en.wikipedia.org/wiki/Siege_of_Vienna_(1529) (A3 #5)
- TDV İA — Süleyman I — https://islamansiklopedisi.org.tr/suleyman-i (A3 #6, #8)
- TDV İA — Viyana — https://islamansiklopedisi.org.tr/viyana (A3 #6)
- Clarke, Villa I Tatti (Warwick) — https://warwick.ac.uk/fac/arts/ren/ugstudy/syllabus-t1-2022-23/georgia_clarke_-_the_emperors_hat._city_space_and_identity_in_contemporary_accounts_of_charles_vs_i_tatti_2013.pdf (A3 #7)
- Wikipedia — Coronation of Charles V — https://en.wikipedia.org/wiki/Coronation_of_Charles_V (A3 #7)
- Wikipedia — Siege of Kőszeg — https://en.wikipedia.org/wiki/Siege_of_K%C5%91szeg (A3 #8)
- New World Encyclopedia — Siege of Vienna — https://www.newworldencyclopedia.org/entry/Siege_of_Vienna (A3 #9)
- Kirchroth (Kaiser Karl V.) — https://www.kirchroth.de/fileadmin/Gemeinde/Dateien/Heimatgeschichte/38_Kaiser_Karl_V.pdf (A3 #9)
- Wien Geschichte Wiki — https://www.geschichtewiki.wien.gv.at/Das_Heer_Karls_V._vor_Wien_1532,_M._Ostendorfer_(1539) (A3 #9)
- Bariska (ises.hu) — https://ises.hu/wp-content/uploads/2024/11/BARISKA_1532_contribution-to-the-history-1.pdf (A3 #9 notu)
- Wikipedia — Franco-Ottoman alliance — https://en.wikipedia.org/wiki/Franco-Ottoman_alliance (A3 #10)
- Military Wiki — Franco-Ottoman alliance — https://military-history.fandom.com/wiki/Franco-Ottoman_alliance (A3 #10)
- Herodote.net — 4 février 1536 — https://www.herodote.net/4_fevrier_1536-evenement-15360204.php (A3 #11)
- EBSCO — Turkish capitulations — https://ebsco.com/research-starters/history/turkish-capitulations-begin (A3 #11)
- Universalis — Capitulations — https://www.universalis.fr/encyclopedie/capitulations/ (A3 #11)
- Wikipedia — Capitulations of the Ottoman Empire — https://en.wikipedia.org/wiki/Capitulations_of_the_Ottoman_Empire (A3 #11)
- İBÜ açık erişim (La Forêt) — https://acikerisim.ibu.edu.tr/items/eb422dd7-f310-4755-bdbf-5941517b9d74 (A3 #11 notu)
- TDV İA — Barbaros Hayreddin Paşa — https://islamansiklopedisi.org.tr/barbaros-hayreddin-pasa (A3 #12, #14)
- TDV İA — Hafsîler — https://islamansiklopedisi.org.tr/hafsiler (A3 #12)
- Wikipedia — Conquest of Tunis (1535) — https://en.wikipedia.org/wiki/Conquest_of_Tunis_(1535) (A3 #13)
- War History Online — Amphibious Warfare I — https://warhistory.org/article/amphibious-warfare-i?amp=1 (A3 #13)
- TDV İA — Halkulvadi — https://islamansiklopedisi.org.tr/halkulvadi (A3 #13)
- Wikipedia — Battle of Preveza — https://en.wikipedia.org/wiki/Battle_of_Preveza (A3 #14)
- Wikipedia — Holy League (1538) — https://en.wikipedia.org/wiki/Holy_League_(1538) (A3 #14)
- EBSCO — Battle of Preveza — https://ebsco.com/research-starters/history/battle-preveza (A3 #14 notu)
- Wikipedia — Algiers expedition (1541) — https://en.wikipedia.org/wiki/Algiers_expedition_(1541) (A3 #15)
- Academia-Lab — Expedición de Argel (1541) — https://academia-lab.com/enciclopedia/expedicion-de-argel-1541/ (A3 #15, #16)
- Hispanopedia — Jornada de Argel — https://es.hispanopedia.com/wiki/Jornada_de_Argel (A3 #15)
- Molina Villeta, Studia Historica — https://revistas.usal.es/uno/index.php/Studia_Historica/article/download/31382/29687/122478 (A3 #16)
- Wikipedia — Truce of Adrianople — https://en.wikipedia.org/wiki/Truce_of_Adrianople (A3 #18)
- Szeged (Mediterrán Tanulmányok) — https://ojs.bibl.u-szeged.hu/index.php/mediterran_tanulmanyok/article/download/34529/33645/39818 (A3 #18)
- GHDI — document 4513 — https://germanhistorydocs.org/en/from-the-reformations-to-the-thirty-years-war-1500-1648/ghdi:document-4513 (A3 #18)
- Universalis — Quint — https://www.universalis.fr/dictionnaire/quint/ (A3 #19)
- Britannica — Vienna / History — https://www.britannica.com/place/Vienna/History (A3 #19)
- Encyclopedia.com — Suleiman — https://www.encyclopedia.com/history/modern-europe/turkish-and-ottoman-history/suleiman (A3 #20)
- Wikipedia — Suleiman the Magnificent's Venetian helmet — https://en.wikipedia.org/wiki/Suleiman_the_Magnificent%27s_Venetian_helmet (A3 #21)
- The Met — 42.41.1 — https://metmuseum.org/toah/works-of-art/42.41.1 (A3 #21)
- Ca' Foscari (iris.unive.it) — https://iris.unive.it/handle/10278/5038680 (A3 #21)
- Necipoğlu 1989 (medievalists.net) — https://www.medievalists.net/2012/02/suleyman-the-magnificent-and-the-representation-of-power-in-the-context-of-ottoman-hapsburg-papal-rivalry/ (A3 #21)
- Christie's lot 6411353 — https://christies.com.cn/lot/lot-6411353 (A3 #21 notu)
- Yale Avalon (ipucu) — https://documents.law.yale.edu/node/156026 (A3 açık uçlar)
- Mannheim MATEO (ipucu) — https://www.uni-mannheim.de/mateo/camenaref/cmh/cmh304.html (A3 açık uçlar)
- Belleten (ipucu) — https://www.belleten.gov.tr/benzer-makaleler/2763?page=14 (A3 açık uçlar)

### A4 — `_ham_olgu_sayfasi.md` (Yeni Dünya/finans)

- Redalyc — https://www.redalyc.org/pdf/589/58949959003.pdf (A4 #1)
- New World Encyclopedia — Battle of Tenochtitlan — https://www.newworldencyclopedia.org/entry/Battle_of_Tenochtitlan (A4 #1)
- Cognito (IB notları) — https://cognito.org/courses/ib/history/ibhl/notes/WWpjS2Rwd0U/2.2-cort-s-the-conquest-of-the-aztecs (A4 #1 notu)
- Maryland Üniv. EADA — İkinci mektup — https://eada.lib.umd.edu/text-entries/second-letter-of-hernando-cortes-to-charles-v (A4 #2)
- UNAM (Cartas de relación) — https://www.noticonquista.unam.mx/sites/default/files/2019-07/martinez_-_cartas_de_relacion_-_final.pdf (A4 #2)
- Archive.org — Saville — https://archive.org/stream/earliestnotice00savi/earliestnotice00savi_djvu.txt (A4 #3)
- Wikipedia — Hernán Cortés — https://en.wikipedia.org/wiki/Hern%C3%A1n_Cort%C3%A9s (A4 #4)
- Hispanopedia — Marquesado del Valle de Oaxaca — https://es.hispanopedia.com/wiki/Marquesado_del_Valle_de_Oaxaca (A4 #4)
- Hispanopedia — Capitulación de Toledo — https://es.hispanopedia.com/wiki/Capitulaci%C3%B3n_de_Toledo (A4 #5)
- UDEP — https://www.udep.edu.pe/hoy/2022/08/la-conquista-de-la-nueva-castilla-y-la-ciudad-de-san-miguel/ (A4 #5)
- Biografías y Vidas — Atahualpa — https://www.biografiasyvidas.com/biografia/a/atahualpa.htm (A4 #6)
- History.co.uk — 16 November — https://www.history.co.uk/this-day-in-history/16-november/pizarro-massacres-5000-incans-and-takes-incan-emperor-hostage (A4 #6)
- PUCP (Jerez, Loredo) — Histórica 8203 — https://revistas.pucp.edu.pe/index.php/historica/article/download/8203/8503 (A4 #7)
- World History Encyclopedia — article 2045 — https://www.worldhistory.org/article/2045 (A4 #7)
- Wikipedia — Ransom Room — https://en.wikipedia.org/wiki/Ransom_Room (A4 #7 notu, #9)
- Wikipedia — Hernando Pizarro — https://en.wikipedia.org/wiki/Hernando_Pizarro (A4 #8)
- History.com — Pizarro executes last Inca emperor — https://www.history.com/this-day-in-history/July-26/pizarro-executes-last-inca-emperor (A4 #9)
- Encyclopedia.com — Potosí — https://www.encyclopedia.com/places/latin-america-and-caribbean/south-american-political-geography/potosi (A4 #10)
- World History Encyclopedia — audioplayer 2-2049 — https://www.worldhistory.org/audioplayer/en/2-2049/ (A4 #10)
- Wikipedia — Price revolution — https://en.wikipedia.org/wiki/Price_revolution (A4 #11)
- Toronto Üniv. (Munro) çalışma kâğıdı — https://www.economics.utoronto.ca/public/workingPapers/UT-ECIPA-MUNRO-02-02.pdf (A4 #11)
- Swiss National Museum — Jakob Fugger — https://blog.nationalmuseum.ch/en/2020/03/jakob-fugger-money-and-spirit-around-1500/ (A4 #12)
- Wikipedia — Fugger family — https://en.wikipedia.org/wiki/Fugger_family (A4 #12)
- DHM — Frankfurt — https://www.dhm.de/mediathek/en/ida/frankfurt-en (A4 #12)
- Financial History Magazine — https://fhmagazine.org/financial-history-issue-114-summer-2015/0717636001440076157/p22 (A4 #13)
- Libertad Digital (köşe yazısı) — https://www.libertaddigital.com/opinion/los-enigmas-del-11m/esos-incautos-banqueros-alemanes-10189/ (A4 #13 notu)
- Binghamton Üniv. — German conquistadors — https://www.binghamton.edu/news/story/3984/german-conquistadors-the-forgotten-rulers-of-venezuela-and-their-legacy (A4 #14)
- Wikipedia — Klein-Venedig — https://en.wikipedia.org/wiki/Klein-Venedig (A4 #14)
- Economic History Review (Álvarez-Nogal–Chamley) — https://people.bu.edu/chamley/history/castilla/EHR12013.pdf (A4 #15)
- Banco de España — https://repositorio.bde.es/bitstream/123456789/7406/2/roja71.pdf (A4 #15)
- Studia Historica (usal) 31805 — https://revistas.usal.es/uno/index.php/Studia_Historica/article/download/31805/29564/121159 (A4 #15 notu)
- H-Net (Tracy kitabı eleştirisi) — https://www.h-net.org/reviews/showpdf.php?id=8990 (A4 #16)
- İspanya Savunma Bakanlığı (Revista de Historia Naval) — https://publicaciones.defensa.gob.es/pprevistas/REVISTAS_PDF21129/pubData/SEO/Page_44.html (A4 #17)
- CSIC — Casa de la Ciencia — https://www.casadelaciencia.csic.es/es/print/blog/primera-vuelta-al-mundo-magallanes-elcano (A4 #17)
- Guinness World Records — First circumnavigation — https://guinnessworldrecords.com/world-records/first-circumnavigation (A4 #18)
- Wikipedia — Victoria (ship) — https://en.wikipedia.org/wiki/Victoria_(ship) (A4 #18)
- Hispanopedia — Primus circumdedisti me — https://es.hispanopedia.com/wiki/Primus_circumdedisti_me (A4 #19)
- Fundación Elkano (Google Arts & Culture) — https://artsandculture.google.com/story/zAUxC9qUHA2hGQ (A4 #19)
- Wikipedia — New Laws — https://en.wikipedia.org/wiki/New_Laws (A4 #20)
- PUCP — Histórica 7982 — https://revistas.pucp.edu.pe/index.php/historica/article/download/7982/8272 (A4 #20)
- Wikipedia — Valladolid debate — https://en.wikipedia.org/wiki/Valladolid_debate (A4 #21)
- UNCuyo — Controversias de Valladolid — https://educacion.uncuyo.edu.ar/upload/controversias-de-valladolid.pdf (A4 #21)
- Wikipedia — A Short Account of the Destruction of the Indies — https://en.wikipedia.org/wiki/A_Short_Account_of_the_Destruction_of_the_Indies (A4 #21 notu)
- Wikipedia — The empire on which the sun never sets — https://en.wikipedia.org/wiki/The_empire_on_which_the_sun_never_sets (A4 #22)
- Hispania Histórica — https://hispaniahistorica.com/siglo-de-oro/carlos-v-emperador-habsburgo/ (A4 #22)

### A1, A2, A5 — URL'si araştırma dosyalarında verilmeyen, yalnız adı geçen kaynaklar

- **A1:** Anne Boleyn Files; WorldHistory.org; WorldHistoryEdu; WesternCiv; Royal Collections Gallery (Galería de las Colecciones Reales); Britannica; HNA; Catholic Encyclopedia; Gazette Drouot; Wikipedia; Boydell/Cambridge Core; Turismo Asturias; Council of Europe; Brainscape; Wikipedia (Sauvage); DHM; EBSCO; Cohn (German History 19, 2001); Wikisource; CHI; bpb; Centre Charlemagne; Univ. of Valladolid; CEEOL; Habsburger.net; Encyclopedia.com; Annals of Human Biology; Smithsonian; Wikiquote; Oxford Reference; The Low Countries.
- **A2:** k-state.edu; Catholic Textbook Project; worldhistory.org; Lutheran Quarterly (Young 2022); Religion-Online; Wikipedia; Christianity Today (Hendrix); CHI; GHDI; evangelisch.de; Ellis; Concordia Nebraska; Schaff; Presbyterian Mission; Lutheran Sentinel; NWE; Berkley Center; EBSCO; Ligonier; Lutheran Reformation; 1517.org; PRCA; ELS; biblicaltraining.org; ellopos; War History; Nobility.org.
- **A5:** Britannica; Herodote.net; Revue Conflits; La Culture générale; Gutenberg (Guizot); British History Online; Wikipedia; HistoryofWar; Smarthistory; Galería de las Colecciones Reales; History of Royal Women; WorldHistory; Hektoen; NBC; PMC (PMC10810993); NEJM 2006; Frontiers 2024; Substack; Motley/Gutenberg; GHDI; habsburger.net; Fundación Yuste; EBSCO; Boletín de Arte (UMA); Limelight; RAH; folklor makalesi.

