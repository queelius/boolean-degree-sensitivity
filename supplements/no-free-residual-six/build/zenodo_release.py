"""Upload, describe, publish and verify the v1.5.0 Zenodo version (draft 23999933).

  zenodo_release.py upload      PUT every dist/ file into the draft bucket (skips files already
                                there with the same MD5), then check the draft's file list
  zenodo_release.py metadata    set the v1.5.0 metadata (the v1.4.0 description is kept below a
                                new section) and print the stored description for inspection
  zenodo_release.py publish     publish the draft
  zenodo_release.py verify OUT  anonymously fetch the public record and every file body,
                                checking size, MD5 and (new files) SHA-256; write the receipt OUT

The token is read from ~/.zenodo.toml and sent only in the Authorization header (never printed,
never in a URL). Receipts and responses are written to receipts/.
"""
import hashlib
import html
import json
import sys
import time
import tomllib
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
DIST = HERE / 'dist'
REC = HERE / 'receipts'
API = 'https://zenodo.org/api'
DRAFT = 23999933
OLD = 23544931
VERSION = '1.5.0'
TOKEN = tomllib.load(open(Path.home() / '.zenodo.toml', 'rb'))['tokens']['production']


def call(method, url, body=None, ctype='application/json', auth=True, headers=None, timeout=600):
    url = url if url.startswith('http') else API + url
    data = json.dumps(body).encode() if isinstance(body, (dict, list)) else body
    r = urllib.request.Request(url, data=data, method=method)
    if auth:
        r.add_header('Authorization', 'Bearer ' + TOKEN)
    if data is not None:
        r.add_header('Content-Type', ctype)
    for k, v in (headers or {}).items():
        r.add_header(k, v)
    for attempt in range(5):
        try:
            with urllib.request.urlopen(r, timeout=timeout) as resp:
                b = resp.read()
                return json.loads(b) if b else None
        except (urllib.error.URLError, ConnectionError, TimeoutError) as e:
            if isinstance(e, urllib.error.HTTPError) and e.code < 500:
                raise SystemExit(f'{method} {url}: HTTP {e.code} {e.read()[:500]!r}')
            if attempt == 4 or (data is not None and not isinstance(data, bytes)):
                raise
            time.sleep(10 * (attempt + 1))


def md5(p):
    h = hashlib.md5()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 22), b''):
            h.update(b)
    return h.hexdigest()


def draft():
    return call('GET', f'/deposit/depositions/{DRAFT}')


def upload():
    REC.mkdir(exist_ok=True)
    d = draft()
    assert d['state'] == 'unsubmitted' and not d['submitted'], d['state']
    bucket = d['links']['bucket']
    have = {f['filename']: f['checksum'] for f in d['files']}
    for p in sorted(DIST.iterdir()):
        want = md5(p)
        if have.get(p.name) == want:
            print(json.dumps(dict(file=p.name, skipped='already uploaded')), flush=True)
            continue
        if p.name in have:
            raise SystemExit(f'{p.name} exists in the draft with different bytes; refusing to overwrite')
        size = p.stat().st_size
        for attempt in range(4):
            try:
                with open(p, 'rb') as f:
                    t = time.monotonic()
                    r = urllib.request.Request(f'{bucket}/{p.name}', data=f, method='PUT')
                    r.add_header('Authorization', 'Bearer ' + TOKEN)
                    r.add_header('Content-Type', 'application/octet-stream')
                    r.add_header('Content-Length', str(size))
                    with urllib.request.urlopen(r, timeout=7200) as resp:
                        out = json.loads(resp.read())
                break
            except (urllib.error.URLError, ConnectionError, TimeoutError) as e:
                if attempt == 3:
                    raise
                print(json.dumps(dict(file=p.name, retry=attempt + 1, error=repr(e)[:200])), flush=True)
                time.sleep(30)
        if out['checksum'] != 'md5:' + want or out['size'] != size:
            raise SystemExit(f'{p.name}: server checksum {out["checksum"]} size {out["size"]}')
        print(json.dumps(dict(file=p.name, bytes=size, md5=want, seconds=round(time.monotonic() - t, 1))), flush=True)
    d = draft()
    names = {f['filename']: f for f in d['files']}
    missing = [p.name for p in DIST.iterdir() if p.name not in names or names[p.name]['checksum'] != md5(p)]
    (REC / 'draft-after-upload.json').write_text(json.dumps(d, indent=1) + '\n')
    print(json.dumps(dict(draft_files=len(names), missing_or_different=missing)))
    if missing or len(names) > 100:
        raise SystemExit(1)


