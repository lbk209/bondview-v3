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
FORMAT = "bondview.fred_observations.csv.v1"
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
    """Validate dates/numbers/provenance without assuming common units/frequency.

    Explicit metadata takes precedence over the compatibility copy in attrs.
    The shared outer date index may align different source frequencies; missing
    entries stay missing and no frequency is inferred from that combined index.
    """
    if not isinstance(data, pd.DataFrame) or not isinstance(data.index, pd.DatetimeIndex) or data.empty:
        raise ValueError("Observations need a nonempty DatetimeIndex.")
    if data.index.hasnans or data.index.has_duplicates or data.columns.has_duplicates:
        raise ValueError("Observation dates and series IDs must be present and unique.")
    for value in data.index:
        exact_date(value)
    metadata = data.attrs.get("metadata", {}) if metadata is None else metadata
    if not isinstance(metadata, dict) or not isinstance(metadata.get("series"), dict):
        raise ValueError("Series metadata is required.")
    series = metadata["series"]
    if not series or set(data.columns) != set(series):
        raise ValueError("Series columns must match the metadata series IDs.")
    for series_id in data.columns:
        if not isinstance(series_id, str) or not re.fullmatch(r"[A-Za-z0-9_]+", series_id):
            raise ValueError("Invalid series ID.")
        info = series[series_id]
        if not isinstance(info, dict) or any(
            not isinstance(info.get(field), str) or not info[field].strip()
            for field in ("units", "frequency")
        ):
            raise ValueError(f"{series_id}: explicit units and frequency are required.")
        if not pd.api.types.is_numeric_dtype(data[series_id]) or pd.api.types.is_bool_dtype(data[series_id]):
            raise ValueError(f"{series_id}: observations must be numeric or missing.")
        if np.isinf(data[series_id].to_numpy(dtype=float, na_value=np.nan)).any():
            raise ValueError("Infinite observations are invalid.")
        provenance = info.get("provenance", metadata)
        if (not isinstance(provenance, dict)
                or not isinstance(provenance.get("source"), str)
                or not provenance["source"].strip()):
            raise ValueError(f"{series_id}: source metadata is required.")
        if not isinstance(provenance.get("retrieved_at_utc"), str):
            raise ValueError(f"{series_id}: retrieval timestamp metadata is required.")
        timestamp = pd.Timestamp(provenance["retrieved_at_utc"])
        if pd.isna(timestamp) or timestamp.tz is None:
            raise ValueError("Retrieval timestamp must include its timezone.")
    if not isinstance(metadata.get("source"), str) or not metadata["source"].strip():
        raise ValueError("Source metadata is required.")
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
        info = data.attrs["metadata"]["series"][series_id]
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

    data.attrs["metadata"] = {
        "source": "FRED / Federal Reserve H.15" if set(ids).issubset(SERIES) else "FRED",
        "transport": transport,
        "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
        "requested_start": str(start.date()) if start is not None else None,
        "requested_end": str(end.date()) if end is not None else None,
        "series": series_metadata,
        "missing_policy": "No filling or date substitution; empty CSV fields mean unavailable.",
        "availability": "Known at retrieval; historical release availability is not reconstructed.",
        "vintage": "Retrieval-time snapshot; source observations may be revised.",
    }

    return validate_observations(data)


def save_observations(data: pd.DataFrame, path, *, metadata=None) -> Path:
    """Write CSV rows and JSON-encoded comment header values in a single file.

    Encoding each header value preserves nested per-series provenance without a
    sidecar. Observation values are CSV numbers, with empty fields for missing.
    """
    data = validate_observations(data, metadata)
    # Validate/encode headers before opening a potentially existing snapshot.
    headers = [f"# format: {json.dumps(FORMAT)}\n"]
    for key, value in data.attrs["metadata"].items():
        if not isinstance(key, str) or not re.fullmatch(r"[a-z_]+", key) or key == "format":
            raise ValueError("Invalid metadata header key.")
        headers.append(f"# {key}: {json.dumps(value, ensure_ascii=False, allow_nan=False)}\n")
    path = Path(path).expanduser()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as stream:
        stream.writelines(headers)
        data.to_csv(stream, index_label="date", date_format="%Y-%m-%d", na_rep="")
    return path


