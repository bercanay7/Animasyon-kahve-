# Durum panosu: hangi iş nerede

Her oturumun başında `.claude/hooks/dal_durumu.sh` çalışır ve `main`'e birleşmemiş dalları listeler. Bu pano onun yanında durur: dalın adı neyi kapsıyor, iş hangi aşamada, sıradaki adım ne.

**Kural (26 Kasım):**
- Her iş parçası bitince bu tablo o oturumda güncellenir (aşama, dal, sıradaki adım).
- Video teslim edilince dalı `main`'e birleştirilir; satırda dal sütunu `main` olur.
- Biten ya da yayına giren iş "Arşiv"e iner; tablo kısa kalır.

Son güncelleme: 26 Kasım 2026.

## Sürmekte olan
| İş | Klasör | Dal | Aşama | Sıradaki adım |
|---|---|---|---|---|
| Dorian Gray | `dorian-gray/` | main | teslim | yayın 28 Kasım 18:00; 48. saat 30 Kasım |
| Gılgamış | `gilgamis/` | main | teslim | yayın 2 Aralık 18:00; 48. saat 4 Aralık |
| Lale Çılgınlığı | `lale-cilginligi/` | main | teslim | yayın 10 Aralık 18:00 (27 Kasım: Frankenstein'la yer değiştirdi); 48. saat 12 Aralık |
| Frankenstein | `frankenstein/` | main | teslim | yayın 6 Aralık 18:00 (kullanıcı, 27 Kasım; şerit denemesi); 48. saat 8 Aralık |
| Çernobil'in çayı | `cernobil/` | main | teslim (Fable düzeltmeleriyle) | yayın 14 Aralık 18:00 (öneri); 48. saat 16 Aralık |
| Stanford Hapishane Deneyi | `stanford/` | main (26 Kasım birleşti) | teslim: YouTube 360 MB, telefon 93 MB | yayın 18 Aralık 18:00 (öneri); `stanford/yayin.md` |
| Şart Shorts'ları | `shorts-sart/` | main (26 Kasım birleşti) | teslim; günlük takvim 26 Kasım – 4 Aralık, 20:00 | takvim ve ölçüm: `shorts-sart/yayin.md` |
| Topluluk gönderileri | `topluluk/` | main (26 Kasım birleşti) | hazır | 26 Kasım Dorian, 30 Kasım Gılgamış, 4 Aralık Lale (19:00); `topluluk/gonderiler.md` |
| Kanal kimliği (logo, avatar, kapak) | `kanal/logo/` | main | bitti (`KIMLIK.md`); 1440p yükleme deneyi yapılmayacak (kullanıcı kararı) | Studio'ya yükleme kullanıcıda |
| Mektuplar: kanal tanıtımı (kurye, yağlıboya canlanan resim) + 3B manken aracı | `kurye/`, `araclar/manken/`, `araclar/tablo/` | `claude/3d-puppet-drawing-shader-4ca4y8` | **sürüyor** (v7, eleştiri turları) | bitince `main`'e birleşir; `CLAUDE.md`'de çakışma var, birleştirmede elle çözülür |

## Yayında (ölçüm bekleyen)
| Video | Yayın | Ölçüm |
|---|---|---|
| Narkissos | 24 Kasım | 48. saat alındı (`analiz/2026-11-26-narkissos-48saat.md`); 0:30 eğrisi bekleniyor |

## Video arşivi
Bitmiş videolar depoda tutulmaz (27 Kasım). Her teslimden sonra kullanıcı YouTube kopyasını Google Drive'daki "Zaman Kuryesi / teslim" klasörüne atar; YouTube'un sakladığı dosya yeniden sıkıştırılmış kopyadır, yüklenen dosya değil. Depodan çıkarılan eski çıktılar git geçmişinde: `kanal/arsiv/cikarilan_videolar_2026-11-27.md`.

## Kanalla ilgisiz dallar
`.claude/hooks/dal_yoksay.txt` içindekiler (Navitas, spa listesi, Erdem Melih). Kanca bunları listelemez; `CLAUDE.md` gereği dokunulmaz.

## Arşiv
Yayına girmiş eski videolar ve dersleri: `kanal/DERSLER.md`, `kanal/OLCUTLER_GECMIS.md`.
