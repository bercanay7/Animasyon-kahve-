// YAZI seti, SAHİP-1: P006. Bu dosyayı yalnız bu sahip değiştirir.
// Kurallar: lib/sahne/KILAVUZ.md. Yardımcılar S1 (s1/cam.js).
'use strict';
(() => {
  // ---- P006 · ayrıntı · A05 · LEVHA: dönen bir vazonun omzunda kırmızı figür yazı ΝΑΡΚΙΣΣΟΣ; 'kelimede' yazı ön yüze gelir, 'narsisizm'de harfler dönüp NARSİSİZM olur ----
  const GR = [...'ΝΑΡΚΙΣΣΟΣ'], TR = [...'NARSİSİZM'];
  const R = 1000, CX = 960, YT = 520, HT = 116;
  // harf yerleşimi yay uzunluğunda: her harf kendi genişliği + EŞİT boşluk (Fable tur 1: harf aralığı eşit). Döner: harf merkezlerinin yay konumu (ortalı)
  const yerlesim = (ws, gap) => { const tot = ws.reduce((a, w) => a + w, 0) + gap * (ws.length - 1); let x = -tot / 2; return ws.map(w => { const c = x + w / 2; x += w + gap; return c; }); };
  let GS = null, TS = null;
  const olc = ctx => {
    if (GS) return;
    const gw = GR.map(ch => ((DIP[ch] || DIP[' '])[0]) * HT);
    ctx.save(); ctx.font = FONT.baslik(HT * 1.12, 700); const tw = TR.map(ch => ctx.measureText(ch).width); ctx.restore();
    GS = yerlesim(gw, HT * .3); TS = yerlesim(tw, HT * .3);
  };
  // gerçek meander (filmin kendi birimi: lib/vazo/style.js meander) silindir üstünde: yatay çizgiler yatay kalır, x yay → ekran
  const meanderCyl = (ctx, phi, y, h, col) => {
    const u = h / 5, cell = h, a = y + u * 1.15, b = y + h - u * 1.15, X = sArc => CX + R * Math.sin(sArc / R + phi);
    const s0 = -R * (PI / 2 + phi) * 1.0, s1 = R * (PI / 2 - phi);
    ctx.save(); ctx.fillStyle = col; ctx.strokeStyle = col;
    // üst ve alt şerit
    for (const yy of [y, y + h - u * .55]) { ctx.beginPath(); ctx.rect(X(s0) , yy, X(s1) - X(s0), u * .55); ctx.fill(); }
    ctx.lineCap = 'butt'; ctx.lineJoin = 'miter';
    const k0 = Math.floor(s0 / cell), k1 = Math.ceil(s1 / cell);
    for (let k = k0; k <= k1; k++) {
      const sx = k * cell, th = sx / R + phi + cell * .4 / R, c = Math.cos(th); if (c < .06) continue;
      ctx.lineWidth = u * .62 * (.45 + .55 * c); ctx.globalAlpha = .35 + .65 * c;
      ctx.beginPath(); ctx.moveTo(X(sx), b); ctx.lineTo(X(sx), a); ctx.lineTo(X(sx + cell * .82), a); ctx.lineTo(X(sx + cell * .82), b);
      ctx.lineTo(X(sx + cell * .3), b); ctx.lineTo(X(sx + cell * .3), a + u * 1.3); ctx.lineTo(X(sx + cell * .55), a + u * 1.3); ctx.stroke();
    }
    ctx.restore();
  };
  // ---- P006 · ayrıntı · A05 · LEVHA: dönen bir vazonun omzunda kırmızı figür yazı ΝΑΡΚΙΣΣΟΣ; 'kelimede' yazı ön yüze gelir, harfler dönüp NARSİSİZM olur.
  //      Fable tur 1: dönüşüm 'narsisizm' sözcüğüne kadar biter ve plan sonuna dek ≥ 1,5 sn tam kalır (bitiş = min('narsisizm' − 0,05, plan sonu − 1,55)) ----
  plan('P006', (ctx, st) => {
    const t = st.t, tK = PE('P006', 0), tN = PE('P006', 1);
    olc(ctx);
    const tEnd = Math.min(tN - .05, st.end - 1.55), per = .07, dur = .42, tM0 = tEnd - (8 * per + dur);
    // dönüş: plan başında yazı sağ yanda, 'kelimede'den biraz önce ön yüzde; sonra çok yavaş sürüklenir (donuk değil)
    const tF = Math.min(tK, tM0 - .25);
    const phi = lerp(.75, 0, ramp(t, st.at, tF, E.out3)) - .03 * Math.max(0, t - tF);
    baseT(ctx);
    ctx.fillStyle = '#1B0F0A'; ctx.fillRect(0, 0, W, H);
    glow(ctx, 960, 540, 1100, 'rgba(110,52,26,.45)');
    camAt(ctx, 960, 540, lerp(1.0, 1.04, E.sine(st.p)));
    ctx.save();
    ctx.beginPath(); ctx.moveTo(-200, 1300); ctx.lineTo(-120, 330); ctx.quadraticCurveTo(200, 150, 700, 130); ctx.lineTo(700, -100); ctx.lineTo(1220, -100); ctx.lineTo(1220, 130); ctx.quadraticCurveTo(1720, 150, 2040, 330); ctx.lineTo(2120, 1300); ctx.closePath();
    const g = ctx.createLinearGradient(-120, 0, 2040, 0); g.addColorStop(0, '#050302'); g.addColorStop(.3, '#120B08'); g.addColorStop(.5, '#1A110C'); g.addColorStop(.7, '#120B08'); g.addColorStop(1, '#050302');
    ctx.fillStyle = g; ctx.fill(); ctx.clip();
    const cyl = th => [CX + R * Math.sin(th), Math.cos(th)];
    ctx.fillStyle = PC.clayR; ctx.fillRect(-300, 300, 2600, 6); ctx.fillRect(-300, 744, 2600, 6);
    // omuzdaki dil motifleri
    for (let k = -40; k <= 40; k++) { const th = k * .055 + phi; const [x, c] = cyl(th); if (c < .05) continue;
      ctx.save(); ctx.translate(x, 268); ctx.scale(c, 1); ctx.beginPath(); ctx.ellipse(0, 0, 21, 26, 0, PI, TAU); ctx.lineTo(21, 22); ctx.lineTo(-21, 22); ctx.closePath(); ctx.fillStyle = k % 2 ? C.red : PC.clayR; ctx.globalAlpha = .4 + .6 * c; ctx.fill(); ctx.restore(); }
    // alt bordür: gerçek meander (Fable tur 1: eski kesik kancalar "GGGG" okunuyordu)
    meanderCyl(ctx, phi, 768, 66, PC.clayR);
    // yazı: harf yerinde dikey ekseninde döner (sırayla), yarı yolda yeni harfe geçer; harf merkezi Yunan yerleşiminden Türkçe yerleşime kayar
    for (let i = 0; i < 9; i++) {
      const u = ramp(t, tM0 + i * per, tM0 + i * per + dur, E.io2), lat = u > .5;
      const sArc = lerp(GS[i], TS[i], E.io2(u)), th = sArc / R + phi, [x, c] = cyl(th); if (c < .04) continue;
      const flip = Math.abs(Math.cos(u * PI));
      ctx.save(); ctx.translate(x, YT - 10 * Math.sin(u * PI)); ctx.scale(c * Math.max(.04, flip), 1); ctx.globalAlpha = .3 + .7 * c;
      if (!lat) dipinto(ctx, GR[i], 0, 0, HT, { col: PC.clayRL, w: .12, seed: 3 + i });
      else { ctx.font = FONT.baslik(HT * 1.12, 700); ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillStyle = PC.clayRL; ctx.fillText(TR[i], 0, 6); }
      ctx.restore();
    }
    const sg = ctx.createLinearGradient(1150, 0, 1420, 0); sg.addColorStop(0, 'rgba(255,220,180,0)'); sg.addColorStop(.5, 'rgba(255,220,180,.07)'); sg.addColorStop(1, 'rgba(255,220,180,0)');
    ctx.fillStyle = sg; ctx.fillRect(1150, 0, 270, 1300);
    ctx.restore();
    ctx.save(); ctx.strokeStyle = 'rgba(201,112,63,.5)'; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(-120, 330); ctx.quadraticCurveTo(200, 150, 700, 130); ctx.moveTo(1220, 130); ctx.quadraticCurveTo(1720, 150, 2040, 330); ctx.stroke(); ctx.restore();
  }, { post: { tex: .45 } });
})();
