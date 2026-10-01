#!/bin/zsh
# P1S catalogue -> A1 catalogue, after merging upstream/main (the P1S edition) into this repo.
# Converts every 3mf still on the P1S, slices and fits the full plates under the print-time
# cap, slices both catalogues, checks every file against its P1S original, and rewrites the
# reports. Long (an hour or more): start it detached
# (nohup ./a1_all.sh > ../logs/a1_all_log.txt 2>&1 &!).
set -e
P="$(cd "$(dirname "$0")/../.." && pwd)"
PY=~/Library/Caches/makebot-build/venv/bin/python
cd "$P/Validation/tools"

echo "### converting to the A1"
$PY -u a1.py convert "$P"/Full\ Plates/*.3mf "$P"/Catalogue*.3mf
echo "### slicing full plates, trimming any over the print-time cap"
$PY -u a1.py fit "$P/Validation/data/a1_slices_devices.json" "$P"/Full\ Plates/*.3mf
echo "### slicing the catalogues"
for n in 1 2; do
  $PY -u report.py slice-catalogue "$P" $n
done
echo "### checking every file against its P1S original"
$PY -u a1.py check "$P" "$P/Validation/data/selfcheck.json"
echo "### writing reports"
$PY -u a1.py data "$P"
$PY -u a1.py previews "$P"
$PY -u report.py write "$P"
$PY -u readme.py "$P"
echo "### done"
