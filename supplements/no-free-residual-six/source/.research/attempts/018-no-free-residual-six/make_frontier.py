"""Typed frontier of the no-free (union 14) residual <= 6 case (PLAN.md step (a)).

From the canonical ledger (empty_pair, budget 28): every open inventory with
remaining defect r <= 6, with the reason union 14 is forced (r <= 4: the
accepted residual-four support constraints; r = 6: 1401/1404 union >= 12 plus
the exclusions of union 12 (checkpoint 1531) and union 13 (checkpoint 1533)),
and pins to existing partial reductions. Scopes are nested, never summed.
Independent check: frontier_reader.py.
"""
import json
import sys
from hashlib import sha256
from pathlib import Path

sys.dont_write_bytecode = True
R = Path(__file__).resolve().parents[2]
A = R / 'attempts'
LEDGER = R / 'findings/negative-quintic-pattern-cases-cycle1388.json'
RES4 = R / 'findings/empty-residual-four-support-constraints.json'
BASIS_R6 = {'union_at_least_12': A / '009-parent-analysis/three-disks-independent-authority-cycle1401.json',
            'union_12_excluded': A / '009-parent-analysis/cycle1531-parent-manifest.json',
            'union_13_excluded': A / '009-parent-analysis/cycle1533-parent-manifest.json'}
PARTIAL = {(2, 2, 2, 2): A / '006-solver-resume/four-double-frontier-cycle91.json',
           (3, 2, 1, 1, 1, 1, 1): A / '009-parent-analysis/empty-3211111-connected-odd-accepted-manifest.json'}


def pin(p):
    p = Path(p).resolve()
    return dict(path=str(p), sha256=sha256(p.read_bytes()).hexdigest())


def main(out):
    led = json.loads(LEDGER.read_text())['empty_pair']
    res4 = {tuple(r['negative_magnitudes']): r for r in json.loads(RES4.read_text())['covered_open_patterns']}
    rows = []
    for p in led['patterns']:
        if p['status'] == 'excluded' or p['remaining_defect'] > 6:
            continue
        mags = tuple(p['negative_magnitudes'])
        r = p['remaining_defect']
        if r <= 4:
            cov = res4[mags]
            if cov['necessary_negative_union_size'] != 14:
                raise SystemExit('residual-four row without union 14')
            basis = dict(kind='RESIDUAL_FOUR_SUPPORT_CONSTRAINTS', authority=pin(RES4))
        else:
            basis = dict(kind='UNION12_AND_13_EXCLUDED', **{k: pin(v) for k, v in BASIS_R6.items()})
        row = dict(negative_magnitudes=list(mags), supports=len(mags), negative_cost=sum(m * (m + 1) for m in mags),
                   remaining_defect=r, status='OPEN', union_14_basis=basis,
                   ledger_partial_reductions=p.get('partial_reductions', []))
        if mags in PARTIAL:
            row['partial_reduction_authority'] = pin(PARTIAL[mags])
        rows.append(row)
    doc = dict(status='NO_FREE_RESIDUAL6_FRONTIER', ledger=pin(LEDGER), budget=led['defect_budget'],
               scope='empty-pair selfdual representative; residual defect <= 6; negative-support union 14',
               rows=rows, open_rows=len(rows), whole_patterns_changed=0, global_status='OPEN')
    Path(out).write_text(json.dumps(doc, indent=1) + '\n')
    print(json.dumps(dict(open_rows=len(rows), by_r={r: sum(x['remaining_defect'] == r for x in rows) for r in (0, 2, 4, 6)})))
    return doc


if __name__ == '__main__':
    main(sys.argv[1])
