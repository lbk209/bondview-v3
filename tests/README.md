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
- `test_scenarios.py`: Analysis 1C inclusive conditioning, complete same-interval
  percent-to-bp vectors, calendar-month/leap-year endpoints, monthly/daily
  sampling, missing-month exclusions, actual elapsed days, reference bounds,
  stable IDs, provenance, empty/singleton sets, hand-calculated quantiles, both
  scatter mappings, calculation-free display, and use without plotting imports.
  An independent endpoint-enumeration oracle checks the selected vectors.

The notebook module also executes 1C in a fresh kernel using only Treasury
setup, without A, B or KW snapshots, including both conditioning tenors.
