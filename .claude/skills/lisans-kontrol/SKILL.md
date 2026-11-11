---
name: lisans-kontrol
description: Yeni açık kaynak kütüphane, font, ikon, ses veya görsel eklemeden önce lisans kontrolü ve araclar/ASSETS.md kaydı. Dışarıdan herhangi bir varlık/paket eklerken (monetize YouTube için) mutlaka kullan.
---
# Lisans kontrolü

YouTube kanalı monetize → **ticari kullanım şart**. Eklemeden önce: lisansı kaynağından oku (README/LICENSE/npm), `araclar/ASSETS.md`'ye satır ekle (ad · sürüm · kaynak URL · lisans · şart/atıf · tarih).

| Lisans | Karar |
|---|---|
| CC0, MIT, ISC, Apache-2.0, OFL | Serbest (MIT/ISC/Apache: lisans metnini dosyayla tut) |
| CC-BY | Atıf gerekir → video açıklamasına yaz |
| CC-BY-SA | Atıf + aynı lisans; videoda kullanımı için dikkat (OpenMoji) |
| **NC (non-commercial)** | YASAK (Piper-TR, XTTS, MMS) |
| GPL/AGPL | Araç olarak yerelde çalıştır; ürüne/yayına gömme (lottie-py AGPL, pedalboard GPL) |
| Ticari/kısıtlı (Spine, Live2D, Remotion şirket lisansı) | Kullanma / ekip büyüklüğüne göre kontrol |
| GSAP "no charge" | Kullanılabilir (MIT değil; rakip animasyon aracı yapma) |

Doğrulayamadığın lisansı "serbest" varsayma; ASSETS.md'ye **"doğrulanamadı"** yaz ve kullanıcıya sor. Üçüncü taraf indirmeleri (npm/pip/zip) önce yalıtılmış geçici dizinde incele.

## Dış skill / repo almadan önce
1. Ham `LICENSE` dosyasını oku (README'deki rozete güvenme); pack/alt klasörün kendi lisansı olabilir.
2. `scripts/`, `SKILL.md`, `package.json` içinde ara: `npx`, `curl`, `wget`, `events`, `telemetry`, `analytics`, token/anahtar isteyen satırlar. Telemetri veya reklam/yönlendirme talimatı varsa ALMA; fikri kendi cümlenle yaz.
3. **Ücretli servise bağlanan** (GPU bulutu, avatar/ses servisi, şirket lisansı) hiçbir şey eklenmez; ekip ücretli araç almıyor (ElevenLabs hariç, o zaten var).
4. Kopya değil paraphrase; Apache-2.0/MIT içerik taşınırsa `ASSETS.md`'ye kaynak+lisans yaz.
