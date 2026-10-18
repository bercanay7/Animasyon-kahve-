#!/usr/bin/env python3
"""Yayın Paneli (tek sayfa, kopyala düğmeli) üretici → yayin/yayin_paneli.html

  python3 yayin/panel_kur.py            # YAYIN_PAKETI.md + bolumler.txt + kapaklar + (varsa) out/ videolarından üretir
  python3 yayin/panel_kur.py --stats '{"sure":"21:26","boyut":"1,4 GB"}'   # el ile istatistik

Tek doğruluk kaynağı: YAYIN_PAKETI.md (başlık/açıklama/yorum/etiket), bolumler.txt. Kimlik bilgisi/bağlantı yazılmaz.
Çıktıyı Artifact olarak yayınlamak için dosya yolu: yayin/yayin_paneli.html"""
import argparse
import base64
import datetime
import io
import json
import os
import re
import subprocess

import cv2

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def read(p):
    return open(os.path.join(HERE, p), encoding="utf-8").read()


def parse_md():
    md = read("YAYIN_PAKETI.md")
    blocks = re.findall(r"```\n(.*?)\n```", md, re.S)
    desc, comment = blocks[0], blocks[1]
    chapters = read("bolumler.txt").strip()
    desc = re.sub(r"\(yayin/bolumler\.txt[^)]*\)", chapters, desc)
    m = re.search(r"\*\*Önerilen:\*\* `(.+?)` \((\d+)\)", md)
    titles = [{"t": m.group(1), "n": int(m.group(2)), "rec": True}]
    alt = re.search(r"Alternatifler[^:]*:\s*(.+)", md).group(1)
    for t, n in re.findall(r"`([^`]+)` \((\d+)\)", alt):
        titles.append({"t": t, "n": int(n), "rec": False})
    tags = re.search(r"## 5\. Etiketler.*?\n\n`(.+?)`", md, re.S).group(1)
    return titles, desc, comment, tags, chapters


def thumb_uri(name, w=720):
    p = os.path.join(HERE, name)
    if not os.path.exists(p):
        return ""
    im = cv2.imread(p)
    h = int(im.shape[0] * w / im.shape[1])
    im = cv2.resize(im, (w, h), interpolation=cv2.INTER_AREA)
    ok, buf = cv2.imencode(".jpg", im, [cv2.IMWRITE_JPEG_QUALITY, 82])
    return "data:image/jpeg;base64," + base64.b64encode(buf.tobytes()).decode()


def probe_stats():
    st = {}
    vid = os.path.join(ROOT, "out", "sarlken_uzun.mp4")
    if os.path.exists(vid):
        d = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", vid]).decode().strip())
        st["sure"] = f"{int(d // 60)}:{int(d % 60):02d}"
        st["boyut"] = f"{os.path.getsize(vid) / 1e9:.2f} GB".replace(".", ",")
    return st


CHECK = [
    ("kulak", "Kulak kontrolü: dört kısa ses kesitini dinle (giriş, Worms, Akdeniz fırtınası, kapanış). Telaffuz ya da müzik hoşuna gitmeyen yer olursa tek cümle yamalanır."),
    ("yukle", "Studio → Video yükle: sarlken_uzun.mp4"),
    ("baslik", "Başlık: önerilen başlığı yapıştır (aşağıdaki Kopyala düğmesi)."),
    ("aciklama", "Açıklama: bölüm zaman damgalarıyla birlikte yapıştır. İlk satır 0:00 olmalı; bölümler otomatik oluşur."),
    ("kapak", "Küçük resim: kapak_A.jpg yükle (B ve C yedek; Test ve Karşılaştır ile üçünü de sınayabilirsin)."),
    ("dil", "Dil: Türkçe · Kategori: Eğitim."),
    ("altyazi", "Altyazı: Altyazılar → Dosya yükle → zamanlamalı → sarlken_tr.srt"),
    ("sentetik", "Değiştirilmiş veya sentetik içerik: Evet (anlatıcı yapay ses)."),
    ("cocuk", "Çocuklara özel değil · yaş sınırı yok."),
    ("liste", "Oynatma listesi: Uzun Dosya (yoksa oluştur)."),
    ("bitis", "Bitiş ekranı (son 7 sn): sol kare son/önerilen video, sağ kare Abone ol. Videodaki iki altın çerçeve bu yuvalara denk gelir."),
    ("zaman", "Zamanla: Pazar 25 Ekim 2026, 20:00 (+03). Konusu olan olayın (25 Ekim 1555, Brüksel) 471. yıldönümü."),
    ("yorum", "Yayından hemen sonra: sabit yorumu yapıştır ve sabitle."),
    ("kisa", "Kısa fragmanı ayrı yükle (aynı gün ya da ertesi sabah), tam videoya bağla."),
    ("olcum", "24. saat, 72. saat ve 7. gün Studio ekran görüntüsünü gönder; Windsor'a YouTube bağlanırsa kendim çekerim."),
]

