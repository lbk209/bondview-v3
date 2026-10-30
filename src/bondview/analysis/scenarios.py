"""Observed conditional joint Treasury changes, independent of KW and plotting.

Monthly starts are the last complete observation in each calendar month;
daily starts are every complete observation. Add calendar months to the actual
start (day clipped by pandas at month end). A matured target must be within the
effective reference history. Match the last complete date on/before that target
in its calendar month, or skip the window if no such date exists. No values are
filled. Partial/incomplete months and gaps can shorten or exclude intervals;
actual endpoints, target dates, elapsed days and exclusions remain inspectable.
"""

from copy import deepcopy
from dataclasses import dataclass
import math
from numbers import Integral, Real

import pandas as pd

from bondview.data.fred import SERIES, exact_date, validate_treasury_observations

CHANGE_COLUMNS = tuple(f"{s}_change_bp" for s in SERIES)
ENDPOINT_CONVENTION = "last_complete_on_or_before_target_in_target_month"
START_CONVENTIONS = {"monthly": "last_complete_observation_per_calendar_month",
                     "daily": "every_complete_observation"}


@dataclass
class ScenarioSet:
    """Reusable joint vectors plus structured construction/provenance metadata.

    `scenarios` retains whole observed vectors; marginal `summary()` rows are
    descriptive, never additional joint scenarios or forecast probabilities.
    No facade or presentation import is needed to calculate or consume these.
    """

    scenarios: pd.DataFrame
    metadata: dict

    def summary(self):
        """Return per-factor min/P10/median/P90/max in bp (NaN for empty sets)."""
        values = self.scenarios.loc[:, list(CHANGE_COLUMNS)]
        result = values.quantile([0, .1, .5, .9, 1]).T
        result.index = pd.Index(SERIES, name="tenor")
        result.columns = ["minimum", "P10", "median", "P90", "maximum"]
        return result

    def show_summary(self, *, labels_path=None):
        from bondview.presentation.scenarios import show_scenario_summary

        return show_scenario_summary(self, labels_path=labels_path)

    def show_plot(self, *, labels_path=None):
        from bondview.plotting.scenarios import plot_scenarios

        figure = plot_scenarios(self, labels_path=labels_path)
        figure.show()
        return figure


def _empty_scenarios():
    return pd.DataFrame({
        "scenario_id": pd.Series(dtype="str"),
        "start_date": pd.Series(dtype="datetime64[ns]"),
        "target_end_date": pd.Series(dtype="datetime64[ns]"),
        "end_date": pd.Series(dtype="datetime64[ns]"),
        "elapsed_days": pd.Series(dtype="int64"),
        **{column: pd.Series(dtype="float64") for column in CHANGE_COLUMNS},
    })


