# Exact spectral exclusion certificates for degree-five Boolean candidates

Alexander Richard Towell  
Southern Illinois University Edwardsville  
ORCID: https://orcid.org/0000-0001-6443-9897

This packet contains ten exact, conditional infeasibility certificates from
a search for a Boolean multilinear polynomial on 14 variables with degree at
most five, value zero at the origin, and value one at every unit vector.
**The existence question remains open.** These certificates exclude ten
specified cases within one signed Fourier geometry. They do not exclude the
whole geometry, all self-dual candidates, or all 14-variable candidates.

The contribution is the specified finite exclusions, their exact evidence,
and reproducible checking software. General Fourier expansion, Parseval's
identity, linear relaxation, and certificates obtained by combining linear
inequalities are established techniques. No priority claim is made for those
techniques or for the partial exclusions.

## Exact scope and conventions

Coordinates are numbered 0 through 13. An integer support mask represents
the set of coordinates at its nonzero bits. Write

    h(x) = 1 - 2f(x) = (1/16) sum_S k_S (-1)^(sum_{i in S} x_i).

The archived case reductions concern the self-dual empty-pair branch:
`f(1-x)=1-f(x)` and `f(e_i+e_j)=1` for every distinct pair. Self-duality is
used only in this proved branch. The required odd Fourier layer sums are
`A1=16`, `A3=-104`, and `A5=104`.

Signed geometry 34 fixes the quintic coefficients on supports
`7216, 9731, 10764, 12736` to `-2`, and those on `7681, 14849` to `+2`.
Its four-coordinate core is `[0,9,11,12]`. The outside-coordinate order is
`[10,13,1,2,3,4,5,6,7,8]`. The marked core pair is `{0,12}`, mask 4097.

Each excluded case fixes the entire function
`B_{0,12}(y)=sum_z h(z,y)(-1)^(z_0+z_12)`. Its values on the 512-point
face with the final outside coordinate zero, and its nonzero Fourier
coefficients, are explicitly listed in `CASES.json`. Odd complement parity
determines the other face. The historical representative IDs are
`221,581,178,386,597,599,601,191,626,656`; the explicit patterns, rather than
the labels alone, define the cases. These patterns are necessary component
data, not Boolean functions solving the original question.

The complete quotient, component catalogs, and preceding restriction
arguments are included in `source/`. Their provenance and independent
verification records remain dependencies of the conditional claim. The
fresh container replay below checks the ten cases' domain deletions, input
construction and exact contradictions. It does not rerun every historical
classification and reduction in the dependency archive.

## Why the certificate proves a contradiction

Parseval gives `sum_S k_S^2=256`. Integer-coefficient inequalities, the three
layer sums, and the six exceptional quintics force energies at least
20, 104 and 132 in degrees one, three and five. Equality therefore holds
throughout: singleton coefficients are in `{1,2}`, cubic coefficients in
`{-1,0}`, and ordinary quintics in `{0,1}`. The singleton sum is 16.

Any Boolean function in a specified case selects exactly one actual
four-coordinate truth table at each outside point and exactly one complete
pattern in each of the six core-pair components. These selections satisfy:

1. Word and pattern normalization equations.
2. Categorical consistency between each selected word and selected pattern.
3. All projected value equations for the empty and singleton core
   characters, with each two-valued Fourier coefficient represented by a
   zero-or-one flag.
4. Five Parseval second-moment equations and the singleton-total equation.

The core-word enumeration checks all 65,536 four-variable truth tables.
The moment equations use averages of squared word values, not squares of
averages. Relaxing the selection variables and flags to `[0,1]` preserves
every actual Boolean function. Independently justified domain deletions
preserve every possible selection.

For each case, an independent implementation reconstructs every equality
and positive gcd divisor and checks the saved primitive matrix entry by
entry. The saved nonnegative integer combination of oriented equalities
and box inequalities cancels every variable. The resulting right-hand side
is strictly negative, proving infeasibility.

The exact contradiction values, matrix sizes, and original verification
commands are in
[`ranked_case_exclusions_cycle652.md`](source/.research/attempts/009-parent-analysis/ranked_case_exclusions_cycle652.md).
The necessity argument is developed in
[`whole_first_case_spectrum_soundness_cycle585.md`](source/.research/attempts/009-parent-analysis/whole_first_case_spectrum_soundness_cycle585.md)
and its cited predecessors. The case-specific input audits specify the
complete domains for each of the ten cases.

Numerical solver termination is not proof authority. These ten certificates
were transferred from a previously checked inequality and checked with
integer arithmetic; no new numerical optimization was required.

## Reproduction and evidence levels

Follow `REPRODUCE.md`. The source payload is byte-identical to the pinned
research artifacts. The container maps that payload to the historical
absolute path without mounting the original research workspace. It has no
network access during verification.

`SOURCE-MANIFEST.json` and `SUPPLEMENT-MANIFEST.json` identify the source
bytes. Hashes establish identity; the mathematical readers establish the
reported checks. `REPLAY-PLAN.json` specifies 138 control tests, independent
domain-deletion replay, and the input and certificate checks for all ten cases.
The final `replay-results/REPLAY-RECEIPT.json` is produced only after every
declared stage succeeds. Logs and exact command arguments are retained.

Some large inherited files belong to earlier cases. They are retained
because the unmodified provenance manifests reference them, not because all
are needed to understand these ten contradictions. The archive includes
historical unsuccessful approaches as such; they are not proof authorities.

This is written reasoning and independently implemented finite computation.
It is not proof-assistant formalization, recorded human peer review, or
external acceptance. Substantial OpenAI Codex assistance was used for
mathematics, implementation, experiments, verification code and exposition.
Independent implementations are not independent human reviewers.

## Prior work and bounded novelty assessment

The mathematical target is motivated by the degree–sensitivity construction
problem described by [Epoch AI](https://epoch.ai/frontiermath/open-problems/degree-sensitivity-boolean).
That broader problem was labeled unsolved when checked on 20 October 2026.
Its status does not prove novelty of any specific partial result here.

Juris Smotrovs and Jurijs Zaicevs discuss the same 14-variable, degree-five
search and unsuccessful construction attempts in their April 26, 2026
[Theory Days slides](https://theorydays.cs.ut.ee/uploads/2026/juris-smotrovs.pdf),
particularly slide 18. Their discussion credits I. Stepanovs for earlier
layer-statistic computations. Those researchers' problem formulations,
previous bounds and computations are predecessor work, not contributions
claimed by this packet.

The primary-source review and the author's existing-record search identified
no matching archived certificate family. This is a bounded observation, not
an exhaustive novelty search or proof of priority. No earlier public
disclosure date is asserted for this packet. An eventual DOI records its
archival publication date; it does not establish correctness, novelty,
peer review or legal priority.

The owning research directory has no Git commit to cite. Exact source-byte
hashes are provided instead. Publication and index metadata must identify the
exact archived version once a public record exists.

## License

Original Python code is offered under MIT; original notes and data under
CC BY 4.0. The archived SciPy/HiGHS binary retains its original notices and
terms. See `LICENSE.md` and `LICENSES/`. No third-party library is reattributed
to the author. Runtime dependencies are installed separately from their
named distributions.
