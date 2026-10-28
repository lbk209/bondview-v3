"""Untransformed FRED observations with per-series units and CSV provenance.

Missing observations remain NaN in memory and empty fields on disk. No fill,
resampling, unit conversion, or date substitution occurs.
"""

from copy import deepcopy
import csv
from datetime import date, datetime, timezone
from io import StringIO
import json
import os
from pathlib import Path
import re
from tempfile import TemporaryDirectory
import warnings
from urllib.parse import urlencode
from urllib.request import urlopen

from dotenv import dotenv_values
import numpy as np
import pandas as pd

SERIES = ("DGS2", "DGS10", "DGS30")
FORMAT = "bondview.fred_observations.csv.v2"
API_BASE = "https://api.stlouisfed.org/fred/"


def _series_ids(series_ids):
    """Validate IDs before using them in API requests or filesystem paths."""
    if isinstance(series_ids, str):
        raise ValueError("Provide a collection of unique valid FRED series IDs.")
    ids = tuple(series_ids)
    if not ids or any(
        not isinstance(s, str) or not re.fullmatch(r"[A-Za-z0-9_]+", s) for s in ids
    ) or len(set(ids)) != len(ids):
        raise ValueError("Provide unique valid FRED series IDs.")
    return ids


def exact_date(value) -> pd.Timestamp:
    """Accept calendar dates only; reject intraday/timezone and missing inputs."""
    if isinstance(value, str) and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        raise ValueError("Use an exact ISO calendar date (YYYY-MM-DD).")
    if not isinstance(value, (str, date, datetime, pd.Timestamp)):
        raise ValueError("A calendar date is required.")
    result = pd.Timestamp(value)
    if pd.isna(result) or result.tz is not None or result != result.normalize():
        raise ValueError("Use a calendar date without a time or timezone.")
    return result


def validate_observations(data: pd.DataFrame, metadata=None) -> pd.DataFrame:
    """Validate observations and their per-ID provenance independently of units.

    Metadata is keyed directly by FRED ID; combined frames do not have shared
    metadata fields. Missing observations remain missing and dates are not filled.
    """
    if not isinstance(data, pd.DataFrame) or not isinstance(data.index, pd.DatetimeIndex) or data.empty:
        raise ValueError("Observations need a nonempty DatetimeIndex.")
    if data.index.hasnans or data.index.has_duplicates or data.columns.has_duplicates:
        raise ValueError("Observation dates and series IDs must be present and unique.")
    for value in data.index:
        exact_date(value)
    metadata = data.attrs.get("metadata", {}) if metadata is None else metadata
    if not isinstance(metadata, dict) or not metadata or set(data.columns) != set(metadata):
        raise ValueError("Per-series metadata must match the observation columns.")
    for series_id in data.columns:
        if not isinstance(series_id, str) or not re.fullmatch(r"[A-Za-z0-9_]+", series_id):
            raise ValueError("Invalid series ID.")
        info = metadata[series_id]
        if not isinstance(info, dict) or any(
            not isinstance(info.get(field), str) or not info[field].strip()
            for field in ("units", "frequency", "source", "retrieved_at_utc")
        ):
            raise ValueError(f"{series_id}: units, frequency, source and retrieval timestamp are required.")
        timestamp = pd.Timestamp(info["retrieved_at_utc"])
        if pd.isna(timestamp) or timestamp.tz is None:
            raise ValueError(f"{series_id}: retrieval timestamp must include its timezone.")
        if not pd.api.types.is_numeric_dtype(data[series_id]) or pd.api.types.is_bool_dtype(data[series_id]):
            raise ValueError(f"{series_id}: observations must be numeric or missing.")
        if np.isinf(data[series_id].to_numpy(dtype=float, na_value=np.nan)).any():
            raise ValueError(f"{series_id}: infinite observations are invalid.")
    result = data.sort_index().copy()
    result.index.name = "date"
    result.attrs["metadata"] = deepcopy(metadata)
    return result


