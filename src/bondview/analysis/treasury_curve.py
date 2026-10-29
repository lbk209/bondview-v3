"""Treasury changes over selected date ranges, independent of terminology.

Yield levels are percent; spread levels and all changes are basis points.
"""

import math

import pandas as pd

from bondview.data.fred import SERIES, validate_observations, validate_treasury_observations
from bondview.utils import select_date_range

# Round floating-point cancellation only, far below source quotation precision.
NUMERICAL_DECIMALS = 10
SEGMENTS = (("DGS2", "DGS10"), ("DGS10", "DGS30"))
KW_SERIES = {
    "2Y": ("THREEFY2", "THREEFYTP2"),
    "10Y": ("THREEFY10", "THREEFYTP10"),
}


def analyze_kw_decomposition(data, start, end, *, metadata=None):
    """Return a dated component path per maturity from daily Percent KW data.

    Only dates with all four KW observations qualify. Each path contains
    original levels (%) and cumulative changes (bp) from its first eligible
    observation within the inclusive selection. No missing values are filled.
    These model-fitted nominal zero-coupon quantities are not DGS forecasts.
    """
    data = validate_observations(data, metadata)
    required = [series for pair in KW_SERIES.values() for series in pair]
    if not set(required).issubset(data.columns):
        raise ValueError("KW decomposition requires THREEFY2, THREEFYTP2, THREEFY10 and THREEFYTP10.")
    for series in required:
        info = data.attrs["metadata"][series]
        if info["units"] != "Percent" or info["frequency"] != "D":
            raise ValueError(f"{series}: KW decomposition requires daily Percent observations.")
    selected = select_date_range(data, start, end).dropna(subset=required)
    if selected.empty:
        raise ValueError("No complete KW observations within the selected date range.")

    results = {}
    for maturity, (fitted, premium) in KW_SERIES.items():
        result = pd.DataFrame({
            "fitted_yield": selected[fitted],
            "expected_rate": selected[fitted] - selected[premium],
            "term_premium": selected[premium],
        })
        result["expected_change_bp"] = (result.expected_rate - result.expected_rate.iloc[0]) * 100
        result["premium_change_bp"] = (result.term_premium - result.term_premium.iloc[0]) * 100
        result["fitted_change_bp"] = result.expected_change_bp + result.premium_change_bp
        result.attrs["metadata"] = {s: data.attrs["metadata"][s] for s in (fitted, premium)}
        results[maturity] = result
    return results


def _bp(value):
    return round(float(value) * 100, NUMERICAL_DECIMALS)


def _validate_tolerance(value, name):
    if not math.isfinite(value) or value < 0:
        raise ValueError(f"{name} must be finite and nonnegative (bp).")


def _direction(value, tolerance_bp=0.0):
    if pd.isna(value):
        return "unavailable"
    return "rose" if value > tolerance_bp else "fell" if value < -tolerance_bp else "unchanged"


def classify_segment(
    short_change_bp, long_change_bp, slope_tolerance_bp=0.0, *,
    yield_change_tolerance_bp=0.0,
):
    """Describe material tenor movements and slope changes separately.

    Both tolerances are inclusive. A broadly unchanged segment takes precedence
    over an approximately parallel shift. Missing inputs are never substituted.
    Movement IDs remain independent of presentation terminology.
    """
    _validate_tolerance(slope_tolerance_bp, "Slope tolerance")
    _validate_tolerance(yield_change_tolerance_bp, "Yield-change tolerance")
    if pd.isna(short_change_bp) or pd.isna(long_change_bp):
        return {"slope": "unavailable", "short_direction": "unavailable",
                "long_direction": "unavailable", "movement": "unavailable"}
    if not all(math.isfinite(v) for v in (short_change_bp, long_change_bp)):
        raise ValueError("Yield changes must be finite or missing.")
    short, long = (round(float(v), NUMERICAL_DECIMALS) for v in (short_change_bp, long_change_bp))
    delta = round(long - short, NUMERICAL_DECIMALS)
    slope = ("unchanged" if abs(delta) <= slope_tolerance_bp else
             "steepening" if delta > 0 else "flattening")
    short_direction = _direction(short, yield_change_tolerance_bp)
    long_direction = _direction(long, yield_change_tolerance_bp)

    if short_direction == long_direction == "unchanged":
        movement = "unchanged"
    elif short_direction == long_direction and slope == "unchanged":
        movement = "parallel_up" if short_direction == "rose" else "parallel_down"
    elif {short_direction, long_direction} == {"rose", "fell"}:
        movement = "twist"
    elif short_direction == long_direction == "rose":
        movement = "bear"
    elif short_direction == long_direction == "fell":
        movement = "bull"
    else:
        movement = "short_only" if long_direction == "unchanged" else "long_only"

    return {"slope": slope, "short_direction": short_direction,
            "long_direction": long_direction, "movement": movement}


def _configuration(spread):
    if pd.isna(spread):
        return "unavailable"
    return "upward" if spread > 0 else "inverted" if spread < 0 else "flat"


def analyze_curve(
    data, start, end, slope_tolerance_bp=0.0, *,
    yield_change_tolerance_bp=0.0, metadata=None,
) -> pd.DataFrame:
    """Return five structured rows, preserving available endpoints independently.

    Start and end bound an inclusive interval. The first and last dates with
    any Treasury observation are used as effective endpoints. Each tenor still
    reports unavailable changes when either endpoint observation is missing.
    Explicit provenance may be supplied when DataFrame attrs are absent.
    """
    data = validate_treasury_observations(data, metadata)
    classify_segment(0, 0, slope_tolerance_bp,
                     yield_change_tolerance_bp=yield_change_tolerance_bp)
    selected = select_date_range(data, start, end)
    available = selected.dropna(how="all", subset=list(SERIES))
    if available.empty:
        raise ValueError("No Treasury observations within the selected date range.")
    start, end = available.index[0], available.index[-1]
    initial, final = available.iloc[0], available.iloc[-1]
    changes = {s: _bp(final[s] - initial[s]) for s in SERIES}
    rows = []
    for s in SERIES:
        rows.append({"measure": s, "start": initial[s], "end": final[s],
                     "level_unit": "%", "change_bp": changes[s],
                     "configuration_start": "not_applicable", "configuration_end": "not_applicable",
                     "movement": _direction(changes[s], yield_change_tolerance_bp), "slope": "not_applicable",
                     "short_direction": "not_applicable", "long_direction": "not_applicable"})
    for short, long in SEGMENTS:
        a, b = _bp(initial[long] - initial[short]), _bp(final[long] - final[short])
        rows.append({"measure": f"{long}_{short}", "start": a, "end": b,
                     "level_unit": "bp", "change_bp": round(b - a, NUMERICAL_DECIMALS),
                     "configuration_start": _configuration(a), "configuration_end": _configuration(b),
                     **classify_segment(
                         changes[short], changes[long], slope_tolerance_bp,
                         yield_change_tolerance_bp=yield_change_tolerance_bp,
                     )})
    result = pd.DataFrame(rows).set_index("measure")
    result.attrs.update(start=str(start.date()), end=str(end.date()),
                        slope_tolerance_bp=slope_tolerance_bp,
                        yield_change_tolerance_bp=yield_change_tolerance_bp)
    return result
