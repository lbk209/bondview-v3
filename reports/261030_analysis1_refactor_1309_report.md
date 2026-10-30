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

## Stage 3 — PASS (with subsequent window and observation-step updates below)

Implemented `build_conditional_scenarios()` and independent `ScenarioSet` in
`bondview.analysis.scenarios`. Added `market.scenarios(...)`, `summary()`,
`show_summary()` and `show_plot()`. Separate presentation and plotting modules
use stored joint vectors. Top-level facade exports are lazy so independent
numerical imports do not load the facade, 1A/1B code or visualization modules.
No common result superclass, forecasting methods, Analysis 2 returns or
Analysis 3 risk calculations were added. No new dependencies were needed.

### Construction and assumptions

The current API uses `sampling_step_observations=1` in both public entry
points. The former `sampling` argument and modes are removed without aliases.
The horizon remains measured in calendar months. The current method is:

1. Validate daily Percent Treasury inputs and retain dates complete for DGS2,
   DGS10 and DGS30 within inclusive reference bounds. Defaults are the first/last
   complete common dates. Never fill, interpolate, resample or average yields.
2. Candidate ends are complete dates satisfying
   `end - DateOffset(months=horizon_months) >= first_common_date`, in ascending
   chronological order. The first candidate anchors sampling.
3. Select every Nth candidate from that oldest candidate, before conditioning or
   window eligibility exclusions. N is the positive integer observation step;
   it counts complete observation dates, not calendar days. Appending later
   observations preserves prior selections if earlier history is unchanged.
4. For each sampled end, intended start = end minus the calendar-month horizon,
   with month-end clipping. Slice `common.loc[target_start:target_end]`
   inclusively; skip fewer than two complete observations and use the first/last
   actual dates. Never search outside the window. Interior gaps are acceptable.
5. Combined shortfall = intended elapsed days minus actual elapsed days. Accept
   seven days or less; reject greater shortfalls without horizon normalization.
6. Subtract those same actual start/end yields for all three tenors, multiply
   percent-point differences by 100 and round floating cancellation to 10 bp
   decimals, as before. Keep actual-date IDs and all existing result columns.
7. Apply unchanged inclusive DGS2/DGS10 bounds to complete joint vectors. Return
   newest intended endpoints first for compatibility with result presentation.

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
earliest-candidate anchor and positive integer step, seven-day maximum shortfall, requested/effective reference dates,
missing-data rule, per-ID source/retrieval provenance, overlap/interpretation and
quantile convention. Counts distinguish reference rows, complete dates, excluded
incomplete rows, candidate/sample endpoint counts, intended windows,
insufficient-observation exclusions, shortfall exclusions, eligible windows and
selected rows. The obsolete
start-anchor and unmatched-month metadata fields are intentionally replaced.
Provenance is copied defensively from input; no point-in-time data is invented.
IDs deliberately stay stable across filters/sampling/source revisions for the
same interval; use accompanying provenance to distinguish retrieval snapshots.

Independent downstream use needs no facade or plotting:

