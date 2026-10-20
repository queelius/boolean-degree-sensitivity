from pathlib import Path
import json
from cubic_degree_profiles import degree_options
from parent00_direct_cycles import linear_for_profile


def test_profile_filter_preserves_genuine_cubic_projection_and_rejects_wrong_count():
    s=json.loads(Path(__file__).with_name('fixed-integral-cubic-pilot-cycle111.json').read_text())
    r=next(r for r in s['records'] if r['context']=='unfixed' and r['negative']==[7]);spec=r['spectrum'];positive=[q for q,k in spec if k==1]
    values=[[sum(k*(-1)**((q&(1<<i)).bit_count()) for q,k in spec)] for i in range(10)]
    choices=degree_options(10,[7],values);maps=[dict(c) for c in choices];degrees=[sum(bool(q>>i&1) for q in positive) for i in range(10)]
    linear=linear_for_profile(degrees,maps,len(positive),1)
    assert [1<<i for i,u in enumerate(linear) if u]==[q for q,k in spec if k==-1]
    assert linear_for_profile(degrees,maps,len(positive)+2,1) is None
    bad=degrees.copy();bad[0]=1;assert linear_for_profile(bad,maps,len(positive),1) is None
