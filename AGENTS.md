# AGENTS.md

## 1. Purpose and execution model

Stable working instructions for agents operating in `lbk209/bondview-v3`. This file governs development practices and execution workflows, not the financial model. Task-specific user instructions take precedence where more specific. Add further analytical or implementation contracts only as the v3 design is reviewed and accepted.

**Direct execution is the default.** Codex executes the user's assigned task directly, using its own capabilities and applicable tools:

- For coding assignments, implement, validate, and report the results.
- For fixed-income or financial-design reviews, independently examine the requested questions and report findings.
- For mixed assignments, perform the authorized responsibilities within the same execution context.

Do not automatically create subagents or adopt Bernie's supervision workflow. Do not represent Codex's own testing or review as verification by an independent subagent.

The general instructions in Sections 1–7 apply to all assignments. The additional instructions in Section 8 apply **only when the user explicitly authorizes a Bernie-supervised assignment**.

Both execution modes follow the same general project, design-authority, implementation, validation, and GitHub workflow requirements unless explicitly overridden by the authorized task.

## 2. Project context

Bondview-v3 is a new project whose ultimate purpose is practical selection, purchase, holding and review decisions for Korean-listed U.S. bond ETFs, supported by analysis of U.S. bond-market conditions.

The current research direction is to apply established fixed-income methods to observable market data and actual ETF characteristics. Numerical analysis and market interpretation serve useful ETF comparisons and practical investment judgments. Reasonable, explicit conventional assumptions and bounded decision policies are acceptable; forecasting future yields, ETF prices or realized returns is not a prerequisite. Do not invent arbitrary rules merely to force a recommendation.

**This is a direction, not a finalized calculation, investment-policy, data, or result contract.** Do not infer that particular formulas, decision labels, thresholds, model layers, or examples have been accepted merely from this summary.

`lbk209/bondview-v2`, `lbk209/bondview`, and their previous conversations are historical references only. No earlier architecture, terminology, classification, score, rule table, or implementation is authoritative for v3 unless explicitly adopted.

## 3. Design sources and authority

- Consult only the design documents authorized for the current task. The user/Archie owns the `docs/` archive; its contents must not be treated as automatically authorized inputs. For financial assignments, access the applicable design documents when the user's task instructions or accepted handoff authorize them.
- Existing architecture and examples in `docs/` remain provisional until explicitly accepted. Mere repository presence does not make a financial model authoritative.
- A specifically accepted v3 design or task instruction takes precedence over a provisional draft. Follow the most specific applicable accepted specification while respecting accepted higher-level constraints.
- Identify material inconsistencies between documents, examples, and code; do not resolve them silently by treating existing implementation or illustrative outputs as authoritative.
- In an explicit design-review task, critically test and revise proposals rather than preserving an earlier draft for its own sake. Do not change accepted design merely to rationalize a coding deviation.

## 4. Source and output directory ownership

- `docs/`: User/Archie-owned financial-design archive. Do not generate implementation reports, reviews, or task artifacts here. Read or modify only specifically authorized design documents.
- `workflow/`: User/Archie-owned operational instructions. Do not silently edit these documents or save generated work here. Bernie-specific workflow contracts apply only to assignments explicitly using the Bernie-supervised execution mode.
- `reports/`: Unique, durable detailed technical reports for GitHub-backed assignments, using `YYMMDD_<scope>_<topic>_<runid>_report.md` or a consistent unique variant.
- `artifacts/work_runs/<run_id>/`: Concise manifests and verifiable evidence/examples, with unique run IDs. Avoid committing unnecessary large logs, market-data caches, or disposable probe code.
- `src/` and `tests/`: Actual code and reproducible tests when needed.

Repository outputs follow authorized task/session branches and verifiable PRs. Do not claim PRs, files, tests, or usage counts unless observed. Never overwrite earlier run deliverables.

For explicitly chat-only or local-only assignments, follow the requested output scope rather than creating unnecessary GitHub deliverables.

## 5. Implementation and review practices

- Do only the requested work. Do not infer a larger implementation roadmap or decide unresolved investment policy on the user's behalf.
- Make straightforward local engineering choices without unnecessary discussion. Surface material economic or architectural assumptions when they affect behavior.
- Prefer clear, small implementations over speculative frameworks, thin wrappers, unnecessary classes, and premature abstractions.
- Reuse code only after checking its assumptions and relevance. Do not import Bondview-v2's analytical machinery merely because the code exists.
- Keep market observations, ETF characteristics, quantitative calculations, and investment judgments distinguishable; use appropriate units, dates, and clearly identified assumptions.
- Prefer established financial calculations where suitable. Do not introduce custom scoring, classification, or decision rules merely to fill an architectural template.
- Do not mistake scenario sensitivities for realized returns or forecasts. Label hypothetical examples, estimates, and unavailable inputs honestly.
- Keep data acquisition and reusable calculations independent of visualization where useful, without requiring a fixed module hierarchy.
- Preserve existing interfaces and behavior unless the task asks to change them; describe and test intentional behavior changes.
- Use the project's Poetry environment. Add dependencies only for a current need.
- Follow `workflow/development_guidelines.md` for applicable coding, data handling, validation, and presentation guidelines. In Bernie-supervised assignments, Bernie must ensure that relevant subagents follow these guidelines.

