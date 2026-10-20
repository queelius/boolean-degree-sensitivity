"""Translate equality weights by structural identity and omitted-tuple algebra."""
from numbers import Integral


def frozen(value):
    if isinstance(value,dict):
        return (dict,tuple((k,frozen(v)) for k,v in sorted(value.items())))
    if isinstance(value,(list,tuple)):
        return (tuple,tuple(frozen(v) for v in value))
    return (type(value),value)


def transfer(source_reasons,weights,target_reasons,partitions):
    if (len(source_reasons)!=len(weights)
            or any(not isinstance(w,Integral) or isinstance(w,bool) for w in weights)):
        raise ValueError('Require one integer weight per source equality.')
    positions={}
    for i,reason in enumerate(target_reasons):
        key=frozen(reason)
        if key in positions:
            raise ValueError('Duplicate target equality identity.')
        positions[key]=i

    def locate(reason):
        key=frozen(reason)
        if key not in positions:
            raise ValueError('Required target equality is absent.')
        return positions[key]

    partition_map={}
    for p in partitions:
        key=(p['block'],p['point'],tuple(p['features']))
        values=[tuple(g['value']) for g in p['groups']]; omitted=tuple(p['omitted'])
        if key in partition_map or len(set(values))!=len(values) or omitted not in values:
            raise ValueError('Invalid or duplicate categorical partition.')
        explicit={}
        for value in values:
            if value==omitted:
                continue
            reason=dict(kind='slice_tuple_distribution',block=p['block'],point=p['point'],
                        features=p['features'],value=list(value))
            explicit[value]=locate(reason)
        word=locate(dict(kind='joint_word_normalization',outside_point=p['point']))
        pattern=locate(dict(kind='slice_pattern_normalization',block=p['block']))
        partition_map[key]=(omitted,explicit,word,pattern)
    result=[0]*len(target_reasons)
    for reason,weight in zip(source_reasons,weights):
        weight=int(weight)
        if reason['kind']!='slice_tuple_distribution':
            result[locate(reason)]+=weight
            continue
        key=(reason['block'],reason['point'],tuple(reason['features']))
        if key not in partition_map:
            raise ValueError('Source distribution has no target partition.')
        omitted,explicit,word,pattern=partition_map[key]
        value=tuple(reason['value'])
        if value==omitted:
            result[word]+=weight
            result[pattern]-=weight
            for index in explicit.values():
                result[index]-=weight
        elif value in explicit:
            result[explicit[value]]+=weight
        # A value absent from both sides of the complete partition has D_v=0.
    return result
