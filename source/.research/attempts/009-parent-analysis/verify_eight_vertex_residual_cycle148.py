"""Independently reconstruct every bounded eight-vertex residual in the pilot."""
from pathlib import Path
from itertools import combinations
from collections import Counter
from time import monotonic
import hashlib,json
import numpy as np
from compose_class40_same_b_acceptance import Bindings
from independent_small_link_cycles import literal_bounded_high_cycles


def run():
    start=monotonic();b=Bindings();path=Path('eight-vertex-residual-pilot-cycle148.json');source=b.read(path)
    assert source['status']=='MEASURED_EIGHT_VERTEX_RESIDUAL_PILOT'
    high=source['vertices'];assert high==list(range(8)) and source['maximum']==[7,7,7,6,5,5,5,5]
    assert source['maximum_faces']==14 and source['anchor']==7
    data=Path(source['data']['path']);assert b.bind(data)==source['data']
    assert hashlib.sha256(Path('small_link_high_cycles.py').read_bytes()).hexdigest()==source['kernel_sha256']
    assert hashlib.sha256(Path('benchmark_eight_vertex_residual_cycle148.py').read_bytes()).hexdigest()==source['script_sha256']
    triangles=[sum(1<<v for v in t) for t in combinations(high,3)]
    found=list(literal_bounded_high_cycles(high,4,source['maximum'],14,triangles))
    assert len(found)==len(set(found));found.sort()
    saved=np.load(data,allow_pickle=False);assert saved.dtype==np.uint64 and saved.tolist()==found
    assert source['cycles']==len(found) and {int(k):v for k,v in source['weights'].items()}==dict(Counter(q.bit_count() for q in found))
    for name in ('verify_eight_vertex_residual_cycle148.py','independent_small_link_cycles.py',
                 'test_independent_small_link_cycles.py','small_link_completeness_cycle139.md',
                 'small_link_high_cycles.py','benchmark_eight_vertex_residual_cycle148.py'):b.bind(Path(name))
    result=dict(status='INDEPENDENTLY_VERIFIED_EIGHT_VERTEX_RESIDUAL_CATALOG',global_status='UNRESOLVED',
        source=b.bind(path),data=source['data'],vertices=high,maximum=source['maximum'],maximum_faces=14,
        cycles=len(found),independent_anchor=4,seconds=monotonic()-start,accepted_parent_exclusions=0,
        files=[dict(path=p,sha256=d) for p,d in sorted(b.files.items())])
    output=Path('eight-vertex-residual-independent-manifest-cycle148.json');assert not output.exists()
    output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True)


if __name__=='__main__':run()
