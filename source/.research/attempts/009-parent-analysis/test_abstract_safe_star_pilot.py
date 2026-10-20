from copy import deepcopy
from pathlib import Path
import json
import pytest
from abstract_safe_star_pilot import first_map
from two_positive_conditional_orbits import move
from verify_coupled_two_positive import literal_embedding


def fixture():
    data=json.loads(Path(__file__).with_name('two-positive-pair-embeddings.json').read_text())
    g=deepcopy(data['representatives'][18]);g['negative_supports']=[]
    return data['domain']['rows'],g


def test_complete_literal_first_row_relabeling():
    rows,g=fixture()
    for source,target in [(55,0),(895,56),(4255,896)]:
        mapping=first_map(rows[source],rows[target],g)
        assert sorted(mapping)==list(range(14))
        assert {move(q,mapping):k for q,k in literal_embedding(rows[source],g,g['selected_pair']).items()}==literal_embedding(rows[target],g,g['selected_pair'])
        assert all(move(p,mapping)==p for p in g['eligible_pairs'])


def test_corrupt_source_permutation_rejected():
    rows,g=fixture();changed=deepcopy(rows[55]);changed['source_to_row'][0]=changed['source_to_row'][1]
    with pytest.raises(AssertionError):first_map(changed,rows[0],g)


def test_wrong_template_rejected():
    rows,g=fixture()
    with pytest.raises(AssertionError):first_map(rows[55],rows[56],g)
