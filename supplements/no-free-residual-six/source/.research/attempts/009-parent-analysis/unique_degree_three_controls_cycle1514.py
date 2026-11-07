"""Only tiny literal sphere/patch controls; no target catalog or solver."""
from itertools import combinations,product

def need(ok,message):
 if not ok:raise ValueError(message)
def edges(triangle):return [triangle^(1<<v) for v in range(triangle.bit_length()) if triangle>>v&1]
def summary(triangles):
 vertices=set();incidence={}
 for t in triangles:
  for i in range(t.bit_length()):
   if t>>i&1:vertices.add(i)
  for e in edges(t):incidence[e]=incidence.get(e,0)+1
 return {'f_vector':[len(vertices),len(incidence),len(triangles)],'Euler':len(vertices)-len(incidence)+len(triangles),'boundary_edges':sorted(e for e,count in incidence.items() if count==1),'edge_counts':incidence}
def connected(adjacency):
 need(adjacency,'empty adjacency');seen=set();todo=[next(iter(adjacency))]
 while todo:
  v=todo.pop()
  if v in seen:continue
  seen.add(v);todo.extend(adjacency[v]-seen)
 return len(seen)==len(adjacency)
def check_sphere(n,triangles):
 need(type(n) is int and 4<=n<=10 and type(triangles) is list,'tiny typed sphere required');need(all(type(t) is int and 0<t<1<<n and t.bit_count()==3 for t in triangles) and len(set(triangles))==len(triangles),'invalid/duplicate triangles');s=summary(triangles);need(s['f_vector'][0]==n and s['Euler']==2 and all(count==2 for count in s['edge_counts'].values()),'not closed Euler2surface')
 adjacency={v:set() for v in range(n)}
 for e in s['edge_counts']:
  a,b=[v for v in range(n) if e>>v&1];adjacency[a].add(b);adjacency[b].add(a)
 need(connected(adjacency),'disconnected surface')
 for v in range(n):
  link={w:set() for w in adjacency[v]}
  for t in triangles:
   if not t>>v&1:continue
   a,b=[w for w in range(n) if w!=v and t>>w&1];link[a].add(b);link[b].add(a)
  need(all(len(neighbors)==2 for neighbors in link.values()) and connected(link),'not simple vertex-link cycle')
 return {'degrees':[len(adjacency[v]) for v in range(n)],'f_vector':s['f_vector']}
def octahedron():return sorted(sum(1<<v for v in choice) for choice in product((0,1),(2,3),(4,5)))
def stack(triangles,face,vertex):
 need(type(face) is int and face in triangles and type(vertex) is int and all(not t>>vertex&1 for t in triangles),'stack source invalid');return sorted([t for t in triangles if t!=face]+[e|(1<<vertex) for e in edges(face)])
def unstack(triangles,vertex):
 star=[t for t in triangles if t>>vertex&1];A=0
 for t in star:A|=t^(1<<vertex)
 need(len(star)==3 and A.bit_count()==3 and A not in triangles,'unstack guard');return sorted([t for t in triangles if not t>>vertex&1]+[A])
