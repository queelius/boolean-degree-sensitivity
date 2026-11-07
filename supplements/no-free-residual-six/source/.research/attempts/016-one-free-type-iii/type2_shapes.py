"""Type II departure shapes up to relabelling, and the private-vertex filter.

A Type II derivative has three distinct cost-two departures: pair numerators
-2 or +1 (on distinct pairs) and doubled quartics l_D = 2. A doubled quartic
with a vertex lying in no other departure is excluded by the constant-free
private-vertex argument (006/two-exception-positive-extension.md, accepted in
006/independent-math-audit/connected-six-unit-exclusion-audit.md).
"""
import itertools
import json
import sys
from collections import Counter

import pynauty

sys.dont_write_bytecode = True
KINDS = ('-2', '+1', 'Q2')


def valid(deps):
    pair_supports = [s for k, s in deps if k != 'Q2']
    return len(set(deps)) == len(deps) and len(set(pair_supports)) == len(pair_supports)


def canon(deps):
    verts = sorted(set().union(*[s for _, s in deps]))
    vi = {v: i for i, v in enumerate(verts)}
    nv = len(verts)
    adj = {i: [] for i in range(nv + len(deps))}
    for j, (_, s) in enumerate(deps):
        adj[nv + j] = [vi[v] for v in s]
    colors = [set(range(nv))] + [{nv + j for j, (k, _) in enumerate(deps) if k == kind} for kind in KINDS]
    g = pynauty.Graph(nv + len(deps), adjacency_dict=adj, vertex_coloring=[c for c in colors if c])
    return nv, tuple(sorted(Counter(k for k, _ in deps).items())), pynauty.certificate(g)


def private_quartic(deps):
    for i, (k, s) in enumerate(deps):
        if k == 'Q2' and s - set().union(*[t for j, (_, t) in enumerate(deps) if j != i]):
            return True
    return False


def shapes():
    """One representative per class: the first departure sits on the lowest
    labels, the second within 0..7 and the third within 0..11, which reaches
    every configuration of three departures (union at most twelve vertices)."""
    v = range(12)
    objs = ([(k, frozenset(p)) for k in ('-2', '+1') for p in itertools.combinations(v, 2)]
            + [('Q2', frozenset(q)) for q in itertools.combinations(v, 4)])
    firsts = [('-2', frozenset({0, 1})), ('+1', frozenset({0, 1})), ('Q2', frozenset({0, 1, 2, 3}))]
    seen = {}
    for f in firsts:
        for s in objs:
            if max(s[1]) > 7:
                continue
            for t in objs:
                deps = [f, s, t]
                if max(t[1]) > 11 or not valid(deps):
                    continue
                seen.setdefault(canon(deps), deps)
    return list(seen.values())


def main():
    out = Counter()
    open_q2 = []
    for deps in shapes():
        kinds = '/'.join(f'{k}x{n}' for k, n in sorted(Counter(k for k, _ in deps).items()))
        priv = private_quartic(deps)
        out[(kinds, 'EXCLUDED_PRIVATE_VERTEX' if priv else 'OPEN')] += 1
        if not priv and any(k == 'Q2' for k, _ in deps):
            open_q2.append([(k, sorted(s)) for k, s in deps])
    rows = [dict(kinds=k, status=s, classes=n) for (k, s), n in sorted(out.items())]
    doc = dict(classes=sum(out.values()), rows=rows, open_with_doubled_quartic=open_q2)
    print(json.dumps(doc, indent=1))
    return doc


if __name__ == '__main__':
    main()
