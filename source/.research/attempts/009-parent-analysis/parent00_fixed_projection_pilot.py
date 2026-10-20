"""Condition the two unfixed pair rows on every member of four complete catalogs."""
from pathlib import Path
from time import monotonic
from collections import Counter
import json
from compose_class40_same_b_acceptance import Bindings
from gzip_certificate_io import read_certificate,write_certificate
from two_positive_four_cube_domains import CubeIndex
from fixed_projection_cube_domains import propagate

H=Path(__file__).resolve().parent


def run():
    start=monotonic();b=Bindings();frontier_path=H/'parent00-cubic-position-frontier-cycle112.json';frontier=b.read(frontier_path)
    assert frontier['status']=='ACCEPTED_PARENT00_CUBIC_POSITION_FRONTIER' and len(frontier['complete_projection_catalogs'])==4
    parent=read_certificate(b,frontier['parent']);rows=b.read(H/'two-positive-pair-embeddings.json','0edddced95caf2082e8bf1f0f7c56fdf17f7e4d032fc1f34a14306e82ea6476b')['domain']['rows'];cubes=CubeIndex.build(rows)
    directory=H/'parent00-fixed-projection-pilot-cycle113';output=directory.with_suffix('.json');assert not directory.exists() and not output.exists();directory.mkdir();records=[]
    for catalog in frontier['complete_projection_catalogs']:
        authority=b.read(catalog['authority']['path'],catalog['authority']['sha256']);source=next(r for r in authority['records'] if r['index']==catalog['index']);assert len(source['survivors'])==catalog['survivors']
        counts=Counter()
        for j,projection in enumerate(source['survivors']):
            spectrum=sorted([(q,1) for q in projection['positive']]+[(q,-1) for q in projection['linear']]+[(q,-2) for q in projection['negative']])
            proof=propagate(parent['domains'],frontier['geometry'],cubes,3,spectrum)
            detail=dict(geometry=frontier['geometry'],parent=frontier['parent'],catalog=catalog['authority'],index=catalog['index'],projection_index=j,projection=projection,
                core_mask=3,spectrum=spectrum,input_domains=parent['domains'],proof=proof)
            path=directory/f'r{catalog["index"]:02d}-p{j:03d}.json.gz';write_certificate(path,detail)
            record=dict(index=catalog['index'],projection_index=j,proof=b.bind(path),status=proof['status'],steps=len(proof['steps']))
            if 'domains' in proof:record['domain_sizes']=[len(d['rows']) for d in proof['domains']]
            records.append(record);counts[proof['status']]+=1
        print(json.dumps(dict(index=catalog['index'],projections=catalog['survivors'],statuses=dict(counts))),flush=True)
    for name in ('fixed_projection_cube_domains.py','test_fixed_projection_cube_domains.py','parent00_fixed_projection_pilot.py'):b.bind(H/name)
    result=dict(status='PARENT00_FIXED_CUBIC_PROJECTION_PROPAGATION_PILOT',global_status='UNRESOLVED',independent_audit='PENDING',frontier=b.bind(frontier_path),geometry=frontier['geometry'],parent=frontier['parent'],core_mask=3,
        records=records,status_counts=dict(Counter(r['status'] for r in records)),elapsed_seconds=monotonic()-start,sources=[dict(path=p,sha256=d) for p,d in sorted(b.files.items())])
    output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(dict(seconds=result['elapsed_seconds'],statuses=result['status_counts'])),flush=True)


if __name__=='__main__':run()
