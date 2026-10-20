"""Independent integer Parseval certificate reader for supplied scalar sets."""


def verify_energy(record,values):
    assert record['result']['status']=='EXACT_BOX_ROW_LP_CONTRADICTION' and record['core_mask']==3
    negative=record['negative'];assert len(negative) in (1,2) and negative==sorted(set(negative))
    assert all(type(q) is int and 0<q<1024 and q.bit_count()==3 for q in negative)
    Q=record['linear_count'];assert type(Q) is int and Q in range(0,11,2)
    assert len(values)==1024 and all(v and v==sorted(set(v)) for v in values) and values[0]==[4]
    assert all(values[x]==sorted(-v for v in values[x^1023]) for x in range(512))
    count=130-len(negative);metadata=record['variables'];assert len(metadata)>=count;local=[]
    for v in metadata[:count]:
        assert v['kind']=='coefficient' and type(v['support']) is int and v['support']&15==3
        assert v['role'] in ('cubic_negative','quintic_positive');local.append((v['support']>>4,-1 if v['role']=='cubic_negative' else 1))
    expected={(q,-1) for q in range(1024) if q.bit_count()==1}|{(q,1) for q in range(1024) if q.bit_count()==3 and q not in negative}
    assert set(local)==expected and len(set(local))==count
    def polynomial(x):
        return -2*sum(-1 if (q&x).bit_count()%2 else 1 for q in negative),{i:sign*(-1 if (q&x).bit_count()%2 else 1) for i,(q,sign) in enumerate(local)}
    rows=[]
    for x in range(1024):
        constant,terms=polynomial(x);rows.append((values[x][0]-constant,values[x][-1]-constant,terms))
    expected_states=[];fixed=0;energy={i:-512 for i in range(count)}
    for point in range(512):
        squares={v*v for v in values[point]}
        if len(squares)==1:fixed+=next(iter(squares));continue
        columns=list(range(count+len(expected_states),count+len(expected_states)+len(values[point])))
        expected_states.extend(dict(kind='generic_fourier_value_state',core_mask=3,outside_point=point,value=v) for v in values[point])
        rows.append((1,1,{i:1 for i in columns}));constant,terms=polynomial(point)
        terms.update({i:-v for i,v in zip(columns,values[point]) if v});rows.append((-constant,-constant,terms))
        energy.update({i:v*v for i,v in zip(columns,values[point]) if v})
    assert metadata[count:]==expected_states
    target=512*4*len(negative)-fixed;rows.append((target,target,energy))
    rows.append((Q,Q,{i:1 for i,(q,sign) in enumerate(local) if sign==-1}))
    positive=Q+4+2*len(negative);rows.append((positive,positive,{i:1 for i,(q,sign) in enumerate(local) if sign==1}))
    assert record['result']['variables']==len(metadata) and record['result']['rows']==len(rows)
    certificate=record['result']['certificate'];residual=[0]*len(metadata);rhs=0;used=set()
    for index,side,multiplier in certificate['terms']:
        assert type(index) is int and 0<=index<len(rows) and side in (-1,1) and type(multiplier) is int and multiplier>0
        low,high,terms=rows[index];rhs+=multiplier*(high if side==1 else -low);used.add(index)
        for i,k in terms.items():residual[i]+=side*multiplier*k
    for column,side,multiplier in certificate['box_terms']:
        assert type(column) is int and 0<=column<len(metadata) and side in (-1,1) and type(multiplier) is int and multiplier>0
        residual[column]+=side*multiplier
        if side==1:rhs+=multiplier
    assert not any(residual) and rhs<0 and rhs==certificate['integer_rhs']
    return dict(integer_rhs=rhs,variables=len(metadata),literal_rows=len(rows),used_rows=len(used),solver_imported=False)
