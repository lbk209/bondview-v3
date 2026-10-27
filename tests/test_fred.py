"""CSV/provenance, shared units/frequencies and credential handling tests."""

from io import StringIO
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import numpy as np
import pandas as pd

from bondview.analysis.treasury_curve import analyze_curve
from bondview.data.fred import (
    SERIES, FredDataManager, download_fred, load_observations, save_observations,
    validate_observations,
)
from test_treasury_curve import example_frame


class FileTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "observations.csv"

    def test_roundtrip_preserves_metadata_missing_values_and_calculations(self):
        data = example_frame()
        data.iloc[0, 2] = np.nan
        data.iloc[1, 0] = 4.123456789012345
        save_observations(data, self.path)
        with patch("bondview.data.fred._read_url", side_effect=AssertionError("Offline means offline")):
            loaded = load_observations(self.path)
        pd.testing.assert_frame_equal(data, loaded, check_exact=True)
        self.assertEqual(data.attrs, loaded.attrs)
        pd.testing.assert_frame_equal(analyze_curve(data, *data.index), analyze_curve(loaded, *data.index))
        content = self.path.read_text()
        self.assertIn('# source: "Design example fixture, not a download"', content)
        self.assertIn('# retrieved_at_utc:', content)
        self.assertIn('# series:', content)
        self.assertIn('2024-09-16,3.56,3.63,\n', content)
        self.assertNotIn("NaN", content)
        self.assertEqual(list(self.path.parent.iterdir()), [self.path])
        pd.testing.assert_frame_equal(pd.read_csv(self.path, comment="#", index_col=0, parse_dates=True,
                                                  float_precision="round_trip"), loaded)

    def test_mixed_units_and_frequency_and_manager_independent_provenance(self):
        data = pd.DataFrame({"RATE": [4.123456789012345, np.nan, -0.01], "FX": [1234.5, 1235., np.nan],
                             "INDEX": [np.nan, 101.23456789012345, np.nan]},
                            index=pd.to_datetime(["2024-01-01", "2024-02-01", "2024-02-02"]))
        metadata = {"source": 'Fixture with comma, colon: and newline\nnot live',
                    "retrieved_at_utc": "2026-10-26T00:00:00+00:00",
                    "series": {"RATE": {"units": "Percent", "frequency": "M"},
                               "FX": {"units": "Won per U.S. Dollar", "frequency": "D"},
                               "INDEX": {"units": "Index 2017=100", "frequency": "Q", "title": "Quoted, title"}}}
        save_observations(data, self.path, metadata=metadata)
        manager = FredDataManager(self.path)
        with patch("bondview.data.fred._read_url", side_effect=AssertionError("No network")), \
             patch("bondview.data.fred.dotenv_values", side_effect=AssertionError("No credentials")):
            loaded = manager.load_or_download("file", start="ignored", end="ignored")
        pd.testing.assert_frame_equal(validate_observations(data, metadata), loaded, check_exact=True)
        loaded.attrs.clear()
        self.assertEqual(manager.metadata, metadata)
        copy = manager.metadata
        copy["series"]["RATE"]["units"] = "broken"
        self.assertEqual(manager.metadata, metadata)
        with patch("sys.stdout", new_callable=StringIO) as output:
            manager.report()
        self.assertIn("Won per U.S. Dollar, D", output.getvalue())
        self.assertIn("Index 2017=100, Q", output.getvalue())
        manager.save()
        self.assertEqual(load_observations(self.path).attrs["metadata"], metadata)
        self.assertEqual(list(self.path.parent.iterdir()), [self.path])

    def test_invalid_csv_and_metadata(self):
        save_observations(example_frame(), self.path)
        valid = self.path.read_text()
        mutations = [
            valid.replace('bondview.fred_observations.csv.v1', 'unknown'),
            '\n'.join(s for s in valid.splitlines() if not s.startswith('# retrieved_at_utc:')),
            valid.replace('2026-10-26T00:00:00+00:00', '2026-10-26'),
            valid.replace('"frequency": "D"', '"frequency": ""'),
            valid.replace('"units": "Percent"', '"units": null'),
            valid.replace('2024-09-16', '2024-02-30'),
            valid.replace('2024-09-16', '2024-09-16T12:00:00'),
            valid.replace('2024-09-16', '2025-01-13'),
            valid.replace('3.56,3.63,3.94', '3.56,3.63'),
            valid.replace('3.56,3.63,3.94', 'True,3.63,3.94'),
            valid.replace('3.56,3.63,3.94', 'NaN,3.63,3.94'),
            valid.replace('3.56,3.63,3.94', 'inf,3.63,3.94'),
            valid.replace('DGS2,DGS10,DGS30', 'DGS2,DGS10,DGS2'),
            valid.replace('# series: ', '# series: []\n# duplicate: '),
            '# format: "duplicate"\n' + valid,
            'date,DGS2\n2024-09-16,4\n',
            '', '{}', 'not csv',
        ]
        for index, content in enumerate(mutations):
            with self.subTest(mutation=index):
                self.path.write_text(content)
                with self.assertRaises(ValueError):
                    load_observations(self.path)
        with self.assertRaises(FileNotFoundError):
            load_observations(self.path.with_name("missing.csv"))

    def test_invalid_metadata_does_not_truncate_existing_snapshot(self):
        save_observations(example_frame(), self.path)
        previous = self.path.read_bytes()
        data = example_frame()
        data.attrs["metadata"]["bad header"] = "invalid"
        with self.assertRaises(ValueError):
            save_observations(data, self.path)
        self.assertEqual(self.path.read_bytes(), previous)

    def test_invalid_in_memory_data(self):
        data = example_frame()
        data.index = ["2024-09-16", "2025-01-13"]
        with self.assertRaises(ValueError):
            validate_observations(data)
        for value in (np.inf, -np.inf):
            data = example_frame()
            data.iloc[0, 0] = value
            with self.assertRaises(ValueError):
                validate_observations(data)
        with self.assertRaises(ValueError):
            FredDataManager(self.path).load_or_download("auto")
        with self.assertRaises(ValueError):
            FredDataManager(self.path).report()


