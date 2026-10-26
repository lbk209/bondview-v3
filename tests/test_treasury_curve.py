"""Hand-checkable endpoint, classification, plotting and input tests (offline)."""

from itertools import product
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import numpy as np
import pandas as pd

from bondview.analysis.treasury_curve import (
    analyze_curve, classify_segment, display_table, interpret_curve,
)
from bondview.data.fred import (
    SERIES, download_fred, exact_date, load_observations, save_observations,
    validate_observations,
)
from bondview.plotting.treasury_curve import plot_yield_history


def example_frame():
    """Accepted design example fixture; not presented as a downloaded dataset."""
    data = pd.DataFrame(
        [[3.56, 3.63, 3.94], [4.40, 4.79, 4.97]],
        columns=SERIES, index=pd.to_datetime(["2024-09-16", "2025-01-13"]),
    )
    data.index.name = "date"
    data.attrs["metadata"] = {
        "source": "Design example fixture, not a download",
        "retrieved_at_utc": "2026-10-26T00:00:00+00:00",
        "series": {s: {"units": "Percent"} for s in SERIES},
    }
    return data


class CurveTests(unittest.TestCase):
    def test_design_example(self):
        result = analyze_curve(example_frame(), "2024-09-16", "2025-01-13")
        self.assertEqual(result.change_bp.tolist(), [84, 116, 103, 32, -13])
        self.assertEqual(result.start.tolist(), [3.56, 3.63, 3.94, 7, 31])
        self.assertEqual(result.end.tolist(), [4.4, 4.79, 4.97, 39, 18])
        self.assertEqual(result.iloc[3].movement, "Bear steepening")
        self.assertEqual(result.iloc[4].movement, "Bear flattening")
        self.assertEqual(result.iloc[3].configuration, "Upward-sloping → Upward-sloping")
        self.assertIn("10Y (+116.00 bp)", interpret_curve(result))

    def test_percent_and_basis_points(self):
        data = example_frame()
        data.iloc[0] = [4.0, 4.5, 4.8]
        data.iloc[1] = [4.01, 4.48, 4.8]
        result = analyze_curve(data, *data.index)
        self.assertEqual(result.start.tolist(), [4, 4.5, 4.8, 50, 30])
        self.assertEqual(result.change_bp.tolist(), [1, -2, 0, -3, 2])

    def test_regimes(self):
        cases = [
            (10, 20, "Bear steepening"), (20, 10, "Bear flattening"),
            (-20, -10, "Bull steepening"), (-10, -20, "Bull flattening"),
            (-10, 10, "Opposing-direction twist steepening"),
            (10, -10, "Opposing-direction twist flattening"),
            (10, 10, "Parallel upward shift"), (-10, -10, "Parallel downward shift"),
            (0, 0, "Unchanged yields"),
            (0, 10, "Long yield rose, other unchanged; steepening"),
            (0, -10, "Long yield fell, other unchanged; flattening"),
            (10, 0, "Short yield rose, other unchanged; flattening"),
            (-10, 0, "Short yield fell, other unchanged; steepening"),
        ]
        for short, long, expected in cases:
            with self.subTest(short=short, long=long):
                self.assertEqual(classify_segment(short, long)["movement"], expected)

    def test_slope_tolerance_is_separate_from_yield_direction(self):
        self.assertEqual(classify_segment(10, 11)["slope"], "Steepening")
        result = classify_segment(10, 11, 1)
        self.assertEqual(result["slope"], "Unchanged slope")
        self.assertEqual(result["movement"], "Bear unchanged slope")
        self.assertIn("yield rose", result["direction"])
        self.assertNotIn("Parallel", result["movement"])
        self.assertEqual(classify_segment(11, 10, 0.99)["slope"], "Flattening")
        self.assertEqual(classify_segment(-0.1, 0.1, 1)["movement"], "Opposing-direction twist unchanged slope")
        for value in (-1, np.nan, np.inf):
            with self.subTest(tolerance=value), self.assertRaises(ValueError):
                classify_segment(0, 0, value)
        with self.assertRaises(ValueError):
            classify_segment(np.inf, 1)
        self.assertEqual(classify_segment(np.nan, 1)["movement"], "N/A")

    def test_classification_sign_grid(self):
        # Independent slope and sign checks across all sign/zero combinations.
        for short, long in product((-20, -10, 0, 10, 20), repeat=2):
            with self.subTest(short=short, long=long):
                result = classify_segment(short, long)
                expected = "Steepening" if long > short else "Flattening" if long < short else "Unchanged slope"
                self.assertEqual(result["slope"], expected)
                self.assertEqual("twist" in result["movement"], short * long < 0)

    def test_partial_endpoints_preserve_independent_results(self):
        # Each of the six input positions can be missing independently.
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
                        self.assertEqual(result.iloc[row].movement, "N/A")
        data = example_frame()
        data["DGS30"] = np.nan
        result = analyze_curve(data, *data.index)
        self.assertEqual(result.iloc[3].change_bp, 32)
        self.assertEqual(result.iloc[3].movement, "Bear steepening")
        self.assertEqual(display_table(result).iloc[2, 0], "N/A")
        self.assertIn("partial", interpret_curve(result))

    def test_exact_weekends_holidays_and_outside_coverage(self):
        data = example_frame()
        for missing_date in ("2024-09-15", "2024-12-25", "2023-01-01"):
            with self.subTest(day=missing_date):
                result = analyze_curve(data, missing_date, "2025-01-13")
                self.assertTrue(result.start.isna().all())
                self.assertTrue(result.change_bp.isna().all())
                self.assertTrue(result.end.notna().all())
                self.assertEqual(result.attrs["start"], missing_date)
                self.assertIn("No tenor", interpret_curve(result))
        # A source-provided holiday row containing missing values remains missing.
        holiday = data.reindex(pd.to_datetime(["2024-09-16", "2024-12-25", "2025-01-13"]))
        self.assertTrue(analyze_curve(holiday, "2024-12-25", "2025-01-13").change_bp.isna().all())
        missing_end = analyze_curve(data, "2024-09-16", "2025-01-12")
        self.assertTrue(missing_end.start.notna().all())
        self.assertTrue(missing_end.end.isna().all())
        self.assertTrue(missing_end.change_bp.isna().all())

    def test_same_day_and_reversed_dates(self):
        data = example_frame()
        result = analyze_curve(data, "2024-09-16", "2024-09-16")
        self.assertEqual(result.change_bp.tolist(), [0] * 5)
        self.assertEqual(result.iloc[3].movement, "Unchanged yields")
        self.assertEqual(display_table(result).shape, (5, 5))
        with self.assertRaises(ValueError):
            analyze_curve(data, "2025-01-13", "2024-09-16")

    def test_configuration_and_downward_interpretation(self):
        data = example_frame()
        data.iloc[0] = [5, 4, 4]
        data.iloc[1] = [4.5, 3, 3.5]
        result = analyze_curve(data, *data.index)
        self.assertEqual(result.iloc[3].configuration, "Inverted → Inverted")
        self.assertEqual(result.iloc[4].configuration, "Flat → Upward-sloping")
        self.assertIn("downward", interpret_curve(result))
        self.assertIn("10Y (-100.00 bp)", interpret_curve(result))
        self.assertEqual(display_table(result).iloc[3, 0], "-100.00 bp")

    def test_exact_date_validation(self):
        for value in (None, 0, "2024/09/16", "2024-09-16T00:00:00", "2024-02-30", pd.NaT,
                      pd.Timestamp("2024-09-16T01:00:00"), pd.Timestamp("2024-09-16", tz="UTC")):
            with self.subTest(value=value), self.assertRaises(ValueError):
                exact_date(value)

    def test_historical_plot_has_all_observations_and_gaps(self):
        data = example_frame().reindex(pd.to_datetime(["2024-09-16", "2024-12-25", "2025-01-13"]))
        fig = plot_yield_history(data)
        self.assertEqual(len(fig.data), 3)
        self.assertEqual([trace.name for trace in fig.data], ["2Y (DGS2)", "10Y (DGS10)", "30Y (DGS30)"])
        for trace in fig.data:
            self.assertEqual(len(trace.x), 3)
            self.assertEqual(trace.mode, "lines")
            self.assertFalse(trace.connectgaps)
            self.assertTrue(pd.isna(trace.y[1]))
        self.assertEqual(list(fig.layout.xaxis.range), ["2024-09-01", "2025-01-31"])
        self.assertTrue(fig.layout.xaxis.rangeslider.visible)
        with self.assertRaises(ValueError):
            plot_yield_history(data, "2025-01-13", "2024-09-16")


class FileTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "observations.json"

    def test_roundtrip_preserves_metadata_missing_values_and_calculations(self):
        data = example_frame()
        data.iloc[0, 2] = np.nan
        save_observations(data, self.path)
        with patch("bondview.data.fred._read_url", side_effect=AssertionError("Offline means offline")):
            loaded = load_observations(self.path)
            pd.testing.assert_frame_equal(data, loaded)
            pd.testing.assert_frame_equal(analyze_curve(data, *data.index), analyze_curve(loaded, *data.index))
        self.assertEqual(data.attrs, loaded.attrs)
        self.assertIn('"DGS30": null', self.path.read_text())
        self.assertNotIn("NaN", self.path.read_text())

    def test_invalid_files_and_units(self):
        save_observations(example_frame(), self.path)
        valid = json.loads(self.path.read_text())
        mutations = [
            lambda p: p.update(format="unknown"),
            lambda p: p["metadata"]["series"]["DGS2"].update(units="Basis points"),
            lambda p: p["metadata"].pop("retrieved_at_utc"),
            lambda p: p["metadata"].update(retrieved_at_utc="2026-10-26"),
            lambda p: p["observations"][0].update(date="2024-02-30"),
            lambda p: p["observations"][0].update(date="2024-09-16T12:00:00"),
            lambda p: p["observations"][0].update(date="2025-01-13"),
            lambda p: p["observations"][0].pop("DGS30"),
            lambda p: p["observations"][0].update(DGS2="4.0%"),
            lambda p: p["observations"][0].update(DGS2=True),
            lambda p: p["observations"][0].update(DGS2=float("inf")),
            lambda p: p.update(observations=[]),
            lambda p: p.update(metadata=[]),
        ]
        for index, mutate in enumerate(mutations):
            with self.subTest(mutation=index):
                payload = json.loads(json.dumps(valid))
                mutate(payload)
                self.path.write_text(json.dumps(payload))
                with self.assertRaises(ValueError):
                    load_observations(self.path)
        for content in ("not json", "{}", "[]"):
            self.path.write_text(content)
            with self.assertRaises(ValueError):
                load_observations(self.path)
        with self.assertRaises(FileNotFoundError):
            load_observations(self.path.with_name("missing.json"))

    def test_invalid_in_memory_data(self):
        data = example_frame()
        data.index = ["2024-09-16", "2025-01-13"]
        with self.assertRaises(ValueError):
            validate_observations(data)
        data = example_frame().drop(columns="DGS30")
        with self.assertRaises(ValueError):
            analyze_curve(data, "2024-09-16", "2025-01-13")


