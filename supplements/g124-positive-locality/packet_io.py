"""Strict relative-path IO only; the two graph algorithms share no kernels. MIT."""
from argparse import ArgumentParser
from hashlib import sha256
from pathlib import Path,PurePosixPath
from time import process_time
import gzip,json,math
ROOT=Path(__file__).resolve().parent
REQUIRED={'data/catalog.json.gz','data/certificate.json.gz','data/external-classification.json'}
def need(ok,message):
 if not ok:raise ValueError(message)
def same(a,b,message):need(json.dumps(a,sort_keys=True,allow_nan=False)==json.dumps(b,sort_keys=True,allow_nan=False),message)
def safe(root,name):
 need(type(name)is str,'Literal relative path required.');p=PurePosixPath(name)
 need(not p.is_absolute() and '..' not in p.parts and p.parts and str(p)==name,'Packet path escape or alias.')
 result=(root/name).resolve();need(result.is_relative_to(root.resolve()),'Packet symlink escape.');return result

def inventory(catalog,certificate):
 for field,value in [('schema_version',1),('vertices',14),('edges_per_graph',124),('graph_count',75)]:same(catalog[field],value,'Catalog scope changed.')
 need(type(catalog['graphs'])is list and len(catalog['graphs'])==75,'Complete75 native graphs required.')
 for field,value in [('schema_version',1),('status','COMPLETE_LITERAL_G124_POSITIVE_LOCALITY_CERTIFICATE'),('vertices',14),('edges_per_graph',124),('native_graphs',75),('graph_lemma_only',True),('original_Boolean_problem_solved',False)]:same(certificate[field],value,'Certificate scope changed.')
 need(type(certificate['records'])is list and len(certificate['records'])==75,'Complete75 certificate records required.')
 same([r['catalog_index'] for r in certificate['records']],list(range(75)),'Native record identities omitted, duplicated or aliased.')

def inputs(root=ROOT):
 root=Path(root).resolve();path=root/'data/manifest.json';raw=path.read_bytes();manifest=json.loads(raw)
 same(manifest['schema_version'],1,'Manifest schema changed.');need(type(manifest['files'])is list,'Typed file inventory required.')
 names=[r['path'] for r in manifest['files']];need(len(names)==len(REQUIRED) and set(names)==REQUIRED,'Complete nonduplicated data files required.')
 bindings={'data/manifest.json':sha256(raw).hexdigest()};decoded={}
 for row in manifest['files']:
  need(type(row['sha256'])is str and len(row['sha256'])==64 and type(row['bytes'])is int and row['bytes']>=0,'Malformed pin.')
  p=safe(root,row['path']);data=p.read_bytes();need(len(data)==row['bytes'] and sha256(data).hexdigest()==row['sha256'],'Data hash/size mismatch.')
  bindings[row['path']]=row['sha256'];decoded[row['path']]=json.loads(gzip.decompress(data) if p.suffix=='.gz' else data)
 external=decoded['data/external-classification.json']
 for key,value in [('doi','10.1002/jcd.20223'),('figure',1),('manuscript_page',4),('vertices',14),('classes_at_124_edges',75),('classification_exhaustive_search_replayed_here',False),('primary_PDF_redistributed',False)]:same(external[key],value,'External classification premise changed.')
 catalog=decoded['data/catalog.json.gz'];certificate=decoded['data/certificate.json.gz'];inventory(catalog,certificate);return catalog,certificate,bindings

def rehash(bindings):
 for name,digest in bindings.items():need(sha256(safe(ROOT,name).read_bytes()).hexdigest()==digest,'Bound packet file changed during replay.')
def incomplete(completed,bindings):
 return dict(status='INCOMPLETE',completed_native_indices=completed,pending_native_indices=[i for i in range(75) if i not in completed],bindings=bindings,complete_cover_verified=False,Boolean_problem_solved=False)

def main(audit,source):
 parser=ArgumentParser();parser.add_argument('--output',type=Path,required=True);parser.add_argument('--cpu-budget',type=float,default=60);args=parser.parse_args()
 need(not args.output.exists(),'Fresh output required; existing files are never replaced.');need(math.isfinite(args.cpu_budget) and args.cpu_budget>0,'Finite positive CPU budget required.')
 result=audit(args.cpu_budget);result['source_bindings']={Path(source).name:sha256(Path(source).read_bytes()).hexdigest(),'packet_io.py':sha256(Path(__file__).read_bytes()).hexdigest()}
 with args.output.open('x') as stream:json.dump(result,stream,indent=2,sort_keys=True);stream.write('\n')
 print(json.dumps({k:v for k,v in result.items() if k not in ('bindings','source_bindings','completed_native_indices','pending_native_indices')},sort_keys=True))
