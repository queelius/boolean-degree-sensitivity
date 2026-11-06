"""Assemble the 26 extended signed-star native models through the pinned loaders.

Reuses attempt 009's hash-checked readers (no copies of their logic):
common rows + context rows (io.native_model) + accepted 1518/1519 added rows,
exactly as run_tip_interval_pilot_cycle1521.py does for its single context.
Sources are the pins recorded in tip-interval-parent-authorization-cycle1520.json.
"""
import sys
sys.dont_write_bytecode = True
from pathlib import Path

H = Path(__file__).resolve().parents[1] / '009-parent-analysis'
sys.path.insert(0, str(H))
import native_sat_pilot_io_cycle1457 as io          # noqa: E402
from gap_transcript_reader_cycle1436 import exact    # noqa: E402

AUTH = H / 'tip-interval-parent-authorization-cycle1520.json'


def load_sources():
    auth = io.read_pinned(dict(path=str(AUTH), sha256=io.pin(AUTH)['sha256']))
    src = auth['sources']
    return dict(auth=auth, src=src, gate=io.read_pinned(src['original_row_authority']),
                common=io.read_pinned(src['common_rows']), packet=io.read_pinned(src['context_rows']),
                inventory=io.read_pinned(src['inventory']))


def build(s, inv_context):
    """Return (model dict, inventory context) with rows translated to variable positions."""
    wanted = inv_context['model_id']
    overlay = io.unique_context(s['packet']['contexts'], wanted)
    model = io.native_model(s['common'], overlay, s['gate'], s['src']['original_row_authority'])
    n0 = len(model['rows'])
    io.need(n0 == inv_context['original_row_count'], 'original row count differs')
    io.need(inv_context['added_row_native_ids'] == list(range(n0, n0 + len(inv_context['added_rows']))),
            'added row ids differ')
    rows = model['rows'] + inv_context['added_rows']
    io.need(len(rows) == inv_context['extended_row_count'] and
            sum(len(r['terms']) for r in rows) == inv_context['extended_nonzero_coefficients'],
            'extended dimensions differ')
    position = {mask: i for i, mask in enumerate(model['variables'])}
    io.need(len(position) == len(model['variables']), 'aliased variable masks')
    out = []
    for r in rows:
        io.need(type(r['lower']) is int and type(r['upper']) is int and r['lower'] <= r['upper'], 'typed bounds')
        terms = [(position[m], c) for m, c in r['terms']]
        io.need(len({v for v, _ in terms}) == len(terms) and all(type(c) is int and c for _, c in terms),
                'row terms aliased or zero')
        out.append((terms, r['lower'], r['upper'], r['key']))
    return dict(model_id=wanted, variables=model['variables'], rows=out,
                status=inv_context['genuine_context_status'], raw_status=inv_context['raw_row_model_status'])


def violated(m, values):
    """Exact check of a 0/1 vector against every row; returns indices of violated rows."""
    bad = []
    for k, (terms, lo, hi, _) in enumerate(m['rows']):
        s = sum(c * values[v] for v, c in terms)
        if not lo <= s <= hi:
            bad.append(k)
    return bad


def label(model_id):
    ni = model_id['native_identity']
    return f"o{ni['order']}-i{ni['original_index']}-c{model_id['constant']}"
