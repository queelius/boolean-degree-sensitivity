"""Independent scalar reconstruction of full tuple-distribution equations."""
from literal_core_slice_rows import LiteralRows,DegreeEncoding,EquationKind


class LiteralCategoricalRows:
    def __init__(self,pools,blocks,caps):
        base=LiteralRows(pools,blocks,caps,encoding=DegreeEncoding.LOW_DEGREE_BASIS)
        self.base=base;self.variable_count=base.variable_count;self.coefficient_blocks=base.coefficient_blocks
        self.retained=tuple(i for i,(kind,_) in enumerate(base.requests) if kind is not EquationKind.LINK)
        self.partitions=[];self.values=[];requests=[]
        for block,(features,patterns) in enumerate(blocks):
            for point,pool in enumerate(base.pools):
                words=tuple(tuple(state[f] for f in features) for state in pool)
                candidates=tuple(tuple(int(patterns[k,point,j]) for j in range(len(features))) for k in range(len(patterns)))
                values=sorted(set(words)|set(candidates))
                counts=[dict(value=list(v),word_count=words.count(v),pattern_count=candidates.count(v)) for v in values]
                omitted=min(values,key=lambda v:(-words.count(v)-candidates.count(v),v))
                index=len(self.partitions)
                self.partitions.append(dict(block=block,point=point,features=list(features),omitted=list(omitted),groups=counts))
                self.values.append((words,candidates))
                requests.extend((index,v) for v in values if v!=omitted)
        self.distributions=tuple(requests);self.row_count=len(self.retained)+len(requests)

    def partition_records(self):return self.partitions

    def row(self,index):
        assert type(index) is int and 0<=index<self.row_count
        if index<len(self.retained):return self.base.row(self.retained[index])
        partition,value=self.distributions[index-len(self.retained)];record=self.partitions[partition]
        words,patterns=self.values[partition];w=self.base.word_offsets[record['point']];p=self.base.block_offsets[record['block']]
        terms={w+i:1 for i,v in enumerate(words) if v==value}
        terms.update({p+i:-1 for i,v in enumerate(patterns) if v==value})
        return terms,0,0

    def inventory(self):
        return dict(variables=self.variable_count,word_variables=self.base.word_count,pattern_variables=self.base.pattern_count,
            coefficient_variables=self.variable_count-self.base.word_count-self.base.pattern_count,
            rows=self.row_count,nonzeros=sum(len(self.row(i)[0]) for i in range(self.row_count)),
            degree_value_rows=sum(self.base.requests[i][0] is EquationKind.BASIS_VALUE for i in self.retained),
            categorical_rows=len(self.distributions),partitions=len(self.partitions),
            omitted_nonzeros=sum(g['word_count']+g['pattern_count'] for p in self.partitions for g in p['groups'] if g['value']==p['omitted']),
            group_memberships=sum(len(words)+len(patterns) for words,patterns in self.values))

    def verify(self,certificate):return LiteralRows.verify(self,certificate)
