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

```python
from bondview import TreasuryMarketAnalysis
market = TreasuryMarketAnalysis(observations)
market.show_history(start, end)
curve = market.curve(start, end, yield_change_tolerance_bp=5, slope_tolerance_bp=5)
curve.show()
numerical_curve = curve.data

decomposition = market.decomposition(kw_observations, start, end)
decomposition.show(width=1300, height=600)
numerical_paths = decomposition.paths
```

Date widgets supply explicit selections on each rerun. Results keep their own
calculated outputs; changing widgets or source data does not change previous
results. Display calls never recalculate financial results. No current-result
or selection state is stored by the facade. 1B takes explicit KW observations
and does not require a 1A computation. Its chart retains the baseline combined
2Y/10Y layout and hover behavior.

Direct functions remain available: `analyze_curve`, `analyze_kw_decomposition`,
`plot_yield_history`, `show_yield_history`, `plot_kw_comparison`,
`show_kw_decomposition`, `display_table`, `interpret_curve`, `show_curve_results`.
Curve levels are percent, spread levels and changes are bp. KW fitted yields,
expected-rate components and premiums are model estimates; changes are bp.
Configurable presentation labels remain in `src/bondview/config/labels.yaml`.

Run `poetry run python -m unittest discover -s tests -v`; see
[`tests/README.md`](../tests/README.md) for coverage. Tests use deterministic
synthetic inputs and block normal notebook network/credential access.
Fresh Jupyter kernels require local socket access.
