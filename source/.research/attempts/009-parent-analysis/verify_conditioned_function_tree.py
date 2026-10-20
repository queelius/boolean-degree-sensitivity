"""Independently restrict parent tables and relabel witnesses before set replay."""
from copy import deepcopy
import numpy as np
from verify_finite_function_csp import verify_tree


def verify_from(tables,relations,tree,indices):
    assert len(tables)==len(indices)
    for table,rows in zip(tables,indices):
        assert len(rows)==len(set(rows)) and all(type(i)is int and 0<=i<len(table)for i in rows)
    restricted=[table[np.asarray(rows,dtype=np.int64)]for table,rows in zip(tables,indices)]
    inverse=[{parent:local for local,parent in enumerate(rows)}for rows in indices]
    translated=deepcopy(tree);stack=[translated]
    while stack:
        node=stack.pop();stack.extend(node.get('children',[]))
        if 'witness'in node:
            assert len(node['witness'])==len(inverse) and all(i in lookup for i,lookup in zip(node['witness'],inverse))
            node['witness']=[lookup[i]for i,lookup in zip(node['witness'],inverse)]
    return verify_tree(restricted,relations,translated)
