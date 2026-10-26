# Analysis 1.A

From the repository root, run `poetry install` and `poetry run jupyter lab`.
Open `analysis1_curve.ipynb` using that Poetry environment's Python kernel.
Run cells in order: configure → load/save → inspect historical plot → choose
dates → manually analyze. For subsequent comparisons, change the date pickers
and run only the final cell. Restarting the kernel requires loading again.

Set `DATA_MODE = "download"` to retrieve DGS2/DGS10/DGS30 and save a snapshot.
`FRED_API_KEY` in the environment takes precedence over the root `.env`. When
neither supplies a key, the downloader uses FRED's public graph CSV endpoint
for these known daily Percent series. Network failures raise an error; there
is no synthetic-data fallback. Set `DATA_MODE = "file"` to load `DATA_PATH`
offline. Display dates and analysis dates are separate inputs.

The default `data/fred/treasury_yields.json` is ignored by Git. Keep credentials
in the environment or ignored `.env`, and keep custom caches outside Git too.
No credentials are written to saved metadata. No new dependency is needed;
Poetry installs the `src/bondview` package so imports work without `sys.path`.

## Local-file format

Use `save_observations(frame, path)` to create a canonical, self-contained JSON
file. `frame` is a pandas DataFrame with a unique, timezone-free calendar-date
DatetimeIndex, numeric series columns and `frame.attrs["metadata"]`.
`load_observations(path)` validates this format and never contacts FRED.
Other financial data modules can reuse the same representation; this analysis
requires the three tenor columns. A missing tenor observation is `null`, not an
omitted column. Bare CSVs and guessed measurement units are intentionally rejected.

Minimal **synthetic format example**, not downloaded market data:

```json
{
  "format": "bondview.fred_observations.v1",
  "metadata": {
    "source": "Synthetic documentation example",
    "retrieved_at_utc": "2026-10-26T00:00:00+00:00",
    "series": {
      "DGS2": {"units": "Percent"},
      "DGS10": {"units": "Percent"},
      "DGS30": {"units": "Percent"}
    }
  },
  "observations": [
    {"date": "2024-09-16", "DGS2": 4.0, "DGS10": 4.5, "DGS30": null}
  ]
}
```

`4.0` means 4%, and a 0.01 percentage-point change equals 1 bp. Downloaded
files also retain source URLs, transport, requested dates, missing-value policy,
retrieval timestamp and vintage/availability limitations. API downloads retain
series titles, last-updated and response realtime dates. They are retrieval-time
snapshots: neither transport reconstructs what was available on a historical
assessment date. Observation dates are not publication dates.

## Interpretation and verification

No date substitution or filling occurs. All five rows remain in the table,
including available endpoints when dependent changes are missing. Yield levels
are in %, spread levels and all changes in bp. Classification tolerance applies
only to slope changes, with exact yield directions displayed separately where
needed. Floating cancellation is rounded to 10 decimal places in bp, far below
the series' quoted precision. This is numerical housekeeping, not a calibrated
economic threshold. Source values retain their original numeric precision.

Endpoint movements describe the selected interval, not every intervening move,
macroeconomic causation, a forecast, or realized ETF returns. A selected tenor's
yield move alone does not quantify an ETF's price effect without compatible
exposure information.

Run offline checks with `poetry run python -m unittest discover -s tests -v`.
See the run report under `reports/` for real-download evidence and notebook
execution results, distinguished from synthetic fixture tests.
