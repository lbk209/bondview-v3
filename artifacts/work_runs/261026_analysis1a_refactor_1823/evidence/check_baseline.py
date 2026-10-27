"""Compare the refactor with PR #36's financial module, without network access.

Run from repository root with `poetry run python <this file>`. Requires the
baseline commit in local Git history; no financial source is duplicated here.
"""

from importlib.util import module_from_spec, spec_from_file_location
from itertools import product
import json
from pathlib import Path
import subprocess
import tempfile

import numpy as np
import pandas as pd

from bondview.analysis.treasury_curve import analyze_curve
from bondview.data.fred import FredDataManager, SERIES, save_observations
from bondview.presentation.treasury_curve import display_table, interpret_curve

BASELINE = "98bf94087ab52ec6ada23dd5cbec031155dcd22d"
ROOT = Path(__file__).resolve().parents[4]
RUN = Path(__file__).resolve().parents[1]


def main():
    source = subprocess.check_output(
        ["git", "show", f"{BASELINE}:src/bondview/analysis/treasury_curve.py"], cwd=ROOT, text=True,
    )
    comparisons = 0
    with tempfile.TemporaryDirectory() as temp:
        module_path = Path(temp) / "baseline.py"
        module_path.write_text(source)
        spec = spec_from_file_location("baseline_curve", module_path)
        baseline = module_from_spec(spec)
        spec.loader.exec_module(baseline)
        def compare(data, start, end, tolerance=0.0):
            nonlocal comparisons
            old = baseline.analyze_curve(data, start, end, tolerance)
            new = analyze_curve(data, start, end, tolerance)
            pd.testing.assert_frame_equal(old[["start", "end", "change_bp", "level_unit"]].reset_index(drop=True),
                                          new[["start", "end", "change_bp", "level_unit"]].reset_index(drop=True),
                                          check_exact=True)
            pd.testing.assert_frame_equal(baseline.display_table(old), display_table(new), check_exact=True)
            assert baseline.interpret_curve(old) == interpret_curve(new)
            comparisons += 1
            return new
        data = pd.DataFrame([[4., 4.5, 5.], [4., 4.5, 5.]], columns=SERIES,
                            index=pd.to_datetime(["2024-09-16", "2025-01-13"]))
        data.index.name = "date"
        data.attrs["metadata"] = {"source": "Synthetic regression fixture", "retrieved_at_utc": "2026-10-26T00:00:00+00:00",
                                  "series": {s: {"units": "Percent", "frequency": "D"} for s in SERIES}}
        for changes in product((-20, -10, 0, 10, 20), repeat=3):
            data.iloc[1] = data.iloc[0] + np.array(changes) / 100
            for tolerance in (0, 9.99, 10, 20):
                compare(data, *data.index, tolerance)
        for endpoint, tenor in product(range(2), range(3)):
            partial = data.copy()
            partial.iloc[endpoint, tenor] = np.nan
            compare(partial, *partial.index)
        for start, end in (("2024-09-15", "2025-01-13"), ("2024-09-16", "2025-01-12"),
                           ("2024-09-16", "2024-09-16"), ("2023-01-01", "2024-12-25")):
            compare(data, start, end)
        synthetic_comparisons = comparisons
        # Reuse the baseline's archived real snapshot; retain retrieval metadata,
        # never claim it was newly downloaded or overwrite its historical file.
        archive = ROOT / "artifacts/work_runs/261026_analysis1a_1000/evidence/real_fred.json"
        payload = json.loads(archive.read_text())
        # Reconstruct just the two observed endpoints from the committed table.
        # The original full cache is intentionally not a required input.
        table = pd.read_csv(ROOT / "artifacts/work_runs/261026_analysis1a_1000/examples/real_fred_comparison.csv")
        real = pd.DataFrame([
            [float(v.rstrip("%")) for v in table.iloc[:3, 1]],
            [float(v.rstrip("%")) for v in table.iloc[:3, 2]],
        ], columns=SERIES, index=pd.to_datetime(["2024-09-16", "2025-01-13"]))
        real.index.name = "date"
        real.attrs["metadata"] = payload["metadata"]
        path = Path(temp) / "historical_snapshot.csv"
        save_observations(real, path)
        manager = FredDataManager(path)
        reloaded = manager.load_or_download("file")
        pd.testing.assert_frame_equal(real, reloaded, check_exact=True)
        assert manager.metadata == payload["metadata"]
        result = compare(reloaded, "2024-09-16", "2025-01-13")
        assert result.change_bp.tolist() == [84, 116, 103, 32, -13]
        result.to_csv(RUN / "examples/archived_real_results.csv")
        display_table(result).to_csv(RUN / "examples/archived_real_display.csv")
        # Keep a small auditable self-contained endpoint CSV, not another cache.
        save_observations(reloaded.loc[["2024-09-16", "2025-01-13"]], RUN / "examples/archived_real_endpoints.csv")
        summary = {"baseline_commit": BASELINE, "synthetic_comparisons": synthetic_comparisons,
                   "archived_real_comparisons": 1, "numeric_differences": 0,
                   "formatted_table_differences": 0, "interpretation_differences": 0,
                   "archived_endpoint_rows_roundtripped": len(real),
                   "archived_retrieved_at_utc": manager.metadata["retrieved_at_utc"],
                   "archived_change_bp": result.change_bp.tolist(),
                   "fresh_market_retrieval": False}
        (RUN / "evidence/baseline_comparison.json").write_text(json.dumps(summary, indent=2) + "\n")
        print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
