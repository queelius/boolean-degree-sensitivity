"""Write the 1534 pattern ledger and acceptance authority (refuses to overwrite).

The successor ledger copies the frozen 1388 ledger and marks the empty-pair
patterns (2^4) and (2^4,1) excluded with basis 018 (lemma L1), after checking
that read-all-l1.json reports ALL_L1_CASES_VERIFIED with 0 rejected, 0 missing,
exact targets and every dependency pin matching the current files. Nothing else
in the ledger changes; check_successor() verifies that.

  make_acceptance_1534.py [--out-dir DIR]   (DIR for a dry run; default: the real targets)
"""
import argparse
import copy
import json
import sys
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
RESEARCH = HERE.parents[1]
H = RESEARCH / 'attempts/009-parent-analysis'
L1388 = RESEARCH / 'findings/negative-quintic-pattern-cases-cycle1388.json'
TARGETS = ([2, 2, 2, 2], [2, 2, 2, 2, 1])
NOTES = ['README.md', 'PLAN.md', 'L1.md', 'NOTES.md', 'CONTROLS.md']
REVIEWS = ['REVIEW-L1-codex.md', 'REVIEW-case754-codex.md', 'REVIEW-l1-assembly-audit-codex.md']
DATA = ['no-free-frontier.json', 'controls-n13.json', 'l1-cover.json', 'read-all-l1.json']
SCRIPTS = ['make_frontier.py', 'frontier_reader.py', 'controls_n13.py', 'cases018.py', 'cover_reader018.py',
           'model018.py', 'certify018.py', 'run018.py', 'status018.py', 'reader018.py', 'read_all018.py',
           'make_acceptance_1534.py']
TESTS = ['test_frontier.py', 'test_model018.py', 'test_reader018.py', 'test_read_all018.py',
         'test_make_acceptance_1534.py']


def pin(path):
    path = Path(path).resolve()
    return dict(path=str(path), sha256=sha256(path.read_bytes()).hexdigest())


def assembly(path=HERE / 'read-all-l1.json'):
    ra = json.loads(Path(path).read_text())
    stale = [d['path'] for d in ra['dependencies'] if pin(d['path'])['sha256'] != d['sha256']]
    if ra['status'] != 'ALL_L1_CASES_VERIFIED' or ra['rejected'] or ra['missing_count'] or not ra['targets_exact'] \
            or sorted(ra['target_inventories']) != sorted(TARGETS) or stale:
        raise SystemExit(f'assembly result does not support the exclusion (stale pins: {stale})')
    return ra


def ledger(old, acceptance_path):
    new = copy.deepcopy(old)
    refs = ['attempts/018-no-free-residual-six/L1.md', 'attempts/018-no-free-residual-six/read-all-l1.json',
            str(Path(acceptance_path).relative_to(RESEARCH)) if Path(acceptance_path).is_relative_to(RESEARCH)
            else str(acceptance_path)]
    for p in new['empty_pair']['patterns']:
        if p['negative_magnitudes'] in TARGETS:
            p.update(status='excluded', proof_refs=refs,
                     whole_pattern_exclusion_basis='L1_NO_FREE_RESIDUAL6_018')
    new['empty_pair']['open_count'] = sum(p['status'] != 'excluded' for p in new['empty_pair']['patterns'])
    new.update(updated_at=datetime.now(timezone.utc).isoformat(), predecessor=pin(L1388),
               whole_original_pattern_statuses_preserved=False, other_original_pattern_statuses_preserved=True,
               new_whole_pattern_exclusions=[list(t) for t in TARGETS])
    return new


def check_successor(old, new):
    """The successor differs from old only in the two target patterns (now excluded) and the header."""
    header = {'updated_at', 'predecessor', 'new_whole_pattern_exclusions', 'whole_original_pattern_statuses_preserved',
              'other_original_pattern_statuses_preserved', 'empty_pair'}
    if {k: v for k, v in old.items() if k not in header} != {k: v for k, v in new.items() if k not in header}:
        raise SystemExit('ledger changed outside the empty-pair patterns')
    a, b = old['empty_pair'], new['empty_pair']
    if {k: v for k, v in a.items() if k not in ('patterns', 'open_count')} != \
            {k: v for k, v in b.items() if k not in ('patterns', 'open_count')}:
        raise SystemExit('empty-pair header changed')
    if [p['negative_magnitudes'] for p in a['patterns']] != [p['negative_magnitudes'] for p in b['patterns']]:
        raise SystemExit('pattern list changed')
    for p, q in zip(a['patterns'], b['patterns']):
        if p['negative_magnitudes'] in TARGETS:
            if p['status'] != 'open' or q['status'] != 'excluded':
                raise SystemExit('target was not open, or is not now excluded')
            if {k: v for k, v in p.items() if k not in ('status', 'proof_refs')} != \
                    {k: v for k, v in q.items() if k not in ('status', 'proof_refs', 'whole_pattern_exclusion_basis')}:
                raise SystemExit('target changed beyond its status')
        elif p != q:
            raise SystemExit('a non-target pattern changed')
    if b['open_count'] != a['open_count'] - 2 or b['open_count'] != sum(p['status'] != 'excluded' for p in b['patterns']):
        raise SystemExit('open count')
    return dict(open_before=a['open_count'], open_after=b['open_count'], excluded=[list(t) for t in TARGETS])


