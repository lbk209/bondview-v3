"""Hand-checkable financial invariants and presentation separation (offline)."""

from copy import deepcopy
from itertools import product
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import yaml

from bondview.analysis.treasury_curve import analyze_curve, classify_segment
from bondview.data.fred import SERIES, exact_date
from bondview.labels import DEFAULT_LABELS_PATH
from bondview.plotting.treasury_curve import plot_yield_history
from bondview.presentation.treasury_curve import display_table, interpret_curve
from bondview.presentation.widgets import date_picker_defaults


def example_frame():
    """Design example fixture, never represented as downloaded data."""
    data = pd.DataFrame(
        [[3.56, 3.63, 3.94], [4.40, 4.79, 4.97]],
        columns=SERIES, index=pd.to_datetime(["2024-09-16", "2025-01-13"]),
    )
    data.index.name = "date"
    data.attrs["metadata"] = {
        s: {"units": "Percent", "frequency": "D",
            "source": "Design example fixture, not a download",
            "retrieved_at_utc": "2026-10-26T00:00:00+00:00"}
        for s in SERIES
    }
    return data


class CurveTests(unittest.TestCase):
    def test_design_example_and_display_units(self):
        result = analyze_curve(example_frame(), "2024-09-16", "2025-01-13")
        self.assertEqual(result.index.tolist(), [*SERIES, "DGS10_DGS2", "DGS30_DGS10"])
        self.assertEqual(result.change_bp.tolist(), [84, 116, 103, 32, -13])
        self.assertEqual(result.start.tolist(), [3.56, 3.63, 3.94, 7, 31])
        self.assertEqual(result.end.tolist(), [4.4, 4.79, 4.97, 39, 18])
        self.assertEqual(result.level_unit.tolist(), ["%", "%", "%", "bp", "bp"])
        self.assertEqual(result.iloc[3].movement, "bear")
        self.assertEqual(result.iloc[3].slope, "steepening")
        self.assertEqual(result.iloc[4].slope, "flattening")
        table = display_table(result)
        self.assertEqual(table.iloc[:, 0].tolist(), ["3.56%", "3.63%", "3.94%", "+7 bp", "+31 bp"])
        self.assertEqual(table.iloc[3, -1], "Bear steepening")
        self.assertEqual(table.iloc[4, -1], "Bear flattening")
        self.assertEqual(table.iloc[3, -2], "Upward-sloping → Upward-sloping")
        self.assertIn("10Y (+116 bp)", interpret_curve(result))

    def test_percent_and_basis_points(self):
        data = example_frame()
        data.iloc[0] = [4.0, 4.5, 4.8]
        data.iloc[1] = [4.01, 4.48, 4.8]
        result = analyze_curve(data, *data.index)
        self.assertEqual(result.start.tolist(), [4, 4.5, 4.8, 50, 30])
        self.assertEqual(result.change_bp.tolist(), [1, -2, 0, -3, 2])

    def test_regimes_preserve_display_conventions(self):
        cases = [
            (10, 20, "bear", "Bear steepening"), (20, 10, "bear", "Bear flattening"),
            (-20, -10, "bull", "Bull steepening"), (-10, -20, "bull", "Bull flattening"),
            (-10, 10, "twist", "Opposing-direction twist steepening"),
            (10, -10, "twist", "Opposing-direction twist flattening"),
            (10, 10, "parallel_up", "Yields rose; little slope change"),
            (-10, -10, "parallel_down", "Yields fell; little slope change"),
            (0, 0, "unchanged", "Little yield movement"),
            (0, 10, "long_only", "Long yield rose, other little change; steepening"),
            (0, -10, "long_only", "Long yield fell, other little change; flattening"),
            (10, 0, "short_only", "Short yield rose, other little change; flattening"),
            (-10, 0, "short_only", "Short yield fell, other little change; steepening"),
        ]
        for short, long, identifier, expected in cases:
            with self.subTest(short=short, long=long):
                self.assertEqual(classify_segment(short, long)["movement"], identifier)
                data = example_frame()
                data.iloc[0] = [4, 4, 4]
                data.iloc[1] = [4 + short / 100, 4 + long / 100, 4]
                self.assertEqual(display_table(analyze_curve(data, *data.index)).iloc[3, -1], expected)

    def test_slope_tolerance_is_separate_from_yield_direction(self):
        self.assertEqual(classify_segment(10, 11)["slope"], "steepening")
        result = classify_segment(10, 11, 1)
        self.assertEqual(result["slope"], "unchanged")
        self.assertEqual(result["movement"], "parallel_up")
        self.assertEqual(result["short_direction"], "rose")
        self.assertEqual(result["long_direction"], "rose")
        self.assertEqual(classify_segment(11, 10, 0.99)["slope"], "flattening")
        self.assertEqual(classify_segment(-0.1, 0.1, 1)["movement"], "twist")
        for value in (-1, np.nan, np.inf):
            with self.subTest(tolerance=value), self.assertRaises(ValueError):
                classify_segment(0, 0, value)
        with self.assertRaises(ValueError):
            classify_segment(np.inf, 1)
        self.assertEqual(classify_segment(np.nan, 1)["movement"], "unavailable")
        # Equal shifts and inclusive tolerance boundaries remain distinct.
        self.assertEqual(classify_segment(10, 10, 5)["movement"], "parallel_up")
        for tolerance, expected in ((0.999, "steepening"), (1, "unchanged"), (1.001, "unchanged")):
            self.assertEqual(classify_segment(10, 11, tolerance)["slope"], expected)

    def test_classification_sign_grid(self):
        for short, long in product((-20, -10, 0, 10, 20), repeat=2):
            with self.subTest(short=short, long=long):
                result = classify_segment(short, long)
                expected = "steepening" if long > short else "flattening" if long < short else "unchanged"
                self.assertEqual(result["slope"], expected)
                self.assertEqual(result["movement"] == "twist", short * long < 0)

    def test_partial_endpoints_preserve_independent_results(self):
        for endpoint, tenor in product(range(2), range(3)):
            with self.subTest(endpoint=endpoint, tenor=tenor):
                data = example_frame()
                data.iloc[endpoint, tenor] = np.nan
                result = analyze_curve(data, *data.index)
                self.assertTrue(pd.isna(result.iloc[tenor].change_bp))
                self.assertFalse(pd.isna(result.iloc[tenor]["end" if endpoint == 0 else "start"]))
                unaffected = [i for i in range(3) if i != tenor]
                self.assertTrue(result.iloc[unaffected].change_bp.notna().all())
                for row, pair in ((3, (0, 1)), (4, (1, 2))):
                    self.assertEqual(pd.isna(result.iloc[row].change_bp), tenor in pair)
                    if tenor in pair:
                        self.assertEqual(result.iloc[row].movement, "unavailable")
        data = example_frame()
        data["DGS30"] = np.nan
        result = analyze_curve(data, *data.index)
        self.assertEqual(result.iloc[3].change_bp, 32)
        self.assertEqual(display_table(result).iloc[2, 0], "N/A")
        self.assertIn("partial", interpret_curve(result))

    def test_effective_endpoints_use_available_dates_in_interval(self):
        # Preserve main's existing analyze_curve behavior, including empty rows.
        data = example_frame()
        for requested, effective in (("2024-09-15", "2024-09-16"),
                                     ("2024-12-25", "2025-01-13"),
                                     ("2023-01-01", "2024-09-16")):
            with self.subTest(day=requested):
                result = analyze_curve(data, requested, "2025-01-13")
                self.assertTrue(result.start.notna().all())
                self.assertEqual(result.attrs["start"], effective)
        holiday = data.reindex(pd.to_datetime(["2024-09-16", "2024-12-25", "2025-01-13"]))
        result = analyze_curve(holiday, "2024-12-25", "2025-01-13")
        self.assertEqual(result.change_bp.tolist(), [0] * 5)
        result = analyze_curve(data, "2024-09-16", "2025-01-12")
        self.assertEqual(result.attrs["end"], "2024-09-16")
        with self.assertRaisesRegex(ValueError, "No Treasury observations"):
            analyze_curve(data, "2024-12-24", "2024-12-26")

    def test_same_day_and_reversed_dates(self):
        data = example_frame()
        result = analyze_curve(data, "2024-09-16", "2024-09-16")
        self.assertEqual(result.change_bp.tolist(), [0] * 5)
        self.assertEqual(result.iloc[3].movement, "unchanged")
        self.assertEqual(display_table(result).shape, (5, 4))
        figure = plot_yield_history(data, "2024-09-16", "2024-09-16")
        self.assertEqual(list(figure.layout.xaxis.range), ["2024-09-16"] * 2)
        for function in (analyze_curve, plot_yield_history):
            with self.assertRaises(ValueError):
                function(data, "2025-01-13", "2024-09-16")

    def test_configuration_and_downward_interpretation(self):
        data = example_frame()
        data.iloc[0] = [5, 4, 4]
        data.iloc[1] = [4.5, 3, 3.5]
        result = analyze_curve(data, *data.index)
        self.assertEqual(result.iloc[3].configuration_start, "inverted")
        self.assertEqual(result.iloc[4].configuration_start, "flat")
        self.assertEqual(display_table(result).iloc[3, -2], "Inverted → Inverted")
        self.assertEqual(display_table(result).iloc[4, -2], "Flat → Upward-sloping")
        self.assertIn("10Y (-100 bp)", interpret_curve(result))
        self.assertEqual(display_table(result).iloc[3, 0], "-100 bp")

    def test_exact_date_validation(self):
        for value in (None, 0, "2024/09/16", "2024-09-16T00:00:00", "2024-02-30", pd.NaT,
                      pd.Timestamp("2024-09-16T01:00:00"), pd.Timestamp("2024-09-16", tz="UTC")):
            with self.subTest(value=value), self.assertRaises(ValueError):
                exact_date(value)

    def test_treasury_contract_and_explicit_provenance(self):
        data = example_frame()
        metadata = deepcopy(data.attrs["metadata"])
        data.attrs.clear()
        analyze_curve(data, *data.index, metadata=metadata)
        plot_yield_history(data, *data.index, metadata=metadata)
        for field, value in (("units", "Index"), ("frequency", "M")):
            bad = deepcopy(metadata)
            bad["DGS2"][field] = value
            with self.assertRaises(ValueError):
                analyze_curve(data, *data.index, metadata=bad)
        with self.assertRaises(ValueError):
            analyze_curve(example_frame().drop(columns="DGS30"), *data.index)

    def test_historical_plot_and_coverage_widget_defaults(self):
        data = example_frame().reindex(pd.to_datetime(["2024-09-16", "2024-12-25", "2025-01-13"]))
        fig = plot_yield_history(data, "2024-10-01", "2025-01-01")
        self.assertIs(type(fig), go.Figure)
        self.assertEqual([trace.name for trace in fig.data], ["2Y (DGS2)", "10Y (DGS10)", "30Y (DGS30)"])
        for trace in fig.data:
            self.assertEqual(len(trace.x), 1)
            self.assertEqual(trace.mode, "lines")
            self.assertFalse(trace.connectgaps)
            self.assertTrue(pd.isna(trace.y[0]))
        self.assertEqual(list(fig.layout.xaxis.range), ["2024-10-01", "2025-01-01"])
        self.assertTrue(fig.layout.yaxis.autorange)
        start, end = date_picker_defaults(data)
        self.assertEqual(start["value"], data.index.min().date())
        self.assertEqual(end["value"], data.index.max().date())
        self.assertNotIn("min", start)  # Outside dates stay selectable.

    def test_yaml_changes_display_without_changing_financial_results(self):
        data = example_frame()
        before = analyze_curve(data, *data.index)
        labels = yaml.safe_load(DEFAULT_LABELS_PATH.read_text())
        labels["analyses"]["treasury_curve"]["measures"]["DGS10_DGS2"] = "Custom segment"
        labels["analyses"]["treasury_curve"]["movement"]["bear"] = "Custom rising regime {slope}"
        labels["analyses"]["treasury_curve"]["slope"]["steepening"] = "Widening"
        labels["analyses"]["treasury_curve"]["plot"]["title"] = "Custom history"
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "labels.yaml"
            path.write_text(yaml.safe_dump(labels))
            table = display_table(before, labels_path=path)
            self.assertEqual(table.index[3], "Custom segment")
            self.assertEqual(table.iloc[3, -1], "Custom rising regime widening")
            self.assertIn("Custom segment", interpret_curve(before, labels_path=path))
            self.assertEqual(plot_yield_history(data, *data.index, labels_path=path).layout.title.text, "Custom history")
            # No module reload needed; a second edit is read on the next call.
            labels["analyses"]["treasury_curve"]["measures"]["DGS2"] = "Custom 2Y"
            path.write_text(yaml.safe_dump(labels))
            self.assertEqual(display_table(before, labels_path=path).index[0], "Custom 2Y")
        with patch("bondview.labels.load_labels", side_effect=AssertionError("Financial logic must not read YAML")):
            after = analyze_curve(data, *data.index)
        pd.testing.assert_frame_equal(before, after)


if __name__ == "__main__":
    unittest.main()