## 6. Validation and reporting

- Run `python -m py_compile` for modified Python files, plus focused tests for affected behavior when applicable.
- For numerical methods, test signs, units, simple hand-checkable cases, missing values, and relevant assumptions.
- For analytical or financial reviews, distinguish verified evidence from assumptions, judgments, and unresolved questions.
- Report checks performed, results, behavior changes, and checks that could not be run. Never claim validation that was not performed.
- For GitHub-backed assignments, publish one detailed, inspectable technical report under `reports/`, with supporting evidence under `artifacts/work_runs/<run_id>/`. Give the user a short, human-readable completion summary in the final session-to-`main` PR description and final response when GitHub publication succeeds.
- Every PR description and comment must be understandable to a human and link to separate files for detailed rationale, numerical checks, logs, and review evidence.
- Task PRs may be more detailed; their summaries emphasize verified changes and observable results. The final session PR synthesizes the most decision-relevant outcomes and limitations without copying every task PR result or number.
- Do not create a redundant summary file merely to duplicate PR prose.
- If no authorized PR exists, report the result truthfully without inventing a GitHub deliverable.
- Keep successful implementation or validation distinct from user acceptance of the financial design.
- Separate factual observations, derived calculations, working assumptions, and investment judgments in technical reports. Keep findings in proportion to the task.
- Use English for user-facing communication, plans, PRs, and reports, unless the user explicitly requests another language. Do not alter source text or identifiers merely to translate them.

## 7. Git and GitHub workflow

Retain the established session-branch review workflow for v3 unless the user directs otherwise. These rules apply to authorized GitHub-backed assignments regardless of whether Codex executes directly or Bernie supervises subagents.

1. Before editing, inspect the current branch, working tree (when a checkout is available), recent commits and live remote branches. Fetch/prune remote references when using Git locally; if operating only through GitHub APIs, verify the equivalent accessible remote state and disclose unavailable checks. Protect uncommitted or unpushed work. Before starting implementation in a local checkout, verify that the assigned working directory is clean. If uncommitted changes are present, stop and inform the user. Do not automatically commit, stash, discard, or bypass those changes by creating a temporary clone or worktree without explicit authorization.

2. Use `main` as the source branch unless directed otherwise. Never commit or push directly to `main` without explicit authorization.

3. Use a remote-visible session branch named `codex/session/YYMMDD_HHMM` for the authorized user-facing GitHub-backed assignment, based on the approved source revision. Reuse an existing session branch **only when it belongs to the same unfinished assignment or the user explicitly requests continuation**. Do not reuse a branch merely because it is the only live session branch; do not silently combine unrelated assignments. If branch ownership or intended base cannot be determined safely, seek clarification rather than risk unrelated changes.

4. For each task, create `codex/task/YYMMDD_HHMM_<short_task_name>` from the session branch. Commit and push the task, then open a PR **into the session branch**.

5. In **every task PR description**, explain the specific behavior or capability added, representative **verified** test/calculation results where useful, material limitations and links to technical evidence. Task PRs may contain more relevant detail than the final session PR, but not full logs or unsupported conclusions. **Every PR comment must remain concise and human-readable**; put detailed reasoning and supporting reviews in linked files. When checks pass and the PR record is complete, merge the task PR into the session branch unless directed otherwise. After confirming the merge, delete both the remote task branch and the corresponding local task branch (when a local checkout is used), provided deletion is safe. Switch away from the task branch before local deletion; never force-delete a branch containing unmerged work. Before declaring the assignment complete, verify that merged task branches have been removed from the remote and the local checkout, as applicable. If a branch must be retained or cleanup is unavailable, identify the branch and reason explicitly in the completion report. Session branch deletion, whether local or remote, is exclusively the user's responsibility. Codex must not delete session branches, regardless of whether their final review PRs exist or are open, merged, or closed. Creating or selecting a new session branch does not authorize deletion of an existing session branch.

6. For ordinary GitHub-backed assignments, commit the detailed technical report under `reports/` and run-specific evidence under `artifacts/work_runs/`. Keep substantial research/audit conclusions in durable files rather than long PR discussions. Do not require such a report for an explicitly chat-only/local-only task, and do not invent a GitHub deliverable when access or permission is missing.

7. **As part of completing an authorized GitHub-backed assignment, automatically open a final PR from its session branch into `main`; no separate user request is needed.** Its description is the primary user-facing completion summary: emphasize the integrated outcome and practical significance, select only representative verified results, state material limitations and link to the detailed report/evidence. Do not aggregate every task PR number or reproduce an exhaustive task list. **Never merge this final PR**; the user independently reviews it and decides whether to merge. For `PARTIAL` results with reviewable repository changes, use a clearly labeled draft PR where possible; if no reviewable changes or permission exist, report the blocker without fabricating a PR. If another base branch is explicitly authorized, follow that instruction instead of assuming `main`.

