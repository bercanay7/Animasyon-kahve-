# KURUL BRİFİ — Medici Parça 1 · TUR 2 (düzeltilmiş sürüm v2)

Sen tur 1'deki üyesin (aynı kod, aynı mercek). Tur 1 raporun `P/kurul/tur1/<KOD>.md`; başkanın kararları `P/kurul/KURUL.md` (kabul edilen, reddedilen ve değiştirilen maddeler, gerekçeleriyle). Yöntem aynı: `/home/user/sisifos-wt/CLAUDE.md` (kurul yöntemi, kapak dersleri). Eşik ≥ 9/10. Bu turda başka üyelerin tur 1 raporlarını OKUYABİLİRSİN (çapraz eleştiri), ama kendi kararını kendin ver.

## Ne değişti (başkanın özeti; doğruluğunu sen sına)
- **Anlatım:** 7 cümle ElevenLabs "Emrullah" sesiyle yeniden seslendirildi ve bölüm sesine örnek düzeyinde yerleştirildi: c1s11 (veba: "yaz boyunca"), c1s16 (Salvestro "kurayla", Mayıs 1378), c1s18 ("ve Salvestro çekildi" kalktı), c1s23 ("en kanlı gün" yerine lonca kaldırıldı/dışlandılar), c1s24 ("Medici'nin bu kolu"), c2s7 (Tim Parks), c2s27 ("torununun oğlu Lorenzo"). Machiavelli III–IV birincil metinle doğrulandı (Gutenberg #2464). Birincil kaynak teyit tablosu: `P/kurul/teyit_P1.md`.
- **Motor:** plaka genişliği/güvenli alan/HUD kıskacı (ekran uzayında), HUD küçüldü, dönem katmanı (`donem.py`: kubbe/çan kulesi/arma/bayrak/madalya yazıtı HUD yılına göre), `qa_yerlesim.py` ve `qa_donem.py`, geçiş süreleri 0,25–2,4 sn ve sert kesme, seçici hareket bulanıklığı (deklanşör), kamera çeşitliliği, `anim.py` (hazırlık/oturma/sarsıntı/damga), figür temas gölgesi, madalya portreleri, kontrast scrim'i, `qa_flow` yeni kapıları. Ayrıntı: `P/notlar_hareket.md`, `P/notlar_donem.md`.
- **Sahneler:** c2 "kart vadisi" figürlü dünya sahnelerine çevrildi; c0 açılışında kapak yankısı; c1 dönem ve Ciompi düzeltmeleri; ekran metinleri, kontrast ve altyazı bandı düzeltmeleri. Kapanan maddeler listesi sahne yazarının raporunda: `P/notlar_c0.md…notlar_c2.md`.
- **Kodlama:** BT.709 renk matrisi düzeltildi; slow/aq-mode 3; VBV 24M/48M; `-shortest` kaldırıldı.
- **Kapak:** K1 "SON MEDİCİ / MİRASI KİLİTLEDİ", K2 "FAİZ YASAKTI" (`P/yayin/studio_paketi_P1/kapak_P1_K1.jpg`, `_K2.jpg`; denetim `P/out_p1/kapak/kapak_qa_P1.png`).
- **Paket:** başlık "Medici Ailesi (1/7): Faiz Yasakken Nasıl Zengin Oldular?", yeni açıklama/sabit yorum/etiket/bölümler (`P/yayin/studio_paketi_P1/`), altyazı (yetim replikler, okuma hızı, bölünme kuralları).

## Kanıt
- Video: `P/out_p1/medici_P1.mp4` (v2). Tur 1 sürümüyle karşılaştırmak istersen başkandan iste (v1 silinmiş olabilir; tur 1 kareleri `P/out_p1/kurul/` yerine `P/out_p1/kurul_v1/` altında saklandı).
- Yeni kanıt paketi: `P/out_p1/kurul/` (aynı adlar: genel_*, gecis_*, tam_*, hareket.json, teknik.json, qa_flow_ozet.txt) + `qa_yerlesim.json`, `qa_donem.json`.

## Rapor biçimi (`P/kurul/tur2/<KOD>.md`)
1. **Karar + puan** (ONAY ≥ 9 / RED).
2. **Tur 1 maddelerinin durumu:** kendi tur 1 listendeki HER madde için: kapandı / kısmen / açık / reddedildi (başkan gerekçesiyle) + kanıt (kare/zaman).
3. **Yeni sorunlar** (düzeltmelerin getirdiği gerilemeler dahil): kare/zaman + koordinat + ne yapılmalı + önem.
4. **Kullanıcının sorusu — açıkça yanıtla (alanına göre 3–6 cümle):** "Bu çizim tarzı çok mu basit, ucuz görünüyor; yapay zekâ ile üretilmiş gibi mi duruyor?" Neyin ucuz/şablon/YZ gibi okunduğunu ve neyin okunmadığını somut karelerle söyle; varsa düzeltme öner.
5. **En emin olmadığım nokta.**

Kurallar: yalnız `P/kurul/tur2/<KOD>.md` dosyanı yaz (ve scratch). Diğer dosyalara dokunma, git kullanma, render yok; ffmpeg ile kare çıkarma ve küçük Python serbest; aynı anda tek ağır işlem. Sesi dinleyemediğini ve videoyu oynatamadığını belirt.
