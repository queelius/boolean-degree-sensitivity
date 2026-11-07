"""Maintain one mutable navigation pointer to an immutable checked checkpoint.

Hash validation is provenance checking, not a replay of mathematical proofs.
Historical manifests and logs are never overwritten by this module.
"""
from argparse import ArgumentParser
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json


def reference(root, path):
    path = path.resolve()
    return dict(path=str(path.relative_to(root)), sha256=hashlib.sha256(path.read_bytes()).hexdigest())


def make_pointer(root, manifest, summary, objective):
    root = root.resolve()
    refs = [reference(root, p) for p in (manifest, summary, objective)]
    data = json.loads(manifest.read_text())
    assert data['status'] == 'UNRESOLVED_CHECKPOINT' and data['global_goal_complete'] is False
    assert type(data['cycle']) is int and data['cycle'] > 0
    sources = {str(Path(r['path']).resolve()): r['sha256'] for r in data['sources']}
    assert sources[str(summary.resolve())] == refs[1]['sha256']
    return dict(schema_version=1, kind='research_checkpoint_pointer', updated_at=datetime.now(timezone.utc).isoformat(),
                scope='normalized-n14-degree-at-most-5-full-origin-sensitivity', global_status='OPEN',
                cycle=data['cycle'], checkpoint=refs[0], summary=refs[1], active_objective=refs[2],
                bookkeeping_replays_mathematics=False)


def write_pointer(root, pointer):
    target = root/'current-checkpoint.json'
    if target.exists():
        existing = json.loads(target.read_text())
        assert existing.get('kind') == 'research_checkpoint_pointer' and existing.get('schema_version') == 1
    temporary = target.with_suffix('.json.partial')
    with temporary.open('x') as stream: stream.write(json.dumps(pointer, indent=2)+'\n')
    temporary.replace(target)


if __name__ == '__main__':
    p = ArgumentParser(description=__doc__)
    for name in ('root', 'manifest', 'summary', 'objective'): p.add_argument('--'+name, type=Path, required=True)
    a = p.parse_args(); pointer = make_pointer(a.root, a.manifest, a.summary, a.objective); write_pointer(a.root, pointer)
    print(json.dumps(dict(cycle=pointer['cycle'], checkpoint_sha256=pointer['checkpoint']['sha256'])))