8. Report the session branch, relevant PR link, merge status, tests, and limitations after completing a GitHub task. Do not claim a branch, commit, or PR exists unless verified.

The branch workflow is an operational convention, not an economic-model design requirement. New v3-specific instructions may be added as the design matures.

## 8. Bernie-supervised assignments

**This section applies only when the user explicitly authorizes the Bernie-supervised workflow.** It adds orchestration requirements to the general instructions above; it does not redefine ordinary Codex execution.

### 8.1 Named roles

- **Archie — Designer / Design Chat:** Works with the user to approve financial design, stage specifications, and final acceptance. Chat-to-Work handoffs are manual and user-mediated; no agent should claim to message Archie automatically.
- **Bernie — Work Orchestrator / Supervisor:** Leads an explicitly authorized Work task, directs subagents, independently checks implementation evidence, resolves in-scope objections, and delivers a detailed technical report with a concise human-readable summary.
- **Carrie — Fixed-Income Reviewer:** A separate actual reviewer subagent, tasked by Bernie to challenge economic correctness and ETF decision usefulness. Carrie reports only to Bernie.
- **Dennis — Developer / Coding Agent:** A separate actual coding subagent, tasked by Bernie to implement and test. Dennis reports only to Bernie.

These names are role aliases, not accounts, model identities, preconfigured agents, or proof that subagent spawning is available.

### 8.2 Delegation and supervision

- An authorized assignment determines permitted actions and iteration limits.
- Create real, distinct subagents only through actual delegation capabilities. Do not simulate the existence of child agents; report unavailable tooling honestly.
- For substantial financial implementation assignments, use the Archie–user understanding-review and authorization gate **only when specified** in the approved handoff.
- Once authorized, Bernie manages internal workstreams and their reviews without routine user intervention.
- Bernie–Carrie–Dennis iterations are bounded by `workflow/work_supervisor_contract.md`; internal coding or financial-aspect tasks are not automatically new user-facing assignments.
- Significant departures from accepted financial design remain reserved for the user and Archie.
- Keep Bernie's reported `PASS` distinct from Archie/user final acceptance. Report real evidence and limitations, not just an overall status.
- For Bernie-supervised assignments, delegate in-scope development to an actual Dennis subagent and in-scope fixed-income review to an actual Carrie subagent.
- Bernie supervises their work, verifies evidence, coordinates corrections, and reports the integrated results.
- Bernie must not silently replace required subagent work with its own execution. If actual delegation is unavailable, report the limitation and do not claim that the supervised workflow was completed.
- Apply Git task-branch and PR requirements to repository changes, not to every internal reasoning, review, or correction round.

### 8.3 Additional workflow contracts

For Bernie-supervised assignments, use the applicable instructions in:

- `workflow/work_supervisor_contract.md`
- `workflow/work_handoff_output_contract.md`
- The approved assignment or handoff

These documents augment but do not replace the general requirements of `AGENTS.md`.

The workflow overview is explanatory, not independent authority.

Bernie reads the applicable contracts but must not silently edit `workflow/`. The user/Archie owns these operational instructions.

Bernie-generated reports and evidence belong in `reports/` and `artifacts/work_runs/`, not `docs/` or `workflow/`.

For authorized GitHub-backed Bernie assignments, Bernie must follow the GitHub workflow in Section 7, including task PRs, verified merges, reporting, and the final unmerged session PR. Delegation does not transfer Bernie's responsibility for verifying these outcomes.

The GitHub restrictions during isolated Work Prerequisites validation remain applicable. Do not create duplicate reporting or PR procedures merely because subagents are involved.

### 8.4 One-time Work Prerequisites assignment

The user launches a **single, self-contained prompt** from `workflow/work_prerequisites.md`.

Bernie manages two conditional **internal activities**:

1. Isolated real-subagent validation in a disposable workspace.
2. Repository setup **only if** validation genuinely passes.

During validation, Bernie must **not access GitHub or the Bondview repository**, including `AGENTS.md`, `docs/`, or `workflow/`; all validation instructions must be supplied in the user-pasted prompt.

Only after `PASS` may Bernie access GitHub, inspect `AGENTS.md` and the standing contracts, and create authorized reports/evidence through the Git workflow.

During conditional prerequisite repository setup, verify the existing contracts and repository state before publishing. Do not republish duplicate contracts or artifacts.

No separate user launch or routine approval is required for the transition; platform permission prompts still apply.

If validation fails, do not attempt setup or access GitHub: report the failure directly in Work.

A successful prerequisite run does **not** authorize financial-model implementation. The prerequisite probe must not create empty application scaffolding.

The one-time prerequisite procedure does not apply to ordinary Codex assignments.