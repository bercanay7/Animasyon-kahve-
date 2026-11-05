# KURUL BRİFİ — Medici Parça 1 · TUR 3b (v3.1 gerileme kontrolü)

Tur 3'teki üyesin. Kodun, merceğin ve yöntemin aynı (`/home/user/sisifos-wt/CLAUDE.md`). Eşik ≥ 9/10. Kendi tur 3 raporun `P/kurul/tur3/<KOD>.md`. Başkanın tur 3 kararları `P/kurul/KURUL.md` → "Tur 3 — v3 sınaması" bölümünde.

**Bu turun işi dar.** Yeni bir genel inceleme değil:
1. Tur 3 raporundaki **açık, kısmen ve yeni** maddelerini v3.1'de tek tek sına.
2. v3.1 değişikliklerinin **senin alanında** getirdiği gerilemeleri ara.
3. Kararını ver.

Gözüne çarpan yeni ve önemli bir sorunu yine yazmak zorundasın.

## v3.1'de ne değişti (iddia; sen doğrula)
- **Tam liste ve kim yaptı:** `P/kurul/tur3_duzeltme_listesi.md` (madde numaraları raporlarda geçer).
- **Ajan raporları (dosya:satır ve önce/sonra kanıtı):** `P/kurul/duzeltme_tur3/SCN-3.md` (c2, defterler, eller, bağlantılar) ve `P/kurul/duzeltme_tur3/ENG-E.md` (motor, c0/c1, doku, yankı, 1737 belgesi).
- **Kanıt kareleri:** `P/out_p1/duzeltme/tur3/<AJAN>/`.
- **Başkan:** 
  - render.py: kod özeti, birleştirme öz sınaması, H.264 seviye 4.1;
  - paket: bitiş ekranı 9:53, P2 günü satırları;
  - sahne düzeltmeleri bf1645b / e7d6e73 / f0bdaad.
- **Değişmeyenler:** ses, anlatım ve altyazı (`timeline.json` aynı).
- **Üretim:** v3.1 bütünüyle yeniden üretildi (tam render; kısmî birleşim yok).

## Kanıt
- **Video:** `P/out_p1/medici_P1.mp4` (**v3.1**; süre, LUFS, peak ve kod özeti `P/out_p1/uretim_v31.log` içinde; v3 dosyasının üstüne yazıldı).
- **Akış/yerleşim/dönem denetimleri:** `P/out_p1/qa_flow_v31.txt`.
- **Kanıt paketi:** `P/out_p1/kurul/` (v3.1 için yeniden üretildi).
- **Paket:** `P/yayin/studio_paketi_P1/`. **Altyazı:** `P/yayin/medici_P1_tr.srt` (değişmedi).

## Rapor (`P/kurul/tur3b/<KOD>.md`; kısa)
1. **Karar + puan:** ONAY ≥ 9 ya da RED.
2. **Tur 3 maddelerimin durumu:** her açık/kısmen/yeni madde için kapandı / kısmen / açık ve kanıt (zaman, kare, koordinat).
3. **v3.1 gerilemeleri:** her biri için zaman, koordinat, ne yapılmalı, önem.
4. **En emin olmadığım nokta.**

**Kurallar:**
- Yalnız `P/kurul/tur3b/<KOD>.md` dosyanı yaz; scratch serbest.
- git yok, render yok.
- ffmpeg ile kare çıkarma ve küçük Python serbest; aynı anda tek ağır işlem.
- Sesi dinleyemediğini ve videoyu oynatamadığını belirt.
- Disk sınırlı: kare dökümlerini iş bitince sil; yalnız raporda andığın kanıtları tut (JPEG, her biri ≤1 MB).
