"""Independent adapter controls; no native target generation."""
import copy
import unittest
from extended_trace_reader_cycle1522 import verify_candidate, row_maps, translate
from gap_transcript_reader_cycle1436 import binding

def row(subject, terms, low, high):
 return dict(key=dict(family='CONTROL',subject=subject,detail=0),terms=terms,lower=low,upper=high)

def fixture():
 model=dict(schema_version=1,header=dict(kind='TOY',n=2,constant=1),variables=[3,5],rows=[row(0,[[3,1]],1,1),row(1,[[3,1],[5,1]],1,1),row(2,[[5,1]],1,1)])
 raw=dict(status='EXACT_INTERVAL_CONTRADICTION',steps=[dict(variable=3,value=1,row=2),dict(variable=5,value=0,row=1)],evaluations=9,fixed_variables=2,contradiction_row=0,contradiction_interval=[0,0])
 forward,inverse=row_maps(1,1,1);native=translate(raw,forward);b=binding(model)
 candidate=dict(model_header=model['header'],model_binding=b,generator_to_native=forward,native_to_generator=inverse,raw_generator_certificate=raw,native_certificate=native,envelope=dict(schema_version=1,model_binding=b,certificate=native))
 return model,candidate

class Controls(unittest.TestCase):
 def test_contradiction(self):
  m,c=fixture();r=verify_candidate(m,c,1,1,1);self.assertEqual(r['status'],'EXACT_CONTRADICTION_ACCEPTED');self.assertEqual(r['contradiction']['row'],2)
 def test_altered_maps(self):
  for field in ('generator_to_native','native_to_generator'):
   m,c=fixture();c[field]=[0,1,2]
   with self.assertRaises(ValueError):verify_candidate(m,c,1,1,1)
 def test_header_binding(self):
  m,c=fixture();c['model_header']=dict(kind='OTHER')
  with self.assertRaises(ValueError):verify_candidate(m,c,1,1,1)
 def test_boolean_index(self):
  with self.assertRaises(ValueError):translate(dict(steps=[dict(variable=3,value=1,row=True)]),[0])
 def test_weakening_is_arithmetic_failure(self):
  m,c=fixture();m['rows'][2]['lower']=0;b=binding(m);c['model_binding']=b;c['envelope']['model_binding']=b
  with self.assertRaisesRegex(ValueError,'not contradictory'):verify_candidate(m,c,1,1,1)
 def test_prefix_not_fixedpoint(self):
  m,c=fixture();raw=dict(status='INTERVAL_FIXED_POINT_INCONCLUSIVE',steps=c['raw_generator_certificate']['steps'][:1],evaluations=1,fixed_variables=1);c['raw_generator_certificate']=raw;c['native_certificate']=translate(raw,c['generator_to_native']);c['envelope']['certificate']=c['native_certificate'];r=verify_candidate(m,c,1,1,1);self.assertEqual(r['status'],'VALID_PREFIX_INCONCLUSIVE');self.assertFalse(r['nonexistence_proved'])
 def test_negative_coeff_degree12_control(self):
  variables=[1|(1<<j) for j in range(1,13)];rows=[row(j,[[v,1]],1,1) for j,v in enumerate(variables[:-1])];rows.append(row(12,[[v,-1 if v==variables[-1] else 1] for v in variables],-1,10));m=dict(schema_version=1,header=dict(kind='DEGREE12',n=13,constant=1),variables=variables,rows=rows);f,i=row_maps(11,0,1);steps=[dict(variable=v,value=1,row=i[j]) for j,v in enumerate(variables[:-1])]+[dict(variable=variables[-1],value=1,row=0)];raw=dict(status='INTERVAL_FIXED_POINT_INCONCLUSIVE',steps=steps,evaluations=12,fixed_variables=12);b=binding(m);nat=translate(raw,f);c=dict(model_header=m['header'],model_binding=b,generator_to_native=f,native_to_generator=i,raw_generator_certificate=raw,native_certificate=nat,envelope=dict(schema_version=1,model_binding=b,certificate=nat));r=verify_candidate(m,c,11,0,1);self.assertEqual(r['values'],[[v,1] for v in variables])
 def test_invalid_sizes_and_raw_shape(self):
  for sizes in ((True,0,1),(-1,1,1),(0,0,0)):
   with self.assertRaises(ValueError):row_maps(*sizes)
  with self.assertRaises(ValueError):translate({},[0])
  with self.assertRaises(ValueError):translate(dict(steps=[dict(variable=3,value=1,row=2)]),[0])

if __name__=='__main__':unittest.main()
