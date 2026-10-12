import sys, json, numpy as np
sys.path.insert(0, '.')
import asr, narrator
exec(open('../dans-vebasi/tts.py').read().split("SENTENCES = [")[0].split("import glob")[0]) if False else None
SENT=[("A","Bir kadın sokakta dansa başladı, ve *günlerce duramadı!*",1.0,1.1,0.26),
("B","Ama asıl çılgınlık, *yetkililerin çözümüydü!*",1.02,1.1,0.22),
("C","Yıl *1518=bin_beş_yüz_on_sekiz*, Strazburg.",1.0,1.0,0.20),
("D","Bir haftada *34=otuz_dört* kişi katıldı, bir ayda *400=dört_yüz!*",1.04,1.15,0.22),
("E","Yemek yok, uyku yok! Yorgunluktan yığılanlar bile oldu!",1.04,1.15,0.20),
("F","Doktorlar *sıcak kan* dedi. Çözüm mü? *Daha fazla dans!*",1.04,1.15,0.20),
("G","Sahne kurdular, *müzisyenler tuttular!*",1.02,1.1,0.22),
("H","Dans bitmek yerine, *daha da yayıldı!*",1.02,1.15,0.24),
("I","Sonunda müziği yasakladılar, ve dansçıları bir türbeye götürdüler.",1.02,1.0,0.24),
("J","Bilim insanları hâlâ emin değil: *ergot zehirlenmesi mi, toplu histeri mi?*",1.04,1.05,0.26),
("K","Ve dans, *müzik susunca bitti!*",1.0,1.15,0.55),
("L","Bazen çözüm, *sessizliktir.*",0.90,0.9,0.0)]
LEX=json.load(open('lex.json')) if __import__('os').path.exists('lex.json') else {}
narrator.LEX.update(LEX)
T,tot,buf=narrator.render(SENT,"out_dans",voice="dfki",profile=dict(speed=1.10))
tl=json.load(open("out_dans/timeline.json")); tw=0
for s in tl["sentences"]:
    a=int(s["t0"]*48000); b=int(s["t1"]*48000)+int(0.3*48000)
    ref=" ".join(w["show"] for w in s["words"])
    hyp=asr.transcribe(buf[a:b],48000); e=asr.wer(ref,hyp); tw+=e
    print(f"{s['id']} {e:.2f} | {hyp}")
print("süre",round(tot,1),"ort WER",round(tw/len(tl['sentences']),3))
