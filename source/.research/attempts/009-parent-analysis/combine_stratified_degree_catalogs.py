"""Assemble complete L=0,...,6 catalogs after checking all overlapping families."""
from argparse import ArgumentParser
from pathlib import Path
import json
from compose_class40_same_b_acceptance import Bindings
from gzip_certificate_io import read_certificate


def run(authority_paths,output):
    b=Bindings();covers={};records={};authorities=[];overlaps=[]
    for path in authority_paths:
        source=b.read(path);assert source['status']=='INDEPENDENTLY_VERIFIED_SINGLETON_STRATIFIED_CUBIC_CATALOGS'
        authorities.append(b.bind(path));assert [c['low_count'] for c in source['covers']]==source['low_counts']
        expected={(c['low_count'],r['index']) for c in source['covers'] for r in c['representatives']}
        assert len(source['records'])==len(expected) and {(r['low_count'],r['index']) for r in source['records']}==expected
        for cover in source['covers']:
            L=cover['low_count']
            if L in covers:assert covers[L]==cover
            else:covers[L]=cover
        for record in source['records']:
            key=record['low_count'],record['index']
            if key in records:
                old=records[key];assert old['negative']==record['negative']
                a=read_certificate(b,old['proof']);c=read_certificate(b,record['proof'])
                assert a['negative']==c['negative'] and a['singletons']==c['singletons']
                assert a['candidates']==c['candidates'] and old['candidates']==record['candidates']==len(a['candidates'])
                overlaps.append(dict(low_count=key[0],index=key[1],candidates=len(a['candidates']),left=old['proof'],right=record['proof']))
            else:records[key]=record
    assert sorted(covers)==list(range(7))
    assert {(r['low_count'],r['index']) for r in records.values()}=={(L,r['index']) for L,c in covers.items() for r in c['representatives']}
    patterns=None
    for L,c in covers.items():
        present={tuple(m['pattern']) for m in c['maps']}
        if patterns is None:patterns=present
        assert present==patterns and len(present)==484
        for r in c['representatives']:assert records[L,r['index']]['negative']==r['pattern']
    b.bind(Path(__file__))
    result=dict(status='INDEPENDENTLY_VERIFIED_SINGLETON_STRATIFIED_CUBIC_CATALOGS',global_status='UNRESOLVED',
        assembly_only=True,every_leaf_previously_independently_verified=True,authorities=authorities,
        low_counts=sorted(covers),covers=[covers[L] for L in sorted(covers)],records=[records[k] for k in sorted(records)],
        overlap_regressions=overlaps,parent_specific_scalar_filter_applied=False,parent_exclusion_claimed=False,
        files=[dict(path=p,sha256=d) for p,d in sorted(b.files.items())])
    assert not output.exists();output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(cases=len(records),candidates=sum(r['candidates'] for r in records.values()),overlap_regressions=len(overlaps))))


if __name__=='__main__':
    p=ArgumentParser(description=__doc__);p.add_argument('--authorities',type=Path,nargs='+',required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();run(a.authorities,a.output)