class DownloadTests(unittest.TestCase):
    def test_public_download_save_and_file_equivalence(self):
        csv = b"observation_date,DGS2,DGS10,DGS30\n2024-09-13,3,4,5\n2024-09-16,3.56,3.63,\n2025-01-13,4.40,4.79,4.97\n2025-01-14,4,5,6\n"
        with patch.dict("os.environ", {}, clear=True), patch("bondview.data.fred._read_url", return_value=csv) as reader:
            data = download_fred("2024-09-16", "2025-01-13")
        self.assertEqual(len(data), 2)
        self.assertEqual(reader.call_count, 1)
        self.assertTrue(pd.isna(data.iloc[0].DGS30))
        self.assertIn("public graph CSV", data.attrs["metadata"]["transport"])
        with tempfile.TemporaryDirectory() as temp:
            path = save_observations(data, Path(temp) / "cache.json")
            loaded = load_observations(path)
        pd.testing.assert_frame_equal(analyze_curve(data, *data.index), analyze_curve(loaded, *loaded.index))
        self.assertEqual(analyze_curve(loaded, *loaded.index).iloc[3].change_bp, 32)

    def test_api_requests_units_and_metadata(self):
        def response(endpoint, key, **params):
            self.assertEqual(key, "secret-test-key")
            s = params["series_id"]
            i = SERIES.index(s)
            if endpoint == "series":
                return {"seriess": [{"units": "Percent", "frequency_short": "D", "title": s, "last_updated": "test"}]}
            self.assertEqual(params["units"], "lin")
            self.assertEqual(params["observation_start"], "2024-09-16")
            return {"count": 2, "realtime_start": "2026-10-26", "realtime_end": "2026-10-26", "observations": [
                {"date": "2024-09-16", "value": str((3.56, 3.63, 3.94)[i])},
                {"date": "2025-01-13", "value": "." if i == 2 else str((4.4, 4.79)[i])},
            ]}
        with patch("bondview.data.fred._api_json", side_effect=response) as mocked:
            data = download_fred("2024-09-16", "2025-01-13", api_key="secret-test-key")
        self.assertEqual(mocked.call_count, 6)
        self.assertTrue(pd.isna(data.iloc[1].DGS30))
        self.assertNotIn("secret-test-key", str(data.attrs))
        self.assertEqual(data.attrs["metadata"]["series"]["DGS2"]["realtime_start"], "2026-10-26")

    def test_key_environment_precedence_and_dotenv(self):
        with tempfile.TemporaryDirectory() as temp:
            env = Path(temp) / ".env"
            env.write_text("FRED_API_KEY=dotenv-test-key\n")
            with patch.dict("os.environ", {}, clear=True), patch("bondview.data.fred._api_json", side_effect=RuntimeError("stop")) as mocked:
                with self.assertRaises(RuntimeError):
                    download_fred(env_path=env)
                self.assertEqual(mocked.call_args.args[1], "dotenv-test-key")
            with patch.dict("os.environ", {"FRED_API_KEY": "environment-test-key"}), patch("bondview.data.fred._api_json", side_effect=RuntimeError("stop")) as mocked:
                with self.assertRaises(RuntimeError):
                    download_fred(env_path=env)
                self.assertEqual(mocked.call_args.args[1], "environment-test-key")

    def test_api_validates_source_units_and_truncation(self):
        info = {"units": "Percent", "frequency_short": "D", "title": "Test", "last_updated": "test"}
        for field, bad in (("units", "Index"), ("frequency_short", "M")):
            with self.subTest(field=field), patch("bondview.data.fred._api_json", return_value={"seriess": [{**info, field: bad}]}):
                with self.assertRaises(ValueError):
                    download_fred(api_key="test")
        with patch("bondview.data.fred._api_json", side_effect=[{"seriess": [info]}, {"count": 2, "observations": []}]):
            with self.assertRaises(ValueError):
                download_fred(api_key="test")

    def test_request_failures_do_not_leak_credentials(self):
        with patch("bondview.data.fred.urlopen", side_effect=OSError("url includes secret-key")):
            with self.assertRaises(RuntimeError) as error:
                download_fred(api_key="secret-key")
        self.assertNotIn("secret-key", str(error.exception))

    def test_download_rejects_invalid_inputs_before_network(self):
        with patch("bondview.data.fred._read_url", side_effect=AssertionError("No request expected")):
            for kwargs in ({"start": "2025-01-13", "end": "2024-09-16"}, {"series_ids": []},
                           {"series_ids": ["DGS2", "DGS2"]}, {"series_ids": ["DGS2&bad"]}):
                with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                    download_fred(**kwargs)


if __name__ == "__main__":
    unittest.main()
