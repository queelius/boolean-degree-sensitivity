"""Shared full-face core words with endpoint spectral flags and exact moments."""
from collections import Counter
from dataclasses import dataclass
from baseline_full_truth_model import Row
from categorical_core_slice_lp import CategoricalModel,prepare as prepare_categories
from selfdual_core_projection import ProjectedCoefficient


@dataclass(frozen=True)
class CoefficientTotal:
    supports: tuple
    target: int


@dataclass(frozen=True)
class CoefficientSlot:
    coefficient: ProjectedCoefficient
    variable: int | None


@dataclass(frozen=True)
class SpectrumModel:
    base: CategoricalModel
    variables: tuple
    slots: tuple
    totals: tuple
    include_moments: bool

    @property
    def variable_count(self):return len(self.variables)

    def coefficient_records(self):
        return [dict(feature=s.coefficient.feature,character=s.coefficient.character,support=s.coefficient.support,
            values=list(s.coefficient.values),variable=s.variable) for s in self.slots]

    def rows(self):
        yield from self.base.rows();base=self.base.basis.base;points=len(base.word_features)
        for feature in sorted({s.coefficient.feature for s in self.slots}):
            slots=[s for s in self.slots if s.coefficient.feature==feature]
            for point in range(points):
                terms=[];constant=0
                for slot in slots:
                    c=slot.coefficient;sign=-1 if (point&c.character).bit_count()%2 else 1
                    constant+=c.values[0]*sign
                    if slot.variable is not None:terms.append((slot.variable,(c.values[-1]-c.values[0])*sign))
                terms.extend((i,-v) for i,v in base.word_features[point][feature])
                yield Row(tuple(terms),-constant,-constant,dict(kind='bounded_spectrum_value',feature=feature,point=point))
            if self.include_moments:
                terms=[(i,v['features'][feature]**2) for i,v in enumerate(base.variables[:base.word_variable_count]) if v['features'][feature]]
                constant=0
                for slot in slots:
                    lo,hi=slot.coefficient.values[0],slot.coefficient.values[-1];constant+=lo*lo
                    if slot.variable is not None and hi*hi!=lo*lo:terms.append((slot.variable,-points*(hi*hi-lo*lo)))
                yield Row(tuple(terms),points*constant,points*constant,dict(kind='bounded_spectrum_parseval',feature=feature))
        lookup={s.coefficient.support:s for s in self.slots}
        for ordinal,total in enumerate(self.totals):
            terms=[];constant=0
            for support in total.supports:
                slot=lookup[support];values=slot.coefficient.values;constant+=values[0]
                if slot.variable is not None:terms.append((slot.variable,values[-1]-values[0]))
            yield Row(tuple(terms),total.target-constant,total.target-constant,dict(kind='bounded_spectrum_total',total=ordinal))

    def inventory(self):
        counts=Counter();rows=nonzeros=0
        for row in self.rows():counts[row.reason['kind']]+=1;rows+=1;nonzeros+=len(row.terms)
        base=self.base.basis.base
        members=sum(len(g.words)+len(g.patterns) for p in self.base.partitions for g in p.groups)
        estimate=(512<<20)+512*nonzeros+4096*(self.variable_count+rows)+64*members+sum(b.values.nbytes for b in base.blocks)
        return dict(variables=self.variable_count,word_variables=base.word_variable_count,
            pattern_variables=base.variable_count-base.word_variable_count,spectral_flags=self.variable_count-base.variable_count,
            rows=rows,nonzeros=nonzeros,categorical_rows=counts['slice_tuple_distribution'],
            spectral_value_rows=counts['bounded_spectrum_value'],spectral_norm_rows=counts['bounded_spectrum_parseval'],
            spectral_total_rows=counts['bounded_spectrum_total'],rows_by_kind=dict(counts),
            estimated_peak_bytes=estimate,estimate_is_a_budget_guard_not_measured_memory=True)


def prepare(pools,blocks,coefficients,*,totals=(),include_moments=True):
    base=prepare_categories(pools,blocks,[]);points=len(pools);width=len(pools[0][0]);coefficients=tuple(coefficients);totals=tuple(totals)
    if type(include_moments) is not bool:raise ValueError('Moment selection must be Boolean.')
    if len({(c.feature,c.character) for c in coefficients})!=len(coefficients) or len({c.support for c in coefficients})!=len(coefficients):
        raise ValueError('Coefficient coordinates and supports must each be unique.')
    for c in coefficients:
        if type(c.feature) is not int or not 0<=c.feature<width or type(c.character) is not int or not 0<=c.character<points or type(c.support) is not int or c.support<0:
            raise ValueError('Coefficient coordinate outside the given cube.')
        if not 1<=len(c.values)<=2 or any(type(v) is not int for v in c.values) or tuple(sorted(set(c.values)))!=tuple(c.values):
            raise ValueError('Use a sorted one- or two-value integer coefficient domain.')
    supports={c.support for c in coefficients}
    if any(type(t.target) is not int or len(set(t.supports))!=len(t.supports) or not set(t.supports)<=supports for t in totals):
        raise ValueError('Coefficient totals need distinct known supports and an integer target.')
    variables=list(base.variables);slots=[]
    for c in sorted(coefficients,key=lambda c:(c.feature,c.character)):
        index=len(variables) if len(c.values)==2 else None;slots.append(CoefficientSlot(c,index))
        if index is not None:variables.append(dict(kind='full_spectral_flag',feature=c.feature,character=c.character,support=c.support,values=list(c.values)))
    return SpectrumModel(base,tuple(variables),tuple(slots),totals,include_moments)
