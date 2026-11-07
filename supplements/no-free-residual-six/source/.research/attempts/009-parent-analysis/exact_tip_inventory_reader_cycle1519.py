"""Independent exact tip restrictions, structured provenance and semantic dedup."""
from positive_inventory_reader_cycle1512 import need,exact,derive as derive_positive,native_order
def evaluate(row,values):
 need(all(type(v) is int and v in (0,1) for v in values.values()),'typed Boolean control values')
 return row['lower']<=sum(c*values.get(m,0) for m,c in row['terms'])<=row['upper']
def derive_rows(variables,context):
 need(context['n']==13 and exact(variables,native_order(13)),'physical13 native domain')
 positives=derive_positive(variables,context);root=context['root'];triangles=context['root_link'];n=13
 edges={t^(1<<v) for t in triangles for v in range(n) if t>>v&1};vertices={v for t in triangles for v in range(n) if t>>v&1};neighbors={v:{e^(1<<v) for e in edges if e>>v&1} for v in vertices}
 need(all(len(neighbors[v]) in (3,4,5,6) for v in vertices),'signed root-link degree range')
 negatives=[]
 for v in sorted(vertices):
  if len(neighbors[v])!=6:continue
  cycle={t^(1<<v) for t in triangles if t>>v&1};adj={w:{u for e in cycle if e>>w&1 for u in range(n) if e>>u&1 and u!=w} for w in range(n) if (1<<w) in neighbors[v]}
  need(len(cycle)==6 and len(adj)==6 and all(len(a)==2 for a in adj.values()),'negative tip simple six-cycle degrees')
  seen=set();stack=[min(adj)]
  while stack:
   a=stack.pop()
   if a in seen:continue
   seen.add(a);stack.extend(adj[a]-seen)
  need(len(seen)==6,'negative tip link must be connected C6')
  negatives.append(dict(tip_vertex=v,tip_mask=1<<v,edge_mask=(1<<root)|(1<<v),degree_edge_masks=[e for e in variables if e.bit_count()==2 and e>>v&1]))
 rows=[];origins=[];indices={}
 def add(family,subject,terms,lower,upper,origin,detail=0):
  terms=sorted(terms);signature=(tuple(tuple(t) for t in terms),lower,upper);row=dict(key=dict(family=family,subject=subject,detail=detail),terms=terms,lower=lower,upper=upper)
  if signature in indices:origins[indices[signature]].append(origin)
  else:indices[signature]=len(rows);rows.append(row);origins.append([origin])
 for p in positives:
  b=p['tip_vertex'];tip=1<<b;A=p['opposite_triangle_mask'];rootedge=p['edge_mask']
  def origin(family,edge,neighbor=None):return dict(premise_key='absence_authority' if family=='POSITIVE_OPPOSITE_TRIANGLE_ABSENT' else 'positive_structure_authority',role='positive',vertex=b,exceptional_edge_mask=rootedge,edge_mask=edge if neighbor is not None else None,opposite_triangle_mask=A,neighbor=neighbor)
  family='POSITIVE_OPPOSITE_TRIANGLE_ABSENT';add(family,A,[[A,1]],0,0,origin(family,rootedge))
  family='POSITIVE_TIP_EXACT_DEGREE';add(family,tip,p['degree_row']['terms'],7,7,origin(family,rootedge))
  for j in range(n):
   if j in (root,b):continue
   pair=tip|(1<<j);terms=[[t,1] for t in variables if t.bit_count()==4 and t&pair==pair]
   need(len(terms)==55,'all quartic cofaces retained')
   if A>>j&1:family='POSITIVE_TIP_A_EDGE_VALENCE';lo=hi=5
   else:family='POSITIVE_TIP_OTHER_EDGE_VALENCE';terms.append([pair,-4]);lo=hi=0
   add(family,pair,terms,lo,hi,origin(family,pair,j))
 for neg in negatives:
  family='NEGATIVE_TIP_DEGREE_INTERVAL';origin=dict(premise_key='link_profile_authority',role='negative',vertex=neg['tip_vertex'],exceptional_edge_mask=neg['edge_mask'],edge_mask=None,opposite_triangle_mask=None,neighbor=None)
  add(family,neg['tip_mask'],[[e,1] for e in neg['degree_edge_masks']],9,11,origin)
 special={p['tip_vertex'] for p in positives+negatives};ordinary=[v for v in range(n) if v!=root and v not in special]
 for v in ordinary:
  incident=[e for e in variables if e.bit_count()==2 and e>>v&1]
  for j in range(n):
   if j==v:continue
   pair=(1<<v)|(1<<j);family='ORDINARY_VERTEX_NO_DEGREE11';origin=dict(premise_key='link_profile_authority',role='ordinary',vertex=v,exceptional_edge_mask=None,edge_mask=pair,opposite_triangle_mask=None,neighbor=j)
   add(family,1<<v,[[e,-1 if e==pair else 1] for e in incident],-1,10,origin,detail=1<<j)
 return dict(positive_tips=positives,negative_tips=negatives,ordinary_vertices=ordinary,added_rows=rows,origins=origins)
