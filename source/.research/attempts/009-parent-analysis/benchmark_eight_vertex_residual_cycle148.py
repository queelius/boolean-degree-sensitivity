"""Measure the eight-vertex residual family needed for the hard L=1 branch."""
from pathlib import Path
from collections import Counter
from time import monotonic
import hashlib,json
import numpy as np
from small_link_high_cycles import bounded_high_codes


def run():
    start=monotonic();caps=[7,7,7,6,5,5,5,5];codes=[];hist=Counter()
    for code,weight,degrees in bounded_high_codes(list(range(8)),7,caps,14):
        codes.append(code);hist[weight]+=1
    assert len(codes)==len(set(codes));codes=np.array(sorted(codes),dtype=np.uint64)
    data=Path('eight-vertex-residual-pilot-cycle148.npy');output=Path('eight-vertex-residual-pilot-cycle148.json')
    assert not data.exists() and not output.exists();np.save(data,codes)
    result=dict(status='MEASURED_EIGHT_VERTEX_RESIDUAL_PILOT',global_status='UNRESOLVED',
        independent_audit='PENDING',accepted_exclusions=0,vertices=list(range(8)),anchor=7,
        maximum=caps,maximum_faces=14,cycles=len(codes),weights=dict(hist),seconds=monotonic()-start,
        data=dict(path=str(data.resolve()),sha256=hashlib.sha256(data.read_bytes()).hexdigest()),
        script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        kernel_sha256=hashlib.sha256(Path('small_link_high_cycles.py').read_bytes()).hexdigest())
    output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True)


if __name__=='__main__':run()
