**Try `certify(..., seed_k=3)` first.** My bounded checks strongly favor changing the row selection. Splitting this case is unnecessary unless the new selection also fails with LRAT enabled.

I did not write files or read/decompress the partial proof. All solver checks used one worker and limits of 30 seconds or less.

1. **What makes the existing core difficult**

Case 754 is `B-ord`, deltahedron index 3, order 9, with **Q = {2,4,5,7} and no departure pair**. All four Q vertices have degree 5 in the root link. Their induced graph is the path `2–4–5–7`, containing no triangular face.

This differs substantially from case 753, whose Q contains three root non-neighbours. Nearby cases 755 and 756 also put all Q vertices in the link: 755 contains the face `{2,4,8}`, while 756 induces a four-cycle. These differences plausibly affect local propagation, but I cannot identify the geometry alone as the cause.

The stronger diagnostic is the selected core:

- 464 rows: 176 triple, 167 value, 118 flag, and 3 degree-cap rows.
- No pair, vertex, constant, or implied rows.
- One value row, on **X = {1,…,9}**, has 253 terms and contributes **17,928 of 34,660 auxiliary variables**.
- The whole CNF has 35,825 variables and 68,137 clauses—smaller than the neighbouring successful CNFs.

I reproduced that CNF and its labels **exactly**, rebuilt all 464 rows using `reader018`, and passed its clause-soundness check.

CP-SAT found this stored core infeasible in **3.06 s**. Removing the size-9 row makes it satisfiable: I independently evaluated the returned assignment against all remaining 463 rows; every row holds, while the removed row evaluates to **1**, outside its required interval **[-6,-4]**.

Thus the large row is essential to this particular core. CP-SAT can reason with the linear constraints directly; CaDiCaL must recover the contradiction through their decision-diagram encoding. This is consistent with the parity/cardinality reasoning limitations discussed in [CaDiCaL’s README](https://github.com/arminbiere/cadical). The exact explanation remains an inference, but the evidence points to a difficult encoding of a particular core rather than excessive CNF size.

2. **Recommended certificate route and alternatives**

Here are my **proof-free** CaDiCaL results, using the installed binary and CNFs constructed entirely in memory:

| Row selection | Rows | Clauses | CaDiCaL wall time |
|---|---:|---:|---:|
| Direct `seed_k=3` | 2,523 | 274,947 | UNSAT, 6.80 s |
| Direct `seed_k=4` | 3,238 | 326,361 | UNSAT, 7.22 s |
| Direct `seed_k=5` | 4,525 | 749,480 | UNSAT, 13.56 s |
| CP-SAT core extracted from seed 3 | 1,437 | 96,538 | UNSAT, 2.68 s |

These are diagnostics, **not certificates**. I did not measure LRAT overhead.

**First choice: existing `seed_k=3`.** In [certify018.py](/home/spinoza/github/math-theory/.research/attempts/018-no-free-residual-six/certify018.py:100), this means every non-value row plus value rows with `|X| ≤ 3`; it is a structural cutoff, not a random seed. It bypasses CP-SAT extraction and disables deletion.

Use a fresh stem matching `l1-*-m1.json`, preserving the failed artifacts, and run the existing LRAT/checker pipeline. No reader or assembly change is needed: the reader already accepts any independently reconstructed row subset. I would initially allow **120 seconds for the LRAT solve**, expecting seconds to a few minutes but without claiming that bound is guaranteed.

There is one practical limitation: direct seed 3 retains the constant row, so its certificate cannot advertise the `c0`/`c3` variants.

**Better compact route, with a producer-only adjustment:** extract an assumption core from the seed-3 subset, then serialize and certify that core normally. My extraction took **4.94 s** and returned 1,437 rows, containing **no constant row**. Such a core can cover `none`, `c0`, and `c3` at m = 1 through the existing variant checks. This needs no trusted-reader change. Allow minutes for extraction, proof production, and checking; proof size remains unmeasured.

**Deletion over all rows:** distinguish two meanings.

- A further deletion pass over the **saved core**, including short rows, cannot remove its essential size-9 row. The satisfying assignment above establishes that.
- Starting from more original model rows can restore alternative contradictions. However, the seed-3 result already gives a cheaper, demonstrated way to do that. An exhaustive deletion pass could consume many minutes or hours; the current routine otherwise stops at its 600-second budget.

**CaDiCaL options:** a small portfolio using `--unsat`, or `--shuffle=true --shufflerandom=true --seed=1`, is compatible with unchanged readers, provided the resulting LRAT passes the pinned checker. I verified these options exist in the installed binary, but did not benchmark them. Budget **60–120 seconds per configuration**. I rank this below the demonstrated structural seeds.

**Splitting:** sound, but it requires more than teaching `read_all018` to count two files. The current reader rejects an arbitrary base-variable unit clause and does not accept extra branch fixings.

A sound extension must:

- Check each child as a **conditional** certificate under exactly `x=0` or `x=1`, with rows rebuilt under that condition.
- Bind both children to the same parent placement and named Boolean variable.
- Require both complementary branches for each claimed `(type, magnitude)` obligation.
- Prevent either child from counting individually as an unconditional certificate.

The justification is exhaustive Boolean case analysis: both `F ∧ ¬x` and `F ∧ x` are infeasible. Different row subsets in the two branches are fine. Merely concatenating proofs that assume opposite units is unsound without discharging those assumptions.

Expect two proof runs plus reader/assembly implementation, negative controls, and review—**hours of engineering rather than a short retry**, with no guarantee that a chosen split helps.

3. **Evidence of a cover or model mistake**

I found **no case-specific mistake**.

I checked that the root exactly matches catalog index 3, its declared and actual orders are both 9, and it has `(V,E,F) = (9,21,14)`, Euler characteristic 2, two faces per edge, and cyclic vertex links. Q and the empty pair are valid for this part/type. The stored rows agree with independent reconstruction, and the CNF reproduces byte-for-byte.

I also ran the five existing model, row-reconstruction, and assembly-binding tests in normal and optimized Python; both runs passed. I inspected the reader tests, but did not generate a coverage report.

The hour-long timeout and neighbouring LRAT successes are facts I **read from the records**, not proof checks I replayed. I did not rerun the complete cover checker or re-prove L1’s inherited mathematical lemmas.

My confidence is **high that structural reselection is the right next action**, moderate about the precise performance mechanism, and limited to these checks regarding overall model soundness. Case 754 remains uncertified until the replacement LRAT passes the pinned checker and assembly.