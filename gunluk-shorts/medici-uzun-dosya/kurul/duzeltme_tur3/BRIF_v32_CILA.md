# BRİF — v3.2 cila turu (kurul tur 3b'nin küçük notları)

Kurul tur 3b'de üyelerin hepsi v3.1'e ONAY verdi (9,3–9,5). Bu turdaki maddelerin hiçbiri koşul değil. Ama birkaçı "videonun ucuz okunabilecek tek karesi" ya da dönem hatası. Bu yüzden tek bir cila turunda kapatılıyor, ardından tek bir tam render yapılıyor.

P = `/home/user/Animasyon-kahve-/gunluk-shorts/medici-uzun-dosya`. Tur 3b raporları: `P/kurul/tur3b/<KOD>.md`.

## Ortak kurallar
- Anlatım, ses ve altyazı DEĞİŞMEZ. Sayılar ve etiket metinleri aynen kalır; yeni olgu iddiası yok.
- Her değişikliği kare kontrolüyle doğrula: `python3 /tmp/claude-0/-home-user/ad251a99-58f4-5d1d-a24b-a2064ec20b78/scratchpad/v3/kare.py <ad> t1 t2 … --w 640 --cols 4`. Hareket için ardışık kare al.
- **Son kapı:** `qa_flow.py --part 1`; 20 GEÇTİ olmalı, en çok bir koşu. İki ajandan SONRA biten koşar; öbürü yalnız kendi alanını kare kontrolüyle doğrular.
- **Yasaklar:** render.py yok, git commit/push yok (başkan yapar), `pkill -f` yok.
- **Disk:** dökümleri sil. Kanıt JPEG'leri (≤1 MB) `P/out_p1/duzeltme/v32/<AJAN>/` altına.
- **Rapor:** `P/kurul/duzeltme_tur3/v32_<AJAN>.md`. Her madde için ne yapıldı, dosya:satır, önce/sonra kanıtı.

## SCN-3 (dosyalar: `c2_kinds.py`, `scenes_c2.py`)
1. **#83 el (PK2-G1, SA1-E-1; 476,3–478,3 sn).** ≥2× yakında anahtarları bırakan el parmaksız bir yumru gibi duruyor. İlk kez izleyen için "ucuz" okunabilecek tek kare bu.
   - Eli kadrajdan çıkar. Anahtarlar kadrajın üstünden kadifeye düşsün: çan eğrisi, küçük sekme ve oturma (`anim.settle`), metal tınısı efektine uyan an.
   - Halka ve anahtarların hızını deklanşöre bildir (`hint_speed`).
2. **#83 başlık × HUD (PK2-G2, TE2-G10; 476–477,5 sn).** Şerit başlığının son "U"su HUD dikdörtgenine ≈10 px giriyor. Başlık HUD'dan ≥16 px uzak olsun (küçült ya da kaydır).
3. **#83 son hâl (TE2-G9; 485,2–486,4 sn).** Özetin son hâli ve "MEDİCİ'DE KALDI" yalnız ≈0,7 sn, hareket bulanıklığı altında görünüyor. Kamera son çerçeveye ≈485,2'de otursun ve geçişe dek dursun: ≥1,2 sn okunur, bulanıklık yok.
4. **#88 ciltler (SA2-G2; 511,7–518,3 sn).** Renkli deri, yaldızlı sırt bantları ve sırt etiketleri 18.–19. yüzyıl kütüphane cildi gibi duruyor. 15. yüzyıl Floransa hesap defteri biçimi:
   - krem/fildişi yumuşak parşömen kapak (limp vellum), deri kayış ya da bağcık;
   - yıllar kapağa ya da sırta mürekkeple elle yazılmış;
   - yaldız bant ve renkli etiket yok.
   - Asılı "1397 – 1420" etiketi ve sandık kalabilir. Sırtlarda yalnız "1397" ve "1420".
5. **ÖZET etiketleri (TE2-G12).** #95 "TÜRKÇESİ ÖZET · ÇEVİRİ BİZE AİT" ve #96 "TÜRKÇE SATIRLAR ÖZET · ÇEVİRİ BİZE AİT" 30 px → 34 px. Konum değişmez (#95 y 850; #96 y 905). Sayfa yazısıyla, levhalarla ve altyazı bandıyla çakışma olmasın.
6. **Catasto ruloları (SA1-G2; 500,0–502,8 sn; `c2_kinds.py` ≈981–991).** Beyanname ruloları sivri elips gibi; yaprak ya da balık deseni gibi okunuyor. Rulo gibi çiz: silindir gövde, iki ucunda sarmal kâğıt kıvrımı, ip ya da mühür.
7. **KEFALET levhası (SA1-G3; 444,9–452,6 sn).** Simge "K" harfine değiyor. Simge ile metin arası ≥12 px olsun.

## ENG-E (dosyalar: `cilt_oda.py`, `c0_kinds.py`, `scenes_c0.py`, `scenes_c1.py`, `c1_kinds.py`)
8. **Asemik el (SA2-G1; 34,6–56,7 sn ve K1 kapağı).** 1737 tarihli resmî belge için el fazla düzensiz ve az eğik. 47,0 sn yakın planında başlık ve satır başları harf parçası gibi okunuyor.
   - Eğim 20–25°.
   - x-yüksekliği satır içinde daha sabit (değişkenlik yarıya).
   - Kancelarya düzeni: düzenli sözcük aralıkları.
   - #8 yakın planında (2,1–2,24×) gövde yazısı biraz sönük (alfa ≈%70). ITALIANO yazımı ve çizgisi önde kalsın.
   - Gerçek sözcük oluşmasın.
   - Kapak PNG'sini başkan yeniden üretecek.
9. **1737 genel planı (TE2-G11; 39,4–40,2 sn).** Kamera tam görünüme dönünce iki ad birlikte görünsün:
   - sol ad (ANNA MARİA LUİSA) `c0s8 −0,35`'te geri gelsin;
   - iki ad `("c0s8", "on", −0,3)`'te birlikte sönsün.
   - Lorraine tarafındayken sol ad yine sönük kalsın (kenarda yarım kalmasın). `names_hide` / `names_out` başkanın eklediği parametreler (`c0_kinds.k_belge`).
10. **#48 levhaları × arma ızgarası (SA1-G1, önemli; 274,1–277,7 sn).** "KISA ÖMÜRLÜ LONCA KALDIRILDI" ve "YÖNETİMDEN DE DIŞLANDILAR" levhaları (≈x 430–1490, y 160–240) üst sıradaki altı armanın tepesini örtüyor. Bu, ENG-E'nin bu çekimin kamerasını 100 px kaydırmasından da gelmiş olabilir.
    - Levhaları y≈90–165'e al (HUD ve çip bölgesine çarpmasın) ya da ızgarayı ≈70 px aşağı indir.
    - Kalıcı çözüm `c1_kinds`'te: dosya artık senin.
    - Düzelirse SA1'in puanı 9,4 oluyor.
