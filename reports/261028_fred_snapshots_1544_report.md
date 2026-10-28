# FRED per-series snapshots and Analysis 1.A integration

Implemented directly by Codex for the 2026-10-28 assignment. Baseline: GitHub `main`, commit `87bd522a277a1cbcd66d2ade7ff6ecb471ac7d22`. The assigned checkout was clean; fetch/prune and live remote inspection confirmed that baseline before editing. No subagents were used.

## Result and usage

`FredDataManager` now takes a snapshot directory. Download, save and load are separate operations:

```python
fred = FredDataManager(PROJECT_ROOT / "data/fred", env_path=PROJECT_ROOT / ".env")
downloaded = fred.download(series_ids=FRED_SERIES, start=None, end=None)
fred.report()  # Optional inspection.
paths = fred.save()
observations = fred.load(series_ids=["DGS2", "DGS10", "DGS30"])
```

`download()` requests only the supplied IDs, supports open date boundaries and writes nothing. API-key precedence remains explicit key, environment, then the specified `.env`. The existing keyless graph-CSV fallback remains limited to the three known Treasury IDs; arbitrary other IDs use the API and require a key. IDs are validated for safe alphanumeric/underscore filenames and retain their original case.

`save()` creates one `<series_id>_<YYYYMMDD>.csv` per downloaded ID. The date comes from the retrieval timestamp converted to UTC, even if saving occurs later. `save()` returns an ID-to-Path dictionary. Previous snapshots remain. Same-day collisions raise `FileExistsError` before publication; even a competing writer after the preflight cannot be overwritten. All files are serialized and validated in a temporary directory before exclusive hard-link publication. A publication failure rolls back only files created by that call. Existing snapshots remain intact. Saving requires a successful download; loading does not authorize saving.

`load()` selects the largest valid calendar-date suffix independently for each requested ID. It checks the self-contained CSV, the single series identity, units/frequency, numeric observations and provenance, including agreement between the filename date and the UTC retrieval date. Missing IDs and malformed names/content produce errors that identify the series or file. A corrupt latest file is an error, never an instruction to use an older snapshot. Loading does not read credentials or use the network. Optional start/end arguments still select a date interval.

Mixed selected snapshot dates issue a visible `UserWarning` listing each ID/date, and loading continues. Matching dates do not imply identical data vintages. No batch IDs, common-date synchronization, database, incremental download, migration or filename mapping configuration were added. The ID convention already supplies the mapping.

## Changed files and metadata contract

| File | Change |
| --- | --- |
| `src/bondview/data/fred.py` | Directory-based manager, per-call ID selection, explicit operations, exclusive saving, discovery/validation, metadata and reporting. |
| `src/bondview/config/labels.yaml` | FRED report and warning templates only; financial presentation definitions remain unchanged. |
| `notebooks/analysis1_treasury_market.ipynb` | Shared seven-ID acquisition instructions, normal offline Treasury loading and shared `DateRangePicker`; stale saved outputs cleared. |
| `tests/test_fred.py` | Lower-level regression coverage and controlled snapshot/API tests. |
| `tests/test_notebook.py` | Tests the current notebook and actual widget/cell structure in a fresh kernel. |
| `tests/test_treasury_curve.py` | Repairs pre-existing outdated imports, label/config paths and expectations to match unchanged baseline behavior. |

The module-level `download_fred()`, `save_observations()` and `load_observations()` are reused. The self-contained `bondview.fred_observations.csv.v1` format remains. The low-level CSV writer retains its general serialization interface; overwrite protection for managed dated snapshots belongs to the manager's publication step. The old single-combined-file manager workflow and `load_or_download()` were removed intentionally. Existing combined CSVs were left untouched.

Downloaded metadata retains its existing root retrieval timestamp. When loading snapshots, `metadata['series'][id]` retains source units/frequency and other series fields, and its `provenance` mapping retains the original non-series headers, including the individual source, transport, request boundaries and retrieval timestamp. Combined loaded metadata has no fabricated shared retrieval timestamp. `metadata` returns a defensive deep copy and remains usable when DataFrame attrs are cleared. Validation accepts both the original shared-provenance form and this per-series form.

Outer alignment preserves the union of observation dates and leaves unavailable values missing. Snapshots saved from a combined download retain that aligned date index. Missing counts therefore include alignment gaps and dates outside each series' nonmissing coverage; they are not a count of source-reported missing releases alone. No filling, interpolation, resampling or unit conversion occurs. Financial analyses retain responsibility for date eligibility.

`report()` prints requested IDs, mode, aligned row coverage, selected dates for loaded snapshots, each series' nonmissing coverage and missing count, source units/frequency and retrieval context. Complete shared coverage uses `dropna()` across all requested columns. Its first/last dates and count do not imply completeness between those dates. All-missing series and no complete shared dates are reported explicitly. Presentation text uses the existing labels configuration.

## Notebook and financial regression boundary

The executable Setup cells initialize the directory-based manager, load DGS2/DGS10/DGS30 offline, report coverage and construct the shared `DateRangePicker`. Optional full-history download/report/save calls for all seven requested IDs appear in a clearly identified Markdown code example, so **Run All does not download or save**. Running those explicit calls is the user's data-refresh action.

Analysis 1.A's plot, calculation and presentation cells retain their existing source, including both 5 bp tolerances. `analyze_curve()`, the plot implementation, financial presentation implementation and widget implementation were not modified. B/C headings and placeholder sections remain unchanged, with no calculations added.

