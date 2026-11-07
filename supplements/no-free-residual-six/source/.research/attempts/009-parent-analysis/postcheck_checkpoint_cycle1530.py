"""Check paused handoff provenance/counts; does not replay mathematics."""
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path

H = Path(__file__).resolve().parent
R = H.parents[1]


def need(condition, message):
    if not condition:
        raise ValueError(message)


def read_ref(ref, base=H):
    path = Path(ref['path'])
    path = path if path.is_absolute() else base / path
    raw = path.read_bytes()
    need(sha256(raw).hexdigest() == ref['sha256'], str(path))
    if 'bytes' in ref:
        need(len(raw) == ref['bytes'], 'Wrong byte count: ' + str(path))
    return raw


def main():
    pointer = json.loads((R / 'current-checkpoint.json').read_text())
    need(pointer['cycle'] == 1530 and pointer['global_status'] == 'OPEN', 'Pointer')
    for key in ('checkpoint', 'summary', 'active_objective'):
        read_ref(pointer[key], R)
    manifest = json.loads(read_ref(pointer['checkpoint'], R))
    for ref in manifest['sources']:
        read_ref(ref)
    status = json.loads(read_ref(manifest['status_snapshot']))
    need(status['run_status'] == 'PAUSED_BY_USER' and not status['global_goal_complete'], 'Pause/status')
    frontier = json.loads(read_ref(status['typed_signed_star_frontier']))
    need(Counter(x['genuine_context_status'] for x in frontier['entries']) ==
         Counter(OPEN=24, EXCLUDED=2), 'Genuine frontier')
    need(Counter(x['raw_row_model_status'] for x in frontier['entries']) ==
         Counter(OPEN=25, EXCLUDED=1), 'Raw frontier')
    ledger = json.loads(read_ref(status['active_original_pattern_ledger']))
    need(Counter(x['status'] for x in ledger['empty_pair']['patterns']) ==
         Counter(open=29, excluded=44), 'Original frontier')
    shutdown = json.loads(read_ref(manifest['session_shutdown']))
    need(shutdown['all_owned_experiment_processes_terminal'] and
         shutdown['producer_exit_code'] == shutdown['reader_exit_code'] == 0,
         'Nonterminal run')
    trace_ref = manifest['accepted_new_authorities']['extended-trace-authority-cycle1522.json']
    trace = json.loads(read_ref(trace_ref))
    need(trace['steps_checked'] == 344 and trace['contradiction'] is None and
         not trace['case_excluded'], 'Wrong prefix scope')
    need(pointer['active_objective']['sha256'] ==
         '56bdac0d6b282cde585f0a8b142b6deab7dcbb6e4a07cc065151915f205d1f71',
         'Objective changed')
    result = dict(schema_version=1, status='PASS', cycle=1530,
                  source_pins_rehashed=len(manifest['sources']),
                  pointer_refs_rehashed=3, run_status='PAUSED_BY_USER',
                  whole_patterns_open=29, genuine_contexts_open=24,
                  raw_row_models_open=25, verified_prefix_values=344,
                  all_owned_experiment_processes_terminal=True,
                  mathematics_or_LRAT_replayed=False,
                  old_transitive_closure_rehashed=False, global_goal_complete=False)
    with (H / 'checkpoint1530-postcheck.json').open('x') as stream:
        json.dump(result, stream, indent=2)
        stream.write('\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
