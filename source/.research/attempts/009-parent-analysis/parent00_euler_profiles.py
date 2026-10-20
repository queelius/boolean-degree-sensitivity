"""Generate the complete degree/count consequences for the negative13 Euler proof."""
from pathlib import Path
import json
from compose_class40_same_b_acceptance import Bindings
from gzip_certificate_io import read_certificate
from generic_parseval_envelope import permitted
from two_positive_four_cube_domains import CubeIndex
from cubic_degree_profiles import degree_options,degree_profiles,low_degree_cycle_bound

H=Path(__file__).resolve().parent


def run():
    b=Bindings();frontier_path=H/'parent00-cubic-position-frontier-cycle111.json';frontier=b.read(frontier_path,'def75edd753c090f628bf4df76009c16864d87020657e1fe013d8207ced65f2d')
    case=next(r for r in frontier['remaining'] if r['negative']==[13]);parent=read_certificate(b,frontier['parent']);g=frontier['geometry']
    rows=b.read(H/'two-positive-pair-embeddings.json','0edddced95caf2082e8bf1f0f7c56fdf17f7e4d032fc1f34a14306e82ea6476b')['domain']['rows'];values=permitted(g,parent['domains'],CubeIndex.build(rows),[3])[3]
    singletons=[values[1<<i] for i in range(10)];profiles=degree_profiles(10,[13],singletons)
    records=[{**r,'obstruction':low_degree_cycle_bound(r['degrees'])} for r in profiles];assert records and all(r['obstruction'] is not None and r['obstruction']['excluded'] for r in records)
    for name in ('parent00_euler_profiles.py','cubic_degree_profiles.py','test_cubic_degree_profiles.py','parent00-negative13-euler-proof-cycle112.md'):b.bind(H/name)
    result=dict(status='PROPOSED_COMPLETE_PARENT00_NEGATIVE13_EULER_EXCLUSION',global_status='UNRESOLVED',independent_audit='PENDING',
        frontier=b.bind(frontier_path),geometry=g,parent=frontier['parent'],core_mask=3,negative=[13],index=case['index'],origin=values[0],singleton_values=singletons,
        degree_options=degree_options(10,[13],singletons),profiles=records,sources=[dict(path=p,sha256=d) for p,d in sorted(b.files.items())])
    output=H/'parent00-negative13-euler-profiles-cycle112.json';assert not output.exists();output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(dict(profiles=len(records),all_obstructed=True)),flush=True)


if __name__=='__main__':run()