def validate_treasury_observations(data, metadata=None):
    """Keep Analysis 1.A's daily Percent contract out of shared FRED storage."""
    data = validate_observations(data, metadata)
    if not set(SERIES).issubset(data.columns):
        raise ValueError("Treasury analysis requires DGS2, DGS10 and DGS30 columns; use NaN for missing observations.")
    for series_id in SERIES:
        info = data.attrs["metadata"][series_id]
        if info["units"] != "Percent" or info["frequency"] != "D":
            raise ValueError(f"{series_id}: Treasury analysis requires daily Percent observations.")
    return data


def _read_url(url: str) -> bytes:
    # Deliberately suppress low-level messages: API URLs contain a credential.
    try:
        with urlopen(url, timeout=45) as response:
            return response.read()
    except Exception:
        raise RuntimeError("FRED request failed. Check network access and API credentials.") from None


def _api_json(endpoint: str, api_key: str, **parameters) -> dict:
    url = API_BASE + endpoint + "?" + urlencode(
        {"api_key": api_key, "file_type": "json", **parameters}
    )
    return json.loads(_read_url(url))


def download_fred(
    start=None, end=None, *, api_key=None,
    env_path=None, series_ids=SERIES,
) -> pd.DataFrame:
    """Download untransformed observations with source units and frequencies.

    None for start/end means earliest/latest available observations.

    Prefer an explicit key, FRED_API_KEY in the environment, then env_path's
    .env key. Without a key, use FRED's public graph CSV for the three known
    Treasury series. Other series can use the API with a key, retaining their
    native frequency.
    This is a retrieval-time snapshot, not a point-in-time vintage database.
    """
    start = exact_date(start) if start is not None else None
    end = exact_date(end) if end is not None else None

    if start is not None and end is not None and start > end:
        raise ValueError("Download start must be on or before end.")

    ids = _series_ids(series_ids)

    key = api_key or os.getenv("FRED_API_KEY")
    if not key and env_path is not None:
        key = dotenv_values(env_path).get("FRED_API_KEY")

    series_metadata = {}

    if key:
        columns = []

        for series_id in ids:
            info = _api_json("series", key, series_id=series_id)["seriess"][0]
            if info.get("id", series_id) != series_id:
                raise ValueError(f"{series_id}: FRED returned a different series identity.")

            params = {
                "series_id": series_id,
                "units": "lin",
                "limit": 100000,
            }
            if start is not None:
                params["observation_start"] = str(start.date())
            if end is not None:
                params["observation_end"] = str(end.date())

            payload = _api_json(
                "series/observations", key, **params
            )

            if int(payload["count"]) != len(payload["observations"]):
                raise ValueError(
                    "FRED response was truncated; request a shorter period."
                )

            observations = payload["observations"]
            columns.append(pd.Series(
                [np.nan if row["value"] == "." else float(row["value"])
                 for row in observations],
                index=pd.DatetimeIndex([row["date"] for row in observations]),
                name=series_id,
                dtype=float,
            ))

            series_metadata[series_id] = {
                "units": info["units"],
                "frequency": info["frequency_short"],
                "title": info["title"],
                "last_updated": info["last_updated"],
                "realtime_start": payload.get("realtime_start"),
                "realtime_end": payload.get("realtime_end"),
                "source_url": f"https://fred.stlouisfed.org/series/{series_id}",
            }

        data = pd.concat(columns, axis=1)
        transport = "FRED API; untransformed observations at source frequency"

    else:
        if not set(ids).issubset(SERIES):
            raise ValueError(
                "An API key is required for series outside DGS2/DGS10/DGS30."
            )

        url = (
            "https://fred.stlouisfed.org/graph/fredgraph.csv?"
            + urlencode({"id": ",".join(ids)})
        )

        raw = pd.read_csv(
            StringIO(_read_url(url).decode("utf-8")),
            na_values=["."],
        )

        if set(raw.columns) != {"observation_date", *ids}:
            raise ValueError("Unexpected FRED CSV columns.")

        raw.index = pd.DatetimeIndex(
            [exact_date(d) for d in raw.pop("observation_date")]
        )
        data = raw.apply(pd.to_numeric, errors="raise")

        # Apply only the explicitly requested date boundaries.
        if start is not None:
            data = data.loc[data.index >= start]
        if end is not None:
            data = data.loc[data.index <= end]

        series_metadata = {
            s: {
                "units": "Percent",
                "frequency": "D",
                "source_url": f"https://fred.stlouisfed.org/series/{s}",
            }
            for s in ids
        }

        transport = "FRED public graph CSV; known H.15 daily Percent series"

    data.index.name = "date"

    # Each series carries complete, independent metadata, including retrieval
    # information shared by the particular download operation.
    common = {
        "source": "FRED / Federal Reserve H.15" if set(ids).issubset(SERIES) else "FRED",
        "transport": transport,
        "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
        "requested_start": str(start.date()) if start is not None else None,
        "requested_end": str(end.date()) if end is not None else None,
        "missing_policy": "No filling or date substitution; empty CSV fields mean unavailable.",
        "availability": "Known at retrieval; historical release availability is not reconstructed.",
        "vintage": "Retrieval-time snapshot; source observations may be revised.",
    }
    data.attrs["metadata"] = {series_id: {**info, **common}
                              for series_id, info in series_metadata.items()}

    return validate_observations(data)


