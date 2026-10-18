# Bondview-v3 — Standard Work Handoff, Evidence and Deliverables Contract

**Status:** Revised proposed reusable input/output contract for Archie/user approval.  
**Prepared:** 2026-10-15  
**Intended repository location:** `workflow/` (user/Design Chat-managed).  
**Companion:** `bondview_v3_work_supervisor_operating_contract_20261015_v03.md`.

## 1. Objective

Eliminate repeated common instructions in each **user-facing Work assignment**. Each assignment contains a short task brief and references the standing contracts. **Archie (A, Designer)** and the user approve the assignment; **Bernie (B, Orchestrator)** manages internal work through **Carrie (C, Fixed-Income Reviewer)** and **Dennis (D, Developer)**. Bernie's output must first allow Archie to verify implementation against approved requirements and then allow the user to assess ETF decision usefulness. Internal subtask or financial-aspect boundaries are **not** automatic user-facing stages.

## 2. Common inputs B must inspect

These inputs do not need to be recopied into every assignment prompt when versioned files are accessible in the repository:

| Standing input | Source | Minimum action |
|---|---|---|
| Project and repository practice | `AGENTS.md` | Inspect current rules before changing code |
| A/B/C/D authority, limits and phases | Work Supervisor Operating Contract | Apply actual agent delegation and bounded iterations |
| Reporting, evidence and files | This document | Use common output structure |
| Development gates | Stage Gates & S0 Setup document | Know stage dependencies and completion boundaries |
| Accepted financial design | Task-specific A-approved document revisions | Use accepted sections only; do not elevate provisional drafts automatically |

**Every user-facing assignment handoff still must supply:**

| Field | Required content |
|---|---|
| Assignment and run ID | user-facing milestone or task label, unique run ID, human-readable purpose |
| Explicit scope | What to build/review, and clear exclusions |
| Design authority | Exact accepted paths and relevant revision/commit; unresolved documents labeled provisional |
| Economic model | Required formulas, risk factors, data conventions, permissible proxies and assumptions where relevant |
| Decision role | Which ETF choice, buy/hold/review or market explanation should improve; practical end-to-end outcome |
| Inputs/data | Market and ETF data sources, available access, cutoff conventions, allowed fixtures |
| Acceptance criteria | Hand-checkable numerical tests, behavioral examples, error/missing-data cases, user demonstration |
| Discretion | What B may refine, what B must reserve for A |
| Git/environment | Target repository and branch reference, available files/tools, permissions and expected outputs |
| Execution authorization | Phase 1 only or explicit Phase 2 approval; for S0 see its special task |

**No implicit authorization:** An assignment with unresolved essential data or repository access must not be made to appear executable by inventing those conditions.

## 3. Minimal task-specific handoff template

Copy only this template when issuing a new stage assignment (and provide source references):

```text
Assignment / task: [user-facing deliverable / short name]
Base repository and revision: [repo, branch, commit if pinned]
Execution mode: [manual understanding review | authorized autonomous execution | one-shot S0]
Accepted specification(s): [exact path / revision / selected sections]
Task objective and practical ETF decision capability: [...]
In scope / out of scope: [...]
Economic calculations / assumptions / allowed proxies: [...]
Required source data and available access: [...]
Expected numerical examples and acceptance checks: [...]
Delegated discretion / reserved choices: [...]
Required user-facing demonstration: [...]
Special iteration or resource limits (if different from standing contract): [...]
Use AGENTS.md plus the standing contracts in workflow/. Do not write
B-generated documents under docs/. Provide the standard consolidated output.
```

## 4. Standard Bernie output: first Archie, then user

### 4.1 One authoritative consolidated report

B writes one final report under `reports/YYMMDD_<scope>_<topic>_<report_type>.md`, with a unique run identifier embedded when necessary. A concise top-level report may link to separate evidence files; **do not scatter the actual conclusion across many subagent documents**.

Recommended report headings:

