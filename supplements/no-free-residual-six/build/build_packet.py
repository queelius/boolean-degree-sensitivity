"""Stage the v1.5.0 packet for the accepted checkpoints 1531 to 1534.

  build_packet.py source OUT        copy the source closure into OUT/source (plain bytes) and
                                    write OUT/SOURCE-MANIFEST.json
  build_packet.py certificates OUT  write OUT/CERTIFICATE-MANIFEST.json and OUT/certificate-files.txt
                                    (the stored certificate files, as tar members relative to the
                                    repository root), hashing each stored file

Source closure: the attempt directories 014 to 018 without their certs/ and __pycache__, plus
every path pinned one level down by the four acceptances, the tip-interval authorization they
rely on (014's verify_core reads its sources) and the checkpoint manifests 1531 to 1534, plus
active-objective.md. Packed files (evidence store) are written as their original bytes and
checked against the store's recorded SHA-256. Certificates stay in their stored form (plain,
or lossless xz with the original SHA-256 recorded in the store map); they are never copied
here, only listed, so the split tar is the one real copy.
"""
import hashlib
import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

REPO = Path('/home/spinoza/github/math-theory')
R = REPO / '.research'
sys.path.insert(0, str(R / 'tools'))
import evidence_store as E  # noqa: E402

H = R / 'attempts/009-parent-analysis'
ATTEMPTS = ['014-context-pricing', '015-sphere-catalog-audit', '016-one-free-type-iii',
            '017-type-ii-three-exception', '018-no-free-residual-six']
CERT_ATTEMPTS = ['014-context-pricing', '017-type-ii-three-exception', '018-no-free-residual-six']
SEEDS = [H / n for n in ('signed-star-two-free-acceptance-cycle1531.json', 'one-free-residual6-acceptance-cycle1532.json',
                         'one-free-residual6-acceptance-cycle1533.json', 'no-free-residual6-acceptance-cycle1534.json',
                         'tip-interval-parent-authorization-cycle1520.json')] + \
        [H / f'cycle{c}-parent-manifest.json' for c in range(1531, 1535)]
EXTRA = [R / 'active-objective.md', H / 'two-free-independent-review-cycle1409.md',
         # read by the 016 and 018 packet tests (found with an open-audit hook on the host run)
         R / 'attempts/006-solver-resume/four-double-frontier-cycle91.json',
         R / 'attempts/006-solver-resume/sphere-triangulations-05.json',
         R / 'attempts/006-solver-resume/sphere-triangulations-06.json',
         H / 'empty-3211111-connected-odd-accepted-manifest.json',
         R / 'findings/empty-residual-four-support-constraints.json']
# 014's CLI tests call the research interpreter by its historical path; in the container that
# path is a symbolic link to the container's Python 3.10 (recorded in the manifest as a shim)
SHIMS = {'.research/venv-exact/bin/python': '/usr/local/bin/python'}
# lrat-trim (upstream github.com/arminbiere/lrat-trim, commit b30f400f4ee5c32b77ee566a7c006081b521534f):
# the pinned binary plus its source, build files and license (the license requires its notice)
LRAT = R / 'attempts/006-solver-resume/lrat-trim'
EXTRA += [LRAT / n for n in ('LICENSE', 'README.md', 'NEWS.md', 'TODO.md', 'configure', 'makefile',
                             'makefile.in', 'lrat-trim.c', '.clang-format', '.gitignore')]
# Pinned files edited after their checkpoint: the packet carries the pinned bytes, recovered by
# reversing the later edits recorded in the session transcript and checked against the pin.
OVERRIDES = {R / 'attempts/018-no-free-residual-six/README.md':
             (Path(__file__).resolve().parents[1] / 'README-018-accepted-cycle1534.md',
              '00a0b9b8da57ca8ff37cfb9d5c230326a14d435bd882ef9e2d792a409cfe3bfc',
              'pinned by the 1534 acceptance and manifest; the live file was edited afterwards '
              '(2026-10-24 08:33 and 22:47 UTC, navigation only); these are the pinned bytes')}
SKIP_PARTS = {'__pycache__', 'certs'}


def pinned_paths(doc):
    if isinstance(doc, dict):
        for k, v in doc.items():
            if k == 'path' and isinstance(v, str):
                yield v
            else:
                yield from pinned_paths(v)
    elif isinstance(doc, list):
        for v in doc:
            yield from pinned_paths(v)


def logical_files(d):
    """Files of an attempt directory by original name (a packed x.xz counts as x)."""
    packed = {k for k in E.load_map() if k.startswith(E.rel(d) + '/')}
    out = set()
    for p in d.rglob('*'):
        if p.is_file() and not SKIP_PARTS & set(p.relative_to(d).parts) and not p.name.endswith('.pyc'):
            out.add(p)
    for k in packed:
        q = R / k
        if not SKIP_PARTS & set(q.relative_to(d).parts):
            out.add(q)
            out.discard(Path(str(q) + '.xz'))
    return out


