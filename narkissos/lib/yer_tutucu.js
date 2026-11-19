// Animatik yer tutucusu: henüz çizilmemiş plan için set renginde basit vazo zemini (yavaş yaklaşır) + plan kartı (kimlik, ölçek, set, 'ne', eylemler).
// ORTAK DOSYA (başkan). Set dosyaları yer tutucuyu şöyle kaydeder:  plan('P035', yt('P035'), { over: ytYazi('P035') });
// Gerçek çizim gelince yt(...) ve ytYazi(...) yerine planın kendi çizimi ve yazısı konur.
// Eylem anlarında (planlar.json 'eylem') küçük bir kil halka çakar: animatikte "sözcüğe bağlı eylem" görünsün.
'use strict';
const YT_GORSEL = { P077: 'tempesta1606.jpg', P078: 'callot1646_resim_satir.jpg', P079: 'callot1646_satir.jpg', P080: 'ellis1898_satir.png', P085: 'freud1914_s1_ust.jpg' };
function ytBeyaz(id) { const p = PL(id); return /beyaz zemin/i.test(p.ne || '') || p.set === 'BELGE'; }
// zemin motifi (sahne koordinatı); t film zamanı
function ytZemin(ctx, id, t) {
  const p = PL(id), set = p.set, wz = ytBeyaz(id), ink = wz ? C.sepia : C.ink, fill = wz ? '#C9A27A' : PC.clayR;
  if (wz) whiteGround(ctx); else glaze(ctx, 960, 760, 1100, 'rgba(120,48,22,.45)');
  const sd = parseInt(id.slice(1), 10) || 1;
  if (set === 'HAVUZ') {
    const wy = 600; waterBody(ctx, c => c.rect(-400, wy, 2800, 900), wy, t, { a: .2, seed: sd, n: 30, depth: 420 });
    farBank(ctx, 700, 2400, wy, t, sd, { h: 40, grass: 8, fill: '#3A1B0D' }); ledge(ctx, 720, wy - 30, wy); shoreLine(ctx, 720, wy);
    for (const [x, s2, h] of [[1300, 5, 60], [1350, 8, 48]]) narcissus(ctx, x, wy - 30, 1.6, t, s2 + sd, { dir: -1, h });
  } else if (set === 'CAM') {
    ctx.save(); ctx.beginPath(); ctx.roundRect(760, 180, 400, 760, 56); ctx.fillStyle = '#0b0705'; ctx.fill(); ctx.lineWidth = 5; ctx.strokeStyle = '#B9653A'; ctx.stroke(); ctx.restore();
  } else if (set === 'ORMAN' || set === 'KEHANET') {
    groundBand(ctx, 820, -400, 2400, wz ? { edge: '#B89878', fill: '#DCCDB0' } : {});
    const n = set === 'ORMAN' ? 5 : 1;
    for (let i = 0; i < n; i++) vaseTree(ctx, 200 + i * 380 + (i % 2) * 90, 820, 1.6 + (i % 3) * .2, sd + i, t, { branches: 6, reach: 100, fill, ink });
    if (set === 'KEHANET') crag(ctx, [[-200, 830], [600, 700], [1100, 760], [1500, 830]], { fill: wz ? '#D6C3A2' : '#5A2C16', line: ink, seed: sd, wob: 6 });
  } else if (set === 'DAG') {
    crag(ctx, [[-300, 900], [300, 380], [760, 520], [1150, 300], [1700, 560], [2300, 900]], { fill: '#5A2C16', seed: sd, wob: 10, strata: 3 });
    ctx.save(); ctx.fillStyle = '#050302'; ctx.beginPath(); ctx.ellipse(1150, 780, 170, 120, 0, PI, TAU); ctx.fill(); ctx.restore();
  } else if (set === 'NEHIR' || set === 'DERE') {
    groundBand(ctx, 560); const wy = 640;
    waterBody(ctx, c => c.rect(-400, wy, 2800, 260), wy, t, { a: .3, seed: sd, n: 40, depth: 200, span: [-200 - (t * 40) % 400, 2400] });
    for (let i = 0; i < 8; i++) grass(ctx, 100 + i * 240, wy, 2, t, sd + i);
  } else if (set === 'DELFI') {
    for (let i = 0; i < 6; i++) column(ctx, 520 + i * 180, 300, 760, 70, C.ink, PC.clayR);
    ctx.save(); ctx.fillStyle = PC.clayR; ctx.fillRect(460, 250, 1000, 50); ctx.fillRect(460, 760, 1000, 40); ctx.restore();
  } else if (set === 'FRIZ' || set === 'YAZI' || set === 'YANKI' || set === 'SON') {
    meander(ctx, -400, 2400, 120, 40, PC.clayR, PC.glaze);
    if (set !== 'SON') meander(ctx, -400, 2400, 840, 40, PC.clayR, PC.glaze); else meander(ctx, -400, 2400, 980, 30, PC.clayR, PC.glaze);
    if (set === 'YANKI') dipinto(ctx, 'ΗΧΩ', 960, 520, 120, { col: C.red, a: .5 + .4 * Math.sin(t * 1.3), seed: sd });
  } else if (set === 'YERALTI') {
    ctx.fillStyle = '#030202'; ctx.fillRect(-3000, -3000, 9000, 9000);
    ctx.save(); ctx.strokeStyle = 'rgba(160,90,50,.35)'; ctx.lineWidth = 2;
    for (let k = 0; k < 14; k++) { const y = 420 + k * 40; ctx.beginPath(); for (let x = -200; x <= 2200; x += 40) ctx.lineTo(x, y + Math.sin(x * .01 + t * .8 + k) * 6); ctx.stroke(); }
    ctx.restore();
  } else if (set === 'BELGE') {
    const im = YT_GORSEL[id];
    if (im) belgeCiz(ctx, im, 960, 600, 1200, 480, { frame: true });
  }
}
// yer tutucu çizimi: yavaş yaklaşma (1,00 → 1,05) + eylem çakmaları
function yt(id) {
  return (ctx, st) => {
    const ev = (PL(id).eylem || []).map(e => A(e.at));
    // ölçeğe göre kadraj (animatikte ölçek değişimi görünsün): geniş uzak, ayrıntı çok yakın, ters açı baş aşağı
    const ol = PL(id).olcek, z = { 'geniş': .78, 'orta': 1.0, 'orta-yakın': 1.3, 'yakın': 1.6, 'ayrıntı': 2.3, 'ters açı': 1.2 }[ol] || 1;
    const fy = PL(id).set === 'HAVUZ' ? 600 : H / 2;
    baseT(ctx); ctx.save();
    if (ol === 'ters açı') { ctx.translate(0, H); ctx.scale(1, -1); }
    slowZoom(ctx, st, W / 2, fy, z, z * 1.05);
    ytZemin(ctx, id, st.t);
    ctx.restore();
    ev.forEach((te, k) => { const u = (st.t - te) / .8; if (u < 0 || u > 1) return; // eylem çakması
      const x = 300 + ((k * 397 + parseInt(id.slice(1), 10) * 131) % 1320), y = 520 + ((k * 173) % 200);
      ctx.save(); ctx.strokeStyle = `rgba(232,160,104,${(1 - u).toFixed(3)})`; ctx.lineWidth = 6 * (1 - u) + 1; ctx.beginPath(); ctx.ellipse(x, y, 30 + 160 * u, (30 + 160 * u) * .45, 0, 0, TAU); ctx.stroke(); ctx.restore(); });
  };
}
// yer tutucu yazısı (üst katman; notext'te görünmez): kimlik, ölçek, set, çapa, 'ne', eylem sırası ve planın yazı alanı
function ytYazi(id) {
  return (ctx, st) => {
    if (NOTEXT) return;
    const p = PL(id), wz = ytBeyaz(id), col = wz ? YAZI.sepya : YAZI.krem, pr = wz ? '236,226,206' : '8,4,2';
    txt(ctx, `${id} · ${(p.olcek || '').toLocaleUpperCase('tr')} · ${p.set} · ${p.at}`, 120, 120, { px: 40, align: 'left', col, font: FONT.baslik(40, 700), ls: 3, panel: .6, panelRGB: pr });
    ctx.save(); ctx.font = FONT.metin(38); ctx.fillStyle = col; ctx.textAlign = 'left'; ctx.textBaseline = 'middle'; ctx.globalAlpha = .92;
    let y = 196; for (const l of wrapLines(ctx, p.ne || '', 1660).slice(0, 5)) { ctx.fillText(l, 120, y); y += 46; }
    ctx.restore();
    // şimdiki ya da son eylem (2,4 sn görünür)
    const ev = (p.eylem || []).map(e => ({ t: A(e.at), ne: e.ne })).filter(e => st.t >= e.t && st.t < e.t + 2.4);
    if (ev.length) { const e = ev[ev.length - 1]; txt(ctx, '→ ' + e.ne, 960, 690, { px: 44, font: FONT.alinti(44), col, a: clamp((st.t - e.t) / .25) * clamp((e.t + 2.4 - st.t) / .3), panel: .7, panelRGB: pr }); }
    if (p.yazi) txt(ctx, 'yazı: ' + p.yazi.slice(0, 110), 120, 800, { px: 32, align: 'left', font: FONT.alinti(32), col, a: .75 });
  };
}
// kayıtsız kalan planlar için (set dosyalarından SONRA yüklenir: lib/eksik.js) — film her an baştan sona oynar
function ytEksikleriKaydet() {
  const done = new Set(SHOTS.map(s => s.id).filter(Boolean));
  for (const id of Object.keys(window.PLAN || {})) if (!done.has(id)) { console.log('yer tutucu (set dosyasında yok): ' + id); plan(id, yt(id), { over: ytYazi(id) }); }
}
