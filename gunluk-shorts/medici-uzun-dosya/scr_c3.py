"""c3 — Kule ve Sürgün (1433–1464). Brif: brif/c3_brif.md. Gerilim → sessiz güç. Mizah ölçülü (sistem/kaynak); 1464 ölümünde kapalı."""
PRON = [
    (r"\bAlberghettino\b", "Albergettino"), (r"\bBernardo Guadagni\b", "Bernardo Guadanyi"),
    (r"\bRinaldo degli Albizzi\b", "Rinaldo delyi Albittsi"), (r"\bAlbizzi\b", "Albittsi"),
    (r"\bMichelozzo\b", "Mikelottso"), (r"\bSignoria\b", "Sinyoriya"), (r"\bSanta Maria Nuova\b", "Santa Maria Nuova"),
    (r"\bMarsilio Ficino\b", "Marsilyo Fiçino"), (r"\bFicino\b", "Fiçino"), (r"\bCareggi\b", "Karecci"),
    (r"\bPadgett\b", "Pedcet"), (r"\bAnsell\b", "Ansel"), (r"\bcompagnia\b", "kompanya"), (r"\bOrfik\b", "Orfik"),
]

CH = dict(id="c3", n="III", title="Kule ve Sürgün", years="1433 – 1464", mood="tense", front="",
          paras=[[
              ("Eylül 1433'te Cosimo, Palazzo Vecchio'ya çağrıldı ve tutuklandı.", None, "◐ M2:K06 (gün söylenmez)"),
              ("Kapatıldığı hücrenin adı Alberghettino'ydu: Küçük Han.", None, "◐ M2:K06 (mizah a: adın kendisi)"),
              ("Bir tutukevi için fazla konuksever bir ad.", None, "YORUM"),
              ("Tek penceresinin dar yarığından şehre bakabildiği anlatılır.", None, "◐ M2:C3.1 (\"anlatılır\")"),
              ("Gonfaloniere Bernardo Guadagni'ydi; arkasında Rinaldo degli Albizzi vardı.", None, "◐ M2:K06"),
              ("Suçlama, halk yönetiminde kendini sıradan yurttaşın üstüne çıkarmaktı; ölüm cezası ihtimali masadaydı.", None, "◐ M2:K06 (History Today özeti)"),
          ], [
              ("Aynı Machiavelli'ye göre Cosimo zehirlenmekten korkup yalnız ekmek yedi; bekçi, getirilen her yemekten kendisi yiyerek onu rahatlattı.", None, "ANEKDOT ◐ M2:K07 (Machiavelli ≈90 yıl sonra; bekçi adı söylenmez)"),
              ("Yine ona göre Cosimo, aracısına küçük bir kâğıt verdi; Santa Maria Nuova hastanesinin başkanından bin yüz duka çekildi, bini gonfaloniere'ye gitti.", None, "ANEKDOT ◐ M2:K08,C3.3"),
              ("Ölüm cezası, sürgüne döndü.", None, "ANEKDOT ◐ M2:K08"),
              ("Aradaki fark, küçük bir kâğıttı.", None, "YORUM (mizah a)"),
          ], [
              ("3 Ekim 1433'te Cosimo, Signoria'nın önüne çıktı ve Padova'ya gönderildi.", None, "◐ M2:K09,D3 (\"serbest bırakıldı\" DEĞİL)"),
              ("Kaynaklar sürgünün süresinde anlaşamıyor: bir yıl diyen de var, yirmi yıl diyen de; çoğu anlatıda on yıl.", None, "◐ çelişki M2:§3,M1:#41 (mizah a)"),
              ("Çok geçmeden Venedik'e geçti; Venedik onu bir diplomat gibi karşıladı ve Floransa'ya elçi gönderdi.", None, "◐ M2:K10,C3.6"),
              ("Yanında mimar Michelozzo vardı.", None, "◐ M2:K10"),
          ], [
              ("Bu sırada Floransa'da rüzgâr değişiyordu.", None, "YORUM"),
              ("Ağustos sonunda kura Cosimo yanlısı bir Signoria çıkardı; Rinaldo degli Albizzi ise ona karşı olağanüstü yetkili bir kurul toplatmaya çalıştı.", None, "◐ M2:K11"),
              ("Eylül sonunda sürgün kararı kalktı; 6 Ekim 1434'te Cosimo Floransa'ya döndü.", None, "◐ M2:K13,K14 (29 Eylül söylenmez)"),
              ("Albizzi'lerin ıssız kalmış konaklarının önünden geçtiği anlatılır.", None, "○ M2:K14 (EB1911 özeti; \"anlatılır\")"),
              ("Rinaldo degli Albizzi ile, 1427'de şehrin en zengini sayılan Palla Strozzi sürgüne gönderildi.", None, "◐ M2:K15; M1:#39 (kaç kişi söylenmez)"),
              ("O gün kimse bilmiyordu ki bu adam, taç takmadan otuz yıl yönetecekti.", None, "◐ 1464 ölümü; \"otuz yıl\"=hesap; DBI/EI \"hiçbir zaman signore olmadı\" (\"hiç makam tutmadı\" DENMEZ)"),
          ], [
              ("Papa II. Pius'a göre Cosimo, adı ve hukuki statüsü dışında bir kraldı.", None, "◐ M2:C3.7 (History Today, Kimblin; Latince okunmadı; çeviri bize ait)"),
              ("Düzenin sırrı torbalardı: Signoria üyeleri torbalardan kurayla çekilirdi.", None, "◐ M2:K16,§2A"),
              ("Cosimo yıllarca, torbaların bir daha kendi çıkarına karşı bir Signoria çıkarmaması için uğraştı.", None, "◐ amaç M2:K16 (NYRB 2003)"),
              ("Kura vardı; torbaya kimin gireceğine ise kura karar vermiyordu.", None, "YORUM (mizah a: kurum)"),
              ("Sosyologlar Padgett ile Ansell bunu bir ağ olarak çizdi: birbirine bağlı olmayan aile grupları yalnız Medici üzerinden birbirine bağlanıyordu.", None, "◐ M1b:bM12,bD16 (ayrıntı rakamları söylenmez)"),
          ], [
              ("Bu iktidarın arka odasında yine bir defter vardı.", None, "YORUM"),
              ("Şube müdürleri sermayeden küçük, kârdan büyük pay alırdı; yani herkes kendi şubesinin hesabını kollardı.", None, "◐ M1:D22,§5C + YORUM"),
              ("1435'ten 1450'ye kadar banka iki yüz doksan bini aşkın florin kâr yazdı; kayıtlara göre bunun yarıdan fazlası Roma'dan geliyordu.", None, "◐ M1:#52,§4C; ◐/○ M1:#54"),
              ("“Holding” sözcüğü sonradan eklendi; o günlerde buna compagnia denirdi.", None, "◐ M1:§5C (çıkarım)"),
          ], [
              ("Cosimo 1 Ağustos 1464'te öldü; Careggi'deki villasında öldüğü yazılır.", None, "◐ M1:#56 + ○ yer M2:K26 (yaş söylenmez: doğum günü çelişkili M5; Careggi mektubu c5'te)"),
          ], [
              ("Cosimo'ya atfedilen bir söz var: şehrinin mizacını bilirmiş; elli yıl geçmeden hepsi sürgüne gönderilirmiş, ama binaları kalırmış.", None, "ANEKDOT ○ M3:§5.20 (PBS); M1b:b64–65 (\"diye aktarılır\")"),
              ("Kaynağı belirsiz.", None, "○"),
              ("Sürgün gerçekten geldi, 1494'te; binalar bugün de ayakta.", None, "◐ M1b:b64 (1494 c10'da)"),
          ]])
