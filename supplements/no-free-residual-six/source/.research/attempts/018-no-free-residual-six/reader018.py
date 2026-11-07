"""Independent reader for a 018 L1 case certificate. Shares no code with
model018.py, certify018.py or the 014 encoder (adapted from the hardened
017 reader017.py, frozen in checkpoint 1533).

Claim checked: the stored rows, each equal to a necessary row of the named
case (a derivative on 13 coordinates with one negative quartic Q of weight
-m, the case's single departure, and its root link), have no common 0/1
solution. Rows are rebuilt from their keys alone:
     pair (a,b)       4 m_ab - L_ab - k_ab = 0
     triple T         L_T - 2 t_T = 0
     vertex v         K_v + P_v = 8
     constant         16 - c_hi <= K + L <= 16 - c_lo
     value X          0 <= |X| - sum m + sum t - sum l <= 2
     flag (v,(a,b,d)) t_vab + t_vbd + t_vad - l_vabd <= 2, only at an ordinary
                      non-root vertex (outside Q and the departure pair) and
                      not in part A (where ordinary links may be disconnected)
     implied_P v      P_v - 2 D_v = -4;  implied_k v  K_v + 2 D_v = 12
     degcap v         D_v <= |root link|, only in part B-ord at an ordinary
                      non-root vertex (the B-ord root has maximum ordinary degree)
with L_S = sum over D containing S of w_D l_D (w_Q = -m, else 1), k_A = -kappa_A
except the departure pair, and t_T = t + 2 t2 + 4 t4 - 1 on the four triples
inside Q (binary t elsewhere). Then the root fixings (m_0v = [v in link],
l_0F = [F a face]) and l_Q = 1 are substituted and the stored row must match
exactly. Then clause soundness and the pinned lrat-trim.
"""
import hashlib
import itertools
import json
import subprocess
import sys
from pathlib import Path

N = 13
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
    TYPES = {'none': (1, 2), 'c0': (0, 0), 'c3': (3, 3), 'pm': (1, 2), 'pp': (1, 2)}

    def __init__(self, case, mag):
        need(type(mag) is int and mag in (1, 2), 'negative magnitude must be 1 or 2')
        need(case.get('part') in ('A', 'B-ord', 'B-exc') and case.get('type') in self.TYPES, 'bad part or type')
        self.part, self.type, self.mag = case['part'], case['type'], mag
        self.c_lo, self.c_hi = self.TYPES[self.type]
        self.Q = vset(sorted(case['Q']), 4)
        need(0 not in self.Q, 'root inside Q')
        pair = case['pair']
        self.exc = {}
        if self.type in ('pm', 'pp'):
            p = vset(sorted(pair), 2)
            self.exc[p] = -2 if self.type == 'pm' else 1
            self.pair = set(p)
        else:
            need(pair == [], 'departure pair given for a pairless type')
            self.pair = set()
        if self.part == 'B-exc':
            need(self.type in ('pm', 'pp') and 0 in self.pair and len(self.pair & set(self.Q)) <= 1, 'B-exc shape')
        if self.part == 'B-ord':
            need(not self.pair or self.pair <= set(self.Q), 'B-ord pair must lie inside Q')
        self.ints = set(itertools.combinations(self.Q, 3))
        faces = [vset(sorted(f) if isinstance(f, list) else f, 3) for f in case['faces']]
        need(len(set(faces)) == len(faces) and faces, 'root link faces')
        link = sorted(set(x for f in faces for x in f))
        need(0 not in link, 'root link labels')
        self.order = len(link)
        self.fixed = {name('m', (0, v)): int(v in link) for v in range(1, N)}
        fs = set(faces)
        for f in itertools.combinations(range(1, N), 3):
            self.fixed[name('l', (0,) + f)] = int(f in fs)
        self.fixed[name('l', self.Q)] = 1

    def lw(self, q):
        return -self.mag if tuple(sorted(q)) == self.Q else 1

    def k(self, pair, acc, coef):
        p = tuple(sorted(pair))
        if p in self.exc:
            return coef * self.exc[p]
        acc[name('kappa', p)] = acc.get(name('kappa', p), 0) - coef
        return 0

    def t(self, T, acc, coef):
        """Add coef * t_T; return the constant part."""
        T = tuple(sorted(T))
        acc[name('t', T)] = acc.get(name('t', T), 0) + coef
        if T in self.ints:
            acc[name('t2', T)] = acc.get(name('t2', T), 0) + 2 * coef
            acc[name('t4', T)] = acc.get(name('t4', T), 0) + 4 * coef
            return -coef
        return 0

    def row(self, key):
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
            const = self.t(T, t, -2)
            return t, -const, -const
        if kind in ('vertex', 'constant'):
            if kind == 'vertex':
                lo = hi = 8
                on = lambda s: key[1] in s
            else:
                lo, hi = 16 - self.c_hi, 16 - self.c_lo
                on = lambda s: True
            for a in itertools.combinations(V, 2):
                if on(a):
                    const += self.k(a, t, 1)
            for q in itertools.combinations(V, 4):
                if on(q):
                    t[name('l', q)] = self.lw(q)
            return t, lo - const, hi - const
        if kind == 'value':
            X = tuple(key[1])
            for a in itertools.combinations(X, 2):
                t[name('m', a)] = -1
            for T in itertools.combinations(X, 3):
                const += self.t(T, t, 1)
            for q in itertools.combinations(X, 4):
                t[name('l', q)] = -self.lw(q)
            return t, -len(X) - const, 2 - len(X) - const
        if kind == 'flag':
            v, (a, b, d) = key[1], key[2]
            need(self.part != 'A' and v != 0 and v not in self.Q and v not in self.pair,
                 'flag row at a vertex whose link need not be a deltahedron')
            for x, y in ((a, b), (b, d), (a, d)):
                const += self.t((v, x, y), t, 1)
            t[name('l', (v, a, b, d))] = -self.lw((v, a, b, d))
            return t, -10 ** 6 - const, 2 - const
        if kind == 'degcap':
            # B-ord roots at an ordinary vertex of maximum degree: D_v <= order of the root link
            v = key[1]
            need(self.part == 'B-ord' and v != 0 and v not in self.Q and v not in self.pair, 'degree cap outside its scope')
            for a in itertools.combinations(V, 2):
                if v in a:
                    t[name('m', a)] = 1
            return t, -10 ** 6, self.order
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
    if kind in ('vertex', 'implied_P', 'implied_k', 'degcap'):
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


