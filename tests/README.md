# Test purposes

Run `poetry run python -m unittest discover -s tests -v` in the Poetry environment.
Notebook tests require local sockets for fresh Jupyter kernels. All transport is
mocked or blocked; synthetic fixtures are not presented as market observations.

- `test_fred.py`: Per-ID CSV v2 precision, missing values, flat per-ID provenance,
  mixed source units/frequencies, explicit acquisition/persistence, immutable
  snapshots, atomic batch publication, latest selection, reporting, and credential
  handling. Save trims external missing padding; internal gaps remain.
- `test_treasury_curve.py`: Analysis 1A signs, percent/bp units, classifications,
  independent tolerances, inclusive effective endpoints, partial data, and
  configurable presentation separate from numerical calculations.
- `test_kw_decomposition.py`: Analysis 1B model pairing, subtraction, bp changes,
  complete common dates, reversing paths, and current combined 2Y/10Y Plotly
  presentation, including shared hover axes and configurable labels.
- `test_notebook.py`: Current Treasury notebook syntax, explicit acquisition,
  offline execution, widget reruns, missing endpoints, and A/B independence.
- `test_market.py`: Facade/direct-function numerical and chart equivalence,
  stored result independence, display without financial recomputation, explicit
  selections, and decomposition without running 1A.
- `test_scenarios.py`: Analysis 1C default integer observation steps, oldest
  candidate anchoring, positional steps 1/5/20, stability under appended history,
  sampling before conditioning/eligibility, independent 1/3/6-month horizons,
  step validation, and preserved complete joint vectors. Hand-checked former
  daily vectors verify step-1 numerical/order compatibility. Coverage also
  retains inclusive in-window endpoints, missing boundaries/interior dates,
  seven-day shortfall acceptance, insufficient windows, dates/IDs/provenance,
  empty schemas, marginal quantiles and unchanged scatter/display behavior.

The notebook module also executes 1C in a fresh kernel using only Treasury
setup, without A, B or KW snapshots, including both conditioning tenors.
