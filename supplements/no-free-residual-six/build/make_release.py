"""Finalize the v1.5.0 release files from a passing staged replay.

  make_release.py RUN_DIR DRAFT_JSON

RUN_DIR/results must hold a complete REPLAY-RECEIPT.json. Copies the receipt, stage records,
control records and the replayed read-all receipts (xz) into packet/verification/, writes
packet/CONTRIBUTION.json, builds dist/no-free-residual6-v1.5.0.tar.gz deterministically (sorted
members, fixed mtime and owner, gzip without name or time), and writes the archive-level
README-v1.5.0.md, CITATION-v1.5.0.cff, NO-FREE-SHA256-v1.5.0.txt and ARCHIVE-INDEX-v1.5.0.json
(the 65 inherited files from the draft JSON plus every new file with size, SHA-256 and MD5).
"""
import gzip
import hashlib
import io
import json
import lzma
import shutil
import sys
import tarfile
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
PACKET = HERE / 'packet'
DIST = HERE / 'dist'
VERSION = '1.5.0'
DOI = '10.5281/zenodo.23999933'
CONCEPT = '10.5281/zenodo.23496541'
TOP = f'no-free-residual6-v{VERSION}'
MTIME = 1793923200          # 2026-11-06T00:00:00Z


def digests(p):
    s, m, n = hashlib.sha256(), hashlib.md5(), 0
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 22), b''):
            s.update(b); m.update(b); n += len(b)
    return dict(bytes=n, sha256=s.hexdigest(), md5=m.hexdigest())


def verification(run):
    res = Path(run) / 'results'
    receipt = json.loads((res / 'REPLAY-RECEIPT.json').read_text())
    if not receipt['complete']:
        raise SystemExit('replay incomplete')
    out = PACKET / 'verification'
    out.mkdir(exist_ok=True)
    for p in sorted(res.iterdir()):
        if p.name.startswith('read-all-'):
            (out / (p.name + '.xz')).write_bytes(lzma.compress(p.read_bytes(), preset=6))
        else:
            shutil.copyfile(p, out / p.name)
    return receipt


def contribution(receipt):
    s = receipt['summary']
    doc = dict(
        schema_version=1, contribution_id='boolean-degree-five-spectral-exclusions', version=VERSION,
        reserved_version_doi=DOI, concept_doi=CONCEPT,
        title='Degree-five Boolean candidates: residual six with a negative-free coordinate excluded and two whole negative-quintic patterns excluded',
        global_problem_status='OPEN', actual_boolean_construction=False, exhaustive_nonexistence_proof=False,
        normalization='existence-preserving self-dual empty-pair representative; arbitrary f not assumed self-dual',
        checkpoints=[
            dict(cycle=1531, authority='source/.research/attempts/009-parent-analysis/signed-star-two-free-acceptance-cycle1531.json',
                 result='residual <= 6 with >= 2 negative-free coordinates excluded (26 signed-star contexts)'),
            dict(cycle=1532, authority='source/.research/attempts/009-parent-analysis/one-free-residual6-acceptance-cycle1532.json',
                 result='one-free residual six: Types I and III excluded, Type II reduced to 24 shape classes'),
            dict(cycle=1533, authority='source/.research/attempts/009-parent-analysis/one-free-residual6-acceptance-cycle1533.json',
                 result='one-free residual six excluded (3,184 certificates); o7-i0-c2 excluded on raw rows'),
            dict(cycle=1534, authority='source/.research/attempts/009-parent-analysis/no-free-residual6-acceptance-cycle1534.json',
                 result='lemma L1; whole patterns (2,2,2,2) and (2,2,2,2,1) excluded (3,662 certificates, 2,221 cases, 4,442 obligations)')],
        open_patterns_after=27, original_patterns=73,
        verification=dict(
            staged_container_replay='PASSED', receipt='verification/REPLAY-RECEIPT.json',
            source_files_verified=s['sources']['files'], certificate_files_verified=s['store']['files'],
            c014_certificates=s['c014']['certificates'], c017=dict((k, s['c017'][k]) for k in ('status', 'certificates', 'rejected', 'missing')),
            c018=dict((k, s['c018'][k]) for k in ('status', 'certificates', 'rejected', 'missing')),
            controls=[r for r in s['controls']['receipts']],
            written_reductions_checked_by_replay=False, review='AI review (OpenAI Codex, Claude subagents); not human peer review',
            proof_assistant_formalization=False, novelty_assessed=False),
        excluded='work after checkpoint 1534 (attempt 019 and later), which is not accepted',
        disclosure=dict(private_research_records='2026-10-23 to 2026-10-24 (checkpoints 1531 to 1534, unpublished research tree)',
                        first_public_disclosure='this archive; its date is the Zenodo publication date',
                        previous_public_source='https://github.com/queelius/boolean-degree-sensitivity (last commit 2026-10-21, '
                                               'v1.4.0 scope; does not contain these results)'),
        restored_pinned_bytes=[e['original_path'] for e in json.loads((PACKET / 'SOURCE-MANIFEST.json').read_text())['files']
                               if 'restored_pinned_bytes' in e],
        authors=[dict(name='Alexander Richard Towell', orcid='0000-0001-6443-9897',
                      affiliation='Southern Illinois University Edwardsville')],
        ai_assistance='substantial: OpenAI Codex (cycles <= 1530; reviewer and auditor for 017 and 018), '
                      'Claude Code with Claude Opus 5.5 (attempts 011 to 018, this packet)',
        licenses=dict(code='MIT', notes_certificates_data='CC-BY-4.0', bundled_lrat_trim='MIT (Armin Biere)'))
    (PACKET / 'CONTRIBUTION.json').write_text(json.dumps(doc, indent=1) + '\n')


