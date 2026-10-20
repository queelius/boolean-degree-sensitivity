"""Independent degree-mask enumeration and scope audit for the elementary Euler proof."""
from argparse import ArgumentParser
from itertools import product
from collections import Counter
from pathlib import Path
import json
from compose_class40_same_b_acceptance import Bindings
from gzip_certificate_io import read_certificate
from cubic_partial_scalar import PartialScalarValues

H=Path(__file__).resolve().parent


def run(output):
    b=Bindings();source_path=H/'parent00-negative13-euler-profiles-cycle112.json';source=b.read(source_path)
    assert source['status']=='PROPOSED_COMPLETE_PARENT00_NEGATIVE13_EULER_EXCLUSION' and source['negative']==[13] and source['core_mask']==3
    frontier=b.read(source['frontier']['path'],source['frontier']['sha256']);assert frontier['status']=='ACCEPTED_PARENT00_CUBIC_POSITION_FRONTIER'
    assert source['geometry']==frontier['geometry'] and source['parent']==frontier['parent']
    assert dict(index=source['index'],negative=[13]) in frontier['remaining'];parent=read_certificate(b,source['parent'])
    rows=b.read(H/'two-positive-pair-embeddings.json','0edddced95caf2082e8bf1f0f7c56fdf17f7e4d032fc1f34a14306e82ea6476b')['domain']['rows'];values=PartialScalarValues(rows,source['geometry']).allowed(parent['domains'],3)
    singletons=[values[1<<i] for i in range(10)];assert source['origin']==values[0]==[4] and source['singleton_values']==singletons
    expected={};options=[set() for i in range(10)]
    for flags in range(1024):
        linear=tuple((flags>>i)&1 for i in range(10));Q=sum(linear);P=Q+6
        for selected_values in product(*singletons):
            degrees=tuple((4-selected_values[i])//2+2*int(bool(13>>i&1))+linear[i] for i in range(10))
            for i,d in enumerate(degrees):
                if 0<=d<=36 and d not in (1,2):options[i].add((d,linear[i]))
            if Q%2 or sum(degrees)!=3*P or any(d<0 or d>36 or d in (1,2) for d in degrees):continue
            expected[degrees,linear]=dict(linear_count=Q,positive_count=P)
    assert source['degree_options']==[[list(p) for p in sorted(s)] for s in options]
    actual={(tuple(r['degrees']),tuple(r['linear'])):r for r in source['profiles']};assert len(actual)==len(source['profiles'])==len(expected)==25 and set(actual)==set(expected)
    counts=Counter()
    for key,parameters in expected.items():
        record=actual[key];assert all(record[k]==v for k,v in parameters.items());degrees,linear=key
        V=sum(d>0 for d in degrees);F=parameters['positive_count'];assert max(degrees)<=5 and F%2==0
        chi=V-F//2;assert chi==3 and F in (10,12)
        assert record['obstruction']==dict(vertices=V,faces=F,euler_characteristic=3,minimum_faces=14,excluded=True)
        counts[V,F,parameters['linear_count']]+=1
    cover=read_certificate(b,frontier['cover']);assert cover['parent']==source['parent'] and cover['representatives'][source['index']]['pattern']==[13]
    literals=[r['pattern'] for r in cover['maps'] if r['representative']==source['index']]
    for name in ('verify_parent00_euler.py','parent00-negative13-euler-proof-cycle112.md','test_cubic_degree_profiles.py','signed-divisibility-criterion-cycle107.md'):b.bind(H/name)
    result=dict(status='INDEPENDENTLY_VERIFIED_PARENT00_NEGATIVE13_EULER_EXCLUSION',global_status='UNRESOLVED',source=b.bind(source_path),
        frontier=source['frontier'],geometry=source['geometry'],parent=source['parent'],core_mask=3,index=source['index'],negative=[13],
        profiles_checked=len(expected),profile_counts=[dict(vertices=k[0],faces=k[1],linear_count=k[2],profiles=v) for k,v in sorted(counts.items())],
        excluded_literal_positions=literals,negative_position_excluded=True,whole_parent_excluded=False,
        files=[dict(path=p,sha256=d) for p,d in sorted(b.files.items())])
    assert not output.exists();output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(dict(profiles=len(expected),excluded_literals=literals)),flush=True)


if __name__=='__main__':
    p=ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);run(p.parse_args().output)
