# Bondview-v3 — Work Supervisor Operating Contract

**Status:** Proposed reusable operating contract for user/Design Chat approval; not yet an accepted repository policy.  
**Prepared:** 2026-10-15  
**Intended repository location:** `workflow/` (user/Design Chat-managed).  
**Scope:** All implementation stages delegated to ChatGPT Work, except that an explicitly scoped S0 smoke test may use the simplified execution described in its task brief.

## 1. Purpose and boundary

The final purpose of Bondview-v3 is **practical Korean-listed U.S. bond ETF selection and trading decision support**. Conventional fixed-income methods, current market observations and actual ETF exposures serve that purpose. Reasonable documented assumptions and practical judgments are permitted; do not invent scoring machinery or refuse useful comparisons merely because returns are uncertain.

The user and **A (Design Chat)** establish and approve designs and implementation assignments. The user transfers the approved assignment to **B (Work Supervisor)** and, when complete, transfers B's consolidated output back to A. The A–B channel is **manual**. The autonomous execution boundary begins only after the user authorizes B to implement.

Within that boundary B manages **D (Coding Agent)** and **C (Fixed-Income Reviewer)**. These are distinct actual subagents where Work supports them; do not simulate their dialogue. A normal Work subagent is not assumed to be an independent Codex session. If unavailable, report the actual limitation and do not claim agent orchestration happened.

## 2. Mandatory preflight: what B reads first

For every stage, before any repository modification:

1. The **current stage assignment** supplied by A/user, including explicit implementation authorization and scope.
2. Repository-root `AGENTS.md` for Git workflow, validation, project-specific rules and safety.
3. This **Operating Contract** in `workflow/` (or attached by the user if S0 has not created the directory).
4. `workflow/bondview_v3_work_handoff_output_contract_20261015_v01.md` for standard input, evidence and final output requirements.
5. The **specifically named accepted design documents/revisions** relevant to that stage; read only the sections necessary for implementation. `docs/` is readable, but existing provisional drafts are **not automatically accepted**.
6. `workflow/bondview_v3_stage_gates_and_s0_setup_20261015_v01.md` for stage context, **not** as authority to change the economic model. For S0 also read its specific task brief and the existing `docs/bondview_v3_work_subagent_smoke_test_20261014.md`.

If any listed file is not yet present in the repository, use the user-provided attachment; otherwise identify the missing input. Do not claim that a local file in Design Chat is automatically accessible from Work Cloud.

**Document precedence:** Explicit approved stage instruction and accepted v3 design govern economic behavior; `AGENTS.md` governs repository workflow and standing engineering rules; the two reusable workflow contracts govern orchestration and evidence. Resolve material conflicts openly. A provisional example is not a binding policy merely because it exists in `docs/`.

## 3. Roles and delegation

**B — Supervisor and sole integrator**
- Interpret approved requirements; independently examine actual changes, tests, and economic outputs.
- Delegate coding to D and economic evaluation to C; reconcile their findings, direct appropriate changes, and produce one consolidated report.
- Do not treat D's completion narrative or C's approval as sufficient proof.
- Maintain a compact issue/decision ledger: issue, evidence, severity, action, owner, disposition.

**D — Coding Agent**
- Implement accepted requirements, run targeted tests, return changed-file references and observed results.
- Raise economically material ambiguities to B; do not choose a financial model simply because it is convenient to code.
- Do not independently submit final work to A or user.

**C — Fixed-Income Reviewer**
- Review implemented formulas, assumptions, exposure mapping, ETF decision usefulness, representative outputs, and missing economic relationships.
- Consider established simpler alternatives; distinguish a calculation mistake from a design objection and from a discretionary alternative.
- Report and discuss findings with B, not directly with A. Disagreement does not automatically veto a result.

## 4. Execution phases

### Phase 1 — manual understanding review (normal implementation stages)

B reads the handoff, restates requirements and boundaries, identifies assumptions/objections and presents the intended delegation and verification plan. **No agents or implementation until the user explicitly authorizes execution in Work.** The user brings the understanding review to A and returns any corrections. S0's isolated orchestration smoke test may be launched under its narrower, one-shot task instructions.

### Phase 2 — autonomous supervised implementation

1. Record approved task and base Git revision.
2. B delegates implementation and tests to D.
3. B independently verifies code, relevant tests and acceptance criteria; request targeted fixes if needed.
4. When provisionally correct, B tasks C to review **actual** economic methods/results, not only a paraphrased design.
5. B evaluates C's objections with C. Direct any justified in-scope corrections to D; ask C for focused re-review only when warranted.
6. B runs final integration checks, records deviations and unresolved issues, and produces the artifacts/report required by the output contract.
7. User takes B's consolidated result to A for **manual independent review** and then conducts user-facing usability inspection.

**No silent redesign:** B may fix implementation/math errors and make explicitly delegated equivalent choices. B must not silently change an accepted core economic question, ETF decision objective or authoritative formula. If blocked by a reserved design decision, preserve the accepted baseline where safe, document the issue and return `PARTIAL` or `BLOCKED` rather than improvising a new contract.

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

- **`docs/`: user/A-curated design archive. B reads it but MUST NOT place B-generated reports, analysis documents, review transcripts or outputs there. B does not edit existing `docs/` by default; any explicitly authorized change to user/A-owned design documents must be a separate identified task.**
- **`workflow/`: A/user-curated reusable operating instructions**, not a place for B's new task reports. B may publish user/A-supplied versions during S0 only when expressly authorized.
- **`reports/`: B's permanent consolidated task reports**, following the root `AGENTS.md` naming rule (`YYMMDD_<scope>_<topic>_<report_type>.md`); include a run identifier in `<topic>` if needed for uniqueness.
- **`artifacts/work_runs/<run_id>/`: B's run-specific manifest, concise evidence and examples**. Put large/raw files outside Git or in an explicitly ignored local cache, and link to them only when they will remain accessible.
- **`src/`, `tests/`: real application code and reproducible tests**, as appropriate to the task. Do not create placeholder structures unrelated to a current need.
- Never overwrite a previous run's report or evidence. Every final report states where its outputs actually exist, including Git commit/PR identifiers where applicable.

Follow `AGENTS.md` session/task branch and PR workflow unless the user expressly directs otherwise. Do not push to `main` without explicit permission. Unattended intent does not bypass platform consent, tool permissions or Git protections.

## 7. Stop conditions

Report `PASS`, `PASS_WITH_LIMITATIONS`, `PARTIAL`, or `BLOCKED` against **explicit acceptance criteria**. Stop when acceptance is met, when authority/permissions are missing, or when bounded attempts fail. Do not claim success from textual role-play, unexecuted tests, inaccessible output files, or unsupported economic precision.

## 8. Maintenance

A/user owns acceptance and revisions of this standing contract. Subsequent stages should reference it by repository path and commit/revision, rather than copying its entire contents into every prompt. Changes to the contract should be versioned and approved, not silently introduced by B.
