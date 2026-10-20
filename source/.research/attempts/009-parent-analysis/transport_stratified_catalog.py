"""Transport complete degree families; these maps need not preserve a parent."""


def move(q,p):return sum(1<<p[i] for i in range(len(p)) if q>>i&1)


def catalog_map(negative,lows,cover,n=10):
    assert lows==sorted(set(lows)) and set(lows)<=set(range(2,n)) and len(lows)==cover['low_count']
    high=sorted(set(range(2,n))-set(lows));order=[0,1]+lows+high;partition=[0]*n
    for new,old in enumerate(order):partition[old]=new
    pattern=sorted(move(q,partition) for q in negative)
    entry=next(m for m in cover['maps'] if m['pattern']==pattern)
    image=[entry['map'][partition[i]] for i in range(n)]
    assert sorted(image)==list(range(n))
    assert sorted(move(q,image) for q in negative)==cover['representatives'][entry['representative']]['pattern']
    return entry['representative'],image


def transport(projection,actual_to_representative):
    image=actual_to_representative;assert sorted(image)==list(range(len(image)))
    inverse=[0]*len(image)
    for old,new in enumerate(image):inverse[new]=old
    return {name:sorted(move(q,inverse) for q in supports) for name,supports in projection.items()}
