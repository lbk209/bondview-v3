# AGENTS.md

## Purpose

Stable working instructions for coding agents in `lbk209/bondview-v3`. This file governs development practices, not the financial model. Task-specific user instructions take precedence where more specific. Add further analytical or implementation contracts only as the v3 design is reviewed and accepted.

## Project context

Bondview-v3 is a new project for analyzing U.S. bond-market conditions and supporting decisions about Korean-listed U.S. bond ETFs.

The current research direction is to apply established fixed-income quantitative methods to observable market data and the actual economic characteristics of each ETF. The intended outputs include numerical analysis, within-ETF comparisons across market conditions, cross-ETF comparisons, and useful bond-market interpretation. The project does not require forecasting future ETF prices or returns.

**This is a direction, not a finalized calculation, investment-policy, data, or result contract.** Do not infer that particular formulas, decision labels, thresholds, model layers, or examples have been accepted merely from this summary.

`lbk209/bondview-v2`, `lbk209/bondview`, and their previous conversations are historical references only. No earlier architecture, terminology, classification, score, rule table, or implementation is authoritative for v3 unless explicitly adopted.

## Design sources and authority

- Consult the current v3 repository and the user-identified design documents for each task.
- The present working documents are `docs/bond_etf_decision_architecture.md` and `docs/bond_etf_decision_examples.md`. **Both are provisional research drafts**, not automatically accepted model contracts.
- A specifically accepted v3 design or task instruction takes precedence over a provisional draft. Follow the most specific applicable accepted specification while respecting accepted higher-level constraints.
- Identify material inconsistencies between documents, examples, and code; do not resolve them silently by treating existing implementation or illustrative outputs as authoritative.
- In an explicit design-review task, critically test and revise proposals rather than preserving an earlier draft for its own sake. Do not change accepted design merely to rationalize a coding deviation.

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

Retain the established session-branch review workflow for v3 unless the user directs otherwise.

1. Before editing, inspect the current branch, working tree, recent commits, and live remote branches; fetch/prune remote tracking references. Protect uncommitted or unpushed work.
2. Use `main` as the source branch unless directed otherwise. Never commit or push directly to `main` without explicit authorization.
3. Work on a remote-visible session branch named `codex/session/YYMMDD_HHMM`. If exactly one live session branch exists, reuse it; if none exists, create one from the source branch. If multiple valid session branches exist, ask the user which to use. An explicit request to start a new session overrides reuse.
4. For each task, create `codex/task/YYMMDD_HHMM_<short_task_name>` from the session branch. Commit and push the task, then open a PR **into the session branch**.
5. Include in the task PR: what changed, relevant files, checks performed and their results, behavior impact, and limitations. When the requested checks pass and the PR record is complete, merge the task PR into the session branch unless directed otherwise; clean up the task branch when safe.
6. Keep durable research/audit conclusions in a committed document or PR when needed for future work. Do not create a separate report when the task is explicitly chat-only/local-only or its deliverable already records the findings. Use `reports/YYMMDD_<scope>_<topic>_<report_type>.md` for dedicated reports.
7. On request to finish the session, open a final PR from the session branch into `main`, summarizing task PRs, validation, and remaining concerns. **Do not merge this final PR**; the user reviews and merges it.
8. Report the session branch, relevant PR link, merge status, tests, and limitations after completing a GitHub task. Do not claim a branch, commit, or PR exists unless verified.

The branch workflow is an operational convention, not an economic-model design requirement. New v3-specific instructions may be added as the design matures.
