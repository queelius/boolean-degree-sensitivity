"""Independent ordinary-set replay of pointwise and binary-candidate proofs."""
import numpy as np


def verify_tree(tables,relations,binary_relations,tree):
    assert tables and all(t.ndim==2 and np.issubdtype(t.dtype,np.integer) for t in tables)
    points=tables[0].shape[1];n=len(tables)
    assert points>0 and len(relations)==points and all(t.shape[1]==points for t in tables)
    allowed=[set(tuple(map(int,row)) for row in relation) for relation in relations]
    assert all(len(row)==n for relation in allowed for row in relation)
    binary=[]
    for relation in binary_relations:
        i,j=relation.left,relation.right
        assert type(i) is int and type(j) is int and i!=j and 0<=i<n and 0<=j<n
        pairs=relation.allowed
        assert pairs.ndim==2 and pairs.shape[1]==2 and np.issubdtype(pairs.dtype,np.integer)
        left=[set() for _ in range(len(tables[i]))];right=[set() for _ in range(len(tables[j]))]
        for a,c in pairs:
            a,c=int(a),int(c);assert 0<=a<len(left) and 0<=c<len(right)
            left[a].add(c);right[c].add(a)
        binary.append((i,j,left,right))
    def point_choices(domains,x):
        assert type(x) is int and 0<=x<points
        values=[{int(table[i,x]) for i in domain} for table,domain in zip(tables,domains)]
        return [r for r in allowed[x] if all(v in choices for v,choices in zip(r,values))]
    def binary_reduction(domains,k):
        assert type(k) is int and 0<=k<len(binary)
        i,j,left,right=binary[k]
        a={u for u in domains[i] if left[u] & domains[j]}
        c={v for v in domains[j] if right[v] & domains[i]}
        return i,j,a,c
    def replay(node,domains):
        if node['kind']=='LIMIT':
            assert set(node)=={'kind'};return 'UNKNOWN'
        for event in node['propagation']:
            updated=list(domains)
            if event['kind']=='point':
                assert set(event)=={'kind','point'};x=event['point'];live=point_choices(domains,x);assert live
                for j,(table,domain) in enumerate(zip(tables,domains)):
                    options={r[j] for r in live};updated[j]={i for i in domain if int(table[i,x]) in options}
            else:
                assert event['kind']=='binary' and set(event)=={'kind','relation'}
                i,j,a,c=binary_reduction(domains,event['relation']);updated[i]=a;updated[j]=c
            assert all(updated) and updated!=domains;domains=updated
        if 'split' in node:
            split=node['split'];j,x,value=split['variable'],split['point'],split['value']
            assert type(j) is int and 0<=j<n and type(x) is int and 0<=x<points and type(value) is int
            chosen={i for i in domains[j] if int(tables[j][i,x])==value}
            assert chosen and chosen!=domains[j] and len(node['children'])==2
            left=list(domains);right=list(domains);left[j]=chosen;right[j]=domains[j]-chosen
            statuses=[replay(node['children'][0],left),replay(node['children'][1],right)]
            result='SAT' if 'SAT' in statuses else ('UNSAT' if statuses==['UNSAT','UNSAT'] else 'UNKNOWN')
            assert node['kind']==result;return result
        if node['kind']=='UNSAT':
            bad=node['contradiction_point']
            if bad['kind']=='empty':assert set(bad)=={'kind'} and any(not d for d in domains)
            elif bad['kind']=='point':
                assert set(bad)=={'kind','point'} and not point_choices(domains,bad['point'])
            else:
                assert bad['kind']=='binary' and set(bad)=={'kind','relation'}
                _,_,a,c=binary_reduction(domains,bad['relation']);assert not a and not c
            return 'UNSAT'
        assert node['kind']=='SAT' and all(len(d)==1 for d in domains)
        witness=[next(iter(d)) for d in domains];assert node['witness']==witness
        assert all(tuple(int(table[i,x]) for table,i in zip(tables,witness)) in allowed[x] for x in range(points))
        assert all(witness[j] in left[witness[i]] for i,j,left,_ in binary)
        return 'SAT'
    return replay(tree,[set(range(len(t))) for t in tables])