The old tests were not a usable baseline contract: the first test run failed to import the moved `date_picker_defaults`. After repairing that import, the Treasury tests exposed 16 failures and one configuration error from obsolete expectations: two-decimal bp labels, old movement wording, flat YAML paths, exact-date rather than effective-available endpoints, full-history rather than interval-filtered plot traces, a range slider, and a former near-parallel movement classification. Tests now check the behavior already present in `main`; the financial implementation was not changed to satisfy them. The existing same-day table has four display columns because its duplicate endpoint-date keys coincide; this existing behavior was retained.

A hand-checkable Treasury fixture produces yield changes **84, 116, 103 bp**, spread changes **32 and -13 bp**, a bear-steepening 2Y–10Y segment and flattening 10Y–30Y segment, before and after snapshot round trips and notebook execution. Missing tenor endpoints retain independent available results. Widget edits and plot-only/calculation-only reruns are verified.

## Validation evidence

- `poetry run python -m py_compile src/bondview/data/fred.py tests/test_fred.py tests/test_notebook.py tests/test_treasury_curve.py`: passed.
- `poetry run python -m unittest discover -s tests -v`: **39 tests passed**, including fresh-kernel execution with network/credential access blocked and anywidget unavailable. [Test output](../artifacts/work_runs/261028_fred_snapshots_1544/tests.log).
- Controlled tests cover arbitrary mixed-case IDs, open download boundaries, subset-only retrieval, no download writes, individual CSVs, UTC naming, previous-file retention, preflight/racing collisions, serialization/publication rollback, latest selection, mismatch/no-mismatch warnings, outer alignment, all-missing and incomplete common coverage, provenance/defensive copies, malformed/latest-file errors, native units/frequency, API truncation and credential suppression. [Inspectable example](../artifacts/work_runs/261028_fred_snapshots_1544/controlled_example.json).
- The actual notebook also executed offline against the real saved Treasury snapshots: 16,910 aligned rows and five analysis-result rows. [Execution evidence](../artifacts/work_runs/261028_fred_snapshots_1544/actual_notebook.json).
- Source comparison verifies that the A/B/C cell sources, numerical implementation and financial presentation configuration are unchanged. The complete affected manager/validation/reporting units and modified tests were reviewed for obsolete branches, duplicate assignments and unnecessary conditions.
- `git diff --check` and a private credential-content check passed. No key, `.env` or market snapshot is included in the commit.

Jupyter cannot open its local kernel sockets inside the default execution sandbox; the fresh-kernel checks passed with approved elevated execution. This is an execution-environment restriction, not a live-data requirement for tests.

## Initial real download

The existing private credential lookup and network were available. All seven IDs were requested with `start=None`, `end=None`; initial retrieval timestamp: **2026-10-28T06:46:44.207917+00:00**. All seven report native **Percent** units and **D** source frequency. The files exist in the assigned workspace at `/home/lbk/works/bondview-v3/data/fred/`, and remain ignored by Git.

| Series | First nonmissing | Last nonmissing | Nonmissing count | Saved file |
| --- | --- | --- | ---: | --- |
| DGS2 | 1976-06-01 | 2026-10-26 | 12,597 | `data/fred/DGS2_20261028.csv` |
| DGS10 | 1962-01-02 | 2026-10-26 | 16,189 | `data/fred/DGS10_20261028.csv` |
| DGS30 | 1977-02-15 | 2026-10-26 | 12,419 | `data/fred/DGS30_20261028.csv` |
| THREEFY2 | 1990-01-02 | 2026-10-23 | 9,189 | `data/fred/THREEFY2_20261028.csv` |
| THREEFYTP2 | 1990-01-02 | 2026-10-23 | 9,189 | `data/fred/THREEFYTP2_20261028.csv` |
| THREEFY10 | 1990-01-02 | 2026-10-23 | 9,189 | `data/fred/THREEFY10_20261028.csv` |
| THREEFYTP10 | 1990-01-02 | 2026-10-23 | 9,189 | `data/fred/THREEFYTP10_20261028.csv` |

There are **9,189 complete shared dates**, from 1990-01-02 through 2026-10-23. [Sanitized download manifest, missing counts and SHA-256 hashes](../artifacts/work_runs/261028_fred_snapshots_1544/live_download.json).

The first verification assertion flagged pandas' inferred `BusinessDay` index frequency after the snapshots had already been saved successfully. CSV stores source frequency explicitly in metadata but does not retain pandas' transient `index.freq`. Verification was corrected to compare values, dates, missing values and dtypes exactly while excluding only that inferred attribute; a subsequent real full-history retrieval matched the saved observations exactly. A repeat save raised `FileExistsError`, preserving the original files. A regression test covers this distinction. Source frequency remains `D` throughout.

## Limitations and review status

- Snapshot dates are retrieval-date consistency indicators, not a vintage reconstruction or a guarantee of simultaneous source releases.
- Exclusive publication requires filesystem hard-link support. Individual files are published complete; this is not a crash-atomic multi-file transaction. An abruptly killed process could leave some complete new snapshots, which a subsequent load will handle independently.
- Snapshot selection follows the accepted date convention; malformed matching filenames fail explicitly. Existing combined files are outside this workflow.
- Default full-history Treasury analysis can have missing shorter-tenor endpoints before those series began. This is preserved Analysis 1.A behavior; the widget allows selection of the desired interval.
- No Analysis 1.B/1.C financial calculations or investment-policy changes were made. Implementation success does not establish acceptance of financial design.

Session branch: `codex/session/261028_1430`. The required publication sequence is a task PR into that session, a verified task merge and task-branch cleanup, then a final session-to-main PR left unmerged for user review. Actual publication links and verified cleanup state are recorded in the completion response and PR record.
