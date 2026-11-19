# Narkissos üslup kapısı: VAZO adayı

Kırmızı figür vazo dili, motor `prometheus/lib` (kaynağı `sisifos/lib`). Ortak sahte anlatım `../ortak/zaman.json`; olaylar `S()` / `Wd()`'ye bağlı.

## Dosyalar
- `index.html`: `?t=…&mb=…` tek kare çizer; `window.renderAt(t, mb)` ve `window.READY`. `?dikey=1` D planını 1080×1920 çizer, `?kapak=yazili|yazisiz` kapak.
- `nark.js`: beş plan (A–E), yansıma (`mirror`), analitik halka (`warpRings`, `ringLines`), telefon camı ↔ havuz biçim dönüşümü (`morphPts`), alttan ışık (`litFigure`).
- `kapak.js`: kapak taslağı (1920'de çizilir, 1280×720'ye küçültülür).
- `main.js`: kare döngüsü, hareket bulanıklığı (180° obtüratör, `mb` alt kare, plan sınırını aşmaz), doku + vinyet + gren (tohum `floor(f/2)`).
- `lib/`: `prometheus/lib`'den kopya. Değişiklikler yalnız `figure.js`'te:
  - `HAIR_MOD`: bugünün genci için kısa saç (`lk.hairPts`);
  - `lk.coatCol`, `lk.sleeveCol`: bugünün giysisi (seyreltik sır ceket, uzun kol);
  - `lk.noCurls`: alın bukleleri yok;
  - sakalsız kırmızı figürde ağız kil çizgisi çizilmez; yüz konturunu aşıp "sigara" gibi okunuyordu, yerine kazıma çizgi.
