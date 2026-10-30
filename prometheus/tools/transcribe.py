"""Seslendirme dosyalarını whisper ile kelime zamanlı yazıya döker ve senaryoyla karşılaştırır.
Kullanım: python3 tools/transcribe.py ses.mp3 [bölüm adı]  -> ses.words.json + hata raporu"""
import sys, json, re, difflib, whisper
path = sys.argv[1]
sec = sys.argv[2] if len(sys.argv) > 2 else None
m = whisper.load_model('small')
r = m.transcribe(path, language='tr', word_timestamps=True, condition_on_previous_text=False, initial_prompt='Prometeus, Ayshilos, Hesiodos, Teogonia, Zeus, Gaya, Uranos, Kronos, Rea, Titan, Tartaros, İapetos, Atlas, Menoitios, Epimeteus, Mekone, Pandora, Hefaistos, Hermes, Kratos, Bia, Okeanos, Temis, İyo, Bosporos, Kerç, Herakles, Göte, Meri Şeli, Frankenştayn, Openhaymır, Azra Erhat, Eyüboğlu, Kafka.')
words = [{'w': w['word'].strip(), 's': round(w['start'], 3), 'e': round(w['end'], 3)} for sg in r['segments'] for w in sg['words']]
json.dump(words, open(path.rsplit('.', 1)[0] + '.words.json', 'w'), ensure_ascii=False)
norm = lambda s: re.sub(r"[^\wçğıöşüâî]+", ' ', s.lower().replace('İ', 'i').replace('I', 'ı').replace("'", '').replace('’', '').replace('â', 'a').replace('î', 'i').replace('û', 'u')).split()
hyp = norm(' '.join(w['w'] for w in words))
if sec:
    d = json.load(open('senaryo.json'))
    ref = norm(' '.join(re.sub(r'\[[^\]]*\]', '', s['tts']) for s in d['segments'] if s['bolum'] == sec))
    sm = difflib.SequenceMatcher(None, ref, hyp)
    errs = [(op, ' '.join(ref[a:b]), ' '.join(hyp[c:d2])) for op, a, b, c, d2 in sm.get_opcodes() if op != 'equal']
    print(f'WER~{sum(max(b-a,d2-c) for op,a,b,c,d2 in sm.get_opcodes() if op!="equal")/len(ref):.3f}', 'dur', words[-1]['e'] if words else 0)
    for e in errs: print('  ', e)