def build_conditional_scenarios(
    observations, *, condition_tenor, lower_bp, upper_bp, horizon_months=6,
    sampling="monthly", reference_start=None, reference_end=None, metadata=None,
) -> ScenarioSet:
    """Select complete same-interval vectors under inclusive bp bounds.

    Valid empty selections retain a typed schema and counts. No complete
    reference observations is instead an input error. IDs identify historical
    endpoints and are stable across conditioning bounds, sampling and row order.
    Input metadata must satisfy the existing daily Percent Treasury contract.
    """
    if condition_tenor not in ("DGS2", "DGS10"):
        raise ValueError("condition_tenor must be DGS2 or DGS10.")
    if any(isinstance(v, bool) or not isinstance(v, Real) or not math.isfinite(v)
           for v in (lower_bp, upper_bp)) or lower_bp > upper_bp:
        raise ValueError("Bounds must be finite numerical bp values with lower_bp <= upper_bp.")
    if isinstance(horizon_months, bool) or not isinstance(horizon_months, Integral) or horizon_months <= 0:
        raise ValueError("horizon_months must be a positive integer calendar-month horizon.")
    if sampling not in START_CONVENTIONS:
        raise ValueError("sampling must be monthly or daily.")
    horizon_months = int(horizon_months)
    data = validate_treasury_observations(observations, metadata)
    requested_start = exact_date(reference_start) if reference_start is not None else None
    requested_end = exact_date(reference_end) if reference_end is not None else None
    if requested_start is not None and requested_end is not None and requested_start > requested_end:
        raise ValueError("reference_start must be on or before reference_end.")
    history = data.dropna(subset=list(SERIES))
    if history.empty:
        raise ValueError("No complete DGS2/DGS10/DGS30 observations in the reference history.")
    start_bound = requested_start if requested_start is not None else history.index[0]
    end_bound = requested_end if requested_end is not None else history.index[-1]
    selected = data.loc[start_bound:end_bound, list(SERIES)]
    complete = selected.dropna(subset=list(SERIES))
    if complete.empty:
        raise ValueError("No complete DGS2/DGS10/DGS30 observations in the reference history.")
    dates = complete.index
    starts = (dates if sampling == "daily" else
              dates.to_series().groupby(dates.to_period("M")).last().array)
    rows = []
    immature = unmatched = 0
    for start in starts:
        target = start + pd.DateOffset(months=horizon_months)
        if target > dates[-1]:
            immature += 1
            continue
        position = dates.searchsorted(target, side="right") - 1
        end = dates[position]
        if end.to_period("M") != target.to_period("M"):
            unmatched += 1
            continue
        # Round floating cancellation below source quotation precision only,
        # consistently with Analysis 1A; no display rounding enters conditioning.
        changes = ((complete.loc[end] - complete.loc[start]) * 100).round(10)
        rows.append({
            "scenario_id": f"UST_{start:%Y%m%d}_{end:%Y%m%d}",
            "start_date": start, "target_end_date": target, "end_date": end,
            "elapsed_days": (end - start).days,
            **{column: float(changes[s]) for s, column in zip(SERIES, CHANGE_COLUMNS)},
        })
    eligible = pd.DataFrame(rows) if rows else _empty_scenarios()
    condition = eligible[f"{condition_tenor}_change_bp"]
    scenarios = eligible.loc[condition.between(lower_bp, upper_bp, inclusive="both")].reset_index(drop=True)
    info = {
        "schema_version": "bondview.scenario_set.v1",
        "scenario_type": "observed_historical_joint_yield_changes",
        "factors": list(SERIES), "input_units": "Percent", "change_units": "bp",
        "condition": {"tenor": condition_tenor, "lower_bp": float(lower_bp),
                      "upper_bp": float(upper_bp), "inclusive": True},
        "horizon_months": horizon_months, "sampling": sampling,
        "start_convention": START_CONVENTIONS[sampling],
        "endpoint_convention": ENDPOINT_CONVENTION,
        "target_convention": "actual_start_plus_calendar_months_clipped_at_month_end",
        "reference": {
            "requested_start": str(requested_start.date()) if requested_start is not None else None,
            "requested_end": str(requested_end.date()) if requested_end is not None else None,
            "effective_start": str(dates[0].date()), "effective_end": str(dates[-1].date()),
        },
        "counts": {
            "reference_rows": len(selected), "complete_observations": len(complete),
            "incomplete_rows_excluded": len(selected) - len(complete),
            "sampled_starts": len(starts), "immature_targets_excluded": immature,
            "unmatched_target_months_excluded": unmatched,
            "eligible_windows": len(eligible), "selected_scenarios": len(scenarios),
        },
        "provenance": {s: deepcopy(data.attrs["metadata"][s]) for s in SERIES},
        "missing_policy": "Complete common observation dates only; no fill, interpolation or averaging.",
        "overlapping_windows": True,
        "interpretation": "Descriptive overlapping historical scenarios, not independent event frequencies or forecast probabilities.",
        "quantile_method": "linear interpolation (pandas default); marginal summaries only",
    }
    return ScenarioSet(scenarios, info)
