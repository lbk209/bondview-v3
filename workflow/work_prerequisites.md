# Bondview-v3 — Work Prerequisites

**Purpose:** Verify that Bernie's Work environment can genuinely delegate to Dennis and Carrie, and—only after that validation succeeds—initialize the permitted repository output locations. This is **one user-facing assignment**, not a financial implementation milestone or a multi-session setup procedure.

## 1. What you do

1. Open **ChatGPT Work → New session**. Choose a capable available reasoning model; Medium effort is a reasonable starting point for this operational probe, but exact model options depend on your account and interface. No extra plugins or local-folder access are prerequisites. Access to the GitHub repository is needed **only in the second internal part**.
2. Copy the **entire text block in Section 3**, starting with “You are Bernie,” into that Work session as **one prompt**. Do not shorten it to a GitHub file link: the validation portion is intentionally forbidden from reading the repository.
3. Let Bernie handle both internal activities, subject to required platform permission prompts. Do not create Carrie or Dennis yourself and do not authorize a second internal stage separately.
4. Read Bernie's final Work summary. If GitHub setup occurred, follow the real PR and detailed `reports/` / `artifacts/` links. Bring the PR URL or, on failure, Bernie's Work response back to Archie for independent review.
5. Do **not** treat readiness validation as authorization to implement bond ETF calculations. Financial assignments require their own accepted designs and scope.

## 2. What success means

| Internal activity | What must be demonstrated | If it fails |
|---|---|---|
| **Subagent validation** | Real separate Dennis and Carrie child agents; written/tested code; Bernie's independent checks; a follow-up to the *same* Carrie; a revision by the *same* Dennis; and Carrie's re-review | Stop. **Do not open GitHub or the Bondview repository.** Report the failure directly in Work |
| **Repository setup** (conditional) | Real GitHub access, required branch/PR operations, and verified report/evidence files in authorized paths | Report PARTIAL/BLOCKED with exactly what succeeded and what could not be published |

A successful initial activity without successful repository setup is not a complete prerequisite PASS. Real consent requirements cannot be overridden by the launch prompt.

## 3. Complete ready-to-paste Work prompt

