from transport_stratified_catalog import catalog_map,transport


def move(q,p):return sum(1<<p[i] for i in range(len(p)) if q>>i&1)


def test_partition_and_negative_map_direction():
    cover=dict(low_count=2,maps=[dict(pattern=[37],representative=0,map=[1,0,3,2,5,4])],
        representatives=[dict(index=0,pattern=[26])])
    index,image=catalog_map([25],[3,5],cover,n=6)
    assert index==0 and move(25,image)==26 and {image[i] for i in [3,5]}=={2,3}
    result=transport(dict(positive=[7,42],linear=[4,32],negative=[26]),image)
    assert result['negative']==[25]


def test_inverse_transport_preserves_every_character_value():
    image=[1,0,4,2,5,3]
    source=dict(positive=[7,42],linear=[4,32],negative=[26]);target=transport(source,image)
    def value(projection,x):
        return sum(k*(1-2*((q&x).bit_count()%2)) for name,k in [('positive',1),('linear',-1),('negative',-2)] for q in projection[name])
    for x in range(64):assert value(target,x)==value(source,move(x,image))
