#!/bin/bash
# Oturum başı kancası: main'e birleşmemiş dalları bu oturumun bağlamına yazar.
# Neden: her oturum main'den başlar; başka dalda kalan iş yeni oturuma görünmez.
# Pano: kanal/DURUM.md. Yoksayılan dallar (kanalla ilgisiz): .claude/hooks/dal_yoksay.txt
set -uo pipefail
cd "${CLAUDE_PROJECT_DIR:-.}" 2>/dev/null || exit 0
git rev-parse --git-dir >/dev/null 2>&1 || exit 0

# Bulut oturumunda klon yalnız main'i ve oturum dalını getirir; öteki dallar
# dosya içeriği olmadan (blob:none) çekilir: ~1 sn, disk payını yemez.
# --depth değil --shallow-since: derinlik sınırı eski birleşmeleri kesip sayıyı şişiriyordu.
if [ "${CLAUDE_CODE_REMOTE:-}" = "true" ]; then
  timeout 60 git -c gc.auto=0 -c maintenance.auto=false fetch -q origin --shallow-since="60 days ago" --filter=blob:none \
    '+refs/heads/*:refs/remotes/origin/*' 2>/dev/null || true
fi

git rev-parse -q --verify origin/main >/dev/null || exit 0
yoksay=.claude/hooks/dal_yoksay.txt
esik=$(date -d '30 days ago' +%s 2>/dev/null || echo 0)
simdiki=$(git rev-parse --abbrev-ref HEAD 2>/dev/null)
liste=""

while IFS='|' read -r ref zaman tarih; do
  dal=${ref#origin/}
  case "$dal" in main|HEAD|origin) continue ;; esac
  [ -f "$yoksay" ] && grep -qxF "$dal" "$yoksay" && continue
  [ "$zaman" -lt "$esik" ] && continue
  n=$(git rev-list --count "origin/main..$ref" 2>/dev/null || echo 0)
  [ "$n" -eq 0 ] && continue
  konu=$(git log -1 --format=%s "$ref" | cut -c1-110)
  isaret=""; [ "$dal" = "$simdiki" ] && isaret=" (bu oturumun dalı)"
  liste+="- \`$dal\`$isaret: $n commit, son $tarih: $konu"$'\n'
done < <(git for-each-ref --sort=-committerdate \
  --format='%(refname:short)|%(committerdate:unix)|%(committerdate:short)' refs/remotes/origin/)

echo "## Dal durumu (oturum başı kancası)"
if [ -n "$liste" ]; then
  echo "main'de olmayan işler (son 30 gün; ayrıntı: git log origin/main..origin/DAL):"
  printf '%s' "$liste"
  echo "Kullanıcı bu işlerden birini sürdürmek isterse önce o dal okunur; bitmiş video dalı main'e birleştirilir."
else
  echo "Son 30 günde main'e birleşmemiş dal yok."
fi
echo "Videoların aşaması ve hangi dalda olduğu: kanal/DURUM.md (iş parçası bitince güncellenir)."
exit 0
