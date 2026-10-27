# Analysis 1.A

Run `poetry install` and `poetry run jupyter lab` from the repository root, then
open `analysis1_curve.ipynb` with that Poetry environment's Python kernel.
Execute configuration, **A. Data → B. Date selection → C. Plot → D. Analysis**.
After changing the two DatePickers, rerun C and D independently as needed. Each
reads the current widget values directly. Rerunning B resets dates to loaded
coverage. Plot zoom, pan and the range slider do not change the selected dates.
The chart retains all loaded observations, initially viewing the selected range.

`DATA_MODE = "download"` retrieves and saves DGS2/DGS10/DGS30. Credential order
is explicit `api_key` → `FRED_API_KEY` environment variable → root `.env`.
Without a key, these known daily Percent series use FRED's public graph CSV.
Other series use the keyed API with their native units and frequency; requests
use `units="lin"` and never impose a common frequency. Network failures raise
an error; there is no synthetic fallback. `DATA_MODE = "file"` loads `DATA_PATH`
without network, credentials or `.env` access.

The default `data/fred/treasury_yields.csv` is ignored by Git. Keep custom caches
and credentials outside Git. No dependency changes or `anywidget` are required.

## Self-contained CSV

`FredDataManager(path, env_path=..., series_ids=...)` manages `download`, `load`,
`save`, `validate`, `report`, and the explicit `load_or_download(mode, ...)`
workflow. `manager.metadata` is an independent defensive copy of provenance;
it survives loss or alteration of `manager.observations.attrs`. Saving and
reporting use that independent metadata. A compatibility metadata copy remains
in returned DataFrames' attrs. The standalone `save_observations(frame, path,
metadata=...)`, `load_observations(path)` and `download_fred(...)` also remain
available. Financial and plotting functions accept explicit `metadata=` when
DataFrame attrs have been lost.

The CSV has comment headers (`# key: JSON-encoded value`) followed by `date` and
series columns. Observation persistence is CSV, with no metadata sidecar. The
header encoding supports nested per-series attributes and escaped punctuation
without changing their content. Required metadata is source, a timezone-aware
retrieval timestamp, and per-series units/frequency. Optional downloaded
metadata includes source URLs, transport, request dates, API series title,
last-updated and realtime bounds, and retrieval-vintage limitations.

Minimal **synthetic example**, not downloaded market data:

```csv
# format: "bondview.fred_observations.csv.v1"
# source: "Synthetic documentation example"
# retrieved_at_utc: "2026-10-26T00:00:00+00:00"
# series: {"DGS2": {"units": "Percent", "frequency": "D"}, "DGS10": {"units": "Percent", "frequency": "D"}, "DGS30": {"units": "Percent", "frequency": "D"}}
date,DGS2,DGS10,DGS30
2024-09-16,4.0,4.5,
```

An empty numeric field means missing, never zero. Dates must be unique calendar
dates; values must be finite numbers or missing. Saving uses original numeric
precision and loading uses a round-trip float parser. Bare CSVs, duplicate dates
or series, malformed rows and absent measurement metadata are rejected. Shared
storage can outer-align series with different source frequencies without filling
or resampling; the per-series frequency is retained. Analysis 1.A separately
requires daily Percent DGS2/DGS10/DGS30 observations.

The former JSON cache format is intentionally no longer accepted. Set download
mode once to create a CSV. To preserve an existing historical snapshot without
retrieval, explicitly extract its `observations` into a dated DataFrame, retain
its `metadata`, and call `save_observations(frame, csv_path, metadata=metadata)`.
Do not rename a JSON cache to `.csv`; generic old files without frequency need
explicit source-frequency information. Existing committed historical evidence
is retained unchanged.

Retrieval snapshots do not reconstruct historical releases or vintages.
Observation dates are not publication dates. No filling, interpolation, unit
conversion or nearby-date substitution is applied to observations.

## Structured calculations and configurable presentation

`analyze_curve(observations, start, end, slope_tolerance_bp=0.0)` returns numeric
columns `start`, `end`, `change_bp`, `level_unit` and stable identifiers. Row IDs
are `DGS2`, `DGS10`, `DGS30`, `DGS10_DGS2`, `DGS30_DGS10`. `configuration_start`,
`configuration_end`, `movement`, `slope`, `short_direction` and `long_direction`
are categorical IDs (`unavailable` for missing classifications,
`not_applicable` where appropriate). These replace the baseline's display-text
row names and combined text fields intentionally. Selected dates and tolerance
remain in result attrs. Source provenance is managed independently by `fred`.

`display_table`, `interpret_curve`, `show_curve_results` live in
`bondview.presentation.treasury_curve`, separate from financial logic.
`plot_yield_history(data, start, end)` returns an ordinary Plotly `Figure`;
`show_yield_history` displays and returns it. Both dates are explicit, including
same-day selections. No callback or shared mutable selection state exists.

User-facing measure names, classification terminology, headings, interpretation
templates, plot labels, widget descriptions and provenance-report wording are
in `config/labels.yaml`. Presentation functions read it on each call, so edits
apply on cell reruns without reimporting or recalculating. Python callers may
supply `labels_path=`. Slope tolerance is exclusively a Python argument, never
YAML configuration. Use the source/editable Poetry installation for this
repository-based notebook workflow.

Yield levels are %, spread levels and all changes bp (0.01 percentage point =
1 bp). All five rows retain available endpoints even if changes are missing.
The slope tolerance is inclusive and applies only to slope, never to underlying
yield directions. Only equal tenor changes are parallel. Floating cancellation
is rounded to 10 decimal places in bp; source observations retain their numeric
precision. Default display conventions and numerical behavior match PR #36.

These are historical net endpoint movements, not the full path, macroeconomic
causes, forecasts, or realized ETF returns. ETF price effects require compatible
duration and other product characteristics.

Run `poetry run python -m unittest discover -s tests -v`. Tests include two
fresh notebook kernels with download transport fixtures or offline files and
blocked `anywidget` imports. Jupyter kernels require local socket access.
