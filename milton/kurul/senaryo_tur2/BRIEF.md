# Senaryo kurulu, tur 2: ortak brif

Tur 1'de verdiğin raporla aynı rolde, aynı ölçütlerle (K1–K7, ağırlıklar, eşik ≥ 9,0 ve hiçbir ölçüt < 7) devam ediyorsun.

## Okunacaklar
1. `/home/user/Animasyon-kahve-/milton/KURUL.md`:
   - tur 1 sonuçları;
   - başkanın uyguladığı kararlar;
   - reddedilen bulgular ve gerekçeleri.
2. Değerlendirilecek metin: `/home/user/Animasyon-kahve-/milton/senaryo.json` (revizyon 2).
   - Aynı içerik `kurul/senaryo_tur2/senaryo_rev2.json` dosyasında da var.
   - Rev1 için: `kurul/senaryo_tur1/senaryo_rev1.json`.
   - Fark özeti: `kurul/senaryo_tur2/fark_rev1_rev2.md`. Kimlikler (id) yeniden dağıtıldı; sıra için rev2 esastır.
3. Kendi tur 1 raporun: `kurul/senaryo_tur1/<kodun>.json`.
4. Alan eşinin tur 1 raporu (aşağıdaki tabloya bak).

| Sen | Alan eşin |
|---|---|
| S-Yon | S-Dram |
| S-Dram | S-Yon |
| K-Uzman | K-Denetim |
| K-Denetim | K-Uzman |
| H-Hukuk | H-Hassasiyet |
| H-Hassasiyet | H-Hukuk |
| T-Tutma | T-Izleyici |
| T-Izleyici | T-Tutma |
| A-Ses | A-Dil |
| A-Dil | A-Ses |

## İş
1. **Çapraz eleştiri:** alan eşinin tur 1 raporunda nelere katıldığını, nelere katılmadığını (gerekçesiyle) ve neyi gözden kaçırdığını yaz. Uzlaşma zorunlu değil.
2. **Doğrulama:** başkanın KURUL.md'deki "uygulanan kararlar" listesi bir iddiadır. Kendi tur 1 bulgularının (ve eşinin önemli bulgularının) rev2'de gerçekten karşılanıp karşılanmadığını metne bakarak kendin doğrula. Her biri için şu durumlardan birini yaz:
   - karşılandı;
   - kısmen;
   - karşılanmadı;
   - reddedildi (gerekçe sana uygun mu?).
3. **Yeni sorunlar:** rev2'nin yarattığı yeni sorunları bul (gerileme, yeni hata, akış kırılması, süre).
4. **Yeniden puanla.**

## Çıktı
Yalnız şu dosyaya JSON yaz: `/home/user/Animasyon-kahve-/milton/kurul/senaryo_tur2/<kodun>.json`

```json
{
  "uye": "<kod>",
  "karar": "ONAY|RED",
  "puanlar": {"K1":0,"K2":0,"K3":0,"K4":0,"K5":0,"K6":0,"K7":0},
  "agirlikli": 0.0,
  "capraz": {"katildigim": ["…"], "katilmadigim": ["… (gerekçe)"], "gozden_kacan": ["…"]},
  "dogrulama": [{"bulgu": "…", "durum": "karşılandı|kısmen|karşılanmadı|reddedildi", "not": "…"}],
  "engelleyici": ["…"],
  "duzeltmeler": [{"sira":1, "id":"…", "sorun":"…", "oneri":"… (somut yeni metin)", "onem":"kritik|yüksek|orta|düşük"}],
  "en_emin_olmadigim_nokta": "…"
}
```

## Kurallar
- Hiçbir dosyayı değiştirme; yalnız kendi rapor dosyanı yaz.
- Tur 1 dosyalarının üzerine yazma.
- "Cehennem benim" / "Ben cehennemim" seçimi kullanıcıya soruluyor. İstersen görüşünü bir cümleyle yaz, ama puanını buna bağlama.
- Son mesajında kararı, puanı ve en önemli en fazla 3 kalan düzeltmeyi kısaca yaz.
