"""KW financial arithmetic, date eligibility, and the two-column Plotly layout."""

from copy import deepcopy
from pathlib import Path
import tempfile
import unittest

import numpy as np
import pandas as pd
import yaml

from bondview.analysis.treasury_curve import analyze_kw_decomposition
from bondview.labels import DEFAULT_LABELS_PATH
from bondview.plotting.treasury_curve import plot_kw_comparison, plot_kw_decomposition


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
                result = analyze_kw_decomposition(data.iloc[::-1], "2024-12-22", "2024-12-28")
                for path in result.values():
                    self.assertEqual(path.index.tolist(), list(pd.to_datetime(["2024-12-23", "2024-12-27"])))
                    np.testing.assert_array_equal(path.iloc[0, 3:], [0, 0, 0])
                np.testing.assert_allclose(result["2Y"].expected_change_bp, [0, -25], atol=1e-12)
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

    def test_side_by_side_independent_axes_and_unified_hover(self):
        results = analyze_kw_decomposition(kw_frame(), "2024-12-19", "2024-12-29")
        figure = plot_kw_comparison(results)
        self.assertEqual(len(figure.data), 10)
        self.assertEqual(figure.layout.hovermode, "x unified")
        self.assertEqual(figure.layout.hoversubplots, "axis")
        # make_subplots enumerates axes in row-major order:
        # (upper 2Y, upper 10Y, lower 2Y, lower 10Y).
        self.assertEqual([t.xaxis for t in figure.data], ["x"] * 3 + ["x3"] * 2
                         + ["x2"] * 3 + ["x4"] * 2)
        self.assertEqual([t.yaxis for t in figure.data], ["y"] * 3 + ["y3"] * 2
                         + ["y2"] * 3 + ["y4"] * 2)
        for axis_name in ("xaxis", "xaxis2", "xaxis3", "xaxis4"):
            axis = getattr(figure.layout, axis_name)
            self.assertIsNone(axis.matches)
            self.assertEqual(axis.type, "date")
            self.assertEqual(list(axis.range), ["2024-12-20", "2024-12-27"])
            self.assertTrue(axis.showticklabels)
        # Each maturity occupies a column; its levels are above its changes.
        self.assertEqual(figure.layout.xaxis.domain, figure.layout.xaxis3.domain)
        self.assertEqual(figure.layout.xaxis2.domain, figure.layout.xaxis4.domain)
        self.assertGreater(figure.layout.yaxis.domain[0], figure.layout.yaxis3.domain[1])
        self.assertGreater(figure.layout.yaxis2.domain[0], figure.layout.yaxis4.domain[1])
        self.assertEqual(figure.layout.yaxis.title.text, "Level (%)")
        self.assertEqual(figure.layout.yaxis2.title.text, "Level (%)")
        self.assertEqual(figure.layout.yaxis3.title.text, "Change (bp)")
        self.assertEqual(figure.layout.yaxis4.title.text, "Change (bp)")
        for i, maturity in enumerate(("2Y", "10Y")):
            path = results[maturity]
            group = list(figure.data[i*5:(i+1)*5])
            for trace, column in zip(group, path.columns[:5]):
                pd.testing.assert_index_equal(pd.DatetimeIndex(trace.x, name="date"), path.index)
                np.testing.assert_array_equal(trace.y, path[column])
                self.assertEqual(trace.mode, "lines")
                self.assertFalse(trace.connectgaps)
                self.assertIsNone(trace.fill)
                self.assertIn(".2f", trace.hovertemplate)
            np.testing.assert_array_equal(group[3].customdata[:, 0], path.fitted_change_bp)
            self.assertEqual(sum("Total KW fitted-yield change" in t.hovertemplate for t in group), 1)
        self.assertEqual(len(figure.layout.annotations), 2)
        self.assertIn("2Y KW Decomposition", figure.layout.annotations[0].text)
        self.assertIn("10Y KW Decomposition", figure.layout.annotations[1].text)
        self.assertEqual(sum(bool(t.showlegend) for t in figure.data), 5)

    def test_single_maturity_unlinked_date_axes_and_unified_hover(self):
        results = analyze_kw_decomposition(kw_frame(), "2024-12-19", "2024-12-29")
        for maturity in ("2Y", "10Y"):
            with self.subTest(maturity=maturity):
                figure = plot_kw_decomposition(results[maturity], maturity)
                self.assertEqual(figure.layout.title.text, f"{maturity} KW Decomposition")
                self.assertEqual(len(figure.data), 5)
                self.assertEqual(figure.layout.hovermode, "x unified")
                self.assertEqual(figure.layout.hoversubplots, "axis")
                self.assertEqual([trace.xaxis for trace in figure.data], ["x"] * 3 + ["x2"] * 2)
                self.assertEqual([trace.yaxis for trace in figure.data], ["y"] * 3 + ["y2"] * 2)
                self.assertIsNone(figure.layout.xaxis.matches)
                self.assertIsNone(figure.layout.xaxis2.matches)
                for axis in (figure.layout.xaxis, figure.layout.xaxis2):
                    self.assertTrue(axis.showticklabels)
                    self.assertEqual(list(axis.range), ["2024-12-20", "2024-12-27"])
                self.assertGreater(figure.layout.yaxis.domain[0], figure.layout.yaxis2.domain[1])
                self.assertEqual(figure.layout.yaxis.title.text, "Level (%)")
                self.assertEqual(figure.layout.yaxis2.title.text, "Change (bp)")
                self.assertFalse(figure.layout.annotations)
                self.assertEqual(sum("Total KW fitted-yield change" in t.hovertemplate
                                     for t in figure.data), 1)
                self.assertTrue(all(".2f" in t.hovertemplate for t in figure.data))

    def test_one_observation_and_configurable_presentation(self):
        results = analyze_kw_decomposition(kw_frame(), "2024-12-27", "2024-12-29")
        figure = plot_kw_decomposition(results["2Y"], "2Y")
        self.assertEqual(list(figure.layout.xaxis.range), ["2024-12-26", "2024-12-28"])
        self.assertEqual(list(figure.layout.xaxis2.range), ["2024-12-26", "2024-12-28"])
        self.assertTrue(all(t.mode == "lines+markers" for t in figure.data))
        labels = yaml.safe_load(DEFAULT_LABELS_PATH.read_text())
        plot = labels["analyses"]["kw_decomposition"]["plot"]
        plot["titles"]["2Y"] = "Custom KW title"
        plot["traces"]["expected_rate"] = "Custom expectation label"
        plot["level_axis"] = "Custom level (%)"
        with tempfile.TemporaryDirectory() as temp:
            config = Path(temp) / "labels.yaml"
            config.write_text(yaml.safe_dump(labels))
            figure = plot_kw_decomposition(results["2Y"], "2Y", labels_path=config)
            comparison = plot_kw_comparison(results, labels_path=config)
        self.assertEqual(figure.layout.title.text, "Custom KW title")
        self.assertEqual(figure.data[1].name, "Custom expectation label")
        self.assertEqual(figure.layout.yaxis.title.text, "Custom level (%)")
        self.assertEqual(comparison.layout.annotations[0].text, "Custom KW title")
        self.assertTrue(all(t.mode == "lines+markers" for t in comparison.data))
        with self.assertRaisesRegex(ValueError, "eligible observations"):
            plot_kw_decomposition(results["2Y"].iloc[:0], "2Y")
        with self.assertRaisesRegex(ValueError, "eligible observations"):
            plot_kw_comparison({"2Y": results["2Y"].iloc[:0], "10Y": results["10Y"]})


if __name__ == "__main__":
    unittest.main()
