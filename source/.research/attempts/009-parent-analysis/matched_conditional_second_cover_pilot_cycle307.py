"""Measure conditional second-row quotients on surviving first-row families."""
from argparse import ArgumentParser
from pathlib import Path
from time import monotonic
import json
from compose_class40_same_b_acceptance import Bindings
from gzip_certificate_io import write_certificate
from verify_coupled_two_positive import literal_embedding
from two_positive_conditional_orbits import cover

H=Path(__file__).resolve().parent


def run(residual_path,output):
    start=monotonic();b=Bindings();residual=b.read(residual_path)
    assert residual['status']=='INDEPENDENTLY_VERIFIED_FIRST_ROW_RESIDUAL_COVER_FROM_PARTIAL_SEARCH'
    quota=b.read(residual['quotient_authority']['path'],residual['quotient_authority']['sha256'])
    assert quota['status']=='INDEPENDENTLY_VERIFIED_MATCHED_FIRST_ROW_QUOTIENT' and quota['complete_actual_cover'] is True
    assert quota['geometry_index']==residual['geometry_index']
    data=b.read(H/'two-positive-pair-embeddings.json','0edddced95caf2082e8bf1f0f7c56fdf17f7e4d032fc1f34a14306e82ea6476b')
    rows=data['domain']['rows'];geometry=dict(quota['geometry']);geometry['selected_pair']=quota['marked_pair']
    selected={}
    for r in residual['residual_source_rows']:selected.setdefault(len(rows[r]['unit_faces']),r)
    second_pair=min(p for p in geometry['eligible_pairs'] if p!=geometry['selected_pair'])
    records=[]
    for family,first in sorted(selected.items()):
        known=literal_embedding(rows[first],geometry,geometry['selected_pair'])
        result=cover(geometry,rows,known,second_pair,list(range(len(rows))))
        records.append(dict(first_row=first,row_family=family,known=sorted(known.items()),second_pair=second_pair,**result))
        print(json.dumps(dict(geometry=geometry['index'],first_row=first,row_family=family,second_pair=second_pair,
                              raw_rows=result['raw_rows'],representatives=result['representative_count'],generators=len(result['generators']))),flush=True)
    proof_path=output.with_suffix('.json.gz');assert not output.exists()and not proof_path.exists()
    write_certificate(proof_path,dict(geometry=geometry,quotient_authority=residual['quotient_authority'],residual_cover=b.bind(residual_path),records=records))
    for name in ('matched_conditional_second_cover_pilot_cycle307.py','two_positive_conditional_orbits.py',
                 'test_two_positive_conditional_orbits.py','matched_conditional_second_cover_soundness_cycle307.md'):b.bind(H/name)
    result=dict(status='PROPOSED_MATCHED_CONDITIONAL_SECOND_ROW_COVER_PILOT',global_status='UNRESOLVED',
                geometry_index=quota['geometry_index'],quotient_authority=residual['quotient_authority'],residual_cover=b.bind(residual_path),
                proof=b.bind(proof_path),sampled_first_rows=[r['first_row']for r in records],
                covered_all_first_rows=False,geometry_exclusions=0,independent_audit='PENDING',seconds=monotonic()-start,
                files=[dict(path=p,sha256=d)for p,d in sorted(b.files.items())])
    output.write_text(json.dumps(result,indent=2)+'\n')


if __name__=='__main__':
    p=ArgumentParser(description=__doc__);p.add_argument('--residual',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();run(a.residual,a.output)
