"""Strengthen an integer equality combination using actual normalization rows."""
from numbers import Integral
from exact_box_row_lp import verify_certificate


def integer(value):
    if not isinstance(value, Integral) or isinstance(value, bool):
        raise ValueError('Require exact integers.')
    return int(value)


def reconstruct(rows, variable_count, weights, groups):
    variable_count = integer(variable_count)
    if variable_count < 0:
        raise ValueError('Invalid variable count.')
    rows = tuple(rows); weights = [integer(w) for w in weights]
    if len(weights) != len(rows):
        raise ValueError('Require one signed integer weight per equality.')
    normalizations = {}; coefficients = [0] * variable_count; rhs = 0
    for i, (row, weight) in enumerate(zip(rows, weights)):
        lower, upper = integer(row.lower), integer(row.upper)
        if lower != upper:
            raise ValueError('Require equality rows.')
        terms = [(integer(j), integer(a)) for j, a in row.terms]
        if len(set(j for j, _ in terms)) != len(terms) or any(not 0 <= j < variable_count for j, _ in terms):
            raise ValueError('Invalid or duplicate matrix columns.')
        rhs += weight * upper
        for j, a in terms:
            coefficients[j] += weight * a
        if upper == 1 and terms and all(a == 1 for _, a in terms):
            normalizations[tuple(sorted(j for j, _ in terms))] = i
    original_box_rhs = rhs + sum(max(0, -c) for c in coefficients)
    seen = set(); normalization_rows = []; minima = []
    for group in groups:
        group = tuple(integer(j) for j in group)
        if (not group or len(set(group)) != len(group) or seen.intersection(group)
                or any(not 0 <= j < variable_count for j in group)):
            raise ValueError('Require disjoint nonempty groups of valid columns.')
        seen.update(group); key = tuple(sorted(group))
        if key not in normalizations:
            raise ValueError('The model does not contain the requested normalization equation.')
        row_index = normalizations[key]
        minimum = min(coefficients[j] for j in group)
        weights[row_index] -= minimum
        rhs -= minimum
        for j in group:
            coefficients[j] -= minimum
        normalization_rows.append(row_index); minima.append(minimum)
    row_rhs = rhs
    box = [[j, -1 if c > 0 else 1, abs(c)] for j, c in enumerate(coefficients) if c]
    rhs += sum(multiplier for _, sign, multiplier in box if sign == 1)
    result = dict(status='INCONCLUSIVE_BOX_ROW_LP',proof_verified=False,
                  original_box_rhs=original_box_rhs,integer_rhs=rhs,row_rhs=row_rhs,
                  box_correction=rhs-row_rhs,normalization_rows=normalization_rows,
                  group_minimums=minima)
    assert rhs <= original_box_rhs
    if rhs < 0:
        terms = [[i, 1 if w > 0 else -1, abs(w)] for i, w in enumerate(weights) if w]
        certificate = dict(terms=terms,box_terms=box,integer_rhs=rhs)
        verify_certificate(rows,variable_count,certificate)
        result.update(status='EXACT_BOX_ROW_LP_CONTRADICTION',proof_verified=True,certificate=certificate)
    return result
