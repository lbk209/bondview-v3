# AGENTS.md

## Purpose

Stable working instructions for coding agents in `lbk209/bondview-v3`. This file governs development practices, not the financial model. Task-specific user instructions take precedence where more specific. Add further analytical or implementation contracts only as the v3 design is reviewed and accepted.

## Project context

Bondview-v3 is a new project whose ultimate purpose is practical selection, purchase, holding and review decisions for Korean-listed U.S. bond ETFs, supported by analysis of U.S. bond-market conditions.

The current research direction is to apply established fixed-income methods to observable market data and actual ETF characteristics. Numerical analysis and market interpretation serve useful ETF comparisons and practical investment judgments. Reasonable, explicit conventional assumptions and bounded decision policies are acceptable; forecasting future yields, ETF prices or realized returns is not a prerequisite. Do not invent arbitrary rules merely to force a recommendation.

**This is a direction, not a finalized calculation, investment-policy, data, or result contract.** Do not infer that particular formulas, decision labels, thresholds, model layers, or examples have been accepted merely from this summary.

`lbk209/bondview-v2`, `lbk209/bondview`, and their previous conversations are historical references only. No earlier architecture, terminology, classification, score, rule table, or implementation is authoritative for v3 unless explicitly adopted.

## Design sources and authority

- Consult only the documents authorized for the current task. The user/Archie owns the `docs/` archive; it is not an input to the one-time Work Prerequisites assignment and must not be browsed automatically. For later financial assignments, access a particular design document only when the accepted handoff expressly names it.
- Existing architecture and examples in `docs/` remain provisional until explicitly accepted. Mere repository presence does not make a financial model authoritative.
- A specifically accepted v3 design or task instruction takes precedence over a provisional draft. Follow the most specific applicable accepted specification while respecting accepted higher-level constraints.
- Identify material inconsistencies between documents, examples, and code; do not resolve them silently by treating existing implementation or illustrative outputs as authoritative.
- In an explicit design-review task, critically test and revise proposals rather than preserving an earlier draft for its own sake. Do not change accepted design merely to rationalize a coding deviation.

## Named roles and Work task boundary

- **Archie (A) — Designer / Design Chat:** Works with the user to approve financial design, stage specifications, and final acceptance. Chat-to-Work handoffs are **manual and user-mediated**; no agent should claim to message Archie automatically.
- **Bernie (B) — Work Orchestrator / Supervisor:** Leads an explicitly authorized Work task, directs subagents, independently checks implementation evidence, resolves in-scope objections, and delivers a detailed technical report with a concise human-readable summary.
- **Carrie (C) — Fixed-Income Reviewer:** A separate actual reviewer subagent, tasked by Bernie to challenge economic correctness and ETF decision usefulness. Carrie reports only to Bernie.
- **Dennis (D) — Developer / Coding Agent:** A separate actual coding subagent, tasked by Bernie to implement and test. Dennis reports only to Bernie.

The names are **role aliases**, not accounts, model identities, preconfigured agents, or proof that subagent spawning is available. An authorized assignment determines permitted actions and iteration limits. Do not simulate the existence of child agents; report unavailable tooling honestly. For substantial financial implementation assignments, use the Archie–user understanding-review and authorization gate **only when specified** in the approved handoff. Once authorized, Bernie manages internal workstreams and their reviews without routine user intervention. Bernie–Carrie–Dennis iterations are bounded by `workflow/work_supervisor_contract.md`; internal coding or financial-aspect tasks are not automatically new user-facing assignments. Significant departures from accepted financial design remain reserved for the user and Archie.

**One-time Work Prerequisites assignment:** The user launches a **single, self-contained prompt** from `workflow/work_prerequisites.md`. Bernie manages two conditional **internal activities**: (1) isolated real-subagent validation in a disposable workspace; (2) repository setup **only if** validation genuinely passes. During validation, Bernie must **not access GitHub or the Bondview repository**, including this file, `docs/`, or `workflow/`; all validation instructions must be supplied in the user-pasted prompt. Only after PASS may Bernie access GitHub, inspect `AGENTS.md` and the standing contracts, and create authorized reports/evidence through the Git workflow. No separate user launch or routine approval is required for the transition; platform permission prompts still apply. If validation fails, do not attempt setup or access GitHub: report the failure directly in Work. A successful prerequisite run does **not** authorize financial-model implementation.

## Source and output directory ownership