SECTION = """<h2>Version 1.5.0: residual six with a negative-free coordinate excluded; two whole negative-quintic patterns excluded</h2>
<p>{p1}</p>
<p>{p2}</p>
<p>{p3}</p>
<p>{p4}</p>
<h2>Earlier versions</h2>
"""


def metadata():
    old = call('GET', f'/deposit/depositions/{OLD}')['metadata']
    m = draft()['metadata']
    e = html.escape
    sec = SECTION.format(
        p1=e('Global status: OPEN. This version archives the accepted research checkpoints 1531 to 1534 for a '
             'Boolean function on 14 variables of real degree at most 5 with full sensitivity at the origin, in the '
             'existence-preserving self-dual empty-pair normal form (the reduction holds for existence only; arbitrary '
             'functions are not assumed self-dual). For residual Fourier defect at most 6, the case with at least '
             'two negative-free coordinates (26 signed-star contexts) and the case with exactly one (Types I, II and '
             'III) are excluded, so every remaining residual <= 6 instance has negative-support union 14; residual '
             '<= 6 is not closed, 20 of its patterns remain open in that case. Lemma L1 then excludes '
             'the whole negative quintic magnitude patterns (2,2,2,2) and (2,2,2,2,1). 27 of the 73 original patterns '
             'remain open.'),
        p2=e('Evidence: 6,871 case certificates (CNF with label maps and CaDiCaL LRAT proofs, 17.8 GB stored as '
             'lossless xz, 100.8 GB uncompressed) over independently checked covers, each read by an independent reader '
             'that rebuilds the rows from their definitions, checks clause soundness and runs the pinned lrat-trim. '
             'A staged, network-less container replay re-ran every certificate with the frozen readers and assembly '
             'drivers, compared every result with the archived receipts, and passed positive and negative controls in '
             'normal and optimized mode. The certificates are one tar split into nine parts; the packet tarball holds '
             'the report, sources, manifests, replay driver and receipt.'),
        p3=e('The results are conditional: on written reductions (attempts 016 to 018, including L1.md) reviewed by AI '
             'models only, the completeness of the sphere catalogs used, and the earlier accepted premises listed in '
             'REPORT.md. The replay does not check the written reductions. No Boolean construction, nonexistence proof, '
             'human peer review, proof-assistant formalization or novelty is claimed. Unaccepted later work is not included.'),
        p4=e('Alexander Richard Towell, with substantial AI assistance: OpenAI Codex (most work up to cycle 1530; '
             'reviewer and auditor for attempts 017 and 018) and Claude Code with Claude Opus 5.5 (attempts 011 to 018 '
             'and this packet). Code MIT; proofs, notes, certificates and data CC-BY-4.0; bundled lrat-trim MIT '
             '(Armin Biere). A DOI is an archival citation, not a guarantee of correctness, novelty, review or priority.'))
    keywords = sorted(set(old['keywords']) | {'LRAT certificates', 'SAT', 'negative quintic patterns'})
    new = dict(old)
    for k in ('doi', 'prereserve_doi'):
        new.pop(k, None)
    new.update(title='Exact exclusions for degree-five Boolean candidates: residual six with a negative-free '
                     'coordinate excluded and two whole negative-quintic patterns excluded, with LRAT certificates',
               version=VERSION, publication_date=time.strftime('%Y-%m-%d', time.gmtime()),
               description=sec + old['description'], keywords=keywords,
               notes='Version 1.5.0 keeps all 65 files of 1.4.0 unchanged and adds the checkpoint 1531 to 1534 packet '
                     'and certificates. Global problem open. No human, formal or novelty claim.',
               prereserve_doi=m.get('prereserve_doi'))
    out = call('PUT', f'/deposit/depositions/{DRAFT}', dict(metadata=new))
    REC.mkdir(exist_ok=True)
    (REC / 'draft-metadata.json').write_text(json.dumps(out, indent=1) + '\n')
    got = out['metadata']
    print(json.dumps({k: got.get(k) for k in ('title', 'version', 'publication_date', 'doi', 'upload_type',
                                              'publication_type', 'license', 'creators')}, indent=1))
    print(got['description'][:len(sec) + 200])


