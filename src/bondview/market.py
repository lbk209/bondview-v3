"""Lightweight notebook facade; selections and results are explicit values."""

from dataclasses import dataclass

import pandas as pd

from bondview.analysis.treasury_curve import analyze_curve, analyze_kw_decomposition


@dataclass
class CurveResult:
    """Stored Analysis 1A output, independently accessible as a DataFrame."""

    data: pd.DataFrame

    def show(self, *, labels_path=None):
        from bondview.presentation.treasury_curve import show_curve_results

        return show_curve_results(self.data, labels_path=labels_path)


@dataclass
class DecompositionResult:
    """Stored Analysis 1B paths; display never recomputes the decomposition."""

    paths: dict[str, pd.DataFrame]

    def show(self, *, labels_path=None, width=1200, height=600):
        from bondview.plotting.treasury_curve import plot_kw_comparison

        figure = plot_kw_comparison(self.paths, labels_path=labels_path, width=width, height=height)
        figure.show()
        return figure


class TreasuryMarketAnalysis:
    """Analyze supplied observations without current-result or selection state.

    Observations remain explicit source data. Each computation reads them at
    call time and produces a separate result. KW inputs are supplied to 1B.
    """

    def __init__(self, observations):
        self.observations = observations

    def show_history(self, start, end, *, labels_path=None, metadata=None):
        from bondview.plotting.treasury_curve import show_yield_history

        return show_yield_history(
            self.observations, start, end, labels_path=labels_path, metadata=metadata,
        )

    def curve(self, start, end, *, yield_change_tolerance_bp=0.0,
              slope_tolerance_bp=0.0, metadata=None):
        return CurveResult(analyze_curve(
            self.observations, start, end, slope_tolerance_bp,
            yield_change_tolerance_bp=yield_change_tolerance_bp, metadata=metadata,
        ))

    def decomposition(self, kw_observations, start, end, *, metadata=None):
        return DecompositionResult(analyze_kw_decomposition(
            kw_observations, start, end, metadata=metadata,
        ))

    def scenarios(self, *, condition_tenor, lower_bp, upper_bp, horizon_months=6,
                  sampling="monthly", reference_start=None, reference_end=None, metadata=None):
        from bondview.analysis.scenarios import build_conditional_scenarios

        return build_conditional_scenarios(
            self.observations, condition_tenor=condition_tenor, lower_bp=lower_bp,
            upper_bp=upper_bp, horizon_months=horizon_months, sampling=sampling,
            reference_start=reference_start, reference_end=reference_end, metadata=metadata,
        )
