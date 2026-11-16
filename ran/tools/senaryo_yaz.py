"""ran/senaryo.json ve senaryo_okuma.md üretir. Kimlikler kesinleşti; cümle çıkarılırsa numarası boş kalır (Kafka dersi)."""
import json, os, re
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = []
ALT = {"Bu, Akira Kurosawa'nın Ran'ı. Japoncada kargaşa demek. Yıl, bin dokuz yüz seksen beş.": "Bu, Akira Kurosawa'nın Ran'ı. Japoncada kargaşa demek. Yıl 1985."}
def b(bolum, rows):
    for i, (tag, txt, kay) in enumerate(rows): S.append(dict(id=None, bolum=bolum, tts=(f'[{tag}] ' if tag else '') + txt.replace('Mōri', 'Mori').replace('Yōko', 'Yoko'), alt=ALT.get(txt, txt), kaynak=kay))
P = 'Ran olay örgüsü (Wikipedia "Ran (film)", Plot; Ebert 1985)'
b('Yanan kale', [
 ('calmly', 'Bir kale yanıyor. İçinden yaşlı bir adam çıkıyor: kılıcı yok, adamları yok, yanında kimse yok.', 'kanca: kullanıcının sahnesi; kapak A; L1 açılır (cevap E05)'),
 ('', 'Bir ömür boyunca kurduğu her şeyi, birkaç gün önce kendi eliyle oğullarına vermişti.', P),
 ('curious', 'Peki şimdi neden tek başına? Ve asıl soru şu: yaptıkların bir gün sana döner mi?', 'başlığın sorusu ilk 10 sn içinde; cevap H07'),
 ('', 'Bu, Akira Kurosawa\'nın Ran\'ı. Japoncada kargaşa demek. Yıl, bin dokuz yüz seksen beş.', 'Ran 乱 = kargaşa, karmaşa. Künye: AKIRA KUROSAWA · RAN · 1985'),
 ('', 'Kurosawa bu sahneyi çekmeden çok önce, resim olarak çizmişti.', 'K3 (Positif 296; TCM)'),
])
b('Resimlerle çekilen film', [
 ('', 'Senaryoyu yetmişli yılların ortasında yazdı. Ama hiçbir stüdyo bu kadar pahalı bir filme para vermedi.', 'K3, K5 (Wikipedia: senaryo 1975, Positif 296; TCM "preparing for a decade")'),
 ('', 'Kurosawa beklerken filmi kare kare boyadı. Yüzlerce resim.', 'K3 (TCM "hundreds of highly detailed storyboard illustrations")'),
 ('', 'Para ancak yıllar sonra, bir Fransız yapımcıyla geldi. Çekim başladığında Kurosawa yetmişini geçmişti ve gözleri iyice zayıflamıştı.', 'K4, K5 (Silberman; çekim 1983, Galbraith; TCM "nearly blind"). "Kör" denmez'),
 ('', 'Ekip sahneleri o resimlere bakarak kurdu.', 'K3 (ikincil: resimler sette şablon)'),
 ('', 'O resimleri burada göstermeyeceğim; hepsi hâlâ Kurosawa\'nın. Onları kendi fırçamızla yeniden kuracağız.', 'telif: Kurosawa resimleri 2068\'e kadar telifli; üslup açıklaması'),
 ('', 'Hikâyenin kendisi ise çok daha eski: Shakespeare\'in Kral Lear\'ı.', 'Kral Lear (~1606). Arşiv masası: Garrick Lear rolünde, 1761 (Met 707787, CC0)'),
 ('curious', 'Kurosawa ona yalnız tek bir şey ekledi. Shakespeare\'in hiç vermediği bir şey.', 'L2 açılır (cevap D06)'),
])
b('Üç ok', [
 ('', 'Hidetora yaşlı bir savaş beyi. Bütün ömrünü savaşarak bir ülke kurmaya vermiş.', P),
 ('', 'Bir av dönüşü kararını açıklar: artık dinlenecek. Ülkeyi üç oğlu arasında bölecek, ama unvanını ve onurunu koruyacak.', P),
 ('', 'Sonra oğullarına birer ok verir. Tek ok kolayca kırılır. Üç ok bir arada kırılmaz.', P + '; kapak B'),
 ('', 'Bu öğüt eski bir Japon efsanesinden gelir: on altıncı yüzyılda yaşamış bey Mōri Motonari\'nin, oğullarına verdiği öğüt.', 'K2; Motonari 1497–1571; efsane ("üç ok") sonradan anlatılır: "efsaneye göre"'),
 ('', 'Kurosawa\'nın aklına şu soru takılmış: ya bu üç oğul iyi olmasaydı?', 'K2 (Peary, Boston Herald 1986)'),
 ('', 'En küçük oğul Saburo üç oku birden dizinde kırar. Kardeşlerin bu ülkeyi paylaşamayacağını söyler.', P),
 ('', 'Hidetora onu sürgüne gönderir. Tıpkı Lear\'ın, babasına yağ çekmeyi reddeden kızı Cordelia\'yı sürmesi gibi.', 'Kral Lear I.1'),
 ('', 'Lear o gün kızına şöyle der: Hiçten hiç çıkar.', 'KL2: "Nothing will come of nothing" I.1, Gutenberg 261 (çevirimiz)'),
 ('', 'Shakespeare\'de üç kız var, Kurosawa\'da üç oğul. Ama asıl fark başka yerde.', 'ABT: AMA'),
])
b('Kapılar', [
 ('', 'Hidetora önce büyük oğlu Taro\'nun kalesine gider. Orada onu Taro\'nun karısı karşılar: Kaede.', P),
 ('', 'Taro babasına boyun eğmez. Onu kışkırtan Kaede\'dir.', P),
 ('', 'Çünkü Kaede\'nin bir geçmişi var.', P),
 ('', 'Yıllar önce Hidetora onun ailesini kılıçtan geçirmişti. Kaede şimdi o adamın oğlunun karısıydı.', P),
 ('', 'Hidetora\'nın yaralayıp hayatta bıraktığı üç kişi var bu hikâyede. Biri bir canavara dönüşecek.', 'L3 açılır (cevap H04–H05)'),
 ('firmly', 'İşte Kurosawa\'nın eklediği şey buydu: geçmiş.', 'L2 kapanır'),
 ('', 'Kurosawa\'ya göre Shakespeare kahramanlarına bir geçmiş vermez. Ran\'da kralın bir geçmişi var. Ve bu geçmiş kanlı.', 'K1 (Great Performances "Ask the Experts"; TCM; Cornell). Dolaylı anlatım, tırnak yok'),
 ('', 'Taro kapıyı kapatır. Sonra ortanca oğul Jiro da.', P),
 ('', 'Lear da kapı kapı dolaşmıştı. Kızına şöyle haykırır: Nankör bir evladın acısı, yılan dişinden keskindir.', 'KL3: "How sharper than a serpent\'s tooth" I.4, Gutenberg 1448 (çevirimiz)'),
])
b('Üçüncü kale', [
 ('', 'Hidetora ona kalan tek yere, sürgündeki Saburo\'nun boş kalesine sığınır.', P),
 ('', 'Ama Taro ile Jiro\'nun orduları kaleyi kuşatır.', P),
 ('', 'Adamları birer birer düşer. Kale yanar. Hidetora kılıcını arar; kılıcı kırıktır.', P + '. Hassasiyet: seppuku girişimi anlatılmaz, toplu ölüm çizilmez'),
 ('', 'Ve o an gelir: yaşlı adam yanan kaleden yürüyerek iner. Askerler önünden çekilir. Kimse ona dokunmaz.', P + '. Kullanıcının sahnesi; filmin kompozisyonu kopyalanmaz'),
 ('softly', 'Neden tek başına? Çünkü her şeyi kılıçla kurmuştu. Şimdi o kılıç ona dönmüştü.', 'L1 kapanır'),
 ('', 'Kurosawa bu kaleyi Fuji Dağı\'nın eteklerinde gerçekten inşa ettirdi, sonra yaktı. Sahne tek çekimde çekildi; ikinci şans yoktu.', 'K7 (Positif 296; TCM)'),
 ('', 'Lear da bu noktada aklını yitirir. Fırtınanın ortasında bağırır: Esin rüzgârlar, patlatın yanaklarınızı!', 'KL4: "Blow, winds, and crack your cheeks!" III.2, Gutenberg 2944'),
 ('', 'Ve en ünlü sözünü söyler: Ben, günah işlediğinden çok kendisine günah işlenmiş bir adamım.', 'KL5: "More sinn\'d against than sinning" III.2, Gutenberg 3019'),
 ('firmly', 'Lear için bu doğru. Hidetora için değil.', 'omurga (kullanıcının okuması)'),
 ('', 'Bu oyunculuk bazen izleyiciyi iter: abartılı, ağır, maske gibi bir yüz.', 'kullanıcının notu (kopuş)'),
 ('', 'Bu bir kaza değil. Altı yüzyılı aşkın Nō tiyatrosunu andırır: yüz bir maskedir, duygu bedende taşınır.', 'K9 (TCM "classical Noh theater"). Arşiv masası: Nō maskesi, 1336–1573 (Met 60220, CC0)'),
])
b('Flüt', [
 ('', 'Aklını yitiren Hidetora harabelerin arasında dolaşır. Bir gece sığındığı kulübede onu genç bir adam karşılar: Tsurumaru.', P),
 ('', 'Tsurumaru\'nun ailesini Hidetora öldürmüş, gözlerini de Hidetora kör ettirmişti.', P + '. Hassasiyet: yara/kan çizilmez'),
 ('', 'Tsurumaru ona flüt çalar. Hidetora o ezgiye dayanamaz.', 'moviemistakes "ending"; DBU makalesi; kullanıcının ikinci sahnesi'),
 ('softly', 'Asıl savaş artık oğullarıyla değil. Kendi vicdanıyla.', 'omurga (kullanıcının okuması)'),
 ('', 'Tsurumaru\'nun ablası Sue de aynı acıyı yaşamıştı. Ailesi Hidetora\'nın kılıcıyla yok olmuş, kendisi Jiro\'ya gelin verilmişti.', P),
 ('', 'Ama Sue nefret etmedi. Hidetora\'yı affetti.', P + ' + Sue Budizme yönelip Hidetora\'yı affetmişti (Wikipedia eski sürüm, epfl wikispeedia aynası; kurosawainreview). Güven B'),
 ('', 'Kaede ise hiçbir şeyi affetmedi.', 'ABT'),
])
b('Dönüş', [
 ('', 'Sürgündeki Saburo babasını aramaya gelir. Hidetora onu görünce kendine gelir ve oğlundan af diler.', P),
 ('', 'Shakespeare\'de de böyledir: Cordelia döner, yaşlı kral onun önünde diz çökmek ister.', 'Kral Lear IV.7. Arşiv masası: Bartolozzi, Lear ve Cordelia, ~1783 (Met 713083, CC0)'),
 ('', 'Bir an her şey düzelecek gibi olur.', ''),
 ('', 'Ama uzaktan atılan bir kurşun Saburo\'yu vurur. Hidetora oğlunun başında ölür.', P + '. Görsel olarak işlenmez'),
 ('', 'Shakespeare\'de de Cordelia ölür. Lear onu kollarında taşır ve beş kez asla der.', 'KL8: "Never, never, never, never, never!" V.3, Gutenberg 6095'),
 ('', 'Kaede\'nin intikamı da tamamlanır. Hidetora\'nın hanedanı çöker. Kaede bunu baştan beri istediğini söyler ve o da ölür.', P + '. Görsel olarak işlenmez'),
 ('curious', 'Ya Sue? O gece kardeşinin unuttuğu flütü almak için geri döndü. Bir daha gelmedi.', 'L4 (soru + cevap aynı cümlede); ' + P),
])
b('Surdaki adam', [
 ('', 'Filmin son karesi: yıkık bir surun ucunda, kör Tsurumaru, tek başına.', P + '; kapanış ve Shorts'),
 ('', 'Flütü yok. Ablası yok. Ablasının bıraktığı resim de elinden düşer.', P + '. Amida resmi: figür çizilmez'),
 ('softly', 'Hiçbir ses yok.', 'ma: ses bandı sıfır'),
 ('', 'Aynı acıyı üç kişi yaşadı. Kaede yakıp yıktı. Sue affetti. Tsurumaru karanlıkta kaldı.', 'L3 kapanır'),
 ('', 'Kaede bir canavardı. Ama onu canavar yapan Hidetora\'ydı. Yine de aynı yarayı taşıyan Sue başka bir yol seçti.', 'kullanıcının okuması (Kaede masum değil)'),
 ('', 'Kurosawa bu filmi yetmiş beş yaşında bitirdi. Çekimler sürerken otuz dokuz yıllık eşi Yōko\'yu kaybetti; işe yalnız bir gün ara verdi.', 'K6 (Interviews s.128; TCM); Ebert "at 75". Ölüm nedeni söylenmez'),
 ('', 'Lear\'a eklediği geçmiş bize de bir soru bırakıyor.', ''),
 ('thoughtfully', 'Yaptıkların bir gün sana döner mi? Hidetora için, evet.', 'A03\'ün cevabı'),
 ('thoughtfully', 'Ama asıl soru öbürü: sana yapılanla ne yaparsın?', 'kapanış sorusu (iksir); yorum çağrısı'),
 ('', 'Geçmişten bugüne böyle sorular taşıyoruz. Bu yolculuğa devam etmek istersen abone ol.', 'abone çağrısı doruk anında'),
 ('', 'Kayasını her gün yeniden iten bir adamın hikâyesi, Sisifos, şimdi ekranda.', 'bitiş ekranı: "ekranda" son 20 sn içinde'),
])
harf = 'ABCDEFGH'; bol = list(dict.fromkeys(s['bolum'] for s in S)); n = {}
for s in S:
    k = harf[bol.index(s['bolum'])]; n[k] = n.get(k, 0) + 1; s['id'] = f'{k}{n[k]:02d}'
