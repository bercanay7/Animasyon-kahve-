import sys, json, wave, numpy as np
sys.path.insert(0,'.')
import asr
d=sys.argv[1]
tl=json.load(open(f"{d}/out/timeline.json"))
w=wave.open(f"{d}/out/voice.wav"); x=np.frombuffer(w.readframes(w.getnframes()),'<i2').astype(np.float32)/32768
tot=0
for s in tl["sentences"]:
    a=int(s["t0"]*48000); b=int(s["t1"]*48000)+int(0.3*48000)
    ref=" ".join(wd["show"] for wd in s["words"]); hyp=asr.transcribe(x[a:b],48000); e=asr.wer(ref,hyp); tot+=e
    print(f"{s['id']} {e:.2f} | {hyp}", flush=True)
print("ORT WER", round(tot/len(tl['sentences']),3))
