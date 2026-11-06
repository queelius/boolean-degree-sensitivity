"""Explicit exact interval transcript reader. No generator or legacy replay imports.

The caller must obtain expected_binding from independently accepted native rows.
A matching digest binds identity/order; it does not itself validate mathematics.
"""
import argparse
import hashlib
import json
from pathlib import Path

def need(ok,message):
 if not ok:raise ValueError(message)

def digest(value):
 return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False).encode()).hexdigest()

def compile_model(model):
 need(type(model) is dict and set(model)=={'schema_version','header','variables','rows'},'structured exact model required')
 need(type(model['schema_version']) is int and model['schema_version']==1,'unsupported model schema')
 header=model['header'];need(type(header) is dict and type(header.get('kind')) is str and header['kind']!='','typed model kind required')
 if 'n' in header:need(type(header['n']) is int and header['n']>0,'typed physical order required')
 if 'constant' in header:need(type(header['constant']) is int,'typed constant required')
 variables=model['variables'];need(type(variables) is list and all(type(v) is int and v>0 for v in variables) and len(variables)==len(set(variables)),'ordered unique integer variables required')
 domain=set(variables);source=model['rows'];need(type(source) is list,'ordered literal rows required');rows=[];keys=set()
 for row in source:
  need(type(row) is dict and set(row)=={'key','terms','lower','upper'},'row fields differ')
  key=row['key'];need(type(key) is dict and set(key)=={'family','subject','detail'},'row identity fields differ')
  need(type(key['family']) is str and key['family']!='' and type(key['subject']) is int and key['subject']>=0 and type(key['detail']) is int and key['detail']>=0,'invalid row identity')
  identity=key['family'],key['subject'],key['detail'];need(identity not in keys,'duplicate row identity');keys.add(identity)
  need(type(row['lower']) is int and type(row['upper']) is int and row['lower']<=row['upper'],'integer inclusive bounds required')
  need(type(row['terms']) is list,'literal term list required');terms=[];last=-1
  for term in row['terms']:
   need(type(term) is list and len(term)==2,'term shape differs');v,c=term
   need(type(v) is int and v in domain and v>last and type(c) is int and c!=0,'typed ordered unique nonzero term required')
   terms.append((v,c));last=v
  rows.append((tuple(terms),row['lower'],row['upper']))
 return domain,rows

def _binding(model):
 return {'schema_version':1,'header_sha256':digest(model['header']),'variables_sha256':digest(model['variables']),'rows_sha256':digest(model['rows']),'variables':len(model['variables']),'rows':len(model['rows'])}

def binding(model):
 compile_model(model);return _binding(model)

def exact(a,b):
 return type(a) is type(b) and (len(a)==len(b) and all(exact(x,y) for x,y in zip(a,b)) if type(a) is list else a.keys()==b.keys() and all(exact(a[k],b[k]) for k in a) if type(a) is dict else a==b)

def interval(row,values,opposite=None):
 low=high=0
 for variable,coefficient in row[0]:
  value=opposite[1] if opposite is not None and variable==opposite[0] else values.get(variable)
  if value is None:
   low+=min(0,coefficient);high+=max(0,coefficient)
  else:low+=coefficient*value;high+=coefficient*value
 return low,high

def disjoint(row,bounds):
 return bounds[0]>row[2] or bounds[1]<row[1]

def row_index(index,rows):
 need(type(index) is int and 0<=index<len(rows),'native row index invalid');return rows[index]

def verify(model,envelope,expected_binding):
 domain,rows=compile_model(model);actual=_binding(model)
 need(exact(actual,expected_binding),'accepted native header/variables/rows binding differs')
 need(type(envelope) is dict and set(envelope)=={'schema_version','model_binding','certificate'} and type(envelope['schema_version']) is int and envelope['schema_version']==1,'transcript envelope differs')
 need(exact(envelope['model_binding'],actual),'transcript bound to different native model')
 cert=envelope['certificate'];need(type(cert) is dict,'structured certificate required')
 status=cert.get('status');need(status in ('EXACT_INTERVAL_CONTRADICTION','INTERVAL_FIXED_POINT_INCONCLUSIVE'),'unsupported or incomplete generator outcome')
 required={'status','steps','evaluations','fixed_variables'}
 if status=='EXACT_INTERVAL_CONTRADICTION':required|={'contradiction_row','contradiction_interval'}
 need(set(cert)==required,'certificate fields differ')
 need(type(cert['steps']) is list and type(cert['evaluations']) is int and cert['evaluations']>=0 and type(cert['fixed_variables']) is int,'typed transcript metadata required')
 values={};checked=[]
 for position,step in enumerate(cert['steps']):
  need(type(step) is dict and set(step)=={'variable','value','row'},'step fields differ')
  variable,value=step['variable'],step['value'];need(type(variable) is int and variable in domain and variable not in values,'unknown or repeated native variable')
  need(type(value) is int and value in (0,1),'literal Boolean value required');row=row_index(step['row'],rows)
  need(any(v==variable for v,c in row[0]),'variable absent from cited native row')
  bounds=interval(row,values,(variable,1-value));need(disjoint(row,bounds),'opposite value not independently impossible')
  checked.append({'step':position,'variable':variable,'value':value,'row':step['row'],'opposite_interval':list(bounds)})
  values[variable]=value
 need(cert['fixed_variables']==len(values),'fixed count differs')
 contradiction=None
 if status=='EXACT_INTERVAL_CONTRADICTION':
  row=row_index(cert['contradiction_row'],rows);bounds=interval(row,values);claimed=cert['contradiction_interval']
  need(type(claimed) is list and len(claimed)==2 and all(type(x) is int for x in claimed) and claimed==list(bounds),'final literal interval differs')
  need(disjoint(row,bounds),'final row is not contradictory');contradiction={'row':cert['contradiction_row'],'interval':list(bounds),'bounds':[row[1],row[2]]}
 return {'status':'EXACT_CONTRADICTION_ACCEPTED' if contradiction is not None else 'VALID_PREFIX_INCONCLUSIVE','model_binding':actual,'fixed_variables':len(values),'values':[[v,x] for v,x in sorted(values.items())],'steps_checked':checked,'contradiction':contradiction,'nonexistence_proved':contradiction is not None,'scope':'Only this exact bound Boolean row system; not an actual14-variable function or whole case cover.','global_goal_complete':False}

def check_assignment(model,assignment):
 domain,rows=compile_model(model);need(type(assignment) is dict and all(type(v) is int and type(x) is int and x in (0,1) for v,x in assignment.items()) and set(assignment)==domain,'complete typed Boolean assignment required')
 return all(low<=sum(c*assignment[v] for v,c in terms)<=high for terms,low,high in rows)

def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--self-test-invalid',type=Path);parser.add_argument('--model',type=Path);parser.add_argument('--envelope',type=Path);parser.add_argument('--expected-binding',type=Path);parser.add_argument('--output',type=Path);args=parser.parse_args()
 if args.self_test_invalid is not None:binding(json.loads(args.self_test_invalid.read_text()));raise ValueError('malformed control was not rejected')
 need(all(x is not None for x in [args.model,args.envelope,args.expected_binding,args.output]),'all exact input/output paths required')
 result=verify(json.loads(args.model.read_text()),json.loads(args.envelope.read_text()),json.loads(args.expected_binding.read_text()))
 with args.output.open('x') as stream:json.dump(result,stream,indent=2);stream.write('\n')
if __name__=='__main__':main()
