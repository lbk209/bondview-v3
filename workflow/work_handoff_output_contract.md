# Bondview-v3 — Work Handoff, Evidence and Output Contract

**Owner:** User / Archie. **Applies to:** Inputs and deliverables for user-authorized Bernie Work assignments. For actual delegation and execution behavior, see [`work_supervisor_contract.md`](work_supervisor_contract.md). For the one-time readiness task, follow the self-contained [`work_prerequisites.md`](work_prerequisites.md) prompt and its initial GitHub-access prohibition.

## 1. Objective and document relationships

Each user-facing assignment should contain **a focused task brief** rather than repeat standing operating instructions. The user and **Archie** accept its economic scope and execution authorization. **Bernie** coordinates **Dennis** and **Carrie**, verifies real results, and publishes inspectable outputs. Internal reviews, corrections, and financial workstreams are not themselves new user-facing stages.

| Standing source | Responsibility |
|---|---|
| Root `AGENTS.md` | Baseline repository rules, Git branches/PRs, testing, directory ownership |
| `workflow/work_supervisor_contract.md` | Subagent delegation, economic challenge, authority and bounded iterations |
| **This contract** | Handoff completeness, report/evidence/PR structure, final checks |
| Explicitly accepted task/design revisions | Financial requirements and allowed design choices; provisional files in `docs/` are not automatically accepted |
| `workflow/README.md` | Overview and user operating steps; not independent implementation authority |

## 2. Mandatory handoff fields

The task need not repeat these contracts, but **must identify** the relevant accepted inputs and concrete success criteria:

| Field | What to specify |
|---|---|
| Assignment identifier | Human-readable purpose, task/assignment ID, unique run ID when known |
| Source/revision | Repository, target baseline branch/commit where pinned, accepted specifications and sections |
| Scope | Actual feature/result to produce, exclusions, practical ETF decision being supported |
| Economic requirements | Formulas, risk factors, conventions, units, proxies, acceptable approximations and limitations, when applicable |
| Data/environment | Required market and ETF data, available data connections or fixtures, dates/cutoffs, available permissions |
| Acceptance | Observable behavior, hand-checkable numerical examples, expected user demonstration, error/missing-data checks |
| Delegated discretion | What Bernie may decide, what must return to Archie/user |
| Execution mode | Understanding review only, separately authorized implementation, or explicit one-shot authorization |
| Outputs/limits | Special resource bounds or deliverables differing from this contract, if any |

Do not invent missing data, access, approved thresholds or accepted economic decisions. If essential conditions are unresolved, return an honest understanding/blocker report instead of manufacturing authorization.

## 3. Minimal reusable assignment template

```text
Assignment / run ID: [unique ID or short topic]
Repository/base revision: [repo, branch; commit if pinned]
Execution: [understanding review only | authorized implementation]
Accepted design/source documents: [exact paths, sections, revisions]
Practical ETF decision capability: [what should become possible]
In scope / out of scope: [...]
Economic methods, assumptions, permitted proxies: [...]
Data sources, dates and access: [...]
Observable numerical examples, tests and acceptance criteria: [...]
Bernie's discretion and reserved user/Archie decisions: [...]
Required user demonstration: [...]
Special iteration or resource limits (if any): [...]
Follow AGENTS.md and both current workflow/*_contract.md documents.
Keep generated results outside docs/ and workflow/. Publish a human-readable
PR summary and detailed report/evidence wherever a genuine PR is possible.
```

The one-time prerequisites assignment is deliberately *not* launched with this abbreviated template. Paste the entire isolated validation prompt from `work_prerequisites.md` once; repository reads begin only if that validation has passed.

## 4. One authoritative completion package — two reading levels

For normal GitHub-backed work, Bernie produces **one coherent completion package**, with an entry-point PR summary and a detailed technical report. Do **not** create a second `summary.md` merely to duplicate PR prose; do not scatter the actual technical conclusions across unrelated subagent narratives.

### 4.1 Human-readable PR description and comments — for the user

**Every PR description and PR comment** must be short, understandable without reading raw logs, and appropriate to its scope. The primary assignment completion summary belongs in the **relevant PR description** whenever such a PR exists. Updates or decisions may appear as brief PR comments, with links to detailed evidence in files.

Recommended summary fields, in a few lines or bullets:

- **What changed or was decided?** One or two sentences.
- **Outcome:** `PASS`, `PASS_WITH_LIMITATIONS`, `PARTIAL` or `BLOCKED`, stating whose assessment it is.
- **Important limitations or unresolved decisions:** Only material ones.
- **Next action:** What the user or Archie should review/approve, if anything.
- **Details:** Actual links to the detailed report, evidence and relevant code/commits.

The summary can include concise test status and PR scope, satisfying `AGENTS.md` PR reporting requirements without inserting full test transcripts, extended financial analysis, or long review conversations. Do not assert merged-to-`main` status unless verified. If work comprises multiple task PRs under an unfinished session, clearly identify which PR is the completion entry point. A session-to-main PR occurs **when requested**, not automatically after each assignment.

**Final Work response:** Repeat or link the same short user-facing summary and the verified PR/report references. If no PR can be created, provide the summary in Work and state the exact missing authorization/tool; do not invent links. **If initial prerequisite subagent validation fails, no GitHub access or PR is permitted:** the direct Work response is the only completion medium.

