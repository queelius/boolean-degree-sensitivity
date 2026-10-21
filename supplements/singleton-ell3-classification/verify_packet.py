"""Standalone literal-certificate and exact family-cover replay; stdlib, MIT."""
from argparse import ArgumentParser
from collections import Counter
from hashlib import sha256
from pathlib import Path
from time import monotonic,process_time
import gzip
import json

import graph_cover as graph
import quota_search as quota

require=graph.require


def check_files(directory,manifest):
    require(type(manifest) is dict and type(manifest.get('files')) is list,'Missing file manifest.')
    seen=set()
    for row in manifest['files']:
        name=row['path'];path=Path(name)
        require(type(name) is str and name not in seen and not path.is_absolute() and '..' not in path.parts,
                'Unsafe or duplicated data path.')
        seen.add(name);raw=(directory/path).read_bytes()
        require(type(row['bytes']) is int and len(raw)==row['bytes'] and sha256(raw).hexdigest()==row['sha256'],
                'Data file pin mismatch: '+name)
    return True


def check_bridge(augmentation,catalog,bridge):
    require(bridge['vertices']==10 and bridge['negative_edges']==8 and bridge['minimum_components']==3,'Wrong bridge scope.')
    representatives=augmentation['grades'][-1]['representatives'];raw=catalog['raw_graphs']
    expected={i for i,m in enumerate(representatives) if len(graph.connected_components(m))>=3}
    seen=set();reached=set()
    for link in bridge['links']:
        i,j=link['augmentation_index'],link['raw_graph_index']
        require(type(i) is int and i in expected and i not in seen and type(j) is int and 0<=j<len(raw),
                'Missing, aliased or invalid uncolored frame link.')
        graph.check_transport(representatives[i],0,raw[j]['negative_pairs'],0,link['old_to_raw'],10)
        require(len(raw[j]['negative_pairs'])==8 and len(graph.connected_components(raw[j]['negative_pairs']))>=3,
                'Wrong eligible raw graph.')
        seen.add(i);reached.add(j)
    require(seen==expected and reached==set(range(len(raw))),'Incomplete uncolored frame bridge.')
    return [(row['source_grade_index'],tuple(row['negative_pairs'])) for row in raw]


def compare_family_sets(actual,expected):
    for rows in [actual,expected]:
        require(type(rows) is list and all(type(f) is list and f==sorted(set(f)) and
            all(type(v) is int and 0<v<1024 and v.bit_count()==4 for v in f) for f in rows),
            'Malformed simple quartet family set.')
        require(rows==sorted(rows) and len(rows)==len({tuple(f) for f in rows}),'Repeated or unordered family set.')
    require(actual==expected,'Exhaustive per-cover family set differs.')
    return True


def component_key(negative,exceptional,positive):
    return tuple(sorted(negative)),exceptional,tuple(sorted(positive))


def verify_components(data):
    require(all(type(v) is int for v in data['parameters'].values()) and
            data['parameters']==dict(vertices=10,constant_coefficient=1,negative_pairs=8,positive_quartics=7,exceptional_mask=7),
            'Wrong component data scope.')
    rows=data['components'];require(len(rows)==17,'The literal17-family inventory differs.')
    keys=set();audits=[]
    for i,row in enumerate(rows):
        require(type(row['component_id']) is int and row['component_id']==i and type(row['exceptional_mask']) is int and
                row['exceptional_mask']==7,'Changed component identity/color.')
        negative=graph.graph_edges(row['negative_pairs'],10);positive=row['positive_quartics']
        require(len(negative)==8 and type(positive) is list and positive==sorted(set(positive)) and len(positive)==7 and
                all(type(v) is int and 0<v<1024 and v.bit_count()==4 for v in positive),'Wrong literal support sizes.')
        key=component_key(negative,7,positive);require(key not in keys,'Duplicate literal component.');keys.add(key)
        values=[1-sum(-1 if (x&e).bit_count()%2 else 1 for e in negative)+
                sum(-1 if (x&f).bit_count()%2 else 1 for f in positive) for x in range(1024)]
        require(values[0]==0 and [values[1<<j] for j in range(10)]==[-8]*3+[0]*7 and
                all(value%8==0 for value in values),'Component origin/singleton/divisibility failed.')
        transformed=values.copy();width=1
        while width<1024:
            for start in range(0,1024,2*width):
                for offset in range(width):
                    a,b=transformed[start+offset],transformed[start+offset+width]
                    transformed[start+offset]=a+b;transformed[start+offset+width]=a-b
            width*=2
        expected=[0]*1024;expected[0]=1024
        for e in negative:expected[e]=-1024
        for f in positive:expected[f]=1024
        require(transformed==expected,'Exact complete Fourier spectrum differs.')
        support=0
        for mask in list(negative)+positive:support|=mask
        audits.append(dict(component_id=i,cube_inputs_checked=1024,fourier_coefficients_checked=1024,
            real_degree=4,active_coordinates=support.bit_count(),histogram={str(k):v for k,v in sorted(Counter(values).items())},
            values_sha256=sha256(json.dumps(values,separators=(',',':')).encode()).hexdigest()))
    return audits


