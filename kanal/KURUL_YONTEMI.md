# Kurul yöntemi (arşiv; 19 Kasım 2026'dan beri kurul ve puanlama yok)

> CLAUDE.md'den taşındı (23 Kasım 2026 sadeleştirmesi); metin değiştirilmeden. Geçerli kurallar CLAUDE.md'de; bu dosya ayrıntı ve geçmiş kayıttır.

## Kurul (bağımsız değerlendirme) yöntemi
**Yapı (kullanıcının kararı, 1 Kasım 2026):**
- **Başkan:** ana oturumdur (yapımcı).
  - Bulguları kendisi doğrular (ölçer, bakar, dinler).
  - Çatışmaları çözer ve son kararı verir.
  - Reddettiği bulguyu gerekçesiyle yazar.
- **Kullanıcının kararları** her şeyin üstündedir.
- **Üyeler:** her alanda **en az iki üye** bulunur. Her üye ayrı bir `Agent` alt ajanıdır ve farklı bir mercekle bakar; aynı bakışın iki kopyası olmaz.
- **Eşik:** ≥9/10 ONAY.

**Alanlar ve üyeler** (29 Ekim projesinin `cumhuriyet/KURUL.md` düzeninden):

| Alan | Üyeler (iki farklı mercek) |
|---|---|
| Senaryo ve dramaturji | senaryo/yönetmenlik + dramaturg (Kahramanın Yolculuğu listesi) |
| Kaynak ve doğruluk | konu uzmanı (tarih/edebiyat/felsefe) + kaynak denetçisi (tarih, alıntı, dize numarası, atıf; uydurma avı) |
| Anlatım (seslendirme) | seslendirme yönetmeni + Türkçe diksiyon uzmanı |
| Kanca ve tutma | YouTube tutma stratejisti + "ilk kez gören izleyici" (akışta kaydıran, şüpheci; şeytanın avukatı) |
| Sanat ve üslup | sanat yönetmeni + üslubun dönem/gelenek uzmanı |
| Animasyon ve kurgu | animasyon yönetmeni + kurgu/ritim uzmanı |
| Ekran yazıları ve altyazı | tipografi tasarımcısı + altyazı editörü (okuma hızı, satır bölme) |
| Müzik, ses ve miks | müzik direktörü + ses tasarımcısı/miks mühendisi |
| Teknik kalite | render ve kodlama denetçisi (renk etiketleri, kare kusurları, ses ölçümleri) + erişilebilirlik (telefon ve TV okunurluğu) |
| Hassasiyet ve hukuk | telif ve YouTube politikaları uzmanı + toplumsal ve dini hassasiyet okuru |
| Kapak, başlık, yayın paketi | TO/paketleme stratejisti + sanat yönetmeni |
| Yayın sonrası analiz (48. saat ve 7. gün) | kanal analisti + paketleme stratejisti; dersleri bu dosyaya yazar |

**Akış (her alan için):**
1. **Bağımsız ilk bakış:** üyeler birbirinin raporunu görmeden puan verir. Her rapor şunları içerir:
   - ONAY ya da RED;
   - 1920×1080 koordinatlı, sıralı düzeltme listesi;
   - "en emin olmadığım nokta".
2. **Çapraz eleştiri:** başkan iki raporu çapraz verir (`SendMessage`). Her üye ötekinin raporunda katıldığını, katılmadığını (gerekçeyle) ve gözden kaçanı yazar. Uzlaşma zorunlu değildir.
3. **Başkan kararı:**
   - Başkan iddiaları kendisi doğrular, düzeltmeleri sıralar ve uygular.
   - Projenin `KURUL.md` dosyasına alan, üyeler, puan, durum, reddedilen bulgular ve gerekçeleri işlenir.
4. **Sonraki tur:** aynı üyelerle devam edilir (`SendMessage`), ölçütler tutarlı kalır. "Yaptığım değişiklikler" listesi iddia olarak verilir; üyeler kendileri doğrular. Önceki turun dosyalarının **üzerine yazılmaz** (yeni tur yeni adla, ör. `board/tur4/…`).

**Kurallar:**
- **Veto:** kaynak/doğruluk ve hassasiyet/hukuk alanlarının engelleyici bulguları estetik oyla geçersiz kılınamaz. Yanlış bilgi, telif ve 5816 bulguları düzeltilmeden iş bitmez.
- **Maliyet:** iki üyeli tam tur yalnız şu kapılarda yapılır:
  - senaryo onayı;
  - üslup karesi;
  - ilk tam kurgu;
  - son render;
  - kapak;
  - yayın paketi.

  Küçük düzeltme turlarında tek üyeyle gerileme kontrolü yeterlidir.
- **Kurulun sınırı:** kurullar sesi dinleyemez. Whisper sözcük güveni, konuşma hızı, duraklar, perde ve enerji eğrileriyle ölçerler; kulakla son onay kullanıcınındır.
- **Kapak test seti:**
  - tam boy;
  - 246×138, 168×94 ve 120×68 küçültmeler;
  - bulanıklık/belirginlik (odak noktası);
  - gri değer;
  - koyu ve açık mobil akış taklidi (`mkfeed.py` mantığı);
  - TV boyunda bakış;
  - sağ alttaki süre rozeti bölgesi.
