"""Check every (path, sha256) pin in the seed documents against the staged source/ bytes.

  check_pins.py PACKET   prints mismatches and pins missing from source/ (repo-root entry docs excepted)
"""
import hashlib, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_packet as B


def pins(doc):
    if isinstance(doc, dict):
        if isinstance(doc.get('path'), str) and isinstance(doc.get('sha256'), str):
            yield doc['path'], doc['sha256']
        for v in doc.values():
            yield from pins(v)
    elif isinstance(doc, list):
        for v in doc:
            yield from pins(v)


def main(packet):
    src = Path(packet) / 'source'
    bad, seen = [], 0
    for s in B.SEEDS:
        for p, h in pins(json.loads(B.E.read_bytes(s))):
            q = Path(p) if p.startswith('/') else B.R / p
            if not q.is_relative_to(B.R) or '/certs/' in str(q):
                continue
            seen += 1
            f = src / q.relative_to(B.REPO)
            got = hashlib.sha256(f.read_bytes()).hexdigest() if f.exists() else None
            if got != h:
                bad.append(dict(seed=s.name, path=str(q), pinned=h, staged=got))
    print(json.dumps(dict(pins_checked=seen, mismatches=bad), indent=1))
    return not bad


if __name__ == '__main__':
    sys.exit(0 if main(sys.argv[1]) else 1)
