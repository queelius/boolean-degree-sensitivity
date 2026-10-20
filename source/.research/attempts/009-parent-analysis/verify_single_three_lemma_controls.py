"""Exhaustive local checks for the degree-(3,5^9) mathematical obstruction."""
from pathlib import Path
from itertools import combinations
from collections import Counter
from functools import reduce
from operator import xor
import json
from compose_class40_same_b_acceptance import Bindings
from verify_parent00_cubic_cycles import independent_cycles


def run():
    b=Bindings();vertices=list(range(6));triangles=[sum(1<<v for v in t) for t in combinations(vertices,3)]
    codes=independent_cycles(vertices,triangles);counts=Counter()
    for code in codes:
        degrees=tuple(sorted(sum(bool(q>>v&1) and bool(code>>j&1) for j,q in enumerate(triangles)) for v in vertices))
        counts[degrees]+=1
    assert len(codes)==1024 and counts[(3,3,3,5,5,5)]==0
    assert counts[(4,4,4,4,4,4)]>0 and counts[(5,5,5,5,5,5)]>0
    edges=[(1<<a)|(1<<c) for a,c in combinations(range(9),2)];links={}
    for size in (3,4,5):
        count=0
        for chosen in combinations(edges,size):
            if reduce(xor,chosen,0):continue
            degrees=[sum(bool(e>>v&1) for e in chosen) for v in range(9)]
            assert all(d in (0,2) for d in degrees) and sum(d>0 for d in degrees)==size
            visited={next(v for v,d in enumerate(degrees) if d)}
            while True:
                extended=visited|{v for e in chosen if any(e>>u&1 for u in visited) for v in range(9) if e>>v&1}
                if extended==visited:break
                visited=extended
            assert len(visited)==size;count+=1
        links[size]=count
    assert links=={3:84,4:378,5:1512}
    for name in ('verify_single_three_lemma_controls.py','verify_parent00_cubic_cycles.py','single_three_all_fives_obstruction_cycle146.md'):b.bind(Path(name))
    result=dict(status='INDEPENDENTLY_VERIFIED_LOCAL_CYCLE_LEMMA_CONTROLS',global_status='UNRESOLVED',
        six_vertex_cycles=len(codes),terminal_degree_sequence_count=0,
        positive_controls={'octahedral_degree_sequence':counts[(4,4,4,4,4,4)],'all_degree_five':counts[(5,5,5,5,5,5)]},
        nine_vertex_even_links=links,ten_vertex_proof='single_three_all_fives_obstruction_cycle146.md',
        accepted_parent_exclusions=0,files=[dict(path=p,sha256=d) for p,d in sorted(b.files.items())])
    output=Path('single-three-local-controls-independent-manifest-cycle146.json');assert not output.exists()
    output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True)


if __name__=='__main__':run()
