# Türkçe boşluk taraması (22 Kasım 2026): dünyada yankı bulmuş, Türkçede az anlatılmış, Türkiye'yi ilgilendiren konular

**Kullanıcının ölçütü (22 Kasım):** popüler konu değil. Türkçede kaynağı az, dünyada yankı bulmuş, Türkiye'de etkisi olması gereken konu.
Bu yüzden önceki taramaların ölçüsü ters çevrildi:
- Türkçe aramada en çok izlenen video küçük olmalı (boşluk).
- İngilizce arama büyük olmalı (yankı).
- Konunun Türkiye'yle bağı olmalı (yer, tarih ya da bugünkü bir tartışma).

Araç: `python3 araclar/talep/iki_dil.py "türkçe sorgu|english query" …`. Türkçe başlık tespiti kaba; sayılar sinyal, karar değil.

## Ölçüm
| Konu | Türkçe: en çok izlenen | Türkçe: medyan | İngilizce: en çok / medyan | Türkiye bağı |
|---|---|---|---|---|
| Lale çılgınlığı (tulip mania) | **16,8 B** | 89 | 718 B / **204 B** | lale İstanbul'dan gitti; Lale Devri; bugünün kripto/döviz yatırımcısı |
| Leonardo'nun Haliç köprüsü | **415** | 102 | 7,0 M (tek viral) / 401 | İstanbul, II. Bayezid, 1502 mektubu |
| 1755 Lizbon depremi | 50 B, 44 B | 632 | 1,0 M / 44 B | 6 Şubat 2023; Rousseau'nun "yedi katlı ev" mektubu |
| Lady Montagu, çiçek aşısı | 51 B (belgesel), gerisi < 4 B | 275 | (İngilizce sorgu zayıf) | 1717 İstanbul, Osmanlı kadınlarının aşılaması; bugünkü aşı tartışması |
| Satranç oynayan Türk (Mechanical Turk) | 154 B | 16 B | 8,5 M / 132 B | **boşluk yok**: "Türkler bilmiyor…" başlıklı 154 B'lik video var |
| Takiyüddin rasathanesi | 8,9 B | 753 | 177 / 22 | Türkçede anlatılmış, dünyada yankı yok |
| Mevlana'nın sahte sözleri | 1,9 M | 101 B | 1,1 M / 35 B | Türkçede kalabalık; dini hassasiyet |
| Diocletianus'un fiyat fermanı (Afrodisias) | 4 B | 61 | 0 | iki dilde de talep yok |
| Auerbach, *Mimesis* (İstanbul'da yazıldı) | 0 | 0 | 0 | YouTube'da iki dilde de talep yok |

## Başkanın sıralaması
1. **1755 Lizbon depremi: "Bu evleri doğa yapmadı."** (Tarihin Dönüm Noktaları + felsefe)
   - **Niş açı:** depremin kendisi Türkçede anlatılmış (iki video ~50 B), ama Avrupa düşüncesini değiştiren tartışması anlatılmamış.
     - Voltaire felaketi Tanrı'nın düzenine sığdıramadı (*Lizbon Felaketi Üzerine Şiir*, 1756; *Candide*, 1759).
     - Rousseau ona 18 Ağustos 1756'da yazdı: o yirmi bin altı-yedi katlı evi oraya doğa toplamadı; şehir daha dağınık ve hafif yapılsaydı zarar çok daha az olurdu (doğrulandı: Wikisource, *Lettre à Voltaire sur la Providence*).
     - Kant aynı yıl depremin doğal nedenleri üzerine üç yazı yazdı. Pombal şehri ilk depreme dayanıklı yapı sistemiyle yeniden kurdu (*gaiola pombalina*) ve kiliselere hasar soru kâğıdı gönderdi. Bu ayrıntılar kaynak denetiminde doğrulanacak.
   - **Türkiye bağı:** 6 Şubat 2023'ten beri Türkiye'nin sorusu bu: "Felaket mi, ihmal mi?" Bağlantıyı video kurmaz, izleyici kurar; Rousseau'nun sözü yeter.
   - **Kişisel soru:** "Seni deprem mi öldürür, oturduğun ev mi?" / "Felaketin suçlusu kim?"
   - **Kaynaklar** kamu malı (Voltaire, Rousseau, Kant). 18. yüzyıl Lizbon yıkıntı gravürleri de kamu malı. Gravür motoru (`milton/lib`) bu döneme uyar.
   - **Riskler:**
     - Hassasiyet en yüksek aday: deprem travması. 2023 görüntüsü, kurban sayısı ve siyasi suçlama kullanılmaz.
     - 1755'teki "ilahi ceza" yorumları dinî karşılaştırmaya girmeden yalnız tarih olarak anlatılır.
     - Hassasiyet kurulu senaryodan önce çalışır.
2. **Lale çılgınlığı: iki lale çılgınlığı, biri İstanbul'da.** (Tarihin Dönüm Noktaları + ekonomi psikolojisi)
   - **Boşluk** taramanın en büyüğü: İngilizcede medyan 204 B, Türkçede en çok izlenen video 17 B.
   - **Niş açı:** "tarihin ilk balonu" olarak bilinen 1637 Hollanda çöküşü. Yakın tarih araştırması (Anne Goldgar, *Tulipmania*, 2007) çöküşün sonradan büyütüldüğünü gösteriyor: Mackay'in 1841'de anlattığı "soğan sanıp lale yiyen denizci" gibi hikâyeler. Lale İstanbul'dan Avrupa'ya gitti. Lale Devri'nde (1718–1730) lale fiyatları 1726–27'de tepe yaptı ve devlet karıştı.
   - **Doğrulanacak:** devletin fiyatı nasıl düzenlediği (narh mı, tavan mı?) taramada kesinleşmedi. Kaynak `acikbilim.yok.gov.tr` 20.500.12812/630392 (*Lale Devri'nin Lalesi*).
   - **Kişisel soru:** "Herkes alıyor diye sen de alır mıydın?" (kripto, borsa, döviz).
   - **Üslup:** Hollanda lale kitaplarının suluboya sayfaları (Rijksmuseum, kamu malı) + Osmanlı lale nakşı. Karma üslup.
3. **Leonardo'nun Haliç köprüsü.**
   - **Boşluk** en temiz olanı: Türkçede en çok izlenen 415.
   - **Olay:** 1502'de II. Bayezid'e yazılan mektup (Topkapı arşivi). 280 m'lik tek kemer, zamanının en uzunu olurdu. Sultan başka bir öneriyi seçti. 2019'da MIT bir model kurup tasarımın ayakta kalacağını gösterdi.
   - **Zayıf yanı:** kişisel soru zayıf ("reddedilen fikir haklı mıydı?"), hikâye kısa.
- **Yedek:** Lady Montagu ve çiçek aşısı. Türkçe boşluk var, Türkiye bağı güçlü. Bugünkü aşı tartışması yüzünden hassasiyet kurulu şart.
- **Elenenler:**
  - Mechanical Turk: Türkçede anlatılmış.
  - Takiyüddin: Türkçede anlatılmış, dünyada yankısı yok.
  - Mevlana: Türkçe kalabalık, dini hassasiyet.
  - Diocletianus ve Auerbach: talep yok.

## Ders
- Kanalın talep kontrolü (a) "Türk izleyici tanıyor mu?" sorusunu soruyordu. Bu ölçüt ters yöne bakıyor: dünyada yankı + Türkçede boşluk + Türkiye bağı.
- İkisi çelişmez. Tanıdık kapı konunun kendisi değil, Türkiye bağı olur (deprem, lale, İstanbul). Başlıkta o kapı öne alınır.
- Sonuç bu ölçütle çıkan ilk videonun 48. saat verisiyle buraya yazılacak.
