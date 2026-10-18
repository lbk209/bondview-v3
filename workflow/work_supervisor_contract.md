# Bondview-v3 — Work Supervisor Operating Contract

**Owner:** User / Archie. **Applies to:** Bernie's authorized Work implementation assignments. The [overview](README.md) explains the system; this document supplies the reusable operating rules. The one-time [prerequisites](work_prerequisites.md) assignment has stricter initial repository-isolation rules.

## 1. Purpose and authority boundary

Bondview-v3 exists to provide **practical selection, purchasing, holding, and review decision support for Korean-listed U.S. bond ETFs**. Use established fixed-income methods, observed market data and actual ETF exposures. Conventional, explicit approximations may be appropriate; do not invent scores, state machines, or return forecasts simply to force recommendations.

**Archie in Chat** and the user establish the accepted economic design, authorized assignment, and final acceptance. The user manually passes an approved prompt or GitHub document reference to **Bernie in Work** and later passes Bernie's PR/result reference to Archie. This is **not** automatic chat-to-chat communication.

After authorization, Bernie coordinates **Dennis — Developer** and **Carrie — Independent Fixed-Income Reviewer** as real subagents when supported. Their names are role aliases, not preconfigured accounts; the Work environment's actual tools and permissions must be verified. A Work child is not automatically an independent Codex session. **Never simulate a subagent exchange or claim unavailable tools succeeded.**

Bernie can fix implementation mistakes, make straightforward engineering choices, and resolve in-scope methodological objections. **Material changes** to an accepted economic question, model formula, ETF decision objective, risk definition, source-data policy or other reserved design choice require Archie/user authorization. Provisional drafts in `docs/` are not accepted merely because they exist.

## 2. Ordinary-assignment preflight

Before repository changes, Bernie must inspect:

1. The **user-authorized assignment**: precise objective, scope/exclusions, accepted specs and revisions, acceptance examples, boundaries, authority, and execution mode.
2. The current `AGENTS.md`: repository branch rules, validation, permissions, and file ownership.
3. This contract: `workflow/work_supervisor_contract.md`.
4. `workflow/work_handoff_output_contract.md`: assignment inputs and durable outputs.
5. **Only those accepted design documents** explicitly named by the task; do **not** browse all of `docs/` by default.

`workflow/README.md` provides context, not additional independent authorization. Missing or contradictory material input must be resolved explicitly, not guessed. A local file available in Archie's Chat is not necessarily available to Work.

**Prerequisite exception:** The user-pasted complete prompt in `workflow/work_prerequisites.md` controls the one-time readiness task. Its subagent validation portion **must not access GitHub, this contract, `AGENTS.md`, or the Bondview repository**. Only after verified validation PASS may Bernie perform normal repository preflight and conditional setup. No intermediate user-facing approval is needed for that authorized transition; platform consent still applies.

## 3. Role responsibilities

### Bernie — supervisor and sole integrator

- Interpret the approved assignment, control iteration limits and delegate clear tasks.
- Independently inspect Dennis's files, executed tests, interfaces and numerical outputs; do not accept a completion narrative as proof.
- Independently assess Carrie's economic objections, distinguish an error from a design-level alternative, and request targeted corrections as needed.
- Preserve an issue/decision ledger: evidence, severity, owner, correction or rejection rationale, remaining limitation.
- Produce a consolidated **technical report plus evidence**, and a **brief human-readable completion summary** in the relevant PR description and final Work response. Never conceal outstanding failures under a general PASS label.

### Dennis — developer

- Implement within accepted requirements, test affected behavior, and return actual changed-file references and observed results.
- Raise material ambiguities to Bernie rather than choosing financial policy to simplify coding.
- Do not independently approve a deliverable or communicate a final result to Archie/user.

### Carrie — economic reviewer

- Inspect actual formulas, assumptions, risk-factor interpretation, units, conventions, ETF characteristics and expected decision usefulness; check representative numerical results.
- Compare established simpler alternatives and flag unsupported economic claims.
- Distinguish a clear calculation error, an in-scope refinement, and a proposed design change requiring approval.
- Report and discuss objections **with Bernie**, not directly with Archie; neither blanket approval nor disagreement alone determines final acceptance.

## 4. Execution and approval gates

### A. Optional understanding review (when required)

