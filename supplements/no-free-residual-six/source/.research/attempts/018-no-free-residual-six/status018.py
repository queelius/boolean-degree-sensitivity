"""Progress of the L1 certificate run, read from certs/results.jsonl.

Counts the (cover case, m) obligations that run018 considers done (its own
variant bookkeeping, imported from run018), the remaining ones by part and
type, and the result statuses. Progress only: acceptance is decided by
read_all018.py, which re-reads every certificate independently.

  status018.py
"""
import json
import statistics
import sys
from collections import Counter
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from run018 import placement_key  # noqa: E402


def status(here=HERE):
    rows = json.loads((here / 'l1-cover.json').read_text())['rows']
    index = {(placement_key(r), r['type']): i for i, r in enumerate(rows)}
    logs = [here / 'certs' / 'results.jsonl', here / 'certs' / 'results-extra.jsonl']
    results = [json.loads(line) for log in logs if log.exists() for line in log.read_text().splitlines()]
    done = set()
    for r in results:
        if r['status'] != 'LRAT_VERIFIED_CORE_UNSAT':
            continue
        base = rows[r['case']]
        for t, m in r.get('variants') or [[base['type'], r['m']]]:
            j = index.get((placement_key(base), t))
            if j is not None:
                done.add((j, m))
    todo = [(i, m) for m in (1, 2) for i in range(len(rows)) if (i, m) not in done]
    walls = [r['job_wall'] for r in results if 'job_wall' in r]
    return dict(obligations=2 * len(rows), done=len(done), remaining=len(todo), certificates=len(results),
                statuses=dict(Counter(r['status'] for r in results)),
                remaining_by_part_type=dict(Counter(f"{rows[i]['part']}/{rows[i]['type']}/m{m}" for i, m in todo)),
                median_job_seconds=statistics.median(walls) if walls else None)


if __name__ == '__main__':
    print(json.dumps(status(), indent=1))
