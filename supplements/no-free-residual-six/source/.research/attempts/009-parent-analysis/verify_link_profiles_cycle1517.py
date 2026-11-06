"""One independent six-catalog profile pass with inherited cover completeness."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import resource
import time

from link_profile_reader_cycle1517 import analyze, exact, require


def ref(path):
    path = Path(path).resolve(); data = path.read_bytes()
    return dict(path=str(path),sha256=hashlib.sha256(data).hexdigest(),bytes=len(data))


def load(source):
    actual = ref(source['path'])
    require(actual['sha256'] == source['sha256'] and
            ('bytes' not in source or actual['bytes'] == source['bytes']), 'source pin')
    return json.loads(Path(source['path']).read_bytes())


def catalog_records(catalog):
    require(catalog['status'] == 'COMPLETE_INVERSE_CONTRACTION_COVER', 'catalog status')
    order = catalog['order']
    require(type(order) is int and order >= 4, 'catalog order')
    selected = []
    for ordinal, record in enumerate(catalog['classes']):
        require(set(record) == {'index','face_masks'} and type(record['index']) is int
                and record['index'] == ordinal, 'original native catalog index')
        degrees, kind = analyze(order, record['face_masks'])
        if kind is not None:
            selected.append(dict(order=order,native_index=ordinal,degrees=degrees,
                                 kind=kind,face_masks=record['face_masks']))
    return selected, len(catalog['classes'])


def compare_proposal(proposal, selected, total, orders):
    summary = {kind:{str(n):count for n,count in sorted(Counter(
        r['order'] for r in selected if r['kind'] == kind).items())}
        for kind in ('ordinary','positive_tip','negative_tip')}
    require(exact(proposal['native_records_checked'], total) and
            exact(proposal['catalogs_checked'], orders) and
            exact(proposal['selected'], selected) and exact(proposal['summary'], summary),
            'complete literal profile result disagreement')
    return summary


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--plan',type=Path,required=True)
    parser.add_argument('--plan-sha256',required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    require(not args.output.exists(), 'fresh independent output')
    resource.setrlimit(resource.RLIMIT_AS,(512*1024**2,512*1024**2))
    resource.setrlimit(resource.RLIMIT_CPU,(4,4))
    start=time.process_time()
    planref=dict(path=str(args.plan.resolve()),sha256=args.plan_sha256)
    plan=load(planref)
    proposal=load(plan['proposal']); authority=load(plan['catalog_authority'])
    require(authority['status'] == 'INDEPENDENTLY_VERIFIED_COMPLETE_NECESSARY_SIGNED_STAR_GEOMETRY_DOMAIN'
            and authority['source_completeness_is_explicit_inherited_premise'] is True,
            'accepted inherited catalog cover')
    require(exact(proposal['source_authority'], plan['catalog_authority']), 'proposal cover authority')
    for source in plan['sources']:
        require(ref(source['path'])['sha256'] == source['sha256'], 'pre-run bound source')
    accepted = {s['path']:s['sha256'] for s in authority['sources']}
    sources=proposal['sources']
    require(len(sources) == 6 and len({s['path'] for s in sources}) == 6 and
            all(accepted.get(s['path']) == s['sha256'] for s in sources),
            'exact accepted six catalog sources')
    records=[];total=0;orders=[];catalog_counts=[]
    for source in sources:
        catalog=load(source)
        kept,count=catalog_records(catalog)
        records.extend(kept);total+=count;orders.append(catalog['order'])
        catalog_counts.append(dict(order=catalog['order'],native_records=count,source=source))
    require(orders == list(range(7,13)) and total == authority['native_records_checked'],
            'complete accepted order interval and record count')
    summary=compare_proposal(proposal,records,total,orders)
    result=dict(schema_version=1,status='INDEPENDENTLY_VERIFIED_LITERAL_VERTEX_LINK_PROFILE_SCAN',
        proposal=plan['proposal'],plan=planref,catalog_authority=plan['catalog_authority'],
        inherited_sphere_cover=authority['inherited_sphere_cover'],
        sources=plan['sources']+sources+[ref(__file__),ref(args.plan)],
        native_records_checked=total,catalogs=catalog_counts,selected=records,summary=summary,
        degree_algorithm='Actual distinct edge-neighbor sets; edge cofaces and every cyclic vertex link checked.',
        source_native_IDs_preserved=True,sphere_cover_completeness_replayed=False,
        inherited_cover_transitions=authority['inherited_sphere_cover_transitions'],
        source_completeness_is_explicit_inherited_premise=True,
        necessary_nonroot_degrees=dict(
            positive_tip=sorted(map(int,summary['positive_tip'])),
            negative_tip=sorted(map(int,summary['negative_tip'])),
            ordinary=sorted({6}|set(map(int,summary['ordinary'])))),
        n6_ordinary='Allowed outside scanned catalogs; literal octahedron control passes.',
        n6_negative='Impossible: a six-vertex simple link graph has maximum degree five.',
        n6_positive='Excluded by the separately accepted1497 elementary six-vertex sphere lemma.',
        applicability='Genuine signed-star sphere: each nonroot tip sees exactly one exceptional edge; other nonroot vertices see none. Central root is not in these profiles.',
        old_relaxed_rows_entail_degree_sets_established=False,
        elapsed_CPU_seconds=time.process_time()-start,
        peak_RSS_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,
        target_models_filtered=0,target_queries=0,new_context_exclusions=0,
        actual_derivative_constructed=False,whole_pattern_excluded=False,global_goal_complete=False)
    for source in result['sources']:
        require(ref(source['path'])['sha256'] == source['sha256'], 'post-run bound source')
    with args.output.open('x') as stream:
        json.dump(result,stream,indent=2);stream.write('\n')
    print(json.dumps({k:result[k] for k in ('status','native_records_checked','summary',
                                          'elapsed_CPU_seconds','peak_RSS_bytes')}))


if __name__=='__main__':
    main()
