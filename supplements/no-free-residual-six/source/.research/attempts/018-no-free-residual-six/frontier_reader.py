"""Independent reader for no-free-frontier.json. Shares no code with make_frontier.py.

Rederives from the cost table alone every multiset of negative quintic
magnitudes m >= 1 with total cost sum m(m+1) in [22, 28] (remaining defect
r = 28 - cost <= 6), checks the ledger lists exactly these with r <= 6, that
the frontier rows are exactly the ledger's open ones among them, that each
row's cost and r are right, and that every pinned file matches its hash.
"""
import json
import sys
from hashlib import sha256
from pathlib import Path


class ReaderError(Exception):
    pass


def need(cond, detail):
    if not cond:
        raise ReaderError(detail)


def multisets(budget_lo, budget_hi):
    out = []

    def rec(prefix, maxm, cost):
        if budget_lo <= cost <= budget_hi:
            out.append(tuple(prefix))
        for m in range(maxm, 0, -1):
            if cost + m * (m + 1) <= budget_hi:
                rec(prefix + [m], m, cost + m * (m + 1))

    rec([], 5, 0)
    return sorted(set(out))


def check_pins(v):
    if isinstance(v, dict):
        if isinstance(v.get('path'), str) and isinstance(v.get('sha256'), str):
            need(sha256(Path(v['path']).read_bytes()).hexdigest() == v['sha256'], 'pin mismatch ' + v['path'])
        for x in v.values():
            check_pins(x)
    elif isinstance(v, list):
        for x in v:
            check_pins(x)


def read(doc):
    need(doc['status'] == 'NO_FREE_RESIDUAL6_FRONTIER' and doc['global_status'] == 'OPEN', 'header')
    need(doc['whole_patterns_changed'] == 0 and doc['budget'] == 28, 'header')
    check_pins(doc)
    led = json.loads(Path(doc['ledger']['path']).read_text())['empty_pair']['patterns']
    universe = multisets(22, 28)
    in_ledger = {tuple(sorted(p['negative_magnitudes'], reverse=True)): p for p in led}
    need(all(m in in_ledger for m in universe), 'ledger misses an r <= 6 inventory')
    need({m for m, p in in_ledger.items() if p['remaining_defect'] <= 6} == set(universe), 'ledger r <= 6 set differs')
    open_ = {m for m in universe if in_ledger[m]['status'] != 'excluded'}
    rows = {tuple(sorted(r['negative_magnitudes'], reverse=True)): r for r in doc['rows']}
    need(len(rows) == len(doc['rows']) == doc['open_rows'], 'row count')
    need(set(rows) == open_, 'frontier rows differ from the ledger open set')
    for m, r in rows.items():
        cost = sum(x * (x + 1) for x in m)
        need(r['negative_cost'] == cost and r['remaining_defect'] == 28 - cost and r['supports'] == len(m), 'row data')
        need(r['status'] == 'OPEN', 'row status')
        need(r['union_14_basis']['kind'] == ('RESIDUAL_FOUR_SUPPORT_CONSTRAINTS' if 28 - cost <= 4
                                             else 'UNION12_AND_13_EXCLUDED'), 'basis kind')
    return dict(status='NO_FREE_FRONTIER_READER_PASS', r_le_6_inventories=len(universe),
                excluded=len(universe) - len(open_), open=len(open_))


if __name__ == '__main__':
    print(json.dumps(read(json.loads(Path(sys.argv[1]).read_text()))))
