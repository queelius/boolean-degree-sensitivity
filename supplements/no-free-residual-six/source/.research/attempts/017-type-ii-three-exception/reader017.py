"""Independent reader for a 017 case certificate. Shares no code with model.py,
certify017.py or the 014 encoder.

Claim checked: the rows R stored in the certificate, each equal to a
necessary row of the named case at every constant listed in `constants`,
have no common 0/1 solution; hence the case (shape placement, root link)
has no ternary derivative at any of those constants.

1. Rebuild every stored row from its key alone, from the definitions:
     pair (a,b)       4 m_ab - sum_{q > ab} l_q - k_ab = 0
     triple T         sum_{q > T} l_q - 2 t_T = 0
     vertex v         sum_{A ni v} k_A + sum_{q ni v} l_q = 8
     constant         sum_A k_A + sum_q l_q = 16 - c
     value X          0 <= |X| - sum_{A < X} m_A + sum_{T < X} t_T - sum_{q < X} l_q <= 2
     flag (v,(a,b,d)) t_vab + t_vbd + t_vad - l_vabd - sum_y l_vyab <= 2 over the
                      +1 partners y of v outside abd, only at a non-root vertex
                      whose type is in NEAR_FLAG_TYPES (all catalog links near-flag)
     implied_P v      sum_{q ni v} l_q - 2 sum_{A ni v} m_A = -4
     implied_k v      sum_{A ni v} k_A + 2 sum_{A ni v} m_A = 12
   with k_A = -kappa_A for baseline pairs and the case's value for exceptions;
   then substitute the root fixings recomputed from the root link (m_0v = [v in
   link], l_{0 F} = [F a face]) and require exact equality with the stored row.
2. Clause soundness of the CNF for those rows (decision-diagram labels), as in
   the 014 reader, re-implemented here.
3. The pinned lrat-trim on exactly these files: exit 20 and 's VERIFIED'.
It does not check that the case belongs to the cover (cover_reader.py) or the
lemmas behind the flag rows and the root catalog (written notes).
"""
import hashlib
import itertools
import json
import subprocess
import sys
from pathlib import Path