def run(directory,output,budget,files_only=False):
    require(not output.exists(),'Fresh output required.')
    require(10<=budget<=120,'CPU budget must be10..120 seconds.')
    start=process_time();wall=monotonic()
    manifest=json.loads((directory/'manifest.json').read_text());check_files(directory,manifest)
    require(all(type(v) is int for v in manifest['math_scope'].values()) and
            manifest['math_scope']==dict(vertices=10,constant_coefficient=1,negative_pairs=8,positive_quartics=7,exceptional_vertices=3)
            and manifest['global_problem_complete'] is False and manifest['canonical_orbit_minimality_claimed'] is False,
            'Wrong manifest scope.')
    if files_only:
        receipt=dict(status='DATA_PINS_ONLY_NOT_A_PROOF_REPLAY',files_checked=len(manifest['files']),complete_proof_replay=False)
    else:
        def read(name):
            raw=(directory/name).read_bytes()
            return json.loads(gzip.decompress(raw) if name.endswith('.gz') else raw)
        catalog=read('graph-catalog.json.gz');augmentation=read('augmentation.json.gz')
        bridge=read('frame-links.json');components=read('components.json');expected=read('expected-solutions.json.gz')
        graph.check_header(catalog)
        require(augmentation['vertices']==10 and augmentation['max_edges']==8,'Wrong augmentation scope.')
        induction=graph.verify_augmentation(augmentation['grades'],10,8)
        eligible=check_bridge(augmentation,catalog,bridge)
        cases=catalog['canonical_cases'];profiles=[]
        for i,case in enumerate(cases):
            require(type(case['case_id']) is int and case['case_id']==i,'Missing/aliased colored case ID.')
            profiles.append(graph.check_profile(case))
        markings=graph.check_marked_cover(catalog['raw_graphs'],cases,eligible)
        audits=verify_components(components)
        instances=[dict(instance_index=i,case_id=case_id,cover_index=cover_id) for i,(case_id,cover_id) in enumerate(
            ( (case['case_id'],j) for case in cases for j,cover in enumerate(case['profile']['covers']) if cover['incidence_capacity_pass']))]
        require(len(expected['instances'])==len(instances)==19112,'Missing expected native instance.')
        registry={component_key(row['negative_pairs'],row['exceptional_mask'],row['positive_quartics']):
                  row['component_id'] for row in components['components']}
        occurrences={i:set() for i in range(17)};records=[];open_audit=None
        for identity,reference in zip(instances,expected['instances']):
            require(all(type(reference[k]) is int and reference[k]==value for k,value in identity.items()),'Changed reference instance identity.')
            remaining=budget-10-(process_time()-start)
            if remaining<=0:open_audit=dict(reason='OPEN_TOTAL_CPU_LIMIT',next_identity=identity);break
            problem=quota.build_problem(cases[identity['case_id']],identity['cover_index'])
            result=quota.enumerate_families(problem['quartics'],problem['targets'],problem['boundary'],10,7,
                cpu_limit=min(5,remaining),node_limit=1000000,branch_limit=10000)
            if result['status']!='EXHAUSTED':
                open_audit=dict(identity=identity,problem=problem,result=result);break
            compare_family_sets(result['families'],reference['families'])
            for family in result['families']:
                key=component_key(problem['negative_pairs'],problem['exceptional_mask'],family)
                require(key in registry,'An enumerated family is absent from the17-family cover.')
                occurrences[registry[key]].add(identity['instance_index'])
            records.append(dict(**identity,nodes=result['nodes'],families=result['families']))
            if len(records)%2000==0:
                print(json.dumps(dict(stage='EXACT_FAMILY_ENUMERATION',checked=len(records),total=19112,
                    cpu_seconds=process_time()-start)),flush=True)
        complete=len(records)==len(instances) and open_audit is None
        if complete:
            for row in components['components']:
                ids=row['source_instance_indices']
                require(type(ids) is list and all(type(i) is int for i in ids) and len(ids)==len(set(ids)) and
                        set(ids)==occurrences[row['component_id']] and ids,'Native source occurrences differ.')
        receipt=dict(status='COMPLETE_PORTABLE_A1_ELL3_FAMILY_COVER_REPLAY' if complete else 'INCOMPLETE_PORTABLE_REPLAY',
            complete_proof_replay=complete,augmentation=induction,uncolored_frame_links=len(bridge['links']),
            raw_marked_transports=markings,colored_frames=len(cases),
            maximal_subspace_covers=sum(p['subspace_covers'] for p in profiles),
            capacity_passing_instances=len(instances),exhausted_instances=len(records),records=records,
            open_audit=open_audit,pending_instance_indices=list(range(len(records),len(instances))),
            literal_components=17,component_audits=audits,
            source_occurrences=sum(len(v) for v in occurrences.values()),
            canonical_uniqueness_required=False,minimal_coordinate_orbit_count_claimed=False,
            standard_library_only=True,research_workspace_imported=False,actual_boolean_function=False,
            a2_ell3_covered=False,global_problem_complete=False,formal_verification=False,human_review=False,
            novelty_established=False,publication_approved=False)
    receipt.update(cpu_seconds=process_time()-start,wall_seconds=monotonic()-wall,
                   data_manifest_sha256=sha256((directory/'manifest.json').read_bytes()).hexdigest())
    if output.name.endswith('.gz'):
        with gzip.open(output,'xt') as stream:json.dump(receipt,stream,separators=(',',':'));stream.write('\n')
    else:
        with output.open('x') as stream:json.dump(receipt,stream,indent=2);stream.write('\n')
    print(json.dumps({key:receipt[key] for key in ['status','complete_proof_replay','cpu_seconds','wall_seconds']}),flush=True)
    return receipt


if __name__=='__main__':
    parser=ArgumentParser(description=__doc__)
    parser.add_argument('--data-dir',type=Path,default=Path(__file__).resolve().parent/'data')
    parser.add_argument('--output',type=Path,required=True);parser.add_argument('--cpu-budget',type=float,default=120)
    parser.add_argument('--check-files-only',action='store_true');args=parser.parse_args()
    run(args.data_dir,args.output,args.cpu_budget,args.check_files_only)