def tarball():
    DIST.mkdir(exist_ok=True)
    out = DIST / f'{TOP}.tar.gz'
    paths = sorted(p for p in PACKET.rglob('*') if p.is_file() or p.is_symlink())
    dirs = sorted({q for p in paths for q in p.relative_to(PACKET).parents if str(q) != '.'})
    with open(out, 'wb') as raw, gzip.GzipFile(filename='', mode='wb', fileobj=raw, mtime=0, compresslevel=9) as gz, \
            tarfile.open(fileobj=gz, mode='w', format=tarfile.PAX_FORMAT) as t:
        def info(name, **kw):
            ti = tarfile.TarInfo(f'{TOP}/{name}' if name else TOP)
            ti.mtime, ti.uid, ti.gid, ti.uname, ti.gname = MTIME, 0, 0, '', ''
            for k, v in kw.items():
                setattr(ti, k, v)
            return ti
        t.addfile(info('', type=tarfile.DIRTYPE, mode=0o755))
        for d in dirs:
            t.addfile(info(str(d), type=tarfile.DIRTYPE, mode=0o755))
        for p in paths:
            rel = str(p.relative_to(PACKET))
            if p.is_symlink():
                t.addfile(info(rel, type=tarfile.SYMTYPE, linkname=str(p.readlink()), mode=0o777))
            else:
                mode = 0o755 if p.stat().st_mode & 0o111 else 0o644
                with open(p, 'rb') as f:
                    t.addfile(info(rel, size=p.stat().st_size, mode=mode), f)
    return out


