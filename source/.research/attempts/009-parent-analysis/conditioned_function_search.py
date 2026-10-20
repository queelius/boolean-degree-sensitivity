"""Reuse immutable relation partitions across explicitly conditioned searches."""


def search_from(solver,domains,*,max_nodes):
    original=solver.initial
    assert len(domains)==len(original)
    assert all(type(d)is int and d>=0 and d&~base==0 for d,base in zip(domains,original))
    try:
        solver.initial=tuple(domains)
        return solver.search(max_nodes)
    finally:
        solver.initial=original