- `docs/`: user/Archie-owned financial-design archive. Bernie and subagents must not generate reports, reviews, or task artifacts there. Read or modify only specifically authorized design documents in a later assignment.
- `workflow/`: user/Archie-owned operational instructions, comprising `README.md` (overview), `quickstart.md` (user actions), `work_prerequisites.md` (one-time self-contained setup and validation), `work_supervisor_contract.md` (Bernie's supervision), and `work_handoff_output_contract.md` (inputs/outputs and evidence). Bernie reads the applicable contracts but must not silently edit them or save generated work here.
- `reports/`: Bernie's unique, durable **detailed technical reports** for GitHub-backed assignments, using `YYMMDD_<scope>_<topic>_<runid>_report.md` (or a consistent unique variant).
- `artifacts/work_runs/<run_id>/`: concise manifests and verifiable evidence/examples, with unique run IDs. Avoid committing unnecessary large logs, market-data caches, or disposable probe code.
- `src/` and `tests/`: actual code and reproducible tests when needed; the prerequisite probe must not create empty application scaffolding.

Use `workflow/work_supervisor_contract.md`, `workflow/work_handoff_output_contract.md`, and the approved assignment for detailed delegation, evidence, file naming, stopping conditions and handoff rules; they augment but do not replace `AGENTS.md`. The overview and quickstart are explanatory, not independent authority. For conditional prerequisite repository setup, verify the currently available contracts; do not republish duplicates. Bernie-generated reports/evidence belong in `reports/` and `artifacts/work_runs/`, **not** `docs/` or `workflow/`. Repository outputs follow authorized task/session branches and verifiable PRs; do not claim PRs/files or usage counts unless observed. Never overwrite earlier run deliverables.

## Agent role and implementation practice

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

## Validation and reporting

- Run `python -m py_compile` for modified Python files, plus focused tests for affected behavior when applicable.
- For numerical methods, test signs, units, simple hand-checkable cases, missing values, and relevant assumptions.
- Report checks performed, results, behavior changes, and checks that could not be run. Never claim validation that was not performed.
- For GitHub-backed Bernie assignments, publish **one detailed, inspectable technical report** under `reports/` with supporting evidence under `artifacts/work_runs/<run_id>/`. Give the user a **short, human-readable completion summary** in the relevant PR description and final Work response. **Every PR description and comment** must be concise, understandable to a human, and point to separate files for detailed rationale, numerical checks, logs, and review evidence. Do not create a redundant summary file merely to duplicate PR prose. If no authorized PR exists, report truthfully in Work; during failed isolated prerequisite validation, accessing GitHub is forbidden.
- Keep Bernie's reported `PASS` distinct from Archie/user final acceptance. Report real evidence and limitations, not just an overall status.
- Separate factual observations, derived calculations, working assumptions, and investment judgments in technical reports. Keep findings in proportion to the task.
- Use English for user-facing communication, plans, PRs, and reports, unless the user explicitly requests another language. Do not alter source text or identifiers merely to translate them.

## Git and GitHub workflow

Retain the established session-branch review workflow for v3 unless the user directs otherwise. Subtasks inside one authorized Bernie assignment need not become separately user-approved stages; apply the Git task/PR rules to repository changes, not to every reasoning or review round.

1. Before editing, inspect the current branch, working tree (when a checkout is available), recent commits and live remote branches. Fetch/prune remote references when using Git locally; if operating only through GitHub APIs, verify the equivalent accessible remote state and disclose unavailable checks. Protect uncommitted or unpushed work.
2. Use `main` as the source branch unless directed otherwise. Never commit or push directly to `main` without explicit authorization.
3. Work on a remote-visible session branch named `codex/session/YYMMDD_HHMM`. If exactly one live session branch exists, reuse it; if none exists, create one from the source branch. If multiple valid session branches exist, ask the user which to use. An explicit request to start a new session overrides reuse.
4. For each task, create `codex/task/YYMMDD_HHMM_<short_task_name>` from the session branch. Commit and push the task, then open a PR **into the session branch**.
5. In **every task PR description**, briefly summarize changes, meaningful checks/results, behavior impact, limitations and links to inspectable details. **Every PR comment must also be concise and human-readable**; keep extended technical reasoning, full test logs, and supporting reviews in linked files. When the requested checks pass and the PR record is complete, merge the task PR into the session branch unless directed otherwise; clean up the task branch when safe.
6. For ordinary GitHub-backed Bernie assignments, commit the detailed technical report under `reports/` and run-specific evidence under `artifacts/work_runs/`. Keep substantial research/audit conclusions in durable files rather than long PR discussions. Do not require such a report for an explicitly chat-only/local-only task outside the normal Bernie implementation workflow, and do not invent a GitHub deliverable when access or permission is missing.
7. **On request to finish the session**, open a final PR from the session branch into `main`, with a short human-readable overview of task PRs, validation, limitations and links. **Do not merge this final PR**; the user reviews and merges it. A user-facing Bernie assignment may finish before that session PR is requested; identify the relevant task PR rather than inventing a final PR.
8. Report the session branch, relevant PR link, merge status, tests, and limitations after completing a GitHub task. Do not claim a branch, commit, or PR exists unless verified.

The branch workflow is an operational convention, not an economic-model design requirement. New v3-specific instructions may be added as the design matures.
