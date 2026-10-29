# Analysis 1.B — Expected short rates and term premiums

Implemented the agreed Kim–Wright decomposition in the existing Treasury-market notebook. The focused verification passes, including offline notebook execution with synthetic fixtures and the existing saved FRED snapshots. Native hover configuration and data are checked; the actual hover interaction awaits user inspection.

## Scope and file responsibilities

| File | Responsibility |
| --- | --- |
| `src/bondview/analysis/treasury_curve.py` | `analyze_kw_decomposition`: validate daily Percent inputs, align four complete KW series, select observations, derive levels and full cumulative-change paths. |
| `src/bondview/plotting/treasury_curve.py` | `plot_kw_decomposition`: one five-trace Plotly figure per maturity, two y domains and one underlying x-axis. |
| `src/bondview/config/labels.yaml` | Independent `kw_decomposition` section for figure titles, axes, trace labels and hover templates. |
| `notebooks/analysis1_treasury_market.ipynb` | Two new B cells: offline snapshot loading and calculation/display using the existing date picker. |
| `tests/test_kw_decomposition.py` | Five focused tests of pairing, arithmetic, missing-data alignment, effective endpoints, full paths, errors, figure structure, hover data and configurable labels. |
| `tests/test_treasury_curve.py` | Update the existing fixture and metadata lookup to the current flat per-series contract, restoring Analysis 1.A regression coverage. Financial expectations remain unchanged. |
| `tests/test_notebook.py` | Exercise A and B offline, preserve explicit acquisition cells, and verify independent reruns using current picker values. |
| `artifacts/work_runs/261029_analysis1b_1220/` | Baseline evidence, focused/full-suite results, saved-snapshot execution evidence and its reproducible verification script. |

No changes to the FRED manager, CSV contracts, architecture, examples, presentation functions, widgets, utilities, Analysis 1.A function bodies or Analysis 1.C placeholders. No dependencies were added. Every pre-existing notebook cell, including its outputs, is unchanged.

## Calculations and presentation

The pairs are `THREEFY2` / `THREEFYTP2` and `THREEFY10` / `THREEFYTP10`. Only dates where all four are nonmissing qualify. The shared date utility selects the inclusive interval; the retained first and last observations are the effective endpoints. No interpolation, filling or replacement occurs. An interval without complete KW observations raises `ValueError` with a clear message.

Each maturity returns a dated DataFrame containing `fitted_yield`, `expected_rate`, `term_premium`, `expected_change_bp`, `premium_change_bp` and `fitted_change_bp`. Expected rates are fitted yield minus premium. Changes are differences from the first eligible observation multiplied by 100, retained at every eligible date. The fitted-yield change is the sum of component changes for hover use. Original levels remain in percent. These are model-fitted nominal zero-coupon quantities, not forecasts of future DGS yields.

Each figure has the specified overall title, three upper-panel level lines and two lower-panel change lines. The y domains allocate 70% and 30% of usable panel height, with a gap. All traces explicitly reference `x`; upper traces reference `y`, lower traces `y2`. The sole date axis is anchored at the bottom and spans the effective endpoints. The configuration uses `hovermode="x"`, `hoversubplots="axis"`, and native vertical spike lines. Upper hover labels contain each of the three levels in percent. Lower hover labels contain both component changes in bp, with the total displayed once through the expected-change trace's custom data. No total line, panel titles, endpoint annotations, shaded areas or custom synchronization are present.

## Verified evidence

- [Focused checks](../artifacts/work_runs/261029_analysis1b_1220/focused_tests.log): **20 tests passed**: 5 KW, 13 Analysis 1.A and 2 notebook tests. The notebook test executes calculations and figure display with synthetic saved snapshots, blocks FRED download/transport and credential access, checks changed picker dates, and verifies that snapshot files remain unchanged.
- Hand-checkable synthetic 2Y expected levels are `[4.2, 4.5, 4.1, 4.25]%`; their changes are `[0, 30, -10, 5] bp`. Term-premium changes are `[0, 10, -10, 5] bp`, and hover totals are `[0, 40, -20, 10] bp`. The intermediate reversal is preserved. Independent 10Y expected changes are `[0, -10, 0, -10] bp`.
- [Actual saved-snapshot notebook execution](../artifacts/work_runs/261029_analysis1b_1220/saved_notebook.json): 11 code cells executed in a copy with the acquisition section skipped and FRED download/transport/credential access blocked. Both figures were created, each with 5 traces and **9,189 complete observation dates**, from **1990-01-02 through 2026-10-23**, within the picker's existing 1962-01-02 to 2026-10-26 selection. All four KW snapshots were dated 20261028. No snapshot or source notebook was rewritten.
- [Analysis 1.A baseline](../artifacts/work_runs/261029_analysis1b_1220/analysis1a_baseline.json): the saved-snapshot result, attributes and serialized figure hash for 2024-09-15 through 2025-01-13 matched the pre-edit output exactly. The verification also compares every pre-existing notebook cell against baseline `75df5635f03875b054ac10d4b74fd42b0a555743`.
- `poetry run python -m py_compile` passed for both modified source Python files, all three affected test files, and the saved-notebook verification script. `git diff --check` passed.
- Complete affected analysis and plotting functions, notebook B cells and test units were reviewed after implementation for duplicate processing, redundant calculations, excess abstractions and consistency with the existing code. Analysis 1.A was not refactored.

Reproduce the focused checks with:

```bash
poetry run python -m unittest discover -s tests -p 'test_kw_decomposition.py' -v
poetry run python -m unittest discover -s tests -p 'test_treasury_curve.py' -v
poetry run python -m unittest discover -s tests -p 'test_notebook.py' -v
poetry run python artifacts/work_runs/261029_analysis1b_1220/verify_saved_notebook.py
```

The last command requires the existing local snapshots; those ignored market-data files are not committed. Jupyter execution required permission for local kernel sockets in this environment and succeeded after that permission was granted. Interactive browser-based hover testing was intentionally not performed.

## Limitations and repository workflow

The full test suite is not green. Before implementation, 39 tests produced 2 failure entries and 50 error entries, including subtest errors; see [baseline results](../artifacts/work_runs/261029_analysis1b_1220/baseline_tests.json). After implementation and the affected fixture/test updates, 44 tests produced 3 failure entries and 14 error entries, all in `test_fred.py`; see [final full-suite results](../artifacts/work_runs/261029_analysis1b_1220/full_tests.json). Every remaining failing test method was already failing or erroring before implementation. Updating the shared Treasury fixture allows some legacy FRED tests to reach later assertions, changing individual error reasons. Those tests still assume older metadata, multi-ID CSV or reporting behavior, and one asserts the old date-row behavior. No claim is made that the full suite passes, and the FRED implementation was left unchanged as requested.

No implementation blocker remains for Analysis 1.B. The actual cross-panel hover and guide behavior awaits user inspection. Successful arithmetic and figure creation do not constitute financial-design acceptance.

Work started from a clean `main` at `75df5635f03875b054ac10d4b74fd42b0a555743`, after fetching/pruning and verifying live remote branches. Session: `codex/session/261029_1220`; task: `codex/task/261029_1220_analysis1b`. The standing workflow authorizes task-to-session integration; the final session-to-main PR must remain unmerged. An initial incorrectly named remote session reference, `codex/session/261029_1b`, remains at the unchanged baseline because session-branch deletion is reserved to the user. It contains no implementation changes.
