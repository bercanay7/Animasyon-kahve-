cd /tmp/claude-0/-home-user/c3662c9d-24be-574f-ac5d-de35ddf76b95/scratchpad/ses3
for s in stems tech intel intel2 lim sfx shorts post compare plots; do nice -n 19 python3 $s.py > $s.log 2>&1 || echo "FAIL $s"; done
echo ALLDONE
