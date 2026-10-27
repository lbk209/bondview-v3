"""Small reusable helpers shared across Bondview analyses."""

from datetime import date, datetime

import pandas as pd


def select_date_range(data, start=None, end=None, *, date_format="%Y-%m-%d"):
    """Return rows in the inclusive date range; preserve missing observations.

    None leaves the corresponding boundary open. Date strings use date_format.
    The input must have an ascending DatetimeIndex; this function never sorts,
    fills, or changes data values.
    """
    if not isinstance(data, pd.DataFrame) or not isinstance(data.index, pd.DatetimeIndex):
        raise ValueError("Data must be a DataFrame with a DatetimeIndex.")
    if data.index.hasnans or not data.index.is_monotonic_increasing:
        raise ValueError("Date index must have valid dates in ascending order.")

    def parse_boundary(value):
        if value is None:
            return None
        if isinstance(value, str):
            try:
                parsed = pd.to_datetime(value, format=date_format, exact=True)
            except (ValueError, TypeError) as exc:
                raise ValueError(f"Invalid date: {value!r} (expected {date_format}).") from exc
        elif isinstance(value, (date, datetime, pd.Timestamp)):
            parsed = pd.Timestamp(value)
        else:
            raise ValueError("Date boundaries must be calendar dates or formatted strings.")
        if pd.isna(parsed):
            raise ValueError("Date boundaries cannot be missing.")
        return parsed

    start, end = parse_boundary(start), parse_boundary(end)
    if start is not None and end is not None and start > end:
        raise ValueError("Start must be on or before end.")
    return data.loc[start:end]
