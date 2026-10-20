from copy import deepcopy
from pathlib import Path
import gzip,json
import pytest
from verify_four_cycle_fixed_cover import check_marked_cover,check_record_cover


def fixture():
    h=Path(__file__).resolve().parent
    source=json.loads((h/'four-cycle-a0056-b0056-fixed-cover-cycle106.json').read_text())
    parent=json.loads(gzip.decompress(Path(source['parent']['path']).read_bytes()))
    cover=json.loads(Path(source['third_cover']['path']).read_text())
    rows=json.loads((h/'two-positive-pair-embeddings.json').read_text())['domain']['rows']
    return rows,source,parent,cover


def test_literal_complete_marked_cover():
    rows,source,parent,cover=fixture()
    assert check_marked_cover(rows,source['geometry'],dict(parent['known']),parent['domains'],cover)==28
    check_record_cover(cover,source['records'])


def test_missing_map_wrong_mark_and_missing_case_rejected():
    rows,source,parent,cover=fixture()
    for field in ('maps','coordinate_marks'):
        bad=deepcopy(cover);bad[field].pop()
        with pytest.raises(AssertionError):check_marked_cover(rows,source['geometry'],dict(parent['known']),parent['domains'],bad)
    with pytest.raises(AssertionError):check_record_cover(cover,source['records'][:-1])
