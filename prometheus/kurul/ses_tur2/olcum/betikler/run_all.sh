set -x
cd /tmp/claude-0/-home-user/c3662c9d-24be-574f-ac5d-de35ddf76b95/scratchpad/ses2
nice -n 19 python3 stems.py > stems.log 2>&1
nice -n 19 python3 tech.py > tech.log 2>&1
nice -n 19 python3 intel.py > intel.log 2>&1
nice -n 19 python3 intel2.py > intel2.log 2>&1
nice -n 19 python3 lim.py > lim.log 2>&1
nice -n 19 python3 voc.py > voc.log 2>&1
nice -n 19 python3 edges.py > edges.log 2>&1
nice -n 19 python3 edges2.py > edges2.log 2>&1
nice -n 19 python3 sfx.py > sfx.log 2>&1
nice -n 19 python3 shorts.py > shorts.log 2>&1
nice -n 19 python3 plots.py > plots.log 2>&1
echo ALLDONE