def closure():
    files = set(EXTRA)
    for a in ATTEMPTS:
        files |= logical_files(R / 'attempts' / a)
    for s in SEEDS:
        files.add(s)
        for p in pinned_paths(json.loads(E.read_bytes(s))):
            q = Path(p) if p.startswith('/') else R / p
            if '/certs/' not in str(q) and q.is_relative_to(R):   # entry docs at the repo root are not evidence
                files.add(q)
    return sorted(files)


def source(out):
    out = Path(out)
    entries = []
    for f in closure():
        data = E.read_bytes(f)            # checks packed bytes against the store map
        note = None
        if f in OVERRIDES:
            src, pin, note = OVERRIDES[f]
            data = src.read_bytes()
            E.require(hashlib.sha256(data).hexdigest() == pin, f'override does not match its pin: {f}')
        rel = f.relative_to(REPO)
        dst = out / 'source' / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(data)
        mode = f.stat().st_mode if f.exists() else E.load_map()[E.rel(f)].get('mode', 0o644)
        os.chmod(dst, 0o755 if mode & 0o111 else 0o644)
        entries.append(dict(original_path=str(f), packet_path=str(Path('source') / rel), bytes=len(data),
                            sha256=hashlib.sha256(data).hexdigest(), **({'restored_pinned_bytes': note} if note else {})))
    for a in CERT_ATTEMPTS:              # mount points for the replay's scratch certificate dirs
        (out / 'source' / '.research/attempts' / a / 'certs').mkdir(parents=True, exist_ok=True)
    for rel, target in SHIMS.items():
        (out / 'source' / rel).parent.mkdir(parents=True, exist_ok=True)
        (out / 'source' / rel).symlink_to(target)
    doc = dict(schema_version=1, kind='SOURCE_MANIFEST', original_root=str(REPO), files=entries,
               shims=[dict(path=str(REPO / k), symlink_to=v) for k, v in SHIMS.items()],
               file_count=len(entries), total_bytes=sum(e['bytes'] for e in entries))
    (out / 'SOURCE-MANIFEST.json').write_text(json.dumps(doc, indent=1) + '\n')
    print(json.dumps(dict(files=len(entries), bytes=doc['total_bytes'])))
    import check_pins                    # every seed pin must hold for the staged bytes
    E.require(check_pins.main(out), 'staged source does not match the checkpoint pins')


def certificates(out):
    out = Path(out)
    smap = E.load_map()
    stored = sorted(p for a in CERT_ATTEMPTS for p in (R / 'attempts' / a / 'certs').iterdir() if p.is_file())

    def one(p):
        digest, n = E.hash_file(p)
        e = dict(member=str(p.relative_to(REPO)), stored_bytes=n, stored_sha256=digest)
        if p.suffix == '.xz' and E.rel(Path(str(p)[:-3])) in smap:
            m = smap[E.rel(Path(str(p)[:-3]))]
            E.require(Path(R / m['archive']).resolve() == p.resolve() or os.path.samefile(R / m['archive'], p),
                      f'archive mismatch {p}')
            e.update(encoding='xz', original_path=str(p)[:-3], original_bytes=m['size'], original_sha256=m['sha256'])
        else:
            E.require(p.suffix != '.xz', f'xz file not in the store map: {p}')
            e.update(encoding='plain', original_path=str(p), original_bytes=n, original_sha256=digest)
        return e

    with ThreadPoolExecutor(6) as ex:
        entries = list(ex.map(one, stored))
    # hardlink-deduplicated originals share another file's archive: record them as aliases
    members = {e['member'] for e in entries}
    aliases = []
    for k, m in sorted(smap.items()):
        q = R / k
        if q.parent.name == 'certs' and q.parent.parent.name in CERT_ATTEMPTS and m['archive'] != k + '.xz':
            member = str((R / m['archive']).relative_to(REPO))
            E.require(member in members, f'alias archive not stored: {k}')
            aliases.append(dict(original_path=str(q), member=member, encoding='xz',
                                original_bytes=m['size'], original_sha256=m['sha256']))
    doc = dict(schema_version=1, kind='CERTIFICATE_MANIFEST', original_root=str(REPO), aliases=aliases,
               note='Members of the certificates tar, relative to the repository root, in stored form. '
                    'encoding xz: lossless xz; decompressing gives original_bytes with original_sha256, '
                    'the hash the certificate JSONs and read-all receipts pin. aliases: original files whose '
                    'bytes are identical to another and that share its archive member.',
               files=entries, file_count=len(entries), stored_bytes=sum(e['stored_bytes'] for e in entries),
               original_bytes=sum(e['original_bytes'] for e in entries))
    (out / 'CERTIFICATE-MANIFEST.json').write_text(json.dumps(doc, indent=1) + '\n')
    (out / 'certificate-files.txt').write_text(''.join(e['member'] + '\n' for e in entries))
    print(json.dumps(dict(files=len(entries), aliases=len(aliases), stored=doc['stored_bytes'],
                          original=doc['original_bytes'])))


if __name__ == '__main__':
    {'source': source, 'certificates': certificates}[sys.argv[1]](sys.argv[2])
