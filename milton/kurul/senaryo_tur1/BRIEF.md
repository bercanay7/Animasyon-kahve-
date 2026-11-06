# Senaryo kurulu, tur 1: ortak brif

Sen "Zaman Kuryesi" YouTube kanalının senaryo kurulunda bağımsız bir üyesin. Kanal Türkçe; mitoloji, tarih, felsefe ve kitap animasyonları yayımlıyor. Anlatıcı ElevenLabs'teki "Emrullah" sesi.

## Okunacaklar
1. `/home/user/Animasyon-kahve-/CLAUDE.md`. Özellikle şu bölümler:
   - "Senaryo yapısı: Kahramanın Yolculuğu";
   - "Kurul";
   - "Ölçütler" (kanal verileri ve dersler);
   - "Kitle";
   - "Sonraki video: Milton". Bu bölüm kullanıcının bağlayıcı kararlarını içerir.
2. `/home/user/Animasyon-kahve-/milton/senaryo.json`: değerlendirilecek senaryo, revizyon 1.
   - `tts` alanı seslendirme metnidir (köşeli parantezde ElevenLabs v4 ses etiketleri, özel adlar okunuşa göre).
   - `alt` alanı altyazı metnidir.
   - `kaynak` alanı iddianın dayanağıdır (KC = Kayıp Cennet, kitap.dize).
3. `/home/user/Animasyon-kahve-/milton/kaynak/notlar.md` ve gerekiyorsa `dnb_milton_1894.md`.
4. Dize kontrolü için `kaynak/kayip_cennet_1674_dizeler.json` dosyası var, ama **tamamını okuma** (çok büyük). Yalnız gereken dizeleri çek:
   `python3 -c "import json;b=json.load(open('/home/user/Animasyon-kahve-/milton/kaynak/kayip_cennet_1674_dizeler.json'));print('\n'.join(f'{i}: {b[\"IV\"][i-1]}' for i in range(73,83)))"`

## Bağlam
- **Kullanıcının istediği:** bir arşiv ya da bilgi videosu değil, **hikâye**. Kullanıcı önceki bir videoyu "başı sonu yok, arşiv videosu gibi" diye beğenmedi.
- **Amaç:** izleyiciyi Şeytan'la empati kurduran bir iç yolculuk. Soru "Şeytan haklı mıydı?" değil.
- **Bağlayıcı kararlar:**
  - yalnız edebi okuma, dinî karşılaştırma yok;
  - Tanrı ve Oğul figürle çizilmez, ışık olarak gösterilir;
  - iki okuma çarpışır (Blake/Romantikler ve Lewis), karar izleyiciye kalır;
  - başkaldırı teması işlenir: çoğu başkaldırı hak ve özgürlük içindir, ama istisnalar var;
  - Milton'ın hayatı kısa tutulur, öne çıkan ayrıntı kör olduktan sonra eseri yazdırması;
  - süre sınırı yok, hikâye ne gerektiriyorsa;
  - görsel üslup Doré gravürü (siyah-beyaz tarama), kodla çizilecek.
- **Kodla çizimin sınırı:** siluet, kompozisyon, ışık, dönüşüm güçlü; yüz yakın planı, el ve karmaşık beden hareketi zayıf.
- Kanal verisine göre kayıp ilk 10–15 saniyede. Kapak ile açılış aynı vaadi vermeli. Merak sorusu ilk cümlelerde sorulup cevabı sona saklanmalı. Her bölüm küçük bir merak sorusuyla açılmalı.
- **Kapak adayları:**
  - A: "CEHENNEM BENİM", Doré tarzı Şeytan;
  - B: Cabanel'in gözyaşı.
  Bunlar henüz öneri.

## Puanlama (her üye bütün ölçütleri puanlar, kendi merceğine ağırlık vererek gerekçelendirir)
| Ölçüt | Ağırlık |
|---|---|
| K1 kaynak sadakati (dize, tarih, atıf; uydurma yok) | %20 |
| K2 açılış (ilk 15 sn kanca, kapak vaadi, merak sorusu) | %15 |
| K3 yapı (hikâye omurgası, kurulum–ödeme, bölümler) | %15 |
| K4 tempo (bölüm soruları, gereksiz sahne, uzunluk/ritim) | %15 |
| K5 psikolojik derinlik ve üslup (empati, iç yolculuk) | %15 |
| K6 dil ve seslendirilebilirlik (Türkçe, tts etiketleri, okunuş) | %10 |
| K7 görselleştirilebilirlik (Doré gravürü + kod çiziminin sınırı) | %10 |

- Ağırlıklı ortalama ≥ 9,0 ise **ONAY**.
- Herhangi bir ölçüt 7'nin altındaysa ortalama ne olursa olsun **RED**.
- Kaynak/doğruluk ve hassasiyet/hukuk alanlarının engelleyici bulguları estetik oyla geçersiz kılınamaz (veto).

## Çıktı
Raporunu **yalnız** şu dosyaya JSON olarak yaz: `/home/user/Animasyon-kahve-/milton/kurul/senaryo_tur1/<senin_kodun>.json`

```json
{
  "uye": "<kod>",
  "mercek": "<bir cümle>",
  "karar": "ONAY|RED",
  "puanlar": {"K1":0,"K2":0,"K3":0,"K4":0,"K5":0,"K6":0,"K7":0},
  "agirlikli": 0.0,
  "engelleyici": ["… (varsa; segment id ile)"],
  "duzeltmeler": [
    {"sira":1, "id":"G09", "sorun":"…", "oneri":"… (somut yeni metin önerisi varsa yaz)", "onem":"kritik|yüksek|orta|düşük"}
  ],
  "korunmali": ["en güçlü 3–5 an, id ile"],
  "en_emin_olmadigim_nokta": "…"
}
```

## Kurallar
- `senaryo.json` dosyasını ya da başka hiçbir dosyayı **değiştirme**. Yalnız kendi rapor dosyanı yaz.
- Somut ol: segment id ver, önerdiğin yeni cümleyi yaz.
- Gerekçesiz "güzel" ya da "kötü" deme. Bir şeyin işe yaradığını düşünüyorsan onu da yaz (`korunmali`).
- Başka üyelerin raporlarını okuma; bağımsız ilk bakış istiyoruz.
- Son mesajında rapordaki kararı, ağırlıklı puanı ve en önemli 3 düzeltmeyi kısaca özetle.
