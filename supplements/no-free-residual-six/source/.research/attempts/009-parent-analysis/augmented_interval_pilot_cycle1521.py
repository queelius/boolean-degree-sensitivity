"""Only a three-block schedule and typed context/resource boundary; no engine."""
import math

from context_first_rows_cycle1438 import inverse_permutation
from gap_transcript_reader_cycle1436 import exact


def need(condition,message):
    if not condition:raise ValueError(message)


def priority_order(common_count,context_count,added_count):
    counts=(common_count,context_count,added_count)
    need(all(type(c) is int and c>=0 for c in counts) and sum(counts)>0,
         'typed nonempty row blocks')
    original=common_count+context_count
    order=list(range(original,original+added_count))+list(range(common_count,original))+list(range(common_count))
    return order,inverse_permutation(order)


def cpu_plan(setup_CPU):
    need(type(setup_CPU) in (int,float) and math.isfinite(setup_CPU) and 0<=setup_CPU<=4,
         'setup budget exceeded; no generation authorized')
    return dict(setup_stop_CPU_seconds=4,generation_CPU_budget_seconds=10,
                total_CPU_soft_seconds=14,total_CPU_hard_seconds=15)


def select_open(contexts,wanted):
    matches=[c for c in contexts if exact(c['model_id'],wanted)]
    need(len(matches)==1 and matches[0]['skip_future_queries'] is False and
         matches[0]['genuine_context_status']=='OPEN','sole exact open context required')
    return matches[0]
