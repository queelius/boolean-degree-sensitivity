"""Independent stable-row adapter, delegating arithmetic to frozen1436 only."""
import copy
from gap_transcript_reader_cycle1436 import need,exact,_binding,verify

def row_maps(common,context,added):
 need(all(type(n) is int and n>=0 for n in (common,context,added)) and common+context+added>0,'typed nonempty row blocks')
 old=common+context;forward=list(range(old,old+added))+list(range(common,old))+list(range(common));inverse=[None]*len(forward)
 for new,native in enumerate(forward):inverse[native]=new
 return forward,inverse

def translate(raw,forward):
 need(type(raw) is dict and type(raw.get('steps')) is list,'structured raw certificate required')
 native=copy.deepcopy(raw)
 def index(i):
  need(type(i) is int and 0<=i<len(forward),'raw row ID invalid');return forward[i]
 for step in native['steps']:
  need(type(step) is dict and set(step)=={'variable','value','row'},'raw step fields differ');step['row']=index(step['row'])
 if 'contradiction_row' in native:native['contradiction_row']=index(native['contradiction_row'])
 return native

def verify_candidate(model,candidate,common,context,added):
 forward,inverse=row_maps(common,context,added)
 need(len(model['rows'])==len(forward),'complete native block counts differ')
 need(exact(candidate['generator_to_native'],forward) and exact(candidate['native_to_generator'],inverse),'complete row permutation/inverse differs')
 need(exact(candidate['model_header'],model['header']),'reconstructed native header differs')
 binding=_binding(model)
 need(exact(candidate['model_binding'],binding),'reconstructed native binding differs')
 native=translate(candidate['raw_generator_certificate'],forward)
 need(exact(native,candidate['native_certificate']),'literal raw/native translation differs')
 envelope=dict(schema_version=1,model_binding=binding,certificate=native)
 need(exact(envelope,candidate['envelope']),'literal native envelope differs')
 return verify(model,envelope,binding)
