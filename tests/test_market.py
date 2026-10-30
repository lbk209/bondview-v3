"""Facade equivalence, independent results and calculation-free display."""

import unittest
from unittest.mock import patch

import pandas as pd

from bondview import CurveResult, DecompositionResult, TreasuryMarketAnalysis
from bondview.analysis.treasury_curve import analyze_curve, analyze_kw_decomposition
from bondview.plotting.treasury_curve import plot_kw_comparison, plot_yield_history
from test_treasury_curve import example_frame
from test_kw_decomposition import kw_frame


class MarketTests(unittest.TestCase):
    def test_curve_equivalence_and_independent_results(self):
        data = example_frame()
        market = TreasuryMarketAnalysis(data)
        first = market.curve(*data.index, yield_change_tolerance_bp=5, slope_tolerance_bp=5)
        self.assertIsInstance(first, CurveResult)
        expected = analyze_curve(data, *data.index, yield_change_tolerance_bp=5, slope_tolerance_bp=5)
        pd.testing.assert_frame_equal(first.data, expected)
        second = market.curve(data.index[0], data.index[0])
        self.assertEqual(second.data.change_bp.tolist(), [0]*5)
        pd.testing.assert_frame_equal(first.data, expected)
        data.iloc[0, 0] = 99
        with patch('bondview.market.analyze_curve', side_effect=AssertionError('recalculation')), \
             patch('IPython.display.display') as display:
            first.show()
            first.show()
        self.assertEqual(display.call_count, 4)
        pd.testing.assert_frame_equal(first.data, expected)
        self.assertEqual(set(vars(market)), {'observations'})

    def test_decomposition_independent_of_curve_and_plot_equivalent(self):
        market = TreasuryMarketAnalysis(None)  # No Treasury calculation/data needed for 1B.
        data = kw_frame()
        result = market.decomposition(data, *data.index[[0,-1]])
        self.assertIsInstance(result, DecompositionResult)
        expected = analyze_kw_decomposition(data, *data.index[[0,-1]])
        for tenor in expected:
            pd.testing.assert_frame_equal(result.paths[tenor], expected[tenor])
        data.iloc[:] = 99
        with patch('bondview.market.analyze_kw_decomposition', side_effect=AssertionError('recalculation')), \
             patch('plotly.graph_objects.Figure.show') as show:
            figure = result.show(width=1300)
        self.assertEqual(figure.to_json(), plot_kw_comparison(expected, width=1300).to_json())
        show.assert_called_once()

    def test_history_delegates_and_preserves_ordinary_figure(self):
        data = example_frame()
        with patch('plotly.graph_objects.Figure.show') as show:
            figure = TreasuryMarketAnalysis(data).show_history(*data.index)
        self.assertEqual(figure.to_json(), plot_yield_history(data, *data.index).to_json())
        show.assert_called_once()