- `fonts/`: Bebas Neue (latin + latin-ext; `orfeus/fonts`'tan, OFL). `sisifos/fonts.css`'te Bebas yok.

## Komutlar
Kökü `narkissos/kapi` olan küçük bir yerel http sunucusu kullanılır (`../ortak/` erişimi için).

```
node kare.js <klasör> A_cam=1.5,4 D_benim=15.0,4        # ad=t[,mb] → PNG
node kare.js <klasör> kapak=kapak:yazili kapak0=kapak:yazisiz
node kare.js <klasör> dikey_D=dikey:14.9,4               # 1080×1920
WORKERS=3 MB=4 node render.js <çıktı.mp4>                # 19,5 sn, 30 fps, H.264 CRF 18, BT.709, sessiz
```

## Tanıma hamlesi ('benim', 14,6 sn) — tur 1
- Su çizgisi kaya üstünden 40 birim aşağıda (`D_WY`, `D_GAP`); el kıyıdan açık suya iner.
- `dReach(t)`: 'Sonra'da (13,49) yakın el kayadan kalkar (hazırlık), yükselir, işaret parmağı 14,30'da suya değer (küçük halka).
- Yansıma kendi zamanından 0,3 sn geride çizilir; yansımanın parmağı tam 'benim'de (14,60) gelir ve iki parmak aynı karede buluşur. Gecikme sıfırlanır (birebir kilit), yansıma soluktan bedenin kiline döner (0,44 → 0,84).
- Genç irkilir: baş geri çekilir, kaşlar kalkar, ağız aralanır; el 15,05'e kadar suda kalır, sonra çekilir.
- Noktalı göz çizgisi kaldırıldı.

## Tur 1 değişiklikleri (FABLE_KAPI.md düzeltmeleri)
- `lib/figure.js`: efeb başı (`HAIR_EF`, `lk.efeb`: kısa bukleli saç, kulak açık, kenarda bukle tümsekleri; `lk.jaw`: köşeli çene), khiton (`lk.khiton`: seyreltik sır rengi, sık kıvrım, koyu sır etek kenarı; nokta deseni, kemer, omuz kası kavisi yok), `lk.headS` (genç oranı), `f.jointsOnly` (çizimsiz eklem hesabı).
- D: yumruk yok (eller açık), halka yansımayı yatay şeritlere böler (`R.shear`; 120 px'te kırık leke), karşı kıyı + nergisler + belirgin su çizgisi.
- C: eller kıyıyı kavrar, 'âşık'ta yalnız yakın el suya iner; karşı kıyıda nergis.
- A/E: telefonu tutan el (`phoneHand`), başparmak 0,35/1,05/1,75'te kaydırır, ekran ışığı kıpırdar; baş büyük, göz iri.
- Halka çizgileri: merkezdeki küçük elips söner (hale okunmasın).
- Kapak: kil kenar çizgisi, ortalama parlaklık ~52, el kadraj dışında, karşı kıyı yok; yazı suya yansımaz.
- Hız: sönmüş halka piksel kaydırmaz, kaydırma yalnız yansıma bölgesinde (`warpBox`).

## Tur 2 değişiklikleri (FABLE_ONAY_tur1.md kalan düzeltmeleri)
- A/E başparmağı (`phoneHand`): kısa (~70 birim, ekranda ≤ 90 px), iki boğumlu (boğum çizgisi), tırnaklı; kökü avuçta, camın sol alt kenarında durur. Kökü avucun arkasında kalır (kutu gibi uç görünmez). Yansıyan yüzün ağız/çene bölgesinden uzak.
- A kaydırma: başparmak üç kez (0,3 / 1,0 / 1,7 sn) yukarı süpürür (uç ~70 px yol); camın arkasında soluk akış kartları (`phoneFeed`) her kaydırmada 330 birim yukarı kayar, 2,0–2,6 sn'de söner (cam yalnız yansımaya kalır).
- A kadrajı telefona yakın (z 1,21 → 1,25), figür ölçeği 24 → 20,5, baş oranı 1,24 → 1,45 (gövde küçük, yüz aynı boyda), `jaw` (köşeli çene).
- D: `HAND.point` yeniden çizildi (kapalı yumruk, yuvarlak uç, tek işaret parmağı, kıvrık parmak boğumları); yansıma bunun aynası, V/makas okunmaz.
- D: uzak kol çizilmez (`f.noFarArm`); efeb figürde dirsek kıvrım çizgisi yok (katlanmış kolda 'kesik uç' gibi okunuyordu).
- D: uzanma yavaş ve alçak (`dReach`: 13,24'te başlar, ara poz dirsek kayada; dönüş 1 sn); hareket bulanıklığında kol lekesi yok.
- D: irkilme büyük: 14,58–14,82'de göz ~85 px geri/yukarı, ağız açık (`mouthOpen` 2,1, efebde görünür kama), göz açılır (`p.eyeWide`), kaş kalkar (`p.browUp`).
- C: ayak arkasındaki ince mızrak çubuğu silindi.

## Tur 3 değişiklikleri (FABLE_ONAY_tur2.md kalan düzeltmeleri)
- A/E (`PH3`, birinci çözüm): yansıma gerçek başın birebir aynası ve **tam altında** (`refDx` 0; camın üst kenarı ayna ekseni). Cam yüzden uzak (`wy` 630), baş daha az eğik (`headA`/`neckA` .3): burun–burun ~300 px, iki yüz çapraz "öpüşme" çizgisi kurmuyor. Yansıyan başın tamamı camın içinde (saç kesilip "uzun saç" gibi akmıyor). Yansıma soluk (`refA` .2; yanakta parlaklık gerçeğin ~%60'ı), üstünden çapraz cam parlaması (`glassGlare`). Gerçek yüzde nötr ağız (`p.mouthFlat`) ve açık göz (`p.eyeWide` .3). Yakın kol telefonu tutan ele uzanır (`armToPhone`; havuza dönerken kadraj altına iner); el camın sol alt köşesinde (`handY` 480), başparmak yansıyan yüzden uzak. Kadraj geniş (z .82–.86), figür + telefon ortada.
- E: yansıyan gözün çevresinde halka kaydırması yumuşakça sıfıra iner (`warpRings(..., calm)`, `eyeCalm` 55): kırık iz yok.
- C: bacaklar düz ve yerde (`proneFig(..., {flatFeet})`), ayak kalkmaz; khiton uyluk ortasına iner ve etek ucu uyluğa dik keser (`p.hemPerp`, `p.hemT` .62; `lib/figure.js`). Figürün altında kalan ot tutamı çizilmez.
- D_halka: gözyaşı halkası ikiye ayrıldı: yüzü dağıtan kaydırma (çizgisiz, `noLines`) + görünen çizgiler (hızlı, sık, eşmerkezli; `D_RV`/`D_RL`). Görünen çizgiler yansıyan figürün 80 birim çevresinde çizilmez (`R.mask`, `reflMask`: dalgasız yansımanın genişletilmiş, yumuşak kenarlı silueti).
- `lib/figure.js`: iri gözde (`eyeWide`) yarı kırpışta bebek kapaktan taşmaz.