doc = dict(voice='Emrullah (ElevenLabs; voice_id creative_list_voices ile bulunur)', revizyon='rev0 (16 Kasım 2026): başkan taslağı; kurul yok (kullanıcının kararı, kullanım %90)',
           not_='Kaynak: kaynak/KAYNAKLAR.md (Kral Lear Gutenberg #1532 satırları; Kurosawa K1–K10). Çeviriler bizim. İskelet: Harmon çemberi (uretim_plani.md). Film diyaloğu alıntılanmaz.', segments=S)
doc['not'] = doc.pop('not_')
json.dump(doc, open(os.path.join(R, 'senaryo.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
o = ['# Kurosawa, Ran: senaryo (rev0; kurul yok)\n\nOkuma kopyası. Asıl dosya `senaryo.json` (üretici `tools/senaryo_yaz.py`).\n']
for bo in bol:
    o.append(f'\n## {bo}\n')
    for s in S:
        if s['bolum'] == bo: o.append(f"- **{s['id']}** {s['alt']}" + (f"  _({s['kaynak']})_" if s['kaynak'] else ''))
open(os.path.join(R, 'senaryo_okuma.md'), 'w', encoding='utf-8').write('\n'.join(o) + '\n')
c = sum(len(s['tts']) for s in S); w = sum(len(s['alt'].split()) for s in S)
print(len(S), 'cümle;', c, 'karakter (tts);', w, 'kelime; ~', round(w / 2.3 / 60, 1), 'dk (2,3 kelime/sn)')
