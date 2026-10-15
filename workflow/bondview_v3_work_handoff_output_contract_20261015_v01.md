# Bondview-v3 — Standard Work Handoff, Evidence and Deliverables Contract

**Status:** Proposed reusable input/output contract for A/user approval.  
**Prepared:** 2026-10-15  
**Intended repository location:** `workflow/` (user/Design Chat-managed).  
**Companion:** `bondview_v3_work_supervisor_operating_contract_20261015_v01.md`.

## 1. Objective

Eliminate repeated common instructions in each stage. Each assignment contains a **small stage-specific task brief** and references these standing contracts. B's output must first allow A to verify whether the implementation matches the approved requirements and then allow the user to evaluate practical ETF decision usefulness.

## 2. Common inputs B must inspect

These inputs do not need to be recopied into every stage prompt when versioned files are accessible in the repository:

| Standing input | Source | Minimum action |
|---|---|---|
| Project and repository practice | `AGENTS.md` | Inspect current rules before changing code |
| A/B/C/D authority, limits and phases | Work Supervisor Operating Contract | Apply actual agent delegation and bounded iterations |
| Reporting, evidence and files | This document | Use common output structure |
| Development gates | Stage Gates & S0 Setup document | Know stage dependencies and completion boundaries |
| Accepted financial design | Task-specific A-approved document revisions | Use accepted sections only; do not elevate provisional drafts automatically |

**Every stage-specific handoff still must supply:**

| Field | Required content |
|---|---|
| Stage and task ID | `S<n>`, unique run ID, human-readable purpose |
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

## 3. Minimal stage-specific handoff template

Copy only this template when issuing a new stage assignment (and provide source references):

```text
Stage / task: [S<n> / short name]
Base repository and revision: [repo, branch, commit if pinned]
Execution mode: [Phase 1 understanding review | Phase 2 authorized | S0 probe]
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

## 4. Standard B output: first A, then user

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

### 4.2 A's review matrix

Make the evidence inspectable without rerunning the whole Work session:

| Requirement ID | Accepted behavior | Actual test/output | Status | Evidence location | Limitation |
|---|---|---|---|---|---|
| R-01 | [specific requirement] | [observed behavior] | PASS/FAIL/NOT_RUN | [file + revision] | [if any] |

A should be able to distinguish: implementation compliance, economic validity, test reproducibility, unresolved design change, and residual user-facing usability risk. A's review is not a guarantee of perfection.

### 4.3 User-facing demonstration

For a financial-capability stage, provide a small practical walkthrough: selected real ETF(s) when data are available, observation dates, assumptions, computed exposures/compensation/scenarios, meaningful selection or review judgment, and clear limitations. **Do not stop at a numerical unit test if the stage goal is an ETF decision.**

For S0, replace ETF demonstrations with: proof of two distinct real agents and follow-ups, actual changed files/tests in the disposable area, B's final integration, and a directory/repository-access check.

## 5. Run-specific evidence and naming

Recommended structure:

```text
reports/
  YYMMDD_sN_<topic>_<runid>_report.md        # durable B report
artifacts/
  work_runs/
    S<N>_YYYYMMDD_HHMM_<short_topic>/
      manifest.json                           # small metadata index
      evidence/                               # concise test and review evidence
      examples/                               # small reproducible sample outputs
```

Use new filenames/run IDs. Never overwrite past final reports; do not fill `docs/` with B-generated documents. Evidence should be small and relevant; large/raw market data, logs or caches belong outside the committed repository unless expressly required.

**Suggested `manifest.json` fields:** `run_id`, `stage_id`, `task`, `design_revision`, `source_commit`, `result_commit`, `final_report_path`, `status`, `test_commands`, `evidence_paths`, `generated_at`, `usage`, `limitations`. Use `null`/`not_exposed` for unknown facts; never invent a commit hash, count or URI.

`workflow/` contains A/user-authored standing contracts, **not B-generated reviews**. `docs/` remains A/user's design-document archive. Publication of these A-authored files during S0 is permitted only by explicit authorization; provenance must remain clear.

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
