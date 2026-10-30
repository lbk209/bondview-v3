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

## Stage 3 — PASS (with window-construction correction below)

Implemented `build_conditional_scenarios()` and independent `ScenarioSet` in
`bondview.analysis.scenarios`. Added `market.scenarios(...)`, `summary()`,
`show_summary()` and `show_plot()`. Separate presentation and plotting modules
use stored joint vectors. Top-level facade exports are lazy so independent
numerical imports do not load the facade, 1A/1B code or visualization modules.
No common result superclass, forecasting methods, Analysis 2 returns or
Analysis 3 risk calculations were added. No new dependencies were needed.

### Construction and assumptions

The original start-anchored construction in `c973def` is superseded by the
user's explicit correction assignment. The current method is:

1. Validate daily Percent Treasury inputs and retain dates complete for DGS2,
   DGS10 and DGS30 within inclusive reference bounds. Defaults are the first/last
   complete common dates. Never fill, interpolate or average yields.
2. For monthly sampling, anchor the newest intended end at the latest complete
   observation. Each older end is the **original anchor minus an integer number
   of calendar months**; do not recursively shift clipped dates or use month-end
   observations as independent anchors. For daily sampling, use every complete
   observation date as an intended end, in reverse chronological order.
3. Intended start = intended end minus the calendar-month horizon, clipping at
   month ends. Stop before intended starts precede complete reference history.
4. Slice `common.loc[target_start:target_end]` inclusively. Skip fewer than two
   complete observations; otherwise use the slice's first/last actual dates.
   Never search outside the intended interval. Interior gaps are acceptable.
5. Combined shortfall = intended elapsed days minus actual elapsed days. Accept
   shortfalls of seven days or less; reject greater shortfalls. This safeguards
   both boundaries without interpolation or horizon normalization.
6. Subtract those same actual start/end yields for all three tenors and multiply
   percent-point differences by 100 to obtain bp. Round floating cancellation to
   10 decimals in bp, consistently with 1A. Keep original actual-date IDs.
7. Apply the unchanged inclusive bounds to DGS2 or DGS10 and keep entire matching
   joint vectors. All outputs follow newest intended end first.

The hand-checkable synthetic January 31 → July 31, 2024 vector remains
`(20, -25, 50)` bp with 182 elapsed days and exact 10Y condition [-25, -25].
Separate fixtures verify six-month leap-year clipping (August 31 → February 29
in 2024, February 28 in 2025) and combined shortfalls of exactly 7 vs 8 days.
These fixtures are not market observations.

### Data and reuse contract

`ScenarioSet.scenarios` is a full pandas DataFrame with columns:

| Column | Meaning |
|---|---|
| `scenario_id` | Stable `UST_YYYYMMDD_YYYYMMDD` actual-endpoint identity |
| `start_date`, `end_date` | Actual common historical endpoints |
| `target_end_date` | Intended end-date anchor |
| `target_start_date`, `shortfall_days` | Appended audit fields: intended start and combined endpoint shortfall |
| `elapsed_days` | Actual endpoint difference in calendar days |
| `DGS2_change_bp`, `DGS10_change_bp`, `DGS30_change_bp` | Complete same-interval numerical changes |

`ScenarioSet.metadata` holds schema/type, factor identity, input/output units,
condition and inclusive bounds, horizon, end-anchor/target/endpoint rules,
latest anchor, seven-day maximum shortfall, requested/effective reference dates,
missing-data rule, per-ID source/retrieval provenance, overlap/interpretation and
quantile convention. Counts distinguish reference rows, complete dates, excluded
incomplete rows, intended windows, insufficient-observation exclusions,
shortfall exclusions, eligible windows and selected rows. The obsolete
start-anchor and unmatched-month metadata fields are intentionally replaced.
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

### Initial implementation evidence (before correction)

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

**Before-correction cached-data integration (`c973def`):** existing DGS snapshots dated 2026-10-28
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

