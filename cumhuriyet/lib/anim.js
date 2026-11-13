// Animatör araçları: anahtar pozlar, hazırlık (anticipation), yerine oturma (settle), gecikme (overlap),
// doğal göz kırpma ve duruşlarda canlılık. Sahneler poz parametrelerini bu araçlarla zamana bağlar.
'use strict';
// keys: [[t, {param: değer}, ease?], ...]. Her parametre yalnızca kendi geçtiği anahtarlar arasında geçiş yapar;
// ease, o anahtara VARIŞ eğrisidir (varsayılan E.io2). Örn. keyed(t, [[t0, {shN: .3}], [t1, {shN: 2.4}, E.outBack]])
function keyed(t, keys) {
  const out = {}, names = new Set();
  for (const k of keys) for (const n in k[1]) names.add(n);
  for (const n of names) {
    let prev = null, next = null;
    for (const k of keys) { if (!(n in k[1])) continue; if (k[0] <= t) prev = k; else { next = k; break; } }
    if (!prev) out[n] = next[1][n];
    else if (!next) out[n] = prev[1][n];
    else { const e = next[2] || E.io2; out[n] = lerp(prev[1][n], next[1][n], e(clamp((t - prev[0]) / (next[0] - prev[0])))); }
  }
  return out;
}
// ani duruştan sonra sönümlü salınım (sarkma / takip hareketi)
function settle(t, t0, amp = 1, freq = 2.6, decay = 5) { const u = t - t0; return u <= 0 ? 0 : amp * Math.exp(-decay * u) * Math.sin(TAU * freq * u); }
// hazırlık: ana hareketten önce ters yöne küçük kaçış; 0→-a→1 eğrisi
function anticip(t, t0, t1, a = .18) {
  const u = clamp((t - t0) / (t1 - t0));
  return u < .3 ? -a * E.io2(u / .3) : lerp(-a, 1, E.out3((u - .3) / .7));
}
// doğal göz kırpma: rastgele aralıklarla (2.2–5.5 sn) 0.14 sn'lik kapanış; seed figüre özgü
function blinkAt(t, seed = 0) {
  const per = 3.6, k0 = Math.floor(t / per);
  for (let k = k0 - 1; k <= k0 + 1; k++) {
    const tb = k * per + hash(k * 7.31 + seed * 13.7) * per * .8;
    const u = (t - tb) / .14;
    if (u >= 0 && u <= 1) return Math.sin(u * PI);
  }
  return 0;
}
// duruşta canlılık: düşük frekanslı küçük gövde/baş oynaması ve nefes
function idleOffsets(t, seed = 0, amt = 1) {
  return { torso: noise1(t * .35, seed) * .018 * amt, neck: noise1(t * .45, seed + 3) * .03 * amt, head: noise1(t * .55, seed + 7) * .045 * amt, breath: Math.sin(t * 1.55 + seed) * .7 * amt };
}
window.FIG_T = 0;
