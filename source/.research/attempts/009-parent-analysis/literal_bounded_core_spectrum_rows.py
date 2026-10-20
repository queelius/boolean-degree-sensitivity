"""Independent integer rows for bounded coefficients and shared-word Parseval."""
from enum import Enum,auto
from literal_categorical_core_slice_rows import LiteralCategoricalRows
from literal_core_slice_rows import LiteralRows


class Kind(Enum):
    VALUE=auto()
    NORM=auto()
    TOTAL=auto()


class LiteralBoundedSpectrumRows:
    def __init__(self,pools,blocks,coefficients,totals=(),*,include_moments=True):
        self.base=LiteralCategoricalRows(pools,blocks,[]);self.variable_count=self.base.variable_count
        self.coefficients=[];self.totals=totals;self.requests=[]
        for c in sorted(coefficients,key=lambda c:(c['feature'],c['character'])):
            values=list(c['values']);assert len(values) in (1,2) and values==sorted(set(values))
            column=self.variable_count if len(values)==2 else None
            if column is not None:self.variable_count+=1
            self.coefficients.append(dict(feature=c['feature'],character=c['character'],support=c['support'],values=values,variable=column))
        self.features=sorted({r['feature'] for r in self.coefficients});self.points=self.base.base.points
        for feature in self.features:
            self.requests.extend((Kind.VALUE,feature,point) for point in range(self.points))
            if include_moments:self.requests.append((Kind.NORM,feature,None))
        self.requests.extend((Kind.TOTAL,i,None) for i in range(len(totals)))
        self.row_count=self.base.row_count+len(self.requests)

    def coefficient_records(self):return self.coefficients

    def partition_records(self):return self.base.partition_records()

    def row(self,index):
        assert type(index) is int and 0<=index<self.row_count
        if index<self.base.row_count:return self.base.row(index)
        kind,which,point=self.requests[index-self.base.row_count];terms={};constant=0;base=self.base.base
        if kind is Kind.VALUE:
            for c in self.coefficients:
                if c['feature']!=which:continue
                sign=-1 if (point&c['character']).bit_count()%2 else 1;constant-=sign*c['values'][0]
                if c['variable'] is not None:terms[c['variable']]=sign*(c['values'][-1]-c['values'][0])
            for i,state in enumerate(base.pools[point]):
                if state[which]:terms[base.word_offsets[point]+i]=-state[which]
        elif kind is Kind.NORM:
            for x,pool in enumerate(base.pools):
                for i,state in enumerate(pool):
                    if state[which]:terms[base.word_offsets[x]+i]=state[which]*state[which]
            for c in self.coefficients:
                if c['feature']!=which:continue
                low,high=c['values'][0],c['values'][-1];constant+=self.points*low*low
                if c['variable'] is not None and high*high!=low*low:terms[c['variable']]=-self.points*(high*high-low*low)
        else:
            assert kind is Kind.TOTAL;record=self.totals[which];constant=record['target']
            for support in record['supports']:
                c=next(c for c in self.coefficients if c['support']==support);constant-=c['values'][0]
                if c['variable'] is not None:terms[c['variable']]=c['values'][-1]-c['values'][0]
        return terms,constant,constant

    def inventory(self):
        base=self.base.base
        return dict(variables=self.variable_count,word_variables=base.word_count,pattern_variables=base.pattern_count,
            spectral_flags=self.variable_count-base.variable_count,rows=self.row_count,
            nonzeros=sum(len(self.row(i)[0]) for i in range(self.row_count)),categorical_rows=len(self.base.distributions),
            spectral_value_rows=sum(kind is Kind.VALUE for kind,_,_ in self.requests),
            spectral_norm_rows=sum(kind is Kind.NORM for kind,_,_ in self.requests),
            spectral_total_rows=sum(kind is Kind.TOTAL for kind,_,_ in self.requests))

    def verify(self,certificate):return LiteralRows.verify(self,certificate)
