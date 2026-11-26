// Zaman Kuryesi işareti: kum saatinin içinden geçen soru işareti.
// Kanca üst haznede (geçmiş), nokta boğazdan düşmüş, alt haznede tabana oturmuş (bugün): "geçmişe gider, bir soruyla döner".
// Soru işareti kahramandır (koyu, kontrastlı); kum saati zeminin bir tonu olarak çerçevedir.
// Kanca ve nokta logo yazısının yazı tipi Fraunces 600'ün kendi "?" glifinden (OFL); işaretle yazı aynı elden.
// Ölçüler 800×800 kutuda. Soru ile cam arası en dar yerde 20 birim (ölçüldü). Levha köşesi merkezden 361 birim.
const ZK = {
  CAM: 'M 240 114 C 190 285 372 374 376 400 C 372 426 190 515 240 686 M 560 114 C 610 285 428 374 424 400 C 428 426 610 515 560 686',
  // Fraunces 600 "?" kancası (noktası çıkarıldı), x 33.5–500.5, y -730.5…-227.5; sap ucu x≈241
  SORU: 'M202-333.5L210.5-254Q213.5-240 220.8-233.8Q228-227.5 241-227.5Q253-227.5 259.8-233.5Q266.5-239.5 271-255L278.5-327.5Q281.5-344.5 288-352.8Q294.5-361 309-364.5L342-373.5Q426.5-396 463.5-440.8Q500.5-485.5 500.5-551.5Q500.5-637 441.8-683.8Q383-730.5 268-730.5Q201-730.5 147.8-706.8Q94.5-683 64-644.3Q33.5-605.5 33.5-559.5Q33.5-522 53.5-501.3Q73.5-480.5 107-480.5Q145-480.5 165.8-504Q186.5-527.5 186.5-569.5L186.5-609Q186.5-644.5 206.3-665.5Q226-686.5 263-686.5Q301-686.5 322.3-656.5Q343.5-626.5 343.5-569Q343.5-507.5 328-469.8Q312.5-432 269-411.5L238.5-398.5Q214-387.5 206-372.3Q198-357 202-333.5Z',
  SORU_YER: 'translate(293.96 458.42) scale(0.44)',
  // Fraunces 600 "?" noktası; alt levhanın üstüne oturur
  NOKTA: 'M239 11Q264.5 11 284.5-1.5Q304.5-14 316.3-34.8Q328-55.5 328-79.5Q328-105 316.3-125.3Q304.5-145.5 284.5-157.8Q264.5-170 239-170Q214.5-170 194.5-157.8Q174.5-145.5 162.5-125.3Q150.5-105 150.5-79.5Q150.5-55.5 162.5-34.8Q174.5-14 194.5-1.5Q214.5 11 239 11Z',
  NOKTA_YER: 'translate(294.73 677.16) scale(0.44)',
  KUTU: '202 82 396 636',    // işaretin kutusu, 10 birim payla (ölçülen: x 212–588, y 92–708)

  // cam: kum saati ve levhalar; soru: soru işareti ve noktası
  isaret(cam, soru, o = {}) {
    const camOp = o.camOpak != null ? ` opacity="${o.camOpak}"` : '';
    return `<g${camOp}><path d="${this.CAM}" fill="none" stroke="${cam}" stroke-width="26"/>` +
      `<rect x="212" y="92" width="376" height="26" rx="9" fill="${cam}"/>` +
      `<rect x="212" y="682" width="376" height="26" rx="9" fill="${cam}"/></g>` +
      `<path transform="${this.SORU_YER}" d="${this.SORU}" fill="${soru}"/>` +
      `<path transform="${this.NOKTA_YER}" d="${this.NOKTA}" fill="${soru}"/>`;
  },
  DUZEN: {
    altin:    { zemin: '#E2B04F', cam: '#9C6F22', soru: '#101B33' },  // avatar (ana)
    lacivert: { zemin: '#101B33', cam: '#46598A', soru: '#E2B04F' },  // koyu zemin: kapak, bitiş ekranı
    fildisi:  { zemin: '#F3EAD7', cam: '#B89A62', soru: '#101B33' },  // açık zemin, baskı
    tek_acik: { zemin: null, cam: '#F3EAD7', soru: '#F3EAD7', camOpak: .45 },  // tek renk, koyu zemin üstü
    tek_koyu: { zemin: null, cam: '#101B33', soru: '#101B33', camOpak: .4 },   // tek renk, açık zemin üstü
  },
  RENK: { altin: '#E2B04F', lacivert: '#101B33', fildisi: '#F3EAD7', koyu_altin: '#9C6F22', gece: '#46598A' },

  // olcek: daire içinde büyütme (avatar 1.06: levha köşesi merkezden 383 birimde, daire 400)
  svg(duzen, boy = 800, o = {}) {
    const d = this.DUZEN[duzen];
    const zemin = d.zemin && !o.zeminsiz ? (o.daire ? `<circle cx="400" cy="400" r="400" fill="${d.zemin}"/>` : `<rect width="800" height="800" fill="${d.zemin}"/>`) : '';
    const k = o.olcek || 1, g = k === 1 ? '' : ` transform="translate(400 400) scale(${k}) translate(-400 -400)"`;
    return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 800" width="${boy}" height="${boy}">${zemin}<g${g}>${this.isaret(d.cam, d.soru, { camOpak: d.camOpak, ...o })}</g></svg>`;
  },
};
if (typeof module !== 'undefined') module.exports = ZK;
