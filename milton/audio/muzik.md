# Kayıp Cennet: müzik ve efekt notu (ses kurulu için)

Her şey `audio/score.py` içinde numpy/scipy ile sentezlenir. Örnek ses yok, indirme yok, ücretli araç yok.
Her vuruş bir cümleye ya da kelimeye bağlıdır (`S('G07')`, `W('G07','ben')`). `timeline.js` değişince yeniden çalıştırmak yeter:

    python3 audio/score.py          # audio/music.wav + audio/motifler.txt   (~75 sn)
    python3 tools/mix.py --stems    # audio/mix.wav + audio/stems/{vo,music}.wav   (~2 dk)

`audio/motifler.txt`: her motifin çaldığı an, cümle ve notalar. Doğrulama listesi olarak kullanılır.

## Palet (17. yüzyıl İngiltere'si × karanlık destan; ton merkezi Sol)
- **Viol topluluğu** (yaylı; solo viol ayrı bir "lead" kanalında, konuşmada daha derin kısılır).
- **Uzak borulu org:** yumuşak, labial, bol salon yankılı. Yalnız uzun akorlar ve pedal sesler kullanılır; ilahi armonisi ve kadansı yok.
- **Lavta ve klavsen:** Milton'ın odası, Aden ve "İki okuma" bölümü.
- **Sözsüz koro "a/u/o":** cennet, güneş, iç ışık. Söz, dua ya da tanınabilir bir ilahi yok.
- **Cehennem ve savaş:** alçak dron, timpani, boom.
- **Tek büyük çan:** yalnız üç kırılmada, birer vuruş (G14, J07, L08b). Çan dizisi çalınmaz.
- **Yasaklar:** ezan, tilavet, ney, makam ve kilise ilahisi çağrışımı yok. Mevcut bir eserden alıntı yok.

## Motifler
| Motif | Notalar | İşlev |
|---|---|---|
| IŞIK (tam) | Si4 Re5 La5 Sol5 | Başmeleğin ışığı: A02, C02, C03. K07'de Blake'in okuması, F08'de sahte parıltı (ince klavsen) |
| IŞIK (minör) | Sib4 Re5 La5 Sol5 | Hatıra ve hüzün: B08, E02, E06, E11, G05, G16, H05, L03 |
| IŞIK (kırık, Frig) | Sib4 Re5 Lab5 Sol5 | İlk acı D05, Günah F03, doruk G07 |
| IŞIK (yarım) | Sib4 Re5 (sıçrama gelmez) | Sönen ışık: E15, H12, J11, K13 |
| IŞIK (umut) | Si4 Re5 La5 (çözülmeden asılı) | G09 "Pişmanlığa hiç yer kalmadı mı?" Cennetten sonra ilk majör |
| IŞIK (ev) | Si4 Re5 La5 Sol5 Fa#5 Sol5 | L09: ilk kez Milton için, tam ve çözülerek. Film bitiş ekranından sonra bununla kapanır (L11 kuyruğu) |
| DÜŞÜŞ | Sol2 Fa#2 Fa2 Mi2 Mib2 Re2, aksak uzun-kısa | A01, C08 (ilk tam hâli), H12, I05, J07, J11, L06. Parçaları C04, E02, H08, K13'te |
| DÜŞÜŞ/9 | Sol2'den Sib1'e dokuz yarım ses | D09 "Dokuz gün düştüler"; her adımda bir timpani |
| Lewis basamakları | Sol3 Fa#3 Fa3 Mi3 Mib3 Re3 | K11: kahraman, general, politikacı, casus, kurbağa, yılan; her basamak bir kelimede |
| ABDİEL | Sol4 Re5 Mi5 Re5 | Süssüz, dik duran çizgi: C10, C11, D02, K16 |
| ADEN | Re5 Si4 Do5 La4 Si4 Sol4 | H04, I06, K01 (çıkışta umut) |
| İki akor | Sol minör (org) / Mib majör (koro) | E10 "gurur / pişmanlık" → L05'te aynı sırayla döner |
| Soru akoru | Do3 Sol3 Re4 Sol4 (asılı) | C12, L06, K16, L10 |

**İç cehennem (G07):** DÜŞÜŞ basta (yaylı ve org) çalar, kırık IŞIK tiz viol ve koroda. İkisi "Ben cehennemim" sözünün bittiği yerde buluşur. A01'deki kanca bunun önizlemesidir: aynı bas ve tek bir Lab5–Sol5 iç çekişi.

