# Yeni "kapı" video için konu adayları (18 Kasım 2026)

Ölçüm: `python3 araclar/talep/talep.py …` (YouTube Türkçe otomatik tamamlama + aramadaki ilk 10 videonun izlenmeleri).
**Uyarı:**
- Aramadaki ilk 10'un medyanı gürültülü: aynı sorgu iki çalıştırmada 24,7 B ve 105 B verdi.
- İlk 10'da konu dışı videolar olabilir (şarkı, ürün, oyun: "ikaros işaret fişeği", "pandora bileklik").
- Sayılar kaba sinyal; öneri listesiyle birlikte okunur.

## Kontrol satırları
| Sorgu | Öneri | İlk 10 medyan | Not |
|---|---|---|---|
| sisifos | 14 | 24,7 B (ikinci çalıştırma 105 B) | "sisifos meme", "sisifos edit": gençlik ve mizah kültüründe yaşıyor |
| dönüşüm kafka | 14 | 33,2 B | özet, analiz, sesli kitap; talep Sisifos kadar güçlü |
| milton kayıp cennet | 1 | 2,9 B | talep yok (Milton'ın sorunu) |

**Ders:** Kafka talep ölçüsünde Sisifos'tan geri değil, buna rağmen dalga gelmedi. Talep gerekli ama yeterli değil. Sisifos'un ayrı bir yanı var: önerilerde "meme" ve "edit" (gençlerin kısa video kültürü). Hipotez, kanıt değil: konu gençlerin paylaşım kültüründe yaşıyorsa geniş kitleye açılma şansı artar. Aynı işaret bu adaylarda da var: nietzsche (edit), marcus aurelius (edit), 1984 (edit).

## Adaylar
| Sorgu | Öneri | İlk 10 medyan | Öne çıkan öneriler |
|---|---|---|---|
| narsisizm | 12 | 202 B | nedir, belirtileri, nasıl tedavi edilir |
| nietzsche | 14 | 365 B | felsefesi, sesli kitap, "nietzsche ağladığında", **edit** |
| marcus aurelius | 14 | 397 B | kendime düşünceler, sözleri, **edit** |
| suç ve ceza | 14 | 85 B | sesli kitap, özet, film |
| 1984 orwell | 14 | 85 B | film, **edit**, özet |
| kürk mantolu madonna | 14 | 54 B | sesli kitap, özet, film, tiyatro |
| küçük prens | 14 | 52 B | sesli kitap, çizgi film, özet |
| yeraltından notlar | 14 | 47 B | özet, kitap yorumu |
| stoacılık | 14 | 21 B | nedir, felsefesi |
| narkissos | 9 | 22 B | "narkissos hikayesi" (mitin adı zayıf; kapı "narsisizm") |
| platon mağara alegorisi | 3 | — | "ne anlatıyor", "truman show" |
| simyacı / beyaz zambaklar / pandora / medusa | | | konu dışı sonuçlar baskın (kimya kanalı, bileklik, dizi) |

## Başkanın sıralaması (talep + kişisel soru + motor + telif + hassasiyet)
1. **Narkissos → narsisizm** (Mitler ve Felsefe + Psikoloji köprüsü).
   - Kapı: "narsisizm" (psikoloji araması güçlü).
   - Soru: "Kendini sevmek ne zaman hastalığa döner?" / "Aynada aradığın kim?"
   - Vazo motoru hazır (Sisifos, Prometheus): en ucuz üretim.
   - Kaynak: Ovidius, *Metamorfozlar* III (kamu malı).
   - Dikkat: tıbbi tanı vaadi yok (psikoloji kavramı, teşhis değil).
2. **Nietzsche, bengi dönüş.**
   - Soru: "Bu hayatı sonsuz kez yaşamak zorunda olsan, değiştirir miydin?"
   - Camus ve Sisifos ile aynı damar; "edit" kültürü var.
   - Karar anı: Torino, Ocak 1889, at sahnesi. Anekdotun kaynağı tartışmalı; kurulda "anlatılır ki" diye verilir.
   - Hassasiyet: "Tanrı öldü" çerçevesine girilmez.
   - Telif yok (1900).
3. **Dostoyevski, *Suç ve Ceza*.**
   - Kullanıcının daha önceki "psikolojik anlatım" önerisi.
   - Soru: "İyi bir amaç için kötülük yapılabilir mi?" / "Vicdanından kaçabilir misin?"
   - Kamu malı.
- **Yedekler:**
  - **Marcus Aurelius:** talep en yüksek, ama kişisel gelişim kanallarıyla kalabalık.
  - ***Kürk Mantolu Madonna*:** Türkiye'de kamu malı, Sabahattin Ali 1948'de öldü; Türk edebiyatına ilk kapı.
  - ***Küçük Prens*:** Türkiye'de kamu malı, Saint-Exupéry 1944'te öldü.
  - **1984:** siyasi hassasiyet riski; hassasiyet kurulu şart.
