#!/usr/bin/env bash
# docker_replay.sh RUN_DIR CERTIFICATES_DIR [replay args...]: the REPRODUCE.md command, parameterized.
set -euo pipefail
P=$(cd "$(dirname "$0")/.." && pwd); RUN=$1; CERTS=$2; shift 2
mkdir -p "$RUN/results" "$RUN/scratch014" "$RUN/scratch017" "$RUN/scratch018"
O=/home/spinoza/github/math-theory/.research/attempts
exec docker run --rm --user "$(id -u):$(id -g)" --network none --read-only --cap-drop ALL \
  --security-opt no-new-privileges --memory 12g --cpus 2 --pids-limit 256 --tmpfs /tmp:rw,size=1g \
  --mount "type=bind,source=$P,target=/packet,readonly" \
  --mount "type=bind,source=$CERTS,target=/certificates,readonly" \
  --mount "type=bind,source=$P/source,target=/home/spinoza/github/math-theory,readonly" \
  --mount "type=bind,source=$RUN/scratch014,target=$O/014-context-pricing/certs" \
  --mount "type=bind,source=$RUN/scratch017,target=$O/017-type-ii-three-exception/certs" \
  --mount "type=bind,source=$RUN/scratch018,target=$O/018-no-free-residual-six/certs" \
  --mount "type=bind,source=$RUN/results,target=/results" \
  boolean-no-free-replay:1.5 python /packet/replay_packet.py "$@"
