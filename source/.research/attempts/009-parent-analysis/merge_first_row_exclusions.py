"""Set assembly after proof authorities establish the exact quotient scope."""


def merge_rows(universe,excluded,new_exclusions):
    assert len(universe)==len(set(universe))
    assert set(excluded)<=set(universe) and set(new_exclusions)<=set(universe)
    combined=set(excluded)|set(new_exclusions);remaining=set(universe)-combined
    return dict(excluded=sorted(combined),remaining=sorted(remaining),
                newly_excluded=sorted(combined-set(excluded)),whole_geometry_excluded=not remaining)
