"""Stream the concatenated certificate tar parts and check every member against CERTIFICATE-MANIFEST.

  verify_tar.py MANIFEST PART [PART ...]   (parts in order; nothing is extracted to disk)

Passes only if the member names are exactly the manifest's, in order, each a regular file whose
size and SHA-256 equal its stored_bytes and stored_sha256. Prints one JSON line.
"""
import hashlib, json, sys, tarfile


class Parts:
    def __init__(self, paths):
        self.paths, self.f = list(paths), None

    def read(self, n=-1):
        out = b''
        while n < 0 or len(out) < n:
            if self.f is None:
                if not self.paths:
                    break
                self.f = open(self.paths.pop(0), 'rb')
            b = self.f.read(-1 if n < 0 else n - len(out))
            if not b:
                self.f.close(); self.f = None
                continue
            out += b
        return out


def main(manifest, parts):
    want = json.load(open(manifest))['files']
    got = []
    with tarfile.open(fileobj=Parts(parts), mode='r|') as t:
        for m in t:
            if not m.isreg():
                raise SystemExit(f'not a regular file: {m.name}')
            h, n, f = hashlib.sha256(), 0, t.extractfile(m)
            for b in iter(lambda: f.read(1 << 22), b''):
                h.update(b); n += len(b)
            got.append((m.name, n, h.hexdigest()))
    exp = [(e['member'], e['stored_bytes'], e['stored_sha256']) for e in want]
    ok = got == exp
    print(json.dumps(dict(status='TAR_MATCHES_MANIFEST' if ok else 'TAR_MISMATCH', members=len(got),
                          expected=len(exp), bytes=sum(g[1] for g in got),
                          first_difference=next((i for i, (a, b) in enumerate(zip(got, exp)) if a != b), None))))
    return ok


if __name__ == '__main__':
    sys.exit(0 if main(sys.argv[1], sys.argv[2:]) else 1)