def publish():
    d = draft()
    assert d['metadata']['version'] == VERSION and len(d['files']) <= 100
    out = call('POST', f'/deposit/depositions/{DRAFT}/actions/publish', timeout=1800)
    REC.mkdir(exist_ok=True)
    (REC / 'publish-response.json').write_text(json.dumps(out, indent=1) + '\n')
    print(json.dumps(dict(state=out['state'], submitted=out['submitted'], doi=out['doi'],
                          record=out['links'].get('record_html'))))


def verify(out_path):
    rec = call('GET', f'/records/{DRAFT}', auth=False)
    index = json.loads((DIST / f'ARCHIVE-INDEX-v{VERSION}.json').read_text())
    new = {a['name']: a for a in index['new_assets']}
    new[index['sha256_file']['name']] = index['sha256_file']
    inherited = {a['name']: a for a in index['inherited_assets']}
    files = rec['files']
    results = []
    for f in sorted(files, key=lambda f: f['key']):
        url = f['links']['self']
        s, m, n = hashlib.sha256(), hashlib.md5(), 0
        with urllib.request.urlopen(urllib.request.Request(url), timeout=7200) as resp:
            for b in iter(lambda: resp.read(1 << 22), b''):
                s.update(b); m.update(b); n += len(b)
        want = new.get(f['key']) or inherited.get(f['key'])
        ok = want is not None and n == want['bytes'] and m.hexdigest() == want['md5'] and \
            ('sha256' not in want or s.hexdigest() == want['sha256']) and f['checksum'] == 'md5:' + m.hexdigest()
        results.append(dict(name=f['key'], bytes=n, sha256=s.hexdigest(), md5=m.hexdigest(), new=f['key'] in new,
                            public_url=url, downloaded_without_authentication=True, ok=ok))
        print(json.dumps(dict(name=f['key'], ok=ok)), flush=True)
    ok = all(r['ok'] for r in results) and {r['name'] for r in results} == set(new) | set(inherited)
    doc = dict(schema_version=1, status='ALL_PUBLIC_FILE_BODIES_VERIFIED' if ok else 'VERIFICATION_FAILED',
               observed_at=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), record_id=DRAFT, version=VERSION,
               version_doi=rec.get('doi'), concept_doi=rec.get('conceptdoi'), record_url=rec['links'].get('self_html'),
               publication_date=rec['metadata'].get('publication_date'), total_public_files=len(results),
               verified_bytes=sum(r['bytes'] for r in results), files=results)
    Path(out_path).write_text(json.dumps(doc, indent=1) + '\n')
    print(json.dumps({k: doc[k] for k in ('status', 'version_doi', 'concept_doi', 'total_public_files', 'verified_bytes')}))
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    cmd = sys.argv[1]
    {'upload': upload, 'metadata': metadata, 'publish': publish}.get(cmd, lambda: verify(sys.argv[2]))()