def archive_files(draft, receipt):
    readme = DIST / f'README-v{VERSION}.md'
    readme.write_text(f"""# Version {VERSION}: residual six with a negative-free coordinate excluded, two whole patterns excluded

Alexander Richard Towell, with substantial AI assistance (OpenAI Codex;
Claude Code with Claude Opus 5.5). DOI {DOI}; concept DOI {CONCEPT}.

**Global status: OPEN.** Version {VERSION} adds the accepted research
checkpoints 1531 to 1534 for a degree-at-most-five Boolean function on 14
variables with full sensitivity at the origin, in the existence-preserving
self-dual empty-pair normal form (existence only): every instance with
residual Fourier defect at most six and a negative-free coordinate is excluded
(so the remaining residual <= 6 instances have negative-support union 14; 20 such
patterns stay open), and lemma L1 excludes the whole negative quintic magnitude
patterns (2,2,2,2) and (2,2,2,2,1); 27 of 73 patterns remain open. The results
are conditional on written reductions reviewed by AI models only and on the
earlier premises listed in the packet's REPORT.md.

New files in this version:

- `{TOP}.tar.gz`: the packet (REPORT.md, REPRODUCE.md, replay driver and
  controls, runtime, the 580 source and evidence files at their original
  paths, manifests, staged replay receipt). Start with its README.md.
  Requires an x86-64 Linux host with Docker (the bundled checker is an x86-64 binary).
- `certificates-v{VERSION}.tar.part00` to `part08`: one tar of the 41,304 stored
  certificate files of attempts 014, 017 and 018 (17.8 GB stored, 100.8 GB
  uncompressed), split into 2 GiB parts. Join with
  `cat certificates-v{VERSION}.tar.part0? | tar -x -C certificates`.
- `NO-FREE-SHA256-v{VERSION}.txt`: SHA-256 of every new file.
- `ARCHIVE-INDEX-v{VERSION}.json`: every file of this version, inherited or new,
  with size, SHA-256 and MD5.
- `CITATION-v{VERSION}.cff`.

The staged container replay re-read all {receipt['summary']['c017']['certificates']:,} (017) and
{receipt['summary']['c018']['certificates']:,} (018) case certificates and {receipt['summary']['c014']['certificates']} raw-row
certificates (014) with the frozen independent readers and lrat-trim, and passed its
controls in normal and optimized mode. It does not check the written
reductions. No Boolean construction, nonexistence proof, human peer review,
formalization or novelty is claimed. All files of earlier versions are kept
unchanged; their scope is described in their own README and ARCHIVE-INDEX files.
""")
    shutil.copyfile(PACKET / 'CITATION.cff', DIST / f'CITATION-v{VERSION}.cff')
    new = sorted(p for p in DIST.iterdir() if p.name not in (f'NO-FREE-SHA256-v{VERSION}.txt', f'ARCHIVE-INDEX-v{VERSION}.json'))
    rec = {p.name: digests(p) for p in new}
    (DIST / f'NO-FREE-SHA256-v{VERSION}.txt').write_text(''.join(f"{rec[n]['sha256']}  {n}\n" for n in sorted(rec)))
    inherited = [dict(name=f['filename'], bytes=f['filesize'], md5=f['checksum']) for f in draft['files']]
    index = dict(schema_version=1, version=VERSION, reserved_version_doi=DOI, concept_doi=CONCEPT,
                 inherited_from_version_doi='10.5281/zenodo.23544931', inherited_assets=sorted(inherited, key=lambda x: x['name']),
                 new_assets=[dict(name=n, **rec[n]) for n in sorted(rec)],
                 sha256_file=dict(name=f'NO-FREE-SHA256-v{VERSION}.txt', **digests(DIST / f'NO-FREE-SHA256-v{VERSION}.txt')),
                 replay_receipt_sha256=hashlib.sha256((PACKET / 'verification/REPLAY-RECEIPT.json').read_bytes()).hexdigest())
    (DIST / f'ARCHIVE-INDEX-v{VERSION}.json').write_text(json.dumps(index, indent=1) + '\n')
    print(json.dumps(dict(new_files=len(rec) + 2, inherited=len(inherited), total=len(rec) + 2 + len(inherited))))


if __name__ == '__main__':
    for n in ('build_packet.py', 'check_pins.py', 'verify_tar.py', 'make_release.py', 'zenodo_release.py'):
        shutil.copyfile(HERE / 'tools' / n, PACKET / 'build' / n)
    receipt = verification(sys.argv[1])
    (PACKET / 'review').mkdir(exist_ok=True)       # the pre-publication AI review and what was done
    shutil.copyfile(HERE / 'REVIEW-packet-codex.md', PACKET / 'review/REVIEW-packet-codex.md')
    shutil.copyfile(HERE / 'consultations/packet-review.answer.md', PACKET / 'review/packet-review.answer.md')
    contribution(receipt)
    tarball()
    archive_files(json.loads(Path(sys.argv[2]).read_text()), receipt)