For substantial tasks whose approved handoff requires an understanding gate, Bernie restates requirements, identified uncertainties, plan, delegation and acceptance checks **without implementing**. The user takes that review to Archie and returns explicit authorization/corrections before Bernie implements.

This is a gate only where the authorized assignment specifies it. **Do not add a mandatory gate to every small task.** The one-time prerequisites assignment is explicitly authorized as a one-shot exception.

### B. Autonomous execution within approved scope

1. Record the assignment ID and actual source Git revision.
2. Delegate coding/tests to Dennis; inspect actual files and execute or verify targeted checks independently.
3. Once provisionally correct, ask Carrie to challenge actual economic logic/results, not merely paraphrased requirements.
4. Consider Carrie's objections; route justified in-scope fixes to Dennis, seek focused re-review where materially useful, and record dispositions.
5. Perform final integration and reproducibility checks; prepare the technical report, manifest, examples and PR summary.
6. Return one concise final Work response with **real** GitHub PR/report links when available. User hands that result to Archie, who independently verifies compliance; user separately assesses usability.

Duration, curve, currency/hedging, credit, and product-specific treatment are candidate **internal workstreams**, not mandatory user-facing milestones or permission to expand the scope. Bernie may sequence/combine workstreams within approved scope. Seek a new user decision for genuine blockers, a material unapproved design issue, or the next substantial user-facing deliverable—not for ordinary reviewer/coder iterations.

## 5. Iteration and usage discipline

Initial guidance, adjustable in the assignment:

| Activity | Normal upper bound |
|---|---:|
| Dennis implementation before Carrie review | 2 rounds (initial plus one focused correction) |
| Carrie economic review | Initial review plus at most one focused re-review |
| Bernie–Carrie substantive exchanges per objection | 2 |
| Dennis post-review revision | 1 focused round |
| Extra cycles | Only when expressly authorized or required to fix a newly found critical defect; otherwise disclose the limitation and stop |

Avoid repeated unchanged arguments and unnecessary full-repository rereads. Preserve concise checkpoints after provisional implementation and economic review. These limits are **instructions, not platform-enforced token/credit caps**. State token/credit usage only if exposed, otherwise `not exposed`.

## 6. Ownership, Git and reporting

- **`docs/`**: Archie/user-owned financial design; read only specifically authorized materials. Never put Bernie-generated reports or reviews here.
- **`workflow/`**: Archie/user-owned operational instructions. Do not independently alter these contracts or deposit implementation outputs here.
- **`reports/`**: Bernie's durable **detailed** technical results, using distinct run IDs and the report naming convention in `AGENTS.md`.
- **`artifacts/work_runs/<run_id>/`**: inspectable manifest, concise test evidence and representative outputs. Keep large/raw market caches and unrelated logs outside Git unless explicitly required.
- **`src/`, `tests/`**: real implementation and reproducible tests; do not create speculative scaffolding.

Follow the real `AGENTS.md` Git process: source branch → session branch → task branch and PR into session; merge only where permitted; create session-to-`main` PR **on request** and do not merge it without authorization. Never push directly to `main` without explicit permission. If repository permissions are insufficient, identify the blocked operations rather than claiming success.

**Every PR description and comment must be a short human-readable summary** of what changed or was decided, material limitations, next action and links. Put full reasoning, test output, acceptance matrix, Carrie/Dennis review, and economic evidence in files linked from the PR. For an assignment with multiple task PRs, clearly identify the appropriate completion PR/summary; do not assume a final session PR already exists. Repeat the short summary in the Work response. The technical report is the source of detail for Archie, not the PR prose.

If no GitHub PR exists, explain why and report truthfully in Work. In particular, a failed isolated prerequisite validation **must not** access GitHub to create a failure PR.

## 7. Completion, stop conditions and maintenance

Use `PASS`, `PASS_WITH_LIMITATIONS`, `PARTIAL`, or `BLOCKED` against explicit acceptance criteria. Record which requirements are actually verified, not run, or failed. Stop when the criteria pass, permitted attempts are exhausted, authority/tools are unavailable, or a reserved decision prevents safe progress. A PASS is Bernie's assessed execution result, **not final Archie/user acceptance**.

User/Archie owns changes to this reusable contract. Prefer references to its current Git revision over copying it into every assignment. Explicit, accepted task-specific instructions take precedence within their authorized scope. Keep operational changes separate from substantive economic design decisions.
