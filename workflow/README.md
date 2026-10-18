# Bondview-v3 — Work Collaboration Overview

**Purpose:** Explain how the Archie–Bernie workflow is used, why it is structured this way, and where its authoritative operating rules live. This overview is not a new contract or an accepted financial-design specification.

**Names used below:** The **user** authorizes assignments and makes final acceptance decisions; **Archie** handles design and independent review in Chat; **Bernie** supervises execution in Work; **Dennis** implements and **Carrie** reviews fixed-income logic as Bernie's subagents when real delegation is available.

## 1. How to use this workflow

**First-time setup:** Before the first financial implementation assignment, complete the one-time [`work_prerequisites.md`](work_prerequisites.md) assignment. It contains a complete prompt to paste into Bernie’s Work session. Bernie validates actual subagent delegation without repository access, then sets up GitHub reporting only if validation succeeds. A failed initial validation must be reported in Work without accessing GitHub.

1. **Prepare the assignment with Archie (Chat).** Agree on the objective, authorized scope, accepted design references, required deliverables and observable acceptance criteria. Include hand-checkable numerical reference cases and tolerances wherever meaningful; for non-numerical requirements, define other verifiable outcomes. Documents in `docs/` are provisional unless specifically accepted.
2. **Provide Bernie with the assignment and data (Work).** Submit the approved prompt or accessible GitHub specification path and revision. Identify relevant input files or data sources, access methods, observation dates/cutoffs, assumptions and permitted proxies. Distinguish observed data from synthetic test fixtures. Data can be supplied directly or obtained by Bernie when the assignment authorizes acquisition; the required access and provenance must be clear. Reference `AGENTS.md`, [`work_supervisor_contract.md`](work_supervisor_contract.md) and [`work_handoff_output_contract.md`](work_handoff_output_contract.md), and specify any required understanding-review authorization gate.
3. **Let Bernie implement and verify.** Bernie coordinates Dennis and Carrie, checks actual outputs against the approved acceptance criteria, reviews economic validity and resolves in-scope issues. Bernie must record which measurable requirements passed, failed or could not be verified before claiming completion; a numerical match alone is not proof of a sound ETF interpretation. The user intervenes only for an explicitly required approval gate, platform permission, genuine blocker or reserved design decision.
4. **Review the completed assignment.** As part of completing authorized GitHub-backed work, Bernie opens a **session PR** (session branch → `main`) without a separate user request. Bernie manages intermediate **task PRs** (task branch → session branch) internally. The session PR highlights the integrated deliverable, a few meaningful verified results and material limitations rather than repeating all task PR details. It links to technical reports and reproducible evidence; Bernie leaves the session PR unmerged.
5. **Obtain independent review and decide whether to accept.** The user provides the session PR to Archie for independent inspection of the results, calculations, code/tests and evidence in `reports/` and `artifacts/work_runs/`. The user then judges practical usefulness, interpretability and fit with the original objective, and requests corrections or merges the PR. Bernie's `PASS` is an execution assessment, not Archie/user acceptance.

If no PR can be published, Bernie reports the actual outcome and limitation directly in Work. The full handoff fields and verification expectations are defined in [`work_handoff_output_contract.md`](work_handoff_output_contract.md); this overview does not replace them.

## 2. Why the workflow exists

Bondview-v3 supports practical selection, purchase, holding and review decisions for **Korean-listed U.S. bond ETFs** using established fixed-income methods, observable market data and actual ETF exposures. The financial architecture and examples in `docs/` remain subject to critical review.

Keeping Archie in Chat separates economical design and independent acceptance from implementation and verification in Work. User-mediated handoffs are brief; Bernie manages ordinary developer/reviewer iterations within the authorized scope.

## 3. Roles and authority

| Role | Responsibility | Boundary |
|---|---|---|
| **User** | Authorizes assignments, approves reserved design decisions and makes final acceptance/merge decisions | Transfers approved instructions to Bernie and the resulting PR to Archie |
| **Archie — Chat** | Develops and critically reviews designs, prepares requirements with the user and independently evaluates completed work | Does not supervise Bernie's subagents or independently authorize reserved changes |
| **Bernie — Work** | Orchestrates authorized work, verifies outcomes, resolves in-scope objections and reports | Must not silently change accepted economic requirements |
| **Carrie — Work subagent** | Reviews fixed-income methods, ETF exposures and decision usefulness | Reports to Bernie; does not set design policy |
| **Dennis — Work subagent** | Implements and tests the accepted assignment | Reports to Bernie; does not set financial policy |

These names denote roles, not preconfigured accounts or proof of subagent availability. Bernie must report missing tools or permissions rather than simulate delegation.

## 4. Execution and approval boundaries

After authorization, Bernie may divide an assignment into coding, financial review, corrections and verification tasks. An ETF topic (e.g., duration, curve, currency or credit) is **not inherently** a separate user-facing stage. An understanding review is required **only when specified by the approved assignment**. Material unapproved design choices and genuine blockers return to the user and Archie.

`AGENTS.md` governs branch/PR operations and publication restrictions. Intermediate task PRs are Bernie's responsibility; the final session-to-`main` PR is the normal review entry point and remains unmerged. Unrelated assignments must not be silently combined in one session branch. Initial prerequisite validation is an exception: GitHub access is prohibited until its validation passes.

Task PRs can give specific verified technical or numerical findings. The final session PR selects integrated achievements and their significance; neither replaces the detailed technical report. Do not present synthetic inputs as observed data, a stress sensitivity as a realized return, or unsupported outcomes as verified. Detailed reporting requirements are in [`work_handoff_output_contract.md`](work_handoff_output_contract.md).

## 5. Repository locations and reporting

| Location | Owner / purpose |
|---|---|
| `AGENTS.md` | Stable Git, validation, engineering and repository-level rules |
| `docs/` | User/Archie financial-design archive; no Bernie-generated material |
| `workflow/` | User/Archie operating instructions, prerequisites and reusable contracts |
| `reports/` | Bernie's durable **detailed technical reports** for independent review |
| `artifacts/work_runs/<run_id>/` | Run manifest, reproducible evidence and representative examples |
| `src/`, `tests/` | Actual application implementation and tests when justified |

**PR descriptions and comments are human-readable summaries**, not repositories for long calculation logs or Carrie/Dennis review transcripts. Important calculation conventions, detailed results, tests, review findings, limitations and actual file references belong in committed reports, code and evidence. A redundant `summary.md` is not required merely to duplicate PR prose.

## 6. Document map and precedence

| Document | Audience / purpose |
|---|---|
| **This `README.md`** | User and Archie: first actions, collaboration map and document navigation |
| [`work_prerequisites.md`](work_prerequisites.md) | User and Bernie: one-time validation/setup and full self-contained Work launch prompt |
| [`work_supervisor_contract.md`](work_supervisor_contract.md) | Bernie: authority, delegation, independent verification, iteration and stopping rules |
| [`work_handoff_output_contract.md`](work_handoff_output_contract.md) | Archie, user and Bernie: assignment inputs, PR summary rules, detailed reports and evidence |

Accepted task instructions and explicitly approved v3 financial-design decisions govern financial behavior; `AGENTS.md` governs baseline Git and engineering procedures; the two contracts elaborate orchestration and deliverables. The prerequisite prompt takes precedence during its isolated validation. This overview adds no independent authority: correct any inconsistency rather than silently overriding a detailed contract.