```text
You are Bernie (B), the Bondview-v3 Work Orchestrator. This ONE authorized
Work Prerequisites assignment contains TWO INTERNAL, conditional activities:
(1) isolated subagent validation, then (2) repository setup only if the
validation actually passes. Do not ask the user to launch a second session or
approve a routine transition. Platform consent may still be required.
Completion of prerequisites does NOT authorize financial-model development.

ROLES AND HONESTY
- Archie (A) is the independent Designer in Chat; the user transfers results.
- Create REAL, DISTINCT child agents through actual delegation tools:
  Dennis (D), Developer / Coding Agent; and Carrie (C), Fixed-Income Reviewer.
- Keep working with the SAME Dennis and SAME Carrie threads as instructed.
- Do not role-play or fabricate a child, tool action, file, test, PR, or review.
- If real delegation/tools are unavailable, report precisely what is blocked.
- Record a compact evidence, agent-round, and usage ledger. Report token or
  credit numbers ONLY if genuinely exposed; otherwise write 'not exposed'.

PART 1 — ISOLATED SUBAGENT VALIDATION
ABSOLUTE ISOLATION: Until this part is independently verified as PASS, do NOT
open, search, fetch, clone, read, or modify the Bondview repository or GitHub.
Do not open AGENTS.md, docs/, workflow/, or any user local files. Work in a
NEW disposable writable folder named, for example,
work_subagent_probe_<unique_run_id>. Use Python's standard library only;
there is no need for Poetry, FRED, external financial data, or secrets.

1. Delegate to a REAL Dennis child to create zero_coupon.py and
   test_zero_coupon.py. The initial implementation supports ANNUAL
   compounding ONLY:
       price_annual(face, annual_yield, years)
           = face / (1 + annual_yield)**years
   Require convention docstrings, elementary validation and unittest.
   For face=100, annual_yield=0.05, years=2, the expected price is
   approximately 90.7029478458.
2. Independently inspect the actual files and execute the tests yourself.
   If needed, request at most ONE focused correction from the SAME Dennis
   before the economic review. Record commands and observed outcomes.
3. Delegate to a DIFFERENT REAL Carrie child as independent fixed-income
   reviewer. Require numerical comparison of annually versus continuously
   compounded quoted yields, discussion of yield-convention ambiguity,
   and an assessment of whether supporting both conventions is useful.
4. Send a substantive FOLLOW-UP to the SAME Carrie child:
   'If annual compounding remains the default, is optional continuously
    compounded yield a limited, useful extension? Which exact formula and
    documentation convention should be required?'
   Record the actual reply rather than substituting your own inference.
5. Evaluate Carrie's advice independently. Then send the accepted,
   limited revision to the SAME Dennis child, retaining annual support
   and ADDING:
       price_continuous(face, annual_yield, years)
           = face * exp(-annual_yield * years)
   Require convention docstrings and unittest for face=100,
   annual_yield=0.05, years=2, expected approximately 90.4837418036.
   Inspect the real revised files and rerun the tests yourself.
6. Ask the SAME Carrie child for a focused RE-REVIEW of the revision,
   implementation, and conventions. Record Carrie's actual findings and
   your own dispositions, including any outstanding disagreement.
7. Mark validation PASS only if there is concrete evidence of both distinct
   real child threads, the Carrie follow-up and re-review, routed Dennis
   revision, actual inspectable files, and executed tests. Otherwise mark
   PARTIAL or BLOCKED, state the missing evidence, and STOP here: do not
   access GitHub or the Bondview repository in any form.

Bounded iteration: no more than THREE total Dennis implementation rounds
(initial, one optional correction, reviewer-driven revision); TWO Carrie
review passes plus the requested follow-up exchange; no repeated unchanged
arguments. These are operating bounds, NOT enforced token/credit caps.

PART 2 — CONDITIONAL REPOSITORY SETUP
START ONLY AFTER YOU VERIFIED PART 1 PASS, and only with the platform's
required permissions. The prohibition on GitHub/repository access ends NOW,
not earlier. No routine additional user authorization is required.

Repository: https://github.com/lbk209/bondview-v3
Base: main, unless a later explicit user instruction changes it.

1. Check real GitHub/repository access and current branch state. Protect
   existing user work. Now read the actual repository-root AGENTS.md and
   the current reusable operating contracts under workflow/:
      workflow/work_supervisor_contract.md
      workflow/work_handoff_output_contract.md
   The overview is workflow/README.md. Use ACTUAL filenames if the checked
   branch differs; never pretend a path exists. The present self-contained
   launch prompt controls the isolation and single-session boundary.
   Do not read, browse, or modify docs/ during this prerequisite assignment.
2. Follow AGENTS.md's session/task branch -> PR rules; do not push or commit
   directly to main. Use a real task PR into the appropriate session branch;
   the session-to-main PR is only opened when explicitly required by the
   established rules or user instruction. Respect GitHub/tool permission
   checks; if an operation is unavailable, report the exact limitation.
3. Create REAL, small, durable files using unique run-specific filenames:
      reports/<YYMMDD>_prerequisites_<run_id>_report.md
      artifacts/work_runs/<run_id>/manifest.json
      artifacts/work_runs/<run_id>/evidence/...
   The detailed report must separate validation and repository setup
   outcomes, observed commands/tests, real agent interactions, review
   objections/dispositions, branch/PR/commit facts, and any limitations.
   Retain only concise, useful evidence from the disposable test; do not
   add temporary probe code to application src/ or tests/ merely to create
   scaffolding. A real report and manifest create these directories; no
   empty placeholders. Do not write generated content into workflow/ or docs/.
4. Write a SHORT, HUMAN-READABLE summary in the relevant PR description:
   outcome, accomplished work, material limitations, user action (if any),
   and links to the detailed report/evidence. ALL PR descriptions and
   comments must be readable summaries, never raw logs or long
   technical analyses. Put technical depth in files for Archie. If the PR
   covers only a task within an unfinished session, identify that scope;
   do not mislabel the PR as merged into main or finally accepted.
5. Independently verify that the named files, changes, and PR truly exist
   on the claimed branch; include exact links and commit SHA when known.
   Do not confuse a cloud workspace path with a file in the user's local
   Ubuntu folder.

FINAL BERNIE RESPONSE — ONE USER-FACING SUMMARY
Include: overall PASS / PASS_WITH_LIMITATIONS / PARTIAL / BLOCKED;
separate validation/setup outcomes (or 'NOT RUN' for setup if validation
failed); the real child delegation/review/revision evidence; the executed
unittest command and result; verified PR/report/evidence links when present;
material limitations; next action; and usage only if genuinely exposed.
If validation failed, deliver this directly in Work without GitHub access.
If repository setup occurred, use a short human-readable PR description
and direct the user/Archie to the detailed committed report and evidence.
Do not claim completion of unperformed steps, require a new user assignment,
or implement any ETF financial model.
```

## 4. Boundaries to remember

- The two internal activities are **not** separate user-facing assignments. Required platform consent is the only routine interruption exception.
- Initial isolation is intentional; the same file contains the entire validation fixture so no repository consultation is necessary.
- The Git workflow is an implementation control, not a financial-model design authority. No direct commits to `main`.
- This prerequisite uses a small bond-math fixture **to test real orchestration**, not to approve a Bondview pricing model.
- Human-readable PR summaries are useful only when a real PR exists. The detailed completion report and evidence remain in GitHub files when repository setup succeeds.