def acceptance(ra, ledger_path):
    return dict(
        status='ACCEPTED_CONDITIONAL_WHOLE_PATTERNS_2222_22221_EXCLUDED',
        cycle=1534,
        author='Alexander Richard Towell; substantial AI assistance (OpenAI Codex for cycles <= 1530 and as '
               'reviewer and auditor in 018, Claude Code Opus 5.5 for 011 to 018)',
        statement='In the selfdual empty-pair existence representative (n = 14, degree <= 5, full sensitivity at the '
                  'origin), the negative quintic magnitude patterns (2,2,2,2) and (2,2,2,2,1) admit no Boolean '
                  'function. Basis: lemma L1 (018 L1.md: if a coordinate u lies in exactly one negative quintic, of '
                  'magnitude m in {1,2}, and in at most one residual departure, of cost 2, then no derivative '
                  'p = Delta_u f with the required properties exists), established by '
                  f'{ra["certificates"]} case certificates (LRAT, independent reader, pinned lrat-trim) covering all '
                  '4442 obligations of an independently checked 2221-case cover at m = 1 and m = 2; and the counting '
                  'in L1.md, which with negative-support union 14 gives an L1 coordinate in both patterns.',
        conditional_on=[
            'everything checkpoint 1533 accepts, including union 14 for both patterns (the no-free frontier '
            'authorities pinned in no-free-frontier.json) and the selfdual empty-pair reduction (existence only)',
            'the written reductions in L1.md (triangle incidence, ordinary-link classification, flagness, '
            'exceptional-endpoint classification, the doubled-quartic exclusion via 006 '
            'connected-six-unit-exclusion-audit.md, the A/B split and maximum-degree root choice), AI-reviewed',
            'completeness of the 017 sphere catalogs (roots-catalog.json, deltahedra.json) and surfaces.py, as '
            'accepted in 1533; CaDiCaL 3.0.1 and the pinned lrat-trim',
        ],
        evidence=dict(
            ledger=pin(ledger_path), previous_ledger=pin(L1388), assembly=pin(HERE / 'read-all-l1.json'),
            assembly_dependencies=ra['dependencies'],
            notes=[pin(HERE / n) for n in NOTES], reviews=[pin(HERE / n) for n in REVIEWS],
            data=[pin(HERE / n) for n in DATA], scripts=[pin(HERE / n) for n in SCRIPTS],
            tests=[pin(HERE / n) for n in TESTS],
            previous_acceptance=pin(H / 'one-free-residual6-acceptance-cycle1533.json'),
        ),
        certificates_note='certs/ (about 85 GB, write-protected) holds every certificate, CNF, label map and LRAT '
                          'proof; read-all-l1.json pins each by SHA-256. The case-754 failed partial proof '
                          '(certs/l1-00754-m1.lrat.failed-timeout.zst) is not evidence.',
        review_kind='lemma, cover and code reviewed by OpenAI Codex (L1 review, case-754 strategy, end-to-end assembly '
                    'audit); exact checks and tests in normal and -O mode; every certificate checked by an independent '
                    'reader and lrat-trim; not human peer review or formal verification',
        still_open=['the other 27 empty-pair patterns (20 with residual <= 6 and union 14, 7 with residual 8 to 12)'],
        whole_patterns_changed=2, open_patterns=27, global_goal_complete=False, global_status='OPEN')


def main(out_dir=None):
    ledger_path = Path(out_dir or RESEARCH / 'findings') / 'negative-quintic-pattern-cases-cycle1534.json'
    accept_path = Path(out_dir or H) / 'no-free-residual6-acceptance-cycle1534.json'
    for p in (ledger_path, accept_path):
        if p.exists():
            raise SystemExit('refusing to overwrite ' + str(p))
    ra = assembly()
    old = json.loads(L1388.read_text())
    new = ledger(old, accept_path)
    summary = check_successor(old, new)
    ledger_path.write_text(json.dumps(new, indent=1) + '\n')
    accept_path.write_text(json.dumps(acceptance(ra, ledger_path), indent=1) + '\n')
    print(json.dumps(dict(summary, written=[pin(ledger_path), pin(accept_path)])))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--out-dir')
    main(ap.parse_args().out_dir)