# Human-readable v2 file order. Additional validated metadata fields follow.
HEADER_FIELDS = (
    "title", "units", "frequency", "source", "source_url", "last_updated",
    "retrieved_at_utc", "transport", "requested_start", "requested_end",
    "realtime_start", "realtime_end", "missing_policy", "availability", "vintage",
)


def _metadata_header(series_id, info):
    """Generate the exact flat CSV header, also used by detailed reports."""
    fields = ["format", "title", "series_id"]
    items = {"format": FORMAT, "series_id": series_id, **info}
    if "format" in info or "series_id" in info:
        raise ValueError("Reserved metadata header field.")
    fields.extend(k for k in HEADER_FIELDS if k != "title")
    fields.extend(k for k in info if k not in fields)
    lines = []
    for key in fields:
        if key not in items:
            continue
        if not re.fullmatch(r"[a-z_]+", key):
            raise ValueError("Invalid metadata header key.")
        lines.append(f"# {key}: {json.dumps(items[key], ensure_ascii=False, allow_nan=False)}\n")
    return lines


def save_observations(data: pd.DataFrame, path, *, metadata=None) -> Path:
    """Persist one FRED ID with a readable flat v2 metadata header."""
    data = validate_observations(data, metadata)
    if len(data.columns) != 1:
        raise ValueError("The v2 CSV format stores exactly one series ID per file.")
    series_id = data.columns[0]
    headers = _metadata_header(series_id, data.attrs["metadata"][series_id])
    path = Path(path).expanduser()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as stream:
        stream.writelines(headers)
        data.to_csv(stream, index_label="date", date_format="%Y-%m-%d", na_rep="")
    return path


def load_observations(path) -> pd.DataFrame:
    """Read a v2 per-ID CSV offline; reject incompatible or malformed files."""
    metadata = {}
    with Path(path).expanduser().open(encoding="utf-8", newline="") as stream:
        for line in stream:
            if not line.startswith("# "):
                body = line + stream.read()
                break
            key, separator, value = line[2:].partition(": ")
            if not separator or key in metadata:
                raise ValueError("Malformed or duplicate CSV metadata header.")
            def reject_constant(value):
                raise ValueError(f"Invalid metadata numeric constant: {value}.")
            metadata[key] = json.loads(value, parse_constant=reject_constant)
        else:
            raise ValueError("CSV observations are required.")
    if metadata.pop("format", None) != FORMAT:
        raise ValueError("Unsupported observation file format; expected Bondview FRED CSV v2.")
    series_id = metadata.pop("series_id", None)
    if not isinstance(series_id, str) or not re.fullmatch(r"[A-Za-z0-9_]+", series_id):
        raise ValueError("CSV requires a valid series_id header.")
    if any(not re.fullmatch(r"[a-z_]+", k) for k in metadata):
        raise ValueError("Invalid metadata header key.")
    rows = list(csv.reader(StringIO(body)))
    if len(rows) < 2 or rows[0] != ["date", series_id]:
        raise ValueError("CSV requires one date column and the declared series ID, plus observations.")
    if any(len(row) != 2 for row in rows[1:]):
        raise ValueError("Every CSV row must contain its date and observation.")
    dates = [exact_date(row[0]) for row in rows[1:]]
    for row in rows[1:]:
        value = row[1]
        if value and (not re.fullmatch(r"[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?", value)
                      or not np.isfinite(float(value))):
            raise ValueError("CSV values must be finite numbers or empty fields.")
    data = pd.read_csv(StringIO(body), index_col=0, float_precision="round_trip")
    data.index = pd.DatetimeIndex(dates, name="date")
    return validate_observations(data, {series_id: metadata})