NOTES = [
    "Kaynak kapısı şartlı geçti. Kritik hata (Aragonlu Catherine imparatorun teyzesi) ve 26 cümlelik hedge/olgu düzeltmesi uygulandı ve yeniden seslendirildi. Kalan HAFIZA maddeleri kaynaklar.md §7'de; yayından önce sayfa düzeyinde teyit önerilir.",
    "Kulak denetimi yapılmadı. Özel adların telaffuzu (Şarlken, Yörg, Halkulvadi, Tenoçtitlan, Komünero) yalnız otomatik çözümlemeyle kontrol edildi. Müzik ve ses efektleri sentezdir; yalnız sayısal olarak ölçüldü.",
    "Ses lisansı: ElevenLabs'te ticari kullanım ücretli plan ve Voice Library sesinin lisans koşullarına bağlıdır. Gelir paylaşımından önce hesap planını ve ses sahibinin koşullarını kontrol et.",
    "Madalyalar ve figürler stilize çizimdir; fotoğraf ya da gerçekçi yüz taklidi değildir. Haritalardaki sınırlar yaklaşıktır ve ekranda böyle yazar. Rivayetler, sonradan eklenenler ve tartışmalı yerler ekranda damgayla işaretlidir.",
]

TEMPLATE = r"""<title>Şarlken Yayın Paneli</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700&family=IBM+Plex+Mono:wght@400;500&family=Spectral:ital,wght@0,400;0,500;0,600;1,400&display=swap">
<style>
/* Düzen: dar tek sütun; her iş bir "levha" (altın kıl çizgili panel). Zaman Kuryesi videolarının kahve-altın dili. */
:root{
  --bg:#F2E9D8; --panel:#FBF5E8; --ink:#2B1E12; --muted:#6E5B45; --line:#D8C8AA; --gold:#86601C; --gold-hi:#A9781F;
  --accent:#8C2B1E; --ok:#2E6A49; --chip:#EADCC0; --btn-ink:#FBF5E8;
  --f-display:"Cinzel","Trajan Pro",Georgia,serif; --f-body:"Spectral",Georgia,"Times New Roman",serif; --f-mono:"IBM Plex Mono",ui-monospace,Menlo,Consolas,monospace;
}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){
  --bg:#110A06; --panel:#1B110A; --ink:#EDE1C8; --muted:#A8977D; --line:#3B2A1A; --gold:#D6B261; --gold-hi:#F0D27A;
  --accent:#E8503F; --ok:#78C896; --chip:#2A1B10; --btn-ink:#1B110A; color-scheme:dark}}
:root[data-theme="dark"]{
  --bg:#110A06; --panel:#1B110A; --ink:#EDE1C8; --muted:#A8977D; --line:#3B2A1A; --gold:#D6B261; --gold-hi:#F0D27A;
  --accent:#E8503F; --ok:#78C896; --chip:#2A1B10; --btn-ink:#1B110A; color-scheme:dark}
*{box-sizing:border-box}
body{background:var(--bg);color:var(--ink);font:17px/1.55 var(--f-body);padding-block:28px 64px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
main{max-width:760px;margin:0 auto;display:flex;flex-direction:column;gap:22px}
h1,h2{font-family:var(--f-display);font-weight:700;letter-spacing:.06em;text-wrap:balance;margin:0}
h1{font-size:clamp(28px,7vw,44px);line-height:1.1;color:var(--gold-hi)}
h2{font-size:15px;text-transform:uppercase;color:var(--gold);letter-spacing:.14em}
p{margin:0}
.eyebrow{font:500 12px/1 var(--f-mono);letter-spacing:.16em;text-transform:uppercase;color:var(--muted)}
.hero{display:flex;flex-direction:column;gap:12px;padding-bottom:6px}
.hero p{color:var(--muted);max-width:60ch}
.facts{display:flex;flex-wrap:wrap;gap:8px 22px;font:500 13px/1.3 var(--f-mono);color:var(--muted);margin-top:4px}
.facts b{color:var(--ink);font-weight:500}
.plate{background:var(--panel);border:1px solid var(--line);border-radius:6px;padding:18px 18px 20px;display:flex;flex-direction:column;gap:14px;min-width:0}
.plate>header{display:flex;align-items:baseline;justify-content:space-between;gap:12px;flex-wrap:wrap}
.count{font:500 13px/1 var(--f-mono);color:var(--gold)}
.row{display:flex;gap:10px;align-items:flex-start;justify-content:space-between;border-top:1px solid var(--line);padding-top:12px;min-width:0}
.row:first-of-type{border-top:0;padding-top:0}
.row .txt{min-width:0;flex:1;overflow-wrap:anywhere}
.row .meta{font:500 12px/1.4 var(--f-mono);color:var(--muted);margin-top:2px}
.rec{color:var(--ok)}
button{font:600 13px/1 var(--f-mono);letter-spacing:.04em;background:var(--gold);color:var(--btn-ink);border:0;border-radius:4px;padding:10px 14px;cursor:pointer;flex:none}
button:hover{background:var(--gold-hi)}
button.ghost{background:transparent;color:var(--gold);border:1px solid var(--gold)}
button:focus-visible,input:focus-visible,summary:focus-visible{outline:2px solid var(--gold-hi);outline-offset:2px}
pre{margin:0;white-space:pre-wrap;overflow-wrap:anywhere;font:400 14px/1.6 var(--f-mono);background:var(--bg);border:1px solid var(--line);border-radius:4px;padding:14px;max-height:360px;overflow:auto}
.tags{display:flex;flex-wrap:wrap;gap:6px}
.tags span{font:400 12.5px/1 var(--f-mono);background:var(--chip);border:1px solid var(--line);border-radius:3px;padding:6px 8px}
.thumbs{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:12px}
.thumbs figure{margin:0;display:flex;flex-direction:column;gap:6px;min-width:0}
.thumbs img{width:100%;aspect-ratio:16/9;object-fit:cover;border:1px solid var(--line);border-radius:3px;display:block}
.thumbs figcaption{font:500 12px/1.4 var(--f-mono);color:var(--muted)}
ol.check{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:2px;counter-reset:s}
ol.check li{display:flex;gap:12px;align-items:flex-start;padding:9px 0;border-top:1px solid var(--line)}
ol.check li:first-child{border-top:0}
ol.check input{width:20px;height:20px;margin:3px 0 0;accent-color:var(--gold);flex:none}
ol.check label{min-width:0;overflow-wrap:anywhere;cursor:pointer}
ol.check li.done label{color:var(--muted);text-decoration:line-through;text-decoration-color:var(--line)}
.prog{font:500 13px/1 var(--f-mono);color:var(--gold)}
ul.notes{margin:0;padding-left:1.1em;display:flex;flex-direction:column;gap:9px}
ul.notes li::marker{color:var(--gold)}
table{border-collapse:collapse;width:100%;font:400 13px/1.4 var(--f-mono)}
td,th{text-align:left;padding:8px 10px 8px 0;border-top:1px solid var(--line);vertical-align:top;overflow-wrap:anywhere}
th{color:var(--muted);font-weight:500;border-top:0}
.wrap{overflow-x:auto}
.toast{position:fixed;left:50%;bottom:calc(18px + env(safe-area-inset-bottom,0px));transform:translate(-50%,20px);background:var(--ink);color:var(--bg);font:500 13px/1 var(--f-mono);padding:10px 16px;border-radius:4px;opacity:0;pointer-events:none;transition:opacity .2s,transform .2s;z-index:20}
.toast.on{opacity:1;transform:translate(-50%,0)}
.when{display:flex;gap:14px;align-items:baseline;flex-wrap:wrap}
.when strong{font:700 clamp(22px,5vw,30px)/1 var(--f-display);color:var(--gold-hi);letter-spacing:.04em}
@media (prefers-reduced-motion:reduce){.toast{transition:none}}
</style>

<main>
  <section class="hero">
    <div class="eyebrow">Zaman Kuryesi · Uzun Dosya 1</div>
    <h1>Şarlken: Dünyayı Teslim Eden İmparator</h1>
    <p>Video, altyazı, küçük resimler ve Kısa hazır. Sende yalnızca Studio'da yükleme ve zamanlama kaldı. Metinleri aşağıdan tek dokunuşla kopyala, adımları işaretleyerek ilerle.</p>
    <div class="facts">{{FACTS}}</div>
  </section>

  <section class="plate" aria-labelledby="h-when">
    <header><h2 id="h-when">Yayın saati</h2><span class="count">25 Ekim 1555 → 25 Ekim 2026 · 471. yıl</span></header>
    <div class="when"><strong>Pazar 25 Ekim 2026 · 20:00</strong><span id="left" class="count"></span></div>
    <p>Konusu olan feragatin yıldönümü, ayrıca planlı Pazar 20:00 slotu. Studio'da "Zamanla" ile bu saate kur; saat dilimi İstanbul (+03).</p>
  </section>

  <section class="plate" aria-labelledby="h-steps">
    <header><h2 id="h-steps">Studio adımları</h2><span class="prog" id="prog"></span></header>
    <ol class="check" id="check"></ol>
  </section>

  <section class="plate" aria-labelledby="h-title">
    <header><h2 id="h-title">Başlık</h2><span class="count">60 karakter sınırı</span></header>
    <div id="titles"></div>
  </section>

  <section class="plate" aria-labelledby="h-thumb">
    <header><h2 id="h-thumb">Küçük resim</h2><span class="count">1280×720 · 2 MB altı</span></header>
    <div class="thumbs">{{THUMBS}}</div>
    <p class="meta">A önerilir: kapak_A.jpg. Studio'da Test ve Karşılaştır ile üçünü birlikte sınayabilirsin.</p>
  </section>

  <section class="plate" aria-labelledby="h-desc">
    <header><h2 id="h-desc">Açıklama</h2><button type="button" data-copy="desc">Kopyala</button></header>
    <pre id="desc"></pre>
  </section>

  <section class="plate" aria-labelledby="h-com">
    <header><h2 id="h-com">Sabit yorum</h2><button type="button" data-copy="comment">Kopyala</button></header>
    <pre id="comment"></pre>
  </section>

  <section class="plate" aria-labelledby="h-tags">
    <header><h2 id="h-tags">Etiketler</h2><button type="button" data-copy="tags">Hepsini kopyala</button></header>
    <div class="tags" id="tagbox"></div>
  </section>

  <section class="plate" aria-labelledby="h-short">
    <header><h2 id="h-short">Kısa fragman</h2><button type="button" data-copy="short">Açıklamayı kopyala</button></header>
    <div class="row"><div class="txt"><b>Kimse Onu Tahttan İndirmedi: Şarlken</b><div class="meta">sarlken_kisa_fragman.mp4 · 9:16 · yakılmış altyazı · #Shorts</div></div><button type="button" class="ghost" data-copy="shorttitle">Başlığı kopyala</button></div>
    <pre id="short"></pre>
  </section>

  <section class="plate" aria-labelledby="h-files">
    <header><h2 id="h-files">Dosyalar</h2></header>
    <div class="wrap"><table>
      <tr><th>Dosya</th><th>Ne</th></tr>
      {{FILES}}
    </table></div>
  </section>

  <section class="plate" aria-labelledby="h-notes">
    <header><h2 id="h-notes">Bilmen gerekenler</h2></header>
    <ul class="notes" id="notes"></ul>
  </section>
</main>
<div class="toast" id="toast" role="status" aria-live="polite">Kopyalandı</div>

<script>
const DATA = {{DATA}};
const $ = (s) => document.querySelector(s);
const toast = (m) => { const t = $("#toast"); t.textContent = m; t.classList.add("on"); clearTimeout(toast.h); toast.h = setTimeout(() => t.classList.remove("on"), 1400); };
async function copyText(txt) {
  try { await navigator.clipboard.writeText(txt); toast("Kopyalandı"); return; } catch (e) {}
  const ta = document.createElement("textarea"); ta.value = txt; ta.style.position = "fixed"; ta.style.opacity = "0"; document.body.appendChild(ta); ta.select();
  try { document.execCommand("copy"); toast("Kopyalandı"); } catch (e) { toast("Kopyalanamadı, metni seçip kopyala"); }
  ta.remove();
}
// başlıklar
$("#titles").innerHTML = DATA.titles.map((t, i) => `<div class="row"><div class="txt"><b>${t.t}</b><div class="meta">${t.n} karakter${t.rec ? ' · <span class="rec">önerilen</span>' : ''}</div></div><button type="button" class="${t.rec ? '' : 'ghost'}" data-title="${i}">Kopyala</button></div>`).join("");
$("#desc").textContent = DATA.desc;
$("#comment").textContent = DATA.comment;
$("#short").textContent = DATA.short;
$("#tagbox").innerHTML = DATA.tags.split(",").map((s) => `<span>${s.trim()}</span>`).join("");
$("#notes").innerHTML = DATA.notes.map((n) => `<li>${n}</li>`).join("");
const store = { get() { try { return JSON.parse(localStorage.getItem("sarlken-panel-v1") || "{}"); } catch (e) { return {}; } }, set(v) { try { localStorage.setItem("sarlken-panel-v1", JSON.stringify(v)); } catch (e) {} } };
let state = store.get();
function renderChecks() {
  $("#check").innerHTML = DATA.check.map(([id, text]) => `<li class="${state[id] ? 'done' : ''}"><input type="checkbox" id="c-${id}" ${state[id] ? 'checked' : ''}><label for="c-${id}">${text}</label></li>`).join("");
  const n = DATA.check.filter(([id]) => state[id]).length;
  $("#prog").textContent = `${n} / ${DATA.check.length}`;
}
$("#check").addEventListener("change", (e) => { const id = e.target.id.slice(2); state[id] = e.target.checked; store.set(state); renderChecks(); });
renderChecks();
document.addEventListener("click", (e) => {
  const b = e.target.closest("button"); if (!b) return;
  if (b.dataset.copy) copyText({ desc: DATA.desc, comment: DATA.comment, tags: DATA.tags, short: DATA.short, shorttitle: "Kimse Onu Tahttan İndirmedi: Şarlken" }[b.dataset.copy]);
  if (b.dataset.title !== undefined) copyText(DATA.titles[+b.dataset.title].t);
});
// geri sayım
function tick() {
  const ms = new Date("2026-10-25T20:00:00+03:00") - new Date();
  if (ms <= 0) { $("#left").textContent = "yayın saati geldi"; return; }
  const d = Math.floor(ms / 864e5), h = Math.floor(ms % 864e5 / 36e5), m = Math.floor(ms % 36e5 / 6e4);
  $("#left").textContent = `${d} gün ${h} sa ${m} dk kaldı`;
}
tick(); setInterval(tick, 30000);
</script>
"""