class DownloadTests(unittest.TestCase):
    def test_public_download_save_and_file_equivalence(self):
        csv = b"observation_date,DGS2,DGS10,DGS30\n2024-09-13,3,4,5\n2024-09-16,3.56,3.63,\n2025-01-13,4.40,4.79,4.97\n2025-01-14,4,5,6\n"
        with tempfile.TemporaryDirectory() as temp, patch.dict("os.environ", {}, clear=True), \
             patch("bondview.data.fred._read_url", return_value=csv) as reader:
            manager = FredDataManager(Path(temp) / "cache.csv")
            data = manager.load_or_download("download", "2024-09-16", "2025-01-13")
            self.assertEqual(len(data), 2)
            self.assertEqual(reader.call_count, 1)
            self.assertTrue(pd.isna(data.iloc[0].DGS30))
            self.assertIn("public graph CSV", manager.metadata["transport"])
            with patch("bondview.data.fred._read_url", side_effect=AssertionError("No network")):
                loaded = manager.load_or_download("file")
        pd.testing.assert_frame_equal(analyze_curve(data, *data.index), analyze_curve(loaded, *loaded.index))
        self.assertEqual(analyze_curve(loaded, *loaded.index).iloc[3].change_bp, 32)

    def test_api_requests_native_units_and_frequency_without_transformation(self):
        infos = {"RATE": ("Percent", "M"), "FX": ("Won per U.S. Dollar", "D"), "INDEX": ("Index", "Q")}
        def response(endpoint, key, **params):
            self.assertEqual(key, "secret-test-key")
            s = params["series_id"]
            if endpoint == "series":
                units, freq = infos[s]
                return {"seriess": [{"units": units, "frequency_short": freq, "title": s, "last_updated": "test"}]}
            self.assertEqual(params["units"], "lin")
            self.assertNotIn("frequency", params)
            self.assertEqual(params["observation_start"], "2024-01-01")
            rows = ([{"date": "2024-01-01", "value": "101.23"}] if s == "INDEX" else
                    [{"date": "2024-01-01", "value": "4.12" if s == "RATE" else "."},
                     {"date": "2024-02-01", "value": "4.13" if s == "RATE" else "1234.5"}])
            return {"count": len(rows), "realtime_start": "2026-10-26", "realtime_end": "2026-10-26", "observations": rows}
        with patch("bondview.data.fred._api_json", side_effect=response) as mocked:
            data = download_fred("2024-01-01", "2024-02-01", api_key="secret-test-key", series_ids=tuple(infos))
        self.assertEqual(mocked.call_count, 6)
        self.assertTrue(pd.isna(data.iloc[0].FX))
        self.assertTrue(pd.isna(data.iloc[1].INDEX))
        self.assertEqual(data.iloc[0].RATE, 4.12)
        for s, (units, frequency) in infos.items():
            self.assertEqual(data.attrs["metadata"]["series"][s]["units"], units)
            self.assertEqual(data.attrs["metadata"]["series"][s]["frequency"], frequency)
        self.assertNotIn("secret-test-key", str(data.attrs))

    def test_key_environment_precedence_and_dotenv(self):
        with tempfile.TemporaryDirectory() as temp:
            env = Path(temp) / ".env"
            env.write_text("FRED_API_KEY=dotenv-test-key\n")
            for explicit, environment, expected in (
                (None, {}, "dotenv-test-key"),
                (None, {"FRED_API_KEY": "environment-test-key"}, "environment-test-key"),
                ("explicit-test-key", {"FRED_API_KEY": "environment-test-key"}, "explicit-test-key"),
            ):
                with patch.dict("os.environ", environment, clear=True), \
                     patch("bondview.data.fred._api_json", side_effect=RuntimeError("stop")) as mocked:
                    with self.assertRaises(RuntimeError):
                        download_fred(env_path=env, api_key=explicit)
                    self.assertEqual(mocked.call_args.args[1], expected)

    def test_api_rejects_truncation_and_missing_measurement_metadata(self):
        info = {"units": "Percent", "frequency_short": "D", "title": "Test", "last_updated": "test"}
        for field, bad in (("units", ""), ("frequency_short", "")):
            with self.subTest(field=field), patch("bondview.data.fred._api_json", side_effect=[
                {"seriess": [{**info, field: bad}]},
                {"count": 1, "observations": [{"date": "2024-01-01", "value": "4"}]},
            ]):
                with self.assertRaises(ValueError):
                    download_fred(api_key="test", series_ids=["TEST"])
        with patch("bondview.data.fred._api_json", side_effect=[{"seriess": [info]}, {"count": 2, "observations": []}]):
            with self.assertRaises(ValueError):
                download_fred(api_key="test")

    def test_request_failures_do_not_leak_credentials(self):
        with patch("bondview.data.fred.urlopen", side_effect=OSError("url includes secret-key")):
            with self.assertRaises(RuntimeError) as error:
                download_fred(api_key="secret-key")
        self.assertNotIn("secret-key", str(error.exception))

    def test_download_rejects_invalid_inputs_before_network(self):
        with patch.dict("os.environ", {}, clear=True), \
             patch("bondview.data.fred._read_url", side_effect=AssertionError("No request expected")):
            for kwargs in ({"start": "2025-01-13", "end": "2024-09-16"}, {"series_ids": []},
                           {"series_ids": ["DGS2", "DGS2"]}, {"series_ids": ["DGS2&bad"]},
                           {"series_ids": ["DEXKOUS"]}):
                with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                    download_fred(**kwargs)


if __name__ == "__main__":
    unittest.main()
