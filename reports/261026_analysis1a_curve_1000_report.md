# Analysis 1.A — Treasury curve conditions and movements

## Execution result and scope

**PASS_WITH_LIMITATIONS**, assessed directly in this standalone Codex session.
The notebook, reusable Python functions, local-file format and focused tests
are implemented. Actual FRED retrieval, package imports and a real-data notebook
execution succeeded. The retrieved endpoint values agree with the accepted
example. A live keyed API request and visual browser interaction were not run;
their distinct limitations are recorded below. This assessment is not user/Archie
final acceptance.

Only Analysis 1.A is implemented. There is no term-premium decomposition,
scenario generation, ETF-return calculation, investment rule or recommendation.
No subagents were created, and no independent role review is claimed.

## Authority, provenance and publication snapshot

- Assignment: user-pasted **Implement Analysis 1.A in Jupyter Notebook**, with
  an explicit standalone-session exception to role delegation, retaining the
  session/task PR and report/evidence workflow.
- Run ID: `261026_analysis1a_1000`; report date: **2026-10-26 (Asia/Seoul)**.
- Clean approved `main` baseline: `58f874e133a6c9405782b1a25f09df257a58413f`.
  Fetch/prune and live remote inspection found only `main` before this run's
  branches were created. No pre-existing working-tree changes were present.
- Accepted financial sources at that revision:
  `docs/bond_etf_decision_architecture.md`, especially §§2.1, 3.1.A, 4–6, and
  `docs/bond_etf_decision_examples.md` §2.1.A. Their provisional headers do not
  override the user's explicit authorization for this assignment. The task's
  exact-date/missing-data instructions and slope parameter supply the more
  specific implementation requirements. No other financial document was used.
- Engineering sources: root `AGENTS.md`, the two named `workflow/*_contract.md`
  contracts, `pyproject.toml`, `poetry.lock` and `.gitignore` at the baseline.
  `docs/` and `workflow/` are unchanged.
