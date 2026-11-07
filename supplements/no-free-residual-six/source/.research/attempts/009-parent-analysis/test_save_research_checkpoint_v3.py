import json
import tempfile
import unittest
from hashlib import sha256
from pathlib import Path

import save_research_checkpoint_v3 as w


def pin(path):
    return dict(path=str(path.resolve()), sha256=sha256(path.read_bytes()).hexdigest())


class Tree:
    """A predecessor checkpoint whose closure pins a navigation doc and its snapshot."""

    def __init__(self, base):
        self.root = base / 'root'; self.h = self.root / 'attempts' / 'H'; self.h.mkdir(parents=True)
        (self.root / 'active-objective.md').write_text('objective\n')
        (self.root / 'log.md').write_text('# log\n')
        self.nav = base / 'CLAUDE.md'; self.nav.write_text('old guidance\n')
        snap = self.h / 'claude-entry-cycle1.md'; snap.write_text('old guidance\n')
        self.snaps = self.h / 'snapshots-cycle1.json'
        self.snaps.write_text(json.dumps(dict(snapshots=[dict(original_navigation_path=str(self.nav),
                                                                snapshot=repr(pin(snap)))])))
        evidence = self.h / 'evidence.json'; evidence.write_text('{}')
        self.evidence = evidence
        self.prev = self.h / 'cycle1-parent-manifest.json'
        self.prev.write_text(json.dumps(dict(status='UNRESOLVED_CHECKPOINT', cycle=1,
                                             sources=[pin(self.nav), pin(self.snaps), pin(evidence)])))
        self.auth = self.h / 'auth.json'
        self.auth.write_text(json.dumps(dict(status='ACCEPTED_TEST', evidence=dict(e=pin(evidence)))))
        self.summary = base / 'summary.md'
        self.summary.write_text('# Checkpoint 2\n\nGLOBAL STATUS: OPEN. Test entry.\n\nMore.\n')

    def run(self, **kw):
        args = dict(superseded=[self.nav], snapshots=[self.snaps], h=self.h, root=self.root)
        args.update(kw)
        return w.run(2, self.prev, pin(self.prev)['sha256'], self.auth, self.summary, [], 3, **args)


class TestWriterV3(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.t = Tree(Path(self.tmp.name))

    def tearDown(self):
        self.tmp.cleanup()

    def test_unchanged_closure_needs_no_supersession(self):
        out = self.t.run(superseded=[], snapshots=[])
        self.assertEqual(out['superseded'], 0)

    def test_records_superseded_navigation_doc(self):
        old = pin(self.t.nav)['sha256']; self.t.nav.write_text('new guidance\n')
        out = self.t.run()
        m = json.loads((self.t.h / 'cycle2-parent-manifest.json').read_text())
        rec, = m['superseded_navigation']
        self.assertEqual(rec['previous_sha256'], old)
        self.assertEqual(rec['current_sha256'], pin(self.t.nav)['sha256'])
        self.assertTrue(rec['snapshot']['path'].endswith('claude-entry-cycle1.md'))
        self.assertIn(dict(path=str(self.t.nav.resolve()), sha256=rec['current_sha256']), m['sources'])
        self.assertEqual(out['superseded'], 1)
        self.assertIn('GLOBAL STATUS: OPEN. Test entry.\nManifest SHA256 ' + out['manifest_sha256'],
                      (self.t.root / 'log.md').read_text())
        self.assertNotIn('—', (self.t.root / 'log.md').read_text() + (self.t.root / 'synthesis.md').read_text())
        ptr = json.loads((self.t.root / 'current-checkpoint.json').read_text())
        self.assertEqual((ptr['cycle'], ptr['checkpoint']['sha256']), (2, out['manifest_sha256']))
        self.assertIn('attempts/H/cycle2-parent-manifest.json', (self.t.root / 'state.md').read_text())

    def test_unlisted_drift_rejected(self):
        self.t.nav.write_text('new guidance\n')
        with self.assertRaises(w.CheckpointError):
            self.t.run(superseded=[], snapshots=[])
        self.assertFalse((self.t.h / 'state-cycle2.md').exists())

    def test_evidence_drift_rejected_even_with_supersession(self):
        self.t.nav.write_text('new guidance\n'); self.t.evidence.write_text('{"x": 1}')
        with self.assertRaises(w.CheckpointError):
            self.t.run()

    def test_superseded_path_must_be_pinned(self):
        stray = Path(self.tmp.name) / 'stray.md'; stray.write_text('x')
        with self.assertRaises(w.CheckpointError):
            self.t.run(superseded=[stray])

    def test_snapshot_must_preserve_old_bytes(self):
        snap = self.t.h / 'claude-entry-cycle1.md'
        self.t.snaps.write_text(json.dumps(dict(snapshots=[])))
        self.t.prev.write_text(json.dumps(dict(status='UNRESOLVED_CHECKPOINT', cycle=1,
                                               sources=[pin(self.t.nav), pin(self.t.snaps), pin(snap)])))
        self.t.nav.write_text('new guidance\n')
        with self.assertRaises(w.CheckpointError):
            self.t.run()

    def test_unpinned_snapshot_file_is_content_addressed_and_bound(self):
        loose = Path(self.tmp.name) / 'loose.json'; loose.write_text(self.t.snaps.read_text())
        self.t.nav.write_text('new guidance\n')
        self.t.run(snapshots=[loose])
        m = json.loads((self.t.h / 'cycle2-parent-manifest.json').read_text())
        self.assertIn(pin(loose), m['sources'])

    def test_snapshot_with_wrong_hash_rejected(self):
        other = self.t.h / 'other.md'; other.write_text('not the old bytes\n')
        self.t.snaps.write_text(json.dumps(dict(snapshots=[dict(original_navigation_path=str(self.t.nav),
                                                                  snapshot=pin(other))])))
        self.t.prev.write_text(json.dumps(dict(status='UNRESOLVED_CHECKPOINT', cycle=1, sources=[pin(self.t.nav)])))
        self.t.nav.write_text('new guidance\n')
        with self.assertRaises(w.CheckpointError):
            self.t.run()

    def test_tampered_snapshot_copy_rejected(self):
        (self.t.h / 'claude-entry-cycle1.md').write_text('rewritten\n'); self.t.nav.write_text('new guidance\n')
        with self.assertRaises(w.CheckpointError):
            self.t.run()

    def test_existing_checkpoint_not_overwritten(self):
        (self.t.h / 'state-cycle2.md').write_text('frozen\n')
        with self.assertRaises(w.CheckpointError):
            self.t.run(superseded=[], snapshots=[])
        self.assertEqual((self.t.h / 'state-cycle2.md').read_text(), 'frozen\n')

    def test_authority_must_be_accepted(self):
        self.t.auth.write_text(json.dumps(dict(status='CANDIDATE')))
        with self.assertRaises(w.CheckpointError):
            self.t.run(superseded=[], snapshots=[])


if __name__ == '__main__':
    unittest.main()