def load_observations(path) -> pd.DataFrame:
    """Read the self-contained CSV strictly offline; reject malformed rows."""
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
        raise ValueError("Unsupported observation file format; expected Bondview FRED CSV.")
    rows = list(csv.reader(StringIO(body)))
    if len(rows) < 2 or rows[0][0:1] != ["date"] or len(set(rows[0])) != len(rows[0]):
        raise ValueError("CSV requires date and unique series columns, plus observations.")
    if any(len(row) != len(rows[0]) for row in rows[1:]):
        raise ValueError("Every CSV row must contain every declared column.")
    dates = [exact_date(row[0]) for row in rows[1:]]
    for row in rows[1:]:
        for value in row[1:]:
            if value and (not re.fullmatch(r"[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?", value)
                          or not np.isfinite(float(value))):
                raise ValueError("CSV values must be finite numbers or empty fields.")
    # round_trip preserves the original binary float through its decimal CSV form.
    data = pd.read_csv(StringIO(body), index_col=0, float_precision="round_trip")
    data.index = pd.DatetimeIndex(dates, name="date")
    return validate_observations(data, metadata)


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
                provenance = deepcopy(data.attrs["metadata"])
                info = provenance.pop("series")[series_id]
                retrieved = pd.Timestamp(provenance["retrieved_at_utc"])
                if retrieved.tz_convert("UTC").strftime("%Y%m%d") != snapshot_date:
                    raise ValueError("Filename date differs from the UTC retrieval date.")
            except (ValueError, KeyError, TypeError, OSError) as exc:
                raise ValueError(f"{series_id}: invalid snapshot {path.name}: {exc}") from exc
            columns.append(data[series_id])
            series_metadata[series_id] = {**info, "provenance": provenance}
            snapshot_dates[series_id] = snapshot_date
        combined = pd.concat(columns, axis=1).sort_index().loc[start:end]
        if combined.empty:
            raise ValueError("No observations within the requested date range.")
        combined.attrs["metadata"] = {"source": "FRED snapshots", "series": series_metadata}
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
        snapshot_date = pd.Timestamp(self._metadata["retrieved_at_utc"]).tz_convert("UTC").strftime("%Y%m%d")
        paths = {s: self.path / f"{s}_{snapshot_date}.csv" for s in data.columns}
        for path in paths.values():
            if os.path.lexists(path):
                raise FileExistsError(f"Snapshot already exists; refusing to overwrite: {path}")
        self.path.mkdir(parents=True, exist_ok=True)
        created = []
        with TemporaryDirectory(prefix=".fred-", dir=self.path) as staging:
            for series_id, path in paths.items():
                metadata = deepcopy(self._metadata)
                metadata["series"] = {series_id: metadata["series"][series_id]}
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

    def report(self, *, labels_path=None):
        """Print per-series provenance and complete shared coverage, never keys."""
        from bondview.labels import load_labels

        labels = load_labels(labels_path)["data"]["fred"]
        data = self.validate()
        print(labels["summary"].format(
            series_ids=", ".join(data.columns), mode=self._mode,
            start=data.index.min().date(), end=data.index.max().date(),
            rows=len(data), path=self.path,
        ))
        for series_id, info in self._metadata["series"].items():
            valid = data[series_id].dropna()
            provenance = info.get("provenance", self._metadata)
            print(labels["series"].format(
                series_id=series_id, units=info["units"], frequency=info["frequency"],
                start=valid.index.min().date() if not valid.empty else labels["no_observations"],
                end=valid.index.max().date() if not valid.empty else labels["no_observations"],
                missing=int(data[series_id].isna().sum()),
                snapshot_date=self.snapshot_dates.get(series_id, labels["unsaved"]),
                source=provenance["source"], retrieved=provenance["retrieved_at_utc"],
            ))
            # All source fields are retained; report the relevant source context.
            print(labels["provenance"].format(details=json.dumps({
                **{k: v for k, v in provenance.items() if k not in ("series", "source", "retrieved_at_utc")},
                **{k: v for k, v in info.items() if k not in ("provenance", "units", "frequency")},
            }, ensure_ascii=False)))
        complete = data.dropna()
        if complete.empty:
            print(labels["no_common"])
        else:
            print(labels["common"].format(
                start=complete.index.min().date(), end=complete.index.max().date(), rows=len(complete),
            ))
        print(labels["snapshot"])
