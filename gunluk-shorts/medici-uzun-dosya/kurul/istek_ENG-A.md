# ENG-A → Başkan / ENG-B / sahne yazarı: istekler ve bildirimler (4 Kasım 2026)

Motor tarafı (benim dosyalarım) bitti; aşağıdakiler başka sahiplerin dosyalarında. Her madde: dosya · ne · neden.

## Sahne yazarı (P1: scenes_c0–c2, c1_kinds/c2_kinds, p1_ortak)
1. **Nominal levha konumları** — `name_plate` artık son kutuyu ekran uzayında kıstırıyor (0 ihlal), ama aşağıdakiler İSTENEN yerlerinde taşıyor ve
   motor kaydırıyor (`out_p1/duzeltme/ENG-A/qa_yerlesim.json` → `uyarilar`, tip `duzeltildi`). Kaydırma, levhayı komşu öğenin üstüne itebilir
   (ör. "VILLANI'NİN KARDEŞİ" HUD'dan kaçarken Peruzzi kalkanına biniyor). Önerilen nominal düzeltme: HUD'un sağ üstünde (x>1500) levha üst kenarı
   **y ≥ 160**; sağ kenar **≤ 1830 − kamera itme payı**; `w` artık alt sınır (metin + 110 px'ten dar verilirse genişler).
   - `c1_kinds.py:882` VILLANI'NİN KARDEŞİ (cx 1400, y gy−790, w 660 → 760 gerekli): y ≥ 160 ya da cx ≈ 1180; kalkanı 40 px aşağı.
   - `c1_kinds.py:875` GIOVANNI VILLANI: x ≥ 90 + yarım genişlik (cx ≥ 485), y ≥ 60 (kamera itmesinde sola/üste taşıyor).
   - `c2_kinds.py:226/250` (yeni sürümde hâlâ varsa) COSSA y=95 → ≥ 160; XXIII. JOHANNES cx 1650 → ≤ 1480, w ≥ 620.
   - `scenes_c1.py:112` STEFANI w=900 → metin 1110 px ister (w'yi kaldır ya da 1120).
   - `c2_kinds.py:625` MACHIAVELLİ'NİN ÇİZDİĞİ w=860 → 906.
2. **`c2_kinds.py` "KONSTANZ KONSİLİ · 1415"** (`CM.tablet(100,50,760,110)` + 46 px yazı ≈ 883 px): yazı levhadan taşıyor (TE2-E1). `CM.name_plate` kullan ya da tablet `w ≥ 960`, x ≥ 120.
3. **`p1_sehir flags="medici"` (Salvestro, 1378)**: dönem katmanı bunu otomatik **düz altın** sancağa çeviriyor (SA2-B2). Açıklık için `flags="plain"` yaz.
   `flags="stripes"` (Ciompi, kaynaksız) → Komün zambağına çevriliyor; istenirse `flags="lily"`/`"cross"` açıkça yazılsın. Alay/kalabalıkta bağlam vermek için
   yeni parametre: `procession(..., flag_ctx="ciompi"|"lonca"|"alay")`, `sehir(..., flag_ctx=...)` (isyan/halk/lonca bağlamında Medici sancağı hiç çizilmez).
4. **YIL_AT** — dönem öğeleri HUD yılına bağlı (çekim yılı = çekim boyunca HUD'da en uzun kalan yıl). Kurulun istediği adımlar (1390'lar, 1410, 1419, 1420)
   eklenmezse yapı/arma/yazıt o çekimlerde önceki yıla göre çizilir. **P3 (c6)**: hiç YIL_AT yok → c6 boyunca 1449; "Piero öldü (1469)" çekiminde Cosimo madalyası
   PATER PATRIAE'siz, skyline fener inşaatta çiziliyor. c6'ya 1465/1469/1471/1478 adımları önerilir.
5. **Madalya portreleri (v2)**: `cilt_medal.V2_FRAME="v1"` — yüz v1 ile aynı yerde/ölçekte, `c6_tarif` kalibre işaretleri (burun/çene/göz) geçerli. Omuzlu büst
   çerçevesi (`V2_FRAME="bust"`) hazır; açılırsa `c6_kinds.py:116–118` işaret ofsetleri yeniden kalibre edilmeli.
6. **p1_medal Lorenzo (≈525–534 sn)**: yeni rol satırı ("TORUNUNUN OĞLU · İLERİDE MUHTEŞEM") 34 px'te levhayı genişletiyor; levha madalyanın sağ kenarına ≈100 px biniyor → `pos`/`size` ya da levha x'i.

7a. **Kapak yankısı (`kapak_kilit`, 0–3,7 sn)**: büyük "SON MEDİCİ" başlığı HUD'un (1548–1848 × 72–138) altına giriyor (sprite yazı; `qa_yerlesim --yazi`
   yalnız `CM.ink` yazılarını ölçer, bunu göremez). Başlığı HUD'dan ≥18 px uzak tut ya da bu çekimde HUD'u gizle (ENG-B).
7b. **`scenes_c1.py` c1s10**: yeni seste "kardeşi"/"ailesindendi" sözcükleri yok → `compose.Program(part=1)` ve `qa_flow --part 1` kurulamıyor (benim QA araçlarım bu
   sürede eksik çapayı cümle başına düşürerek çalıştı; `eksik_capa` alanı JSON'da).

## ENG-B (compose, cilt_fx, qa_flow)
7. **`compose.Program(shots=…)`** modunda `cx.year` = 1397 (YearState boş varsayılanı). `donem.py` bunu çağrı yığınından tanıyıp yılı yok sayıyor; açık sözleşme
   için shots modunda `cx.year = None` verilmesi önerilir (kapak `engine_frame`, reel).
8. **Geçiş şeritleri / kaplamalar** (`cilt_fx` carry "paper" vb.) `CM.mini_palle` çiziyor: çekim dışı olduğundan son çekimin yılı kullanılıyor (tek renk; mavi top yok).
   İstenirse geçiş çiziminde `variant=` açıkça verilebilir.
9. **qa_flow kapısı**: `python3 qa_yerlesim.py` (levha: taşma/kenar/HUD; çıkış ≠0) ve `python3 qa_donem.py` (dönem; çıkış ≠0) qa_flow'a kapı olarak bağlanabilir.
   `--yazi` modu tüm serbest yazıları da raporlar (uyarı): bölüm etiketi x=78 (`chapter_tag`, güvenli alan 90 — TE2-K2).
10. **Kontrast zemini**: `CM.ink(scrim=None)` artık varsayılan olarak arka planı ölçer (WCAG; küçük 4,5:1, ≥46 px 3:1) ve gerekirse yumuşak koyu/açık zemin
    çizer (`CM.AUTO_SCRIM`, `CM.KICK_SCRIM`). compose bitiş ekranı etiketleri ve fresk başlık sloganı da bundan yararlanır; istemeyen çağrı `scrim=False` verir.
    `CM.kick` ayrıca son kutusunu güvenli alana kıstırır (`CM.KICK_SAFE`; TE2-Ö2 "18 ŞUBAT 1743" üst kenar).

## Başkan
11. **Disk %99 dolu** (≈0,7 GB boş, 4 Kasım 16:35). Önbellekler: `out/_cache/world` ≈ 85 MB (dönem ekli kareaşlar dâhil). Tam render öncesi yer açılmalı.
12. **Dönem önbelleği**: aşamalı çizim kodu değişirse `cilt_city.ERA_VER` artırılmalı (dosya adına girer; eski dönem kareaşları elle silinebilir: `rm out/_cache/world/*_e1*`).
