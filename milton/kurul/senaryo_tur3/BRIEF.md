# Senaryo kurulu, tur 3: gerileme kontrolü

Aynı rolde, aynı ölçütlerle (K1–K7; eşik ≥ 9,0 ve hiçbir ölçüt < 7) devam ediyorsun. Bu tur alan başına tek üyeyle yapılıyor; alanının öbür üyesinin tur 2 raporundaki açık bulgulara da sen bakıyorsun.

## Okunacaklar
1. `/home/user/Animasyon-kahve-/milton/KURUL.md`, "Tur 2 (rev2 → rev3)" bölümü: uygulanan kararlar, reddedilenler ve gerekçeleri.
2. Değerlendirilecek metin: `/home/user/Animasyon-kahve-/milton/senaryo.json` (revizyon 3).
3. Fark özeti: `kurul/senaryo_tur3/fark_rev2_rev3.md`.
4. Kendi tur 2 raporun ve alan eşinin tur 2 raporu: `kurul/senaryo_tur2/<kod>.json`.

## İş
1. Kendi tur 2 düzeltmelerinin ve alan eşinin "kritik" ve "yüksek" düzeltmelerinin rev3'te karşılanıp karşılanmadığını metne bakarak doğrula. Başkanın listesi bir iddiadır.
2. Rev3'ün getirdiği yeni hata ya da gerileme var mı? Özellikle yeniden yazılan cümleler: A03, B02, B04–B05, C05, D02–D04, E04, E08, F03, G13, H10–H11, I04–I06, J06, J09, J11, K03, K07–K08, K11–K16, L04–L09, L11.
3. Yeniden puanla. Engelleyici bulgun yoksa ve eşik aşıldıysa ONAY ver. Onaydan sonra da küçük öneri yazabilirsin; "düşük" olarak işaretle.

## Çıktı
Yalnız şu dosyaya JSON yaz: `/home/user/Animasyon-kahve-/milton/kurul/senaryo_tur3/<kodun>.json`

```json
{
  "uye": "<kod>", "karar": "ONAY|RED",
  "puanlar": {"K1":0,"K2":0,"K3":0,"K4":0,"K5":0,"K6":0,"K7":0}, "agirlikli": 0.0,
  "dogrulama": [{"bulgu":"…","durum":"karşılandı|kısmen|karşılanmadı|reddedildi","not":"…"}],
  "engelleyici": [], "duzeltmeler": [{"sira":1,"id":"…","sorun":"…","oneri":"…","onem":"kritik|yüksek|orta|düşük"}],
  "en_emin_olmadigim_nokta": "…"
}
```

## Kurallar
- Hiçbir dosyayı değiştirme; yalnız kendi rapor dosyanı yaz. Geçici betik gerekiyorsa adının başına kendi kodunu koy (ortak klasörde ad çakışması yaşandı).
- Süre sınırı yok (kullanıcı kararı). Tempoyu "kısa mı?" diye değil, "bu cümle hikâyeye bir şey katıyor mu?" diye değerlendir.
- Son mesajında kararı, puanı ve varsa kalan en fazla 3 düzeltmeyi yaz.
