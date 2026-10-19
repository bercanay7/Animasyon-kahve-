# Görev: Medici c6–c16 metinleri için BAĞIMSIZ gerçeklik / ton / seslendirilebilirlik incelemesi

Türkçe çalış. Rapor: `inceleme_c6_c16.md` (bu klasörde). **scr_c*.py dosyalarına DOKUNMA** (ana ajan uygulayacak); önerilerini cümle kimliğiyle ve TAM yedek cümleyle yaz.

## Bağlam
"Zaman Kuryesi" kanalının Medici belgeseli (17 bölüm c0–c16, 7 yayın parçası). Anlatı Stefan Zweig / Plutarkhos / Emrah Safa Gürkan tonunda: popüler dil, ölçülü günlük konuşma, küfür yok, ağır sahnelerde mizah KAPALI, iç dünya yalnız kaynaktan (uydurma diyalog/iç monolog yok), "uzak profesör" yok. Cümle ortalama 14–18, üst sınır 28 sözcük. Metin `script.py` + `scr_c0.py … scr_c16.py` içinde; cümle biçimi `(görüntü_metni, söylenen_metin_veya_None, "sınıf kaynak-etiketi")`; sınıflar ● (birincil okundu — bu ortamda HİÇBİRİ), ◐, ○, ANEKDOT, YORUM, MİT, HAFIZA. Her bölümün docstring'i ruh hâli/mizah izni/tuzakları söyler.

**c0–c5 için GERÇEK ses üretildi (değişiklik pahalı/yama gerekir) — onları İNCELEME DIŞI bırak** (yalnız c6'nın c5'ten kapıya uyumuna bak). **c6–c16 için ses HENÜZ ÜRETİLMEDİ → metin değişikliği şimdi ücretsizdir; hataları şimdi yakalamak değerli.**

## Okuyacakların
- scr_c6.py … scr_c16.py (ana inceleme nesnesi); brif/c6_brif.md … c16_brif.md (özellikle §3 mizah, §5 tuzaklar, §7 ekran/akış, §10 eksikler); arastirma/*.md (M1–M5, M2c, M4c — olgu dayanağı); kaynaklar_P3.md … kaynaklar_P7.md (sınıf dağılımı + yayın öncesi teyit listesi); KAPSAM_VE_YAPI.md; USLUP_REHBERI.md; script.py (PRON okunuş kuralları, rakam/ordinal dönüşümü).
- Yayın parçaları (kullanıcı kararı): P3=c6–c7 · P4=c8–c9 · P5=c10–c11 · P6=c12–c13 · P7=c14–c16. Her parça kendi başına, öncesini görmemiş izleyiciye de açılır: **c8, c10, c12, c14 parça açılışlarıdır** (c6 de: P2'den bir hafta sonra). İlk 2 cümle, kim/ne zaman/nerede bağlamını (önceki bölümü görmeden) kurmalı mı? Gerekiyorsa EN KÜÇÜK düzeltmeyi öner (mevcut güçlü açılışları bozma).

## Yapılacaklar
1. **Olgu denetimi (öncelik 1):** Her bölümde ad/tarih/sayı/unvan/yer/nedensellik iddialarını araştırma dosyalarıyla ve kendi bilginle karşılaştır; çelişki, abartı ya da kaynakla desteklenmeyen kesin ifade bul. Emin olmadığın yerde WebSearch (mode "standard") ile doğrula (WebFetch bu ortamda çalışmıyor; arama özetleri ◐/○ düzeyidir — kanıt gücünü dürüstçe yaz). Özellikle: tarih/yaş uyuşmaları (iç tutarlılık: bölümler arası aynı olgu aynı biçimde mi?), sayılar (florin, askerler, yıllar), "ilk/tek/en" iddiaları, Pazzi suikastı ayrıntıları (c7), aforoz/interdikt/Napoli (c8), Osmanlı bağlantıları (Bandini, Otranto, Mehmed II'nin ölümü — HAFIZA-Y satırları), şapa/şube kapanışları (c9), Savonarola/Charles VIII/1494–98 (c10), Leo X/Clement VII/1527/kuşatma/Alessandro (c11), Cosimo I/Uffizi/İnebahtı (c12), Catherine/Marie/Rubens/çatal-dondurma-zehir mitleri (c13), Galileo/matbaa/Euridice/piyano/pietre dure (c14), Livornina/Mustafa Ağa/Fahreddin/Francesco I DNA çalışması/Gian Gastone (c15), 1737/1743 sözleşmesi (c16).
2. **Ton / üslup:** mizahın yeri (kapalı olması gereken sahnelerde şaka var mı?), uydurma iç dünya, kaynaksız duygu/diyalog, didaktik/demagojik cümleler, argo ölçüsü, tekrarlayan kalıplar (aynı espri/yapı çok kez), bölüm içi ritim (uzun cümle yığılması), "kapı" cümlesi (bölüm sonu) gücü.
3. **Kaynak sınıfı etiketleri:** ◐/○/ANEKDOT/MİT/YORUM doğru mu? Rivayet olan şey kesin anlatılmış mı? ("Aktarıldığına göre/rivayet" işaretleri var mı?)
4. **Seslendirilebilirlik (ElevenLabs eleven_v4, Türkçe):** yabancı özel adların okunuşu (PRON listesi eksik/yanlış mı), rakam→söz dönüşümü, ordinal ("19. yüzyıl"), kısaltma, kafa karıştıran noktalama, ünlem/soru kökleri, çok uzun cümle, tek sesli okunamayacak ifade (parantez, tırnak içi yabancı sözcük). Yanlış okunma riski taşıyan her yer için PRON satırı önerisi (regex + okunuş).
5. **Parça sınırı kancaları:** her parçanın son bölümünün kapısı (P3 sonu c7, P4 sonu c9, P5 sonu c11, P6 sonu c13) ve sonraki parçanın açılışı (c8, c10, c12, c14) ardışık okununca akıyor mu? Önerin varsa asgari değişiklik.

## Çıktı biçimi (`inceleme_c6_c16.md`)
- Özet tablo: bölüm başına `K1` (kesin hata/yayını engeller), `K2` (olası hata/zayıf dayanak), `K3` (ton/üslup), `K4` (okunuş) sayıları.
- Her bulgu: `[K?] cNsM` · sorun (1–2 cümle) · gerekçe/kanıt (kaynak dosya adı ya da arama özeti; kanıt gücü ◐/○) · **önerilen yedek cümle (TAM, script biçiminde `(görüntü, söylenen/None, "sınıf etiket")`)**.
- Sonda: "kullanıcıya yayın öncesi teyit" kısa listesi (sayfa düzeyinde doğrulanması gereken 10–15 kalem).
- Küçük zevk meselelerini listeleme; yalnız fark yaratanları yaz. Önerilerin toplam kapsamı ≈ ≤40 cümle olsun.

## Kurallar
- Dosya yazma: yalnız `inceleme_c6_c16.md` (ve gerekirse `/tmp` çalışma dosyaları). git KULLANMA. CPU'yu meşgul eden iş çalıştırma (render yok; yalnız okuma/arama/küçük Python). Başka ajanlar çalışıyor.
- Dürüst ol: ● düzeyinde teyit yapamıyorsan söyle; tahmini kesin gibi sunma.
- Bittiğinde kısa Türkçe rapor ver (K1/K2 sayıları ve en önemli 5 bulgu).
