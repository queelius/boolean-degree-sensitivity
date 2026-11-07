"""CNF encoding of integer linear rows lo <= sum c_i x_i <= hi over Boolean x.

Each row becomes a decision diagram on partial sums. Node (k, s) means "the
first k terms sum to s and the row can still be satisfied". With
minrest/maxrest the extreme sums of terms k.., a node is
  FALSE if s + minrest > hi or s + maxrest < lo,
  TRUE  if lo <= s + minrest and s + maxrest <= hi,
otherwise it branches on x_k to (k+1, s + c_k) and (k+1, s). Clauses
(one direction suffices):
  root;   node & x_k -> high;   node & ~x_k -> low;
where an edge into FALSE becomes (~node | ~x_k) or (~node | x_k), and an
edge into TRUE adds nothing. Any model restricted to x satisfies the row
(follow the path: every node on it is forced true, FALSE is never reached).
Conversely a satisfying x extends by setting each node to its truth value.
"""


class CNF:
    def __init__(self, nvars):
        self.nvars = nvars
        self.clauses = []
        self.labels = {}      # aux var -> (tag, k, s): 'first k terms of row tag sum to s'

    def new(self):
        self.nvars += 1
        return self.nvars

    def add_row(self, terms, lo, hi, tag=None):
        """terms: [(var (1-based), coeff)]. Returns number of aux vars added."""
        start = self.nvars
        n = len(terms)
        minrest = [0] * (n + 1); maxrest = [0] * (n + 1)
        for k in range(n - 1, -1, -1):
            c = terms[k][1]
            minrest[k] = minrest[k + 1] + min(c, 0)
            maxrest[k] = maxrest[k + 1] + max(c, 0)

        def kind(k, s):
            if s + minrest[k] > hi or s + maxrest[k] < lo:
                return False
            if lo <= s + minrest[k] and s + maxrest[k] <= hi:
                return True
            return None

        root = kind(0, 0)
        if root is True:
            return 0
        if root is False:
            self.clauses.append([])          # row unsatisfiable by itself
            return 0
        node = {(0, 0): self.new()}
        self.labels[node[(0, 0)]] = (tag, 0, 0)
        self.clauses.append([node[(0, 0)]])
        frontier = [0]
        for k in range(n):
            v, c = terms[k]
            nxt = set()
            for s in frontier:
                me = node[(k, s)]
                for lit, child in ((v, s + c), (-v, s)):
                    t = kind(k + 1, child)
                    if t is True:
                        continue
                    if t is False:
                        self.clauses.append([-me, -lit])
                        continue
                    if (k + 1, child) not in node:
                        node[(k + 1, child)] = self.new()
                        self.labels[node[(k + 1, child)]] = (tag, k + 1, child)
                        nxt.add(child)
                    self.clauses.append([-me, -lit, node[(k + 1, child)]])
            frontier = sorted(nxt)
        return self.nvars - start

    def dimacs(self):
        out = [f'p cnf {self.nvars} {len(self.clauses)}']
        out += [' '.join(map(str, c + [0])) for c in self.clauses]
        return '\n'.join(out) + '\n'
