"""Complete explicit coordinate-map cover of two-negative cubic placements."""
from itertools import combinations
from pathlib import Path
import json
from compose_class40_same_b_acceptance import Bindings
from gzip_certificate_io import read_certificate
from two_positive_conditional_orbits import coordinate_generators
from center_negative_placement_cover import orbit_cover
from verify_four_cube_pair_domains import LiteralCubeChecker

H=Path(__file__).resolve().parent


def run():
    b=Bindings();authority_path=H/'fixed-cubic-mask03-N1-exclusion-independent-manifest.json';authority=b.read(authority_path)
    assert authority['status']=='INDEPENDENTLY_VERIFIED_CONDITIONAL_CUBIC_ONE_NEGATIVE_EXCLUSION'
    parent=read_certificate(b,authority['parent']);known=dict(parent['known']);g=authority['geometry'];_,outside=LiteralCubeChecker.coordinates(g)
    full_generators=coordinate_generators(known,tuple(g['eligible_pairs']));generators=[]
    for image in full_generators:
        assert {image[v] for v in outside}==set(outside)
        generators.append([outside.index(image[v]) for v in outside])
    triples=[q for q in range(1024) if q.bit_count()==3];patterns=list(combinations(triples,2));representatives,maps=orbit_cover(patterns,generators,10)
    for name in ('cubic_negative_pair_cover.py','two_positive_conditional_orbits.py','center_negative_placement_cover.py','test_center_negative_placement_cover.py'):b.bind(H/name)
    output=H/'cubic-two-negative-position-cover-cycle108.json';assert not output.exists()
    output.write_text(json.dumps(dict(status='PROPOSED_COMPLETE_CONDITIONAL_CUBIC_TWO_NEGATIVE_POSITION_COVER',global_status='UNRESOLVED',independent_audit='PENDING',
        authority=b.bind(authority_path),geometry=g,parent=authority['parent'],core_mask=authority['core_mask'],negative_count=2,
        initial_known=parent['known'],outside=outside,coordinate_marks=g['eligible_pairs'],full_generators=full_generators,generators=generators,
        representatives=[dict(index=i,pattern=list(p)) for i,p in enumerate(representatives)],maps=maps,literal_positions=len(patterns),
        representative_count=len(representatives),canonicalizer_trusted_for_completeness=False,
        sources=[dict(path=p,sha256=d) for p,d in sorted(b.files.items())]),indent=2)+'\n')
    print(json.dumps(dict(literal_positions=len(patterns),representatives=len(representatives),generators=len(generators))),flush=True)


if __name__=='__main__':run()
