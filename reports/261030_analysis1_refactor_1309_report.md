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

## Stage 3 — PASS

Implemented `build_conditional_scenarios()` and independent `ScenarioSet` in
`bondview.analysis.scenarios`. Added `market.scenarios(...)`, `summary()`,
`show_summary()` and `show_plot()`. Separate presentation and plotting modules
use stored joint vectors. Top-level facade exports are lazy so independent
numerical imports do not load the facade, 1A/1B code or visualization modules.
No common result superclass, forecasting methods, Analysis 2 returns or
Analysis 3 risk calculations were added. No new dependencies were needed.

### Construction and assumptions

This is a deterministic historical selection convention chosen under the
assignment's engineering discretion, not an investment-policy threshold:

1. Validate existing daily Percent Treasury inputs and per-ID metadata. Require
   DGS2, DGS10 and DGS30 at each eligible observation date. Never fill yields.
2. Reference bounds are inclusive; defaults are the first/last complete common
   observation dates. Preserve requested and effective coverage separately.
3. Monthly starts are each calendar month's last complete common observation;
   daily starts are every complete common observation. Partial reference months
   are included. An incomplete last row does not supply a start.
4. Target = actual start + configured calendar months, with day clipped at month
   end. Exclude targets later than the last complete reference observation.
5. Use the last complete observation on/before the target **within its calendar
   month**. Exclude a window if no such observation exists; never reach into a
   different month to compensate for a gap.
6. Subtract the same actual start/end yields for all three tenors and multiply
   percent-point differences by 100 to obtain bp. Round floating cancellation
   to 10 decimals in bp, consistent with 1A; no display rounding sets membership.
7. Apply inclusive finite numeric bounds to DGS2 or DGS10 and retain the entire
   matching vector. Overlapping windows remain dependent historical evidence.

For example, the synthetic leap-year fixture's 2024-01-31 → 2024-07-31 vector
is `(20, -25, 50)` bp with 182 actual elapsed days; the exact condition
`DGS10 ∈ [-25, -25]` retains it. A one-month target from 2024-01-31 clips to
2024-02-29. A 2024-03-29 target uses the available 2024-03-28 endpoint.
These are test constructions, not market observations.

### Data and reuse contract

`ScenarioSet.scenarios` is a full pandas DataFrame with columns:

| Column | Meaning |
|---|---|
| `scenario_id` | Stable `UST_YYYYMMDD_YYYYMMDD` actual-endpoint identity |
| `start_date`, `end_date` | Actual common historical endpoints |
| `target_end_date` | Calendar-month target before observation matching |
| `elapsed_days` | Actual endpoint difference in calendar days |
| `DGS2_change_bp`, `DGS10_change_bp`, `DGS30_change_bp` | Complete same-interval numerical changes |

`ScenarioSet.metadata` holds schema/type, factor identity, input/output units,
condition and inclusive bounds, horizon, sampling/start/target/endpoint rules,
requested/effective reference dates, missing-data rule, per-ID source/retrieval
provenance, overlap/interpretation and quantile convention. Counts distinguish
reference rows, complete dates, excluded incomplete rows, sampled starts,
immature targets, unmatched target months, eligible windows and selected rows.
Provenance is copied defensively from input; no point-in-time data is invented.
IDs deliberately stay stable across filters/sampling/source revisions for the
same interval; use accompanying provenance to distinguish retrieval snapshots.

Independent downstream use needs no facade or plotting:

```python
from bondview.analysis.scenarios import build_conditional_scenarios
scenario_set = build_conditional_scenarios(
    observations, condition_tenor="DGS10", lower_bp=-25, upper_bp=25,
    horizon_months=6, sampling="monthly",
)
joint_vectors = scenario_set.scenarios
construction_and_sources = scenario_set.metadata
```

Analyses 2/3 can preserve each row's full vector and ID across compared exposures
and choose a documented year-fraction treatment using actual dates/elapsed days.
The nominal month horizon must not silently replace actual elapsed periods.
The exposed pandas objects and metadata are intentionally inspectable/mutable;
callers should retain their own copies if modifying them.

### Presentation and notebook

The complete machine-readable set is the primary output. A secondary table
reports minimum/P10/median/P90/maximum in bp using linear marginal quantiles,
with condition, coverage and selected/eligible counts. A tertiary Plotly scatter
uses Δ2Y vs Δ30Y colored by Δ10Y, or Δ10Y vs Δ30Y colored by Δ2Y, with actual
interval dates, target and elapsed days in hover. Presentation text/units use
`labels.yaml`. Empty selections retain typed columns, NaN summaries and an
empty chart. No complete reference data raises an explicit error.

Moved Treasury loading into shared setup. C executes from that setup alone;
B uses its own `kw_date_range` selector and explicit KW inputs. Removed
unimplemented KW-conditioned scenario placeholders: KW is not a scenario input.
Notebook code outputs are cleared; no large saved display payload is committed.

### Verified evidence and limitations

- Focused scenario suite: **11 PASS**. Tests check independent endpoint
  enumeration, signs/units, inclusive boundaries, calendar/leap handling,
  complete vectors, missing months, coverage, reproducible IDs, provenance,
  hand-calculated summaries, both plot mappings and no rebuild during display.
