# Replay the frozen evidence

Requirements: Docker on Linux, approximately 10 GB of free disk space for the
unpacked evidence and runtime, and enough memory for a container limited to
6 GiB. The numerical LP solver is not run. The verification process itself
does not require network access; the initial runtime build downloads pinned
Python dependencies.

Run from the extracted packet directory:

```bash
docker build --tag boolean-spectral-replay:1 --file runtime/Dockerfile runtime
mkdir fresh-results
docker run --rm \
  --user "$(id -u):$(id -g)" \
  --network none --read-only --cap-drop ALL \
  --security-opt no-new-privileges \
  --memory 6g --cpus 2 --pids-limit 128 \
  --tmpfs /tmp:rw,size=64m \
  --mount "type=bind,source=$PWD,target=/packet,readonly" \
  --mount "type=bind,source=$PWD/source,target=/home/spinoza/github/math-theory,readonly" \
  --mount "type=bind,source=$PWD/fresh-results,target=/results" \
  boolean-spectral-replay:1 python /packet/replay_packet.py
```

The user flag lets the container write results owned by the invoking user.
The historical research path exists only inside the container and refers
only to the archive's `source/` directory. These commands do not overwrite
the host research directory.

A successful run writes `fresh-results/REPLAY-RECEIPT.json` after all stages
succeed. Its declared counts must be 138 controls and ten cases, with all
selected input and certificate checks passing. Every case must reproduce
the exact negative integer in `CASES.json`. A nonzero exit, timeout, missing
receipt or missing check is a failed or incomplete replay.

The selected checks cover complete input construction and exact row
contradictions conditional on the archived component-catalog and quotient
reductions. The domain-deletion stage is replayed as well. Earlier
classification and restriction certificates remain explicitly documented
dependencies; a successful run does not certify a global nonexistence claim.

The archived results directory preserves the original staged replay. Always
use a new output directory for another run. The driver intentionally refuses
to overwrite logs. Its source checks preserve original artifacts byte for
byte; it does not rewrite embedded paths or change recorded hashes.
