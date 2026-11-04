"""c1 — Florin Şehri (1252–1397). Brif: brif/c1_brif.md. Mizah: Dante/Villani/Machiavelli/çeyiz; veba ve Ciompi'nin ezilişi KAPALI."""
PRON = [
    (r"\bGiovanni di Bicci\b", "Covanni di Biççi"), (r"\bPiccarda Bueri\b", "Pikkarda Bueri"),
    (r"\bVieri di Cambio\b", "Vyeri di Kambiyo"), (r"\bVieri\b", "Vyeri"),
    (r"\bVia Porta Rossa\b", "Viya Porta Rossa"), (r"\bVia Calimala\b", "Viya Kalimala"),
    (r"\bOrsanmichele\b", "Orsanmikele"), (r"\bVillani\b", "Villani"), (r"\bEdward\b", "Edvard"),
    (r"\bBoccaccio\b", "Bokkaço"), (r"\bMarchionne di Coppo Stefani\b", "Markyonne di Koppo Stefani"),
    (r"\bPeruzzi\b", "Perutsi"), (r"\bCiompi\b", "Çompi"), (r"\bMichele di Lando\b", "Mikele di Lando"),
    (r"\bSalvestro\b", "Salvestro"), (r"\bMachiavelli\b", "Makyavelli"), (r"\bgonfaloniere\b", "gonfalonyere"),
    (r"\bPalazzo Vecchio\b", "Palattso Vekkyo"),
]

