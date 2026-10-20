from pathlib import Path
import gzip,json
import pytest
from four_cycle_fixed_cover import marked_cover
from verify_coupled_two_positive import literal_embedding
from verify_two_positive_conditional_orbits import relabel


def fixture():
    h=Path(__file__).resolve().parent
    a=json.loads((h/'safe-four-cycle-second-frontier-independent-manifest.json').read_text());first=next(r for r in a['records'] if r['first_row']==56);child=next(r for r in first['records'] if r['second_row']==56)
    parent=json.loads(gzip.decompress(Path(child['proof']['path']).read_bytes()));g=a['geometry']
    pair=next(d['pair'] for d in parent['domains'] if len(d['rows'])>1);candidates=next(d['rows'][:3] for d in parent['domains'] if d['pair']==pair)
    rows=json.loads((h/'two-positive-pair-embeddings.json').read_text())['domain']['rows']
    return rows,g,dict(parent['known']),pair,candidates


def test_explicit_maps_cover_every_requested_row():
    rows,g,known,pair,candidates=fixture();cover=marked_cover(g,rows,known,pair,candidates)
    assert [r['source_row'] for r in cover['maps']]==candidates
    for witness in cover['maps']:
        target=cover['representatives'][witness['representative']]['row'];image=tuple(witness['map'])
        assert {relabel(q,image):k for q,k in literal_embedding(rows[witness['source_row']],g,pair).items()}==literal_embedding(rows[target],g,pair)


def test_duplicate_input_rejected():
    rows,g,known,pair,candidates=fixture()
    with pytest.raises(AssertionError):marked_cover(g,rows,known,pair,candidates+candidates[:1])
