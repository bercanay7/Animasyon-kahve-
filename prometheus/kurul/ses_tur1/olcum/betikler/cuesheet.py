import sys, json, numpy as np
sys.path.insert(0, '/home/user/Animasyon-kahve-/prometheus/audio')
import score as S
REC = []
span2 = ['piano_arp', 'bed', 'lyre_ost', 'wind', 'crackle', 'war_drums', 'heartbeat', 'ripples', 'arp', 'wings', 'gadfly', 'typewriter']
span_notes = ['pad', 'drone', 'choir']
seq = ['bowed', 'aulos', 'lyre_line']
point = {'fire_motif': 2.2, 'chain_motif': 3.5, 'hammer': .5, 'chain_rattle': .7, 'thunder': 1.5, 'eagle_cry': .75, 'boom': 1.0, 'throne_hit': 1.0,
         'quake': 2.0, 'whoosh': .45, 'metal': .6, 'thud': .3, 'debris': .6, 'bell': 2.0, 'piano': 1.5, 'strum': 1.5, 'lyre': 1.5, 'pizz': .5,
         'fdrum': .4, 'riser': 0, 'swell_into': 0, 'clinks': .5}
def mk(name):
    def f(*a, **k):
        if name in span2: t0, t1 = a[0], a[1]
        elif name in span_notes: t0, t1 = a[1], a[2]
        elif name in seq: t0 = a[1] if name == 'lyre_line' and False else a[0]; ph = a[1]; t1 = t0 + sum(p[1] for p in ph)
        elif name in ('riser',): t1 = a[0]; t0 = a[0] - a[1]
        elif name in ('swell_into',): t1 = a[0]; t0 = a[0] - (a[1] if len(a) > 1 else k.get('dur', 1.6))
        else: t0 = a[0]; t1 = t0 + point[name]
        REC.append((name, float(t0), float(t1), k.get('inst', ''), k.get('gain', k.get('vel', None))))
    return f
for n in span2 + span_notes + seq + list(point): setattr(S, n, mk(n))
for f in (S.s00_opening, S.s01_question, S.s02_thrones, S.s03_rage, S.s04_mekone, S.s05_trial, S.s06_defence, S.s07_witnesses, S.s08_secret, S.s09_other_end, S.s10_storm, S.s11_legacy, S.s12_rebel, S.s13_coda):
    f()
mt, mv, used = S.speech_mask()
tg, gg = S.master_gain(S.N)
json.dump(REC, open('cuesheet.json', 'w'))
np.savez('scoremask.npz', mt=mt, mv=mv, tg=tg, gg=gg)
print(len(REC), 'calls; vo used', used)
