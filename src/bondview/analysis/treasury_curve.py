"""Exact-date Treasury endpoint comparisons; yields in percent, spreads in bp."""

import math

import pandas as pd

from bondview.data.fred import SERIES, exact_date, validate_observations

# Round floating-point cancellation only, far below source quotation precision.
NUMERICAL_DECIMALS = 10


def _bp(value):
    return round(float(value) * 100, NUMERICAL_DECIMALS)


def _direction(value):
    if pd.isna(value):
        return "N/A"
    return "Yield rose" if value > 0 else "Yield fell" if value < 0 else "Yield unchanged"


def classify_segment(short_change_bp, long_change_bp, slope_tolerance_bp=0.0):
    """Keep underlying directions distinct from the net slope descriptor.

    Tolerance applies only to the slope, inclusively; yield directions still
    use their actual signs. One stationary tenor is described explicitly.
    Opposing-direction twist is a descriptive convention, not a universal
    exclusive taxonomy. A tolerated slope change is not called parallel unless
    the two changes are equal to numerical precision.
    """
    if not math.isfinite(slope_tolerance_bp) or slope_tolerance_bp < 0:
        raise ValueError("Slope tolerance must be finite and nonnegative (bp).")
    if pd.isna(short_change_bp) or pd.isna(long_change_bp):
        return {"slope": "N/A", "direction": "N/A", "movement": "N/A"}
    if not all(math.isfinite(v) for v in (short_change_bp, long_change_bp)):
        raise ValueError("Yield changes must be finite or missing.")
    short, long = (round(float(v), NUMERICAL_DECIMALS) for v in (short_change_bp, long_change_bp))
    delta = round(long - short, NUMERICAL_DECIMALS)
    slope = "Unchanged slope" if abs(delta) <= slope_tolerance_bp else "Steepening" if delta > 0 else "Flattening"
    direction = f"Short: {_direction(short).lower()}; long: {_direction(long).lower()}"
    if short == long:
        movement = "Unchanged yields" if short == 0 else "Parallel upward shift" if short > 0 else "Parallel downward shift"
    elif short * long < 0:
        movement = f"Opposing-direction twist {slope.lower()}"
    elif short > 0 and long > 0:
        movement = f"Bear {slope.lower()}"
    elif short < 0 and long < 0:
        movement = f"Bull {slope.lower()}"
    else:
        moving = "Short" if long == 0 else "Long"
        change = short if long == 0 else long
        movement = f"{moving} yield {'rose' if change > 0 else 'fell'}, other unchanged; {slope.lower()}"
    return {"slope": slope, "direction": direction, "movement": movement}


def _configuration(spread):
    if pd.isna(spread):
        return "N/A"
    return "Upward-sloping" if spread > 0 else "Inverted" if spread < 0 else "Flat"


def analyze_curve(data, start, end, slope_tolerance_bp=0.0) -> pd.DataFrame:
    """Return five rows, preserving every available endpoint independently.

    Missing dates (including weekends, holidays and dates outside loaded
    coverage) yield missing inputs, never replacement observations. Start and
    end may be equal; reverse intervals are rejected.
    """
    data = validate_observations(data)
    if not set(SERIES).issubset(data.columns):
        raise ValueError("Treasury analysis requires DGS2, DGS10 and DGS30 columns; use NaN for missing observations.")
    classify_segment(0, 0, slope_tolerance_bp)  # Validate parameter even with no data.
    start, end = exact_date(start), exact_date(end)
    if start > end:
        raise ValueError("Selected start must be on or before end.")
    endpoints = data.reindex([start, end])
    initial, final = endpoints.iloc[0], endpoints.iloc[1]
    changes = {s: _bp(final[s] - initial[s]) for s in SERIES}
    rows = []
    for s, label in zip(SERIES, ("2Y yield", "10Y yield", "30Y yield")):
        rows.append({"measure": label, "start": initial[s], "end": final[s],
                     "level_unit": "%", "change_bp": changes[s],
                     "configuration": "—", "movement": _direction(changes[s]),
                     "slope": "—", "direction": _direction(changes[s])})
    for short, long, label in (("DGS2", "DGS10", "10Y−2Y spread"), ("DGS10", "DGS30", "30Y−10Y spread")):
        a, b = _bp(initial[long] - initial[short]), _bp(final[long] - final[short])
        descriptor = classify_segment(changes[short], changes[long], slope_tolerance_bp)
        rows.append({"measure": label, "start": a, "end": b, "level_unit": "bp",
                     "change_bp": round(b - a, NUMERICAL_DECIMALS),
                     "configuration": f"{_configuration(a)} → {_configuration(b)}", **descriptor})
    result = pd.DataFrame(rows).set_index("measure")
    result.attrs.update(start=str(start.date()), end=str(end.date()), slope_tolerance_bp=slope_tolerance_bp)
    return result


def display_table(result) -> pd.DataFrame:
    """Format units and N/A at the presentation boundary, keeping numbers reusable."""
    rows = []
    for measure, row in result.iterrows():
        def level(value):
            if pd.isna(value):
                return "N/A"
            return f"{value:.2f}%" if row.level_unit == "%" else f"{value:+.2f} bp"
        rows.append({"Treasury measure": measure,
                     result.attrs["start"]: level(row.start),
                     # Distinct headings also handle the same-day case.
                     "End " + result.attrs["end"]: level(row.end),
                     "Change": "N/A" if pd.isna(row.change_bp) else f"{row.change_bp:+.2f} bp",
                     "Curve configuration": row.configuration,
                     "Movement / regime": row.movement})
    return pd.DataFrame(rows).set_index("Treasury measure")


def interpret_curve(result) -> str:
    """Describe observed concentration without inferring causes or ETF returns."""
    changes = result.iloc[:3].change_bp.dropna()
    if changes.empty:
        return "No tenor has both selected-date observations. Endpoint movements are unavailable; inspect the history and choose other dates if useful."
    statements = []
    for predicate, extreme, description in ((changes > 0, max, "upward"), (changes < 0, min, "downward")):
        subset = changes[predicate]
        if not subset.empty:
            value = extreme(subset)
            names = ", ".join(subset.index[subset == value].str.replace(" yield", ""))
            statements.append(f"Greatest {description} yield movement among available tenors: {names} ({value:+.2f} bp).")
    if not statements:
        statements.append("Available tenor yields were unchanged.")
    if len(changes) < 3:
        statements.append("This comparison is partial because some endpoint observations are unavailable.")
    statements.extend(f"{label}: {row.movement}." for label, row in result.iloc[3:].iterrows())
    statements.append("These are net endpoint movements, not the full path or a forecast. ETF rate-price effects depend on duration and other product characteristics.")
    return " ".join(statements)
