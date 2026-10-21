from copy import deepcopy
import json
import pytest
from audit_empty_residual_four import SIX, check_report


def test_exact_scope_and_missing_case():
    report = json.loads((SIX/'empty-residual-four-cover.json').read_text())
    ledger = json.loads((SIX/'empty-residual-four-ledger-input.json').read_text())
    assert check_report(report, ledger)['new_patterns'] == 6
    bad = dict(report, local_cases=report['local_cases'][1:])
    with pytest.raises(AssertionError):
        check_report(bad, ledger)
    bad = deepcopy(report)
    bad['covered_open_patterns'][0]['necessary_johnson_components'] += 1
    with pytest.raises(AssertionError):
        check_report(bad, ledger)
