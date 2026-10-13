# AGENTS.md

## Purpose

This file gives coding agents stable working instructions for the new bond-ETF research and decision-support project (initially referred to as **v3**).

It is intentionally **not** a model specification or a replacement for the project's design documents. The analytical design is still being developed. Task-specific user instructions take precedence where more specific.

## 1. Project context and design authority

### Purpose and current direction

The project aims to support decisions about Korean-listed ETFs with U.S. bond exposure, using observable bond-market information, actual ETF exposure characteristics, and established fixed-income quantitative methods.

The present design direction is to:

- Evaluate **actual ETFs**, using available quantitative characteristics rather than automatically replacing them with predefined Short / Intermediate / Long categories.
- Use market observations such as Treasury yields, yield curves, credit spreads, and FX information as appropriate. ETF documents and ETF return histories can supply instrument-specific information and empirical checks.
- Apply relevant conventional bond-pricing, sensitivity, carry/compensation, credit, and currency relationships. Different products may require different appropriate calculations.
- Produce interpretable numerical results and comparisons, including comparisons of the same ETF under different market conditions and across ETFs, to inform decisions.
- Support separate interpretation of bond-market conditions as a useful output, without requiring a prior market-level attractiveness score.
- Avoid making forecasts of future ETF prices a prerequisite for useful analysis. Standardized hypothetical scenarios and stated investment assumptions are permitted; identify them as such.

These are **current goals and design direction**, not acceptance of any particular formula, horizon, threshold, decision policy, or architecture. Do not silently turn them into a comprehensive model contract.

### Authority and maturity of documents

- **This repository's** explicitly accepted or user-designated architecture, example, and model documents govern the corresponding task. Use the most specific applicable accepted document, consistent with any accepted system-level document.
- If `docs/system_architecture.md` and `docs/evaluation_examples.md` exist, consult both for design and implementation work. They may initially be **working drafts**. Do not treat a draft, illustrative example, or hypothetical calculation as a finalized rule merely because it is present in `docs/`.
- When the acceptance status, document name, or a materially conflicting requirement is uncertain, say what is unsettled. For implementation tasks, implement only the unambiguous portion instead of silently choosing a disputed design.
- When explicitly asked to design or revise the architecture, the agent **may challenge and revise** draft conventions; preserving the old draft is not the objective.
- This `AGENTS.md` governs working practices; it should not override a later, explicitly accepted quantitative model contract.

### Relationship to earlier projects

`lbk209/bondview-v2` and the original `lbk209/bondview` are **historical references only**. Their code, documents, accepted rules, and vocabulary have no authority in this project unless the user explicitly adopts a specific item.

In particular, do **not** import the v2 architecture's Component / State Classification / Rule Case / Rule Mapping / Core Score / Macro Adjustment structure as an implicit requirement. Do not transplant v2's Duration thresholds, smoothing or stabilization conventions, or ordinal scoring rules merely because implementations are available.

Reuse individual utilities or research methods only when they solve a present task, with an appropriate review of their assumptions and dependencies. Prefer independently specified, conventional financial calculations where those answer the economic question.

## 2. Agent role and scope

- Implement the requested task, not an inferred future roadmap. Do not independently settle material investment-policy, product-coverage, or system-level design choices.
- For a local engineering choice that does not change documented behavior, choose the simplest correct implementation and proceed.
- For genuinely open research or design questions, distinguish findings, assumptions, alternatives, and the decisions still requiring user review.
- Do not introduce extensive abstractions, taxonomies, configuration schemas, or generic evaluation frameworks in anticipation of future needs.
- If the current task is an architecture or examples review, actively look for unnecessary complexity, missing economics, conflicting examples, and assumptions that do not follow from established formulas.
- Do not change the repository's authoritative design documents merely to rationalize an implementation divergence.

## 3. Analytical implementation guidance

These rules control **implementation discipline**, not which model the project ultimately adopts.

### Market observations, ETF characteristics, and calculations

