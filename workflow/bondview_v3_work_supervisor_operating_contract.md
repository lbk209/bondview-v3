# Bondview-v3 — Work Supervisor Operating Contract

**Status:** Revised proposed reusable operating contract; requires Archie/user approval before use.  
**Prepared:** 2026-10-15  
**Intended repository location:** `workflow/` (user/Design Chat-managed).  
**Scope:** All implementation assignments delegated to ChatGPT Work. S0 is one user-facing Work assignment with two conditional internal steps managed by Bernie.

## 1. Purpose and boundary

The final purpose of Bondview-v3 is **practical Korean-listed U.S. bond ETF selection and trading decision support**. Conventional fixed-income methods, current market observations and actual ETF exposures serve that purpose. Reasonable documented assumptions and practical judgments are permitted; do not invent scoring machinery or refuse useful comparisons merely because returns are uncertain.

The user and **Archie (A, Designer in Chat)** establish and approve designs and implementation assignments. The user transfers the approved assignment to **Bernie (B, Work Orchestrator)** and, when complete, transfers Bernie's consolidated output back to Archie. The Archie–Bernie channel is **manual**. The autonomous execution boundary begins only after the user authorizes Bernie to implement.

Within that boundary Bernie manages **Dennis (D, Developer/Coding Agent)** and **Carrie (C, Fixed-Income Reviewer)**. These are distinct actual subagents where Work supports them; do not simulate their dialogue. A normal Work subagent is not assumed to be an independent Codex session. If unavailable, report the actual limitation and do not claim agent orchestration happened.

## 2. Mandatory preflight: what Bernie reads

For ordinary implementation assignments, before any repository modification:

1. The **current stage assignment** supplied by A/user, including explicit implementation authorization and scope.
2. Repository-root `AGENTS.md` for Git workflow, validation, project-specific rules and safety.
3. This **Operating Contract** in `workflow/` (or attached by the user if S0 has not created the directory).
4. `workflow/bondview_v3_work_handoff_output_contract_20261015_v03.md` for standard input, evidence and final output requirements.
5. The **specifically named accepted design documents/revisions** relevant to that stage; read only the sections necessary for implementation. `docs/` is readable, but existing provisional drafts are **not automatically accepted**.
6. `workflow/bondview_v3_stage_gates_and_s0_setup_20261015_v03.md` for task/milestone context, **not** as authority to change the economic model. For S0, follow the self-contained launch instructions supplied by the user; do **not** open the repository or any `docs/` files during S0-A.

If any listed file is not yet present in the repository, use the user-provided attachment; otherwise identify the missing input. Do not claim that a local file in Design Chat is automatically accessible from Work Cloud.

**Document precedence:** Explicit approved stage instruction and accepted v3 design govern economic behavior; `AGENTS.md` governs repository workflow and standing engineering rules; the two reusable workflow contracts govern orchestration and evidence. Resolve material conflicts openly. A provisional example is not a binding policy merely because it exists in `docs/`.

## 3. Roles and delegation

**Bernie (B) — Orchestrator and sole integrator**
- Interpret approved requirements; independently examine actual changes, tests, and economic outputs.
- Delegate coding to D and economic evaluation to C; reconcile their findings, direct appropriate changes, and produce one consolidated report.
- Do not treat D's completion narrative or C's approval as sufficient proof.
- Maintain a compact issue/decision ledger: issue, evidence, severity, action, owner, disposition.

**Dennis (D) — Developer / Coding Agent**
- Implement accepted requirements, run targeted tests, return changed-file references and observed results.
- Raise economically material ambiguities to B; do not choose a financial model simply because it is convenient to code.
- Do not independently submit final work to A or user.

**Carrie (C) — Fixed-Income Reviewer**
- Review implemented formulas, assumptions, exposure mapping, ETF decision usefulness, representative outputs, and missing economic relationships.
- Consider established simpler alternatives; distinguish a calculation mistake from a design objection and from a discretionary alternative.
- Report and discuss findings with B, not directly with A. Disagreement does not automatically veto a result.

## 4. Execution phases

### Phase 1 — manual understanding review (when required for substantial implementation assignments)

Bernie reads the handoff, restates requirements and boundaries, identifies assumptions/objections and presents the intended delegation and verification plan. **No implementation until the user explicitly authorizes execution in Work**, when this review gate is part of the approved handoff. The user brings the understanding review to Archie and returns any corrections. **S0 is an explicit one-shot exception:** its launch prompt authorizes the complete S0 task, with no manual stop between its internal steps.

### Phase 2 — autonomous supervised implementation (one authorized assignment)

