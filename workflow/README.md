# Bondview-v3 — Work Collaboration Overview

**Purpose:** Explain how the Archie–Bernie workflow operates, give the user the minimum steps to run an assignment, and link to detailed operating contracts. This overview is not a new contract or a substitute for accepted financial design.

## 1. Why the workflow exists

Bondview-v3 supports practical decisions about **Korean-listed U.S. bond ETFs**, grounded in established fixed-income methods, observed market data, and actual ETF exposures. Architecture and examples under `docs/` remain subject to critical review; their existence alone does not authorize implementation.

The workflow separates **design and independent acceptance in Chat** from **implementation and verification in Work**. It minimizes user-mediated handoffs while allowing Bernie to manage coding and review iterations autonomously within an approved assignment.

## 2. Roles and authority

| Role | Responsibility | Boundary |
|---|---|---|
| **User** | Approves assignments, reserved design decisions, and final acceptance | Manually transfers a brief assignment or reference to Bernie and a result reference to Archie |
| **Archie — Chat** | Designs, critically evaluates assumptions, defines accepted requirements, and independently reviews completed results | Does not supervise Bernie's Work subagents or silently authorize design changes |
| **Bernie — Work** | Orchestrates authorized work, verifies actual outputs, resolves in-scope objections, integrates and reports | Must not silently redesign accepted economic requirements |
| **Carrie — Work subagent** | Reviews fixed-income logic, ETF exposure mapping, and practical decision usefulness | Reports to Bernie; does not approve design independently |
| **Dennis — Work subagent** | Implements and tests the accepted assignment | Reports to Bernie; does not set financial policy |

Names denote roles, not preinstalled accounts or proof that Work supports subagent delegation. Missing capabilities or permissions must be reported rather than simulated.

## 3. End-to-end lifecycle

1. **Design and authorization:** The user and Archie agree on the objective, accepted requirements, scope, acceptance criteria, and which decisions remain reserved. Where required, the user approves Bernie's understanding review before implementation.
2. **Manual handoff:** The user submits Archie's approved prompt or GitHub specification reference to Bernie in Work. A reference is generally sufficient once the supporting material is accessible.
3. **Autonomous execution:** Bernie manages Dennis and Carrie, verifies actual code, calculations and tests, and iterates within accepted scope and operating limits.
4. **Completion:** Bernie prepares a concise, human-readable PR description and final Work summary, backed by a detailed technical report and inspectable evidence. Every PR comment must also be concise and readable, linking to files for technical detail.
5. **Independent review:** The user gives Archie the relevant PR link or run ID; Archie examines the report, code, calculations, objections, and evidence. Bernie's `PASS` does **not** constitute Archie/user acceptance.
6. **Session finalization:** When the user is ready to finish the Git session, Bernie opens a session-to-`main` PR **on explicit request**. The user reviews and merges that final PR; successful task-level review does not itself merge into `main`.

A topic such as duration, curve, currency, or credit does **not** automatically require a separate user-facing assignment. Internal workstreams and ordinary reviewer/developer iterations belong to Bernie. Material unapproved design choices and genuine blockers return to Archie/user.

## 4. User operating procedure

For an **ordinary assignment**, the practical steps are:

1. **Prepare with Archie (Chat).** Establish the objective, authorized scope, accepted design references, and concrete acceptance criteria, including numerical checks where relevant. Distinguish accepted decisions from provisional material in `docs/`.
2. **Launch Bernie (Work).** Open a Work session and provide the approved assignment prompt or GitHub path/revision. Reference `AGENTS.md`, [`work_supervisor_contract.md`](work_supervisor_contract.md), and [`work_handoff_output_contract.md`](work_handoff_output_contract.md). State whether immediate implementation is authorized or an understanding review is required first.
3. **Handle exceptions only.** If an understanding review is required, have Archie evaluate it and return the authorization or corrections. Otherwise Bernie manages internal delegation, corrections, economic review, and tests. The user responds only to mandatory platform permissions, material reserved decisions, or genuine blockers.
4. **Review the result.** Read the short PR description and Bernie's final Work summary. Give Archie the PR link or run ID to examine the detailed report in `reports/`, changes/tests, and evidence in `artifacts/work_runs/<run_id>/`. Accept, request a focused correction, or defer a reserved decision based on that review.
5. **Finish the Git session when appropriate.** Explicitly ask Bernie to open the session-to-`main` PR, then review and merge it. The user does not need to do this for each internal task. If GitHub or PR publication was impossible, Bernie reports the actual limitation and available results in Work without fabricating links.

For the **first run**, complete the one-time readiness assignment in [`work_prerequisites.md`](work_prerequisites.md) before starting financial implementation. That file contains the entire self-contained prompt. Its two internal activities must not be launched separately. If isolated validation fails, Bernie must **not access GitHub** and instead reports the failure directly in Work.

## 5. Repository locations and reporting

| Location | Owner / purpose |
|---|---|
| `AGENTS.md` | Stable repository-level engineering, Git, validation and safety conventions |
| `docs/` | User/Archie financial-design archive; no Bernie-generated material |
| `workflow/` | User/Archie instructions: this overview, prerequisites, and reusable contracts |
| `reports/` | Bernie's **detailed**, durable per-assignment technical reports |
| `artifacts/work_runs/<run_id>/` | Bernie's run manifest and focused verification evidence/examples |
| `src/`, `tests/` | Actual implementation and reproducible tests when warranted |

Repository-changing work follows the session/task branch → PR workflow in `AGENTS.md`. **PR descriptions and comments are human-readable summaries**, not locations for full logs, lengthy reasoning, or economic review evidence. The technical detail belongs in linked files under `reports/` and `artifacts/`. No separate summary Markdown is required merely to duplicate PR prose. If an authorized PR does not exist, Bernie must describe the limitation truthfully in Work.

## 6. Document map and precedence

| Document | Audience / purpose |
|---|---|
| **This `README.md`** | **User and Archie:** system overview, practical user actions, and reference map |
| [`work_prerequisites.md`](work_prerequisites.md) | **User and Bernie:** one-time validation/setup instructions plus the complete ready-to-paste Work prompt |
| [`work_supervisor_contract.md`](work_supervisor_contract.md) | **Bernie:** authority, subagent delegation, validation, iteration limits, and stopping conditions |
| [`work_handoff_output_contract.md`](work_handoff_output_contract.md) | **Archie, user, and Bernie:** assignment inputs, PR summary rules, durable reports, and evidence requirements |

Explicitly accepted tasks and v3 financial-design decisions govern economic behavior. `AGENTS.md` governs baseline repository operations. The supervisor and handoff contracts supply the detailed operating requirements. The prerequisite prompt takes precedence for its initial isolated test. This overview introduces no additional independent requirements; inconsistencies with a detailed contract must be resolved explicitly.
