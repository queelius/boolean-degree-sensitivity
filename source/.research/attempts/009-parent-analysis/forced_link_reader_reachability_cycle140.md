# A safe reachability prune for the full-face reader

The first cycle-140 reader spends substantial time expanding branches with
no reachable final degree. No partial run is accepted as a catalog audit.

In the nonexceptional forced-link classification, restoring one low vertex
adds its three star faces and toggles its high triangle. Each of the three
affected high degrees therefore increases by either one or three; all other
high degrees stay fixed. With r restorations left, a current high degree d
must end in the interval [d,d+3r]. If none of that vertex's allowed final
degrees lies in this interval, the branch is impossible. This is a necessary
bound only; it makes no claim that every intermediate degree is reachable.
The separate exceptional tetrahedron branch is unchanged.

`verify_forced_link_cycles_v2.py` recomputes current degrees from the full
ambient face mask and applies this bound before expansion. It still restores
the low vertices in the opposite order from the producer and uses the
independent high-cycle enumeration and literal coefficient reconstruction.
It now shares this proved pruning criterion with the producer; it no longer
has the older reader's deliberate omission of the reachability bound.
`test_verify_forced_link_cycles_v2.py` checks complete six-vertex spaces for
zero through four low vertices, varied critical sets and face caps, and the
positive tetrahedron-component controls. The new catalog entry point is
`verify_singleton_stratified_catalogs_v3.py`.