class FredDataManager:
    """Download in memory and explicitly save/load independent ID snapshots.

    ``path`` is a directory. The manager owns the ID_YYYYMMDD.csv convention;
    dates are retrieval dates in UTC, not observation dates or vintage IDs.
    ``series_ids`` configures stable defaults for calls omitting explicit IDs.
    """

    def __init__(self, path, *, env_path=None, series_ids=SERIES):
        self.path = Path(path).expanduser()
        self.env_path = env_path
        self.series_ids = _series_ids(series_ids)
        self.observations = None
        self._metadata = {}
        self._mode = None
        self.snapshot_dates = {}

    @property
    def metadata(self):
        """Independent defensive copy, available even if DataFrame attrs are lost."""
        return deepcopy(self._metadata)

    def _accept(self, data, mode, snapshot_dates=None):
        data = validate_observations(data)
        self._metadata = deepcopy(data.attrs["metadata"])
        self.observations = data
        self._mode = mode
        self.snapshot_dates = dict(snapshot_dates or {})
        return data

    def validate(self):
        return validate_observations(self.observations, self._metadata)

    def download(self, start=None, end=None, *, series_ids=None, api_key=None):
        """Retrieve only the requested IDs; never write files."""
        self._mode = None
        ids = self.series_ids if series_ids is None else _series_ids(series_ids)
        return self._accept(download_fred(
            start, end, api_key=api_key, env_path=self.env_path, series_ids=ids,
        ), "download")

    def _latest_snapshot(self, series_id):
        candidates = []
        # Parse IDs greedily: underscores are valid inside a FRED ID.
        for path in self.path.glob(f"{series_id}_*.csv"):
            match = re.fullmatch(r"([A-Za-z0-9_]+)_([0-9]{8})\.csv", path.name)
            if match is None:
                raise ValueError(f"{series_id}: malformed snapshot filename: {path.name}")
            if match[1] != series_id:
                continue
            try:
                datetime.strptime(match[2], "%Y%m%d")
            except ValueError:
                raise ValueError(f"{series_id}: invalid snapshot date: {path.name}") from None
            candidates.append((match[2], path))
        if not candidates:
            raise FileNotFoundError(f"{series_id}: no saved snapshots in {self.path}.")
        return max(candidates)

    def load(self, start=None, end=None, *, series_ids=None):
        """Load the latest snapshot per ID offline; never fall back on corruption.

        Outer alignment retains every date and missing value. Eligibility for
        financial calculations remains the responsibility of each analysis.
        """
        self._mode = None
        ids = self.series_ids if series_ids is None else _series_ids(series_ids)
        start = exact_date(start) if start is not None else None
        end = exact_date(end) if end is not None else None
        if start is not None and end is not None and start > end:
            raise ValueError("Start must be on or before end.")
        columns, series_metadata, snapshot_dates = [], {}, {}
        for series_id in ids:
            snapshot_date, path = self._latest_snapshot(series_id)
            try:
                data = load_observations(path)
                if list(data.columns) != [series_id]:
                    raise ValueError("Snapshot must contain exactly its named series ID.")
                info = deepcopy(data.attrs["metadata"][series_id])
                retrieved = pd.Timestamp(info["retrieved_at_utc"])
                if retrieved.tz_convert("UTC").strftime("%Y%m%d") != snapshot_date:
                    raise ValueError("Filename date differs from the UTC retrieval date.")
            except (ValueError, KeyError, TypeError, OSError) as exc:
                raise ValueError(f"{series_id}: invalid snapshot {path.name}: {exc}") from exc
            columns.append(data[series_id])
            series_metadata[series_id] = info
            snapshot_dates[series_id] = snapshot_date
        combined = pd.concat(columns, axis=1).sort_index().loc[start:end]
        if combined.empty:
            raise ValueError("No observations within the requested date range.")
        combined.attrs["metadata"] = series_metadata
        data = self._accept(combined, "file", snapshot_dates)
        if len(set(snapshot_dates.values())) > 1:
            from bondview.labels import load_labels

            labels = load_labels()["data"]["fred"]
            warnings.warn(labels["mismatch"].format(
                dates="\n".join(f"{s}: {d}" for s, d in snapshot_dates.items()),
            ), UserWarning, stacklevel=2)
        return data

    def save(self):
        """Save the current download without replacing any existing snapshot.

        Validate and serialize all files in a temporary staging directory first.
        Hard links publish complete files exclusively; a failure removes only
        files published by this call, leaving all existing snapshots untouched.
        Per-series leading/trailing missing padding is trimmed; internal gaps remain.
        """
        if self._mode != "download":
            raise RuntimeError("Saving is allowed only after downloading FRED data.")
        data = self.validate()
        paths = {
            s: self.path / f"{s}_{pd.Timestamp(self._metadata[s]['retrieved_at_utc']).tz_convert('UTC').strftime('%Y%m%d')}.csv"
            for s in data.columns
        }
        for path in paths.values():
            if os.path.lexists(path):
                raise FileExistsError(f"Snapshot already exists; refusing to overwrite: {path}")
        self.path.mkdir(parents=True, exist_ok=True)
        created = []
        with TemporaryDirectory(prefix=".fred-", dir=self.path) as staging:
            for series_id, path in paths.items():
                metadata = {series_id: deepcopy(self._metadata[series_id])}
                series_data = data[[series_id]]
                valid = series_data[series_id].dropna()
                if valid.empty:
                    raise ValueError(f"{series_id}: cannot save a snapshot with no nonmissing observations.")
                # Exclude NaN padding introduced by aligning unrelated series,
                # but keep missing observations within this series' valid range.
                series_data = series_data.loc[valid.index[0]:valid.index[-1]]
                save_observations(series_data, Path(staging) / path.name, metadata=metadata)
            try:
                for path in paths.values():
                    os.link(Path(staging) / path.name, path)
                    created.append(path)
            except OSError:
                for path in created:
                    path.unlink()
                raise
        return paths

    def report(self, *, series_ids=None, labels_path=None):
        """Summarize nonmissing counts, or display v2 metadata without CSV comment prefixes.

        Headers are generated from the current per-ID metadata, including data
        retrieved but not yet saved. No CSV observation rows are printed.
        """
        from bondview.labels import load_labels

        data = self.validate()
        if series_ids is not None:
            ids = _series_ids([series_ids] if isinstance(series_ids, str) else series_ids)
            unavailable = set(ids) - set(data.columns)
            if unavailable:
                raise ValueError(f"Series IDs not present in current observations: {sorted(unavailable)}")
            for i, series_id in enumerate(ids):
                if i:
                    print()
                print(
                    "".join(
                        line.removeprefix("# ")
                        for line in _metadata_header(series_id, self._metadata[series_id])
                    ),
                    end="",
                )
            return

        labels = load_labels(labels_path)["data"]["fred"]
        print(labels["summary"].format(mode=self._mode))
        print(labels["summary_columns"])
        for series_id, count in data.count().items():
            print(labels["summary_row"].format(series_id=series_id, count=int(count)))
        complete_count = int(data.notna().all(axis=1).sum())
        print(labels["common"].format(count=complete_count))
