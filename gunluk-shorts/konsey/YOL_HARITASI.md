# ZAMAN KURYESİ: YOL HARİTASI (2026-10-18 → 2027-01-16, 13 hafta)

Bu belge `KANAL_ANAYASASI.md` v2'nin işletim planıdır. Gerekçeler: `ANAYASA_ANALIZI_2026-10-17.md`. Ölçüm: `../olcum/`. Etiketler: [V] kendi verimiz · [P] platform (ikincil) · [H] varsayım · **[K]** kullanıcının yapacağı · **[C]** Claude'un yapacağı.

## 0. Strateji tezi

1. **Darboğaz dağıtım ve ilk saniyedir; cilt ve tipografi ikincildir.** Emu tek dağıtım testini geçti, %43 stayed to watch ile genişlemedi; kitlenin %57'si ilk saniyelerde kaydırdı [V]. Çözüm: sabit kadans + güçlü kare 0/ilk cümle + dürüst, kaynaklı içerik.
2. **İlerleme birimi "yayınlanmış ve ölçülmüş video"dur.** Motor/cilt geliştirmesi ancak yayın kuyruğu doluysa yapılır.
3. **Kaliteyi hızdan önde tutuyoruz:** gelir 2027 başından önce gerçekçi değil [P: YPP eşikleri]; bu süre bir öğrenme ve vitrin kurma süresi.
4. **Hukuki/politika zeminini baştan sağlama alıyoruz:** ses lisansı, özgünlük kayıtları, doğruluk kapısı.
5. **Karar kapıları veriyle:** Gün 14/28/60/90'da "ne kalıyor, ne değişiyor" yazılı verilir.

**Kanalın sözü (öneri):** *"Bildiğini sandığın şeyin ters yüzü. Tarihten, bilimden ve halk sağlığından kaynaklı, sakin tempolu kısa hikâyeler. Her teslimatın başında vaat, sonunda kanıt."*

## 1. Durum fotoğrafı

