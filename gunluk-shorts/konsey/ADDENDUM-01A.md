# EK 01A: DOSYA 01'e düzeltmeler

**Wins over DOSSIER-01-kanal-yonu.md and earlier addenda where they conflict (DOSSIER-01-kanal-yonu.md ve önceki eklerle çelişkide bunun dediği geçerlidir).** Yalnız düzeltme ve ölçüm içerir. Hiçbir üyenin tutumu, oyu veya gerekçesi burada yer almaz.

Maddeler önceki eklerden devam eden sürekli numara taşır (bu ekte 1–11).

## 1. F2/E7: "izlenme" sayısının metriği belirsiz; Shorts sayım kuralı değişti

- **Dosya şunu dedi:** Emu ≈1700, Dans ≈100 "izlenme" (F2); E7 platform kurallarının değiştiğini söyleyip ayrıntı vermedi.
- **Doğrusu:** YouTube, 31 Mart 2025'ten itibaren Shorts görüntülenmesini "oynatma başladığında" sayıyor (önceki minimum izlenme eşiği kalktı); eski ölçüt Analytics'te "Engaged views" adıyla duruyor. Dosyadaki 1700 ve 100 sayılarının hangi metrik, hangi tarih ve hangi pencereyle alındığı belli değil; ham görüntülenme ile "engaged views" karışmış olabilir. İkincil kaynaklara göre 24 Ağustos 2026'dan itibaren sayımın tüm biçimlerde "ilk karede" yapıldığı da bildirilmiş; bu resmî sayfadan okunamadı (UNVERIFIED).
- **Kaynak:** VERIFICATION.md V36 (WebSearch özetleri; resmî Help sayfası okunamadı).
- **Bulan:** doğrulayıcı; buyume, topluluk, seo, analitik, izleyici, qc, senarist, kanca, motion.
- **Önemi:** Soru 7 ve tüm seçenekler (karar metriği).

## 2. E7: Shorts azami süresi 3 dakika; 40 sn bir tercih

- **Dosya şunu dedi:** Süre kuralları değişti (belirsiz).
- **Doğrusu:** Shorts üst sınırı 15 Ekim 2024'ten beri 3 dakikadır. ~40 sn platform sınırı değil, kanalın seçimidir.
- **Kaynak:** VERIFICATION.md V36/V37 (ikincil kaynaklar ve YouTube Help parçaları).
- **Bulan:** doğrulayıcı; buyume, topluluk, seo, analitik, senarist, kanca, motion, qc.
- **Önemi:** Soru 4 (tempo/uzunluk).

## 3. F7: ilk kare ölçümü (kare çıkarıp bakıldı)

- **Dosya şunu dedi:** Dans'ta ilk karede büyük başlık/kanca kartı yoktu (hatırlamaya dayalı, doğrulanmamış).
- **Ölçülen:** 0. kareler `konsey/ilk_kareler_kanit.png` içindedir. **Dans:** ilk karede kâğıt-kesme sokak sahnesi ve küçük "DANSÇI 1" sayacı var; kanca metni yok, anlatım yazısı ilk kelimede beliriyor ("Bir kadın"). **Emu:** ilk karede büyük "ORDU 0 – EMU 1" skor tabelası ve "MERMİ 9.860" sayacı var. **Zanzibar:** ilk karede saat kadranı ve "00:00" sayacı var, metin yok. **Titanik:** ilk karede büyük başlık kartı var (önceki ölçüm).
- **Kaynak:** videolardan ffmpeg ile çıkarılan 0., 12. ve 48. kareler; VERIFICATION.md "videolar" iddiaları.
- **Bulan:** qc, illustrator, motion, izleyici (doğrulanmamış diye işaretlediler); ölçümü kolaylaştırıcı yaptı.
- **Önemi:** E1 (Emu–Dans farkı), Soru 4.

## 4. F4: "kuru oran ~%8,5" yanlış etiket

- **Dosya şunu dedi:** Yankı "kuru oran ~%8,5".
- **Doğrusu:** Kodda `reverb_wet=0.085` yankılı (ıslak) paydır; karışım formülü etkin ıslak kazancı yaklaşık %13,6 yapar (`wet * 0.085 * 1.6`). Yani sinyalin ~%91,5'i kuru değil; bu oran önceki sürümlerde duyulan yankıyı açıklayabilir. Kadın/kuru sürümde ıslak pay 0 olarak ayarlıdır.
- **Kaynak:** VERIFICATION.md V45; `gunluk-shorts/ses-lab/narrator.py`.
- **Bulan:** doğrulayıcı; seslendirme, dil.
- **Önemi:** Soru 3 (ses).

## 5. F4: "Whisper kelime hata oranı ~%20" ölçüm sınırı

- **Dosya şunu dedi:** Anlaşılırlık ölçümü ~%20.
- **Doğrusu:** Ölçüm Whisper'ın kendi hatasını TTS hatasından ayırmıyor; rakamlar ve yabancı adlar normalize edilmemiş; hangi videoda kaç kelime ölçüldüğü kayıtlı değil. Sayı "TTS %20 hatalı" olarak okunamaz. Yeniden çalıştırma yapılmadı (UNVERIFIED).
- **Kaynak:** VERIFICATION.md V46; `ses-lab/check_voice.py`.
- **Bulan:** doğrulayıcı; dil, qc, seslendirme.
- **Önemi:** Soru 3, Soru 6.

## 6. C1 Emu Savaşı: sayılar komutanın öz-bildirimidir

