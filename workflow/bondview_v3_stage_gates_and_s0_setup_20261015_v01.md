# Bondview-v3 — Provisional Development Stages and S0 Repository Setup

**Status:** Proposed sequence, for discussion and subsequent approval; not a finalized economic architecture.  
**Prepared:** 2026-10-15  
**Intended repository location:** `workflow/` (user/Design Chat-managed).

## 1. Stage principle

Each stage should deliver a **small end-to-end ETF decision-support capability**, actual implementation evidence, and a user-facing demonstration where relevant. A manually reviews B's completed output with the user before the next stage. B, C and D operate autonomously **within** an authorized stage; the A–B handoffs remain manual.

Avoid treating Duration, Curve, Credit and Currency as obligatory independent scores. The proposed order below is for incremental practical validation, not financial-model authority; A/user can merge, split or reorder stages after reviewing the accepted architecture.

## 2. Provisional roadmap

| Stage | Candidate scope | Completion question / gate |
|---|---|---|
| **S0** | Verify Work subagents, repository access, Git/report permissions and folder conventions | Can B orchestrate actual C/D work and create verifiable deliverables in permitted locations? |
| **S1** | One Treasury ETF decision vertical slice: observed Treasury conditions + actual ETF duration + conventional sensitivity and minimum defensible compensation assumptions | Can the system produce a meaningful conditional buy/hold/review assessment, not only display rates? |
| **S2** | Curve/nonparallel sensitivity where supported; ETF-to-ETF and same-ETF-over-time comparisons | Do curve and exposure differences change meaningful comparisons correctly? |
| **S3** | KRW investor: hedged vs unhedged exposure, FX and hedge-economics approximations | Are currency-specific ETF judgments defensible and transparently conditional? |
| **S4** | Credit-aware ETFs: Treasury-rate versus credit-spread sensitivity and compensation | Are credit ETF decisions not incorrectly treated as Treasury-only judgments? |
| **S5** | Other supported structures (e.g. futures) and final integrated workflow, as justified | Can selected product types be handled correctly with usable decision outputs and no unsupported universal formula? |

Stage boundaries are provisional. Some currency/compensation treatment may already be required in S1, depending on the accepted ETF and investment objective. S5 is not an obligation to model every derivative product.

## 3. Common gate at the end of every financial stage

1. B verifies requirements, tests, economic results and completeness of delivered artifacts.
2. C reviews the actual economic implementation and substantive ETF decision usefulness.
3. B resolves in-scope issues through D within bounded iterations; otherwise reports limitations/reserved design questions.
4. B provides an A-readable evidence matrix and a separate user-facing demonstration in its consolidated report.
5. User transfers B's result to A. A evaluates financial and architectural compliance; the user evaluates usability and missed issues.
6. A/user explicitly accepts, requests targeted correction, or defers the next stage. Code that merely runs is not sufficient evidence that the stage's ETF decision goal was reached.

## 4. S0 combines smoke test and folder initialization; no separate pre-stage needed

**S0 has two deliberately separate substages**, to protect the validity of the original disposable probe:

### S0-A: isolated real-subagent smoke test

Use the existing `docs/bondview_v3_work_subagent_smoke_test_20261014.md` as the smoke-test specification. The smoke phase must **not** access, modify or depend on the Bondview repository. Verify two actual distinct agents; D's file creation, B's actual test run, C's follow-up, D's economic revision, C's re-review, B's integrated report; record genuine PASS/PARTIAL/BLOCKED. If tools are absent, do not pretend a textual role-play is a pass.

### S0-B: repository access and folder setup

Proceed only after S0-A passes **and** the user has authorized repository modifications and any required platform permissions are granted. This is a separate operation, which may use the same Work session if the tool/permissions allow, or a separate task within S0. Never retroactively claim S0-A used the repository.

1. Inspect repository branch, uncommitted changes, remote state, `.gitignore`, `AGENTS.md` and current folders before edits.
2. Confirm the A/user-authored standing contracts are accessible (attached or already available in repository). When specifically authorized, publish these supplied files in `workflow/`; do not rewrite them as B-generated design documents.
3. Create only directory paths for actual deliverables: `reports/` and `artifacts/work_runs/<S0_run_id>/` using meaningful files, not placeholder empty directories. Create `src/` and `tests/` only when a real implementation task requires them.
4. Record a small S0 manifest, setup evidence and **one B-authored report under `reports/`**. Do not put B-generated files under `docs/` or `workflow/`.
5. Use the existing `AGENTS.md` session/task branch → PR process; do not push to `main` without explicit user authorization. Verify PR, commit, file and branch references before reporting them.
6. Check that generated evidence is actually accessible from the intended Work environment; cloud paths alone do not establish local Ubuntu availability. Exclude bulky temporary probe files from the repository.

**S0 outcome:** The real-agent orchestration check and repository setup should each have its own status. If the smoke test fails, do not conceal that by successfully creating folders. If repo permissions fail after smoke passes, report **S0-A PASS / S0-B BLOCKED**; the overall S0 remains incomplete.

### Folder ownership after S0

```text
bondview-v3/
  AGENTS.md
  docs/                                   # user/A archive; READ-ONLY to B by default
  workflow/                               # A/user-authored standing contracts
    bondview_v3_work_supervisor_operating_contract_20261015_v01.md
    bondview_v3_work_handoff_output_contract_20261015_v01.md
    bondview_v3_stage_gates_and_s0_setup_20261015_v01.md
    bondview_v3_s0_work_assignment_20261015_v01.md
  reports/                                # B's unique consolidated reports
  artifacts/work_runs/<run_id>/            # B's evidence, manifest and examples
  src/                                     # only when implementation requires it
  tests/                                   # only when implementation requires it
```

Do not treat this folder proposal as a command to move existing design files out of `docs/` or create empty software modules during S0.

## 5. S0 acceptance checklist

- [ ] S0-A passed the **actual** smoke-test evidence criteria.
- [ ] S0-B verified repository access, permission scope and compatibility with `AGENTS.md`.
- [ ] A/user's standing contracts are accessible to future Work assignments via confirmed repository paths or designated attachments.
- [ ] B generated no documents under `docs/` and did not silently modify accepted design.
- [ ] Run report and small evidence index have unique filenames, verified references and accessible locations.
- [ ] Actual agent rounds and available usage figures (or `not exposed`) are reported.
- [ ] User can return the completed S0 report to A for acceptance before S1.

## 6. Do not overbuild S0

S0 checks orchestration, environment, evidence and file conventions. It is **not** a miniature Bondview MVP, an invitation to define duration/credit models, or proof that subagents will scale reliably to large later stages. An additional S-minus-1 stage adds coordination without a corresponding independent economic outcome; two substages inside S0 are sufficient.
