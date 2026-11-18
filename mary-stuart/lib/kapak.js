// Kapaklar (Mary Stuart): filmin motoruyla 16:9 tam kadraj (perde yok). kapak.html?v=A | B
// A: karar (Çatışma + hareket oku): gece denizi, teknede Mary (kırmızı astar), karşı kıyıda taçlı dev siluet; "RAKİBİNE SIĞINDI"
// B: son (ortadan başlamak, tek renk): filmin ilk karesindeki gravür, siyahın altından kırmızı; "İDAMINA KIRMIZI GİYDİ"
// Kurallar: Bebas Neue, büyük harf ≥ %18 (font ≥ 290 px), sağ alt rozet (x 1440–1874, y 829–1034) boş, tek odak, kan/balta/kütük yok.
'use strict';
const KQ = new URLSearchParams(location.search), KV = KQ.get('v') || 'A';
const KW = 1920, KH = 1080, kmk = () => { const c = document.createElement('canvas'); c.width = KW; c.height = KH; return c; };
const KT = kmk(), kt = KT.getContext('2d'), KR = kmk(), kr = KR.getContext('2d'), KM = kmk(), km = KM.getContext('2d');
function kapakCiz() {
  const cv = document.getElementById('c'), g = cv.getContext('2d');
  kt.fillStyle = '#000'; kt.fillRect(0, 0, KW, KH); kr.clearRect(0, 0, KW, KH);
  const st = { t: 3, lt: 3, p: .5, at: 0 }, G = BOYA.ctx(kt, kr, st);
  G.zemin = v => { kt.save(); kt.setTransform(1, 0, 0, 1, 0, 0); kt.fillStyle = G.gri(v); kt.fillRect(0, 0, KW, KH); kt.restore(); };
  let look = { sepia: .16, strength: .3 }, renkTon = 'brightness(2.4) contrast(1.25)';
  if (KV === 'B') {
    G.zemin(.07); const im = IMG.siyah, W = im.naturalWidth, H = im.naturalHeight, k = .96, ox = 1200 - .535 * W * k, oy = 600 - .53 * H * k;
    for (const c of [kt, kr]) c.setTransform(k, 0, 0, k, ox, oy);
    kt.save(); kt.beginPath(); kt.rect(.372 * W, .27 * H, (.765 - .372) * W, (.762 - .27) * H); kt.clip(); kt.drawImage(BOYA.griOn(im, 1.45, .93), 0, 0); kt.restore();
    const fade = kt.createLinearGradient(.372 * W, 0, .44 * W, 0); fade.addColorStop(0, 'rgba(18,18,18,1)'); fade.addColorStop(1, 'rgba(18,18,18,0)'); kt.fillStyle = fade; kt.fillRect(.36 * W, .25 * H, .09 * W, .52 * H);
    const P = G.pathOf(SIYAH_ETEK.map(([x, y]) => [x * W, y * H]), true, .45);
    kr.filter = 'blur(12px)'; kr.fillStyle = 'rgb(176,22,30)'; kr.fill(P); kr.filter = 'none'; kr.globalCompositeOperation = 'destination-in'; kr.drawImage(BOYA.koyuOn(im, .5), 0, 0);
    kr.globalCompositeOperation = 'destination-out'; kr.filter = 'blur(6px)'; for (const c of SIYAH_CIKAR) kr.fill(G.pathOf(c.map(([x, y]) => [x * W, y * H]), true, .5)); kr.filter = 'none'; kr.globalCompositeOperation = 'source-over'; G.renkVar = true;
    for (const c of [kt, kr]) c.setTransform(1, 0, 0, 1, 0, 0);
    const sp = kt.createRadialGradient(1220, 640, 120, 1220, 640, 900); sp.addColorStop(0, 'rgba(255,255,255,0)'); sp.addColorStop(1, 'rgba(0,0,0,.55)'); kt.fillStyle = sp; kt.fillRect(0, 0, KW, KH);
    look = { sepia: .14, strength: .16 }; renkTon = 'brightness(2.6) contrast(.95)';
  } else {
    // gece: gökte I. Elizabeth'in madalya profili (gerçek, 16. yy), altında İngiliz kıyısı; teknede elini uzatan Mary
    const ufuk = 690, gr = kt.createLinearGradient(0, 0, 0, ufuk); gr.addColorStop(0, G.gri(.08)); gr.addColorStop(1, G.gri(.36)); kt.fillStyle = gr; kt.fillRect(0, 0, KW, ufuk);
    const md = IMG.madalya; if (md) { const c = BOYA.griOn(md, 1.25, .9), mw = md.naturalWidth, mh = md.naturalHeight, R = 430, cx = 1440, cy = 330;
      const hl = kt.createRadialGradient(cx, cy, R * .7, cx, cy, R * 1.6); hl.addColorStop(0, G.gri(.75, .7)); hl.addColorStop(1, G.gri(.4, 0)); kt.fillStyle = hl; kt.fillRect(0, 0, KW, KH);
      kt.save(); kt.beginPath(); kt.arc(cx, cy, R, 0, Math.PI * 2); kt.clip(); const sc = (R * 2.15) / (mw * .62); kt.drawImage(c, cx - .52 * mw * sc, cy - .45 * mh * sc, mw * sc, mh * sc); kt.restore();
      const kn = kt.createLinearGradient(0, cy, 0, cy + R); kn.addColorStop(0, G.gri(.36, 0)); kn.addColorStop(1, G.gri(.36, .9)); kt.fillStyle = kn; kt.fillRect(cx - R, cy, R * 2, R + 10); }
    G.kiyi(900, 2100, ufuk + 4, 110, { seed: 7, v: .2, d0: .05, d1: .9, k: 3 });
    const sg = kt.createLinearGradient(0, ufuk - 60, 0, ufuk + 120); sg.addColorStop(0, G.gri(.5, 0)); sg.addColorStop(.5, G.gri(.55, .6)); sg.addColorStop(1, G.gri(.5, 0)); kt.fillStyle = sg; kt.fillRect(0, ufuk - 60, KW, 180);
    const dz = kt.createLinearGradient(0, ufuk, 0, KH); dz.addColorStop(0, G.gri(.34)); dz.addColorStop(1, G.gri(.08)); kt.fillStyle = dz; kt.fillRect(0, ufuk + 30, KW, KH);
    const q = G.rng(5); for (let i = 0; i < 60; i++) { const u = Math.pow(q(), 1.4), y = ufuk + 40 + u * 340, x = q() * KW, w = 40 + u * 260; kt.fillStyle = G.gri(q() < .5 ? .14 : .5, .7); kt.beginPath(); kt.ellipse(x, y, w, 2 + u * 5, 0, 0, Math.PI * 2); kt.fill(); }
    for (let k = 0; k < 26; k++) { const u = k / 26, y = ufuk + 40 + Math.pow(u, 1.3) * 260, x = lerp(1380, 900, u), w = lerp(150, 60, u) * (.6 + .4 * Math.sin(k * 1.7)); kt.fillStyle = G.gri(.9, .7 * (1 - u * .5)); kt.fillRect(x - w / 2, y, w, lerp(3, 7, u)); }
    G.tekne({ x: 720, y: 980, s: 880, f: 1, t: 1.2, oar: .3, sail: 0, direk: false, kisi: [{ kind: 'erkek', x: -.3, h: .26, poz: 'otur', kol: 'kurek', f: 1 },
      { kind: 'mary', x: .28, h: .64, kol: 'uzat', f: 1, kirmizi: 'etek', veil: .9, veilA: .7 }] });
    look = { sepia: .1, strength: .16 }; renkTon = 'contrast(.55) brightness(1.65)';
  }
  const RD = new SFR.Redraw(KW, KH), FP = new SFP.FilmPost(KW, KH);
  const src = RD.render(KT, { frame: 7, ...REDRAW0 });
  let mask = null; if (G.renkVar) { km.clearRect(0, 0, KW, KH); km.drawImage(KR, 0, 0); km.globalCompositeOperation = 'multiply'; km.filter = renkTon; km.drawImage(src, 0, 0); km.filter = 'none'; km.globalCompositeOperation = 'destination-in'; km.drawImage(KR, 0, 0); km.globalCompositeOperation = 'source-over'; mask = KM; }
  const dev = FP.render(src, { frame: 7, strength: look.strength, sepia: look.sepia, crank: 1, exposure: 1, halation: 1 }, mask);
  g.drawImage(dev, 0, 0);
  // yazı (Bebas Neue, temiz; hafif gölge)
  const yaz = (txt, x, y, px, renk, kontur) => { g.font = `400 ${px}px "Bebas Neue"`; g.textBaseline = 'alphabetic'; g.textAlign = 'left'; g.shadowColor = 'rgba(0,0,0,.85)'; g.shadowBlur = 30; g.shadowOffsetY = 6; g.fillStyle = renk; g.fillText(txt, x, y); g.shadowBlur = 0; g.shadowOffsetY = 0;
    if (kontur) { g.lineWidth = 5; g.strokeStyle = kontur; g.strokeText(txt, x, y); } };
  const AK = '#f2ebdc', KZ = 'rgb(206,34,40)';
  if (KV === 'B') { yaz('İDAMINA', 90, 330, 300, AK); yaz('KIRMIZI', 90, 620, 300, 'rgb(226,38,43)', 'rgba(242,235,220,.9)'); yaz('GİYDİ', 90, 910, 300, AK); }
  else { yaz('RAKİBİNE', 80, 300, 300, AK); yaz('SIĞINDI', 80, 580, 300, AK); }
  window.READY = true;
}
window.GORSEL = { siyah: 'kaynak/gorsel/mary_siyah_hacli_tamboy.jpg', madalya: 'kaynak/gorsel/elizabeth_madalya_16yy.jpg' };
const SIYAH_ETEK = [[.405, .51], [.45, .525], [.5, .545], [.55, .525], [.585, .51], [.574, .57], [.565, .63], [.63, .642], [.655, .69], [.672, .758], [.5, .762], [.36, .758], [.372, .69], [.385, .62], [.395, .56]];
const SIYAH_CIKAR = [[[.535, .565], [.645, .56], [.655, .655], [.535, .66]]];
(async () => { await document.fonts.load('400 300px "Bebas Neue"', 'RAKİBNESIĞDMZYGabc'); await document.fonts.ready; if (!document.fonts.check('400 300px "Bebas Neue"', 'RAKİBİNE')) console.log('HATA Bebas yüklenmedi'); await document.fonts.load('600 40px Cinzel'); await Promise.all(Object.entries(GORSEL).map(([k, v]) => loadImg(k, v))); kapakCiz(); })();
