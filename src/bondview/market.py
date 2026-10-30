"""User-facing Treasury market analyses.

Each entry point receives its own observations; no shared market instance is needed.
"""

from dataclasses import dataclass

import pandas as pd

from bondview.analysis.treasury_curve import analyze_curve, analyze_kw_decomposition
from bondview.data.fred import validate_treasury_observations


class CurveAnalysis:
    """Analysis 1A: inspect Treasury history, then analyze a selected interval.

    ``result`` contains the latest numerical curve-movement DataFrame, or None
    until the first successful analysis. The original observations are retained
    independently for history plots and subsequent date selections.
    """

    def __init__(self, observations, *, metadata=None):
        self.observations = observations
        self.metadata = metadata
        self.result: pd.DataFrame | None = None

    def show_history(self, start=None, end=None, *, labels_path=None):
        """Show the full available yield history by default, or a chosen range."""
        from bondview.plotting.treasury_curve import show_yield_history

        data = validate_treasury_observations(self.observations, self.metadata)
        if start is None:
            start = data.index.min()
        if end is None:
            end = data.index.max()
        return show_yield_history(
            data, start, end, labels_path=labels_path, metadata=self.metadata,
        )

    def analyze(self, start, end, *, formatted=True, labels_path=None,
                yield_change_tolerance_bp=0.0, slope_tolerance_bp=0.0):
        """Calculate movements once; show the formatted result or return raw data.

        In both modes ``result`` stores the latest calculated DataFrame.
        ``formatted=True`` displays the formatted table and interpretation;
        ``formatted=False`` returns the numerical DataFrame without displaying.
        """
        if not isinstance(formatted, bool):
            raise TypeError("formatted must be a bool.")

        result = analyze_curve(
            self.observations, start, end, slope_tolerance_bp,
            yield_change_tolerance_bp=yield_change_tolerance_bp,
            metadata=self.metadata,
        )
        self.result = result
        if not formatted:
            return result

        from bondview.presentation.treasury_curve import show_curve_results
        show_curve_results(result, labels_path=labels_path)
        return None


@dataclass
class DecompositionResult:
    """Stored Analysis 1B paths; display never recomputes the decomposition."""

    paths: dict[str, pd.DataFrame]

    def show(self, *, labels_path=None, width=1200, height=600):
        from bondview.plotting.treasury_curve import plot_kw_comparison

        figure = plot_kw_comparison(self.paths, labels_path=labels_path, width=width, height=height)
        figure.show()
        return figure


def curve(observations, *, metadata=None) -> CurveAnalysis:
    """Create an observation-bound Analysis 1A workflow."""
    return CurveAnalysis(observations, metadata=metadata)


def decomposition(kw_observations, start, end, *, metadata=None) -> DecompositionResult:
    """Calculate the 1B decomposition for the selected date interval."""
    return DecompositionResult(analyze_kw_decomposition(
        kw_observations, start, end, metadata=metadata,
    ))


def scenarios(observations, *, condition_tenor, lower_bp, upper_bp,
              horizon_months=6, sampling_step_observations=1,
              reference_start=None, reference_end=None, metadata=None):
    """Construct the same Analysis 1C joint historical scenario set."""
    from bondview.analysis.scenarios import build_conditional_scenarios

    return build_conditional_scenarios(
        observations, condition_tenor=condition_tenor, lower_bp=lower_bp,
        upper_bp=upper_bp, horizon_months=horizon_months,
        sampling_step_observations=sampling_step_observations,
        reference_start=reference_start, reference_end=reference_end,
        metadata=metadata,
    )