- **Dosya şunu dedi:** ~20.000 emu, ~10.000 mermi, ~1.000 emu öldürüldü, kuş başına ~10 mermi, zikzak, 50 km/s, ordu geri çekildi.
- **Doğrusu:** "~1.000 emu / ~10 mermi" komutan Meredith'in kendi raporundaki sayımdır (986 emu, 9.860 mermi) ve tartışmalıdır; ilk fazda 2.500 mermiyle 50–200 emu bildirilmiştir (bu fazın oranı 12–50 mermi/kuş). Görev gücü üç kişi ve iki Lewis makineli tüfeğidir; videoda "ordu" deniyor. "Zikzak" ifadesi arama özetlerinde bulunamadı (UNVERIFIED). ~20.000 kuş, ~50 km/s ve kuşların küçük gruplara bölünmesi doğrulandı; ordunun geri çekilişi doğrulandı (operasyon ikinci kez sürdü).
- **Kaynak:** VERIFICATION.md V3–V11; olgu koltuğu raporu §2.
- **Bulan:** doğrulayıcı; olgu, topluluk.
- **Önemi:** Soru 1, 6 (kaynak/doğruluk standardı).

## 7. C2 Titanik/Futility: nitelemesiz iddialar ve "kehanet" çerçevesi

- **Dosya şunu dedi:** İkisi de "batmaz" diye tanıtıldı, sancak tarafı, 24/20 bot, 244/269 m, "6 benzerlik".
- **Doğrusu:** Titan 800 ft (244 m), Titanic 882 ft 9 in (269 m) ve romanda 24 bota karşı Titanic'te 20 bot doğrulandı. Roman 1912'de gözden geçirilip yeniden basılmıştır (deplasman 45.000 tondan 70–75.000 tona çıkarıldığı bildirilmiş); 800 ft ve 24 bot değerlerinin hangi baskıdan geldiği doğrulanamadı. "Batmaz tanıtıldı" Titanic için tartışmalıdır (1911 basını ve The Shipbuilder "practically unsinkable" diyor). "Sancak tarafı" ifadesi tek aramada bulunamadı (UNVERIFIED). "6 benzerlik" yazarın seçtiği bir sayımdır.
- **Kaynak:** VERIFICATION.md V16–V21; olgu koltuğu raporu §2.
- **Bulan:** doğrulayıcı; olgu, senarist, seo, kanca.
- **Önemi:** Soru 1, 5 (başlık ve kanca-vaat uyumu).

## 8. C4 Dans Salgını: kişi sayısı üst sınır, ölüm iddiaları geç kaynaklı

- **Dosya şunu dedi:** ~400 kişi dans etti; bazıları öldü.
- **Doğrusu:** ~400, 50–400 aralığının üst sınırıdır; ölüm iddiaları sonraki kroniklerden gelir, dönemin Strazburg kayıtları ölümü belirtmez. "Bir haftada 34 kişi", müzik yasağı ve türbe ayrıntıları doğrulanamadı.
- **Kaynak:** VERIFICATION.md V28–V33.
- **Bulan:** doğrulayıcı; olgu.
- **Önemi:** Soru 1, 6.

## 9. F4/F6: bayat QA raporu; ses seviyesi ölçümü

- **Dosya şunu dedi:** Her videoda otomatik QA vardır (F6).
- **Doğrusu:** Emu'nun `qa_raporu.txt` dosyası bayattır (960 kare yazıyor; teslim edilen video 12 Ekim'de yeniden render edilmiş: 1032 kare / 43 sn). LUFS ölçümü `qa.py`'de değil `audio.py`'dedir; ölçülen: Emu −14,1, Titanik −14,0 LUFS. QA yalnız teknik ölçümleri yapar (kare, boş kare, HUD, ilk/son kare, hareket, LUFS); kanca, telaffuz, kaynak ve telefonda okunabilirlik denetimi içermez.
- **Kaynak:** VERIFICATION.md V47–V49 (ffprobe, kod okuması).
- **Bulan:** doğrulayıcı; qc.
- **Önemi:** Soru 6.

## 10. Kontrol edilemeyen bilgiler (açık)

- **Dosya şunu dedi:** HUD y≈260 ve "alt %25 güvenli alan" yeterli güvenli alan tarifidir.
- **Doğrusu:** Alt %25'in yanında üst ve sağ kenarlarda da Shorts arayüzü vardır; HUD (y≈260) üst arayüz bölgesine girebilir. Resmî bir ölçü bulunamadı, üçüncü taraf kaynaklar çelişiyor. Bu açıktır; kural olarak yazılırsa deneme ile doğrulanmalıdır. Piper modellerinin "erkek" etiketi yalnız üçüncü taraf bir siteden doğrulanmıştır.
- **Kaynak:** renktipo raporu §2; VERIFICATION.md V41.
- **Bulan:** renktipo; doğrulayıcı.
- **Önemi:** Soru 3, 4.

## 11. Dosyada olmayan kayıtlar

- **Dosya şunu demedi:** (eksik) Dört videonun başlık, açıklama, yayın saati ve yayın tarihi; video metinleri; Studio'daki tutma eğrisi, kaydıran oranı ve trafik kaynakları; yorum sayısı. Bunlar bizde yok; bulunacak yer YouTube Studio ve `*/tts.py`/`yayin_metni.md` dosyalarıdır ("aranmadı" ile "yok" aynı şey değildir).
- **Kaynak:** DOSSIER bölüm 6; birden çok üye raporu.
- **Bulan:** seo, topluluk, analitik, qc, dil.
- **Önemi:** Soru 7.

## Kaydedilen ama karara bağlanmayan anlaşmazlıklar

Olgusal bir ölçüm anlaşmazlığı yok. (Tutum ayrılıkları tally'de, bu ekte değil, kaydedilir.)

## Sürekli talimat

Bu kaydı da kontrol edin. Başka bir şey bulursanız bildirin; tartışmak yerine kaynağı kontrol etmeyi veya analizi çalıştırmayı tercih edin.
