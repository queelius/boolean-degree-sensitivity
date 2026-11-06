"""Certificate-producing integer interval propagation for Boolean linear rows."""
from collections import defaultdict, deque


def interval(row, values, override=None):
    low = high = 0
    for variable, coefficient in row.terms:
        value = override[1] if override is not None and variable == override[0] else values.get(variable)
        if value is None:
            low += min(0, coefficient)
            high += max(0, coefficient)
        else:
            low += coefficient * value
            high += coefficient * value
    return low, high


def impossible(row, low, high):
    return low > row.upper or high < row.lower


def propagate(rows):
    watchers = defaultdict(list)
    for index, row in enumerate(rows):
        for variable, coefficient in row.terms:
            assert coefficient != 0
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
            return dict(status='EXACT_INTERVAL_CONTRADICTION', steps=steps,
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
            assert not (zero_bad and one_bad)
            if zero_bad or one_bad:
                forced.append((variable, int(zero_bad)))
        for variable, value in forced:
            assert variable not in values
            values[variable] = value
            steps.append(dict(variable=variable, value=value, row=index))
            for affected in watchers[variable]:
                if affected not in queued:
                    pending.append(affected)
                    queued.add(affected)
    return dict(status='INTERVAL_FIXED_POINT_INCONCLUSIVE', steps=steps,
                evaluations=evaluations, fixed_variables=len(values))


def replay(rows, certificate):
    values = {}
    for step in certificate['steps']:
        variable, value = step['variable'], step['value']
        assert variable not in values and value in (0, 1)
        row = rows[step['row']]
        assert variable in dict(row.terms)
        low, high = interval(row, values, (variable, 1-value))
        assert impossible(row, low, high)
        values[variable] = value
    if certificate['status'] == 'EXACT_INTERVAL_CONTRADICTION':
        row = rows[certificate['contradiction_row']]
        assert impossible(row, *interval(row, values))
    return values