| Başlık | Durum | Kaynak |
|---|---|---|
| Kanal | 4 günlük, **6 abone**, 28 günde 1.728 görüntülenme (%94'ü Emu) | Studio 14 Eki [V] |
| Canlı videolar | Zanzibar, Emu, Dans, Titanik v1 + 3 depoda kaydı olmayan (Antik Mısır, Romalılar, Moğol) | Studio [V] |
| Hazır, yayınlanmamış | #5 Sıtma (39 sn, mavi baskı; kullanıcı tempo/bağlam/çizim eleştirdi), #6 Dune (156 sn), #7 Pellagra (105 sn) + Titanik v2 (40 sn, düzeltilmiş) | yayın günlüğü, git |
| Üretim hızı | ≈1 Özel video/gün (15–17 Eki); #6 ve #7 yeni cilt, #5 Titanik'le aynı cilt | git [V] |
| Ses | Piper `dfki` (kullanıcı: "ses iyi"); veri seti CC BY-NC-SA 4.0 | MODEL_CARD [V] |
| Konu havuzu | 9 aday (2 kullanıldı), öncelik belirsiz | `../konu-havuzu/` |
| Ölçüm | ekran görüntüsü, elle; şema yoktu | — |

## 2. Fazlar

| Faz | Tarih | Amaç | Çıktı |
|---|---|---|---|
| **0 Temizlik + ilk yayın** | 18–19 Eki | Vitrini düzelt, Pellagra'yı yayınla, ölçümü başlat | Pellagra yayında; Titanik v1 + 4 eski video private; ses testi dinlendi |
| **1 Kadans ve baz çizgi** | 20 Eki – 15 Kas (4 hafta) | Haftada 3 yayın; kendi referans sınıfımızı kur; teşhis okumasını alışkanlık yap | ≥11 video yayında; `olcum.csv` dolu; E1–E2 ilk okuma; ses kararı |
| **2 Çoğalt ve sağlamlaştır** | 16 Kas – 13 Ara (4 hafta) | Çalışanı çoğalt, çalışmayanı bırak; ses geçişi; Dune çıpası hazırlığı | ilk "çatlak" denemesi; ses CC0'a geçti; sezon/cilt politikası oturdu |
| **3 Ölçek kararı** | 14 Ara – 16 Oca (5 hafta) | 90 günlük değerlendirme; uzun video/YPP yolu | Gün 60 ve Gün 90 kararları; 2027 planı |

Gün sayımı: **Gün 0 = Pazar 18 Ekim.** Gün 14 = 1 Kas (Paz), **Gün 28 = 15 Kas (Paz), Gün 60 = 17 Ara (Per), Gün 90 = 16 Oca (Cmt).**

## 3. Faz 0: ilk 72 saat (18–20 Ekim)

| # | Ne | Kim | Süre | Not |
|---|---|---|---|---|
| 1 | **Pellagra kontrolü:** 10 sn'lik kulak kontrolleri ("pelagra", "Misisipi", "yuttu lar", "Goldberger", "dışkısından", "Cevap, tabaktaydı"); YouTube arama kutusunda "pellagra" ve "dışkı yutan doktor" önerileri | **[K]** | 15 dk | Yanlış niyetli öneri baskınsa yedek başlık (`pellagra-mikrop-degildi/yayin_metni.md`) |
| 2 | **Pellagra'yı Pazar 18 Eki 20:00'ye zamanla.** Başlık/açıklama/sabit yorum hazır; açıklamanın sonuna atıf satırı; Studio'da kare 0 küçük resim; "Değiştirilmiş içerik: Hayır"; "Çocuklara özel değil"; oynatma listesi: Ters Köşe Dosyaları | **[K]** | 15 dk | Atıf satırı: *Ses: yapay (Piper TTS; veri seti MaryTTS/DFKI, CC BY-NC-SA 4.0). Çizimler kodla üretilmiştir.* |
| 3 | **Titanik v1'i özel (private) yap** (silme yok) | **[K]** | 2 dk | v2 Salı yayında |
| 4 | **Ses A/B/C** (`ses_testi/lisans_karsilastirma/`): hangisi anlatıcı olabilir? Hangisini seçmezsin? (kör; anahtar `ANAHTAR.txt`, sonra aç) | **[K]** | 5 dk | Karar Gün 28'e kadar yeter |
| 5 | **Antik Mısır, Romalılar, Moğol, Zanzibar'ı özel (private) yap** (öneri) ya da bana durumlarını söyle | **[K]** | 5 dk | Kaynak denetiminden geçenler geri açılır |
| 6 | **Emu sabit yorum** ve **Dans başlık + sabit yorum** düzeltmeleri (metinleri ben yazarım) | **[C]** yazar, **[K]** yapıştırır | 10 dk | §10 |
| 7 | **Kanal vitrini** (§8) | **[K]** | 20 dk | metinler hazır |
| 8 | **K1 (Cuma) ve Ö2 (Pazar) üretimi:** kaynak kapısı, metin, kanca adayları | **[C]** | 2 oturum | §5 |
| 9 | **Pellagra 24. sa okuması** (Pzt 19 Eki 20:00) ve **72. sa okuması** (Çar 21 Eki 20:00): Reach + Engagement ekran görüntüleri | **[K]** ekran, **[C]** `olcum.csv` | 10 dk/okuma | E1 ilk işareti |
| 10 | (Opsiyonel) **Rakip/niş taraması:** Supermetrics "YouTube Public Data"yı bağla; ben niş kanalların son Shorts'larını (süre, görüntülenme, başlık kalıbı) çekip analiz ederim | **[K]** bağlar, **[C]** analiz | 2 dk + 1 oturum | Bağlantı sohbette verildi |

## 4. Haftalık ritim (işletim sistemi)

| Gün | Ne | Kim | Süre |
|---|---|---|---|
| **Pzt** | Haftalık gözden geçirme: önceki Cuma (72. sa), Pazar (24. sa), önceki Salı (7. gün) okumaları → `olcum.csv`; 3 satır karar notu; haftanın konuları | **[K]** ekran + **[C]** | 30 dk |
| Pzt–Çar | Üretim: kaynak kapısı, metin (3 kanca adayı), TTS, sahneler | **[C]** | — |
| Per | QA + kullanıcıya ön izleme/kulak kontrolü listesi | **[C]** → **[K]** | 15 dk |
| **Sal / Cum / Paz 20:00** | Yayın + sabit yorum + ilk saat yorum cevapları | **[K]** | 15 dk + 10 dk/gün |
| Cmt | Tampon ve ertesi haftanın kuyruğu | **[C]** | — |

**Kullanıcı süresi ≈ 3 saat/hafta** (yükleme 45 dk, yorum cevapları 60–90 dk, haftalık okuma 30 dk). **Claude üretimi ≈ 9 saat/hafta** (1 Özel ≈5 saat + 2 Kısa ≈2 saat).

**Yayın öncesi kontrol listesi (kullanıcı, ≤15 dk):** (1) bayraklı sözcüklerin kulak kontrolü; (2) arama kutusu önerileri; (3) başlık ≤60 karakter, vaat önde; (4) açıklama kalıbı + atıf satırı; (5) sabit yorum hazır; (6) Studio'da küçük resim = kare 0; (7) "değiştirilmiş içerik": Hayır; (8) "çocuklara özel değil"; (9) oynatma listesi; (10) zamanlama 20:00; (11) ilgili uzun video varsa Related video; (12) **yalnız ilk yüklemede:** telefonda izle, HUD'un (y≈262) Shorts üst arayüzüyle çakışıp çakışmadığına bak (açık soru, Anayasa §13 bilinmeyenler) ve sonucu bana yaz.

**Yayın sonrası:** ilk saat yorum cevapları; 24./72./7. gün okumaları.

## 5. Yayın kuyruğu

**Slotlar:** Salı–Cuma–Pazar 20:00 (+03) [H]. Her slot bir kulvar (Kısa/Özel) ve bir içeriğe bağlıdır. Kuyruk kaynak kapısına bağlıdır; geçmeyen konu çıkar, sıradaki girer.

| Slot | Tarih | Kulvar | İçerik | Durum |
|---|---|---|---|---|
| 0 | Paz 18 Eki | Özel | **Pellagra** (105 sn, guaj kukla) | hazır |
| 1 | Sal 20 Eki | Kısa | **Titanik v2** (40 sn, mavi baskı; v1 yerine) | hazır |
| 2 | Cum 23 Eki | Kısa | K1: P2 tuhaf olay (aday: Domuz Savaşı 1859 \*) | üretilecek |
| 3 | Paz 25 Eki | Özel | Ö2: **Konya obrukları** (P1/P3; AFAD 741 obruk, Eylül 2026; en yüksek puan) | üretilecek |
| 4 | Sal 27 Eki | Kısa | K2: P1 (aday: iyot, tuz) | üretilecek |
| 5 | Cum 30 Eki | Kısa | K3: P2 (aday: Kova Savaşı 1325 / Boston melas seli 1919 \*) | üretilecek |
| 6 | Paz 1 Kas | Özel | Ö3: **Sığır vebası** (P1; İstanbul 1902 bağlantısı) | üretilecek |
| 7 | Sal 3 Kas | Kısa | K4 | üretilecek |
| 8 | Cum 6 Kas | Kısa | K5 | üretilecek |
| 9 | Paz 8 Kas | Özel | Ö4: **Oralit (ORS)** (P1) | üretilecek |
| 10 | Sal 10 Kas | Kısa | K6 | üretilecek |
| 11 | Cum 13 Kas | Kısa | K7 | üretilecek |
| 12 | Paz 15 Kas | Özel | Ö5: **Sıtma (yeniden)** — Özel + yeni cilt | üretilecek |
| — | **Sal 15 Ara** | Özel | **Dune × Star Wars** (çıpa: *Dune: Part Three*, 18 Aralık 2026 [P]); yayın öncesi ilk kanıt 51. sn → ≤30. sn'ye çekilir | hazır; çıpaya saklanır |

\* Kısa kulvarı için fikirler **doğrulanmamış adaylardır** (kaynak kapısından geçmediler): Domuz Savaşı (1859), Kova Savaşı (1325), Boston melas seli (1919), Serçe kampanyası (Çin, 1958), "Jenkins'in Kulağı" savaşı (1739). Havuz hedefi ≥10 kaynaklı aday (Anayasa §15); haftada +3 aday araştırılır.

**Konu puanları (ilk öneri, [H]; 0–5, Anayasa §15 formülü):**

| Konu | Kanca (×3) | Merak (×2) | Kaynak (×2) | Çizim (×1) | TR (×1) | Çıpa (×1) | Risk | Toplam |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Sığır vebası | 4 | 3 | 4 | 4 | 5 | 1 | −1 | 12+6+8+4+5+1−1 = **35** |
| Oralit (ORS) | 4 | 4 | 4 | 4 | 4 | 1 | −1 | 12+8+8+4+4+1−1 = **36** |
| Konya obrukları | 4 | 4 | 3 | 5 | 5 | 3 | −1 | 12+8+6+5+5+3−1 = **38** |
| Sıtma (yeniden) | 4 | 3 | 5 | 4 | 5 | 1 | −1 | 12+6+10+4+5+1−1 = **37** |
| Kurşunlu benzin | 4 | 4 | 4 | 4 | 3 | 2 | −1 | 12+8+8+4+3+2−1 = **36** (Türkçe'de taze rakip var) |
| Karantina (Osmanlı) | 3 | 3 | 4 | 4 | 5 | 1 | −1 | 9+6+8+4+5+1−1 = **32** |
| İyot | 3 | 3 | 4 | 4 | 4 | 1 | −1 | 9+6+8+4+4+1−1 = **31** |
| Arsenik (Bangladeş) | 3 | 2 | 3 | 3 | 1 | 1 | −2 | 9+4+6+3+1+1−2 = **22** (eşik altı) |

Puanlar yalnız ilk sıralama içindir; kanca adayları ve arama önerisi kontrolü sonrası değişir. **Eşik ≥30 ve risk ≤2.**

## 6. Kulvarlar ve üretim planı

| | Kısa | Özel |
|---|---|---|
| Süre / metin | 35–50 sn, ≤80 sözcük, ≤1,9 sözcük/sn | 75–150 sn, ≤1,8 sözcük/sn |
| Cilt | **önerilen:** guaj kukla kitini yeniden kullan ("sezon 1"), 8–10 videoda | yeni cilt [K] |
| Kaynak tablosu | hafif | tam |
| Hedef süre | ≈2 saat | ≈4–6 saat |
| Haftalık | 2 | 1 |

**Neden "sezon" cildi (Kısa için)?** Kit zaten var (`kukla.py`, `props.py`, `guaj.py`): yeni konu = yeni sahne + yeni rekvizit. Kanalın tanınırlığı için bir "Kısa" yüzü oluşur; Özel'de yeni cilt [K] (anthology kimliği) korunur. Kullanıcı "her video yeni cilt" derse Kısa sayısı düşer (≈1/hafta) ve kadans 2'ye iner.

## 7. Öğrenme planı (deneyler)

Örneklem küçük olduğundan 2×2 yok. Her soru için **bir bilinçli değişiklik**, `yayin_gunlugu.jsonl: not_` alanına yazılır, **aynı yönde ≥3 video** gelmeden kural değişmez.

| # | Soru | Nasıl | Ölçüt | Karar |
|---|---|---|---|---|
| **E1** | Özel (75–150 sn) mi, Kısa (35–50 sn) mı? | iki kulvar zaten dönüşümlü | gösterilme, stayed to watch, ort. izlenme sn ve %, tekrar oranı | Gün 28: ort. izlenme % farkı ≥15 puan (her biri ≥4 video) → iyi kulvarın payı %70 |
| **E2** | Kanca türü: R (çelişki) mu, S (soru) mu? | ardışık iki videoda aynı tür yok | stayed to watch | Gün 60: ≥6 video/tür, fark ≥10 puan + ≥3 aynı yön |
| **E3** | Saat: 20:00 mi, 12:30 mu? | Gün 28'den sonra dönüşümlü | gösterilme (24. sa), stayed to watch | Gün 60 |
| **E4** (Faz 2) | Açılış sesi: 0,05 sn mi, 0,3 sn sessizlik + vuruş mu? | tek değişiklik | stayed to watch | Gün 90 |

**Okuma:** ≥300 gösterilme; referans = aynı kulvarın son 5 videosunun medyanı; <5 puan = ayırt edilemedi; 5–10 ipucu; ≥10 olası etki. Çatlak: 7 günde medyanın ≥10 katı görüntülenme ve stayed to watch ≥%60 → otopsi.

## 8. Kanal vitrini (Faz 0, bir kerelik)

**Kanal açıklaması (öneri, ≤1000 karakter; kadans cümlesi K1 onaylanınca eklenir):**

> Zaman Kuryesi: bildiğini sandığın şeyin ters yüzü. Tarihten, bilimden ve halk sağlığından kaynaklı, sakin tempolu kısa hikâyeler. Her teslimatın başında vaat, sonunda kanıt; kaynaklar sabit yorumda. Haftada üç teslimat: Salı, Cuma, Pazar 20:00. Seslendirme yapay (Piper TTS), çizimler kodla üretilmiştir.

**Varsayılan açıklama şablonu (Studio → Ayarlar → Yükleme varsayılanları):**

```
{vaat cümlesi} · TESLİMAT #{N}
Kaynak: {tek kaynak}
#{etiket1} #{etiket2} #{etiket3}
Ses: yapay (Piper TTS; veri seti MaryTTS/DFKI, CC BY-NC-SA 4.0). Çizimler kodla üretilmiştir.
```

(CC0 sese geçilince son satır: *Ses: yapay (Piper TTS; veri seti CC0).*)

**Kontrol listesi:** 2 adımlı doğrulama açık · varsayılan "çocuklara özel değil" · üç oynatma listesi: *Ters Köşe Dosyaları*, *Tuhaf Olaylar*, *Takvim Çıpası* · kanal açıklaması + bağlantılar · kanal logosu/başlığı (yoksa sade bir tane) · öne çıkan: Pellagra (ilk kez gelenlere).

## 9. Ölçüm ve hedefler

Metrikler ve protokol: Anayasa §8 ve §16, `../olcum/README.md`. **Hedefler "çıta"dır [H]; Gün 14'te baz çizgiyle yeniden yazılır.**

| | Gün 28 (15 Kas) | Gün 60 (17 Ara) | Gün 90 (16 Oca) |
|---|---|---|---|
| Yayınlanan video (kümülatif) | ≥11 (13 slotun ≈%85'i) | ≥23 | ≥35 |
| Medyan stayed to watch (baz Emu %43) | ≥%50; en iyi ≥%60 | ≥%55 | ≥%60 |
| Dağıtım | ≥3 video ≥2.000 gösterilme | ≥1 çatlak | ≥2 çatlak benzeri kalıp |
| Abone (toplam) | ≥50 | ≥250 | ≥500 |
| Abone / 1.000 görüntülenme | ≥2 | ≥3 | ≥3 |
| Doğruluk | yayında bulunan maddi hata = 0 | 0 | 0 |
| Ses | A/B/C kararı verildi | CC0'a geçildi | — |

**Abone ve görüntülenme çıtaları tahmindir;** tek bir çatlak bunları bir günde aşabilir, hiç çatlak çıkmazsa aşılmaz. Bu yüzden asıl ölçüt **oranlar** (stayed to watch, tekrar, abone/1.000) ve **sürecin sağlığıdır** (kadans, kapı süresi, hata sayısı).

## 10. Karar kapıları

| Kapı | Tarih | Girdi | Karar |
|---|---|---|---|
| **G14** | Paz 1 Kas | ilk 5–7 video, Pellagra 7. gün, ses A/B/C | Kadans tuttu mu (≥6/7 slot)? Tutmadıysa haftada 2. Baz çizgi ve çıtalar yeniden yazılır. Kanca/ilk 2 sn sorunu varsa (medyan <%45) yeniden yazım. |
| **G28** | Paz 15 Kas | ≥11 video, E1 ilk okuma | **Format kararı** (Özel/Kısa payı); **ses kararı** (CC0 sese geçiş, hangi ses); cilt politikası (Kısa için sezon onayı); çatlak var mı → otopsi |
| **G60** | Per 17 Ara | ≥23 video, Dune sonucu, ses geçişi | **Ölçek kararı:** uzun video pilotu (16:9, 6–10 dk; Related video köprüsü; watch-hours yolu) evet/hayır; YPP yolu (2027 eşikleri [P] doğrulanarak); sponsor/ticari kullanım için ses kapısı tamam mı |
| **G90** | Cmt 16 Oca | 13 hafta | **Yön kararı:** devam / daralt / yön değiştir; 2027 Q1 planı |

## 11. Karar bekleyenler (kullanıcıya) — öneri ve varsayılan

Cevap gelmezse **varsayılan** uygulanır (üretim durmasın); her karar sonradan değiştirilebilir.

| # | Karar | Öneri / varsayılan |
|---|---|---|
| K1 | **Kadans** | Haftada 3 (Sal/Cum/Paz 20:00); günlük değil (kapasite). Günlük istenirse önce Kısa kulvarı yeniden kullanılabilir cilde taşınır. |
| K2 | **Titanik v1** | Private yap; v2 Salı yayınlanır. |
| K3 | **Eski 4 video** (Zanzibar, Antik Mısır, Romalılar, Moğol) | Private; kaynak denetimini geçerlerse geri açılır. |
| K4 | **Sıtma (#5)** | Yayınlanmaz; Özel + yeni cilt ile yeniden yapılır (Slot 12). |
| K5 | **Dune (#6)** | 15 Aralık'a (Dune: Part Three çıpası) saklanır; yayın öncesi ilk kanıt ≤30. sn'ye çekilir. Alternatif: hemen yayınla. |
| K6 | **Ses** | A/B/C kör testi (5 dk) → Gün 28'e kadar karar; CC0'a geçiş Faz 2'de. Karar gelene kadar `dfki` + atıf satırı. |
| K7 | **Cilt politikası** | Özel: her video yeni cilt [K]; Kısa: "sezon" cildi (guaj kukla kiti). |
| K8 | **Kısa kulvarı** | 35–50 sn, ≤1,9 sözcük/sn (§12-2 ile uyumlu). |
| K9 | **Yayın saati** | 20:00 (+03); E3 ile 12:30 dönüşümlü sınanır. |
| K10 | **Niş/sütunlar** | P1 Ters Köşe Dosyaları ≈%60 · P2 Tuhaf Olaylar ≈%30 · P3 Takvim Çıpası ≈%10. |
| K11 | **Atıf satırı** | Her açıklamanın son satırı (lisans gereği). |
| K12 | **Uzun video pilotu** | G60'a ertelendi. |
| K13 | **Çapraz paylaşım** (TikTok/Reels; aynı dikey dosya) | Faz 2'de dene (Metricool'e marka ekleyerek); YouTube kararlarını bozmaz. |
| K14 | **Rakip taraması** (Supermetrics "YouTube Public Data" bağlantısı) | Yap (2 dk); niş kalıplarını ölçerek E1–E2 sorularını hızlandırır. |

## 12. Risk kaydı

| # | Risk | Olasılık / etki | Önlem | Sahip |
|---|---|---|---|---|
| R1 | Dağıtım yine gelmez (soğuk başlangıç) | orta / yüksek | kadans, ilk 2 sn, G14 teşhisi, Pellagra'nın 72. sa okuması | K+C |
| R2 | Ses lisansı (CC BY-NC-SA) ticari aşamada engel | kesin / orta (gelir yok) | atıf satırı; CC0 geçiş (G28/G60) | K+C |
| R3 | "Özgün olmayan içerik" izlenimi (şablon, TTS, yüksek hacim) | düşük-orta / yüksek (gelir) | Anayasa §14-U1, her videoya özgü görsel, kayıtlar | C |
| R4 | Yayında maddi hata | orta / yüksek | kapı 1, sabit yorumda niteleme, ≤48 sa istisnası | C+K |
| R5 | Kapasite/tükenme (Özel ≈4–6 saat) | yüksek / yüksek | iki kulvar, tampon ≥2, kadans düşer (kapı değil) | C |
| R6 | Uzun Shorts (75–150 sn) dağıtılmaz | orta / orta | E1; Kısa payı artırılır | C |
| R7 | Yanlış arama niyeti | orta / düşük | kapı 4 (arama kutusu) | K |
| R8 | Hassas konu (dışkı, tıp) kısıtlama | düşük / orta | §14-U4: bağlam, uyarı, tıbbi tavsiye yok | C |
| R9 | Platform kuralı değişir (YPP, sayım) | yüksek / orta | §14-U9 üç ayda bir; resmî sayfa okuması (kullanıcı erişimi) | K |
| R10 | Ölçüm eksik kalır (ekran görüntüsü atlanır) | orta / yüksek | Pazartesi 30 dk ritmi; `olcum.csv` | K+C |
| R11 | Hesap güvenliği | düşük / çok yüksek | 2 adımlı doğrulama | K |

## 13. Sürecin tek sayfası

**Her hafta:** Pzt okuma + plan → Pzt–Çar üretim → Per QA + kulak listesi → **Sal/Cum/Paz 20:00 yayın** → ilk saat yorum → `olcum.csv`.
**Her 2 haftada:** kapı (G14, G28 …) ya da kısa gözden geçirme.
**Hiçbir zaman:** kapı gevşetme, yapay etkileşim, kaynaksız mutlak sözcük, tek videodan kural çıkarma.
