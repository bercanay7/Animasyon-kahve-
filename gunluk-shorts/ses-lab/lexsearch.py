"""Telaffuz arayıcı: sorunlu kelimeler için alternatif yazımları dener, Whisper'ın en iyi anladığını lex.json'a yazar."""
import sys, json, os
sys.path.insert(0, '.')
import asr, narrator

TARGETS = {   # kelime(küçük) : (içinde geçtiği cümle, aday yazımlar)
 "çılgınlık": ("Ama asıl çılgınlık, yetkililerin çözümüydü!", ["çılgın lık", "çılgınnlık", "çılgınlık", "çıılgınlık", "çılgın-lık"]),
 "strazburg": ("Yıl bin beş yüz on sekiz, Strazburg.", ["strazburg", "strasburg", "estrazburg", "strazbürg", "strazburk", "strazbur g"]),
 "yığılanlar": ("Yorgunluktan yığılanlar bile oldu!", ["yığılanlar", "yıılanlar", "yıhılanlar", "yıyılanlar", "yı ılanlar", "yııılanlar"]),
 "dans!": ("Doktorlar sıcak kan dedi. Çözüm mü? Daha fazla dans!", ["dans!", "dans.", "danns!", "dans ", "danss!"]),
 "zehirlenmesi": ("Ergot zehirlenmesi mi?", ["zehirlenmesi", "zeehirlenmesi", "zehirlenmesi", "zehir lenmesi", "zehirlenmesii"]),
 "histeri": ("Toplu histeri mi?", ["histeri", "histeeri", "hisseteri", "histerii", "his teri", "isteri"]),
 "sahne": ("Sahne kurdular, müzisyenler tuttular!", ["sahne", "sahnee", "sahnê", "sah ne"]),
}
ONE = {"A": None}
tts = narrator.load_tts("dfki", narrator.PROFILE)
lex = json.load(open('lex.json')) if os.path.exists('lex.json') else {}

def test(sentence, key, cand):
    narrator.LEX.clear(); narrator.LEX.update(lex)
    narrator.LEX[key.rstrip("!.")] = cand.rstrip("!. ") if key.endswith("!") is False else narrator.LEX.get(key, key)
    T, tot, buf = narrator.render([("x", sentence, 1.04, 1.1, 0.0)], "out_tmp", voice="dfki", profile=dict(speed=1.10))
    tl = json.load(open("out_tmp/timeline.json"))["sentences"][0]
    hyp = asr.transcribe(buf[int(tl["t0"] * 48000): int(tl["t1"] * 48000) + 14400], 48000)
    return asr.wer(sentence.replace("!", "").replace("?", ""), hyp), hyp

for key, (sent, cands) in TARGETS.items():
    best = None
    for c in cands:
        if key.endswith("!"):      # 'dans!' : cümle içinde noktalama etkisi → sözlük yerine cümle yazımını dene
            continue
        w, hyp = test(sent, key, c)
        print(f"{key:14s} <- {c:14s} WER {w:.2f} | {hyp}", flush=True)
        if best is None or w < best[0]:
            best = (w, c)
    if best and best[1] != key:
        lex[key] = best[1]
json.dump(lex, open('lex.json', 'w'), ensure_ascii=False, indent=1)
print("LEX:", lex)