- Distinguish raw market observations, transformations, ETF-provided characteristics, quantitative calculations, hypothetical scenarios, and investment judgments in code and outputs.
- Prefer actual ETF-specific numerical properties (e.g. effective duration and spread sensitivity) when reliable. If unavailable, use a representative proxy only when the task permits it; identify the approximation and do not present it as a reported ETF property.
- Use standard economic relationships for the purpose they actually support. For example, a duration-based response to an assumed rate move is **not** a verified historical ETF return or a predicted future return.
- Do not double-count equivalent sensitivities (such as applying both parallel duration and its key-rate duration decomposition as additive rate effects).
- Do not use an ordinary cash-bond return or carry formula as an exact calculation for Treasury futures, leveraged products, or other materially different structures. A limited, valid sensitivity comparison is still useful when the full return model is unavailable.
- Be careful with price versus total return, distribution adjustments, as-of dates, currency denomination and hedge assumptions. Do not invent product characteristics, yield inputs, or realized ETF performance.
- Keep current market observations separate from historical observations and clearly label hypothetical numerical fixtures.

### Quantitative outputs and decisions

- Retain meaningful continuous results and economic units (basis points, years of duration, percentage returns, DV01, etc.) rather than discretizing values by default.
- No universal attractiveness score, threshold system, Rule Table, or other proprietary evaluation machinery is required unless explicitly accepted in the new project's design.
- Different financial formulas may calculate related elements of a single economic assessment. This is not a requirement to create independent scores and combine them.
- Where a user-facing preference depends on an investment objective, constraint, scenario, or judgment, state that assumption rather than presenting it as a mathematical theorem.
- An incomplete but meaningful assessment may be preferable to constructing a detailed product model that the current decision does not need. Clearly delimit what the result does and does not establish.
- New calculations or decision mechanisms should be justified by the specific question they answer; first check whether conventional methods or direct comparisons already suffice.

### Design examples and reproducibility

- Treat design examples as **testable specifications of intended behavior**, not fabricated observations of real markets. Preserve a clear distinction between hypothetical examples and real-data MVP results.
- When implementation results differ from an example, investigate whether the discrepancy comes from inputs, assumptions, formulas, numerical precision, or a genuinely missing design decision; do not adjust the model simply to force preferred outcomes.
- Preserve enough calculation inputs, units, dates, data sources, and assumptions to reproduce important results. This does **not** require a universal component lineage system or a classification layer.
- Separate data acquisition and calculations from reporting and visualization where that separation is useful. Do not mandate additional layers merely for architectural symmetry.

## 4. General implementation rules

- Make only the requested changes; create or delete files only as needed. Avoid unrelated cleanup or broad refactoring.
- Prefer simple code at its natural call site. Avoid thin forwarding wrappers, speculative factories, and one-use abstraction layers.
- Extract a shared function or module when genuine reuse, meaningful validation, or clear responsibility justifies it—not merely because two pieces of code look similar.
- Keep one authoritative implementation of a calculation; avoid duplicate paths with subtly different conventions.
- Preserve documented APIs, input/output formats, behavior and ordering unless the task explicitly calls for a change.
- Favor clear numerical types, explicit units, missing-data behavior, and validation at external-data boundaries.
- Use configuration for parameters that actually need to vary; do not create configuration frameworks or hard-code arbitrary decisions merely to avoid discussion.
- Do not mutate caller-owned data unexpectedly, and keep reusable calculations independent of plotting and notebook display.
- Do not add dependencies without a specific present need. Use the existing Poetry environment and edit `pyproject.toml` / lockfile only when necessary.
- If a model change affects outputs, say what changed, why, and how it was checked. Never claim compatibility without verifying it.

## 5. Validation expectations

For changed Python files, run at least:

`python -m py_compile <modified_python_files>`

Also run focused tests or smoke checks for the behavior actually affected: acquisition, parsing, unit conversion, bond calculations, date alignment, FX treatment, serialization, notebooks, or plots as relevant.

For formulas, use small manually checkable numerical examples and confirm units, signs, and boundary cases. For real-data pipelines, record the source, observation date, known gaps, and refresh/cache behavior as appropriate.

Do not substitute successful execution for economic correctness. If a check cannot be run because of missing credentials, unavailable dependencies, network limits, or missing source data, report the limitation. Never fabricate validation results.

## 6. Git and GitHub workflow

