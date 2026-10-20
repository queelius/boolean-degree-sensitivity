"""Derive a component index from its common local-core coordinate structure."""


def component_for_pair(geometry,instance,pair):
    core=geometry['positive_doubles'][0]&geometry['positive_doubles'][1]
    assert core.bit_count()==4 and pair.bit_count()==2 and pair&core==pair
    vertices=[v for v in range(core.bit_length())if core>>v&1]
    local=sum(1<<i for i,v in enumerate(vertices)if pair>>v&1)
    assert [c['local_core_pair']for c in instance['components']]==instance['core_pair_order']
    assert len(set(instance['core_pair_order']))==len(instance['core_pair_order'])
    return instance['core_pair_order'].index(local)