1. **Executive result:** `PASS` / `PASS_WITH_LIMITATIONS` / `PARTIAL` / `BLOCKED`, with reason and scope actually completed.
2. **Provenance:** Approved task/design revisions, environment, base and output Git commit, session/task branches, PR and merge status where real.
3. **Requirements-to-evidence matrix:** each material acceptance criterion, `PASS` / `FAIL` / `NOT_RUN` / `NOT_APPLICABLE`, evidence path, limitation. The overall status is not a substitute for item-level results.
4. **Implemented features and artifacts:** changed files, their role, execution commands and actual observable outputs.
5. **Verified calculations:** economically important synthetic expected-vs-observed numbers, units, assumptions, signs, tolerances; actual data demonstrations only when supported.
6. **C's economic review and B's disposition:** major objections, evidence, alternative, accepted/rejected/deferred rationale, resulting D changes.
7. **Remaining deviations/risks:** any unmet requirement, proxy limitation, contradictory output, reserved decision or unavailable data.
8. **Execution ledger and usage:** actual C/D rounds, interruptions, checkpoints and **measured token/credit data only when exposed**; otherwise `not exposed`.
9. **User demonstration:** how to run/inspect real ETF analyses or the S0 operational probe, representative outputs, supported/not-supported tasks and usability warnings.
10. **Artifacts index:** manifest and actual file/PR links, with verification that artifacts exist in the stated environment.

### 4.2 Archie's review matrix

Make the evidence inspectable without rerunning the whole Work session:

| Requirement ID | Accepted behavior | Actual test/output | Status | Evidence location | Limitation |
|---|---|---|---|---|---|
| R-01 | [specific requirement] | [observed behavior] | PASS/FAIL/NOT_RUN | [file + revision] | [if any] |

A should be able to distinguish: implementation compliance, economic validity, test reproducibility, unresolved design change, and residual user-facing usability risk. A's review is not a guarantee of perfection.

### 4.3 User-facing demonstration

For a financial-capability stage, provide a small practical walkthrough: selected real ETF(s) when data are available, observation dates, assumptions, computed exposures/compensation/scenarios, meaningful selection or review judgment, and clear limitations. **Do not stop at a numerical unit test if the stage goal is an ETF decision.**

For S0, replace ETF demonstrations with proof of two distinct real agents, the follow-up and revision, actual verified files/tests, and repository setup results **within the same completed Work assignment**. Report S0-A and S0-B separately inside one consolidated report.

## 5. Run-specific evidence and naming

Recommended structure:

```text
reports/
  YYMMDD_<scope>_<topic>_<runid>_report.md   # durable Bernie report
artifacts/
  work_runs/
    <assignment>_YYYYMMDD_HHMM_<short_topic>/
      manifest.json                           # small metadata index
      evidence/                               # concise test and review evidence
      examples/                               # small reproducible sample outputs
```

Use new filenames/run IDs. Never overwrite past final reports; do not fill `docs/` with B-generated documents. Evidence should be small and relevant; large/raw market data, logs or caches belong outside the committed repository unless expressly required.

**Suggested `manifest.json` fields:** `run_id`, `assignment_id`, `task`, `design_revision`, `source_commit`, `result_commit`, `final_report_path`, `status`, `test_commands`, `evidence_paths`, `generated_at`, `usage`, `limitations`. Use `null`/`not_exposed` for unknown facts; never invent a commit hash, count or URI.

`workflow/` contains Archie/user-authored standing contracts, **not Bernie-generated reviews**. `docs/` remains Archie/user's design archive and is not an S0 input. Bernie may reference the contracts but should not duplicate or alter them as a side effect of setup.

### S0 exception to the normal preflight

The user's **single S0 Work prompt** fully specifies the isolated S0-A test; Bernie must not open GitHub or read `AGENTS.md`/`workflow/` until S0-A passes. S0-B then performs normal repository preflight and setup without requesting another routine user authorization. Do not require a second Work session or intermediate Archie review to move between internal S0 steps.

## 6. Required completion checklist

- [ ] B inspected the actual code/artifacts, not just D's summary.
- [ ] B can reproduce the material test outcomes or explains why not.
- [ ] C provided an independent economically substantive review when the stage has bond-model logic.
- [ ] Each materially accepted objection was fixed and verified; others were explained.
- [ ] A-readable requirements evidence and user-readable demonstration are present.
- [ ] `docs/` received **no** B-generated reports or documents.
- [ ] Repository branch, PR, report and evidence locations are real and accessible as claimed.
- [ ] Agent rounds and usage figures distinguish measured facts from unavailability.
- [ ] Any unmet acceptance criterion is flagged rather than disguised as a pass.