- Full regression suite: **59 PASS**, including two fresh offline kernels.
  One runs C with only Treasury snapshots/setup and neither A, B nor KW inputs;
  both condition tenors are exercised. Another checks full notebook reruns,
  source cache preservation and sparse-history empty output.
- Full current notebook also executed offline against existing local Treasury
  and KW snapshots, without downloading or changing those caches.
- Modified Python files compile; `git diff --check` passes. Complete affected
  calculation, facade, presenter and plotting units were reviewed directly by
  Codex, not by an independent reviewer/subagent.
- A newly written notebook fixture initially expected four eligible windows;
  hand enumeration identified three. Corrected that test expectation before
  the passing regression run. No unresolved introduced failure remains.

**Observed cached-data integration:** existing DGS snapshots dated 2026-10-28
provide complete common coverage 1977-02-15 to 2026-10-26 (12,419 complete dates,
546 incomplete rows within default bounds). For a six-calendar-month inclusive
10Y condition of [-25, +25] bp, monthly sampling gives **153 selected / 590
eligible**; daily gives **3,230 / 12,142**. Every selected vector was separately
checked against source endpoint subtraction, condition bounds and elapsed days.
File hashes, copied provenance, counts, summaries and three representative rows
per sampling mode are in
[cached_history_check.json](../artifacts/work_runs/261030_1309_analysis1/cached_history_check.json).
This validates integration with the existing retrieval snapshots; it is not an
independent source audit or a claim about information available historically.

Missing observations can shorten intervals within their target month or exclude
them altogether. The conservative maturity rule can omit the last potential
window when its calendar target lies after final observed coverage, even if a
nearby earlier business-day endpoint exists. Actual periods are visible.
Sampling and historical reference choices change descriptive samples. Overlap,
source revisions, historical availability and limited counts prevent interpreting
these quantiles/counts as independent frequencies or forecast probabilities.
No additional probability model or economic policy was inferred.

Evidence: [stage3.json](../artifacts/work_runs/261030_1309_analysis1/stage3.json).
Stage 2 publication: commit `2a06247`, [PR #52](https://github.com/lbk209/bondview-v3/pull/52),
merged as `b57ddaf`; remote/local task branches deleted and verified by Git.

## Publication and completion

| Stage | Status | Implementation/test commit | Task PR |
|---|---|---|---|
| Baseline alignment | PASS | `8732c29` | [#51](https://github.com/lbk209/bondview-v3/pull/51), merged into session |
| Facade/results | PASS | `2a06247` | [#52](https://github.com/lbk209/bondview-v3/pull/52), merged into session |
| Conditional scenarios | PASS | `d876a80` | [#53](https://github.com/lbk209/bondview-v3/pull/53), verified and published into session review workflow |

All three output contracts are satisfied. Source baseline remains fixed at
`ee79747b25ad0f45dffa7c040823560415159890`. The final session-to-main PR is
opened for user review and must remain unmerged. Its description and the final
response record the verified final PR and task-branch cleanup outcome after
publication. Session branch deletion remains exclusively the user's decision.
This report's PASS is implementation verification, not user acceptance or an
independent financial review. Final notebook cleanup was followed by a focused
rerun: **3 notebook tests PASS**; the focused scenario suite also passed after
adding a default-reference row-count invariant. Existing 1A/1B numerical,
presentation, plotting and FRED production modules remain unchanged from baseline.

## Token usage and account allowances

No reliable session token counters, context occupancy/capacity, or account
allowance counters are exposed in the tools available to this assignment.
No estimates or inference from transcript length are used.

| Metric | Stage 1 | Stage 2 | Stage 3 | Assignment total |
|---|---|---|---|---|
| Input tokens | Not available | Not available | Not available | Not available |
| Output tokens | Not available | Not available | Not available | Not available |
| Cached-input tokens | Not available | Not available | Not available | Not available |
| Reasoning-output tokens | Not available | Not available | Not available | Not available |
| Total tokens | Not available | Not available | Not available | Not available |
| Attributable stage tokens / share | Not available | Not available | Not available | Not available |
| Active context used / capacity / percent | Not available | Not available | Not available | Not available |

Beginning allowance measurement attempt: 2026-10-30 13:09:31 Asia/Seoul
(04:09:31 UTC); five-hour, weekly and other allowance percentages: **Not available**.
Stage-end allowance values: **Not available**; no measurement interface.
Cumulative consumption, context occupancy and account allowances are distinct.

Stage 1/2/3 consumption and each stage's percentage of assignment total:
**Not available**, because no reliable per-stage counter differences exist.
The available tool inventory was inspected for usage/context/account counters;
no applicable measurement interface was exposed. Goal bookkeeping is not a
session/account usage counter and was not used to fabricate statistics.
End-of-assignment allowance reporting checkpoint: 2026-10-30 13:21:18 Asia/Seoul
(04:21:18 UTC). Five-hour, weekly and other allowance percentages: **Not available**.
This timestamp records an availability check, not a successful measurement.
