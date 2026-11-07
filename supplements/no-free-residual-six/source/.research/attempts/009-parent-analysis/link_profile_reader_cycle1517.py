"""Independent literal neighbor-set profile computation; no1516 imports."""
from collections import Counter
import json


def require(condition, message):
    if not condition:
        raise ValueError(message)


def exact(first, second):
    return json.dumps(first,sort_keys=True,separators=(',',':'),allow_nan=False) == \
           json.dumps(second,sort_keys=True,separators=(',',':'),allow_nan=False)


def connected(adjacency):
    require(bool(adjacency), 'nonempty adjacency')
    seen = set()
    todo = [next(iter(adjacency))]
    while todo:
        v = todo.pop()
        if v not in seen:
            seen.add(v)
            todo.extend(adjacency[v] - seen)
    return seen == set(adjacency)


def classify(degrees):
    counts = Counter(degrees)
    if set(counts) <= {4, 5}:
        return 'ordinary'
    if counts[3] == 1 and set(counts) <= {3, 4, 5}:
        return 'positive_tip'
    if counts[6] == 1 and set(counts) <= {4, 5, 6}:
        return 'negative_tip'
    return None


def analyze(n, face_masks):
    require(type(n) is int and n >= 4, 'integer order')
    require(type(face_masks) is list and face_masks and
            all(type(f) is int and 0 < f < 1 << n and f.bit_count() == 3
                for f in face_masks), 'literal triangular masks')
    require(len(face_masks) == len(set(face_masks)), 'distinct triangles')
    neighbors = {v:set() for v in range(n)}
    links = {v:{} for v in range(n)}
    edge_cofaces = Counter()
    for f in face_masks:
        a,b,c = (v for v in range(n) if f >> v & 1)
        for x,y in ((a,b),(a,c),(b,c)):
            neighbors[x].add(y)
            neighbors[y].add(x)
            edge_cofaces[(x,y)] += 1
        for v,x,y in ((a,b,c),(b,a,c),(c,a,b)):
            links[v].setdefault(x,set()).add(y)
            links[v].setdefault(y,set()).add(x)
    require(all(neighbors.values()) and connected(neighbors), 'all vertices used and connected')
    require(all(count == 2 for count in edge_cofaces.values()), 'two triangles per edge')
    require(n-len(edge_cofaces)+len(face_masks) == 2, 'Euler two')
    for v in range(n):
        require(set(links[v]) == neighbors[v] and
                all(len(adjacent) == 2 for adjacent in links[v].values()) and
                connected(links[v]), 'connected cyclic vertex link')
    degrees = [len(neighbors[v]) for v in range(n)]
    return degrees, classify(degrees)
