// Zaman Kuryesi işareti: kum saati, kumu soru işareti çizer.
// Üst haznede soru işaretinin kancası, sap boğazdan geçer, düşen kum ince bir çizgi, noktası alttaki kum tepeciği.
// Bütün ölçüler 800×800 kutuda; işaretin kendisi x 208–592, y 144–656 arasında.
const ZK = {
  RENK: {
    altin:   '#E2B04F',  // avatar zemini
    lacivert:'#101B33',  // kum saati, koyu zemin
    kiremit: '#A63D26',  // kum (altın ve fildişi zeminde)
    fildisi: '#F3EAD7',  // kum saati (koyu zeminde), açık zemin
    kum:     '#E2B04F',  // kum (koyu zeminde)
  },
  CAM: 'M 266 182 C 266 302 384 350 390 400 C 384 450 266 498 266 618 M 534 182 C 534 302 416 350 410 400 C 416 450 534 498 534 618',
  SORU: 'M 338 262 C 338 222 366 196 400 196 C 436 196 462 222 462 256 C 462 290 440 304 420 318 C 406 328 400 340 400 356 L 400 372',
  TEPE: 'M 322 616 C 346 546 454 546 478 616 Z',
  // cam: kum saatinin rengi, kum: soru işaretiyle tepeciğin rengi
  isaret(cam, kum, o = {}) {
    const akis = o.akissiz ? '' :
      `<path d="M 400 428 V 552" stroke="${kum}" stroke-width="6" stroke-linecap="round" stroke-dasharray="1 14"/>`;
    return `<path d="${this.CAM}" fill="none" stroke="${cam}" stroke-width="22" stroke-linecap="round"/>` +
      `<rect x="208" y="144" width="384" height="40" rx="12" fill="${cam}"/>` +
      `<rect x="208" y="616" width="384" height="40" rx="12" fill="${cam}"/>` +
      `<path d="${this.SORU}" fill="none" stroke="${kum}" stroke-width="42" stroke-linecap="round" stroke-linejoin="round"/>` +
      akis + `<path d="${this.TEPE}" fill="${kum}"/>`;
  },
  // hazır renk düzenleri
  DUZEN: {
    altin:    { zemin: '#E2B04F', cam: '#101B33', kum: '#A63D26' },  // avatar (ana)
    lacivert: { zemin: '#101B33', cam: '#F3EAD7', kum: '#E2B04F' },  // koyu zemin, bitiş ekranı, kapak
    fildisi:  { zemin: '#F3EAD7', cam: '#101B33', kum: '#A63D26' },  // açık zemin, baskı
    tek_acik: { zemin: null,      cam: '#F3EAD7', kum: '#F3EAD7' },  // filigran, tek renk
    tek_koyu: { zemin: null,      cam: '#101B33', kum: '#101B33' },
  },
  svg(duzen, boy = 800, o = {}) {
    const d = this.DUZEN[duzen];
    const zemin = d.zemin && !o.zeminsiz ? (o.daire ? `<circle cx="400" cy="400" r="400" fill="${d.zemin}"/>` : `<rect width="800" height="800" fill="${d.zemin}"/>`) : '';
    // olcek: daire içinde işareti büyütür (avatar 1.14: levha köşeleri merkezden 365 birimde, daire 400)
    const k = o.olcek || 1, g = k === 1 ? '' : ` transform="translate(400 400) scale(${k}) translate(-400 -400)"`;
    return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 800" width="${boy}" height="${boy}">${zemin}<g${g}>${this.isaret(d.cam, d.kum, o)}</g></svg>`;
  },
};
if (typeof module !== 'undefined') module.exports = ZK;
