import json,sys
exec(open(sys.argv[1]).read())
seg=[]
for ln in S.strip().split('\n'):
    p=ln.split('|'); assert len(p)==5, ln
    i,b,alt,tts,k=p
    seg.append(dict(id=i,bolum=b,tts=tts or alt,alt=alt,kaynak=k))
d=dict(voice="Emrullah (ElevenLabs; voice_id creative_list_voices ile bulunur)",revizyon=sys.argv[3],
 not_="",segments=seg)
d={"voice":d["voice"],"revizyon":d["revizyon"],"not":"Kaynaklar: kaynak/DOGRULAMA.md. Çeviriler bizim. İskelet: Kahramanın Yolculuğu, kahraman lale (uretim_plani.md §4).","segments":seg}
json.dump(d,open(sys.argv[2],'w'),ensure_ascii=False,indent=1)
w=sum(len(x['alt'].split()) for x in seg); c=sum(len(x['tts']) for x in seg)
print(len(seg),'cümle',w,'kelime',c,'tts karakter')
