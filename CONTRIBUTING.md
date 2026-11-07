# Contributing

The question here is open. Is there a Boolean function on 14 variables, of
real polynomial degree at most 5, with f(0) = 0 and f(e_i) = 1 for every i?
Such a function has sensitivity 14 > 5^(log 6 / log 3) ≈ 13.8, so it would
answer Epoch AI's
[degree vs. sensitivity problem](https://epoch.ai/frontiermath/open-problems/degree-sensitivity-boolean)
at degree five. Contributions of any size are welcome. Each kind is described
below, with the standard of evidence it needs.

## Kinds of contribution

1. **A construction.** Any function meeting the conditions above settles the
   d = 5 case. Check it exactly before posting it:

   ```bash
   python tools/check_candidate.py candidate.json
   ```

   The checker uses only the Python standard library. It evaluates the function
   on all 16,384 inputs, recomputes its unique multilinear representation (so the
   degree it reports is exact, not a bound), and reports f(0) and the origin
   sensitivity. Its docstring gives the input format, and its tests show worked
   examples, including Kushilevitz's function. A construction for any other
   degree that beats the exponent log 6 / log 3 also answers Epoch's question;
   the checker reports this as `beats_kushilevitz_exponent`.

2. **A proof for an open case.** After version 1.5.0, 27 of the 73 negative
   quintic magnitude patterns are open: 20 with residual Fourier defect at most
   6 (negative-support union 14) and 7 with remaining defect 8 to 12. See
   [the v1.5.0 report](supplements/no-free-residual-six/REPORT.md) and the issues.
   A written argument is welcome. A computer proof should come with a
   certificate that a separate, simple checker can verify (for SAT, an LRAT
   proof ending in the empty clause).

3. **Review of the written reductions.** The certificates are machine-checked,
   but the reductions that make a finite case list exhaustive have been reviewed
   only by AI models. Human review of any of them is valuable, whether it finds
   a gap or confirms the argument. Each supplement's README names its written
   lemmas.

4. **Independent replay.** Re-running the certificate checks on other hardware,
   or with a different checker (for example cake_lpr for LRAT), strengthens the
   evidence. The supplements' `REPRODUCE.md` files give the steps. The large
   files are in the Zenodo archives listed in the README.

5. **Formalization.** Lean statements and proofs of the problem, its normal
   form, the known bounds or any lemma here are welcome. The public Lean
   definitions `BoolFunc`, `sensitivity` and `polyDegree` on
   [Prove2Me](https://prove2.me) are one starting point.

## Standards

- Keep these categories apart: a necessary condition, a proved exclusion, a
  Boolean function verified on every input, and a solver UNKNOWN or timeout.
  A timeout is not evidence of anything.
- The self-dual normal form used in the supplements preserves *existence*
  only. Do not assume an arbitrary Boolean function is self-dual.
- Scopes are nested (decision cases, magnitude patterns, signed-star
  contexts, raw row relaxations). Never add counts across scopes or quote a
  percentage of the problem as solved.
- Every result here is conditional on the premises its report lists. Say
  which premises a new result uses.

## How to contribute

- **Issues** for a specific open case, a suspected error, or a replay report.
  For a suspected error, give the file, the claim and a counterexample or the
  failing step.
- **Pull requests** for code, checkers or written arguments. Code is MIT
  licensed and notes and data are CC BY 4.0 (see [LICENSE.md](LICENSE.md)).
  By contributing you agree to license your contribution the same way.
- Contributions that change a published claim go into new files. Published
  supplements are frozen, and their hashes are recorded in Zenodo archives
  and receipts.

Please disclose substantial AI assistance, as this project does. Most of the
work so far was done with OpenAI Codex, and later work with Claude Code; the
reports say which parts. Contributors are credited in the next archive version.
