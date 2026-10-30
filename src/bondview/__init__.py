"""Dated market observations and fixed-income analysis for Bondview."""

from bondview.analysis.scenarios import ScenarioSet, build_conditional_scenarios

__all__ = ["TreasuryMarketAnalysis", "CurveResult", "DecompositionResult",
           "ScenarioSet", "build_conditional_scenarios"]


def __getattr__(name):
    # Numerical scenario consumers need neither the facade nor its 1A/1B imports.
    if name in ("TreasuryMarketAnalysis", "CurveResult", "DecompositionResult"):
        from bondview import market

        return getattr(market, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
