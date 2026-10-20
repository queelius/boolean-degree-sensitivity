from itertools import combinations
from pathlib import Path
import json
from parent00_cubic_cycles import cycle_basis,gray_cycles,stellar


def test_coning_basis_matches_complete_small_binary_cycle_space():
    vertices=list(range(5));triangles,basis=cycle_basis(vertices);actual=set(gray_cycles(basis));expected=set()
    pairs=[sum(1<<i for i in p) for p in combinations(vertices,2)]
    for code in range(1<<len(triangles)):
        faces=[q for i,q in enumerate(triangles) if code>>i&1]
        if all(sum(q&p==p for q in faces)%2==0 for p in pairs):expected.add(code)
    assert actual==expected and len(actual)==16


def test_stellar_removal_reconstructs_genuine_both_apex_projection():
    s=json.loads(Path(__file__).with_name('fixed-integral-cubic-pilot-cycle111.json').read_text())
    r=next(r for r in s['records'] if r['context']=='unfixed' and r['negative']==[7]);positive={q for q,k in r['spectrum'] if k==1};center=2
    containing={q for q in positive if q>>center&1};assert len(containing)==3
    face=0
    for q in containing:face|=q^(1<<center)
    base=(positive-containing)|{face};assert stellar(base,face,center)==positive
