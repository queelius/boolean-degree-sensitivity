"""Exact Boolean interval deductions, including two-infeasible-value gaps.

Certificates use the existing replay format.  A value is inferred from the
impossibility of its alternative, even if it is also itself impossible;
the immediately revisited row then records the contradiction.
"""
from collections import defaultdict, deque
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "009-parent-analysis"))
from exact_binary_row_propagation import interval, impossible, replay


def propagate(rows):
    watchers = defaultdict(list)
    for index, row in enumerate(rows):
        for variable, coefficient in row.terms:
            assert coefficient
            watchers[variable].append(index)
    values, steps = {}, []
    pending = deque(range(len(rows)))
    queued = set(pending)
    evaluations = 0
    while pending:
        index = pending.popleft()
        queued.remove(index)
        row = rows[index]
        low, high = interval(row, values)
        evaluations += 1
        if impossible(row, low, high):
            return dict(status="EXACT_INTERVAL_CONTRADICTION", steps=steps,
                        contradiction_row=index, contradiction_interval=[low, high],
                        evaluations=evaluations, fixed_variables=len(values))
        forced = []
        for variable, coefficient in row.terms:
            if variable in values:
                continue
            base_low = low - min(0, coefficient)
            base_high = high - max(0, coefficient)
            zero_bad = impossible(row, base_low, base_high)
            one_bad = impossible(row, base_low + coefficient, base_high + coefficient)
            if zero_bad or one_bad:
                forced.append((variable, int(zero_bad)))
                if zero_bad and one_bad:
                    # Recheck this gap immediately; the usual literal-row
                    # checker independently verifies both inference and clash.
                    break
        for variable, value in forced:
            assert variable not in values
            values[variable] = value
            steps.append(dict(variable=variable, value=value, row=index))
            for affected in watchers[variable]:
                if affected not in queued:
                    pending.append(affected)
                    queued.add(affected)
    return dict(status="INTERVAL_FIXED_POINT_INCONCLUSIVE", steps=steps,
                evaluations=evaluations, fixed_variables=len(values))
