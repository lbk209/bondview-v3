# Analysis 1 interface and conditional scenarios

Assignment run: `261030_1309_analysis1`. Direct execution; no subagents.
Session: `codex/session/261030_1309`.
Fixed GitHub main baseline: `ee79747b25ad0f45dffa7c040823560415159890`.
Starting checkout `user_review` was clean. Remote references were fetched/pruned;
its commits remain protected. Authorized design inputs: assignment, AGENTS.md
§§1–7, development guidelines, architecture §§3.1, 3.2, 4, baseline code/notebook.
No user-owned design or workflow files were edited.

## Stage 1 — PASS

Baseline execution found 3 failures and 16 errors among 39 discovered cases
(two modules could not import). The failures encoded former multi-ID CSV v1 /
nested metadata, verbose reports, removed single-maturity KW plotting and old
notebook cell layouts. Corrected tests to reflect current per-ID CSV v2, flat
metadata, concise reports with explicit detail calls, trimmed outer missing
padding, combined KW plotting and two date selectors. Preserved arithmetic,
precision, invalid input, provenance, safe publication and missing-data checks.
The removed single-maturity plotting test targeted a function absent from main;
combined chart checks retain the applicable layout/hover expectations.

Production calculations and presentation were unchanged. Added test-purpose
documentation. All **44 tests PASS**, including a fresh offline notebook kernel.
The first sandboxed notebook attempt could not open local sockets; rerunning
with required local access passed. Modified Python test files compile, and
`git diff --check` passes. No unresolved baseline failure blocks Stage 2.
Evidence: [stage1.json](../artifacts/work_runs/261030_1309_analysis1/stage1.json).

## Stage 2 — PASS

Added `TreasuryMarketAnalysis` in `bondview.market`, exported from `bondview`.
`show_history(start, end)` delegates existing history presentation.
`curve(start, end, ..., yield_change_tolerance_bp=..., slope_tolerance_bp=...)`
returns `CurveResult.data`, exactly the existing `analyze_curve` DataFrame.
`CurveResult.show()` delegates the existing table/interpretation presenter.
`decomposition(kw_observations, start, end)` returns `DecompositionResult.paths`,
the existing `analyze_kw_decomposition` dictionary. Its `show()` plots and returns
the existing combined KW Figure. Display calls use retained results, without
financial recomputation. No common superclass or mutable current-result/date
state exists. Source observations are read at calculation time; KW is explicit.
Existing direct functions and calculations are unchanged.

Updated the current notebook and its usage documentation; cleared stored outputs
(including bulky historical Plotly payloads). Numerical equivalence, chart JSON
equivalence, repeated display without recalculation and standalone 1B are tested.
Focused facade tests: **3 PASS**; full suite: **47 PASS**, including offline
notebook reruns. Modified Python files compile; whitespace checks pass.
No unresolved introduced regressions. Results expose ordinary mutable pandas
objects for notebook inspection; callers can edit them deliberately.
Evidence: [stage2.json](../artifacts/work_runs/261030_1309_analysis1/stage2.json).
Stage 1 publication: commit `8732c29`, [PR #51](https://github.com/lbk209/bondview-v3/pull/51),
merged as `2f7ae6a`; remote/local task branches deleted and verified by Git.

## Token usage and account allowances

No reliable session token counters, context occupancy/capacity, or account
allowance counters are exposed in the tools available to this assignment.
No estimates or inference from transcript length are used.

| Metric | Stage 1 | Stage 2 | Assignment total |
|---|---|---|---|
| Input tokens | Not available | Not available | Not available |
| Output tokens | Not available | Not available | Not available |
| Cached-input tokens | Not available | Not available | Not available |
| Reasoning-output tokens | Not available | Not available | Not available |
| Total tokens | Not available | Not available | Not available |
| Attributable stage tokens / share | Not available | Not available | Not available |
| Active context used / capacity / percent | Not available | Not available | Not available |

Beginning allowance measurement attempt: 2026-10-30 13:09:31 Asia/Seoul
(04:09:31 UTC); five-hour, weekly and other allowance percentages: **Not available**.
Stage-end allowance values: **Not available**; no measurement interface.
Cumulative consumption, context occupancy and account allowances are distinct.