Those initial counts and tests describe the former construction only. Current
verification, corrected statistics and limitations follow below. Original evidence
files remain unchanged as inspectable before-correction records.

Evidence: [stage3.json](../artifacts/work_runs/261030_1309_analysis1/stage3.json).
Stage 2 publication: commit `2a06247`, [PR #52](https://github.com/lbk209/bondview-v3/pull/52),
merged as `b57ddaf`; remote/local task branches deleted and verified by Git.

## Historical-window correction — PASS

Continued PR #54 in the same session branch after fetching/pruning remote refs
and verifying its open state and head `c973def553e6b89c3adbe56bba10e75c1f70e4ba`.
The checkout was clean. Task branch: `codex/task/261030_1400_window_correction`.
This is a targeted correction to window construction, not a new Analysis 1C.
The original main baseline remains recorded above; correction implementation
is based on the verified session revision, not restarted from main.

The revised algorithm is specified under Construction above. `ScenarioSet`,
`TreasuryMarketAnalysis.scenarios()` and `build_conditional_scenarios()` public
signatures are unchanged, as are actual-date ID formatting, actual dates,
elapsed days, joint bp columns, quantiles and scatter mappings. Existing columns
keep their order; `target_start_date` and `shortfall_days` are appended, including
for empty results. Rows now follow reverse intended-end order. Construction and
rejection metadata intentionally change to match the new rules. Labels,
notebook explanation, usage documentation and test-purpose documentation are
updated. Facade, 1A/1B, plotting/presentation Python and FRED code are unchanged.
No architecture/workflow document was modified, and no dependencies were added.

### Verification

- **17 focused scenario tests PASS**: hand-specified monthly end sequences,
  inclusive actual endpoints, no outside searching, missing boundary and interior
  observations, insufficient slices, seven-day acceptance/eight-day rejection
  for monthly and daily sampling, month-end/leap-year arithmetic without drift,
  conditioning, IDs, schema, summaries and independent result consumption.
- **65 full regression tests PASS**, including a fresh notebook kernel executing
  C with only Treasury setup, no A/B/KW. Another notebook run checks A/B reruns,
  empty scenario output and unchanged snapshot files. Tests are deterministic
  synthetic fixtures and do not assert obsolete historical counts.
- Modified Python files compile with `poetry run python -m py_compile`;
  `git diff --check` passes. No unresolved introduced, pre-existing or
  environmental failure was encountered in the correction verification.
- Cached integration re-executed both the old implementation from `c973def` and
  corrected implementation on the same existing snapshots. SHA-256 hashes match
  the prior evidence. Every **eligible** corrected vector (not only selected
  ones) was checked against independent boolean date filtering, actual first/last
  endpoints, bp subtraction, nominal/actual days, shortfall and horizon. The
  conditional result exactly matches inclusive filtering of the eligible set.
- Complete affected calculation and tests were reviewed directly by Codex;
  no independent reviewer or subagent is claimed.

### Observed cached-history changes

Configuration is unchanged: 10Y condition [-25, +25] bp, six calendar months,
complete reference coverage 1977-02-15 through 2026-10-26. Counts reflect the
explicitly changed method:

| Sampling | Before: selected / eligible | Corrected: selected / eligible |
|---|---|---|
| monthly | 153 / 590 | 162 / 591 |
| daily | 3,230 / 12,142 | 3,282 / 12,295 |

Descriptive statistics in bp, shown as **before → corrected**. Each statistic
is marginal; no row of quantiles is converted into a historical joint vector.

| Sampling / tenor | Minimum | P10 | Median | P90 | Maximum |
|---|---|---|---|---|---|
| monthly / DGS2 | -226 → -155 | -58.8 → -51.9 | 2 → -0.5 | 53.8 → 53.6 | 118 → 117 |
| monthly / DGS10 | -25 → -25 | -19.8 → -21 | -1 → -4 | 21 → 19 | 25 → 24 |
| monthly / DGS30 | -52 → -49 | -27.4 → -28.8 | 0 → -4 | 27.8 → 25.9 | 70 → 56 |
| daily / DGS2 | -226 → -259 | -59 → -59 | 1 → 1 | 61.1 → 60 | 135 → 135 |
| daily / DGS10 | -25 → -25 | -21 → -21 | -2 → -2 | 20 → 20 | 25 → 25 |
| daily / DGS30 | -67 → -76 | -31 → -31 | -2 → -2 | 26 → 26 | 93 → 93 |

The latest three eligible monthly windows demonstrate the intended/actual
boundaries below. They are **eligible-window examples**, not members of the
[-25, +25] bp conditional set: their 10Y changes are +65, +75 and +64 bp.

| Intended start | Intended end | Actual start | Actual end | Elapsed days | Shortfall days |
|---|---|---|---|---|---|
| 2026-04-26 | 2026-10-26 | 2026-04-27 | 2026-10-26 | 182 | 1 |
| 2026-03-26 | 2026-09-26 | 2026-03-26 | 2026-09-25 | 183 | 1 |
| 2026-02-26 | 2026-08-26 | 2026-02-26 | 2026-08-26 | 181 | 0 |

Full numerical comparison, rejection counts, copied provenance, snapshot hashes,
latest eligible and latest condition-selected examples are in
[window_correction_1400.json](../artifacts/work_runs/261030_1309_analysis1/window_correction_1400.json).
The original `cached_history_check.json` and `stage3.json` remain historical
records of the earlier construction; they are not the current expected results.

### Remaining limitations

Windows overlap, so counts and quantiles remain descriptive, not independent
frequencies or forecast probabilities. Up to seven days of actual shortening
is allowed; no yield/horizon normalization is performed. Incomplete or sparse
history can exclude windows, while interior gaps alone do not invalidate them.
Reference end changes deliberately change the monthly original anchor and can
change the selected sample. Snapshots are retrieval-time data, not reconstructed
historical availability/vintages. No returns or risk calculations are included.

## Publication and completion

| Stage | Status | Implementation/test commit | Task PR |
|---|---|---|---|
| Baseline alignment | PASS | `8732c29` | [#51](https://github.com/lbk209/bondview-v3/pull/51), merged into session |
| Facade/results | PASS | `2a06247` | [#52](https://github.com/lbk209/bondview-v3/pull/52), merged into session |
| Conditional scenarios | PASS | `d876a80` | [#53](https://github.com/lbk209/bondview-v3/pull/53), verified and published into session review workflow |

All three output contracts and the targeted correction are satisfied. Source baseline remains fixed at
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

| Metric | Stage 1 | Stage 2 | Stage 3 | Correction | Assignment total |
|---|---|---|---|---|---|
| Input tokens | Not available | Not available | Not available | Not available | Not available |
| Output tokens | Not available | Not available | Not available | Not available | Not available |
| Cached-input tokens | Not available | Not available | Not available | Not available | Not available |
| Reasoning-output tokens | Not available | Not available | Not available | Not available | Not available |
| Total tokens | Not available | Not available | Not available | Not available | Not available |
| Attributable stage tokens / share | Not available | Not available | Not available | Not available | Not available |
| Active context used / capacity / percent | Not available | Not available | Not available | Not available | Not available |

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

Correction beginning reporting checkpoint: 2026-10-30 14:00:41 Asia/Seoul
(05:00:41 UTC). Correction input/output/cached-input/reasoning-output/total token
counts, attributable consumption, stage percentage, context used/capacity/percent
and five-hour/weekly/other allowance percentages: **Not available**. The exposed
tool inventory again supplies no applicable reliable usage counters; no counter
differences or account allowance measurements can be derived. Original stage
usage remains unavailable. Correction end checkpoint is recorded in its evidence.

Correction end reporting checkpoint: 2026-10-30 14:07:04 Asia/Seoul
(05:07:04 UTC). Token/context figures and beginning/end account allowance
percentages remain **Not available**; these checkpoints record availability
checks, not successful measurements.
