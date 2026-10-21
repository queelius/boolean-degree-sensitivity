"""Bounded exact Boolean case splits with literal-row certificates.

Rows are substituted only for exploration.  Every leaf retains deductions
against the original rows plus the explicit branch assumptions.
"""
from collections import Counter
import time

from exact_binary_gap_propagation import propagate, replay
from negative_free_complex import Row


def substitute(rows, values):
    reduced, indices = [], []
    for index, row in enumerate(rows):
        fixed = sum(coefficient * values[variable] for variable, coefficient in row.terms
                    if variable in values)
        terms = tuple((variable, coefficient) for variable, coefficient in row.terms
                      if variable not in values)
        low, high = row.lower - fixed, row.upper - fixed
        interval_low = sum(min(0, c) for _, c in terms)
        interval_high = sum(max(0, c) for _, c in terms)
        if low <= interval_low and interval_high <= high:
            continue
        reduced.append(Row(terms, low, high, row.reason))
        indices.append(index)
    return reduced, indices


def choose_variable(rows, values):
    scores = Counter()
    for row in rows:
        unknown = [v for v, _ in row.terms if v not in values]
        if not unknown:
            continue
        weight = 1 / (len(unknown) ** 2)
        for variable in unknown:
            scores[variable] += weight
    edges = [v for v in scores if v.bit_count() == 2]
    return max(edges or list(scores), key=lambda v: (scores[v], -v))


def solve(rows, max_nodes=31, seconds=120, first_variable=None):
    assert max_nodes >= 1 and seconds > 0
    started = time.monotonic()
    count = 0
    variables = {v for row in rows for v, _ in row.terms}

    def visit(values, steps, assumptions):
        nonlocal count
        if count >= max_nodes or time.monotonic() - started > seconds:
            return {"status": "BOUNDED_INCONCLUSIVE", "assumptions": assumptions}
        count += 1
        reduced, row_indices = substitute(rows, values)
        proof = propagate(reduced)
        local_values = replay(reduced, proof)
        current = dict(values)
        current.update(local_values)
        new_steps = steps + [dict(variable=step["variable"], value=step["value"],
                                  row=row_indices[step["row"]]) for step in proof["steps"]]
        if proof["status"] == "EXACT_INTERVAL_CONTRADICTION":
            leaf = {"status": "EXACT_INTERVAL_CONTRADICTION", "steps": new_steps,
                    "contradiction_row": row_indices[proof["contradiction_row"]],
                    "assumptions": assumptions}
            replay(rows + [Row(((v, 1),), value, value, "branch_assumption")
                           for v, value in assumptions], leaf)
            return leaf
        if len(current) == len(variables):
            assert all(row.lower <= sum(c * current[v] for v, c in row.terms) <= row.upper for row in rows)
            return {"status": "SAT_ROW_MODEL", "values": sorted(current.items()), "assumptions": assumptions}
        variable = first_variable if not assumptions and first_variable not in current and first_variable in variables else choose_variable(reduced, current)
        children = []
        for value in (0, 1):
            branch_values = dict(current)
            branch_values[variable] = value
            branch_steps = new_steps + [dict(variable=variable, value=value, row=len(rows) + len(assumptions))]
            child = visit(branch_values, branch_steps, assumptions + [[variable, value]])
            children.append(child)
            if child["status"] == "SAT_ROW_MODEL":
                # The full assignment witnesses the parent problem as well;
                # its particular successful search branch is not a premise.
                return {**child, "assumptions": assumptions}
        status = "EXACT_BRANCH_CONTRADICTION" if all(child["status"] in
                  ("EXACT_BRANCH_CONTRADICTION", "EXACT_INTERVAL_CONTRADICTION") for child in children) else "BOUNDED_INCONCLUSIVE"
        return {"status": status, "variable": variable, "zero": children[0], "one": children[1],
                "assumptions": assumptions}

    tree = visit({}, [], [])
    return {"status": tree["status"], "tree": tree, "nodes": count,
            "seconds": time.monotonic() - started, "limits": {"max_nodes": max_nodes, "seconds": seconds}}


def verify(rows, result):
    def visit(node, assumptions):
        assert node["assumptions"] == assumptions
        if node["status"] == "EXACT_INTERVAL_CONTRADICTION":
            replay(rows + [Row(((v, 1),), value, value, "branch_assumption") for v, value in assumptions], node)
        elif node["status"] == "SAT_ROW_MODEL":
            values = dict(node["values"])
            assert all(type(value) is int and value in (0, 1) for value in values.values())
            assert all(row.lower <= sum(c * values[v] for v, c in row.terms) <= row.upper for row in rows)
            assert all(values[v] == value for v, value in assumptions)
        elif "variable" in node:
            variable = node["variable"]
            assert variable not in dict(assumptions)
            visit(node["zero"], assumptions + [[variable, 0]])
            visit(node["one"], assumptions + [[variable, 1]])
            if node["status"] == "EXACT_BRANCH_CONTRADICTION":
                assert all(node[branch]["status"] in ("EXACT_INTERVAL_CONTRADICTION", "EXACT_BRANCH_CONTRADICTION")
                           for branch in ("zero", "one"))
        else:
            assert node["status"] == "BOUNDED_INCONCLUSIVE"
    assert result["status"] == result["tree"]["status"]
    visit(result["tree"], [])
