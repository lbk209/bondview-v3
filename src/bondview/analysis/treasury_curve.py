"""Exact-date Treasury calculations with stable IDs, independent of terminology.

Yield levels are percent; spread levels and all changes are basis points.
"""

import math

import pandas as pd

from bondview.data.fred import SERIES, exact_date, validate_treasury_observations

# Round floating-point cancellation only, far below source quotation precision.
NUMERICAL_DECIMALS = 10
SEGMENTS = (("DGS2", "DGS10"), ("DGS10", "DGS30"))


def _bp(value):
    return round(float(value) * 100, NUMERICAL_DECIMALS)


def _direction(value):
    if pd.isna(value):
        return "unavailable"
    return "rose" if value > 0 else "fell" if value < 0 else "unchanged"


def classify_segment(short_change_bp, long_change_bp, slope_tolerance_bp=0.0):
    """Classify signs and slope separately, preserving baseline conventions.

    Tolerance applies inclusively only to slope. Unequal tenor changes never
    become parallel shifts. Missing inputs have no substituted classification.
    Movement IDs identify the convention; short/long directions remain explicit.
    """
    if not math.isfinite(slope_tolerance_bp) or slope_tolerance_bp < 0:
        raise ValueError("Slope tolerance must be finite and nonnegative (bp).")
    if pd.isna(short_change_bp) or pd.isna(long_change_bp):
        return {"slope": "unavailable", "short_direction": "unavailable",
                "long_direction": "unavailable", "movement": "unavailable"}
    if not all(math.isfinite(v) for v in (short_change_bp, long_change_bp)):
        raise ValueError("Yield changes must be finite or missing.")
    short, long = (round(float(v), NUMERICAL_DECIMALS) for v in (short_change_bp, long_change_bp))
    delta = round(long - short, NUMERICAL_DECIMALS)
    slope = "unchanged" if abs(delta) <= slope_tolerance_bp else "steepening" if delta > 0 else "flattening"
    if short == long:
        movement = "unchanged" if short == 0 else "parallel_up" if short > 0 else "parallel_down"
    elif short * long < 0:
        movement = "twist"
    elif short > 0 and long > 0:
        movement = "bear"
    elif short < 0 and long < 0:
        movement = "bull"
    else:
        movement = "short_only" if long == 0 else "long_only"
    return {"slope": slope, "short_direction": _direction(short),
            "long_direction": _direction(long), "movement": movement}


def _configuration(spread):
    if pd.isna(spread):
        return "unavailable"
    return "upward" if spread > 0 else "inverted" if spread < 0 else "flat"


def analyze_curve(data, start, end, slope_tolerance_bp=0.0, *, metadata=None) -> pd.DataFrame:
    """Return five structured rows, preserving available endpoints independently.

    Row IDs and categorical values are stable identifiers. Missing dates,
    including weekends and dates outside coverage, remain unavailable. Explicit
    provenance may be supplied when DataFrame attrs are absent.
    """
    data = validate_treasury_observations(data, metadata)
    classify_segment(0, 0, slope_tolerance_bp)
    start, end = exact_date(start), exact_date(end)
    if start > end:
        raise ValueError("Selected start must be on or before end.")
    endpoints = data.reindex([start, end])
    initial, final = endpoints.iloc[0], endpoints.iloc[1]
    changes = {s: _bp(final[s] - initial[s]) for s in SERIES}
    rows = []
    for s in SERIES:
        rows.append({"measure": s, "start": initial[s], "end": final[s],
                     "level_unit": "%", "change_bp": changes[s],
                     "configuration_start": "not_applicable", "configuration_end": "not_applicable",
                     "movement": _direction(changes[s]), "slope": "not_applicable",
                     "short_direction": "not_applicable", "long_direction": "not_applicable"})
    for short, long in SEGMENTS:
        a, b = _bp(initial[long] - initial[short]), _bp(final[long] - final[short])
        rows.append({"measure": f"{long}_{short}", "start": a, "end": b,
                     "level_unit": "bp", "change_bp": round(b - a, NUMERICAL_DECIMALS),
                     "configuration_start": _configuration(a), "configuration_end": _configuration(b),
                     **classify_segment(changes[short], changes[long], slope_tolerance_bp)})
    result = pd.DataFrame(rows).set_index("measure")
    result.attrs.update(start=str(start.date()), end=str(end.date()), slope_tolerance_bp=slope_tolerance_bp)
    return result
