"""FRED Treasury yields and a self-describing, offline JSON file format.

Values are percent (4.0 means 4%, not 0.04). Missing observations remain NaN
in memory and null on disk. No fill, resampling, or date substitution occurs.
"""

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
FORMAT = "bondview.fred_observations.v1"
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


def validate_observations(data: pd.DataFrame) -> pd.DataFrame:
    """Validate the shared representation and return a sorted copy."""
    if not isinstance(data.index, pd.DatetimeIndex) or data.empty:
        raise ValueError("Observations need a nonempty DatetimeIndex.")
    if data.index.hasnans or data.index.has_duplicates:
        raise ValueError("Observation dates must be present and unique.")
    for value in data.index:
        exact_date(value)
    metadata = data.attrs.get("metadata", {})
    series = metadata.get("series", {})
    if not series or set(data.columns) != set(series):
        raise ValueError("Series columns must match the metadata series IDs.")
    for series_id in data.columns:
        if not isinstance(series_id, str) or not re.fullmatch(r"[A-Z0-9_]+", series_id):
            raise ValueError("Invalid series ID.")
        if series[series_id].get("units") != "Percent":
            raise ValueError(f"{series_id}: units must explicitly be Percent.")
        if not pd.api.types.is_numeric_dtype(data[series_id]) or pd.api.types.is_bool_dtype(data[series_id]):
            raise ValueError(f"{series_id}: observations must be numeric or missing.")
        if np.isinf(data[series_id].to_numpy(dtype=float)).any():
            raise ValueError("Infinite observations are invalid.")
    if not metadata.get("source") or not metadata.get("retrieved_at_utc"):
        raise ValueError("Source and retrieval timestamp metadata are required.")
    timestamp = pd.Timestamp(metadata["retrieved_at_utc"])
    if pd.isna(timestamp) or timestamp.tz is None:
        raise ValueError("Retrieval timestamp must include its timezone.")
    return data.sort_index().copy()


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
    start="2024-01-01", end="2025-01-31", *, api_key=None,
    env_path=None, series_ids=SERIES,
) -> pd.DataFrame:
    """Download untransformed daily percent observations.

    Prefer an explicit key, FRED_API_KEY in the environment, then env_path's
    .env key. Without a key, use FRED's public graph CSV for the three known
    Treasury series. Other percent series can use the API with a key.
    This is a retrieval-time snapshot, not a point-in-time vintage database.
    """
    start, end = exact_date(start), exact_date(end)
    if start > end:
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
            if info["units"] != "Percent" or info["frequency_short"] != "D":
                raise ValueError(f"{series_id}: expected daily Percent observations.")
            payload = _api_json(
                "series/observations", key, series_id=series_id,
                observation_start=str(start.date()), observation_end=str(end.date()),
                units="lin", limit=100000,
            )
            if int(payload["count"]) != len(payload["observations"]):
                raise ValueError("FRED response was truncated; request a shorter period.")
            observations = payload["observations"]
            columns.append(pd.Series(
                [np.nan if row["value"] == "." else float(row["value"]) for row in observations],
                index=pd.DatetimeIndex([row["date"] for row in observations]),
                name=series_id, dtype=float,
            ))
            series_metadata[series_id] = {
                "units": info["units"], "frequency": info["frequency_short"],
                "title": info["title"], "last_updated": info["last_updated"],
                "realtime_start": payload.get("realtime_start"),
                "realtime_end": payload.get("realtime_end"),
                "source_url": f"https://fred.stlouisfed.org/series/{series_id}",
            }
        data = pd.concat(columns, axis=1)
        transport = "FRED API; untransformed daily observations"
    else:
        if not set(ids).issubset(SERIES):
            raise ValueError("An API key is required for series outside DGS2/DGS10/DGS30.")
        url = "https://fred.stlouisfed.org/graph/fredgraph.csv?" + urlencode({"id": ",".join(ids)})
        raw = pd.read_csv(StringIO(_read_url(url).decode("utf-8")), na_values=["."])
        if set(raw.columns) != {"observation_date", *ids}:
            raise ValueError("Unexpected FRED CSV columns.")
        raw.index = pd.DatetimeIndex([exact_date(d) for d in raw.pop("observation_date")])
        data = raw.apply(pd.to_numeric, errors="raise")
        # Public graph requests can return the full available history. Bound it locally.
        data = data.loc[(data.index >= start) & (data.index <= end)]
        series_metadata = {s: {
            "units": "Percent", "frequency": "D",
            "source_url": f"https://fred.stlouisfed.org/series/{s}",
        } for s in ids}
        transport = "FRED public graph CSV; known H.15 daily Percent series"
    data.index.name = "date"
    data.attrs["metadata"] = {
        "source": "FRED / Federal Reserve H.15" if set(ids).issubset(SERIES) else "FRED",
        "transport": transport,
        "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
        "requested_start": str(start.date()), "requested_end": str(end.date()),
        "series": series_metadata,
        "missing_policy": "No filling or date substitution; null means unavailable.",
        "availability": "Known at retrieval; historical release availability is not reconstructed.",
        "vintage": "Retrieval-time snapshot; source observations may be revised.",
    }
    return validate_observations(data)


def save_observations(data: pd.DataFrame, path) -> Path:
    """Save one portable JSON file with metadata and explicit missing values."""
    data = validate_observations(data)
    rows = [{"date": str(day.date()), **{
        s: None if pd.isna(row[s]) else float(row[s]) for s in data.columns
    }} for day, row in data.iterrows()]
    payload = {"format": FORMAT, "metadata": data.attrs["metadata"], "observations": rows}
    path = Path(path).expanduser()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    return path


def load_observations(path) -> pd.DataFrame:
    """Load the documented JSON format offline, never contacting FRED."""
    try:
        def reject_constant(value):
            raise ValueError(f"Invalid JSON numeric constant: {value}; use null for missing data.")
        payload = json.loads(
            Path(path).expanduser().read_text(encoding="utf-8"), parse_constant=reject_constant,
        )
        if payload["format"] != FORMAT:
            raise ValueError("Unsupported observation file format.")
        rows = payload["observations"]
        ids = list(payload["metadata"]["series"])
        if not rows or any(set(row) != {"date", *ids} for row in rows):
            raise ValueError("Each observation must have date and every declared series column.")
        for row in rows:
            if any(row[s] is not None and (isinstance(row[s], bool) or not isinstance(row[s], (int, float))) for s in ids):
                raise ValueError("Values must be JSON numbers or null.")
        data = pd.DataFrame(rows)
        data.index = pd.DatetimeIndex([exact_date(d) for d in data.pop("date")], name="date")
        data = data.astype(float)
        data.attrs["metadata"] = payload["metadata"]
        return validate_observations(data)
    except (KeyError, TypeError, AttributeError, OverflowError) as error:
        raise ValueError("Malformed observation file or metadata.") from error