## Bölüm bölüm
| Bölüm | Çalgılar | Motif | Efektler |
|---|---|---|---|
| A Ben cehennemim | dron, koro, org, viol, lavta | DÜŞÜŞ (A01), IŞIK tam (A02) | rüzgâr, iç alev, kanat (A03), yanan göl, zincir (A04 "zincirlerle"), sayfa (A05) |
| B Kör şair | lavta (Sol minör), viol, uzak org (B06) | IŞIK minör (B08) | tüy kalem (B02), sayfa, kitap ateşi ve kalabalık (B04 "cellat"; "sekiz yıldır kördü"de söner) |
| C Işık taşıyan | koro "a", org, klavsen, viol | IŞIK tam (C02, C03), DÜŞÜŞ (C08), ABDİEL (C10–C11) | yıldız parıltısı (C03), timpani "özgürlük" (C06) |
| D Dokuz gün | timpani, savaş davulu, yaylı, koro/org (D08 araba) | IŞIK kırık (D05), DÜŞÜŞ/9 (D09) | kılıç çekme (D01), kılıç darbesi, on adım ve diz (D04), top (D07), dağ (deprem), gök gürlemesi (D09 "kaos"), kapanış (D09 "kapandı") |
| E Cehennemde kral | dron, Frig org, koro "o", timpani | IŞIK minör (E02, E06, E11) | göl ateşi, zincirler düşer ve kanat (E05), mızrak darbesi (E07), Pandemonium kazısı ve yükselişi (E12) |
| F Kapıdaki bekçiler | dron (Sol–Reb), yaylı glissando | IŞIK kırık (F03), IŞIK tam/klavsen (F08, sahte) | tıslama izi (F02), ağır kapı (F05), Kaos rüzgârı, kanat, düşüş, yukarı fırlayış (F06), altın zincir (F07) |
| G Güneşe itiraf (DORUK) | yalnız rüzgâr, tek viol, org pedalı, koro "u"; en seyrek bölüm | İÇ CEHENNEM (G07), IŞIK umut (G09), minör (G16) | kalem (G02b), zincir halkası (G09b "boyun"), üç "elveda" çekişi, **çan** (G14 "kötülük") |
| H Aden'de bir yabancı | klavsen pastorali, ince yaylı | ADEN (H04), IŞIK minör (H05), DÜŞÜŞ (H12) | kuşlar (yalnız aralarda), sıçrama, karabatak kanadı, sayfa ve kalem (H07), kurbağa (H09), mızrak dokunuşu (H10) |
| I Yılanın içinde | dron, viol, koro (I06) | DÜŞÜŞ (I05), ADEN ve "sersem iyilik"te iki ışık notası (I06) | yedi gece nabzı (I02), meyve kopması ve ısırık (I08), dünyanın yarası: gürleme ve rüzgâr (I09), "Kazanmıştır."ın hemen ardından tek darbe (I10) |
| J Alkış | sahte parıltı (Lab majör koro/org), yaylı | DÜŞÜŞ (J07, J11), IŞIK yarım (J11) | kalabalık sevinci (J02); **J04 gerçek sessizlik** (J03'ün son sözünden J05 "tek bir ses"e kadar müzik tamamen kapalı, yalnız −58 dB oda tonu); J05'te 12 sesli tıslama yavaşça kabarır; dönüşüm, yere yığılış, **çan** (J07 "devasa"); tıslayan salon (J08); kül (J10) |
| K01–K04 Dünya önlerindeydi | açık Sol, lavta, koro "a" | ADEN (K01) | uzak alev, damla, sayfa (K03), mum söner (K04) |
| K05–K16 İki okuma | klavsen nabzı, viol, sade akorlar | IŞIK tam (K07 Blake), Lewis basamakları (K11), ABDİEL (K16) | zincir (K07, K15), taç (K15b) |
| L Bir damla yaş | Mib viol/org, koro | IŞIK minör (L03), iki akor (L05), DÜŞÜŞ (L06), **IŞIK ev (L09, L11 sonu)** | gözyaşı damlası (L03), kendi vurduğu zincirin halkaları (L07, "gururu"), kapalı kapı (L08), **çan** (L08b), sıcak bitiş ekranı ve 4 sn'lik temiz sönüş |

## Miks (`tools/mix.py`)
**Anlatım:**
- Yalnız hafif işlem: 70 Hz yüksek geçiren, 250 Hz'de −1,5 dB, 3,5 kHz'de +1 dB, 3:1 tepe sıkıştırma ve güvenlik sınırlayıcısı.
- Cümle kazancı yok; fısıltılar oyunculuğun parçası. De-esser uygulanmadı; sibilans ayrıca ölçülmedi, kulakla kontrol edilmeli.

**Müzik, iki aşamalı kısma:**
1. `score.py`, konuşma bandında (220 Hz–3,8 kHz) STFT ile en çok 9 dB keser. Önemli cümlelerde (A01, G07, G09, G09b, G14, I10, L08b, L09, L10) daha derin keser.
2. `mix.py`, 3 sn'lik pencerelerle yavaş bir "fader" uygular: konuşma boyunca müziği anlatımın yaklaşık 15 LU altında tutar. Kazanç −9 ile +3 dB arasında kalır ve 2 sn'de yumuşatılır.

**Ölçüm (bu çizelgeyle):**
- Entegre −14,0 LUFS, gerçek tepe −2,5 dBTP.
- Kelime anlarında anlatım ile müzik farkı ortanca 20 LU, en az 14,4 LU (D09, gök gürlemesi). 3 sn'lik pencerelerde ortanca 18,6 LU.
- 1–4 kHz bandında konuşma anlarında anlatım müzikten ortanca 31 dB yukarıda.
- J04 sessizliğinde müzik izi −57 dBFS RMS (yalnız oda tonu).

Kurul sesi dinleyemez; kulakla son onay kullanıcınındır.
