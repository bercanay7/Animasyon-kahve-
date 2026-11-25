# Deney: ayrıntılı prompt mu, yalnız yön mü? (23 Kasım 2026, kullanıcının kararı)

**Soru:** Üretim oturumuna adım adım talimat yerine yalnız bir yön verilirse video daha mı iyi olur?

**Kaynak:** kullanıcının sektörden duyduğu görüş: "Opus'a ayrıntılı prompt verince kötüleşiyor, yalnız yön ver."

**Düzen:**
- **Lale Çılgınlığı:** ayrıntılı prompt (`2026-11-22-lale-baslangic-prompt.md`). Omurga, kaynak listesi, üslup önerisi ve 10 adımlık akış veriliyor.
- **Gılgamış:** yalnız yön (`2026-11-23-gilgamis-yon-prompt.md`).
  - Yönü Fable yazdı (danışman olarak değil, tek seferlik yön; ~115 kelime).
  - Fable Hattuşa'yı, 1872 ve 2011 tabletlerini, üslubu ve iskeleti bilerek dışarıda bıraktı ("yön değil malzeme").
- **İki oturumda da aynı olan:** CLAUDE.md otomatik yüklenir. Kanalın kuralları (kredi onayı, Emrullah, telif, hassasiyet, tempo dersleri) iki oturumda da aynıdır; değişen yalnız oturuma verilen ilk metindir.

**Başkanın beklentisi (yayından önce yazıldı):**
- Yön promptunda omurga ve üslup seçimi daha özgün çıkar. Ayrıntılı prompt oturumu bizim önerilerimize (iki efsane, "yalnız laleler renkli") bağlar.
- Ama yön promptunda kanal kurallarından biri atlanabilir: yeni kural CLAUDE.md'nin derinindeyse.
- Uzun ve açık uçlu yaratıcı iş için yön; maliyetli ya da geri alınamaz adımlar (kredi, yayın, telif) için açık kural. CLAUDE.md zaten bu ikinci görevi görüyor.

**Karar (23 Kasım, kullanıcıyla konuşuldu): tek yön, tek değişken.**
- Fable yalnız başta yön verdi. Üretim sırasında yeniden yön vermek için çağrılmaz.
- Alt ajanlar iki videoda da aynı kurala bağlı: başkanın takdirinde (kullanıcının 23 Kasım açıklaması: 19 Kasım kararı kurulu ve puanlamayı kaldırdı, alt ajanları değil). Yani bu da iki videoda sabit.
- Sondaki "Fable'ın tek son yorumu" iki videoda da serbest. Yön değil denetim olduğu için deneyi bozmaz.
- Neden: aynı anda iki şey değişirse sonucun hangisinden geldiği anlaşılmaz.
- Sonraki adaylar:
  - (a) Fable'ın senaryo taslağından sonra ikinci kez yön vermesi;
  - (b) Opus yönetmen + Sonnet ölçüm ajanlarının kurallı bir düzen olarak kurulması.
  - Her biri ayrı bir videoda denenir.

**Ölçüler:** her iki video için doldurulur.

| Ölçü | Lale (ayrıntılı) | Gılgamış (yön) |
|---|---|---|
| Kullanıcının üretim sırasındaki düzeltme sayısı | | |
| Atlanan kanal kuralı (başkanın ya da Fable'ın yakaladığı) | | |
| Kullanıcının kendi notu (1–10, "videoyu beğendin mi") | | |
| 48. saat: 0:30'da kalan, ortalama izlenme %, TO | | |
| Yayın (sıra 23 Kasım'da değişti) | 6 Aralık (Gılgamış'tan sonra) | 2 Aralık (Dorian'dan sonra) |
| 7. gün: aynı ölçüler | | |

**Ortam (23 Kasım):**
- İki oturum da sadeleştirmeden önce açıldı, ikisi de eski CLAUDE.md'yle (93 KB) çalışıyor. Ortam sabit; değişen yalnız ilk metin.
- Gılgamış oturumu üretimin başında `main`'i alıp sadeleştirilmiş CLAUDE.md'yi okuyacak. İçinde Lale'nin yeni kuralları da var: fikir sorma, yeni hassasiyet simgeleri, `film.js`. Lale bunları kendi üretti; Gılgamış hazır alıyor. Fark küçük ama kayıtta dursun.
- İkisine de aynı ortam notu verildi: CLAUDE.md'ye dokunma, alt ajanlar takdirinde, yayın tarihi. Not yaratıcı yön değil, ikisinde de aynı.

**Uyarı:** konular farklı olduğu için bu kontrollü bir deney değil. Tek çiftten kural çıkmaz; ipucu çıkar. Sonuç iki üç çiftte aynı yöne giderse CLAUDE.md'ye yazılır.

## Ek: Frankenstein, ikinci yön videosu (23 Kasım 2026)
- **Yön:** kullanıcının yazdığı yön (`analiz/2026-11-24-frankenstein-yon-prompt.md`; gerekçe ve doğrulanacaklar Fable'ın notu). Gılgamış'taki gibi tek yön, sonradan yön yok.
- **Alt ajanlar:** Fable'ın seslendirme öncesi senaryo okuması (6 engelleyici) ve ayrı bir okuyucunun yazısız kare okuması (9 engelleyici). İkisi de denetim; yön vermedi.
- **Başkanın seçtikleri ve yönün yetmediği yerler:** `frankenstein/geriye_bakis.md`.
- **Ölçüler** (Lale ve Gılgamış tablosuyla aynı): kullanıcının üretim sırasındaki düzeltmesi 0 (geriye bakış yazılırken); atlanan kanal kuralı: yok bulundu (kullanıcının fikrini sorma adımı yön metniyle karşılandı, Gılgamış'taki gibi); 48. saat ve 7. gün `analiz/tahminler.md` F1–F3.

## Ek: Stanford Hapishane Deneyi, dördüncü yön videosu (25 Kasım 2026)
- **Yön:** Fable'ın yazdığı yön (`analiz/2026-11-25-stanford-yon-prompt.md`; gerekçe ve doğrulanacaklar `2026-11-25-stanford-yon-notlari.md`). Tek yön, sonradan yön yok.
- **Yeni değişken (kullanıcının isteği):** senaryodan önce internetten kanca kaynakları araştırması.
  - Bu konuda abonesi az ama çok izlenmiş videoların çözümlemesi de istenmişti; kullanıcı 25 Kasım'da "şimdilik es geçelim" dedi, sonraki bir videoya kaldı.
    - Kısıt: bu kaptan izleme sayfası ve altyazı alınamıyor (429). Arama, kanal sayfası (abone) ve kapaklar alınabiliyor.
  - Önceki üç yön videosunda bu adım yoktu. Fark çıkarsa yönden mi araştırmadan mı geldiği ayrılamaz; geriye bakışta araştırmanın neyi değiştirdiği ayrıca yazılır.
- **Ölçüler:** aynı tablo; 48. saat ve 7. gün `analiz/tahminler.md`.
