#!/usr/bin/env bash
# Audio QA report for a finished file: loudness, true peak, clipping, dead air.
# usage: qa_audio.sh <file>   (exit 1 if any check fails)
# QA_PAUSES=N allows N deliberate pauses (chapter cards) of up to 3.2 s each; anything longer, or more of them, fails.
set -uo pipefail
f=$1; fail=0
ln=$(ffmpeg -nostdin -hide_banner -i "$f" -af loudnorm=print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
I=$(echo "$ln" | python3 -I -c "import sys,json;print(json.load(sys.stdin)['input_i'])")
TP=$(echo "$ln" | python3 -I -c "import sys,json;print(json.load(sys.stdin)['input_tp'])")
echo "integrated loudness: $I LUFS (target -14 +/-1)"
echo "true peak:           $TP dBTP (must be <= -1.0)"
python3 -I -c "import sys;i,t=float('$I'),float('$TP');sys.exit(0 if -15<=i<=-13 and t<=-1.0 else 1)" || { echo "FAIL loudness/peak"; fail=1; }

sil=$(ffmpeg -nostdin -hide_banner -i "$f" -af silencedetect=noise=-45dB:d=1.5 -f null - 2>&1 | grep -o 'silence_duration: [0-9.]*' || true)
allow=${QA_PAUSES:-0}
n=$(echo -n "$sil" | grep -c . || true); long=$(echo "$sil" | awk '$2>3.2' | grep -c . || true)
if [[ -z "$sil" ]]; then echo "dead air: none over 1.5 s"
elif (( n <= allow && long == 0 )); then echo "dead air: only the $n deliberate chapter pauses (allowed $allow, each <= 3.2 s)"; echo "$sil" | sed 's/^/  /'
else echo "FAIL dead air (>1.5 s below -45 dB; $allow deliberate pauses allowed):"; echo "$sil" | sed 's/^/  /'; fail=1; fi

exit $fail
