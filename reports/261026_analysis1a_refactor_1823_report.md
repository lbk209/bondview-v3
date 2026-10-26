# Analysis 1.A refactor — verification report

Result: **PASS with validation limitations**. This standalone Codex assignment
refactors PR #36 without changing its financial behavior. It introduces
self-contained FRED CSV storage, a small stateful data manager, manual
DatePicker-to-output notebook steps, and terminology separate from calculations.
No additional analyses, financial rules, or design-document changes are included.

## Authority and protected work

- Baseline: PR [#36](https://github.com/lbk209/bondview-v3/pull/36), open from
  `codex/session/261026_1000` into `main`, at
  `98bf94087ab52ec6ada23dd5cbec031155dcd22d` when inspected.
- Read the user-pasted assignment, `AGENTS.md`, applicable standing contracts,
  the specifically authorized architecture/examples documents, the notebook,
  and relevant modules/tests. The assignment expressly makes this standalone;
  no Bernie/Carrie/Dennis agents, delegated review, or authorization gate applies.
- Initial checkout had uncommitted edits to `notebooks/analysis1_curve.ipynb`,
  `pyproject.toml`, and an untracked alternate notebook. All were preserved.
  Implementation used `/tmp/bondview-analysis1a-refactor`, cloned from the local
  Git history, with origin reset to the real GitHub repository and fetched/pruned.
- Remote session and main heads were verified before editing. Work uses task
  branch `codex/task/261026_1823_analysis1a_refactor` into the existing session.
  PR #36 is the existing final review PR; no duplicate final PR or main merge
  is authorized. Publication/merge/cleanup status is recorded in GitHub.
- `docs/`, `workflow/`, prior reports, and prior run evidence remain unchanged.
  No dependencies or lockfile changes were necessary; `anywidget` was absent.

## Implementation and intentional interface changes

[`FredDataManager`](../src/bondview/data/fred.py) owns snapshot path,
observations, and a defensive independent metadata copy. It provides download,
load, save, validation, explicit mode dispatch, and reporting. Existing standalone
transport/load/save functions remain available. File mode never contacts FRED
or reads credentials. Explicit key → environment → `.env` precedence and the
known-Treasury public-CSV fallback remain unchanged. API series retain source
units/frequency and request untransformed observations without resampling.
Analysis 1.A separately enforces daily Percent Treasury inputs.

CSV comment headers store the format, source, timezone-aware retrieval timestamp,
per-series units/frequency and available source attributes. Each header value is
JSON-encoded to retain nested metadata and escaping; observations themselves are
ordinary CSV rows. No metadata sidecar exists. Empty numeric fields are missing;
round-trip float parsing preserves source numbers. Dates and rows are validated,
without filling, interpolation, inferred units, or endpoint substitution. Invalid
metadata is encoded/validated before opening an existing file for writing.

The old JSON cache format is intentionally rejected. Users may download once
into the new `.csv` path or explicitly convert a valid historical snapshot while
retaining its provenance. The notebook README documents conversion requirements;
no automatic migration or silent network fallback occurs.

The notebook now has configuration and four code steps: A loads/reports through
the manager; B creates two ordinary DatePickers initialized from loaded coverage;
C calls `show_yield_history(observations, start_picker.value, end_picker.value)`;
D calls `analyze_curve` with those same direct inputs and `show_curve_results`.
Both dates are read anew on each respective execution. A normal Plotly Figure
retains full history, gaps, zoom, pan, hover and its range slider. Figure state
has no callback or other path to the widgets. Reexecuting B resets the controls.

[`analysis/treasury_curve.py`](../src/bondview/analysis/treasury_curve.py)
returns structured numeric results and stable IDs. Yield IDs are `DGS2`, `DGS10`,
`DGS30`; segment IDs are `DGS10_DGS2`, `DGS30_DGS10`. Endpoint configurations,
movement family, slope, and individual short/long directions are separate IDs.
This intentionally replaces the previous display-text index and combined text
fields. Missing and inapplicable classifications have distinct stable IDs;
missing numeric results remain NaN. Numeric units remain `%` and `bp`.

[`presentation/treasury_curve.py`](../src/bondview/presentation/treasury_curve.py)
owns table formatting, interpretation and display. [`config/labels.yaml`](../config/labels.yaml)
owns measure/tenor names, regimes, directions, configurations, unit formatting,
headings, interpretation templates, plot labels, widget descriptions, and report
wording. Each presentation call reloads labels. Calculations never read YAML;
`slope_tolerance_bp=0.0` remains an overridable Python default exclusively.
Presentation helpers moved out of the financial module; plotting now requires
explicit dates. The source/editable Poetry notebook workflow is documented;
standalone wheel deployment is outside this assignment and was not tested.

## Acceptance evidence

All paths below are relative to
[`artifacts/work_runs/261026_analysis1a_refactor_1823/`](../artifacts/work_runs/261026_analysis1a_refactor_1823).

| Requirement | Observed behavior | Assessment | Evidence / limit |
|---|---|---|---|
| CSV round-trip | Exact dates, values (including long decimal floats), missing entries and nested metadata preserved; one file only | PASS | `tests/test_fred.py`; `evidence/unittest.txt` |
| Reusable native units/frequency | Monthly Percent, daily FX and quarterly Index fixtures download/align without transformations; units/frequency retained | PASS, fixtures | `tests/test_fred.py`; no live authenticated API run |
| Independent provenance | Clearing DataFrame attrs or mutating a returned metadata copy leaves manager reporting/saving intact | PASS | `test_mixed_units_and_frequency_and_manager_independent_provenance` |
| Offline file mode | Network and dotenv readers guarded against calls; fresh notebook file kernel succeeds | PASS | Data and notebook tests |
| Credentials | Explicit, environment and dotenv precedence retained; request errors hide credential-bearing URLs | PASS, fixtures | Download tests |
| Coverage-based widgets | Two DatePickers use min/max loaded dates without blocking out-of-coverage selections | PASS | Plot/default tests and notebook execution |
| Manual plot rerun | Both widget values changed, plot cell rerun, Figure range updates while old analysis stays unchanged | PASS | Fresh-kernel notebook tests in both modes |
| Independent analysis rerun | Dates changed again, analysis rerun without redrawing the older Figure; current widget dates used | PASS | Same notebook tests |
| Plot state isolation | Figure range changed, widget dates and rerun analysis remain tied to selected values | PASS, object-level | No interactive browser gesture QA |
| Exact missing endpoints | Sundays, holidays, missing individual tenor endpoints, out-of-coverage dates remain N/A; independent available values retained | PASS | Curve tests; regression comparison |
| Financial behavior | Signs, units, all movement families, stationary tenors, parallel shifts, equal dates, inclusive tolerance and partial results checked | PASS | Curve tests; 510 synthetic baseline comparisons |
| Label independence | Custom YAML changes table names/regimes, interpretation and plot title; numbers/IDs unchanged, no reimport required | PASS | `test_yaml_changes_display_without_changing_financial_results` |
| No anywidget | Notebook executes in fresh file/download kernels with anywidget import explicitly blocked | PASS | `tests/test_notebook.py`; actual Poetry environment also lacks anywidget |
| Notebook simplification | Five code cells (configuration + A–D); operational branches/loops/functions/classes absent, direct widget inputs present | PASS | AST assertions in notebook tests |
| Python syntax / notebook schema | 14 current source/test/evidence Python files compiled; notebook validates | PASS | `evidence/checks.json` |
| Poetry / diff checks | `poetry check`, `git diff --check` pass | PASS | Same evidence |
| Live retrieval / browser frontend | No new live FRED request or interactive browser session performed | NOT_RUN | Intentional validation limitations, not claimed as passed |

## Financial parity and archived observed example

[`evidence/check_baseline.py`](../artifacts/work_runs/261026_analysis1a_refactor_1823/evidence/check_baseline.py)
loads the baseline financial module from Git history and compares it to current
calculations. It checks 125 constructed three-tenor change vectors at four
slope tolerances (0, 9.99, 10, 20 bp), six individually missing endpoint cases,
and four missing-date/same-day cases: **510 synthetic comparisons**. It also
reconstructs the two real observed endpoints from the baseline's committed
result table and provenance record, round-trips them through CSV, and compares
that observed interval. There are **zero numeric, formatted-table or
interpretation-text differences** across all comparisons. This extends focused
unit checks without treating the old source as financial-design authority.

| Measure | Start 2024-09-16 | End 2025-01-13 | Change | Default movement label |
|---|---:|---:|---:|---|
| 2Y | 3.56% | 4.40% | +84 bp | Yield rose |
| 10Y | 3.63% | 4.79% | +116 bp | Yield rose |
| 30Y | 3.94% | 4.97% | +103 bp | Yield rose |
| 10Y−2Y | +7 bp | +39 bp | +32 bp | Bear steepening |
| 30Y−10Y | +31 bp | +18 bp | −13 bp | Bear flattening |

One percentage point = 100 bp; slope change is long-tenor change minus
short-tenor change. Thus 116−84 = +32 bp and 103−116 = −13 bp. Each segment is
classified independently. The largest observed rise is at 10Y. These findings
support Treasury-tenor context, without estimating an ETF's price effect,
future return or a purchase recommendation.

The real endpoints were originally retrieved in the baseline run at
2026-10-26T07:45:15.134022+00:00. This refactor did **not** download new market
observations or validate a full historical cache. The initial checkout's ignored
JSON cache did not match the baseline's archived SHA-256, so it was not used as
baseline evidence. Only the committed endpoint table/provenance are used for
the reproducible observed-data comparison. The small endpoint CSV retains that
original provenance; its inherited `missing_policy` text refers to the original
JSON storage. CSV empty fields are defined by the new format. No vintage or
historical publication-availability reconstruction is claimed.

## Checks and reproduction

Executed using the existing project's Poetry virtual environment, with the
isolated clone's `src/` explicitly selected through `PYTHONPATH`:

```bash
poetry run python -m unittest discover -s tests -v
poetry run python artifacts/work_runs/261026_analysis1a_refactor_1823/evidence/check_baseline.py
poetry run python -m py_compile <all current source, test, and run-evidence Python files>
poetry check
git diff --check
```

Final suite: **26 tests passed**, including both fresh notebook kernels.
The initial kernel attempt hit the sandbox's local-socket restriction; the
permission-enabled rerun passed. No test failure remains. Notebook execution
uses transport fixtures and real DatePicker objects. Full browser rendering,
mouse/touch interaction and a live keyed API request remain unverified.
No independent reviewer subagent was used or represented as having reviewed.
Usage/token statistics were not exposed.

To demonstrate: install with Poetry, open the notebook, choose file/download,
execute A–D, change both controls, and rerun C or D independently. Choose
2024-09-16 and 2025-01-13 when those observations are loaded to reproduce the
reference comparison. Choose a Sunday for one endpoint to see N/A without
substitution. Edit display terminology in YAML and rerun output cells to observe
presentation changes with stable numerical results and IDs. All detailed
results are linked from the [manifest](../artifacts/work_runs/261026_analysis1a_refactor_1823/manifest.json).
