"""Independent native positive-tip restrictions; no producer/SAT imports."""
from itertools import combinations
def need(ok,message):
 if not ok:raise ValueError(message)
def exact(a,b):
 if type(a) is not type(b):return False
 if type(a) is list:return len(a)==len(b) and all(exact(x,y) for x,y in zip(a,b))
 if type(a) is dict:return a.keys()==b.keys() and all(exact(a[k],b[k]) for k in a)
 return a==b
def native_order(n):
 need(type(n) is int and 5<=n<=13,'typed dimension5..13')
 return [sum(1<<v for v in c) for k in (2,3,4) for c in combinations(range(n),k)]
def transport(mask,permutation):
 need(type(mask) is int and mask>=0 and type(permutation) is list and all(type(v) is int for v in permutation) and sorted(permutation)==list(range(len(permutation))) and mask<1<<len(permutation),'literal permutation')
 return sum(1<<permutation[v] for v in range(len(permutation)) if mask>>v&1)
def derive(variables,context):
 n=context['n'];root=context['root'];triangles=context['root_link'];need(type(root) is int and type(n) is int and 0<=root<n and variables==native_order(n),'exact native variable order/root')
 need(type(triangles) is list and triangles and all(type(t) is int and 0<t<1<<n and t.bit_count()==3 and not t>>root&1 for t in triangles) and len(set(triangles))==len(triangles),'literal distinct root-link triangles')
 edges={t^(1<<v) for t in triangles for v in range(n) if t>>v&1};vertices={v for t in triangles for v in range(n) if t>>v&1};order=context['model_id']['native_identity']['order'];need(type(order) is int and len(vertices)==order,'root-link original order')
 rows=[]
 for v in sorted(vertices):
  neighbors={e^(1<<v) for e in edges if e>>v&1}
  if len(neighbors)!=3:continue
  opposite=sum(neighbors);cycle={t^(1<<v) for t in triangles if t>>v&1};expected={sum(s) for s in combinations(neighbors,2)}
  need(cycle==expected and len(cycle)==3 and opposite.bit_count()==3,'degree3 tip must have exact triangular link')
  tip=1<<v;degree=dict(lower=7,upper=n-1,terms=[[e,1] for e in variables if e.bit_count()==2 and e&tip])
  need(len(degree['terms'])==n-1,'all physical edge slots required')
  rows.append(dict(tip_vertex=v,tip_mask=tip,edge_mask=(1<<root)|tip,opposite_triangle_mask=opposite,unit_value=0,degree_row=degree))
 return rows
