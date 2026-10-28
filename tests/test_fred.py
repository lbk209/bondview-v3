"""CSV/provenance, shared units/frequencies and credential handling tests."""

from io import StringIO
from pathlib import Path
import tempfile
import unittest
import warnings
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
        manager = FredDataManager(self.path.parent, series_ids=tuple(metadata["series"]))
        data = validate_observations(data, metadata)
        with patch("bondview.data.fred.download_fred", return_value=data):
            manager.download()
        manager.save()
        with patch("bondview.data.fred._read_url", side_effect=AssertionError("No network")), \
             patch("bondview.data.fred.dotenv_values", side_effect=AssertionError("No credentials")):
            loaded = manager.load()
        pd.testing.assert_frame_equal(validate_observations(data, metadata), loaded, check_exact=True)
        loaded.attrs.clear()
        self.assertEqual(manager.metadata["series"]["RATE"]["provenance"]["source"], metadata["source"])
        copy = manager.metadata
        copy["series"]["RATE"]["units"] = "broken"
        self.assertEqual(manager.metadata["series"]["RATE"]["provenance"]["source"], metadata["source"])
        with patch("sys.stdout", new_callable=StringIO) as output:
            manager.report()
        self.assertIn("Won per U.S. Dollar, D", output.getvalue())
        self.assertIn("Index 2017=100, Q", output.getvalue())
        with self.assertRaises(RuntimeError):
            manager.save()
        for series_id in metadata["series"]:
            saved = load_observations(self.path.parent / f"{series_id}_20261026.csv")
            self.assertEqual(saved.attrs["metadata"]["series"], {series_id: metadata["series"][series_id]})

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
            FredDataManager(self.path, series_ids=["../bad"])
        with self.assertRaises(ValueError):
            FredDataManager(self.path).report()


class DownloadTests(unittest.TestCase):
    def test_public_download_save_and_file_equivalence(self):
        csv = b"observation_date,DGS2,DGS10,DGS30\n2024-09-13,3,4,5\n2024-09-16,3.56,3.63,\n2025-01-13,4.40,4.79,4.97\n2025-01-14,4,5,6\n"
        with tempfile.TemporaryDirectory() as temp, patch.dict("os.environ", {}, clear=True), \
             patch("bondview.data.fred._read_url", return_value=csv) as reader:
            manager = FredDataManager(Path(temp))
            data = manager.download("2024-09-16", "2025-01-13")
            manager.save()
            self.assertEqual(len(data), 2)
            self.assertEqual(reader.call_count, 1)
            self.assertTrue(pd.isna(data.iloc[0].DGS30))
            self.assertIn("public graph CSV", manager.metadata["transport"])
            with patch("bondview.data.fred._read_url", side_effect=AssertionError("No network")):
                loaded = manager.load()
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

class SnapshotTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name) / "fred"
        self.manager = FredDataManager(self.directory)

    def snapshot(self, series_id, day="20261026", values=(1., np.nan, 3.), dates=None):
        dates = dates or ["2024-01-01", "2024-01-02", "2024-01-03"]
        metadata = {
            "source": f"Controlled source {series_id}",
            "retrieved_at_utc": f"{day[:4]}-{day[4:6]}-{day[6:]}T23:30:00+00:00",
            "transport": "fixture; no live network",
            "series": {series_id: {"units": "Index" if series_id == "Other_ID" else "Percent",
                                   "frequency": "M" if series_id == "Other_ID" else "D",
                                   "source_url": f"https://fred.stlouisfed.org/series/{series_id}",
                                   "last_updated": "fixture"}},
        }
        data = pd.DataFrame({series_id: values}, index=pd.to_datetime(dates))
        return save_observations(data, self.directory / f"{series_id}_{day}.csv", metadata=metadata)

    def accept_download(self, data=None):
        data = example_frame() if data is None else data
        with patch("bondview.data.fred.download_fred", return_value=data) as request:
            downloaded = self.manager.download(series_ids=list(data.columns))
        request.assert_called_once_with(None, None, api_key=None, env_path=None, series_ids=tuple(data.columns))
        return downloaded

    def test_download_is_memory_only_save_separate_and_provenance_roundtrip(self):
        original = self.accept_download()
        self.assertFalse(self.directory.exists())
        paths = self.manager.save()
        self.assertEqual(set(paths), set(SERIES))
        original_metadata = self.manager.metadata
        for series_id, path in paths.items():
            self.assertEqual(path.name, f"{series_id}_20261026.csv")
            one = load_observations(path)
            self.assertEqual(list(one.columns), [series_id])
            self.assertEqual(one.attrs["metadata"]["series"], {series_id: original_metadata["series"][series_id]})
        with patch("bondview.data.fred._read_url", side_effect=AssertionError("Offline")), \
             patch("bondview.data.fred.dotenv_values", side_effect=AssertionError("No key lookup")):
            loaded = self.manager.load(series_ids=SERIES)
        pd.testing.assert_frame_equal(original, loaded)
        pd.testing.assert_frame_equal(analyze_curve(original, *original.index), analyze_curve(loaded, *loaded.index))
        self.assertNotIn("retrieved_at_utc", self.manager.metadata)
        for series_id in SERIES:
            info = self.manager.metadata["series"][series_id]
            self.assertEqual(info["provenance"], {k: v for k, v in original_metadata.items() if k != "series"})
        loaded.attrs.clear()
        self.manager.validate()
        copy = self.manager.metadata
        copy["series"]["DGS2"]["provenance"]["source"] = "tampered"
        self.assertNotEqual(copy, self.manager.metadata)
        with self.assertRaises(RuntimeError):
            self.manager.save()

    def test_collision_preflight_protects_every_existing_file(self):
        self.accept_download()
        existing = self.snapshot("DGS10")
        before = existing.read_bytes()
        with self.assertRaisesRegex(FileExistsError, "refusing to overwrite"):
            self.manager.save()
        self.assertEqual(existing.read_bytes(), before)
        self.assertEqual(list(self.directory.iterdir()), [existing])

    def test_failed_serialization_and_publication_leave_no_partial_batch(self):
        self.accept_download()
        self.manager._metadata["bad header"] = "invalid"
        with self.assertRaisesRegex(ValueError, "header"):
            self.manager.save()
        self.assertEqual(list(self.directory.iterdir()), [])
        self.accept_download()
        import os
        link = os.link
        def fail_second(source, target):
            if Path(target).name.startswith("DGS10_"):
                raise OSError("Controlled publication failure")
            link(source, target)
        with patch("bondview.data.fred.os.link", side_effect=fail_second):
            with self.assertRaisesRegex(OSError, "Controlled"):
                self.manager.save()
        self.assertEqual(list(self.directory.iterdir()), [])

    def test_business_day_index_frequency_is_not_a_csv_source_frequency(self):
        data = example_frame()
        data.index = pd.date_range("2024-01-01", periods=2, freq="B", name="date")
        original = self.accept_download(data)
        self.manager.save()
        loaded = self.manager.load()
        # Source frequency is explicit metadata; pandas' inferred index.freq
        # is transient and is not serialized by the existing CSV format.
        pd.testing.assert_frame_equal(original, loaded, check_exact=True, check_freq=False)
        self.assertEqual(self.manager.metadata["series"]["DGS2"]["frequency"], "D")

    def test_publication_race_does_not_replace_or_remove_competing_file(self):
        self.accept_download()
        import os
        link = os.link
        competing = self.directory / "DGS10_20261026.csv"
        def race(source, target):
            if Path(target) == competing:
                competing.write_text("Created by another writer")
            link(source, target)
        with patch("bondview.data.fred.os.link", side_effect=race):
            with self.assertRaises(FileExistsError):
                self.manager.save()
        self.assertEqual(competing.read_text(), "Created by another writer")
        self.assertEqual(list(self.directory.iterdir()), [competing])

    def test_utc_filename_retains_previous_snapshots(self):
        data = example_frame()
        data.attrs["metadata"]["retrieved_at_utc"] = "2026-10-28T00:30:00+09:00"
        self.accept_download(data)
        paths = self.manager.save()
        self.assertTrue(all(p.name.endswith("_20261027.csv") for p in paths.values()))
        data.attrs["metadata"]["retrieved_at_utc"] = "2026-10-28T01:00:00+00:00"
        self.accept_download(data)
        self.manager.save()
        self.assertEqual(len(list(self.directory.glob("*.csv"))), 6)
        self.manager.load()
        self.assertEqual(set(self.manager.snapshot_dates.values()), {"20261028"})

    def test_latest_selected_independently_and_mismatch_warning(self):
        self.snapshot("DGS2", "20261025")
        self.snapshot("DGS2", "20261028", values=(4., 5., 6.))
        self.snapshot("Other_ID", "20261027", values=(8., np.nan), dates=["2024-01-02", "2024-01-04"])
        with self.assertWarnsRegex(UserWarning, "DGS2: 20261028\\nOther_ID: 20261027"):
            loaded = self.manager.load(series_ids=["DGS2", "Other_ID"])
        self.assertEqual(loaded.index.strftime("%Y-%m-%d").tolist(), ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04"])
        self.assertEqual(loaded.DGS2.iloc[0], 4)
        self.assertTrue(pd.isna(loaded.Other_ID.iloc[0]))
        self.assertTrue(pd.isna(loaded.Other_ID.iloc[-1]))
        self.assertTrue(pd.isna(loaded.DGS2.iloc[-1]))
        self.assertEqual(self.manager.metadata["series"]["Other_ID"]["frequency"], "M")
        with patch("sys.stdout", new_callable=StringIO) as output:
            self.manager.report()
        text = output.getvalue()
        self.assertIn("2026-10-28T23:30:00+00:00", text)
        self.assertIn("2026-10-27T23:30:00+00:00", text)
        self.assertIn("Other_ID: Index, M", text)
        self.assertIn("missing: 3", text)
        self.assertIn("2024-01-02 to 2024-01-02 | 1 dates", text)

    def test_matching_dates_no_warning_common_coverage_with_holes(self):
        self.snapshot("DGS2", values=(1., np.nan, 3.))
        self.snapshot("DGS10", values=(2., 2., 4.))
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            self.manager.load(series_ids=["DGS2", "DGS10"])
        self.assertEqual(caught, [])
        with patch("sys.stdout", new_callable=StringIO) as output:
            self.manager.report()
        self.assertIn("2024-01-01 to 2024-01-03 | 2 dates", output.getvalue())
        self.assertIn("intervening dates may be incomplete", output.getvalue())

    def test_report_no_common_and_all_missing_series(self):
        self.snapshot("DGS2", values=(np.nan, np.nan, np.nan))
        self.snapshot("DGS10")
        self.manager.load(series_ids=["DGS2", "DGS10"])
        with patch("sys.stdout", new_callable=StringIO) as output:
            self.manager.report()
        self.assertIn("No common complete observations", output.getvalue())
        self.assertIn("No nonmissing observations", output.getvalue())
        self.assertIn("missing: 3", output.getvalue())

    def test_download_report_is_unsaved_and_uses_retrieval_metadata(self):
        self.accept_download()
        with patch("sys.stdout", new_callable=StringIO) as output:
            self.manager.report()
        self.assertIn("Not loaded from a saved snapshot", output.getvalue())
        self.assertIn("2026-10-26T00:00:00+00:00", output.getvalue())
        self.assertIn("DGS2, DGS10, DGS30", output.getvalue())

    def test_missing_invalid_identity_dates_and_corrupt_latest_fail_clearly(self):
        with self.assertRaisesRegex(FileNotFoundError, "UNAVAILABLE"):
            self.manager.load(series_ids=["UNAVAILABLE"])
        old = self.snapshot("DGS2")
        latest = self.directory / "DGS2_20261028.csv"
        latest.write_text("malformed")
        with self.assertRaisesRegex(ValueError, "DGS2_20261028.csv"):
            self.manager.load(series_ids=["DGS2"])
        latest.write_bytes(old.read_bytes())
        with self.assertRaisesRegex(ValueError, "retrieval date"):
            self.manager.load(series_ids=["DGS2"])
        latest.unlink()
        content = old.read_text()
        for bad in (content.replace('DGS2', 'DGS10'), content.replace('1.0', 'inf')):
            old.write_text(bad)
            with self.assertRaisesRegex(ValueError, "DGS2.*invalid snapshot"):
                self.manager.load(series_ids=["DGS2"])
        old.write_text(content)
        for name in ("DGS2_20260230.csv", "DGS2_latest.csv"):
            path = self.directory / name
            path.write_text(content)
            with self.assertRaisesRegex(ValueError, "filename|snapshot date"):
                self.manager.load(series_ids=["DGS2"])
            path.unlink()
        for kwargs in ({"start":"2025-01-01","end":"2024-01-01"}, {"start":"2025-01-01"}):
            with self.assertRaisesRegex(ValueError, "Start|No observations"):
                self.manager.load(series_ids=["DGS2"], **kwargs)

    def test_api_arbitrary_ids_full_history_subset_no_file_or_key_leak(self):
        def response(endpoint, key, **params):
            self.assertEqual(params["series_id"], "Other_ID")
            if endpoint == "series":
                return {"seriess":[{"id":"Other_ID","units":"Index","frequency_short":"M","title":"Other","last_updated":"fixture"}]}
            self.assertNotIn("observation_start", params)
            self.assertNotIn("observation_end", params)
            return {"count":2,"observations":[{"date":"2000-01-01","value":"."},{"date":"2000-02-01","value":"12.123456789012345"}]}
        with patch("bondview.data.fred._api_json", side_effect=response) as request:
            self.manager.download(series_ids=["Other_ID"], api_key="secret-test-key")
        self.assertEqual(request.call_count, 2)
        self.assertFalse(self.directory.exists())
        self.manager.save()
        with patch("sys.stdout", new_callable=StringIO) as output:
            self.manager.report()
        self.assertNotIn("secret-test-key", output.getvalue())
        self.assertNotIn("secret-test-key", next(self.directory.iterdir()).read_text())
        loaded = self.manager.load(series_ids=["Other_ID"])
        self.assertTrue(pd.isna(loaded.iloc[0,0]))
        self.assertEqual(loaded.iloc[1,0], 12.123456789012345)

    def test_failed_download_cannot_save_previous_state(self):
        self.accept_download()
        with patch("bondview.data.fred.download_fred", side_effect=RuntimeError("controlled")):
            with self.assertRaises(RuntimeError):
                self.manager.download()
        with self.assertRaises(RuntimeError):
            self.manager.save()
        self.assertFalse(self.directory.exists())


if __name__ == "__main__":
    unittest.main()
