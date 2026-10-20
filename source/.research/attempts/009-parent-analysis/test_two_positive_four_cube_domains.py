from pathlib import Path
import json
import numpy as np
import pytest
from two_positive_four_cube_domains import relation, supported_values, CubeIndex, setup, propagate
from two_positive_pair_domains import index_rows
from verify_coupled_two_positive import literal_embedding

H = Path(__file__).resolve().parent


@pytest.fixture(scope='module')
def data():
    return json.loads((H / 'two-positive-pair-embeddings.json').read_text())


def test_boolean_constant_control():
    assert (0, 0, 0) in relation((3, 5, 9), 3, 0)
    assert (-2, -2, -2) not in relation((3, 5, 9), 3, 0)


def test_inactive_star_negative_control():
    assert (-1, -1, -1) not in relation((3, 5, 9), 1, 1)
    assert (-1, -1, 0) in relation((3, 5, 9), 1, 1)


def test_supports_retain_only_jointly_extendible_values():
    assert supported_values(((-1, 0), (0, 1)), (6, 4)) == (2, 4)
    assert supported_values(((-1, 0),), (4, 4)) == (0, 0)


def test_row_transform_against_literal_parity(data):
    rows = [data['domain']['rows'][i] for i in (0, 56, 896)]
    cubes = CubeIndex.build(rows)
    for j, row in enumerate(rows):
        terms = {q: 1 for q in row['unit_faces']} | {13: 2, 14: 2}
        terms.update({1 << v: k for v,k in enumerate(row['linear_numerators']) if k})
        for point in range(1024):
            x = (point & 3) | ((point >> 2) << 4)
            numerator = -sum(k * (-1 if (q & x).bit_count()%2 else 1) for q,k in terms.items())
            assert numerator % 8 == 0 and cubes.table[j, point] == numerator // 8
            assert cubes.partitions(point)[numerator // 8 + 2] >> j & 1


def test_three_identical_star_rows_excluded(data):
    geometry = data['representatives'][18]
    pairs, outside = setup(geometry)
    assert len(pairs) == 3 and len(outside) == 10
    initial = {}
    for pair in geometry['eligible_pairs']:
        more = literal_embedding(data['domain']['rows'][0], geometry, pair)
        assert all(q not in initial or initial[q] == k for q,k in more.items())
        initial.update(more)
    proof = propagate(initial, geometry, index_rows(data['domain']['rows']), CubeIndex.build(data['domain']['rows']))
    assert proof['status'] == 'EXACT_FOUR_CUBE_PAIR_DOMAIN_CONTRADICTION'
    assert proof['contradiction_point'].bit_count() == 1
