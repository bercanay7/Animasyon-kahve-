# Okunuş notları ve ses kapısı (Piper `fahrettin`)

Güncelleme: 2026-10-18 (Pellagra yeniden seslendirmesi). Shorts/Özel anlatıcısı `fahrettin` (kullanıcının kör test seçimi; veri seti CC0, taban model belirsizliği için Anayasa §4).

## Jeton işareti (`narrator.py`)

- `gösterilen=söylenen` · `_` = boşluk · `*vurgu*` · virgül/iki nokta/nokta = parça sınırı (her parça **ayrı** sentezlenir, duraklar `gap_*`).
- **Kelime dizini** = boşlukla ayrılmış jeton sırası. Sahne/ses işaretleri (`wt("F2", 4)` gibi) buna bağlıdır; bu yüzden `doktor_Goldberger` **tek jetondur** (ekranda “doktor Goldberger”, dizinler kaymaz).

## fahrettin ile bulunan okunuş çözümleri (Whisper-medium, aynı ifade 6 sentez; `okunus_dene.py`)

| Sorun | Çözüm | 6 dinlemede doğru |
|---|---|---|
| “Goldberger” parça/cümle başında “Bold…” / “Gold Ballyer” duyuluyor | ünvanla başlat: `Doktor_Goldberger` | 4–5 (öncesi 0–1) |
| `pellagra=pelagra` → “pelabre”, “pelabe” | `pellagra=pelagıra` | 5 |
| “tabaktaydı” → “tabartaydı”, “tabahtaydı” | `tabaktaydı=tabakta_idi` | 4 |
| tek kelimelik “Mikrop,” cümle içinde “Mikrofon” | zor sözcük kapısı (aşağıda) | 5 |
| “eksikliğiydi” cümlede “eksik iyiydi” | zor sözcük kapısı + yeniden örnekleme | — |

Genel desen: **yabancı ad cümle/parça başında bozuluyor; önüne gelen bir sözcük (ünvan) onu kurtarıyor.** Sessiz-sessiz kümeleri (`gr`, `kt`) kısa bir ünlüyle (`pelagıra`) açmak işe yarıyor. Tek hece/tek kelimelik parçalar en kırılgan olanlar.

## Kalite kapısı (`pellagra-mikrop-degildi/tts_best.py`, yeni videolara kopyalanır)

1. Her parça K=5 kez sentezlenir, Whisper'ın en doğru yazıya döktüğü seçilir; en iyi aday hâlâ kötüyse (WER ≥ 0,3 ya da zor sözcük duyulmadıysa) KMAX=15'e kadar sürer.
2. Adaylar **karışımdaki gibi vurgu işlemesinden geçirilip** dinletilir (`_shape`): vurgulu sözcüğün parlaklık eklemesi ham seste doğru duyulan “pellagra / tabaktaydı”yı bozabiliyordu.
3. **Zor sözcük listesi** (`MUST`, regex): Whisper bu sözcüğü duymak zorundadır; duymayan aday elenir (“Boldberger”, “pelabre”, “mikrofon”, “tabartaydı”, “eksik iyiydi” kabul edilmez). Zor sözcük içeren parçalar iki farklı seviye/boşlukla dinlenir, ikisi de geçmelidir.
4. Parça önbelleği `out/_chunk_cache/` (git'e girmez): metin değişince yalnız değişen parçalar yeniden sentezlenir. Belirli parçaları zorla yeniden denemek: `RETRY="parça metni|başka" python3 tts_best.py 5`.
5. `dogrula.py`: karışık sesi cümle sınırlarından keser, Whisper'a verir (ortalama WER, duyulmayan zor sözcük sayısı).

**Sınır:** Whisper bir kulak değildir. Okunabilirliği ölçer, sesin *doğallığını ve sıcaklığını* ölçmez; Anayasa kapısı “insan kulağı kontrolü” yerine geçmez.

## Yeni videoda

1. Yeni özel ad / zor sözcük için `python3 okunus_dene.py fahrettin "<ifade>" "<alternatif>"` ile 3–4 yazılış dene (6 dinleme).
2. Güvenilir biçimi `tts.py`'ye yaz; sözcüğü `tts_best.py` içindeki `MUST` sözlüğüne (kabul edilen duyuşların kalıbı) ekle.
3. `python3 tts_best.py 5` → `python3 dogrula.py` → miks; cümle düzeyinde “duyulmayan zor sözcük” sayısı **0** olmalı.