def build(stats):
    titles, desc, comment, tags, chapters = parse_md()
    short = ("Tam video: Zaman Kuryesi — Şarlken: Dünyayı Teslim Eden İmparator\n\n"
             "25 Ekim 1555, Brüksel. Elli beş yaşında bir adam, Avrupa'nın ve Yeni Dünya'nın büyük bölümünü bırakıyor. Kimse onu tahttan indirmedi. Peki neden?\n\n#Shorts #Şarlken #TarihBelgeseli")
    facts = []
    if stats.get("sure"):
        facts.append(f"<span>süre <b>{stats['sure']}</b></span>")
    facts += ["<span>1920×1080 · 24 k/sn</span>", "<span>ses <b>−14 LUFS</b></span>", "<span><b>14</b> bölüm</span>"]
    if stats.get("boyut"):
        facts.append(f"<span>dosya <b>{stats['boyut']}</b></span>")
    thumbs = ""
    for k, nm in (("A", "kapak_A.jpg"), ("B", "kapak_B.jpg"), ("C", "kapak_C.jpg")):
        uri = thumb_uri(nm)
        if uri:
            thumbs += f'<figure><img src="{uri}" alt="Küçük resim {k}"><figcaption>{k}{" · önerilen" if k == "A" else ""} · {nm}</figcaption></figure>'
    files = [
        ("sarlken_uzun.mp4", "ana video, 1920×1080, 24 kare/sn"),
        ("sarlken_tr.srt", "Türkçe altyazı (zamanlamalı dosya)"),
        ("kapak_A / B / C.jpg", "küçük resim adayları"),
        ("sarlken_kisa_fragman.mp4", "dikey Kısa fragman"),
        ("bolumler.txt", "bölüm zaman damgaları (açıklamada hazır)"),
        ("kulak_kontrol/*.mp3", "dört kısa ses kesiti (giriş, Worms, Akdeniz fırtınası, kapanış)"),
    ]
    frows = "\n".join(f"<tr><td>{a}</td><td>{b}</td></tr>" for a, b in files)
    data = {"titles": titles, "desc": desc, "comment": comment, "tags": tags, "short": short, "check": CHECK, "notes": NOTES}
    html = (TEMPLATE.replace("{{FACTS}}", "".join(facts)).replace("{{THUMBS}}", thumbs).replace("{{FILES}}", frows)
            .replace("{{DATA}}", json.dumps(data, ensure_ascii=False)))
    out = os.path.join(HERE, "yayin_paneli.html")
    open(out, "w", encoding="utf-8").write(html)
    open(os.path.join(HERE, "aciklama_hazir.txt"), "w", encoding="utf-8").write(desc + "\n")
    print(out, f"{len(html) / 1e3:.0f} KB")
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--stats", default=None)
    a = ap.parse_args()
    st = probe_stats()
    if a.stats:
        st.update(json.loads(a.stats))
    build(st)
