"""Bütün bölüm çekimlerini Whisper ile kelime zamanlı yazıya döker ve senaryoya karşı karşılaştırır.
Kullanım: python3 tools/transcribe_all.py [iş parçacığı]  → vo/sNN_x.words.json + vo/rapor.json
Bir dosyanın .words.json'u varsa atlanır (kaldığı yerden sürer)."""
import sys, os, json, re, difflib, glob
import torch, whisper
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
torch.set_num_threads(int(sys.argv[1]) if len(sys.argv) > 1 else 4)
only = sys.argv[2].split(',') if len(sys.argv) > 2 else None
P = "Prometeus, Ayshilos, Hesiodos, Teogonia, Zeus, Gaya, Uranos, Kronos, Rea, Titan, Tartaros, İapetos, Atlas, Menoitios, Epimeteus, Mekone, Pandora, Hefaistos, Hermes, Kratos, Bia, Okeanos, Temis, İyo, Bosporos, Kerç, Herakles, Göte, Meri Şeli, Frankenştayn, Openhaymır, Azra Erhat, Eyüboğlu, Kafka."
norm = lambda s: re.sub(r"[^\wçğıöşüâî]+", ' ', s.lower().replace('İ', 'i').replace('I', 'ı').replace("'", '').replace('’', '').replace('â', 'a').replace('î', 'i').replace('û', 'u')).split()
secs = {s['onek']: s for s in json.load(open(os.path.join(ROOT, 'vo', 'bolumler.json')))}
m = whisper.load_model('small')
rep_p = os.path.join(ROOT, 'vo', 'rapor.json')
rep = json.load(open(rep_p)) if os.path.exists(rep_p) else {}
for f in sorted(glob.glob(os.path.join(ROOT, 'vo', 's[0-9][0-9]_[ab].mp3'))):
    key = os.path.basename(f)[:-4]; onek = key[:3]
    if only and onek not in only: continue
    wj = f[:-4] + '.words.json'
    if not os.path.exists(wj):
        r = m.transcribe(f, language='tr', word_timestamps=True, condition_on_previous_text=False, initial_prompt=P)
        words = [{'w': w['word'].strip(), 's': round(w['start'], 3), 'e': round(w['end'], 3)} for sg in r['segments'] for w in sg['words']]
        json.dump(words, open(wj, 'w'), ensure_ascii=False)
    words = json.load(open(wj))
    ref = norm(re.sub(r'\[[^\]]*\]', ' ', secs[onek]['metin'])); hyp = norm(' '.join(w['w'] for w in words))
    sm = difflib.SequenceMatcher(None, ref, hyp, autojunk=False)
    ops = [(op, ' '.join(ref[a:b]), ' '.join(hyp[c:d])) for op, a, b, c, d in sm.get_opcodes() if op != 'equal']
    wer = sum(max(b - a, d - c) for op, a, b, c, d in sm.get_opcodes() if op != 'equal') / max(1, len(ref))
    rep[key] = {'wer': round(wer, 4), 'sure': words[-1]['e'] if words else 0, 'hatalar': ops}
    json.dump(rep, open(rep_p, 'w'), ensure_ascii=False, indent=1)
    print(key, f'WER {wer:.3f}', f"{rep[key]['sure']:.1f} sn", flush=True)
