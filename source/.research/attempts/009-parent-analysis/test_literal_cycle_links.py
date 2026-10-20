from verify_hard_low_one_cubic_cycles import literal_cycle_links
from small_link_high_cycles import small_even_links


def test_edge_subsets_equal_cycle_permutations_on_small_vertex_sets():
    for n in range(3,7):
        vertices=list(range(n));actual=list(literal_cycle_links(vertices))
        expected=[e for e in small_even_links(vertices,5) if len(e) in (4,5)]
        assert len(actual)==len(set(actual)) and set(actual)==set(expected)