### 4.2 Detailed durable technical report — for Archie

Create one report under `reports/` with a unique filename compatible with the `AGENTS.md` convention, for example:

`reports/YYMMDD_<scope>_<topic>_<runid>_report.md`

The report is the **authoritative technical account** of the assignment and should include, as relevant:

1. **Executive result and scope:** status, what was completed, what was not, and why.
2. **Provenance:** approved specs and revisions, actual environment, source/output commit IDs, branches, PR numbers and true merge state.
3. **Requirements-to-evidence matrix:** item-specific `PASS` / `FAIL` / `NOT_RUN` / `NOT_APPLICABLE`, observed behavior, evidence path and limitation. Overall PASS never substitutes for item-level findings.
4. **Implementation:** changed files, interfaces/behavior changes, actual commands/checks and observed outcomes.
5. **Economic correctness:** representative calculations, convention/units, sign checks, hand-checkable expected versus observed values and tolerances, supported versus hypothetical results.
6. **Carrie's independent review and Bernie's dispositions:** substantive objections, simpler alternatives, what was fixed, rejected or deferred, rationale and corresponding Dennis changes.
7. **Remaining risk/deviations:** unverified acceptance items, data gaps, important proxies, inconsistent outputs or reserved design decisions.
8. **Delegation/usage:** actual subagent rounds, interruptions, user permissions/checkpoints, measured token/credit usage only if exposed (`not exposed` otherwise).
9. **User demonstration:** reproducible steps and clear limitations; see Section 5.
10. **Verified artifact index:** paths/PR links to evidence and outputs; never claim files exist merely from chat text.

Keep it readable but sufficiently detailed that Archie can assess design compliance and economic validity **without having to trust Bernie's conclusions**. Full transcripts and bulky caches are not automatically required: preserve the evidence necessary for independent verification.

### 4.3 Evidence and run-specific manifest

```text
reports/
  YYMMDD_<scope>_<topic>_<runid>_report.md
artifacts/
  work_runs/
    <run_id>/
      manifest.json
      evidence/
      examples/
```

Use unique run IDs; never overwrite previous reports/evidence. Place material reproducible tests in `tests/`, code in `src/`, and small auditable outcomes in the run evidence tree. Keep unneeded large/raw logs, market data, downloaded caches and temporary smoke-test code outside committed source unless expressly necessary. `docs/` and `workflow/` are **never** Bernie-generated output destinations.

Suggested `manifest.json` keys: `run_id`, `assignment_id`, `task`, `design_revision`, `source_commit`, `result_commit`, `final_report_path`, `status`, `test_commands`, `evidence_paths`, `generated_at`, `usage`, `limitations`. Use `null` or `not_exposed` where appropriate. Link only genuinely persistent/accessible files.

## 5. Archie review and user demonstration

Provide an inspectable table of the form:

| Requirement | Accepted behavior | Observed test/output | Status | Evidence location | Limitation |
|---|---|---|---|---|---|
| R-01 | [specific requirement] | [observed result] | PASS/FAIL/NOT_RUN | [file at actual revision] | [if applicable] |

Archie needs to distinguish **implementation compliance**, **economic validity**, **reproducibility**, **reserved design changes**, and **usability gaps**. Archie reviews underlying files, actual code, data conventions, numerical examples and Carrie/Dennis evidence; a favorable PR summary is not sufficient.

For financial assignments, include a small real-world walkthrough: the actual ETF(s) where data permit, observation dates, assumed exposures, computed risks/scenarios/carry where authorized, comparisons or decision implications, and explicit limitations. Never present a scenario sensitivity as a realized return or a forecast. A unit test alone does not prove that a completed financial feature helps select or review ETFs.

For prerequisite validation, the demonstration instead establishes actual distinct child agents, follow-up, code revision, re-review, executed tests, and conditional repository setup. Record the two internal outcomes separately within the **single** completion report if publication is permitted.

## 6. Completion checklist and exceptions

- [ ] Bernie's report matches the approved task and actual Git revision; deviations and reserved decisions are explicit.
- [ ] Bernie inspected the actual deliverables and independently ran or validated material tests.
- [ ] Carrie provided substantive economic review where relevant; dispositions are recorded; Dennis fixed accepted in-scope objections.
- [ ] Every material acceptance criterion has specific evidence, status and limitations.
- [ ] Real PR description and comments are short human-readable summaries with links, **not** substitutes for detailed evidence.
- [ ] The final Work response supplies a concise, truthful result and exact accessible PR/report links where available.
- [ ] No Bernie outputs were written to `docs/` or `workflow/`; no unauthorized direct write to `main`.
- [ ] Usage statistics, child-agent interactions, tests, commits and access are never invented.
- [ ] If GitHub or PR creation is impossible, the obstacle and unavailable durable results are identified honestly.
- [ ] For failed initial prerequisite validation, the repository has **not** been accessed; the Work response documents the failure and repository setup is `NOT RUN`.

**Acceptance rule:** Bernie may mark execution PASS, but **Archie/user retains independent review and final acceptance**. No completed task silently authorizes subsequent financial implementation.
