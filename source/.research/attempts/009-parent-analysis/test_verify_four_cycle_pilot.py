from copy import deepcopy
from pathlib import Path
import json,gzip
import pytest
from verify_four_cycle_pilot import check_cycle,check_second


def fixture():
    h=Path(__file__).resolve().parent
    source=json.loads((h/'abstract-safe-four-cycle-second-pilot-cycle105.json').read_text());record=source['records'][0]
    rows=json.loads((h/'two-positive-pair-embeddings.json').read_text())['domain']['rows']
    cover=json.loads(Path(record['cover']['path']).read_text());parent=json.loads(gzip.decompress(Path(record['parent']['path']).read_bytes()))
    return rows,source['geometry'],dict(parent['known']),parent['domains'],cover


def test_valid_cycle_and_complete_conditional_cover():
    rows,g,known,domains,cover=fixture();check_cycle(g)
    assert check_second(rows,g,known,domains,cover)==len(cover['representatives'])


def test_wrong_graph_or_incomplete_cover_rejected():
    rows,g,known,domains,cover=fixture();bad=deepcopy(g);bad['eligible_pairs'].pop()
    with pytest.raises(AssertionError):check_cycle(bad)
    bad=deepcopy(cover);bad['maps'].pop()
    with pytest.raises(AssertionError):check_second(rows,g,known,domains,bad)
