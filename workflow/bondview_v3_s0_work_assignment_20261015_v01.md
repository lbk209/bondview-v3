# Bondview-v3 — S0 Work Assignment (Ready for Manual A → B Handoff)

**Status:** Proposed S0 assignment, requires user authorization before Work execution.  
**Prepared:** 2026-10-15  
**Intended repository location:** `workflow/` (user/Design Chat-managed).

## 1. Give B these materials

- This task brief.
- `bondview_v3_work_supervisor_operating_contract_20261015_v01.md`.
- `bondview_v3_work_handoff_output_contract_20261015_v01.md`.
- `bondview_v3_stage_gates_and_s0_setup_20261015_v01.md`.
- Repository `AGENTS.md`, `.gitignore` and the existing smoke-test specification `docs/bondview_v3_work_subagent_smoke_test_20261014.md`.

Before `workflow/` exists, **attach the four A-authored files** to Work, or provide another actually accessible source. A URL/path that Work cannot access is not a supplied file. Check required Work permissions before granting any modifications.

## 2. Ready-to-paste instruction to B

```text
You are B, the Bondview-v3 Work Supervisor. This is S0, an operational
verification and minimal repository setup, NOT financial-model implementation.

Read the attached S0 task and standing contracts plus repository AGENTS.md.
Honor their ownership, Git, evidence, authority and usage rules.
The user/Design Chat manually authorizes this S0 assignment. Do not claim
that Chat and Work can communicate automatically.

Execute S0 in two clearly separated parts:

S0-A (ISOLATED): Perform the actual subagent orchestration smoke test using
"docs/bondview_v3_work_subagent_smoke_test_20261014.md" as specification.
Use a disposable, dependency-free workspace. During S0-A, DO NOT access,
modify, or depend on the Bondview repository. Create real distinct Coding
Agent and Fixed-Income Reviewer child tasks, not a scripted impersonation.
Verify file creation/tests, a substantive reviewer follow-up, routed coding
revision, focused re-review and your own final integration. Preserve
compact evidence. Report PASS/PARTIAL/BLOCKED from observed results.

S0-B (SEPARATE REPOSITORY SETUP): Proceed ONLY if S0-A passes, if repository
access is available, and if authorized permissions permit it. At this point
the S0-A prohibition on repository use has ended; do not retroactively mix
repo work into the disposable probe. Inspect the live working tree/branches
and AGENTS.md workflow. Publish the supplied, A-authored standing contracts
under workflow/ if expressly authorized; do not alter their substance.
Initialize reports/ and artifacts/work_runs/<unique_S0_run_id>/ with a
real report/manifest and concise evidence, not decorative empty folders.
Do not create src/ or tests/ unless needed for actual task work.
Do not write any B-generated document in docs/ or workflow/. Do not move
or rewrite existing docs. Follow AGENTS.md task/session branch and PR rules;
never push directly to main without explicit authorization.

Report S0-A and S0-B independently and produce one consolidated final report
with real files, tests, branch/PR links, exact locations, decisions,
limitations, and actual agent round counts. Report token/credit usage ONLY
if genuinely exposed by the platform; otherwise say not exposed.

Keep work bounded, with no extra agents or endless retries. If S0-A is not a
verified PASS, do not perform S0-B. If repository permissions are missing,
report S0-B BLOCKED rather than inventing an artifact or bypassing approval.

Finish by giving the user a concise handoff for manual review by A. Do not
begin S1 or implement any real ETF financial logic during S0.
```

## 3. Expected final outputs

1. S0-A status with specific evidence of real agent threads, code artifacts and actual test output.
2. S0-B status with actual repository visibility, added paths and a real task PR if permitted, or a clear blocker.
3. One B-authored consolidated report in `reports/` with the required A verification matrix and user-facing explanation.
4. Run metadata and concise evidence in `artifacts/work_runs/<run_id>/` if repository setup succeeds; otherwise return any accessible disposable evidence references and explain the limitation.
5. Usage report with agent rounds, interventions and measured usage where exposed.

## 4. S0 gate

**S0 is accepted only after the user brings B's results to A and they verify that both S0-A orchestration and S0-B setup were actually completed.** Reaching this gate is not authorization to implement S1. No new preliminary development stage is required.

**Important:** The existing smoke-test prompt says never to access the repository; it applies to S0-A. Use this assignment to define a separate S0-B, not to quietly weaken or reinterpret the disposable probe.
