"""Optional historical preparation, not portable verification; MIT.

Requires the original research directory and its pinned pynauty solely to
discover literal frame-link permutations. All those maps are verified without
that dependency by the portable checker. No absolute source path is embedded.
"""
from argparse import ArgumentParser
import ast
from hashlib import sha256
import gzip
import importlib.util
import json
from pathlib import Path
import shutil


def extract(path,names,imports,header,remove_debug=False):
    tree=ast.parse(path.read_text());selected=[]
    class DebugIndependent(ast.NodeTransformer):
        def visit_Name(self,node):
            return ast.copy_location(ast.Constant(value=True),node) if node.id=='__debug__' else node
    for node in tree.body:
        if isinstance(node,(ast.FunctionDef,ast.ClassDef)) and node.name in names:
            if remove_debug:node=DebugIndependent().visit(node)
            selected.append(node)
    if {node.name for node in selected}!=set(names):raise ValueError('Missing extraction function.')
    return header+'\n'+imports+'\n\n'+ast.unparse(ast.Module(body=selected,type_ignores=[]))+'\n'


def run(research,output):
    data=output/'data';data.mkdir(exist_ok=True)
    sources={}
    def read(name):
        raw=(research/name).read_bytes();sources[name]=dict(sha256=sha256(raw).hexdigest(),bytes=len(raw))
        return json.loads(gzip.decompress(raw) if name.endswith('.gz') else raw)
    catalog=read('canonical-negative-graph-catalog-cycle1216.json.gz')
    augmentation=read('canonical-negative-graph-reader-augmentation-cycle1220.json.gz')
    full=read('singleton-a1-ell3-full-cover-chunk0002-cycle1227.json.gz')
    independent=read('independent-complete-quartet-cover-cycle1228.json.gz')
    for source,dest in [('canonical-negative-graph-catalog-cycle1216.json.gz','graph-catalog.json.gz'),
                        ('canonical-negative-graph-reader-augmentation-cycle1220.json.gz','augmentation.json.gz')]:
        if (data/dest).exists():raise ValueError('Fresh data files required.')
        shutil.copyfile(research/source,data/dest)
    path=research/'canonical_negative_graph_cycle1216.py';sources[path.name]=dict(sha256=sha256(path.read_bytes()).hexdigest())
    spec=importlib.util.spec_from_file_location('historical_discovery_helper',path)
    helper=importlib.util.module_from_spec(spec);spec.loader.exec_module(helper)
    lookup={tuple(row['negative_pairs']):i for i,row in enumerate(catalog['raw_graphs'])};links=[]
    for i,graph in enumerate(augmentation['grades'][-1]['representatives']):
        if len(helper.components(graph))<3:continue
        target,permutation=helper.canonical(graph,0,10)
        if target not in lookup:raise ValueError('Missing producer raw graph.')
        links.append(dict(augmentation_index=i,raw_graph_index=lookup[target],old_to_raw=permutation))
    bridge=dict(schema_version=1,vertices=10,negative_edges=8,minimum_components=3,links=links,
                discovery_dependency='pynauty2.8.8.1 via pinned historical helper; verification requires literal maps only')
    (data/'frame-links.json').write_text(json.dumps(bridge,separators=(',',':'))+'\n')
    components=dict(schema_version=1,parameters=dict(vertices=10,constant_coefficient=1,negative_pairs=8,positive_quartics=7,exceptional_mask=7),
       components=[{key:row[key] for key in ['component_id','negative_pairs','exceptional_mask','positive_quartics','source_instance_indices']}
                   for row in full['components']],claim='COMPLETE_NATIVE_FAMILY_COVER_NOT_MINIMAL_ORBITS')
    (data/'components.json').write_text(json.dumps(components,indent=2)+'\n')
    expected=dict(schema_version=1,instances=[{key:row[key] for key in ['instance_index','case_id','cover_index','families']}
                                           for row in independent['records']])
    with gzip.open(data/'expected-solutions.json.gz','xt') as stream:json.dump(expected,stream,separators=(',',':'));stream.write('\n')
    graph_names=['require','integer','graph_edges','image_mask','check_transport','verify_augmentation','connected_components',
                 'linear_span','even_subspaces','exact_integer_list','check_profile','check_header','check_marked_cover']
    path=research/'verify_canonical_negative_graph_cycle1220.py';sources[path.name]=dict(sha256=sha256(path.read_bytes()).hexdigest())
    (output/'graph_cover.py').write_text(extract(path,graph_names,
       'from collections import Counter\nfrom functools import lru_cache\nfrom itertools import combinations',
       '"""Literal graph/marking/subspace certificate replay; standard library, MIT.\nAdapted from the separately reviewed cycle1220 reader; no canonicalizer.\n"""'))
    path=research/'independent_quartet_enumerator_cycle1226.py';sources[path.name]=dict(sha256=sha256(path.read_bytes()).hexdigest())
    (output/'quota_search.py').write_text(extract(path,['require','clique_boundary','in_span','build_problem','enumerate_families'],
       'from collections import Counter\nfrom itertools import combinations\nfrom math import comb\nfrom time import process_time',
       '"""Exact quota-vertex enumeration; standard library, MIT.\nAdapted from independent cycle1226; explicit checks also run under -O.\nOnly the historical __debug__ restriction is removed.\n"""',remove_debug=True))
    files=[]
    for path in sorted(data.iterdir()):
        files.append(dict(path=path.name,sha256=sha256(path.read_bytes()).hexdigest(),bytes=path.stat().st_size))
    manifest=dict(schema_version=1,math_scope=dict(vertices=10,constant_coefficient=1,negative_pairs=8,positive_quartics=7,exceptional_vertices=3),
                  files=files,global_problem_complete=False,canonical_orbit_minimality_claimed=False)
    (data/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    (output/'SOURCE_PINS.json').write_text(json.dumps(dict(schema_version=1,historical_sources=sources,
       source_pins_are_replay_dependencies=False,portable_replay_imports_research_workspace=False,
       preparation_only_dependency='pynauty2.8.8.1; not imported by portable replay'),indent=2)+'\n')
    print(json.dumps(dict(frame_links=len(links),components=len(components['components']),expected_instances=len(expected['instances']))))


if __name__=='__main__':
    parser=ArgumentParser(description=__doc__);parser.add_argument('--research-dir',type=Path,required=True)
    parser.add_argument('--output-dir',type=Path,default=Path(__file__).parent);args=parser.parse_args();run(args.research_dir,args.output_dir)
