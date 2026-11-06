"""Freeze a checkpoint like save_research_checkpoint_v2, allowing named mutable
navigation documents (CLAUDE.md, AGENTS.md, the handoff) to have changed since
the predecessor.

Every pin reachable from the predecessor manifest and the authority must still
match, except a path listed in --superseded. Such a path must (a) actually be
pinned somewhere in that closure, and (b) have an entry in a navigation
snapshot file whose immutable copy hashes to exactly that pinned old hash, so
the old bytes stay recoverable. The copy is content-addressed by the closure's
own pin, so the snapshot file need not itself be in the closure; it is bound
into the new manifest. The manifest records old hash, snapshot and new
hash for each, and binds the current file. Checks raise instead of asserting,
so they hold under python -O. Hash checks are provenance, not mathematics.
"""
from argparse import ArgumentParser
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import ast
import json
from write_checkpoint_pointer import make_pointer, write_pointer

H = Path(__file__).resolve().parent
ROOT = H.parents[1]


class CheckpointError(Exception):
    pass


def require(cond, detail):
    if not cond:
        raise CheckpointError(detail)


class Bindings:
    def __init__(self, superseded=()):
        self.files, self.superseded = {}, {str(Path(p).resolve()): set() for p in superseded}

    def bind(self, path, expected=None):
        key = str(Path(path).resolve())
        if key not in self.files:
            self.files[key] = sha256(Path(key).read_bytes()).hexdigest()
        if expected is not None:
            if key in self.superseded:
                self.superseded[key].add(expected)
            else:
                require(self.files[key] == expected, 'pin mismatch: ' + key)
        return key

    def walk(self, value):
        if isinstance(value, dict):
            if isinstance(value.get('path'), str) and isinstance(value.get('sha256'), str):
                self.bind(value['path'], value['sha256'])
            for item in value.values():
                self.walk(item)
        elif isinstance(value, list):
            for item in value:
                self.walk(item)

    def read(self, path, expected=None):
        data = json.loads(Path(self.bind(path, expected)).read_text())
        self.walk(data)
        return data


def snapshot_ref(entry):
    ref = entry['snapshot']
    return ast.literal_eval(ref) if isinstance(ref, str) else ref


def supersessions(b, snapshot_paths):
    """For each superseded path, the pinned old hash and its verified snapshot."""
    snaps = {}
    for path in snapshot_paths:
        b.bind(path)
        for entry in json.loads(Path(path).read_text())['snapshots']:
            ref = snapshot_ref(entry)
            b.bind(ref['path'], ref['sha256'])
            snaps.setdefault(str(Path(entry['original_navigation_path']).resolve()), []).append(ref)
    out = []
    for key, old in sorted(b.superseded.items()):
        require(len(old) == 1, f'superseded path must be pinned with exactly one hash: {key} {sorted(old)}')
        (old,) = old
        match = [r for r in snaps.get(key, []) if r['sha256'] == old]
        require(match, 'no pinned snapshot preserves the old bytes of ' + key)
        out.append(dict(path=key, previous_sha256=old, snapshot=dict(path=str(Path(match[0]['path']).resolve()),
                        sha256=match[0]['sha256']), current_sha256=b.files[key]))
    return out


def run(cycle, previous_path, previous_digest, authority_path, summary_path, artifacts, next_cycle,
        superseded=(), snapshots=(), h=H, root=ROOT):
    b = Bindings(superseded)
    previous = b.read(previous_path, previous_digest)
    authority = b.read(authority_path)
    require(previous['status'] == 'UNRESOLVED_CHECKPOINT' and previous['cycle'] < cycle, 'bad previous checkpoint')
    require(authority['status'].startswith(('INDEPENDENTLY_VERIFIED_', 'ACCEPTED_', 'VERIFIED_ASSEMBLY_')),
            'authority not accepted: ' + authority['status'])
    summary = Path(summary_path).read_text()
    require('GLOBAL STATUS: OPEN.' in summary, 'summary must state GLOBAL STATUS: OPEN.')
    superseded_record = supersessions(b, snapshots)
    state, manifest = h / f'state-cycle{cycle}.md', h / f'cycle{cycle}-parent-manifest.json'
    require(not state.exists() and not manifest.exists(), 'checkpoint files already exist')
    state.write_text(summary)
    for path in (Path(__file__), summary_path, state, *artifacts):
        b.bind(path)
    result = dict(status='UNRESOLVED_CHECKPOINT', cycle=cycle, global_goal_complete=False,
                  previous=b.bind(previous_path), authority=b.bind(authority_path),
                  verification=dict(accepted_authority_status=authority['status'], source_integrity_checked=True,
                                    bookkeeping_replays_mathematics=False),
                  superseded_navigation=superseded_record, next_cycle_in_progress=next_cycle,
                  sources=[dict(path=p, sha256=d) for p, d in sorted(b.files.items())])
    manifest.write_text(json.dumps(result, indent=2) + '\n')
    digest = sha256(manifest.read_bytes()).hexdigest()
    with (root / 'log.md').open('a') as f:
        f.write(f'\n\n## Checkpoint {cycle} ({datetime.now(timezone.utc).isoformat()})\n\n'
                + summary.split('\n\n')[1] + '\nManifest SHA256 ' + digest + '.\n')
    rel = manifest.resolve().relative_to(root.resolve())
    (root / 'state.md').write_text(summary + f'\nAuthoritative manifest: {rel}, SHA256 {digest}.\n')
    (root / 'synthesis.md').write_text('# Current research synthesis: unresolved\n\n' + summary
                                       + '\nThis is a checkpoint in an active goal, not completion.\n')
    write_pointer(root, make_pointer(root, manifest, state, root / 'active-objective.md'))
    return dict(cycle=cycle, manifest_sha256=digest, bound_files=len(b.files), superseded=len(superseded_record))


if __name__ == '__main__':
    p = ArgumentParser(description=__doc__)
    p.add_argument('--cycle', type=int, required=True); p.add_argument('--previous', type=Path, required=True)
    p.add_argument('--previous-sha256', required=True); p.add_argument('--authority', type=Path, required=True)
    p.add_argument('--summary', type=Path, required=True); p.add_argument('--artifacts', type=Path, nargs='*', default=[])
    p.add_argument('--superseded', type=Path, nargs='*', default=[])
    p.add_argument('--snapshots', type=Path, nargs='*', default=[])
    p.add_argument('--next-cycle', type=int, required=True); a = p.parse_args()
    artifacts = a.artifacts + [H / 'save_research_checkpoint_v3.py', H / 'test_save_research_checkpoint_v3.py',
                               H / 'write_checkpoint_pointer.py']
    print(json.dumps(run(a.cycle, a.previous, a.previous_sha256, a.authority, a.summary, artifacts, a.next_cycle,
                         a.superseded, a.snapshots)))
