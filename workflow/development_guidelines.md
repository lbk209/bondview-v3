# Development Guidelines

These guidelines supplement `AGENTS.md` for coding, data handling, validation, and user-facing analytical presentation in Bondview-v3. They apply to direct Codex assignments and to relevant work performed by Bernie-supervised subagents, including Dennis. Bernie should ensure that the applicable guidance is conveyed to subagents and checked during review.

This is a user-maintained, evolving set of practical guidelines, **not** an independent financial-model contract. Task-specific instructions and accepted design contracts take precedence. Apply each guideline where relevant rather than introducing machinery solely to satisfy the document.

## 1. Code responsibilities and reuse

- **Before creating a new function**, inspect relevant existing functions and shared utilities. Consider whether an existing implementation could be reused or generalized through a small, justified change.
- Reuse functionality when responsibilities, assumptions, and interfaces are compatible. Do not force reuse that introduces unnecessary coupling, ambiguity, or unintended behavior changes.
- Keep generic utilities independent of analysis-specific assumptions and decisions. Let the relevant analysis determine domain-specific selection, classification, and handling rules.

### Post-modification review

- After implementing or revising code, review the **complete affected function or logical unit**, not only the edited lines. This is particularly important after multiple rounds of changes.
- Identify and simplify redundancies introduced or exposed by revisions, such as duplicate conditions, unnecessary branches, repeated assignments, unreachable code, and obsolete intermediate processing.
- Where conditional blocks have equivalent conditions, consider consolidating them **only if** execution order, state changes, side effects, and observable behavior are preserved. Identical condition text alone does not guarantee that merging is safe.
- Do not retain structural complexity solely because it existed in an earlier version.

## 2. Data handling

- Preserve the distinction between observed values, missing values, and derived results. Do not silently fill, substitute, or discard missing observations merely to produce complete-looking output.
- Apply missing-data eligibility and fallback rules at the appropriate analysis layer, according to the applicable analytical requirements. A generic selection utility should not silently impose a particular analysis's sufficiency criteria.
- Make any intentional filtering, substitution, or aggregation that materially affects the result explicit and verifiable.

## 3. Calculations and presentation configuration

- Keep numerical calculations and analytical classifications separate from user-facing text, terminology, and display formatting.
- Use the established presentation configuration (such as `labels.yaml`) for configurable labels, units, and explanatory wording rather than duplicating them in calculation code.
- Share presentation definitions only when their meanings are genuinely common across consumers. Do not couple separate analyses merely because their labels look alike.

## 4. Validation after changes

- Validate behavior against the current task and accepted requirements, not merely against existing test expectations.
- When a test appears to encode obsolete assumptions, investigate whether it identifies a genuine regression. Report the discrepancy rather than changing correct application behavior solely to satisfy the test, or dismissing the test without examination.
- Include focused checks for newly changed behavior and, where practical, for any simplification performed during post-modification review. Do not assume that passing tests alone proves the final code is free of redundant structure.

## 5. User-facing analytical presentation

- Keep explanatory text concise and relevant to interpretation. Avoid repeatedly qualifying distinctions already apparent from the analysis context.
- In Treasury tenor analyses, do not routinely emphasize that the results are *not* ETF analyses. Tenor-level observations do not carry an ETF product profile, and this distinction normally needs no repeated explanation.
- Explain the tenor-versus-ETF distinction when the user asks or when missing product-specific exposure information would materially affect an inference, comparison, or decision.
- Retain qualifications necessary to avoid materially misleading financial conclusions; do not remove important caveats merely to shorten the output.
