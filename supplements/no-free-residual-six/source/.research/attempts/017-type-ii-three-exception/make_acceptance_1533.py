"""Write the 1533 one-free frontier and acceptance authority (refuses to overwrite).

The successor frontier copies the frozen 1532 frontier and marks each of its
24 OPEN Type II rows EXCLUDED with basis 017, after checking that
read-all-result.json reports ALL_CASES_VERIFIED with the universe bound to
exactly those rows. The authority also records the root-7 c = 2 raw-row
certificate (014 ROOT7-C2-RAW.md).
"""
import json
import sys
from hashlib import sha256
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
H = (HERE / '../009-parent-analysis').resolve()
C14 = (HERE / '../014-context-pricing').resolve()
F1532 = H / 'one-free-residual6-frontier-cycle1532.json'
F1533 = H / 'one-free-residual6-frontier-cycle1533.json'
ACCEPT = H / 'one-free-residual6-acceptance-cycle1533.json'
NOTES = ['PLAN.md', 'VERTEX-TYPES.md', 'CROSS-EDGES.md', 'NEAR-FLAG.md', 'SPECIAL-SHAPES.md', 'CERTIFICATES.md']
REVIEWS = ['REVIEW-vertex-types.md', 'REVIEW-vertex-types-codex.md', 'REVIEW-cross-edges-codex.md',
           'REVIEW-chain-codex.md', 'REVIEW-special-codex.md', 'REVIEW-final-codex.md']
DATA = ['vertex-types-result.json', 'roots-catalog.json', 'deltahedra.json', 'near-flag-result.json',
        'cover-cases.json', 'triangle-cover.json', 'shape1-cover.json', 'read-all-result.json']
SCRIPTS = ['surfaces.py', 'vertex_types.py', 'step4_count.py', 'roots.py', 'near_flag.py', 'cases.py',
           'cover_reader.py', 'model.py', 'solve_cases.py', 'certify017.py', 'reader017.py', 'run_cover.py',
           'read_all.py', 'make_acceptance_1533.py']
TESTS = ['test_surfaces_vertex_types.py', 'test_step4_count.py', 'test_reader017.py', 'test_cover.py',
         'test_assembly.py']


def pin(path):
    path = Path(path).resolve()
    return dict(path=str(path), sha256=sha256(path.read_bytes()).hexdigest())


def frontier():
    old = json.loads(F1532.read_text())
    ra = json.loads((HERE / 'read-all-result.json').read_text())
    if ra['status'] != 'ALL_CASES_VERIFIED' or not ra['universe_matches_frontier_1532'] or ra['missing_count'] \
            or ra['rejected'] or ra['frontier']['sha256'] != pin(F1532)['sha256']:
        raise SystemExit('assembly result does not support the successor frontier')
    rows = []
    for r in old['type_ii_classes']:
        r = dict(r)
        if r['status'] == 'OPEN':
            r.update(status='EXCLUDED', reason='THREE_EXCEPTION_CERTIFICATES', basis='certificates_017')
        rows.append(r)
    bases = dict(old['type_ii_bases'], certificates_017=dict(note=pin(HERE / 'CERTIFICATES.md'),
                                                             review=pin(HERE / 'REVIEW-final-codex.md'),
                                                             assembly=pin(HERE / 'read-all-result.json')))
    types = [dict(t) for t in old['types']]
    for t in types:
        if t['type'] == 'II':
            t.update(status='EXCLUDED', open_shape_classes=0)
    return dict(old, types=types, type_ii_classes=rows, type_ii_bases=bases, predecessor=pin(F1532),
                status='ONE_FREE_RESIDUAL6_FRONTIER', one_free_residual6_excluded=True,
                global_status='OPEN', whole_patterns_changed=0)


def acceptance():
    return dict(
        status='ACCEPTED_CONDITIONAL_ONE_FREE_RESIDUAL6_EXCLUDED',
        cycle=1533,
        author='Alexander Richard Towell; substantial AI assistance (OpenAI Codex for cycles <= 1530 and as '
               'reviewer in 017, Claude Code Opus 5.5 for 014 to 017)',
        statement='In the selfdual existence representative, the one-free residual-six case (residual Fourier defect '
                  '<= 6 with exactly one negative-free coordinate) has no Boolean function: Types I and III were '
                  'excluded in 1532, and the 24 Type II shape classes left open there are excluded by 3184 '
                  'case certificates (LRAT, independent reader) over an independently checked cover, each valid at '
                  'c = 1 and c = 2. Also: the root-7 signed-star context o7-i0-c2 has infeasible raw rows without '
                  'the 1497 unit clauses (014 raw pipeline, LRAT, 014 reader), so all 26 signed-star contexts are '
                  'excluded on raw rows.',
        conditional_on=[
            'everything checkpoint 1532 accepts for Types I and III, and the 1513/1523 trichotomy with its premises',
            'the written lemmas VERTEX-TYPES.md, CROSS-EDGES.md, NEAR-FLAG.md, SPECIAL-SHAPES.md (AI-reviewed)',
            'the 015 sphere enumeration (Steinitz-Rademacher contractible edges, pynauty certificates, Whitney '
            'uniqueness); CaDiCaL 3.0.1 and the pinned lrat-trim',
            'for o7-i0-c2: the 009 native raw rows and the 1409 premises, as for the other signed-star contexts',
        ],
        evidence=dict(
            frontier=pin(F1533), previous_frontier=pin(F1532),
            assembly=pin(HERE / 'read-all-result.json'),
            notes=[pin(HERE / n) for n in NOTES], reviews=[pin(HERE / n) for n in REVIEWS],
            data=[pin(HERE / n) for n in DATA], scripts=[pin(HERE / n) for n in SCRIPTS],
            tests=[pin(HERE / n) for n in TESTS],
            root7_c2=dict(note=pin(C14 / 'ROOT7-C2-RAW.md'), certificate=pin(C14 / 'certs/raw-1.json'),
                          reader_result=pin(C14 / 'certs/raw-1.verify.json'), core=pin(C14 / 'cores/raw-1.json')),
            previous_acceptance=pin(H / 'one-free-residual6-acceptance-cycle1532.json'),
        ),
        review_kind='written lemmas and code reviewed by OpenAI Codex (four reviews plus an end-to-end audit with a '
                    'sampled certificate re-check) and a Claude subagent; exact checks and 44 tests in normal and -O '
                    'mode; certificates checked by an independent reader and lrat-trim; not human peer review or '
                    'formal verification',
        still_open=['the no-free residual-six case', 'residual Fourier defect above six'],
        whole_patterns_changed=0, open_patterns=29, global_goal_complete=False, global_status='OPEN')


def main():
    for p in (F1533, ACCEPT):
        if p.exists():
            raise SystemExit('refusing to overwrite ' + str(p))
    F1533.write_text(json.dumps(frontier(), indent=1) + '\n')
    ACCEPT.write_text(json.dumps(acceptance(), indent=1) + '\n')
    print(json.dumps([pin(F1533), pin(ACCEPT)]))


if __name__ == '__main__':
    main()
