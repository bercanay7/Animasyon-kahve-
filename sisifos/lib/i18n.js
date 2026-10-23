// Ekrandaki yazıların İngilizce sürümü (?lang=en). Anahtar: Türkçe metin; zamanlama ve yerleşim değişmez.
'use strict';
const LANG = (typeof location !== 'undefined' && new URLSearchParams(location.search).get('lang')) || 'tr';
const I18N_EN = {
  'SİSİFOS': 'SISYPHUS', 'Tanrıları kandıran adam': 'The man who fooled the gods', 'NEDEN?': 'WHY?', 'mutlu?': 'happy?',
  'EFİRA': 'EPHYRA', 'KORİNT': 'CORINTH', 'iki deniz arasında': 'between two seas',
  'BÖLÜM I': 'CHAPTER I', 'BÖLÜM II': 'CHAPTER II', 'BÖLÜM III': 'CHAPTER III', 'BÖLÜM IV': 'CHAPTER IV', 'BÖLÜM V': 'CHAPTER V', 'BÖLÜM VI': 'CHAPTER VI',
  "KORİNT'İN KURNAZ KRALI": 'THE CUNNING KING OF CORINTH', 'KARTAL VE PINAR': 'THE EAGLE AND THE SPRING', 'ÖLÜMÜ ZİNCİRLEYEN ADAM': 'THE MAN WHO CHAINED DEATH',
  'İKİNCİ HİLE': 'THE SECOND TRICK', 'CEZA': 'THE PUNISHMENT', 'CAMUS VE ABSÜRT': 'CAMUS AND THE ABSURD',
  'Korint Körfezi': 'Gulf of Corinth', 'Saron Körfezi': 'Saronic Gulf', 'Egina': 'Aegina', 'PELOPONNESOS': 'PELOPONNESE', 'ATTİKA': 'ATTICA',
  'ZEKÂ': 'MIND', 'HOMEROS': 'HOMER', 'Kör ozan, İlyada ve Odysseia': 'The blind poet of the Iliad and the Odyssey',
  '“insanların en kurnazı”': '“the craftiest of men”', '— HOMEROS, İLYADA VI.153': '— HOMER, ILIAD VI.153',
  'AUTOLYKOS': 'AUTOLYCUS', 'Ünlü hırsız': 'A famous thief', 'GECE I': 'NIGHT I', 'GECE II': 'NIGHT II', 'GECE III': 'NIGHT III',
  'AUTO|LYKOS': 'AUTO|LYCUS', 'BENİ|AUTOLYKOS|ÇALDI': 'AUTOLYCUS|STOLE|ME',
  'Tanrıların kralı': 'King of the gods', 'EGİNA': 'AEGINA', "Irmak tanrısı Asopos'un kızı": 'Daughter of the river god Asopus',
  'ASOPOS': 'ASOPUS', 'Irmak tanrısı': 'River god', 'Ölüm': 'Death', 'Savaş tanrısı': 'God of war',
  "Sisifos'un karısı": 'Wife of Sisyphus', 'GÖMME': 'BURIAL', 'TÖREN': 'RITES', 'ADAK': 'OFFERINGS',
  'PERSEFONİ': 'PERSEPHONE', 'Ölülerin kraliçesi': 'Queen of the dead', 'Yeraltının kralı': 'King of the underworld',
  'yıllar…': 'years…', 'Tanrıların habercisi': 'Messenger of the gods',
  'TARTAROS': 'TARTARUS', 'ZİRVE': 'SUMMIT', '2. GÜN': 'DAY 2', '3. GÜN': 'DAY 3', '100. YIL': 'YEAR 100', '1000. YIL': 'YEAR 1000',
  '“Hiçbir işe yaramayan, umutsuz bir emekten daha korkunç bir ceza yoktur.”': '“There is no more dreadful\npunishment than futile\nand hopeless labor.”',
  'Sisifos Söyleni': 'The Myth of Sisyphus', '1913 – 1960 · yazar, düşünür': '1913 – 1960 · writer, thinker',
  '“Bütün bunlar ne için?”': '“What is all this for?”', 'anlam arayan insan  ·  sessiz kalan dünya': 'the human need for meaning  ·  the silence of the world',
  'ABSÜRT': 'ABSURD', 'bilincin saati': 'the hour of consciousness', '— son satırlar —': '— the closing lines —',
  '“Zirvelere doğru verilen mücadelenin kendisi,\nbir insan yüreğini doldurmaya yeter.”': '“The struggle itself toward the heights\nis enough to fill a man’s heart.”',
  '“Sisifos’u mutlu hayal etmek gerekir.”': '“One must imagine Sisyphus happy.”', '“Sisifos’u mutlu\nhayal etmek gerekir.”': '“One must imagine\nSisyphus happy.”',
  'iş': 'job', 'sorumluluk': 'duty', 'hayal': 'dream', 'her sabah': 'every morning',
  'Senin kayan ne?': 'What is your rock?', 'sen?': 'you?', 'Senin kayan neyse, yorumlarda anlat.': 'Whatever your rock is, tell us in the comments.',
};
function L(s) {
  if (LANG !== 'en' || typeof s !== 'string') return s;
  if (s in I18N_EN) return I18N_EN[s];
  let m;
  if ((m = s.match(/^MÖ (\d+)$/))) return m[1] + ' BC';
  if ((m = s.match(/^MS (\d+)$/))) return 'AD ' + m[1];
  return s;
}
// konumsal sözcük dizileri (sözcük sırası dile göre değişir)
const LA = a => L(a.join('|')).split('|');
