# Residual-six derivative lemmas and conditional support bounds

Prepared source supplement **1.4.0** for
<https://github.com/queelius/boolean-degree-sensitivity>. Archival publication
is pending. No new version DOI is assigned in this metadata snapshot. The
predecessor1.3.0 archive, <https://doi.org/10.5281/zenodo.23539867>, does not
archive these new proofs. The existing concept family is
<https://doi.org/10.5281/zenodo.23496541>.

Alexander Richard Towell, SIUE, ORCID
[0000-0001-6443-9897](https://orcid.org/0000-0001-6443-9897), is the author.
Substantial OpenAI Codex assistance in research, code, exposition and independent
AI review is disclosed. Human peer review, formal verification and novelty are
not established.

[THEOREM.md](THEOREM.md) proves the tripled-quartic and private-tip obstructions
and the four-free coupling bound. [THREE-FREE.md](THREE-FREE.md),
[ENDPOINT.md](ENDPOINT.md), [CORE-DISKS.md](CORE-DISKS.md),
[DISK-LEMMA.md](DISK-LEMMA.md) and [UNION12.md](UNION12.md) give the complete new
three-free classification and disk argument for a conditional lower bound of
12 on the negative-quintic support union. The local disk lemma is elementary.
The Boolean support conclusions assume the explicitly named inherited
normalization and local derivative theorems, including **BASELINE_LE3**.
Their full certificate/catalog/runtime closure is not bundled or replayed.
The whole-pattern application has further unbundled graph premises, identified
in [APPLICATION.md](APPLICATION.md). The original fourteen-variable decision
problem remains open. No two-free extension is asserted here.

The active replay uses Python 3.10 or later and its standard library only:

```sh
python -S -m unittest -v test_packet test_successor
python -S -O -m unittest -v test_packet test_successor
python -S verify_packet.py --output /tmp/residual-six-new.json
python -S -O verify_packet.py --output /tmp/residual-six-new-optimized.json
```

Use fresh output names outside the packet. Copy the entire directory anywhere;
from `/`, invoke the copied adapter by its absolute path with `PYTHONPATH` unset.
No owning workspace, network, solver, NumPy, manifold catalog or old certificate
is accessed. Historical source paths are nonexecuted provenance. The retained
original endpoint CLI still rejects optimized Python; the portable adapter
calls its explicit-guard pure functions, whose behavior is tested under `-O`.

Replay checks every manifest byte and the mathematical dependency DAG, all 61
abstract allocations and 54,411 incidence cases, the complete endpoint/core/disk
control records, and exact normalized AST equality for retained original
functions and classes. These finite controls support the written arguments;
they do not replace the proofs or inherited classifications. Tests include
omission, alias, sign, noninvolution and incorrect scope controls.

[CLAIMS.json](CLAIMS.json) records mathematics independently of archival events.
[PUBLICATION-PLAN.json](PUBLICATION-PLAN.json) and [CITATION.cff](CITATION.cff)
record the lifecycle snapshot. Their validator checks consistency, not the truth of any
external publication event. Hypothetical reserved/published test fixtures do
not reserve or publish anything. Historical receipts under verification/ retain
their original scope; PREPARATION-cycle1408.json records this successor's checks.

Original code is MIT; original notes/data are CC-BY 4.0. See
[LICENSE.md](LICENSE.md), [PROVENANCE.json](PROVENANCE.json) and
[RETRIEVAL.md](RETRIEVAL.md). Third-party PDF/dataset bodies are excluded.
A future DOI would supply an archival citation, not correctness or peer review.

The [independent copied-packet review](verification/INDEPENDENT-PACKAGING-REVIEW.md)
accepted the conditional claim boundaries and fresh isolated normal/optimized
replays. It did not regenerate the inherited classifications or supply human
peer review. Its author also authored the elementary disk lemma; this packaging
review is not an independent rediscovery of every mathematical argument.
Historical preparation receipts remain unchanged. Source disclosure and archive
publication are distinct observed events; local preparation is not disclosure.
