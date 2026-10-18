# Bondview-v3 — Work Collaboration Overview

**Purpose:** Explain how the Archie–Bernie workflow is used, why it is structured this way, and where its authoritative operating rules live. This overview is not a new contract or an accepted financial-design specification.

**Names used below:** The **user** approves assignments and results; **Archie** handles design and independent review in Chat; **Bernie** supervises execution in Work; **Dennis** implements and **Carrie** reviews fixed-income logic as Bernie's subagents when real delegation is available.

## 1. How to use this workflow

1. **Prepare with Archie (Chat).** Agree on the objective, authorized scope, accepted design references, and observable acceptance criteria (including numerical checks when relevant). Draft financial-design documents in `docs/` are provisional unless specifically accepted.
2. **Launch Bernie (Work).** Give Bernie the authorized assignment prompt or a GitHub specification link/revision. Point to `AGENTS.md`, [`work_supervisor_contract.md`](work_supervisor_contract.md) and [`work_handoff_output_contract.md`](work_handoff_output_contract.md). State whether implementation is already authorized or a separate understanding review is required.
3. **Leave internal work to Bernie.** Bernie coordinates Dennis and Carrie, verifies implementation and economic results, and handles corrections. The user intervenes only for a required understanding/authorization gate, platform permission, genuine blocker, or reserved design decision. Internal tasks are not separate user-facing assignments.
4. **Receive the final review PR automatically.** Bernie manages intermediate **task PRs** (task branch → session branch) and, upon completing the authorized GitHub-backed assignment, opens a **session PR** (session branch → `main`) without another user request. The session PR description summarizes the completed capability and its most meaningful verified results and limitations; it **does not copy all task PR details**. Technical reports and evidence are linked separately. Bernie does **not** merge this PR into `main`.
5. **Review and accept.** The user reads the concise session PR description, gives the PR URL to Archie for review of `reports/`, code/tests and `artifacts/work_runs/`, and decides whether to request corrections or merge. Bernie's `PASS` is not Archie/user acceptance. If a PR cannot be created, Bernie reports the real limitation and any available results directly in Work.

**First run:** Before financial implementation, run the one-time [`work_prerequisites.md`](work_prerequisites.md) assignment. It contains the **complete ready-to-paste prompt**. Bernie conducts initial subagent validation without GitHub/repository access, then performs repository setup only after verified validation success. If validation fails, Bernie reports in Work and must not access GitHub.

## 2. Why the workflow exists

Bondview-v3 supports practical selection, purchase, holding and review decisions for **Korean-listed U.S. bond ETFs** using established fixed-income methods, observable market data and actual ETF exposures. The financial architecture and examples in `docs/` remain subject to critical review.

Keeping Archie in Chat separates economical design and independent acceptance from implementation and verification in Work. User-mediated handoffs are brief; Bernie manages ordinary developer/reviewer iterations autonomously within the authorized scope.

## 3. Roles and authority

| Role | Responsibility | Boundary |
|---|---|---|
| **User** | Approves assignments, reserved design decisions and final acceptance | Transfers the assignment to Bernie and completed PR reference to Archie |
| **Archie — Chat** | Designs, challenges assumptions, accepts requirements and independently reviews results | Does not supervise Bernie's subagents or silently approve design changes |
| **Bernie — Work** | Orchestrates assigned implementation, verifies outcomes, resolves in-scope objections and reports | Must not silently change accepted economic requirements |
| **Carrie — Work subagent** | Reviews fixed-income methods, ETF exposures and decision usefulness | Reports to Bernie; does not set design policy |
| **Dennis — Work subagent** | Implements and tests the accepted assignment | Reports to Bernie; does not set financial policy |

These names denote roles, not preconfigured accounts or proof of subagent availability. Bernie must report missing tools/permissions rather than simulate delegation.

## 4. Execution and approval boundaries

After authorization, Bernie may divide an assignment into coding, financial review, corrections and verification tasks. An ETF topic (e.g., duration, curve, currency or credit) is **not automatically** a separate user-facing stage. An understanding review is required **only when specified by the approved assignment**. Material unapproved design choices and genuine blockers return to the user and Archie.

GitHub branch and PR policy is defined in `AGENTS.md`: verified task PRs are merged into the assignment's session branch; upon completion, Bernie opens the session-to-`main` PR for human review and leaves it unmerged. Keep unrelated assignments out of the same session branch. When repository publication is impossible, no PR is invented. The isolated prerequisite validation has a stricter no-GitHub rule.

The **task PR** may explain its particular numerical/technical result in meaningful detail. The **session PR** presents a selective, integrated picture of what the entire authorized assignment achieved. Neither substitutes for the technical report; no PR should invent results, imply a forecast from a stress test, or present hypothetical fixtures as real ETF observations. Full reporting rules are in [`work_handoff_output_contract.md`](work_handoff_output_contract.md).

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