CH = dict(id="c1", n="I", title="Florin Şehri", years="1252 – 1397", mood="curious", front="ALTIN",
          paras=[[
              ("1252'de Floransa kendi altınını basmaya başladı; kendini küçük görmeyen bir şehrin işiydi bu.", None, "◐ M1:#4 + YORUM"),
              ("Adı florin: yaklaşık üç buçuk gram ağırlığında, neredeyse saf altın.", None, "◐ M1:#4,§4A"),
              ("Şehrin en ünlü şairi Dante, bu altına “lanetli çiçek” dedi: çobanı kurda çeviren çiçek.", None, "◐ ifade M1:D01 (çeviri bize ait; terzina söylenmez)"),
              ("Floransa, yine de, basmaya devam etti.", None, "◐ M1:#6 (mizah a)"),
          ], [
              ("Kronikçi Giovanni Villani eski bir darphane yöneticisiydi; yani sayı saymayı bilirdi.", None, "◐ M1:#12,D02 + YORUM"),
              ("1338'de kenti de saydı: ona göre Floransa'da yaklaşık doksan bin kişi yaşıyordu ve çocuklar okuma yazmanın yanında hesap okullarına da gidiyordu.", None, "◐ \"Villani'ye göre\" M1:D02"),
              ("Defterlerin şehri böyle yetişiyordu.", None, "YORUM"),
          ], [
              ("Çok şubeli banka da Medici'nin icadı değildi: bir kaynağa göre, 1330'larda Peruzzi bankasının on beş şubesi vardı.", None, "◐/○ M1:#11,düz2,mit2 (\"bir kaynağa göre\")"),
              ("Peruzzi de Bardi de 1340'larda battı; sebep olarak çoğu zaman İngiltere Kralı {III. Edward|Üçüncü Edvard}'ın ödemediği borçlar gösterilir.", None, "◐ M1:#13,düz2,mit4 (\"gösterilir\")"),
              ("Bu borcu kaydeden kronikçi Villani'nin kardeşi de Peruzzi'de çalışıyordu; yani sayıyı veren adam, kaybedenlerin ailesindendi.", None, "◐ M1:#14,D08 (mizah b; tarafsızlık notu)"),
              ("Veba, 1348 Mart'ında geldi ve yaz boyunca şehri bırakmadı.", None, "◐ M1:#15 + kurul KA1-K3/KA2-Ö2 (Boccaccio Mart–Temmuz sayımı, Stefani Eylül: 'yaz boyunca' ikisiyle uyumlu)"),
          ], [
              ("Boccaccio anlatır: sağlıklılar hastadan kaçıyor, hasta yalnız ölüyor, cesetler evlerde ve sokaklarda yığılıyordu.", None, "◐ M1:D03 (\"anlatır\")"),
              ("Marchionne di Coppo Stefani o yıl on iki yaşındaydı; yıllar sonra yazdığı kronikte, ölülerin toplu çukurlara konup üstlerinin katman katman toprakla örtüldüğünü anlatır.", None, "◐ M1:D04 (History Today özeti; birebir söz yok)"),
              ("Ne düşündüğünü bilmiyoruz; ne gördüğünü yazdığını biliyoruz.", None, "YORUM (kalıp)"),
          ], [
              ("1378'de bu kez ölüm değil, öfke sokaktaydı.", None, "YORUM"),
              ("O yılın Mayıs'ında, Medici ailesinin başka bir kolundan Salvestro, kurayla şehrin başı sayılan gonfaloniere olmuştu.", None, "● Machiavelli, Ist. fior. III ('was drawn Gonfalonier', Mayıs–Haziran 1378 Signoria'sı; Giovanni'nin atası DEĞİL düz9) — kurul tur 1 başkan doğrulaması"),
              ("Ama Floransa'yı asıl döndüren yün işçilerinin loncası yoktu; yani sesi de yoktu.", None, "◐ M1:#19,D06"),
              ("22 Temmuz'da Ciompi denen bu işçiler Palazzo Vecchio'yu ele geçirdi; bir yün tarayıcısı, Michele di Lando, gonfaloniere oldu.", None, "● Machiavelli III (görevdeki gonfaloniere Luigi Guicciardini; Salvestro'nun dönemi Haziran'da bitmişti) — kurul KA1-K2/KA2-Ö1"),
              ("Talepleri, yazıldığına göre, vergide adalet, işçilere lonca hakkı ve kamu borcunun azaltılmasıydı.", None, "○ M1:#19 (tek kaynak; \"yazıldığına göre\")"),
              ("Bir buçuk asra yakın sonra, Medici'nin siparişiyle tarih yazan Machiavelli, adı bile belli olmayan bir isyancının ağzına koca bir konuşma koydu.", None, "◐ M1:D07,mit11 (mizah c; kurgu uyarısı)"),
              ("Konuşma tarihçinin; isyancının değil.", None, "◐ M1:D07"),
              ("Ağustos sonunda loncaların milisleri isyanı ezdi.", None, "◐ M1:#21"),
              ("Yün işçilerinin kısa ömürlü loncası kaldırıldı; yönetimden de dışlandılar.", None, "◐ M1:#21 + kurul KA1-V5 (dayanaksız 'en kanlı' iddiası kaldırıldı; mizah YOK)"),
          ], [
              ("Medici'nin bu kolu o yıllarda şehrin seçkinlerinin bir kademe altındaydı; kır gelirleriyle geçiniyordu.", None, "◐ M1:D09 + kurul KA1-V4/KA2-K1 (genelleme Giovanni'nin koluna daraltıldı)"),
              ("Bu ailenin Giovanni di Bicci adlı üyesi, babasının mütevazı mirasından küçük bir pay aldı.", None, "◐ M1:D09"),
              ("Roma'da Vieri di Cambio'nun bankasında çalıştı; Vieri çekilince, 1390'ların başında, Roma işinin alacak ve borçlarını devraldı.", None, "◐ M1:#23,#24 (1391–93 çelişkili → \"1390'ların başında\")"),
              ("Ortaklığa karısı Piccarda Bueri'nin bin beş yüz florinlik çeyiziyle girdi; hanedanın ilk sermayesi, diyelim ki, bir evlilik sözleşmesiydi.", None, "◐ M1:#23,D09 (mizah b, sıcak)"),
              ("1397'de işi Roma'dan Floransa'ya taşıdı: Orsanmichele yakınında, Via Porta Rossa ile Via Calimala'nın kesiştiği köşeye.", None, "◐ M1:#25,D10,düz1 (\"kurdu\" denmez)"),
              ("Sermaye on bin florindi.", None, "◐ toplam M1:#26"),
              ("Orsanmichele'nin köşesinde artık bir masa ve bir defter vardı.", None, "YORUM"),
          ], [
              ("Para kazanmanın yolu belliydi.", None, "YORUM"),
              ("Zor olan, Kilise'nin “faiz günahtır” dediği bir çağda onu huzurla kazanmaktı.", None, "◐ faiz yasağı M1:K2"),
          ]])
