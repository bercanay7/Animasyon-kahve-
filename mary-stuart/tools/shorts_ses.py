"""Shorts sesi: shorts/edl.json kesitleri audio/mix.wav'dan (40 ms yumuşak geçişle), son kartta yalnız müzik (M12'den); -14 LUFS / -1,5 dBTP.
python3 tools/shorts_ses.py → shorts/mix_shorts.wav"""
import json, subprocess, os, re
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); A = lambda p: os.path.join(R, p)
e = json.load(open(A('shorts/edl.json'))); tl = open(A('timeline.js'), encoding='utf-8').read()
M12 = json.loads(tl.split('window.CUES = ')[1].split(';\n')[0])['M12']['s']
ins, flt = [], []
for i, k in enumerate(e['kesit']):
    d = k['src1'] - k['src0']; ins += ['-ss', f"{k['src0']:.3f}", '-t', f'{d:.3f}', '-i', A('audio/mix.wav')]
    flt.append(f'[{i}:a]afade=t=in:d=0.04,afade=t=out:st={d - .04:.3f}:d=0.04[a{i}]')
n = len(e['kesit']); d = e['son']['d']
ins += ['-ss', f'{M12:.3f}', '-t', f'{d:.3f}', '-i', A('audio/music.wav')]
flt.append(f'[{n}:a]volume=-8dB,afade=t=in:d=0.3,afade=t=out:st={d - 1.2:.3f}:d=1.2[a{n}]')
fc = ';'.join(flt) + ';' + ''.join(f'[a{i}]' for i in range(n + 1)) + f'concat=n={n + 1}:v=0:a=1,aresample=48000[o]'
tmp = A('shorts/_ham.wav'); subprocess.run(['ffmpeg', '-y', '-v', 'error', *ins, '-filter_complex', fc, '-map', '[o]', tmp], check=True)
r = subprocess.run(['ffmpeg', '-hide_banner', '-i', tmp, '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json', '-f', 'null', '-'], capture_output=True, text=True).stderr
m = json.loads(r[r.rindex('{'):r.rindex('}') + 1])
af = f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true"
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', tmp, '-af', af + ',aresample=48000', '-c:a', 'pcm_s16le', A('shorts/mix_shorts.wav')], check=True); os.remove(tmp)
print('shorts/mix_shorts.wav', e['DUR'], 'sn')
