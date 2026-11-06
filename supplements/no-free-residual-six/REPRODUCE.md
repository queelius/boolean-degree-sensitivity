# Replay the v1.5.0 certificates

Requirements: an **x86-64** Linux host with Docker (the bundled lrat-trim is
a dynamically linked x86-64 ELF binary; on another architecture rebuild it
from the included source, which changes its pinned hash, or use x86-64
emulation), about 20 GB of disk for the downloaded certificate parts plus
about 18 GB for their extraction (the parts can be deleted after extraction),
and scratch space while the replay runs. Each worker decompresses one
certificate at a time (the largest uses about 3.5 GB), so with `--jobs J`
plan for about J x 3.5 GB of scratch; the 100.8 GB uncompressed total is never
needed at once. The verification itself runs without
network access; building the runtime image downloads the pinned base image
and Python packages once.

## 1. Download and check

From the Zenodo record, download `no-free-residual6-v1.5.0.tar.gz`, the nine
parts `certificates-v1.5.0.tar.part00` to `part08`, and
`NO-FREE-SHA256-v1.5.0.txt`. Then:

```bash
sha256sum -c NO-FREE-SHA256-v1.5.0.txt
tar -xzf no-free-residual6-v1.5.0.tar.gz          # creates no-free-residual6-v1.5.0/
mkdir certificates
cat certificates-v1.5.0.tar.part0? | tar -x -C certificates
```

`certificates/` then holds `.research/attempts/{014,017,018}-*/certs/` in
stored form: small files plain, larger ones as lossless `.xz`. Decompressing
an `.xz` member gives exactly the bytes whose SHA-256 the certificate JSONs
and receipts pin (`CERTIFICATE-MANIFEST.json`, fields `original_sha256`).

## 2. Build the runtime

```bash
cd no-free-residual6-v1.5.0
docker build --tag boolean-no-free-replay:1.5 --file runtime/Dockerfile runtime
```

The image is Python 3.10.20 (pinned by digest) with numpy 2.2.6, scipy
1.15.3, python-sat 1.8.dev24, pynauty 2.8.8.1 and pytest 9.1.1, the versions
of the research interpreter.

## 3. Run

```bash
P="$PWD"; C="$PWD/../certificates"; RUN="$PWD/../replay-run"
O=/home/spinoza/github/math-theory/.research/attempts
mkdir -p "$RUN/results" "$RUN/scratch014" "$RUN/scratch017" "$RUN/scratch018"
docker run --rm --user "$(id -u):$(id -g)" --network none --read-only --cap-drop ALL \
  --security-opt no-new-privileges --memory 12g --cpus 2 --pids-limit 256 --tmpfs /tmp:rw,size=1g \
  --mount "type=bind,source=$P,target=/packet,readonly" \
  --mount "type=bind,source=$C,target=/certificates,readonly" \
  --mount "type=bind,source=$P/source,target=/home/spinoza/github/math-theory,readonly" \
  --mount "type=bind,source=$RUN/scratch014,target=$O/014-context-pricing/certs" \
  --mount "type=bind,source=$RUN/scratch017,target=$O/017-type-ii-three-exception/certs" \
  --mount "type=bind,source=$RUN/scratch018,target=$O/018-no-free-residual-six/certs" \
  --mount "type=bind,source=$RUN/results,target=/results" \
  boolean-no-free-replay:1.5 python /packet/replay_packet.py --jobs 2
```

The historical research path `/home/spinoza/github/math-theory` exists only
inside the container. It is the packet's read-only `source/` tree, so the
frozen readers, which name absolute paths, run unchanged; the three `certs/`
directories are empty writable scratch mounts. The one addition to the tree
is a symbolic link `source/.research/venv-exact/bin/python` to the
container's Python, recorded in `SOURCE-MANIFEST.json` under `shims`, which
the 014 command-line tests call. Nothing on the host is read except the
mounted directories. More jobs (`--jobs`, with a matching `--cpus`) shorten
the run.

## 4. Expected result

The run prints one JSON line per stage and ends with
`{"receipt": "REPLAY-RECEIPT.json", "complete": true}`. The receipt in
`results/` must report:

- `sources`: 580 files; `store`: 41,304 files;
- `c014`: 26 certificates, all verified and equal to their archived records;
- `c017`: `ALL_CASES_VERIFIED`, 3,184 certificates, 0 rejected, 0 missing,
  results equal to the archived receipt;
- `c018`: `ALL_L1_CASES_VERIFIED`, 3,662 certificates, 0 rejected,
  0 missing, results equal to the archived receipt;
- `controls`: 15 of 15 in normal and 15 of 15 in optimized mode;
- `tests`: the packet tests of 014 to 018 pass in both modes.

A nonzero exit, a missing receipt or a `PARTIAL-RECEIPT-*` file is a failed
or incomplete replay. The staged run on the author's machine took the time
recorded in `verification/REPLAY-RECEIPT.json` with two jobs. Use a fresh run
directory for every run: the driver refuses non-empty scratch directories
and existing logs.

## Checking a single certificate

To read one 018 certificate by hand inside the same container, decompress its
`.json`, `.cnf`, `.labels.json` and `.lrat` from `certificates/` into the
scratch `certs/` directory and run
`python $O/018-no-free-residual-six/reader018.py $O/018-no-free-residual-six/certs/<name>.json`.
The 017 reader (`reader017.py`) and the 014 reader (`verify_core.py --require-raw`)
work the same way.

`build/` contains the scripts that staged this packet, kept for provenance
(`build_packet.py`, `check_pins.py`, `verify_tar.py`, `make_release.py`,
`zenodo_release.py`); their paths refer to the author's staging layout. The
helper `build/docker_replay.sh RUN_DIR CERTIFICATES_DIR [args]` runs the
command above from an extracted packet.
