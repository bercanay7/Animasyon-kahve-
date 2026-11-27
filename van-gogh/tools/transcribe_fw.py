"""Seslendirme çekimlerini faster-whisper (MIT; model ağırlıkları MIT) ile kelime zamanlı yazıya döker, senaryoyla karşılaştırır.
milton/tools/transcribe.py'nin faster-whisper sürümü (openai-whisper kapta yok). Kredi harcamaz.
Kullanım: <venv>/bin/python tools/transcribe_fw.py vo/s00_a.mp3 [...]   -> vo/s00_a.words.json + hata raporu (WER, farklar)"""
import sys, json, re, difflib, os, subprocess, numpy as np
from faster_whisper import WhisperModel
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
bol = {b['onek']: b for b in json.load(open(os.path.join(ROOT, 'vo', 'bolumler.json')))}
segs = {s['id']: s for s in json.load(open(os.path.join(ROOT, 'senaryo.json')))['segments']}
m = WhisperModel(os.environ.get('MODEL', 'medium'), device='cpu', compute_type='int8', cpu_threads=4)
IP = "Van Gogh, Vincent, Theo, Jo, Louvre, Arles, Gauguin, Saint-Rémy, Auvers, Utrecht, Amsterdam, Brüksel, İrisler, Bağımsızlar, gulden, frank, Zaman Kuryesi."
BIR = ['', 'bir', 'iki', 'üç', 'dört', 'beş', 'altı', 'yedi', 'sekiz', 'dokuz']; ON = ['', 'on', 'yirmi', 'otuz', 'kırk', 'elli', 'altmış', 'yetmiş', 'seksen', 'doksan']
def sayi(n):   # Türkçe okunuş (sözcük listesi), 0 < n < 1e6
    w = []
    if n >= 1000: k = n // 1000; w += ([] if k == 1 else sayi(k)) + ['bin']; n %= 1000
    if n >= 100: k = n // 100; w += ([] if k == 1 else [BIR[k]]) + ['yüz']; n %= 100
    if n >= 10: w.append(ON[n // 10]); n %= 10
    if n: w.append(BIR[n])
    return w
def ac(words):   # Whisper rakam yazar ("1886'nın", "2.000'den"): sözcüklere aç, süre harf payıyla bölünür, ek son sözcüğe
    out = []
    for x in words:
        mt = re.fullmatch(r"([\d.]+)(['’]?)(\w*)([.,;:!?]*)", x['w'])
        if not mt or not mt.group(1).replace('.', '').isdigit(): out.append(x); continue
        ws = sayi(int(mt.group(1).replace('.', ''))) or ['sıfır']; ws[-1] += mt.group(3)
        L = sum(len(q) for q in ws); t = x['s']; d = x['e'] - x['s']
        for q in ws: e = t + d * len(q) / L; out.append({'w': q, 's': round(t, 3), 'e': round(e, 3)}); t = e
    return out
norm = lambda s: re.sub(r"[^\wçğıöşüâî]+", ' ', s.replace('İ', 'i').replace('I', 'ı').lower().replace("'", '').replace('’', '').replace('â', 'a').replace('î', 'i').replace('û', 'u')).split()
for path in sys.argv[1:]:
    pcm = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-ac', '1', '-ar', '16000', '-f', 'f32le', '-'], capture_output=True).stdout, np.float32)
    seg, _ = m.transcribe(pcm, language='tr', word_timestamps=True, condition_on_previous_text=False, initial_prompt=IP, beam_size=5, vad_filter=False)
    words = [{'w': w.word.strip(), 's': round(w.start, 3), 'e': round(w.end, 3)} for sg in seg for w in sg.words]
    words = ac(words)
    json.dump(words, open(path.rsplit('.', 1)[0] + '.words.json', 'w'), ensure_ascii=False)
    onek = os.path.basename(path).split('_')[0]
    ref = norm(' '.join(re.sub(r'\[[^\]]*\]', '', segs[i]['tts']) for i in bol[onek]['ids']))
    hyp = norm(' '.join(w['w'] for w in words))
    sm = difflib.SequenceMatcher(None, ref, hyp, autojunk=False)
    ops = [(op, ' '.join(ref[a:b]), ' '.join(hyp[c:d])) for op, a, b, c, d in sm.get_opcodes() if op != 'equal']
    wer = sum(max(b - a, d - c) for op, a, b, c, d in sm.get_opcodes() if op != 'equal') / max(1, len(ref))
    print(f'== {os.path.basename(path)} WER~{wer:.3f} süre {words[-1]["e"] if words else 0}', flush=True)
    for e in ops: print('   ', e, flush=True)
