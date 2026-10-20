"""Audit actual N=1 signatures and transfer exact fixed-negative interval proofs."""
from argparse import ArgumentParser
from itertools import combinations
from pathlib import Path
import json
from compose_class40_same_b_acceptance import Bindings
from gzip_certificate_io import read_certificate,write_certificate
from verify_cubic_n2_batch import read_basis
from verify_missing_diagonal_witnesses import ScalarValues

H=Path(__file__).resolve().parent


def actual_singletons(data,frames):
    evidence=[]
    for frame in frames:
        index=frame['geometry'];g=data['representatives'][index];p,r=g['positive_doubles'];core=p&r
        vertices=[i for i in range(14) if core>>i&1];apices=(p|r)^core
        missing=[sum(1<<i for i in pair) for pair in combinations(vertices,2) if sum(1<<i for i in pair) not in g['eligible_pairs']]
        assert len(missing)==2 and missing[0]&missing[1]==0
        for pair in missing:
            negative=[q^pair for q in g['negative_supports'] if q&core==pair]
            assert len(negative) in (1,2) and all(q.bit_count()==3 for q in negative)
            if len(negative)==1:evidence.append(dict(geometry=index,core_pair=pair,negative_outside=negative[0],apices=apices,apex_count=(negative[0]&apices).bit_count()))
    return evidence


def run(output):
    b=Bindings();source_path=H/'fixed-cubic-mask03-N1-independent-manifest.json'
    source=b.read(source_path,'13bdb570a8dabcc16bbf566b4d73173ce5048e3474c2c292a7c7b8d88c9e0b6a')
    assert source['status']=='INDEPENDENTLY_VERIFIED_COMPLETE_FIXED_CUBIC_ONE_NEGATIVE_PLACEMENT_SCREEN'
    frame_path=H/'safe-four-cycle-first-second-covers-independent-manifest.json';frames=b.read(frame_path,'7aaaed46c192db0cf0a5886378778dd9c1c877e1154e504b7fd0c9570c53d0de')
    data=b.read(H/'two-positive-pair-embeddings.json','0edddced95caf2082e8bf1f0f7c56fdf17f7e4d032fc1f34a14306e82ea6476b');evidence=actual_singletons(data,frames['actual_frames'])
    allowed={r['apex_count'] for r in evidence};assert allowed=={1,2} and len(evidence)==42
    patterns=[q for q in range(1024) if q.bit_count()==3 and (q&3).bit_count() in allowed];assert len(patterns)==64
    frontier_path=H/'four-cycle-a0056-b0056-fixed-frontier-independent-manifest.json';frontier=b.read(frontier_path,'79befb992d4d16c9616bbcab0bf1f2a55a7039828459c716ca100370479ac4bc')
    assert source['geometry']==frontier['geometry']==frames['geometry'] and source['core_mask']==3
    scalar=ScalarValues(data['domain']['rows'],source['geometry']);base=read_certificate(b,source['parent']);base_values=scalar.allowed(tuple(d['rows'][0] for d in base['domains']),3)
    bases={};proofs={}
    for record in source['records']:
        assert len(record['negative'])==1;q=record['negative'][0]
        if q not in patterns or not record['independently_excluded']:continue
        detail=read_certificate(b,record['proof']);assert detail['parent']==source['parent'] and detail['negative']==[q] and detail['core_mask']==3
        basis=read_basis(detail,1);rhs=basis.evaluate(base_values);assert rhs==record['verification']['integer_rhs']==detail['result']['certificate']['integer_rhs'] and rhs<0
        bases[q]=basis;proofs[q]=record['proof']
    assert set(patterns)-set(bases)=={13,14}
    directory=output.with_suffix('');assert not output.exists() and not directory.exists();directory.mkdir();results=[]
    for case in frontier['records']:
        parent=read_certificate(b,case['propagation']);domains=parent['domains'];assert [d['pair'] for d in domains]==source['geometry']['eligible_pairs'] and all(len(d['rows'])==1 for d in domains)
        values=scalar.allowed(tuple(d['rows'][0] for d in domains),3);checks=[]
        for q in patterns:
            rhs=bases[q].evaluate(values) if q in bases else None
            checks.append(dict(negative=[q],basis=proofs.get(q),integer_rhs=rhs,excluded=rhs is not None and rhs<0))
        remaining=[r['negative'] for r in checks if not r['excluded']]
        detail=dict(status='EXACT_SCALAR_CUBIC_SINGLETON_INTERVAL_TRANSFERS',parent=case['propagation'],geometry=source['geometry'],core_mask=3,negative_count=1,checks=checks)
        path=directory/f"t{case['third_row']:04d}-u{case['fourth_row']:04d}.json.gz";write_certificate(path,detail)
        result=dict(third_row=case['third_row'],fourth_row=case['fourth_row'],parent=case['propagation'],proof=b.bind(path),total_positions=64,excluded_positions=64-len(remaining),remaining=remaining)
        results.append(result);print(json.dumps(dict(third=case['third_row'],fourth=case['fourth_row'],excluded=result['excluded_positions'],remaining=len(remaining))),flush=True)
    for name in ('verify_cubic_singleton_transfers.py','test_verify_cubic_singleton_transfers.py','cubic-interval-certificate-transfer-lemma-cycle108.md'):b.bind(H/name)
    result=dict(status='INDEPENDENTLY_VERIFIED_ACTUAL_CUBIC_SINGLETON_INTERVAL_TRANSFERS',global_status='UNRESOLVED',
        source=b.bind(source_path),frames_authority=b.bind(frame_path),fixed_frontier_authority=b.bind(frontier_path),geometry=source['geometry'],
        core_mask=3,negative_count=1,actual_evidence=evidence,allowed_apex_counts=sorted(allowed),literal_patterns=[[q] for q in patterns],records=results,
        solver_imported=False,files=[dict(path=p,sha256=d) for p,d in sorted(b.files.items())])
    output.write_text(json.dumps(result,indent=2)+'\n')


if __name__=='__main__':
    p=ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);run(p.parse_args().output)
