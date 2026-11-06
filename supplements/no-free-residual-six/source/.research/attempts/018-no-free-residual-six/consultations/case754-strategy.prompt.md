You are being consulted by a Claude Code session that orchestrates this research. Read /home/spinoza/github/math-theory/.research/CODEX_BRIEFING.md for context and rules. Work read-only; do not start long solver runs unless the question asks for a bounded check. Say what you verified yourself, what you only read, and how confident you are. Disagree when you see a gap.

Question: how should we certify the one failed L1 obligation, cover case 754 at m = 1 (type none)?

Context: attempts/018-no-free-residual-six. Read README.md (section "State on 2026-10-23"), L1.md, model018.py, certify018.py, and the case itself (row 754 of l1-cover.json). The pipeline is CP-SAT core -> 014 CNF encoder -> CaDiCaL 3.0.1 LRAT -> pinned lrat-trim, then reader018.py rebuilds every row from its key. For this case CP-SAT reported the core infeasible, but CaDiCaL did not refute the core's CNF in 3600 s (certs/results.jsonl, the ERROR line; certs/l1-00754-m1.cnf and .labels.json exist; do not decompress the .zst partial proof). Nearly all other cases certify in under a minute.

Please assess, with reasons and rough cost:
1. Why might this case be hard for CaDiCaL while CP-SAT found it infeasible? Look at what distinguishes case 754 (root link order, Q and pair placement) from its neighbours if you can.
2. Which fix keeps the certificate fully checkable by the existing reader018/read_all018 without weakening anything: a different core seed (certify(..., seed_k=)), running the deletion pass over all rows, splitting the case on one variable into two sub-certificates (and what read_all018 would then need to accept the pair soundly), CaDiCaL options, or another idea?
3. Anything about this case that suggests a mistake in the cover or model rather than solver difficulty.
You may run small bounded read-only checks (CNF statistics, the case's rows) but no solver run longer than 2 minutes, and do not write anywhere.
