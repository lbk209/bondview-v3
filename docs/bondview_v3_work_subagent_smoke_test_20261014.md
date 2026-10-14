# Bondview-v3 — Work Subagent Orchestration Smoke Test

**Status:** Proposed operational test; **not yet executed in the user's Work account**.  
**Date:** 2026-10-14  
**Purpose:** Verify whether one Work session can autonomously spawn a Coding Agent and a Fixed-Income Reviewer, route substantive follow-ups, produce an actual code revision, and return one Supervisor-authored report. **This is not a benchmark of financial models or implementation quality.**

## Test prerequisites

1. Open a **new ChatGPT Work** session in the same client/environment intended for Bondview-v3. This must be Work, not regular Chat or a Codex CLI session.
2. Ensure Work can create files and run shell commands in a disposable workspace. No GitHub access, Bondview repository, API key, Python packages, or financial market data are required.
3. Inspect whether the **Subagents** activity is visible in your account. Do not assume availability merely because official documentation mentions it.
4. Copy the prompt below into Work **once**. After that, do not provide intervention unless Work requires a platform permission; record any such interruption.
5. After completion, inspect the reported code and tests, the Subagents activity (if displayed), and Settings → Usage if available.

## Paste into a new Work session

```text
You are WORK SUPERVISOR conducting a small, disposable OPERATIONAL TEST.
This is a test of actual Work subagent orchestration, not a simulation of a
conversation among hypothetical roles, and not a Bondview design evaluation.

Constraints:
- Use only an isolated, newly created writable directory named
  work_subagent_probe_20261014 in your accessible workspace.
- Do not access, modify, or depend on the real Bondview repository.
- Use only the Python standard library and local shell/tools available to Work.
- Spawn REAL subagents using the available delegation tools. If the tools are
  absent or permissions block required actions, do not claim success: record
  BLOCKED with the exact missing capability.
- No additional user guidance after this one message. Do not create extra
  agents. Keep logs and model usage compact; still verify real outputs.
- You alone produce the final consolidated report.

Mandatory sequential workflow:

STEP 1: CODING AGENT -- FIRST IMPLEMENTATION
Create one actual subagent titled CODING AGENT and assign it a narrow coding
job: create zero_coupon.py and test_zero_coupon.py in the disposable folder.
First version must support annual-compounded yield ONLY:

    price_annual(face, annual_yield, years) = face / (1+annual_yield)**years

Use a clear docstring, basic input validation, and unittest-based checks,
including face=100, annual_yield=.05, years=2 (approx 90.7029478458).
The Coding Agent must return the names of files changed and the test outcome.

STEP 2: SUPERVISOR VERIFICATION
Inspect the actual files and execute the tests yourself. Do not accept the
Coding Agent's narrative report without confirming evidence. If failing,
request a targeted fix from that Coding Agent, within a maximum of one fix.

STEP 3: FIXED-INCOME REVIEWER -- FIRST ECONOMIC REVIEW
Create a DIFFERENT actual subagent titled FIXED-INCOME REVIEWER. Provide the
implemented code and results, and ask this reviewer to consider the economic
meaning of annual vs continuously compounded yields, ambiguity in yield
quoting, and whether supporting both conventions improves correctness.
Ask for at least one concrete numerical comparison and a reasoned position.

STEP 4: ACTUAL SUPERVISOR ↔ REVIEWER FOLLOW-UP
Ask the same Fixed-Income Reviewer a substantive follow-up question:
'Given a desire to preserve annual compounding as the default, is an optional
continuous-compounding convention a useful, limited extension? What must its
formula and documentation state?' Obtain the reviewer's response. Do not
substitute your own imagined response.

STEP 5: SUPERVISOR → CODING AGENT REVISION
Evaluate that response, then send a revision instruction to the Coding Agent:
keep the annual method/default and ADD continuous-compounding support using

    price_continuous(face, annual_yield, years) = face * exp(-annual_yield*years)

Provide docstrings identifying the convention and a unittest example:
face=100, annual_yield=.05, years=2 => approx 90.4837418036.
The Coding Agent must actually modify code and tests. Review and rerun tests.

STEP 6: REVIEWER RE-REVIEW
Request a focused re-review from the same Fixed-Income Reviewer of the revised
implementation and documentation. Record whether the reviewer considers the
compounding convention transparent and the implementation mathematically sound.

STEP 7: FINAL CONSOLIDATED REPORT FROM SUPERVISOR
Return exactly one final report, authored by you, containing:
- Status: PASS / PARTIAL / BLOCKED, with a short reason.
- Actual evidence of TWO distinct subagent threads (or missing-tool blocker).
- Evidence of at least one reviewer follow-up, one routed coding revision,
  and a focused reviewer re-review.
- Real files created, test command and observed output (not predicted output).
- Your own review findings and decision on the reviewer's proposal.
- Number of implementation/review rounds; any intervention or approval asked.
- Limitations and whether the result demonstrates only the intended mechanisms,
  rather than financial-model quality or reliability at Bondview scale.
- Actual usage details only if exposed; do NOT estimate or invent token counts.

Hard-ish operational instruction: after at most 3 Coding Agent implementation
rounds (initial, optional focused fix, reviewer-driven revision) and 2
Fixed-Income Reviewer review passes, stop, report PARTIAL/BLOCKED
if unfinished, and do not retry the same failed mechanism indefinitely.
These limits are instructions, not a guaranteed runtime-enforced token cap.

Never claim that a text-only role-play is an actual subagent execution.
```

## Evidence checklist

| Evidence | PASS condition |
| --- | --- |
| Actual delegation | Work Subagents activity shows two distinct specialized task threads, not only character names in one answer |
| Coding artifacts | Real `zero_coupon.py` and `test_zero_coupon.py` exist; not merely proposed source code |
| Initial checks | Annual calculation test actually runs and passes |
| Reviewer exchange | First review **and** subsequent follow-up are handled by an actual child, as evidenced by the Work activity/log |
| Rework | Coding Agent receives a later instruction; file changes and continuous-compounding test result are visible |
| Re-review | Fixed-Income Reviewer returns a second, focused assessment of the revised behavior |
| Integration | Work Supervisor produces final integrated report, without the reviewer becoming the final messenger |
| Unattended flow | No extra user instruction was needed after initiating the Work task; required system approvals, if any, are recorded |
| Stop discipline | No additional irrelevant agents or indefinite follow-up loops |

**Classification:** `PASS` means all requested orchestration steps were genuinely performed and evidenced; `PARTIAL` means some real steps completed with specific missing ones; `BLOCKED` means agent spawning or essential tool access prevented testing. The test does not establish future performance on larger workflows or any parity with standalone Codex.

## If the test fails

Record whether the failure is attributable to (a) feature availability, (b) shell/file tool permission, (c) child-message/follow-up routing, (d) agent-control/termination behavior, (e) interruption/context loss, or (f) unexpected additional user approval. Try a different Work client/model **only if you want to diagnose that specific compatibility issue**; do not repeat blindly.

## Relevant documentation

- [OpenAI — Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)
- [OpenAI — Use ChatGPT](https://learn.chatgpt.com/docs/use-chatgpt)
- [OpenAI — ChatGPT Work and Codex](https://help.openai.com/en/articles/20001275-chatgpt-work-and-codex)