N = 13
NEAR_FLAG_TYPES = {(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (2, 0)}
LRAT_TRIM = Path(__file__).resolve().parents[1] / '006-solver-resume/lrat-trim/lrat-trim'
LRAT_TRIM_SHA = '179d041f645a98d51d3ca6dbbe4950806ad8eceb54c9a762f54e7acee154f8df'


class ReaderError(Exception):
    pass


def need(cond, detail):
    if not cond:
        raise ReaderError(detail)


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def name(kind, s):
    return (kind, tuple(sorted(s)))


class Case:
    def __init__(self, case, c):
        need(type(c) is int and c in (1, 2), 'constant outside Type II')
        self.c = c
        self.exc = {}
        for item in case['exceptions']:
            need(isinstance(item, list) and len(item) == 2, 'bad exception')
            p, k = item
            p = vset(sorted(p) if isinstance(p, list) else p, 2)
            need(type(k) is int and k in (-2, 1) and p not in self.exc, 'bad exception')
            self.exc[p] = k
        self.doubled = [vset(sorted(q) if isinstance(q, list) else q, 4) for q in case.get('doubled', [])]
        minus = [p for p, k in self.exc.items() if k == -2]
        if self.doubled:
            # shape 1: -2 on two disjoint pairs whose union is the doubled quartic (SHAPE1.md)
            need(len(self.doubled) == 1 and len(self.exc) == 2 and len(minus) == 2
                 and tuple(sorted(set(minus[0]) | set(minus[1]))) == self.doubled[0], 'not shape 1')
            self.wides = {T for T in itertools.combinations(self.doubled[0], 3)}
            self.special = set(self.doubled[0])
        else:
            need(len(self.exc) == 3, 'three distinct exceptional pairs')
            tri = tuple(sorted(set(x for p in minus for x in p)))
            # Lemma 1: only the all -2 exceptional triangle may lie in four tetrahedra
            self.wides = {tri} if len(minus) == 3 and len(tri) == 3 else set()
            self.special = set(tri) if self.wides else set()
        faces = [vset(sorted(f) if isinstance(f, list) else f, 3) for f in case['faces']]
        need(len(set(faces)) == len(faces) and faces, 'root link faces')
        link = sorted(set(x for f in faces for x in f))
        need(0 not in link, 'root link labels')
        self.fixed = {name('m', (0, v)): int(v in link) for v in range(1, N)}
        fs = set(faces)
        for f in itertools.combinations(range(1, N), 3):
            self.fixed[name('l', (0,) + f)] = int(f in fs)
        for q in self.doubled:
            need(0 not in q, 'root inside the doubled quartic')
            self.fixed[name('l', q)] = 1          # l_q = 2: coefficient 2 below, variable fixed to 1

    def lw(self, q):
        return 2 if tuple(sorted(q)) in self.doubled else 1

    def k(self, pair, acc, coef):
        """Add coef * k_pair to acc; return the constant part."""
        p = tuple(sorted(pair))
        if p in self.exc:
            return coef * self.exc[p]
        acc[name('kappa', p)] = acc.get(name('kappa', p), 0) - coef
        return 0

    def vtype(self, v):
        return (sum(1 for p, k in self.exc.items() if v in p and k == -2),
                sum(1 for p, k in self.exc.items() if v in p and k == 1))

    def row(self, key):
        """(terms dict, lo, hi) of the full row named by key."""
        kind, t, const = key[0], {}, 0
        V = range(N)
        if kind == 'pair':
            a, b = key[1]
            t[name('m', (a, b))] = 4
            for q in itertools.combinations(V, 4):
                if a in q and b in q:
                    t[name('l', q)] = -self.lw(q)
            const = self.k((a, b), t, -1)
            return t, -const, -const
        if kind == 'triple':
            T = set(key[1])
            for q in itertools.combinations(V, 4):
                if T <= set(q):
                    t[name('l', q)] = self.lw(q)
            t[name('t', T)] = -2
            if tuple(sorted(T)) in self.wides:
                t[name('t2', T)] = -2
            return t, 0, 0
        if kind in ('vertex', 'constant'):
            rhs = 8 if kind == 'vertex' else 16 - self.c
            on = (lambda s: key[1] in s) if kind == 'vertex' else (lambda s: True)
            for a in itertools.combinations(V, 2):
                if on(a):
                    rhs -= self.k(a, t, 1)
            for q in itertools.combinations(V, 4):
                if on(q):
                    t[name('l', q)] = self.lw(q)
            return t, rhs, rhs
        if kind == 'value':
            X = tuple(key[1])
            need(len(set(X)) == len(X) >= 2 and all(0 <= x < N for x in X), 'bad value set')
            for a in itertools.combinations(sorted(X), 2):
                t[name('m', a)] = -1
            for T in itertools.combinations(sorted(X), 3):
                t[name('t', T)] = 1
                if T in self.wides:
                    t[name('t2', T)] = 1   # cubic coefficient is -(t + t2)
            for q in itertools.combinations(sorted(X), 4):
                t[name('l', q)] = -self.lw(q)
            return t, -len(X), 2 - len(X)
        if kind == 'flag':
            v, (a, b, d) = key[1], key[2]
            need(v != 0 and self.vtype(v) in NEAR_FLAG_TYPES and v not in self.special,
                 'flag row at a vertex whose link need not be near-flag')
            need(len({v, a, b, d}) == 4, 'bad flag triple')
            for x, y in ((a, b), (b, d), (a, d)):
                t[name('t', (v, x, y))] = 1
            t[name('l', (v, a, b, d))] = -1
            plus = [x for p, k in self.exc.items() if k == 1 and v in p for x in p if x != v]
            relax = [y for y in plus if y not in (a, b, d)]
            for y in relax:
                t[name('l', (v, y, a, b))] = -1
            return t, -3 - len(relax), 2
        if kind == 'implied_P':
            v = key[1]
            for q in itertools.combinations(V, 4):
                if v in q:
                    t[name('l', q)] = self.lw(q)
            for a in itertools.combinations(V, 2):
                if v in a:
                    t[name('m', a)] = -2
            return t, -4, -4
        if kind == 'implied_k':
            v, rhs = key[1], 12
            for a in itertools.combinations(V, 2):
                if v in a:
                    rhs -= self.k(a, t, 1)
                    t[name('m', a)] = t.get(name('m', a), 0) + 2
            return t, rhs, rhs
        raise ReaderError('unknown row kind ' + str(kind))

    def substituted(self, key):
        t, lo, hi = self.row(key)
        shift = sum(co * self.fixed[nm] for nm, co in t.items() if nm in self.fixed)
        return {nm: co for nm, co in t.items() if nm not in self.fixed and co}, lo - shift, hi - shift


def vertex(x):
    need(type(x) is int and 0 <= x < N, f'not a coordinate: {x!r}')
    return x


def vset(xs, size=None, min_size=None):
    need(isinstance(xs, list), 'vertex set must be a list')
    out = tuple(vertex(x) for x in xs)
    need(len(set(out)) == len(out) and list(out) == sorted(out), 'vertex set must be distinct and sorted')
    need(size is None or len(out) == size, 'wrong vertex-set size')
    need(min_size is None or len(out) >= min_size, 'vertex set too small')
    return out


def parse_key(k):
    """Strict schema: every vertex an int in 0..12, sets distinct and sorted, exact arity."""
    need(isinstance(k, list) and k and isinstance(k[0], str), 'bad key')
    kind = k[0]
    if kind in ('pair', 'triple'):
        need(len(k) == 2, 'bad key arity')
        return (kind, vset(k[1], 2 if kind == 'pair' else 3))
    if kind in ('vertex', 'implied_P', 'implied_k'):
        need(len(k) == 2, 'bad key arity')
        return (kind, vertex(k[1]))
    if kind == 'constant':
        need(len(k) == 1, 'bad key arity')
        return ('constant',)
    if kind == 'value':
        need(len(k) == 2, 'bad key arity')
        return ('value', vset(k[1], min_size=2))
    if kind == 'flag':
        need(len(k) == 3, 'bad key arity')
        v, abd = vertex(k[1]), vset(k[2], 3)
        need(v not in abd, 'flag triple contains its vertex')
        return ('flag', v, abd)
    raise ReaderError('unknown key ' + json.dumps(k))


SIZES = {'l': 4, 'm': 2, 't': 3, 'kappa': 2, 't2': 3}


def parse_name(nm):
    need(isinstance(nm, list) and len(nm) == 2 and nm[0] in SIZES, 'bad variable name')
    return (nm[0], vset(nm[1], SIZES[nm[0]]))


def read_cnf(path):
    clauses, cur, header = [], [], None
    for line in open(path):
        t = line.split()
        if not t or t[0] == 'c':
            continue
        if t[0] == 'p':
            header = (int(t[2]), int(t[3]))
            continue
        for x in map(int, t):
            if x == 0:
                clauses.append(cur)
                cur = []
            else:
                cur.append(x)
    need(not cur and header is not None and header[1] == len(clauses), 'malformed CNF')
    return header[0], clauses


def check_clauses(rows, nbase, nvars, clauses, labels):
    lab = {}
    for v, r, k, s in labels:
        need(nbase < v <= nvars and v not in lab and 0 <= r < len(rows) and 0 <= k <= len(rows[r][0]), f'bad label {v}')
        lab[v] = (r, k, s)
    rest = []
    for terms, lo, hi in rows:
        mn, mx = [0] * (len(terms) + 1), [0] * (len(terms) + 1)
        for k in range(len(terms) - 1, -1, -1):
            mn[k] = mn[k + 1] + min(terms[k][1], 0)
            mx[k] = mx[k + 1] + max(terms[k][1], 0)
        rest.append((mn, mx))
    for cl in clauses:
        if not cl:
            need(any(rest[r][0][0] > rows[r][2] or rest[r][1][0] < rows[r][1] for r in range(len(rows))),
                 'unjustified empty clause')
            continue
        if len(cl) == 1 and cl[0] in lab and lab[cl[0]][1:] == (0, 0):
            continue
        need(len(cl) in (2, 3) and cl[0] < 0 and -cl[0] in lab, f'unrecognized clause {cl[:4]}')
        r, k, s = lab[-cl[0]]
        terms, lo, hi = rows[r]
        need(k < len(terms), 'step past end')
        v, c = terms[k]
        lit = -cl[1]
        need(abs(lit) == v, 'clause literal is not term k of its row')
        s2 = s + (c if lit > 0 else 0)
        if len(cl) == 3:
            need(cl[2] in lab and lab[cl[2]] == (r, k + 1, s2), 'bad step clause')
            continue
        mn, mx = rest[r]
        need(s2 + mn[k + 1] > hi or s2 + mx[k + 1] < lo, 'unjustified dead-end clause')


def read(cert_path):
    cert = json.loads(Path(cert_path).read_text())
    constants = cert.get('constants', [cert['c']])
    need(constants and len(set(constants)) == len(constants) and cert['c'] in constants, 'bad constant list')
    cases = [Case(cert['case'], c) for c in constants]
    for k in ('cnf', 'labels', 'proof'):
        need(sha(cert[k]['path']) == cert[k]['sha256'], k + ' changed')
    names = [parse_name(nm) for nm in cert['variables']]
    need(len(set(names)) == len(names), 'duplicate variable names')
    index = {nm: i + 1 for i, nm in enumerate(names)}
    rows = []
    for i, r in enumerate(cert['rows']):
        want, lo, hi = cases[0].substituted(parse_key(r['key']))
        for other in cases[1:]:
            need(other.substituted(parse_key(r['key'])) == (want, lo, hi), f'row {i} depends on the constant')
        got = {}
        terms = []
        for nm, co in r['terms']:
            nm = parse_name(nm)
            need(nm not in got and type(co) is int and co, 'aliased or zero term')
            got[nm] = co
            terms.append((index[nm], co))
        need(got == want and (r['lo'], r['hi']) == (lo, hi), f'row {i} differs from its definition')
        rows.append((terms, lo, hi))
    nvars, clauses = read_cnf(cert['cnf']['path'])
    labels = json.loads(Path(cert['labels']['path']).read_text())
    # labels carry the certifier's row ids; map them to positions in the stored list
    pos = {r['id']: i for i, r in enumerate(cert['rows'])}
    need(len(pos) == len(cert['rows']), 'duplicate row ids')
    labels = [[v, pos[r], k, s] for v, r, k, s in labels]
    check_clauses(rows, len(names), nvars, clauses, labels)
    need(sha(LRAT_TRIM) == LRAT_TRIM_SHA, 'checker changed')
    p = subprocess.run([str(LRAT_TRIM), '--forward', '--no-trim', cert['cnf']['path'], cert['proof']['path']],
                       capture_output=True, text=True)
    ok = p.returncode == 20 and any(line.strip() == 's VERIFIED' for line in p.stdout.splitlines())
    return dict(case=cert['case']['exceptions'], root_order=cert['case']['order'], root_index=cert['case']['root_index'],
                constants=constants, rows=len(rows), clauses=len(clauses), clause_soundness='PASS',
                lrat_trim_exit=p.returncode, verdict='CASE_ROWS_INFEASIBLE_VERIFIED' if ok else 'NOT_VERIFIED')


if __name__ == '__main__':
    r = read(sys.argv[1])
    print(json.dumps(r))
    sys.exit(0 if r['verdict'] == 'CASE_ROWS_INFEASIBLE_VERIFIED' else 1)
