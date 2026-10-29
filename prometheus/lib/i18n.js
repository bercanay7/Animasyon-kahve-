// Ekran yazıları: bu filmde yalnız Türkçe (İngilizce dublaj yok). txt() ve chapterCard() L() üzerinden geçer.
'use strict';
const LANG = 'tr';
if (typeof document !== 'undefined') document.documentElement.lang = LANG;
const L = s => s;
const LA = a => a;
const WdL = (id, w) => Wd(id, w);
