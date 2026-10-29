"""Offline, hand-checkable KW paths and native Plotly figure contracts."""

from copy import deepcopy
from pathlib import Path
import tempfile
import unittest

import numpy as np
import pandas as pd
import yaml

from bondview.analysis.treasury_curve import analyze_kw_decomposition
from bondview.labels import DEFAULT_LABELS_PATH
from bondview.plotting.treasury_curve import plot_kw_decomposition


def kw_frame():
    """Synthetic levels with an intermediate reversal, not market observations."""
    data = pd.DataFrame({
        "THREEFY2": [4., 4.4, 3.8, 4.1],
        "THREEFYTP2": [-.2, -.1, -.3, -.15],
        "THREEFY10": [5., 5.1, 4.9, 5.2],
        "THREEFYTP10": [.5, .7, .4, .8],
    }, index=pd.to_datetime(["2024-12-20", "2024-12-23", "2024-12-24", "2024-12-27"]))
    data.index.name = "date"
    data.attrs["metadata"] = {
        s: {"units": "Percent", "frequency": "D", "source": "Synthetic test fixture",
            "retrieved_at_utc": "2026-10-29T00:00:00+00:00"}
        for s in data.columns
    }
    return data


class KWTests(unittest.TestCase):
    def test_pairing_subtraction_bp_and_complete_reversing_paths(self):
        data = kw_frame()
        original = data.copy(deep=True)
        result = analyze_kw_decomposition(data, "2024-12-19", "2024-12-29")
        self.assertEqual(list(result), ["2Y", "10Y"])
        for maturity, fitted, premium, expected, changes, tp_changes, totals in (
            ("2Y", "THREEFY2", "THREEFYTP2", [4.2, 4.5, 4.1, 4.25],
             [0, 30, -10, 5], [0, 10, -10, 5], [0, 40, -20, 10]),
            ("10Y", "THREEFY10", "THREEFYTP10", [4.5, 4.4, 4.5, 4.4],
             [0, -10, 0, -10], [0, 20, -10, 30], [0, 10, -10, 20]),
        ):
            with self.subTest(maturity=maturity):
                path = result[maturity]
                pd.testing.assert_index_equal(path.index, data.index)
                np.testing.assert_array_equal(path.fitted_yield, data[fitted])
                np.testing.assert_array_equal(path.term_premium, data[premium])
                np.testing.assert_allclose(path.expected_rate, expected)
                np.testing.assert_allclose(path.expected_change_bp, changes, atol=1e-12)
                np.testing.assert_allclose(path.premium_change_bp, tp_changes, atol=1e-12)
                np.testing.assert_allclose(path.fitted_change_bp, totals, atol=1e-12)
                self.assertEqual(set(path.attrs["metadata"]), {fitted, premium})
        pd.testing.assert_frame_equal(data, original)

    def test_common_nonmissing_alignment_and_effective_endpoints(self):
        for series in kw_frame().columns:
            with self.subTest(missing_series=series):
                data = kw_frame().reindex(pd.date_range("2024-12-20", "2024-12-29"))
                data.loc["2024-12-24", series] = np.nan
                # Sunday and Saturday bounds: only Mon/Fri qualify; no filling.
                result = analyze_kw_decomposition(data.iloc[::-1], "2024-12-22", "2024-12-28")
                for path in result.values():
                    self.assertEqual(path.index.tolist(), list(pd.to_datetime(["2024-12-23", "2024-12-27"])))
                    np.testing.assert_array_equal(path.iloc[0, 3:], [0, 0, 0])
                np.testing.assert_allclose(result["2Y"].expected_change_bp, [0, -25], atol=1e-12)
        # A holiday bound moves inward to the next observation, never backward.
        result = analyze_kw_decomposition(kw_frame(), "2024-12-25", "2024-12-29")
        for path in result.values():
            self.assertEqual(path.index.tolist(), [pd.Timestamp("2024-12-27")])
            np.testing.assert_array_equal(path.iloc[0, 3:], [0, 0, 0])

    def test_empty_intervals_and_invalid_inputs(self):
        for start, end in (("2024-12-25", "2024-12-26"), ("2025-01-01", "2025-01-10")):
            with self.subTest(start=start), self.assertRaisesRegex(ValueError, "No complete KW observations"):
                analyze_kw_decomposition(kw_frame(), start, end)
        missing = kw_frame()
        missing["THREEFY10"] = np.nan
        with self.assertRaisesRegex(ValueError, "No complete KW observations"):
            analyze_kw_decomposition(missing, "2024-12-20", "2024-12-29")
        with self.assertRaises(ValueError):
            analyze_kw_decomposition(kw_frame(), "2024-12-29", "2024-12-20")
        data = kw_frame().drop(columns="THREEFYTP10")
        data.attrs["metadata"] = {s: data.attrs["metadata"][s] for s in data.columns}
        with self.assertRaisesRegex(ValueError, "requires THREEFY2"):
            analyze_kw_decomposition(data, "2024-12-20", "2024-12-29")
        for key, value in (("units", "Index"), ("frequency", "M")):
            metadata = deepcopy(kw_frame().attrs["metadata"])
            metadata["THREEFY2"][key] = value
            with self.assertRaisesRegex(ValueError, "daily Percent"):
                analyze_kw_decomposition(kw_frame(), "2024-12-20", "2024-12-29", metadata=metadata)

    def test_figure_values_single_axis_domains_units_and_hover(self):
        results = analyze_kw_decomposition(kw_frame(), "2024-12-19", "2024-12-29")
        for maturity, path in results.items():
            with self.subTest(maturity=maturity):
                figure = plot_kw_decomposition(path, maturity)
                self.assertEqual(figure.layout.title.text, f"{maturity} KW Decomposition")
                self.assertEqual(len(figure.data), 5)
                self.assertEqual(figure.layout.hovermode, "x")
                self.assertEqual(figure.layout.hoversubplots, "axis")
                self.assertNotIn("xaxis2", figure.to_plotly_json()["layout"])
                self.assertEqual(figure.layout.xaxis.anchor, "y2")
                self.assertEqual(figure.layout.xaxis.side, "bottom")
                self.assertTrue(figure.layout.xaxis.showticklabels)
                self.assertEqual(figure.layout.xaxis.type, "date")
                self.assertEqual(list(figure.layout.xaxis.range), ["2024-12-20", "2024-12-27"])
                self.assertTrue(figure.layout.xaxis.showspikes)
                self.assertEqual(figure.layout.xaxis.spikemode, "across")
                self.assertEqual(figure.layout.xaxis.spikesnap, "data")
                self.assertEqual(figure.layout.yaxis.title.text, "Level (%)")
                self.assertEqual(figure.layout.yaxis2.title.text, "Change (bp)")
                upper, lower = figure.layout.yaxis.domain, figure.layout.yaxis2.domain
                self.assertGreater(upper[0], lower[1])
                self.assertAlmostEqual((upper[1]-upper[0])/(lower[1]-lower[0]), 7/3)
                self.assertFalse(figure.layout.annotations)
                for trace, column, axis in zip(figure.data, path.columns[:5], ["y"]*3+["y2"]*2):
                    pd.testing.assert_index_equal(pd.DatetimeIndex(trace.x, name="date"), path.index)
                    np.testing.assert_array_equal(trace.y, path[column])
                    self.assertEqual(trace.xaxis, "x")
                    self.assertEqual(trace.yaxis, axis)
                    self.assertEqual(trace.mode, "lines")
                    self.assertIsNone(trace.fill)
                    self.assertFalse(trace.connectgaps)
                    if axis == "y":
                        self.assertIn("%{y:.4f}%", trace.hovertemplate)
                    else:
                        self.assertIn("bp", trace.hovertemplate)
                        self.assertEqual(trace.y[0], 0)
                expected, premium = figure.data[3:]
                np.testing.assert_array_equal(expected.customdata[:, 0], path.fitted_change_bp)
                self.assertIn("Expected-rate change:", expected.hovertemplate)
                self.assertIn("%{customdata[0]:+.2f} bp", expected.hovertemplate)
                self.assertIn("Term-premium change:", premium.hovertemplate)
                self.assertEqual(sum(t.hovertemplate.count("Total KW fitted-yield change:") for t in figure.data), 1)
                self.assertIsNone(premium.customdata)

    def test_one_observation_and_configurable_presentation(self):
        path = analyze_kw_decomposition(kw_frame(), "2024-12-27", "2024-12-29")["2Y"]
        figure = plot_kw_decomposition(path, "2Y")
        self.assertEqual(list(figure.layout.xaxis.range), ["2024-12-27"]*2)
        labels = yaml.safe_load(DEFAULT_LABELS_PATH.read_text())
        plot = labels["analyses"]["kw_decomposition"]["plot"]
        plot["titles"]["2Y"] = "Custom KW title"
        plot["traces"]["expected_rate"] = "Custom expectation label"
        plot["level_axis"] = "Custom level (%)"
        with tempfile.TemporaryDirectory() as temp:
            config = Path(temp)/"labels.yaml"
            config.write_text(yaml.safe_dump(labels))
            figure = plot_kw_decomposition(path, "2Y", labels_path=config)
        self.assertEqual(figure.layout.title.text, "Custom KW title")
        self.assertEqual(figure.data[1].name, "Custom expectation label")
        self.assertEqual(figure.layout.yaxis.title.text, "Custom level (%)")
        with self.assertRaisesRegex(ValueError, "eligible observations"):
            plot_kw_decomposition(path.iloc[:0], "2Y")


if __name__ == "__main__":
    unittest.main()
