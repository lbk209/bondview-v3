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
from urllib.parse import urlencode
from urllib.request import urlopen

from dotenv import dotenv_values
import numpy as np
import pandas as pd

SERIES = ("DGS2", "DGS10", "DGS30")
FORMAT = "bondview.fred_observations.csv.v1"
API_BASE = "https://api.stlouisfed.org/fred/"


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
        if not isinstance(series_id, str) or not re.fullmatch(r"[A-Z0-9_]+", series_id):
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
    if not isinstance(metadata.get("source"), str) or not metadata["source"].strip():
        raise ValueError("Source metadata is required.")
    if not isinstance(metadata.get("retrieved_at_utc"), str):
        raise ValueError("Retrieval timestamp metadata is required.")
    timestamp = pd.Timestamp(metadata["retrieved_at_utc"])
    if pd.isna(timestamp) or timestamp.tz is None:
        raise ValueError("Retrieval timestamp must include its timezone.")
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

    ids = tuple(series_ids)
    if not ids or len(set(ids)) != len(ids) or any(
        not isinstance(s, str) or not re.fullmatch(r"[A-Z0-9_]+", s) for s in ids
    ):
        raise ValueError("Provide unique valid FRED series IDs.")

    key = api_key or os.getenv("FRED_API_KEY")
    if not key and env_path is not None:
        key = dotenv_values(env_path).get("FRED_API_KEY")

    series_metadata = {}

    if key:
        columns = []

        for series_id in ids:
            info = _api_json("series", key, series_id=series_id)["seriess"][0]

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
    """Manage one local snapshot and independent provenance."""

    def __init__(self, path, *, env_path=None, series_ids=SERIES):
        self.path = Path(path).expanduser()
        self.env_path = env_path
        self.series_ids = tuple(series_ids)
        self.observations = None
        self._metadata = {}
        self._mode = None

    @property
    def metadata(self):
        """Independent defensive copy, available even if DataFrame attrs are lost."""
        return deepcopy(self._metadata)

    def _accept(self, data):
        data = validate_observations(data)
        self._metadata = deepcopy(data.attrs["metadata"])
        self.observations = data
        return data

    def validate(self):
        return validate_observations(self.observations, self._metadata)

    def download(self, start=None, end=None, *, api_key=None):
        self._mode = None

        data = self._accept(download_fred(
            start, end, api_key=api_key, env_path=self.env_path,
            series_ids=self.series_ids,
        ))

        self._mode = "download"
        return data

    def load(self, start=None, end=None):
        # Read the local snapshot without network access.
        self._mode = None
        data = load_observations(self.path)

        start = exact_date(start) if start is not None else None
        end = exact_date(end) if end is not None else None

        if start is not None and end is not None and start > end:
            raise ValueError("Start must be on or before end.")

        metadata = deepcopy(data.attrs["metadata"])

        if start is not None:
            data = data.loc[data.index >= start]
        if end is not None:
            data = data.loc[data.index <= end]

        if data.empty:
            raise ValueError("No observations within the requested date range.")

        data.attrs["metadata"] = metadata
        data = self._accept(data)

        self._mode = "file"
        return data

    def save(self):
        if self._mode != "download":
            raise RuntimeError(
                "Saving is allowed only after downloading FRED data."
            )

        return save_observations(
            self.observations, self.path, metadata=self._metadata,
        )

    def load_or_download(self, mode, start=None, end=None, *, api_key=None):
        if mode == "file":
            return self.load(start, end)

        if mode == "download":
            data = self.download(start, end, api_key=api_key)
            self.save()
            return data

        raise ValueError('DATA_MODE must be "download" or "file".')

    def report(self, *, labels_path=None):
        """Print provenance, coverage and missing counts without exposing keys."""
        from bondview.labels import load_labels

        labels = load_labels(labels_path)["data"]["fred"]
        data = self.validate()

        print(labels["summary"].format(
            source=self._metadata["source"],
            retrieved=self._metadata["retrieved_at_utc"],
            start=data.index.min().date(),
            end=data.index.max().date(),
            rows=len(data),
            path=self.path,
        ))

        for series_id, info in self._metadata["series"].items():
            print(labels["series"].format(
                series_id=series_id,
                units=info["units"],
                frequency=info["frequency"],
                missing=int(data[series_id].isna().sum()),
            ))

        print(labels["snapshot"])
