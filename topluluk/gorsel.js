// Topluluk gönderisi görselleri (1080×1080): film karesinden kare kırpım + yazı. node topluluk/gorsel.js
// Kaynak kareler topluluk/kaynak/*.jpg (filmlerin tools/kare.js'i, ekran yazısız). Fontlar narkissos/fonts.css (Bebas Neue, Cormorant).
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
const { serve } = require('../shorts-sart/tools/sunucu');
const G = [
  { ad: 'narkissos', cx: 760, satir: [['O BENİM.', '#E0643A', 210]], alt: 'Narkissos ve Eko · şimdi kanalda', konum: 'alt' },
  { ad: 'dorian', cx: 1060, satir: [['SEN DEĞİL,', '#F2E8D8', 150], ['TABLO YAŞLANSAYDI?', '#D9A441', 150]], alt: "Dorian Gray · Cumartesi 28 Kasım, 18:00", konum: 'alt' },
  { ad: 'gilgamis', cx: 900, satir: [['HER ŞEYİNİ KAYBETTİ.', '#FBEBD0', 128], ['NEDEN ÖVÜNDÜ?', '#E8622E', 150]], alt: 'Gılgamış · Çarşamba 2 Aralık, 18:00', konum: 'alt' },
  { ad: 'lale', cx: 960, satir: [['BİR SOĞANA', '#F2E8D8', 170], ['BEŞ EV.', '#C86AA8', 190]], alt: 'Lale Çılgınlığı · Perşembe 10 Aralık, 18:00', konum: 'alt' },
  { ad: 'frankenstein', cx: 900, satir: [['YÜZÜNÜ GÖREMEDİ.', '#F2E8D8', 150], ['SESİNE İNANDI.', '#E8B23A', 170]], alt: 'Frankenstein · Pazar 6 Aralık, 18:00', konum: 'ust' },
];
(async () => {
  const srv = await serve(), port = srv.address().port, br = await chromium.launch();
  const p = await br.newPage({ viewport: { width: 1080, height: 1080 } });
  await p.goto(`http://127.0.0.1:${port}/topluluk/bos.html`);
  for (const g of G) {
    const b64 = await p.evaluate(async g => {
      await document.fonts.load('400 100px "Bebas Neue"', 'ĞİŞÖÜÇ'); await document.fonts.load('italic 500 40px "Cormorant Garamond"', 'ĞİŞÖÜÇ');
      const im = new Image(); im.src = `/topluluk/kaynak/${g.ad}.jpg`; await im.decode();
      const c = document.createElement('canvas'); c.width = 1080; c.height = 1080; const x = c.getContext('2d');
      x.drawImage(im, Math.max(0, Math.min(1920 - 1080, g.cx - 540)), 0, 1080, 1080, 0, 0, 1080, 1080);
      const ust = g.konum === 'ust', H = g.satir.reduce((a, s) => a + s[2] * .92, 0) + 150;
      const gr = ust ? x.createLinearGradient(0, 0, 0, H + 120) : x.createLinearGradient(0, 1080 - H - 120, 0, 1080);
      const a = 'rgba(8,5,3,.82)', z = 'rgba(8,5,3,0)';
      if (ust) { gr.addColorStop(0, a); gr.addColorStop(.75, 'rgba(8,5,3,.55)'); gr.addColorStop(1, z); x.fillStyle = gr; x.fillRect(0, 0, 1080, H + 120); }
      else { gr.addColorStop(0, z); gr.addColorStop(.25, 'rgba(8,5,3,.55)'); gr.addColorStop(1, a); x.fillStyle = gr; x.fillRect(0, 1080 - H - 120, 1080, H + 120); }
      x.textAlign = 'center'; x.lineJoin = 'round';
      let y = ust ? 70 : 1080 - H + 10;
      for (const [s, col, px] of g.satir) { y += px * .92; x.font = `400 ${px}px "Bebas Neue"`; const sc = Math.min(1, 980 / x.measureText(s).width);
        x.save(); x.translate(540, y); x.scale(sc, sc); x.lineWidth = px * .12; x.strokeStyle = 'rgba(8,4,2,.9)'; x.strokeText(s, 0, 0); x.fillStyle = col; x.fillText(s, 0, 0); x.restore(); }
      x.font = 'italic 500 46px "Cormorant Garamond"'; x.fillStyle = '#F4E6C8'; x.fillText(g.alt, 540, y + 70);
      return c.toDataURL('image/jpeg', .92).split(',')[1];
    }, g);
    fs.writeFileSync(path.join(__dirname, `${g.ad}.jpg`), Buffer.from(b64, 'base64')); console.log('yazıldı', g.ad);
  }
  await br.close(); srv.close();
})();
