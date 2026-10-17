# Ölçüm günlüğü (Kanal Anayasası §8 ve §16)

`olcum.csv` her video için **okuma başına bir satır** tutar. Üretim/yayın olguları (kulvar, kanca türü, bilinçli değişiklik) `../yayin_gunlugu.jsonl`'dadır; **metrikler burada**. Başlangıç satırları 2026-10-14 Studio ekran görüntülerinden (`../konsey/veri/`) alındı; boş hücre = bilinmiyor.

## Ne zaman okunur (her video için 3 okuma)

| Okuma | Zaman | Amaç |
|---|---|---|
| **24. sa** | yayından 24 saat sonra | işaret; dağıtım (gösterilme) başladı mı |
| **72. sa** | 72 saat sonra | **okuma**; stayed to watch, ort. izlenme, tekrar |
| **7. gün** | 7 gün sonra | **karar**; trafik kaynağı, abone, çatlak mı |

## Studio'da nereden alınır (telefon/masaüstü)

Content → videoyu aç → **Analytics**:
- **Reach:** *Shown in feed* (gösterilme), *Viewed vs swiped away*, trafik kaynakları (Shorts akışı / arama / kanal sayfası), arama terimleri.
- **Engagement:** *Stayed to watch*, *Average view duration* (sn ve %), *Engaged views*, *Unique viewers*, tutma eğrisi.
- Kanal toplamı: Channel analytics → Overview (28 gün).

Ekran görüntüsünde **metrik adı ve tarih görünsün**; dosya adı `video_okuma_metrik.png` (ör. `pellagra_72sa_reach.png`), `konsey/veri/` veya `olcum/ekran/` altına.

## Sütunlar

| Sütun | Anlam |
|---|---|
| `video_no`, `baslik_kisa`, `yayin_tarihi`, `yayin_saati` | kimlik |
| `kulvar` | `K` Kısa (35–50 sn) / `O` Özel (75–150 sn) |
| `sure_sn`, `cilt`, `kanca_turu` | `R` çelişki / `S` soru |
| `kaynak_sinifi` | ● birincil / ◐ ≥2 ikincil / ○ (Anayasa §5) |
| `okuma`, `okuma_tarihi` | `24sa`, `72sa`, `7g` ya da "yayından beri" |
| `gosterilme` | Shown in feed (sayı) |
| `stayed_to_watch_pct`, `swiped_away_pct` | Viewed vs swiped away |
| `ort_izlenme_sn`, `ort_izlenme_pct` | Average view duration / % |
| `views`, `engaged_views`, `unique_viewers` | `tekrar_orani` = views ÷ unique_viewers |
| `abone_kazanimi`, `begeni`, `yorum` | etkileşim |
| `akis_pct`, `arama_pct`, `kanal_sayfasi_pct` | trafik kaynağı payları |
| `tutma_notu` | eğrinin gözle okunan özeti (ilk 3 sn, ilk 10 sn, ortası, sonu) |
| `not` | n<300 etiketi, ek gözlem, bilinçli değişiklik |

## Okuma kuralları (özet; ayrıntı Anayasa §8)

- **≥300 gösterilme** olmadan oran okunmaz (`not`: "n<300"); 300'de %43'ün %95 aralığı ≈ ±5,6 puan, 1.000'de ≈ ±3,1.
- Referans: **aynı kulvarın son 5 videosunun medyanı.** <5 puan = ayırt edilemedi; 5–10 = ipucu; ≥10 = etki olası. **Tek video kural değiştirmez** (≥3 aynı yönde).
- **Çatlak:** 7 günde kanal medyanının ≥10 katı görüntülenme **ve** stayed to watch ≥%60 → otopsi (kanca, süre, tempo, konu, ses, saat).
- "Views" kalite ölçütü değildir (24 Ağustos 2026'dan beri tüm biçimlerde ilk karede sayılır [P]).

## Haftalık gözden geçirme notu (Pazartesi, ≤30 dk; `YOL_HARITASI.md` §4)

```
Hafta: YYYY-MM-DD
Okunan: <video> (72sa) · <video> (24sa) · <video> (7g)
Ne kalıyor: …
Ne değişiyor (en çok 1 bilinçli değişiklik): …
Bu haftanın konuları: …
Çatlak/ipucu: …
```
