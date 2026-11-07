# Repository instructions

## Working style

- Run unit and integration tests, and add tests for new features. Inspect
  coverage for missing cases. Prefer focused, meaningful checks; preserve
  negative controls and checks under Python optimization where relevant.
- Prefer principled, scalable solutions. Parse structured data structurally;
  do not use regex to parse JSON or hardcode mappings that require manual
  updates. Derive behavior and indices from structured sources.
- Prefer MCP tools over CLI equivalents when both are available.
- Perform authorized operational work using available tools. Delegate a
  manual step only when it genuinely requires the user, such as OAuth,
  a substantive judgment, or nontrivial expenditure. If suggesting a manual
  path, also give the tool-based alternative where possible.

## Research publication and durable records

Standing preference recorded2026-10-20: make important, sufficiently verified
findings public, citable, searchable and traceable to dated public disclosures.
Include publication readiness in research handoffs; do not wait for a larger
discovery when a useful complete contribution is ready.

The central public index is https://github.com/queelius/research-records,
local checkout `/home/spinoza/github/research-records`. Keep source,
development and detailed lifecycle tracking in the owning project. Add
curated records and canonical links to the index.

Prefer Zenodo for durable archives and DOIs. The configured CLI is
`uv tool run --from zenodo-uploader==0.1.3 zenodo-upload`, reading
`~/.zenodo.toml`. Reuse its authentication without exposing credentials.
Read the index's `PUBLISHING.md` for metadata and pagination limitations.

Search existing records before creating a deposit. Use one canonical
record/version family per coherent contribution and version substantive
updates. Cite the exact archived version. Do not mint a DOI for each
experiment, minor edit or index update.

Archive a self-contained reproducible packet containing the exact claim,
scope, assumptions, source pins, evidence, meaningful controls, limitations,
license and citation metadata. Record original public disclosure dates and
URLs separately from DOI publication dates; never backdate a deposit.

Credit Alexander Richard Towell, retain predecessor/collaborator attribution
and disclose substantial AI assistance. Distinguish written proofs, formal
verification, finite computation, AI review, human review, repository acceptance
and novelty assessments. A DOI alone establishes none of correctness,
novelty, peer review or legal priority.

Carry out authorized publication with available tools, verify public records
and files, and link DOI and canonical source from the index. Respect coauthor,
license, confidentiality and destination requirements. Do not change source
visibility or expose unrelated private material to create an index entry.

## Workspace ownership

Use `/home/spinoza/github/math-research` for new general mathematics research.
Keep platform-specific checkouts separate. Existing `math-theory` evidence
stays here until a portable successor passes reproduction checks, preserves
frozen evidence and citations, and supplies an old-to-new source mapping.
See `../math-research/docs/research-workflow.md`.

## User identity — source of truth

- Canonical name: **Alexander Richard Towell**.
- Formal common name: Alexander Towell; casual: Alex Towell; handle: queelius.
- Pronouns: he/him.
- Primary email: `lex@metafunctor.com`.
- Other emails: `queelius@gmail.com`, `atowell@siue.edu`.
- GitHub: https://github.com/queelius
- Website: https://metafunctor.com (also https://queelius.github.io).
- PyPI: https://pypi.org/user/queelius
- R-universe: https://queelius.r-universe.dev
- Bluesky: https://bsky.app/profile/queelius.bsky.social
- Mastodon: https://mastodon.social/@queelius
- X/Twitter: https://x.com/queelius
- ORCID: https://orcid.org/0000-0001-6443-9897
- Google Scholar ID: `E9mnFzQAAAAJ`.
- Domains: `metafunctor.com`, `queelius.github.io`.
- Institution: Southern Illinois University Edwardsville (SIUE).
- PhD Computer Science at SIUE, in progress; MS Mathematics2023;
  MS Computer Science2015.
- Research interests: broad, currently AI, machine learning and cybersecurity
  (encrypted search); statistics, including Bayesian methods, underlies much
  of the work. Information retrieval was an earlier emphasis.
- Short bio: Code butcher, cancer survivor, hobby jogger.

Use this identity in commits, paper/package metadata, author fields and
citations. Update this section directly if the user changes a field.