- Session branch: `codex/session/261026_1000`.
- Task branch: `codex/task/261026_1000_analysis1a`.
- Verified implementation/evidence commit:
  [`b489e070ed5d8278f4fa026b514ea6e698befb49`](https://github.com/lbk209/bondview-v3/commit/b489e070ed5d8278f4fa026b514ea6e698befb49).
  This report and the manifest are a subsequent documentation commit on the
  same task branch; use the task PR's final head for the complete package.
- [Task PR #35](https://github.com/lbk209/bondview-v3/pull/35) was verified open,
  unmerged and targeting the session branch when this report was authored.
  Integration, remote task-branch removal and the final session-to-`main` PR
  are subsequent publication operations. Their resulting state is verified in
  the final PR/session response, rather than predicted here. This report is
  the technical verification snapshot before those Git operations.

Environment: Poetry 2.3.3, Python 3.12.1, pandas 3.0.6, NumPy 2.5.4,
Plotly 6.9.0, ipywidgets 8.1.9, nbclient 0.11.0 and nbformat 5.11.1 in the
existing Poetry environment. No dependency was added or updated. `poetry.lock`
is unchanged; `poetry check --lock` passed after package configuration changed.

## Requirements and observed evidence

Paths below are relative to
[`artifacts/work_runs/261026_analysis1a_1000/`](../artifacts/work_runs/261026_analysis1a_1000/).
Tests are reproducible repository files, not claimed market observations.

| Requirement | Accepted behavior | Observed result | Status | Evidence | Limitation |
|---|---|---|---|---|---|
| R01 — real download | Attempt actual DGS2/10/30 retrieval | Public FRED CSV succeeded; 285 dated rows for 2024-01-01 through 2025-01-31; 14 missing observations per series | PASS | `evidence/real_fred.json` | Initial sandbox DNS failure resolved with network permission |
| R02 — keyed API | Read explicit/env/.env key; daily original-unit retrieval | Fixtures verify key precedence, unit/frequency checks, missing marker, response metadata and truncation rejection | PASS (fixtures) | `tests/test_treasury_curve.py`, `evidence/checks.json` | No key present for a live API request |
| R03 — keyed live retrieval | Real authenticated API request when credentials permit | Not run; `FRED_API_KEY` absent from environment and root `.env` | NOT_RUN | `evidence/real_fred.json` identifies actual public transport | Real download itself succeeded without credentials |
| R04 — save/load | Shared observations with dates, series, units and retrieval metadata | Canonical JSON round-trip preserves values, missing observations and metadata; downloaded/loaded calculations identical | PASS | `evidence/real_fred.json`; file/transport tests | Canonical JSON only; bare CSV is rejected |
| R05 — offline file mode | Never contact FRED | Fresh-kernel file mode and load tests use a transport guard that fails on any request | PASS | `tests/test_notebook.py`, `evidence/checks.json` | Requires a valid local canonical file |
| R06 — invalid input | Validate dates, series columns and units | Invalid dates, duplicate dates, missing columns, units, timestamps, strings, booleans, infinity, malformed JSON and missing files checked | PASS | `tests/test_treasury_curve.py` | Units must be explicit Percent; no magnitude guessing |
| R07 — historical chart | Plotly lines for all loaded history, %, dates, legend, hover/zoom, initial Sep–Jan view | Three historical line traces, 285 dated observations each, missing gaps, range slider and hover configuration | PASS (execution/configuration) | `evidence/notebook_execution.json`; plotting test | Browser interaction not visually checked |
| R08 — date controls | Simple controls, manual analysis, no reactive download | Two DatePickers instantiated; final cell rerun with changed Sunday input and network forbidden | PASS | `tests/test_notebook.py`, `evidence/checks.json` | No user browser was available |
| R09 — exact dates | No substitution, fill or interpolation | Absent weekends/holidays/out-of-coverage dates produce missing inputs; available opposite endpoints remain | PASS | curve tests, notebook manual-rerun assertion | Users may choose another exact date themselves |
| R10 — partial results | Missing one tenor does not discard other rows | Missing 30Y start preserves 4.97% end, 18 bp end spread and valid +32 bp 10Y−2Y change | PASS | `examples/missing_30y_start.csv`, `evidence/edge_examples.json` | This missing-data modification is synthetic |
| R11 — arithmetic | Five rows; yield %, spread bp; derived spreads | +84/+116/+103 bp, +32/−13 bp reproduced with matching endpoints | PASS | `examples/real_fred_comparison.csv`; design/unit tests | Net interval changes only |
| R12 — classifications | Independent segment slope and direction, zero/default/nonzero tolerance | Bull/bear, opposing-direction twist, four stationary-tenor cases, parallel shifts, unchanged and tolerance boundaries checked | PASS | classification tests, `evidence/edge_examples.json` | Twist is a documented convention; tolerance is not calibrated |
| R13 — interpretation | Identify concentration without unsupported ETF inference | 10Y has largest observed rise (+116 bp); segment labels differ correctly | PASS | `evidence/real_fred.json` | Does not establish causes, forecasts or ETF returns |
| R14 — package/notebook | Importable src package, understandable execution order | Root package installed; fresh kernels execute both modes from temporary directories; real-data execution from `notebooks/` completes | PASS | `tests/test_notebook.py`, `evidence/notebook_execution.json` | Select the Poetry Python kernel |
| R15 — checks | Python syntax, focused tests, lock/configuration | 21 tests pass; all Python files compile; notebook schema valid; lock and diff checks pass | PASS | `evidence/checks.json` | Kernel tests need local socket permission in restricted environments |
| R16 — visual frontend | Inspect hover, zoom and calendar interaction | Computer-use inventory returned no apps/browsers | NOT_RUN | `evidence/notebook_execution.json` | No claim of browser QA; MIME/controls/configuration verified instead |
| R17 — ownership/security | No credentials/caches in Git; no design/workflow edits | Root `/data/` ignored; tracked output contains concise provenance/endpoints, no raw cache or credential | PASS | changed-file list in task PR; `.gitignore` | Custom cache paths must also stay outside Git |
| R18 — independent review | Standalone exception | No role simulation or child agents | NOT_APPLICABLE | User assignment | Economic checks were performed by the implementing session |

## Implementation and interfaces

- [`notebooks/analysis1_curve.ipynb`](../notebooks/analysis1_curve.ipynb): brief
  operating instructions, configuration/imports, load/save, historical plot,
  date pickers and manually executed analysis. Delivered without execution
  outputs or embedded market caches.
- [`notebooks/README.md`](../notebooks/README.md): launch steps, JSON schema,
  percent/bp convention, credential precedence and interpretation boundaries.
- [`src/bondview/data/fred.py`](../src/bondview/data/fred.py):
  `download_fred`, `save_observations`, `load_observations`,
  `validate_observations` and `exact_date`. The common representation is a
  pandas DataFrame with unique calendar dates, numeric series columns and
  `attrs["metadata"]`. Default IDs are DGS2, DGS10 and DGS30. The API path can
  retrieve other daily Percent series; other measurement types are outside
  this assignment. Local persistence is reusable independently of plotting.
- [`src/bondview/analysis/treasury_curve.py`](../src/bondview/analysis/treasury_curve.py):
  `analyze_curve`, `classify_segment`, `display_table` and `interpret_curve`.
  Numeric outputs remain numeric; presentation converts missing values to
  `N/A` and attaches units. Same-day comparisons are valid; reversed intervals
  and intraday/timezone inputs are rejected.
- [`src/bondview/plotting/treasury_curve.py`](../src/bondview/plotting/treasury_curve.py):
  `plot_yield_history` returns a Plotly Figure using all loaded observations;
  display limits change the viewport, not the underlying dataset.
- Package `__init__.py` files establish the importable modules. `pyproject.toml`
  enables normal Poetry package installation with `src/bondview`; no path hacks
  or new dependencies. `.gitignore` adds root-only `/data/` cache exclusion.
- [`tests/test_treasury_curve.py`](../tests/test_treasury_curve.py) and
  [`tests/test_notebook.py`](../tests/test_notebook.py): offline unittest suite,
  with explicit synthetic fixtures and actual fresh-kernel notebook execution.

## Financial verification and real-world walkthrough

Actual source: [FRED DGS2](https://fred.stlouisfed.org/series/DGS2),
[DGS10](https://fred.stlouisfed.org/series/DGS10),
[DGS30](https://fred.stlouisfed.org/series/DGS30), H.15 constant-maturity market
yields, daily Percent. FRED's [API documentation](https://fred.stlouisfed.org/docs/api/fred/series_observations.html)
defines the untransformed-observation request used by the keyed transport.
Real retrieval occurred at `2026-10-26T07:45:15.134022+00:00` via public graph CSV.
The ignored local cache's SHA-256 and metadata are retained in `real_fred.json`.

| Measure | Actual FRED 2024-09-16 | Actual FRED 2025-01-13 | Calculated change | Difference from accepted example |
|---|---:|---:|---:|---:|
| 2Y yield | 3.56% | 4.40% | +84 bp | 0 bp |
| 10Y yield | 3.63% | 4.79% | +116 bp | 0 bp |
| 30Y yield | 3.94% | 4.97% | +103 bp | 0 bp |
| 10Y−2Y | +7 bp | +39 bp | +32 bp; bear steepening | 0 bp |
| 30Y−10Y | +31 bp | +18 bp | −13 bp; bear flattening | 0 bp |

Example arithmetic: `(4.79 − 3.63) × 100 = 116 bp`.
`116 − 84 = +32 bp` and `103 − 116 = −13 bp`. Both underlying
yields rose within each segment, so the descriptors are bear steepening and
bear flattening respectively. Both segments remained upward-sloping.
Spreads are derived from tenor observations, never separately downloaded.
The example cites Treasury par-yield data; this implementation uses FRED/H.15.
All six endpoint levels and all five reported changes agree in this retrieval;
that is an observed comparison, not an assumption of universal source equality.

The greatest upward yield move was at 10Y among the three selected maturities.
This is useful Treasury-market context for reviewing maturity exposure, but an
ETF's price effect also requires its duration and other characteristics. No
actual ETF was evaluated because the assignment authorizes Treasury-tenor
analysis only. No macroeconomic cause or future movement is inferred.

Conventions and hand checks:

- A yield level of `4.0` means **4%**; `(end − start) × 100` gives bp. The
  separate 4.0/4.5/4.8 fixture derives **50/30 bp** segment spreads.
- For each segment, `delta_slope_bp = delta_long_bp − delta_short_bp`.
  Positive/negative changes beyond tolerance are steepening/flattening.
  `abs(delta_slope_bp) <= slope_tolerance_bp` is unchanged slope, including
  the boundary. Default tolerance is **0.0 bp**, with no calibration model.
- Both yields rising/falling distinguish bear/bull; opposite signs identify
  a descriptive twist. Equal changes are parallel upward/downward shifts;
  both zero are unchanged yields. One stationary tenor is stated explicitly
  instead of implying that both yields moved in the same direction.
- For synthetic short/long changes **+10/+11 bp**, zero tolerance gives bear
  steepening; **1 bp** tolerance gives bear unchanged slope. It is not labeled
  parallel: actual directions and slope are distinct fields.
- Float cancellation is rounded at **10 decimal places in bp**, many orders
  below source quotation precision. This is documented numerical precision,
  separate from the user-controlled economic slope tolerance.
- A synthetic missing 30Y start retains 30Y end **4.97%**, 30Y−10Y end
  **18 bp** and 10Y−2Y change **+32 bp**; dependent changes are `N/A`.
  Missing dates and observations are never filled, interpolated or treated as
  zero. Available start/end configurations are also preserved independently.

## Verification commands and limitations

Executed checks, with outputs in [`evidence/checks.json`](../artifacts/work_runs/261026_analysis1a_1000/evidence/checks.json):

```text
poetry install --only-root
poetry check --lock
poetry run python -m unittest discover -s tests -v
poetry run python -m py_compile <all Python files under src/ and tests/>
git diff --check
nbformat.validate(notebook) and output-free delivered notebook assertion
```

The final suite ran **21 tests in 4.799 seconds**, all passing. Subtests include
the 25-pair sign grid, all six single-missing endpoint positions, malformed
file variants, and two independent notebook kernels. Notebook fixture execution
covers both download and file modes, then changes the selected start to a Sunday
and manually reruns analysis with network access forbidden. Imports work from
temporary directories without `sys.path` edits.

The delivered notebook was also executed from `notebooks/` in **file mode with
the actual downloaded 285-row cache**: five code cells completed, zero errors,
three 285-point Plotly traces, a widget output containing the two DatePickers,
and both expected classifications in the displayed HTML table. Large executed
notebook/HTML previews were kept only in `/tmp`, not committed evidence.

The initial sandbox denied DNS and local kernel sockets. Authorized escalated
execution resolved both; these were environmental restrictions, not fabricated
successful runs. Jupyter emitted a local TCP transport warning during execution;
the actual tests completed. Static nbconvert export could not represent Plotly's
MIME output, so the Plotly figure was exported separately for inspection.
Computer-use inventory then reported no browser/app, preventing visual QA.
No claim is made that browser hover/zoom/calendar interaction was observed.

Additional limitations:

- Real **keyed** API retrieval remains unverified because no key was configured.
  Its request behavior is covered by transport fixtures. Real retrieval was
  independently verified through the implemented public CSV path, not a fixture.
- FRED observations can be revised. Retrieval timestamps indicate when the
  snapshot was obtained; observation dates do not assert original release or
  availability dates. This is not an ALFRED vintage reconstruction or an
  as-known-at-the-time backtest. API metadata retains response realtime dates
  and series last-updated information when supplied by that transport.
- Public CSV may return full source history; the downloader explicitly selects
  the requested inclusive interval locally. Units for its three supported IDs
  are the known documented Percent definitions; other IDs require the API path.
- Local files must use the documented canonical JSON format. The implementation
  does not guess the units/provenance of arbitrary spreadsheets or CSVs.
- All descriptions are net endpoint classifications, not an account of every
  intervening movement. Alternative tolerances are parameters, not recommendations.

## Direct review dispositions and usage

No reserved financial design change was required. The implementation chooses a
single self-describing JSON file to avoid disconnected metadata sidecars; this
is an engineering choice within the authorized file-mode requirements.
The public FRED path supplies real observations despite absent credentials and
is explicitly identified; an invalid configured API key does not silently switch
transport. Tolerated unequal yield moves retain their direction/slope distinction.
The root cache ignore is anchored so that `src/bondview/data/` remains tracked.

The standalone exception makes reviewer/developer delegation **not applicable**.
All code inspection, financial arithmetic checks and tests were performed directly
in this session. Child-agent rounds: **0**. Token/credit usage: **not exposed**.
Platform escalations were used for Git metadata/network, Poetry installation,
real FRED retrieval and local Jupyter kernels. No additional user scope gate
was introduced; no one-time prerequisites validation was conducted.

## Reproduction and artifact index

1. Check out the final session PR and run `poetry install` from its root.
2. Run `poetry run python -m unittest discover -s tests -v` (local kernel sockets
   must be permitted), then `poetry run jupyter lab`.
3. Open `notebooks/analysis1_curve.ipynb` with the Poetry Python kernel.
   Default `download` mode saves the ignored `data/fred/treasury_yields.json`.
   An API key in the environment or root `.env` is used if present; otherwise
   the known Treasury series use the public FRED endpoint.
4. Inspect the historical plot. Keep the initial 2024-09-16/2025-01-13 endpoints
   and run the analysis cell for the table above. Inspect other exact dates
   by editing the pickers and rerunning only the final cell.
5. For offline use, set `DATA_MODE = "file"`, choose a previously saved canonical
   file and run the sequence. No network is required. The raw cache is not part
   of the Git deliverable, so a new checkout needs a download or existing file.

Verified durable evidence:

- [`manifest.json`](../artifacts/work_runs/261026_analysis1a_1000/manifest.json)
- [`evidence/checks.json`](../artifacts/work_runs/261026_analysis1a_1000/evidence/checks.json)
- [`evidence/real_fred.json`](../artifacts/work_runs/261026_analysis1a_1000/evidence/real_fred.json)
- [`evidence/notebook_execution.json`](../artifacts/work_runs/261026_analysis1a_1000/evidence/notebook_execution.json)
- [`evidence/edge_examples.json`](../artifacts/work_runs/261026_analysis1a_1000/evidence/edge_examples.json)
- [`examples/real_fred_comparison.csv`](../artifacts/work_runs/261026_analysis1a_1000/examples/real_fred_comparison.csv)
- [`examples/missing_30y_start.csv`](../artifacts/work_runs/261026_analysis1a_1000/examples/missing_30y_start.csv)

The PR history is the source of final publication/merge state. The final
session-to-`main` PR must remain unmerged for independent user/Archie review.
