# AGENTS.md

## Purpose

Stable working instructions for coding agents in `lbk209/bondview-v3`. This file governs development practices, not the financial model. Task-specific user instructions take precedence where more specific. Add further analytical or implementation contracts only as the v3 design is reviewed and accepted.

## Project context

Bondview-v3 is a new project whose ultimate purpose is practical selection, purchase, holding and review decisions for Korean-listed U.S. bond ETFs, supported by analysis of U.S. bond-market conditions.

The current research direction is to apply established fixed-income methods to observable market data and actual ETF characteristics. Numerical analysis and market interpretation serve useful ETF comparisons and practical investment judgments. Reasonable, explicit conventional assumptions and bounded decision policies are acceptable; forecasting future yields, ETF prices or realized returns is not a prerequisite. Do not invent arbitrary rules merely to force a recommendation.

**This is a direction, not a finalized calculation, investment-policy, data, or result contract.** Do not infer that particular formulas, decision labels, thresholds, model layers, or examples have been accepted merely from this summary.

`lbk209/bondview-v2`, `lbk209/bondview`, and their previous conversations are historical references only. No earlier architecture, terminology, classification, score, rule table, or implementation is authoritative for v3 unless explicitly adopted.

## Design sources and authority

- Consult only the documents authorized for the current task. The user/Design Chat owns the `docs/` archive; it is not part of the S0 implementation inputs and must not be browsed automatically. For later financial stages, access a particular design document only when the accepted stage handoff expressly names it.
- Existing architecture and examples in `docs/` remain provisional until explicitly accepted. Mere repository presence does not make a financial model authoritative.
- A specifically accepted v3 design or task instruction takes precedence over a provisional draft. Follow the most specific applicable accepted specification while respecting accepted higher-level constraints.
- Identify material inconsistencies between documents, examples, and code; do not resolve them silently by treating existing implementation or illustrative outputs as authoritative.
- In an explicit design-review task, critically test and revise proposals rather than preserving an earlier draft for its own sake. Do not change accepted design merely to rationalize a coding deviation.

## Named roles and Work task boundary

- **Alisa (A) — Designer / Design Chat:** Works with the user to approve financial design, stage specifications, and final acceptance. Chat-to-Work handoffs are **manual and user-mediated**; no agent should claim to message Alisa automatically.
- **Branson (B) — Work Orchestrator / Supervisor:** Leads an explicitly authorized Work task, directs subagents, independently checks implementation evidence, handles objections, and authors one consolidated final report.
- **Clara (C) — Fixed-Income Reviewer:** A separate actual reviewer subagent, tasked by Branson to challenge economic correctness and ETF decision usefulness. Clara reports only to Branson.
- **Devon (D) — Developer / Coding Agent:** A separate actual coding subagent, tasked by Branson to implement and test. Devon reports only to Branson.

The names are **role aliases**, not accounts, model identities, preconfigured agents, or proof that subagent spawning is available. A stage assignment determines permitted actions and iteration limits. Do not simulate the existence of child agents; report unavailable tooling honestly. For substantial financial implementation assignments, use the approved Alisa–user understanding-review and authorization gate when specified in the handoff. Once authorized, Branson manages internal workstreams and their reviews without routine user intervention. Subsequent Branson–Clara–Devon iterations are bounded by the approved workflow contract; internal coding or financial-aspect tasks are not automatically new user-facing stages. Significant departures from accepted financial design remain reserved for the user and Alisa.

**Special case S0 (single user-facing Work assignment):** The user authorizes one S0 task covering two **Branson-managed internal steps**. First, **S0-A** runs a disposable subagent smoke test without opening or depending on the Bondview repository, including this file, `docs/`, or `workflow/`; the complete smoke-test instructions are included in the user-pasted S0 launch prompt. Only when S0-A genuinely passes may **S0-B** inspect the repository, read these instructions and the reusable `workflow/` contracts, and create the authorized report/evidence folders through the established Git workflow. No additional user handoff is required between these steps; platform-required permissions still apply. If S0-A fails, do not attempt S0-B. The single final S0 report must distinguish both results.

## Source and output directory ownership

- `docs/`: user/Alisa-owned design archive. Branson and subagents must not create reports, reviews or generated documents there. Reading or modifying a specific design file in a later stage requires an explicit stage instruction; S0 does not require it.
- `workflow/`: user/Alisa-owned reusable Work contracts and stage instructions. Read the specified existing contracts once per task; do not put Branson-generated results here or silently modify these contracts.
- `reports/`: Branson's unique, durable final task reports, using the report naming pattern below.
- `artifacts/work_runs/<run_id>/`: concise manifests and verifiable evidence, with unique run IDs. Avoid committing unnecessary large logs, market-data caches or disposable probe files.
- `src/` and `tests/`: actual code and reproducible tests when needed; S0 should not create empty application scaffolding.

Use the named, approved `workflow/` contracts and task brief for evidence, file naming, delegation, stop conditions and handoff requirements; these augment but do not replace `AGENTS.md`. For S0-B, verify the currently available standing contracts; do not republish duplicates. B-generated files must never be placed under `docs/` or `workflow/`. Repository output must be created on the authorized task/session branches and linked to a verified PR. Report actual usage only when exposed; do not invent token counts. Never overwrite an earlier run's deliverables.

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
- Separate factual observations, derived calculations, working assumptions, and investment judgments in reports. Keep findings in proportion to the task.
- Use English for user-facing communication, plans, PRs, and reports, unless the user explicitly requests another language. Do not alter source text or identifiers merely to translate them.

## Git and GitHub workflow

Retain the established session-branch review workflow for v3 unless the user directs otherwise. Subtasks inside one authorized Branson assignment need not become separately user-approved stages; apply the Git task/PR rules to repository changes, not to every reasoning or review round.

1. Before editing, inspect the current branch, working tree (when a checkout is available), recent commits and live remote branches. Fetch/prune remote references when using Git locally; if operating only through GitHub APIs, verify the equivalent accessible remote state and disclose unavailable checks. Protect uncommitted or unpushed work.
2. Use `main` as the source branch unless directed otherwise. Never commit or push directly to `main` without explicit authorization.
3. Work on a remote-visible session branch named `codex/session/YYMMDD_HHMM`. If exactly one live session branch exists, reuse it; if none exists, create one from the source branch. If multiple valid session branches exist, ask the user which to use. An explicit request to start a new session overrides reuse.
4. For each task, create `codex/task/YYMMDD_HHMM_<short_task_name>` from the session branch. Commit and push the task, then open a PR **into the session branch**.
5. Include in the task PR: what changed, relevant files, checks performed and their results, behavior impact, and limitations. When the requested checks pass and the PR record is complete, merge the task PR into the session branch unless directed otherwise; clean up the task branch when safe.
6. Keep durable research/audit conclusions in a committed document or PR when needed for future work. Do not create a separate report when the task is explicitly chat-only/local-only or its deliverable already records the findings. Use `reports/YYMMDD_<scope>_<topic>_<report_type>.md` for dedicated reports.
7. On request to finish the session, open a final PR from the session branch into `main`, summarizing task PRs, validation, and remaining concerns. **Do not merge this final PR**; the user reviews and merges it.
8. Report the session branch, relevant PR link, merge status, tests, and limitations after completing a GitHub task. Do not claim a branch, commit, or PR exists unless verified.

The branch workflow is an operational convention, not an economic-model design requirement. New v3-specific instructions may be added as the design matures.