The established v2 GitHub review workflow is retained provisionally, independently of v2's analytical architecture. Follow a task-specific user instruction if it explicitly replaces this workflow.

### Core branch model

Before editing, check the current branch, working tree status, recent commits, and local/remote branches. Fetch and prune remote-tracking refs before selecting the session branch. The default source branch is `main`, unless the repository or user specifies otherwise.

Use a **GitHub-visible session branch** as the durable integration branch for multi-step work. Only that session branch is long-lived among agent-created branches. Each task should create a task branch and a PR into the session branch, unless explicitly instructed otherwise.

The required remote state after each completed task is:

- A live session branch on GitHub.
- A task branch created from the current session branch.
- A reviewable task PR containing critical details and validation evidence.
- A merged task PR into the session branch once requested validation passes.

Do not push or commit directly to the source branch unless explicitly instructed. The agent must **not** merge the session branch into the source branch. Only the user may authorize that final merge.

Local checkout, branch cleanup, and temporary implementation details are subordinate to the GitHub-visible review record. Protect uncommitted or unpushed work from being overwritten.

### Branch naming

Use `codex/` for agent-created branches:

- Session: `codex/session/YYMMDD_HHMM`
- Task: `codex/task/YYMMDD_HHMM_<short_task_name>`
- Revert: `codex/revert/YYMMDD_HHMM_<short_revert_name>`

A session name identifies the session, not a specific module or task. Task names should be short and descriptive.

### Session branch selection

Use the **live remote branch state** after fetching and pruning, not stale local branch names.

- If no clear live `codex/session/` branch exists, create a new session branch from the source branch and push it before starting work.
- If exactly one exists, continue from it.
- If multiple plausible live session branches exist, ask the user to select one.
- If the user explicitly requests a new session from the source branch, create one even if another session branch exists.
- Unrelated remote branches, local-only branches, and leftover task branches are not by themselves session-branch ambiguity; inspect them for safety rather than treating them as session branches.

### Task branch and task PR

For each task:

1. Create a task branch from the current session branch.
2. Make the requested changes and run relevant validation.
3. Push the task branch and open a PR targeting the session branch.
4. Include in the PR description: summary, files changed, commands/tests run, validation outcomes, behavior impact, and limitations or unavailable checks.
5. Merge the task PR into the session branch after the requested validation passes and the PR record is complete, unless the user directs otherwise.
6. Delete the remote task branch after merge unless instructed otherwise. Update the local session branch and clean local task branches when safe.

Critical design conclusions, implementation details, and checks must be preserved in committed files or the PR description, not only in the agent's final chat message.

A later-discovered fundamentally incorrect merged task should normally be reverted by a separate revert task branch and PR. Ordinary follow-up work can use a new task branch.

After a task, report the session branch, task PR link/number, merge and cleanup status, validation results, and limitations.

### Analysis-only and audit-only work

Do not modify production code for an audit-only task.

When an audit, design review, or analysis produces durable findings needed for later work, create a Markdown report under `reports/`, commit it, and submit it through the ordinary task PR workflow. Do not create a report for a chat-only or explicitly local-only task, or when the task already creates an appropriate durable artifact.

For reports, use `reports/YYMMDD_<scope>_<topic>_<report_type>.md` with short lowercase/underscore names. Preserve key findings and rationale in the report and link it from the PR description. Reports do not replace a clear PR summary.

### Final session PR

When the user asks to finish the session, open **one final PR from the session branch into the source branch**. Do not merge it.

The final PR should summarize the session, link task PRs and any important reports, identify changed areas, explain validation and behavior impact, and state unresolved issues. The user reviews and decides whether to merge it.

## 7. Reporting and communication

- Use **English** for user-visible plans, progress, questions, PR descriptions, and final reports unless the user explicitly directs otherwise. Preserve source text, identifiers, and file content when translation would change their meaning.
- State concrete actions actually performed. Distinguish design proposals from accepted decisions and implemented behavior.
- Explain relevant economic or technical assumptions in proportion to their importance; do not inflate routine decisions into extended design debates.
- Do not present research examples as live market results, and do not promise future returns from backward-looking calculations.