```python
from bondview.analysis.scenarios import build_conditional_scenarios
scenario_set = build_conditional_scenarios(
    observations, condition_tenor="DGS10", lower_bp=-25, upper_bp=25,
    horizon_months=6, sampling_step_observations=1,
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
The initial implementation cleared outputs. The user's subsequent notebook
review commit `1cf74c8` retains A/B display outputs; those cells and outputs are
preserved. Only affected C outputs are cleared for the new sampling default.

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

## Historical-window correction — PASS (PR #55 checkpoint)

Continued PR #54 in the same session branch after fetching/pruning remote refs
and verifying its open state and head `c973def553e6b89c3adbe56bba10e75c1f70e4ba`.
The checkout was clean. Task branch: `codex/task/261030_1400_window_correction`.
This is a targeted correction to window construction, not a new Analysis 1C.
The original main baseline remains recorded above; correction implementation
is based on the verified session revision, not restarted from main.

At this checkpoint, monthly ends moved backward from the latest complete date
and daily ends used all complete dates, newest first. Both used inclusive slices
and the seven-day shortfall rule. The observation-step update below replaces
those sampling schedules while retaining the window logic. `ScenarioSet`,
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
At this checkpoint, reference end changes altered the monthly original anchor.
The observation-step update below removes that latest-date sampling dependency. Snapshots are retrieval-time data, not reconstructed
historical availability/vintages. No returns or risk calculations are included.

## Numerical observation-step sampling — PASS

Continued the clean current PR #54 session at
`1cf74c85e95dcd7fb2284ff799bd237aa3b42a7d`, verified against live remote refs.
That revision includes the user's committed notebook review. Task branch:
`codex/task/261030_1626_observation_steps`.

Both public entry points now default to `sampling_step_observations=1` and no
longer accept the old `sampling` argument. Positive integers, including NumPy
integer scalars, are accepted; zero/negative, fractional/integral floats,
booleans, strings, missing/nonfinite values and invalid containers are rejected
with a clear message. No aliases or additional sampling settings were added.

The chronological rule is described under Construction above. Positional
selection uses `take(range(0, count, step))`, equivalent to `[::step]`, avoiding
pandas frequency-multiplication overflow for very large valid integer steps.
Candidate count and sampled count are recorded before window rejection and
conditioning. An empty candidate sequence has a null sampling anchor and the
unchanged typed empty result schema.

### Files and necessary presentation compatibility change

| Files | Direct purpose |
|---|---|
| `src/bondview/analysis/scenarios.py`, `src/bondview/market.py` | New API, positive-integer validation, chronological positional sampling, metadata |
| `src/bondview/presentation/scenarios.py` | One formatter argument changed to the new metadata key |
| `src/bondview/config/labels.yaml` | Summary wording and observation-step explanation |
| `tests/test_scenarios.py`, `tests/test_notebook.py`, `tests/README.md` | Sampling/window verification and current notebook expectations |
| `notebooks/analysis1_treasury_market.ipynb`, `notebooks/README.md` | New parameter/default and usage guidance; C outputs cleared |
| This report and `observation_steps_1626.json` | Durable verification/publication evidence |

**Documented scope exception:** the old summary presenter accessed
`info["sampling"]` directly. Removing that metadata key makes `show_summary()`
fail unless the formatter reads `info["sampling_step_observations"]`. Only that
argument is changed; formatting, summary calculations and scatter Python remain
unchanged. No compatibility metadata alias is introduced.

The notebook's reviewed A/B cells and outputs, shared setup and non-C code are
preserved. C retains the user's DataFrame display and direct `show_summary()`
style. Tests now inspect `scenarios.summary()` rather than require the removed
notebook variable `scenario_summary`; the output/shape checks remain. No
unrelated tests, financial calculations, FRED modules, architecture/workflow
files or dependencies changed. Existing IDs, dates, elapsed/shortfall fields,
all columns/order, bounds, rounding, source provenance and result methods remain.

### Verification

- **21 focused scenario tests PASS**. They verify both defaults, no old parameter,
  complete step-1 endpoints, hand-checked previous daily vectors/order, positions
  1/6/11/... for step 5, the same rule for step 20, gaps counted as observations,
  append stability, sampling before conditioning/eligibility, independent 1/3/6
  month horizons, leap/month ends, invalid steps, unchanged inclusive slices and
  shortfall, schemas, units, ID/provenance, summaries and plot mappings.
- **3 focused notebook tests PASS**, including a fresh C-only kernel with no
  A/B/KW execution and rerun with step 5. Full notebook fixture execution checks
  missing Treasury endpoints and empty scenarios without changing cache files.
- **69 full regression tests PASS**. Modified Python modules/tests compile;
  `git diff --check` passes. No unresolved relevant failures or blockers remain.
- The new test for extremely large positive integer steps exposed a pandas
  frequency overflow in direct slicing. Positional `take` fixed it without
  restricting the accepted positive integer domain; focused/full suites passed
  afterward. No financial behavior was changed to satisfy tests.

### Exact equivalence and cached-history examples

Both the previous implementation loaded from `1cf74c8` with its daily mode and
the new default were executed against the same synthetic fixture and unchanged
Treasury snapshots. **Exact DataFrame equality** verifies every result column,
ID, actual/intended date, yield change, elapsed/shortfall value and row order.
Marginal summary equality, source provenance and reference metadata also pass.
Snapshot SHA-256 hashes match the PR #55 evidence. For six-month 10Y changes
in [-25, +25] bp, step 1 reproduces **3,282 / 12,295** exactly.

| Observation step | Candidate endpoints | Sampled endpoints / eligible windows | Condition-selected scenarios |
|---|---|---|---|
| 1 | 12,295 | 12,295 | 3,282 |
| 5 | 12,295 | 2,459 | 649 |
| 20 | 12,295 | 615 | 161 |

All cached sampled windows meet the endpoint safeguard. For each step, the
conditional output was verified as the exact step-1 subset at that step's
candidate positions, not as every Nth qualifying scenario. The anchor is the
first complete endpoint supporting the horizon; full metadata, first sampled
candidate dates, summaries and representative selected rows are retained in
[observation_steps_1626.json](../artifacts/work_runs/261030_1309_analysis1/observation_steps_1626.json).
Earlier evidence files remain unchanged as historical checkpoints.

Observation steps are approximate trading-week/month spacings, not calendar
intervals or independence adjustments. Earlier reference-history revisions,
start-bound changes or changed horizons can change alignment; appending later
unchanged-prefix history cannot. Counts/quantiles remain descriptive, and the
seven-day shortening allowance is unchanged. There are no unresolved deviations
beyond the documented necessary summary formatter argument change.

## Publication and completion

| Stage | Status | Implementation/test commit | Task PR |
|---|---|---|---|
| Baseline alignment | PASS | `8732c29` | [#51](https://github.com/lbk209/bondview-v3/pull/51), merged into session |
| Facade/results | PASS | `2a06247` | [#52](https://github.com/lbk209/bondview-v3/pull/52), merged into session |
| Conditional scenarios | PASS | `d876a80` | [#53](https://github.com/lbk209/bondview-v3/pull/53), verified and published into session review workflow |
| Window correction | PASS | `a0356c7` | [#55](https://github.com/lbk209/bondview-v3/pull/55), published into the same session |

All three output contracts, the window correction and the observation-step update are satisfied. Source baseline remains fixed at
`ee79747b25ad0f45dffa7c040823560415159890`. The final session-to-main [PR #54](https://github.com/lbk209/bondview-v3/pull/54)
is open for user review and must remain unmerged. Its description and the final
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

Observation-step assignment usage checkpoint: 2026-10-30 16:26:39–16:33:47
Asia/Seoul (07:26:39–07:33:47 UTC). No reliable input/output/cached/reasoning/total
or per-stage token counts, context occupancy/capacity or account allowance
counters are exposed. These statistics and attribution percentages are
**Not available**; no estimates or token-to-allowance inference were made.
