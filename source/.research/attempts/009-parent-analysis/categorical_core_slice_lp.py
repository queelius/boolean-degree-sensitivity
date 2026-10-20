"""Complete tuple-distribution links for shared words and whole-pattern weights."""
from collections import Counter,defaultdict
from dataclasses import dataclass
from baseline_full_truth_model import Row
from core_slice_basis_lp import BasisModel,prepare as prepare_basis


@dataclass(frozen=True)
class ValueGroup:
    value: tuple
    words: tuple
    patterns: tuple


@dataclass(frozen=True)
class Partition:
    block: int
    point: int
    features: tuple
    omitted: tuple
    groups: tuple


@dataclass(frozen=True)
class CategoricalModel:
    basis: BasisModel
    partitions: tuple

    @property
    def variables(self):return self.basis.variables

    @property
    def variable_count(self):return self.basis.variable_count

    @property
    def coefficient_blocks(self):return self.basis.coefficient_blocks

    def rows(self):
        for row in self.basis.rows():
            if row.reason['kind']!='slice_component_link':yield row
        for partition in self.partitions:
            for group in partition.groups:
                if group.value==partition.omitted:continue
                terms=tuple((i,1) for i in group.words)+tuple((i,-1) for i in group.patterns)
                yield Row(terms,0,0,dict(kind='slice_tuple_distribution',block=partition.block,
                    point=partition.point,features=list(partition.features),value=list(group.value)))

    def partition_records(self):
        return [dict(block=p.block,point=p.point,features=list(p.features),omitted=list(p.omitted),
            groups=[dict(value=list(g.value),word_count=len(g.words),pattern_count=len(g.patterns)) for g in p.groups])
            for p in self.partitions]

    def inventory(self):
        counts=Counter();nonzeros=rows=0
        for row in self.rows():counts[row.reason['kind']]+=1;rows+=1;nonzeros+=len(row.terms)
        omitted=sum(len(g.words)+len(g.patterns) for p in self.partitions for g in p.groups if g.value==p.omitted)
        members=sum(len(g.words)+len(g.patterns) for p in self.partitions for g in p.groups)
        base=self.basis.base
        estimate=(512<<20)+512*nonzeros+4096*(self.variable_count+rows)+64*members+sum(b.values.nbytes for b in base.blocks)
        return dict(variables=self.variable_count,word_variables=base.word_variable_count,
            pattern_variables=base.variable_count-base.word_variable_count,
            coefficient_variables=self.variable_count-base.variable_count,rows=rows,nonzeros=nonzeros,
            degree_value_rows=counts['slice_degree_basis_value'],categorical_rows=counts['slice_tuple_distribution'],
            partitions=len(self.partitions),omitted_nonzeros=omitted,group_memberships=members,
            rows_by_kind=dict(counts),estimated_peak_bytes=estimate,estimate_is_a_budget_guard_not_measured_memory=True)


def prepare(pools,blocks,caps):
    basis=prepare_basis(pools,blocks,caps);base=basis.base;by_point=defaultdict(list)
    for i,variable in enumerate(base.variables[:base.word_variable_count]):
        by_point[variable['outside_point']].append((i,variable['features']))
    partitions=[]
    for b,(block,offset) in enumerate(zip(base.blocks,base.block_offsets)):
        for point in range(len(pools)):
            words=defaultdict(list);patterns=defaultdict(list)
            for i,state in by_point[point]:words[tuple(state[f] for f in block.features)].append(i)
            for k,values in enumerate(block.values[:,point,:]):patterns[tuple(map(int,values))].append(offset+k)
            values=sorted(words.keys()|patterns.keys())
            groups=tuple(ValueGroup(v,tuple(words[v]),tuple(patterns[v])) for v in values)
            omitted=min(groups,key=lambda g:(-len(g.words)-len(g.patterns),g.value)).value
            partitions.append(Partition(b,point,block.features,omitted,groups))
    return CategoricalModel(basis,tuple(partitions))
