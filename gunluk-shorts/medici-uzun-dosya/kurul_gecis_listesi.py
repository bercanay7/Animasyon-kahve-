#!/usr/bin/env python3
"""Kurul kanıt paketi için geçiş listesi: P1 programındaki farklı geçiş türlerinden birer örnek + birkaç sert kesme → kurul_kanit.py --gecisler değeri.
  python3 kurul_gecis_listesi.py --part 1     # 'ad:sn,ad:sn,…' yazar
"""
import argparse
import compose

ap = argparse.ArgumentParser(); ap.add_argument("--part", type=int, default=1); ap.add_argument("--n", type=int, default=12)
a = ap.parse_args()
p = compose.Program(part=a.part)
seen, out, cuts = set(), [], []
for s in p.shots[1:]:
    tr = getattr(s, "tr", None)
    name = (tr if isinstance(tr, str) else (tr[0] if tr else None)) or "cut"
    t = round(float(s.t0) - float(getattr(p, "t_off", 0.0)), 2)
    if name == "cut":
        cuts.append(("kesme", t)); continue
    if name not in seen:
        seen.add(name); out.append((name, t))
# türler + en fazla 3 kesme, zamana göre
sel = sorted(out[: a.n - 3] + cuts[:: max(1, len(cuts) // 3)][:3], key=lambda x: x[1])
print(",".join(f"{n}_{i}:{t}" if n == "kesme" else f"{n}:{t}" for i, (n, t) in enumerate(sel)))
