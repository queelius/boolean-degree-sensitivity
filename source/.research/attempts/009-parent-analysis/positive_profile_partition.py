"""Partition necessary degree profiles by their exact positive support and forced links."""
from collections import defaultdict


def positive_profile_groups(profiles):
    groups=defaultdict(list)
    for i,p in enumerate(profiles):
        degrees=p['degrees'];active=tuple(v for v,d in enumerate(degrees) if d)
        forced=tuple(v for v,d in enumerate(degrees) if d==3)
        groups[active,forced].append(i)
    result=[]
    for (active,forced),indices in sorted(groups.items()):
        high=[v for v in active if v not in forced]
        allowed={v:sorted({profiles[i]['degrees'][v] for i in indices}) for v in high}
        result.append(dict(active=list(active),forced=list(forced),high=high,allowed=allowed,
                           profile_indices=indices,maximum_faces=max(profiles[i]['positive_count'] for i in indices)))
    return result
