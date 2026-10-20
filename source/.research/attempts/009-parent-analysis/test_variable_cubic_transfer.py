from pathlib import Path
import gzip,json
from variable_cubic_transfer import extract


def test_exact_identity_recomputes_reference_and_does_not_exclude_wide_bounds():
    path=Path(__file__).with_name('parent00-second-coefficient-pilot-cycle114')/'r07-p118-j00-e0.json.gz'
    record=json.loads(gzip.decompress(path.read_bytes()));identity=extract(record)
    assert identity.evaluate(record['values'],1)==record['result']['certificate']['integer_rhs']<0
    assert identity.evaluate([[-16,16]]*1024,1)>=0
    assert identity.evaluate(record['values'],2)-identity.evaluate(record['values'],1)==identity.negative_count_weight
    sparse={x:record['values'][x] for x in identity.points()};assert identity.evaluate(sparse,1)==identity.evaluate(record['values'],1)
