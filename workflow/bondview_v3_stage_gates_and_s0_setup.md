# Bondview-v3 — Delivery Milestones and One-Assignment S0 Setup

**Status:** Revised proposed workflow, pending Archie/user approval.  
**Prepared:** 2026-10-15  
**Repository destination:** `workflow/bondview_v3_stage_gates_and_s0_setup_20261015_v03.md`  
**Named roles:** Archie (A, Designer), Bernie (B, Orchestrator), Carrie (C, Fixed-Income Reviewer), Dennis (D, Developer).

## 1. User-facing versus internal work

Keep **user-facing Work assignments and approval checkpoints to a practical minimum**. Archie and the user approve a sufficiently complete design and substantial deliverables; Bernie autonomously decomposes an authorized assignment into coding tasks, economic reviews, corrections, tests, and checkpoints. A financial aspect (Duration, Curve, Credit, FX) is **not automatically** a separate user-facing stage or Work session.

The Archie ↔ Bernie handoff remains manual and user-mediated. Bernie, Carrie and Dennis work without routine user intervention **within** authorized scope. Reserve meaningful new financial-design choices and final acceptance for Archie/user; do not demand user decisions for normal internal implementation details.

## 2. S0 is ONE user-facing Work assignment

One Work launch authorizes both internal steps below. No user-mediated handoff or separate Work session between them; platform-required consent remains possible.

**S0-A — isolated subagent smoke test:** Bernie executes the full test supplied in the S0 launch prompt in a disposable, non-repository workspace. Do not open or depend on Bondview, `docs/`, `workflow/`, or GitHub during the test. Actual Dennis/Carrie agents, implementation, supervisor verification, a Carrie follow-up, routed revision, and re-review must be evidenced. No simulated dialogue. If the result is not a verified PASS, stop: **do not execute S0-B**.

**S0-B — conditional repository setup:** Following a verified S0-A PASS, Bernie accesses `lbk209/bondview-v3`, reads current `AGENTS.md` and approved `workflow/` contracts, verifies permissions and branch state, and produces real files under `reports/` and `artifacts/work_runs/<run_id>/` using the existing session/task branch → PR workflow. The four workflow contracts already exist; **do not republish them**. Do not generate files in `docs/` or `workflow/`; do not write directly to `main`, create speculative `src/`/`tests/` scaffolding, or implement financial logic.

Bernie produces **one final consolidated S0 report** including separate `S0-A` and `S0-B` statuses, evidence and PR references, actual agent round counts and available measured usage. The user brings that report to Archie. S0 success is not authorization for financial implementation.

### S0 acceptance criteria

- S0-A real subagents, interactions, file modifications, and executed tests are verifiably evidenced.
- S0-B verified repository and allowed Git operations; its report and artifact index exist in permitted paths.
- The two internal steps are separately labeled PASS/PARTIAL/BLOCKED, with an accurate overall outcome.
- `docs/` and `workflow/` have no Bernie-generated reports; no unauthorized design or `main` changes.
- Outputs are accessible through real files/PR links, not asserted cloud paths.
- Any missing user permission or platform capability is reported without pretending success.

## 3. Financial implementation after S0

Do **not** create a mandatory user-facing S1–S5 sequence. The following are candidate **Bernie-managed internal workstreams** inside one or a small number of Archie-approved substantial implementation assignments, depending on the accepted financial design:

| Internal workstream (illustrative) | Economic/engineering objective |
|---|---|
| Treasury ETF foundation | Real ETF properties, market observations, conventional rate sensitivity and practical decision demonstration |
| Curve and ETF comparisons | Nonparallel exposure, same-ETF-over-time and cross-ETF comparisons where meaningful |
| KRW currency treatment | Unhedged/hedged economics with transparent assumptions |
| Credit-aware calculations | Distinguish Treasury-rate and credit-spread risks when supported |
| Product-specific integration | Futures/other instrument models where justified; output and usability checks |

Bernie may combine, sequence, or omit internal workstreams **within the approved scope**; must not silently extend authority to unapproved products or redesign the financial architecture.

A **user-facing review** should occur when there is a substantial finished deliverable, a material unapproved design choice, a true blocker, or final acceptance—not automatically after every internal aspect.

## 4. Common final acceptance evidence

For each completed user-facing assignment, Bernie's report must provide: a requirements-to-evidence matrix, actual code/revisions, executed tests, Carrie's economic findings and Bernie's dispositions, important numerical examples, limitations, Git/PR status, concise user demonstration, and actual usage when exposed. Archie verifies design/economic compliance; the user reviews practical usability. Code execution alone is not sufficient evidence of useful ETF decision support.

## 5. File and authority boundaries

```text
bondview-v3/
  AGENTS.md                           # shared repository instructions
  docs/                               # Archie/user design archive; no B-generated files
  workflow/                           # Archie/user-approved reusable contracts
  reports/                            # Bernie final consolidated reports
  artifacts/work_runs/<run_id>/        # Bernie manifest and concise evidence
  src/                                # actual code when needed
  tests/                              # actual reproducible tests when needed
```

Use distinct run IDs and filenames; never overwrite earlier results. Follow `AGENTS.md` for Git, safety and testing, and `bondview_v3_work_handoff_output_contract_20261015_v03.md` for report structure. The stage plan is **not** financial-model authority.
