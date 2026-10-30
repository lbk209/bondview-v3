# Treasury market notebook

Use the Poetry Python kernel with `analysis1_treasury_market.ipynb`.
The older `analysis1_curve.ipynb` is a historical notebook, not the current API.

The optional Download section retrieves observations in memory; `fred.save()`
explicitly persists them. Skip that section when snapshots already exist.
`FredDataManager` loads the latest `ID_YYYYMMDD.csv` per requested ID offline,
with flat per-ID provenance and original units/frequency. Retrieval dates are
UTC snapshot dates, not historical availability dates. No synthetic fallback,
interpolation or missing-yield filling is performed. Save trims external missing
padding, preserves internal gaps, and refuses to overwrite existing snapshots.

## Analyses 1A and 1B

Import the `market` module directly. Each analysis receives its own observations;
there is no `TreasuryMarketAnalysis` instance or shared observations state.

```python
from bondview import market

# 1A: inspect history, then select analysis dates.
curve_analysis = market.curve(observations)
curve_analysis.show_history()
curve_analysis.analyze(start, end, yield_change_tolerance_bp=5,
                       slope_tolerance_bp=5, formatted=True)

# The underlying numerical DataFrame is retained without recalculation.
numerical_curve = curve_analysis.result

# Or obtain numerical data without the formatted display.
numerical_curve = curve_analysis.analyze(start, end, formatted=False)

# 1B: keep date selection at calculation time; cumulative changes start
# at the first eligible observation within the selected interval.
yield_decomposition = market.decomposition(kw_observations, start, end)
yield_decomposition.show(width=1300, height=600)
numerical_paths = yield_decomposition.paths
```

Date widgets supply explicit selections on each rerun. In 1A, `show_history()`
initially plots the available history; optional start/end arguments restrict
that plot. `analyze()` calculates the selected date interval and stores the
numerical DataFrame in `curve_analysis.result`. With `formatted=True` (default),
it displays the existing formatted movement table and interpretation; with
`formatted=False`, it returns the numerical DataFrame without displaying it.
A later successful call replaces the stored result; a failed calculation does
not replace it. 1A does not require an additional `CurveResult` wrapper.
1B keeps its existing `DecompositionResult`, selected-interval calculation and
`.show()` presentation; it does not depend on 1A.

Direct functions remain available: `analyze_curve`, `analyze_kw_decomposition`,
`plot_yield_history`, `show_yield_history`, `plot_kw_comparison`,
`show_kw_decomposition`, `display_table`, `interpret_curve`, `show_curve_results`.
Curve levels are percent, spread levels and changes are bp. KW fitted yields,
expected-rate components and premiums are model estimates; changes are bp.
Configurable presentation labels remain in `src/bondview/config/labels.yaml`.

Run `poetry run python -m unittest discover -s tests -v`; see
[`tests/README.md`](../tests/README.md) for coverage. Existing tests may require
API migration because the old facade and `CurveResult` were deliberately removed.
Fresh Jupyter kernels require local socket access.

## Analysis 1C — conditional historical scenarios

After the shared Treasury load/setup, C runs independently of A and B. It needs
only DGS2/DGS10/DGS30 daily Percent observations and their per-ID metadata.

```python
yield_scenarios = market.scenarios(
    observations,
    condition_tenor="DGS10", lower_bp=-25, upper_bp=25,
    horizon_months=6, sampling_step_observations=1,
    reference_start=None, reference_end=None,
)
joint_scenarios = yield_scenarios.scenarios
metadata = yield_scenarios.metadata
statistics_bp = yield_scenarios.summary()
yield_scenarios.show_summary()
yield_scenarios.show_plot()
```

For independent numerical use, import
`ScenarioSet, build_conditional_scenarios` from `bondview.analysis.scenarios`.
`build_conditional_scenarios(observations, ...)` takes the same configuration
and returns the same `ScenarioSet` without the facade or visualization imports.
Future analyses can iterate each row's `scenario_id`, `start_date`, `end_date`,
`elapsed_days`, `DGS2_change_bp`, `DGS10_change_bp`, `DGS30_change_bp`, keeping
whole vectors paired across compared exposures. Metadata retains conditions,
units, source/retrieval provenance, counts, coverage and construction rules.
This assignment does not calculate returns or risk.

Candidate endpoints are complete Treasury observation dates whose calendar-month
horizon fits within the selected reference history. Sort them oldest to newest,
then select positions 1, 1 + step, 1 + 2 × step, etc., before conditioning.
`sampling_step_observations=1` is the default in both public entry points.
Step 5 counts five complete observations, approximately a trading week; step 20
is approximately a trading month. Neither means a fixed number of calendar days.
The former `sampling` parameter is removed, with no compatibility alias.

The chronological anchor is the earliest candidate supporting the horizon.
Appending later complete observations preserves previously sampled endpoints
and vectors if earlier history is unchanged. Changing the starting reference
history or horizon can change the candidate sequence and sampling alignment.
Results retain reverse chronological endpoint order for presentation.

Subtract `horizon_months` calendar months from each sampled end, clipping at
month end. Use the first/last complete observations inside the inclusive slice
`common.loc[target_start:target_end]`. Skip fewer than two observations or a
combined shortfall over seven days: `(target_end - target_start).days -
(end_date - start_date).days > 7`. No outside searching, filling, interpolation,
resampling or horizon normalization occurs. Interior gaps alone do not invalidate
a window. One-, three- and six-month horizons are independent of observation step.

Reference bounds remain inclusive and default to complete common coverage.
Metadata records the positive integer step, earliest-candidate anchor/convention,
candidate and sampled endpoint counts, intended windows, eligibility exclusions,
selected scenarios and provenance. `target_start_date`, `target_end_date`,
`shortfall_days`, actual dates and elapsed days retain their meanings. Actual-date
IDs, rounding and inclusive DGS2/DGS10 conditioning are unchanged.

The primary result is the complete `ScenarioSet`; minimum/P10/median/P90/maximum
are secondary marginal descriptive summaries using linear quantiles. The scatter
shows Δ2Y vs Δ30Y colored by Δ10Y, or Δ10Y vs Δ30Y colored by Δ2Y. Hover retains
actual historical dates and elapsed days. Overlapping observations are dependent;
counts and quantiles are not independent-event frequencies or forecasts. Empty
selections retain a usable typed schema, NaN summaries and an empty chart.
No complete reference observations instead raises a clear input error.
