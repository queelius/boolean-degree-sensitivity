"""Discover explicit pair transports; completeness of the automorphism tool is unused."""
from argparse import ArgumentParser
from collections import deque
from pathlib import Path
import json
from compose_class40_same_b_acceptance import Bindings
from two_positive_conditional_orbits import coordinate_generators,move

H=Path(__file__).resolve().parent


def run(frontier_path,output):
    b=Bindings();frontier=b.read(frontier_path);assert frontier['status']=='VERIFIED_ASSEMBLY_MATCHED_FIRST_ROW_FRONTIER'
    quota=b.read(frontier['scope']['quotient_authority']['path'],frontier['scope']['quotient_authority']['sha256'])
    geometry=quota['geometry'];marked=quota['marked_pair'];known={q:-2 for q in geometry['negative_supports']}|{q:2 for q in geometry['positive_doubles']}
    generators=coordinate_generators(known,());seen={marked:list(range(14))};todo=deque([marked])
    while todo:
        source=todo.popleft()
        for generator in generators:
            target=move(source,generator)
            if target not in seen:seen[target]=[generator[v]for v in seen[source]];todo.append(target)
    assert set(seen)<=set(geometry['eligible_pairs'])
    transports=[dict(source_pair=marked,target_pair=target,map=image)for target,image in sorted(seen.items())if target!=marked]
    for name in ('propose_safe_pair_transports_cycle323.py','two_positive_conditional_orbits.py'):b.bind(H/name)
    result=dict(status='PROPOSED_SIGNED_GEOMETRY_SAFE_PAIR_TRANSPORTS',frontier=b.bind(frontier_path),
                quotient_authority=frontier['scope']['quotient_authority'],geometry_index=geometry['index'],
                marked_pair=marked,transports=transports,canonicalizer_trusted_for_completeness=False,
                files=[dict(path=p,sha256=d)for p,d in sorted(b.files.items())])
    assert not output.exists();output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(geometry=geometry['index'],marked_pair=marked,transported_pairs=[r['target_pair']for r in transports])))


if __name__=='__main__':
    p=ArgumentParser(description=__doc__);p.add_argument('--frontier',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();run(a.frontier,a.output)