1. Record approved task and base Git revision.
2. B delegates implementation and tests to D.
3. B independently verifies code, relevant tests and acceptance criteria; request targeted fixes if needed.
4. When provisionally correct, B tasks C to review **actual** economic methods/results, not only a paraphrased design.
5. B evaluates C's objections with C. Direct any justified in-scope corrections to D; ask C for focused re-review only when warranted.
6. B runs final integration checks, records deviations and unresolved issues, and produces the artifacts/report required by the output contract.
7. User takes B's consolidated result to A for **manual independent review** and then conducts user-facing usability inspection.

**Internal task separation is not a user-facing stage boundary.** Bernie may partition work into financial aspects, code tasks, targeted reviews, and checkpoints without requesting a new Work session or user approval each time. Significant unapproved design changes still return to Archie/user as reserved decisions.

**No silent redesign:** B may fix implementation/math errors and make explicitly delegated equivalent choices. B must not silently change an accepted core economic question, ETF decision objective or authoritative formula. If blocked by a reserved design decision, preserve the accepted baseline where safe, document the issue and return `PARTIAL` or `BLOCKED` rather than improvising a new contract.

### Special S0 sequence — one Work assignment

- The user pastes **one self-contained S0 launch prompt** from `bondview_v3_s0_work_assignment_20261015_v03.md` into a new Work session. This supplies S0-A instructions without requiring repository access.
- **S0-A:** Bernie spawns real Dennis and Carrie subagents in a disposable non-repository workspace, verifies actual implementation, review, follow-up, revision and re-review.
- **S0-B:** Only after a verified S0-A PASS, Bernie accesses GitHub, reads `AGENTS.md` and approved `workflow/` contracts, and initializes `reports/` and `artifacts/work_runs/<run_id>/` through the existing Git branch/PR workflow.
- No user-facing approval or separate Work task between S0-A and S0-B. Platform-mandated consent is an exception; missing access or failed smoke test produces a truthful PARTIAL/BLOCKED report.
- One final Bernie report is returned to the user for the manual Archie review. S0 does not authorize financial implementation.

## 5. Bounded iteration and usage discipline

Initial guidance, adjustable in a stage assignment:

| Activity | Normal cap |
|---|---:|
| D implementation rounds before C review | 2 total (initial plus one targeted correction) |
| C economic reviews | 1 initial + at most 1 focused re-review |
| B–C substantive exchanges per material objection | 2 |
| D revision rounds following C's initial review | 1 ordinary round |
| Extra rounds | Only if explicitly granted or needed to repair a new critical defect; otherwise stop and disclose |

Do not repeat unchanged arguments or re-read entire repositories unnecessarily. Save compact checkpoints after provisional coding and material economic review, including state, references, tests and next action. A prompt-level cap is **not** a platform-enforced token/credit limit. Report only actually exposed usage figures; otherwise write `unavailable`.

## 6. File ownership and Git boundaries

- **`docs/`: user/Archie-curated design archive. Bernie must not browse it by default or place B-generated reports, analysis documents, review transcripts or outputs there. Access to an expressly identified financial design file is permitted only under a later approved assignment; none is required for S0.**
- **`workflow/`: Archie/user-curated reusable operating instructions**, not a place for Bernie-generated task reports. Do not republish or silently modify existing contracts during S0.
- **`reports/`: B's permanent consolidated task reports**, following the root `AGENTS.md` naming rule (`YYMMDD_<scope>_<topic>_<report_type>.md`); include a run identifier in `<topic>` if needed for uniqueness.
- **`artifacts/work_runs/<run_id>/`: B's run-specific manifest, concise evidence and examples**. Put large/raw files outside Git or in an explicitly ignored local cache, and link to them only when they will remain accessible.
- **`src/`, `tests/`: real application code and reproducible tests**, as appropriate to the task. Do not create placeholder structures unrelated to a current need.
- Never overwrite a previous run's report or evidence. Every final report states where its outputs actually exist, including Git commit/PR identifiers where applicable.

Follow `AGENTS.md` session/task branch and PR workflow unless the user expressly directs otherwise. Do not push to `main` without explicit permission. Unattended intent does not bypass platform consent, tool permissions or Git protections.

## 7. Stop conditions

Report `PASS`, `PASS_WITH_LIMITATIONS`, `PARTIAL`, or `BLOCKED` against **explicit acceptance criteria**. Stop when acceptance is met, when authority/permissions are missing, or when bounded attempts fail. Do not claim success from textual role-play, unexecuted tests, inaccessible output files, or unsupported economic precision.

## 8. Maintenance

Archie/user owns acceptance and revisions of this standing contract. Subsequent stages should reference it by repository path and commit/revision, rather than copying its entire contents into every prompt. Changes to the contract should be versioned and approved, not silently introduced by B.
