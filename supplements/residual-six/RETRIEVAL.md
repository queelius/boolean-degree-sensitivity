# Explicit external premises and optional retrieval

Portable new controls require no downloads. The inherited old local derivative
theorem remains a named assumption; running the new controls does not re-prove
it. The complete baseline and positive-quadratic manifold filters use Florian
Frick, *Combinatorial restrictions on cell complexes*(2015), Theorem3.10,
printed page44, and Frank H. Lutz's complete small-valence data:

* Primary thesis:<https://d-nb.info/1076082246/34>.
  Historical PDF SHA256:
  `0ff12e3638b45cb27a3fc491637bf829918b502438b7d019ee6d21566c47dd59`.
* Primary data page:
  <https://www3.math.tu-berlin.de/IfM/Nachrufe/Frank_Lutz/stellar/3-manifolds.html>.
  Follow its link to `manifolds_lex_d3_deg5.txt.gz`.
  Expected432,948 bytes; SHA256:
  `41071b36a731396d5273c60748aea7937c876136684ac479971e87e27e2fbb59`.
  The external completeness assertion covers4,787 records.

If independently retrieving a file, save it outside this immutable packet and
verify its bytes before interpreting an old audit:

```sh
python - /path/to/manifolds_lex_d3_deg5.txt.gz <<'PY'
from hashlib import sha256
from pathlib import Path
import sys
data = Path(sys.argv[1]).read_bytes()
if len(data) != 432948 or sha256(data).hexdigest() != '41071b36a731396d5273c60748aea7937c876136684ac479971e87e27e2fbb59':
    raise SystemExit('Unexpected catalog bytes')
print('Historical catalog bytes match; completeness remains the cited theorem.')
PY
```

Redistribution terms for the third-party PDF and raw dataset were not established
in this preparation. Their bodies and extracted thesis text are therefore not
included, and they are not offered under Towell's original-work licenses.
Historical enumeration completeness was not regenerated.

Inherited graph premises cite Klas Markström and John Talbot,
*On the density of 2-colourable 3-graphs in which any four points span at most
two edges*, DOI[10.1002/jcd.20223](https://doi.org/10.1002/jcd.20223),
especially the unrestricted order14 near-extremal classification counts in
Figure1. Author manuscript:
<http://abel.math.umu.se/~klasm/Uppsatser/2colturan.pdf>.
Their extremal126 and G125/G124/G123 classification statements remain explicit
inputs to the applicable inherited graph lemmas. The old GLPK/nauty enumeration
is not rerun. The new residual-six controls do not use or fetch this paper.
