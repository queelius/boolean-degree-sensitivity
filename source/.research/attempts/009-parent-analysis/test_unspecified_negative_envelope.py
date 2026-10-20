"""Known coefficient controls; these spectra are not asserted to be Boolean."""
from itertools import combinations
from pathlib import Path
import json
from unspecified_negative_envelope import build_projection
from exact_box_row_lp import solve,verify_certificate


def coefficient_control(negative_count):
    d=json.loads(Path(__file__).with_name('two-positive-pair-embeddings.json').read_text())
    g=d['representatives'][18];core=g['positive_doubles'][0]&g['positive_doubles'][1]
    vs=[v for v in range(14) if core>>v&1];center=1<<vs[3]
    apices=[(p^core).bit_length()-1 for p in g['positive_doubles']]
    outside=apices+sorted(set(range(14))-set(vs)-set(apices))
    quadruples=list(combinations(range(10),4));chosen=quadruples[:negative_count]
    free={center|sum(1<<outside[v] for v in q) for q in chosen}
    known={p:2 for p in g['positive_doubles']};known[center]=1
    for size in (2,4):
        for q in combinations(outside,size):
            support=center|sum(1<<v for v in q)
            if support not in free:known[support]=0
    lower=[]
    for point in range(1024):
        value=1-2*sum((-1)**sum((point>>v)&1 for v in q) for q in chosen)
        values=[0]*16;values[8]=value;lower.append(values)
    return g,known,dict(outside=outside,lower=lower,upper=lower)


def test_four_negative_coefficients_are_permitted():
    variables,rows=build_projection(*coefficient_control(4),8)
    result=solve(rows,len(variables),seconds=10)
    assert result['status']=='NUMERICALLY_FEASIBLE_BOX_RELAXATION'


def test_fifth_negative_is_ruled_out_with_exact_certificate():
    variables,rows=build_projection(*coefficient_control(5),8)
    result=solve(rows,len(variables),seconds=10)
    assert result['status']=='EXACT_BOX_ROW_LP_CONTRADICTION'
    assert verify_certificate(rows,len(variables),result['certificate'])<0
