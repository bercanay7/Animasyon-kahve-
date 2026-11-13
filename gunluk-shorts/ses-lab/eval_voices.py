import sys, json, wave, numpy as np
sys.path.insert(0, '.')
import asr, narrator
SENT = [("A","Bir kadın sokakta dansa başladı, ve *günlerce duramadı!*",1.0,1.1,0.2),
 ("B","Ama asıl çılgınlık, *yetkililerin çözümüydü!*",1.0,1.1,0.2),
 ("C","Yıl *1518=bin_beş_yüz_on_sekiz*, Strazburg.",1.0,1.0,0.2),
 ("D","Bir haftada *34=otuz_dört* kişi katıldı, bir ayda *400=dört_yüz!*",1.0,1.1,0.2),
 ("E","Yemek yok, uyku yok! Yorgunluktan yığılanlar bile oldu!",1.0,1.1,0.2),
 ("F","Doktorlar *sıcak kan* dedi. Çözüm mü? *Daha fazla dans!*",1.0,1.1,0.2),
 ("J","Bilim insanları hâlâ emin değil: *ergot zehirlenmesi mi, toplu histeri mi?*",1.0,1.0,0.2),
 ("L","Bazen çözüm, *sessizliktir.*",0.92,0.9,0.0)]
voices = sys.argv[1:] or ["dfki","fahrettin","fettah"]
for v in voices:
    T, tot, buf = narrator.render(SENT, f"out_{v}", voice=v)
    tl = json.load(open(f"out_{v}/timeline.json"))
    tot_w = 0; n = 0
    for s in tl["sentences"]:
        a = int(s["t0"]*narrator.SR); b = int(s["t1"]*narrator.SR)
        ref = " ".join(w["show"] for w in s["words"])
        # referans: söylenen metin (rakamlar kelimeye)
        hyp = asr.transcribe(buf[a:b+int(0.3*narrator.SR)], narrator.SR)
        w_ = asr.wer(ref, hyp); tot_w += w_; n += 1
        print(f"  {v} {s['id']} WER {w_:.2f} | {hyp}")
    print(f"== {v}: süre {tot:.1f} sn, ortalama WER {tot_w/n:.2f}")
