"""Positive controls for no-free derivative lemmas, from the 012 n = 13 witnesses.

For every self-dual degree-5 witness on 13 variables (attempt 012, truth
tables verified there), compute k_S = 16 hat g(S) for g = 1 - 2f (integral
by degree 5), and at every coordinate u lying in exactly one negative
quintic, the derivative data: 16 Delta_u f = sum over S containing u of
k_S chi_{S - u}, i.e. constant k_u, pair numerators k_{uab}, quartic
numerators k_{uabcd} (exactly one negative). These derivatives are real: any
proposed local lemma about one-negative-quartic derivatives whose argument
does not use the coordinate count must not exclude them (they live on 12
coordinates rather than 13).
"""
import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
W = HERE.parent / '012-n13-probe'


def spectrum(tt, n):
    h = 1 - 2 * np.array(tt, dtype=np.int64)
    step = 1
    while step < len(h):
        h = h.reshape(-1, 2 * step)
        a, b = h[:, :step].copy(), h[:, step:].copy()
        h = np.concatenate([a + b, a - b], axis=1).reshape(-1)
        step *= 2
    k = {}
    for S in np.nonzero(h)[0]:
        v = 16 * int(h[S])
        if v % (1 << n):
            raise SystemExit('non-integral scaled coefficient')
        k[int(S)] = v >> n if v >= 0 else -((-v) >> n)
    return k


def bits(S):
    return [i for i in range(13) if S >> i & 1]


def explicit(k, u):
    """All coefficients of 16 Delta_u f on the other 12 coordinates, relabelled 0..11."""
    lab = {x: i for i, x in enumerate(x for x in range(13) if x != u)}
    pairs, quarts = [], []
    for S, v in k.items():
        if S >> u & 1 and bin(S).count('1') in (3, 5):
            rest = sorted(lab[x] for x in bits(S) if x != u)
            (pairs if len(rest) == 2 else quarts).append([rest, v])
    return dict(constant=k.get(1 << u, 0), pairs=sorted(pairs), quartics=sorted(quarts))


def derivative(k, u):
    pairs = Counter(v for S, v in k.items() if S >> u & 1 and bin(S).count('1') == 3)
    quarts = Counter(v for S, v in k.items() if S >> u & 1 and bin(S).count('1') == 5)
    return dict(constant=k.get(1 << u, 0), pair_numerators=dict(sorted(pairs.items())),
                quartic_numerators=dict(sorted(quarts.items())))


def main(out):
    idx = json.loads((W / 'witness-index.json').read_text())
    rows = []
    for w in idx:
        if w['n'] != 13 or not w['self_dual']:
            continue
        d = json.loads((W / w['file']).read_text())
        k = spectrum(d['truth_table'], 13)
        neg5 = [S for S, v in k.items() if bin(S).count('1') == 5 and v < 0]
        delta = [sum(1 for S in neg5 if S >> u & 1) for u in range(13)]
        for u in range(13):
            if delta[u] == 1:
                (Q,) = [S for S in neg5 if S >> u & 1]
                rows.append(dict(witness=w['file'], u=u, negative_quintic=bits(Q), magnitude=-k[Q],
                                 derivative=derivative(k, u), explicit=explicit(k, u)))
    doc = dict(status='N13_ONE_NEGATIVE_QUARTIC_CONTROLS', witnesses_scanned=sum(
        1 for w in idx if w['n'] == 13 and w['self_dual']), controls=rows)
    Path(out).write_text(json.dumps(doc, indent=1) + '\n')
    for r in rows:
        print(r['witness'].split('/')[-1], r['u'], r['magnitude'], json.dumps(r['derivative']))
    return doc


if __name__ == '__main__':
    main(sys.argv[1])
