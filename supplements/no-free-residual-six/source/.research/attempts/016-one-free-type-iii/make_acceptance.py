"""Write the 1532 frontier, its reader result and the acceptance authority.

Runs the producer, then the independent reader on the written file, and
pins everything by SHA-256. Refuses to overwrite: frozen outputs are
immutable.
"""
import json
import sys
from hashlib import sha256
from pathlib import Path

import one_free_frontier
import one_free_frontier_reader

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
H = (HERE / '../009-parent-analysis').resolve()
S = (HERE / '../006-solver-resume').resolve()
FRONTIER = H / 'one-free-residual6-frontier-cycle1532.json'
READER = HERE / 'one-free-frontier-reader-result.json'
ACCEPT = H / 'one-free-residual6-acceptance-cycle1532.json'
TESTS = ['test_link_lemmas.py', 'test_one_seven_spheres.py', 'test_type2_shapes.py',
         'test_rigid_shape_facts.py', 'test_vertex_type_screen.py', 'test_one_free_frontier.py']
SCRIPTS = ['link_lemmas.py', 'one_seven_spheres.py', 'type2_shapes.py', 'rigid_shape_facts.py',
           'vertex_type_screen.py', 'one_free_frontier.py', 'one_free_frontier_reader.py', 'make_acceptance.py']


def pin(path):
    path = Path(path).resolve()
    return dict(path=str(path), sha256=sha256(path.read_bytes()).hexdigest())


def acceptance():
    return dict(
        status='ACCEPTED_CONDITIONAL_ONE_FREE_RESIDUAL6_TYPES_I_III_EXCLUDED_TYPE_II_REDUCED',
        cycle=1532,
        author='Alexander Richard Towell; substantial AI assistance (OpenAI Codex for cycles <= 1530, '
               'Claude Code Opus 5.5 for 014 to 016)',
        statement='In the one-free residual-six case (residual Fourier defect <= 6 with exactly one '
                  'negative-free coordinate u, classified by the 1513/1523 trichotomy), Type III '
                  '(c in {0,3}) and Type I (sole -3 cubic) have no realization, and Type II (c in {1,2}, '
                  'three cost-two departures through u) is reduced from 136 departure-shape classes to 24 '
                  'open ones: 23 three-pair shapes and the doubled-quartic shape -2{0,1}, -2{2,3}, '
                  'Q2{0,1,2,3}. These are statements about one derivative p = Delta_u f.',
        conditional_on=[
            'the 1513/1523 one-free trichotomy and every premise it inherits (selfdual representative, '
            'defect accounting)',
            'Type III: the accepted local premises of each two-exception source theorem (one-six-edge and '
            'one-three-edge arguments, six-vertex and pentagon lemmas, endpoint sphere catalogs and their '
            'inherited inverse-cover completeness), the 1526/1527 acceptance, the 76-record scan and the '
            'completeness of the Frick 2015 Theorem 3.10 catalog for (+1,+1), the 015 enumeration for L7/L8',
            'Type I: the 1395 local argument from its displayed form onward; the endpoint lemma is a hand '
            'proof at all orders',
            'Type II: the 006 private-vertex argument (two-exception-positive-extension.md and its accepted '
            'audit), the parity and weight identities of TYPE-II-RIGID-SHAPES.md, small-sphere facts S3, S4, '
            'S6 (exhaustive to 12 vertices and by curvature), pynauty for the producer shape list (the reader '
            'does not use it)',
        ],
        evidence=dict(
            frontier=pin(FRONTIER), frontier_reader_result=pin(READER), notes=pin(HERE / 'NOTES.md'),
            pricing=pin(HERE / 'TYPE-II-PRICING.md'),
            scripts=[pin(HERE / s) for s in SCRIPTS], tests=[pin(HERE / t) for t in TESTS],
            catalog_audit=pin(HERE / '../015-sphere-catalog-audit/audit-result.json'),
            previous_acceptance=pin(H / 'signed-star-two-free-acceptance-cycle1531.json'),
            premise_sources=[pin(H / n) for n in ('one-free-residual-six-and-extension-audit-cycle1513.md',
                                                  'one-free-parent-acceptance-cycle1523.json',
                                                  'minus-three-links-independent-review-cycle1395.md')]
            + [pin(S / n) for n in ('two-exception-positive-extension.md',
                                    'independent-math-audit/connected-six-unit-exclusion-audit.md')],
        ),
        review_kind='written arguments, each reviewed by a fresh AI subagent (Claude) that re-derived it and '
                    'replayed or rebuilt its finite checks in scratch files; small exact checks with tests in '
                    'normal and -O mode; not human peer review or formal verification',
        open_after=['Type II: 24 shape classes (frontier rows with status OPEN)', 'the no-free residual-six case',
                    'residual Fourier defect above six'],
        whole_patterns_changed=0, open_patterns=29, global_goal_complete=False, global_status='OPEN')


def main():
    for path in (FRONTIER, READER, ACCEPT):
        if path.exists():
            raise SystemExit('refusing to overwrite ' + str(path))
    one_free_frontier.main(['--out', str(FRONTIER)])
    result = one_free_frontier_reader.main([str(FRONTIER), '--out', str(READER)])
    if result['status'] != 'ONE_FREE_FRONTIER_READER_PASS':
        raise SystemExit('reader did not pass')
    ACCEPT.write_text(json.dumps(acceptance(), indent=1) + '\n')
    print(json.dumps(pin(ACCEPT)))


if __name__ == '__main__':
    main()