SIZES = {'l': 4, 'm': 2, 't': 3, 'kappa': 2, 't2': 3, 't4': 3}


def parse_name(nm):
    need(isinstance(nm, list) and len(nm) == 2 and nm[0] in SIZES, 'bad variable name')
    return (nm[0], vset(nm[1], SIZES[nm[0]]))


def pinned(pin, detail):
    """The bytes of a pinned file, read once, so the hash covers what is parsed."""
    data = Path(pin['path']).read_bytes()
    need(hashlib.sha256(data).hexdigest() == pin['sha256'], detail)
    return data


def read_cnf(text):
    clauses, cur, header = [], [], None
    for line in text.splitlines():
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
    raw = Path(cert_path).read_bytes()
    cert = json.loads(raw)
    case = Case(cert['case'], cert['magnitude'])
    variants = cert.get('variants', [[cert['case']['type'], cert['magnitude']]])
    need(isinstance(variants, list) and [cert['case']['type'], cert['magnitude']] in variants
         and len({tuple(v) for v in variants}) == len(variants), 'bad variant list')
    others = []
    for t, mg in variants:
        need(t in Case.TYPES and (t == cert['case']['type'] or {t, cert['case']['type']} <= {'none', 'c0', 'c3'}),
             'variant changes more than the constant-only type')
        if [t, mg] != [cert['case']['type'], cert['magnitude']]:
            others.append(Case(dict(cert['case'], type=t), mg))
    cnf_text = pinned(cert['cnf'], 'cnf changed').decode()
    labels = json.loads(pinned(cert['labels'], 'labels changed'))
    # lrat-trim reads the CNF and the proof by path, so for them hash and read are separate; the
    # acceptance run reads a write-protected certs/ to close that window
    need(sha(cert['proof']['path']) == cert['proof']['sha256'], 'proof changed')
    names = [parse_name(nm) for nm in cert['variables']]
    need(len(set(names)) == len(names), 'duplicate variable names')
    index = {nm: i + 1 for i, nm in enumerate(names)}
    rows = []
    for i, r in enumerate(cert['rows']):
        want, lo, hi = case.substituted(parse_key(r['key']))
        for other in others:
            need(other.substituted(parse_key(r['key'])) == (want, lo, hi), f'row {i} differs between variants')
        got = {}
        terms = []
        for nm, co in r['terms']:
            nm = parse_name(nm)
            need(nm not in got and type(co) is int and co, 'aliased or zero term')
            got[nm] = co
            terms.append((index[nm], co))
        need(got == want and (r['lo'], r['hi']) == (lo, hi), f'row {i} differs from its definition')
        rows.append((terms, lo, hi))
    nvars, clauses = read_cnf(cnf_text)
    # labels carry the certifier's row ids; map them to positions in the stored list
    pos = {r['id']: i for i, r in enumerate(cert['rows'])}
    need(len(pos) == len(cert['rows']), 'duplicate row ids')
    labels = [[v, pos[r], k, s] for v, r, k, s in labels]
    check_clauses(rows, len(names), nvars, clauses, labels)
    need(sha(LRAT_TRIM) == LRAT_TRIM_SHA, 'checker changed')
    p = subprocess.run([str(LRAT_TRIM), '--forward', '--no-trim', cert['cnf']['path'], cert['proof']['path']],
                       capture_output=True, text=True)
    ok = p.returncode == 20 and any(line.strip() == 's VERIFIED' for line in p.stdout.splitlines())
    # case and cert_sha256 are those of the bytes checked above, for the assembly to bind
    return dict(part=case.part, type=case.type, Q=list(case.Q), magnitude=case.mag, variants=variants, rows=len(rows), clauses=len(clauses), clause_soundness='PASS',
                case=cert['case'], cert_sha256=hashlib.sha256(raw).hexdigest(),
                files={k: dict(path=cert[k]['path'], sha256=cert[k]['sha256']) for k in ('cnf', 'labels', 'proof')},
                lrat_trim_exit=p.returncode, verdict='CASE_ROWS_INFEASIBLE_VERIFIED' if ok else 'NOT_VERIFIED')


if __name__ == '__main__':
    r = read(sys.argv[1])
    print(json.dumps(r))
    sys.exit(0 if r['verdict'] == 'CASE_ROWS_INFEASIBLE_VERIFIED' else 1)
