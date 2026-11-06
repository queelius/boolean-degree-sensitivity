#!/usr/bin/env bash
# core -> certify -> independent verify, for one context index (raw rows).
set -u
i=$1
D=/home/spinoza/github/math-theory/.research/attempts/014-context-pricing
cd /home/spinoza/github/math-theory
uv run --extra search python $D/core.py --index $i --raw --core-seconds 3600 --test-seconds 30 --out $D/cores/raw-$i.json > $D/cores/raw-$i.log 2>&1 || { echo "$i core-failed"; exit 0; }
uv run --extra search python $D/certify.py --core $D/cores/raw-$i.json --stem $D/certs/raw-$i > $D/certs/raw-$i.run.log 2>&1
.research/venv-exact/bin/python $D/verify_core.py --require-raw $D/certs/raw-$i.json > $D/certs/raw-$i.verify.json 2>&1
echo "$i $(tail -1 $D/certs/raw-$i.verify.json)"
