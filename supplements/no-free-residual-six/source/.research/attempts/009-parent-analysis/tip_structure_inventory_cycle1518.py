"""Typed necessary local rows; preserves accepted1511 physical identities."""
import json

from positive_tip_inventory_cycle1511 import derive_context, require


def exact(a,b):
    return json.dumps(a,sort_keys=True,separators=(',',':'),allow_nan=False) == \
           json.dumps(b,sort_keys=True,separators=(',',':'),allow_nan=False)


def rows_for_context(context, variables):
    require(context['n'] == 13 and type(context['n']) is int, 'thirteen physical coordinates')
    rebuilt=derive_context(context,variables)
    require(exact(rebuilt['positive_tips'],context['positive_tips']), 'accepted positive-tip identities')
    root=context['root'];root_mask=1<<root;n=context['n']
    positions={m:i for i,m in enumerate(variables)}
    pairs=[m for m in variables if m.bit_count()==2]
    quartics=[m for m in variables if m.bit_count()==4]
    rows=[];provenance=[];seen={};occurrences=0

    def add(family,subject,terms,lower,upper,origin,detail=0):
        nonlocal occurrences
        occurrences+=1
        terms=sorted(terms)
        require(len({m for m,a in terms})==len(terms) and
                all(m in positions and type(a) is int and a != 0 for m,a in terms),
                'literal distinct native row terms')
        row=dict(key=dict(family=family,subject=subject,detail=detail),
                 terms=terms,lower=lower,upper=upper)
        signature=(tuple(map(tuple,terms)),lower,upper)
        if signature in seen:
            index=seen[signature]
            require(exact(rows[index],row), 'identical literal row with inconsistent key')
            provenance[index].append(origin)
        else:
            seen[signature]=len(rows);rows.append(row);provenance.append([origin])

    for p in rebuilt['positive_tips']:
        tip=p['tip'];tipmask=p['tip_mask'];opposite=p['opposite_triangle_mask']
        base=dict(role='positive',vertex=tip,exceptional_edge_mask=root_mask|tipmask,
                  opposite_triangle_mask=opposite,neighbor=None,edge_mask=None)
        add('POSITIVE_OPPOSITE_TRIANGLE_ABSENT',opposite,[[opposite,1]],0,0,
            dict(base,premise_key='absence_authority'))
        incident=[[m,1] for m in pairs if m&tipmask]
        add('POSITIVE_TIP_EXACT_DEGREE',tipmask,incident,7,7,
            dict(base,premise_key='positive_structure_authority'))
        for neighbor in range(n):
            if neighbor in (root,tip):
                continue
            pair=tipmask|(1<<neighbor)
            cofaces=[[q,1] for q in quartics if q&pair==pair]
            require(len(cofaces)==55, 'all pair-containing native quartics')
            origin=dict(base,premise_key='positive_structure_authority',neighbor=neighbor,edge_mask=pair)
            if opposite>>neighbor&1:
                add('POSITIVE_TIP_A_EDGE_VALENCE',pair,cofaces,5,5,origin)
            else:
                add('POSITIVE_TIP_OTHER_EDGE_VALENCE',pair,cofaces+[[pair,-4]],0,0,origin)
    negative_tips=[]
    for edge in rebuilt['special_edges']:
        if edge['valence'] != 6:
            continue
        tipmask=edge['pair_mask']^root_mask
        require(tipmask.bit_count()==1 and edge['quadratic_numerator']==-2, 'negative tip star')
        tip=tipmask.bit_length()-1
        incident=sorted(m for m in pairs if m&tipmask)
        negative_tips.append(dict(tip=tip,tip_mask=tipmask,negative_edge_mask=edge['pair_mask'],
            degree_edge_masks=incident,native_degree_variable_indices=[positions[m] for m in incident]))
        add('NEGATIVE_TIP_DEGREE_INTERVAL',tipmask,[[m,1] for m in incident],9,11,
            dict(premise_key='link_profile_authority',role='negative',vertex=tip,
                 exceptional_edge_mask=edge['pair_mask'],opposite_triangle_mask=None,
                 neighbor=None,edge_mask=None))
    exceptional_tips={(e['pair_mask']^root_mask).bit_length()-1 for e in rebuilt['special_edges']}
    ordinary_vertices=[v for v in range(n) if v!=root and v not in exceptional_tips]
    for vertex in ordinary_vertices:
        vmask=1<<vertex
        for neighbor in range(n):
            if neighbor==vertex:
                continue
            pair=vmask|(1<<neighbor)
            terms=[[m,-1 if m==pair else 1] for m in pairs if m&vmask]
            add('ORDINARY_VERTEX_NO_DEGREE11',vmask,terms,-1,10,
                dict(premise_key='link_profile_authority',role='ordinary',vertex=vertex,
                     exceptional_edge_mask=None,opposite_triangle_mask=None,
                     neighbor=neighbor,edge_mask=pair),detail=1<<neighbor)
    return dict(added_rows=rows,row_provenance=provenance,
        native_term_variable_indices=[[positions[m] for m,a in r['terms']] for r in rows],
        negative_tips=negative_tips,ordinary_vertices=ordinary_vertices,
        row_occurrences_before_deduplication=occurrences,
        duplicate_row_occurrences=occurrences-len(rows),
        added_nonzero_coefficients=sum(len(r['terms']) for r in rows))
