"""Equivalent bounded low-degree coefficient coordinates for shared core words."""
from collections import Counter
from dataclasses import dataclass,replace
from baseline_full_truth_model import Row
from core_slice_degree_lp import prepare as prepare_character_model


@dataclass(frozen=True)
class BasisModel:
    base: object
    variables: tuple
    coefficient_blocks: tuple

    @property
    def variable_count(self):return len(self.variables)

    def rows(self):
        yield from self.base.rows()
        for block in self.coefficient_blocks:
            if not block['bound']:continue
            bound=block['bound'];feature=block['feature'];offset=block['offset']
            for point in range(len(self.base.word_features)):
                signs=[-1 if (point&character).bit_count()%2 else 1 for character in block['characters']]
                terms=tuple((offset+k,2*bound*sign) for k,sign in enumerate(signs))
                terms+=tuple((i,-value) for i,value in self.base.word_features[point][feature])
                target=bound*sum(signs)
                yield Row(terms,target,target,dict(kind='slice_degree_basis_value',feature=feature,point=point))

    def inventory(self):
        counts=Counter();nonzeros=rows=0
        for row in self.rows():counts[row.reason['kind']]+=1;rows+=1;nonzeros+=len(row.terms)
        estimate=(512<<20)+512*nonzeros+4096*(self.variable_count+rows)+sum(b.values.nbytes for b in self.base.blocks)
        return dict(variables=self.variable_count,word_variables=self.base.word_variable_count,
            pattern_variables=self.base.variable_count-self.base.word_variable_count,
            coefficient_variables=self.variable_count-self.base.variable_count,
            rows=rows,nonzeros=nonzeros,degree_value_rows=counts['slice_degree_basis_value'],
            rows_by_kind=dict(counts),estimated_peak_bytes=estimate,estimate_is_a_budget_guard_not_measured_memory=True)


def prepare(pools,blocks,caps):
    checked=prepare_character_model(pools,blocks,caps);base=replace(checked,caps=())
    variables=list(base.variables);coefficient_blocks=[];points=len(pools)
    for cap in checked.caps:
        bound=max(abs(int(state[cap.feature])) for pool in pools for state in pool)
        characters=[s for s in range(points) if s.bit_count()<=cap.degree] if bound else []
        offset=len(variables)
        variables.extend(dict(kind='slice_coefficient_weight',feature=cap.feature,character=s,bound=bound) for s in characters)
        coefficient_blocks.append(dict(feature=cap.feature,degree=cap.degree,bound=bound,characters=characters,offset=offset))
    return BasisModel(base,tuple(variables),tuple(coefficient_blocks))
