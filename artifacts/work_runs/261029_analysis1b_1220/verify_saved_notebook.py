"""Execute A/B offline with local snapshots; compare A to the pre-edit baseline.

Run from the repository root using Poetry. No notebook or snapshot is written.
Only concise verification evidence is saved alongside this script.
"""

import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from unittest.mock import patch

from nbclient import NotebookClient
import nbformat

from bondview.analysis.treasury_curve import analyze_curve
from bondview.data.fred import FredDataManager
from bondview.plotting.treasury_curve import plot_yield_history

ROOT = Path(__file__).resolve().parents[3]
RUN = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "tests"))
from test_notebook import offline_notebook

BASE = "75df5635f03875b054ac10d4b74fd42b0a555743"
original = json.loads(subprocess.check_output(
    ["git", "show", f"{BASE}:notebooks/analysis1_treasury_market.ipynb"], cwd=ROOT
))
current = json.loads((ROOT / "notebooks/analysis1_treasury_market.ipynb").read_text())
# Only B gained cells: every pre-existing cell, including results, is unchanged.
old_ids = {c["id"] for c in original["cells"]}
assert [c for c in current["cells"] if c["id"] in old_ids] == original["cells"]

with patch("bondview.data.fred._read_url", side_effect=AssertionError("Offline")):
    observations = FredDataManager(ROOT / "data/fred").load()
    result = analyze_curve(observations, "2024-09-15", "2025-01-13",
                           slope_tolerance_bp=5, yield_change_tolerance_bp=5)
    figure = plot_yield_history(observations, "2024-09-15", "2025-01-13")
baseline = json.loads((RUN / "analysis1a_baseline.json").read_text())
assert result.to_json() == baseline["result"]
assert result.attrs == baseline["attrs"]
assert hashlib.sha256(figure.to_json().encode()).hexdigest() == baseline["figure_sha256"]

snapshots = ROOT / "data/fred"
before = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in snapshots.glob("*.csv")}
notebook = offline_notebook(snapshots)
notebook.cells.insert(0, nbformat.v4.new_code_cell('''
import bondview.data.fred as transport
def reject_network(*args, **kwargs):
    raise AssertionError("Saved-snapshot verification must remain offline")
transport._read_url = reject_network
transport.download_fred = reject_network
transport.dotenv_values = reject_network
'''))
notebook.cells.append(nbformat.v4.new_code_cell('''
import json
assert len(kw_results) == len(kw_figures) == 2
for maturity, path in kw_results.items():
    assert len(path) > 2
    assert len(kw_figures[maturity].data) == 5
    assert (path.iloc[0][["expected_change_bp", "premium_change_bp", "fitted_change_bp"]] == 0).all()
print("KW_EVIDENCE=" + json.dumps({
    "selected_dates": [str(d) for d in date_range.get_dates()],
    "maturities": {m: {"observations": len(p), "first": str(p.index[0].date()),
                       "last": str(p.index[-1].date()), "final_changes_bp": p.iloc[-1][[
                           "expected_change_bp", "premium_change_bp", "fitted_change_bp"]].to_dict(),
                       "figure_traces": len(kw_figures[m].data)} for m, p in kw_results.items()},
    "snapshot_dates": fred.snapshot_dates,
}))
'''))
with tempfile.TemporaryDirectory() as temp:
    NotebookClient(notebook, timeout=90, kernel_name="python3").execute(cwd=temp)
for cell in notebook.cells:
    if cell.cell_type == "code":
        assert not any(o.output_type == "error" for o in cell.outputs)
summary = next(json.loads(o.text.split("KW_EVIDENCE=", 1)[1])
               for o in notebook.cells[-1].outputs if o.output_type == "stream" and "KW_EVIDENCE=" in o.text)
after = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in snapshots.glob("*.csv")}
assert before == after
summary.update({"baseline": BASE, "analysis1a_result_and_figure_match_baseline": True,
                "all_preexisting_notebook_cells_unchanged": True,
                "executed_code_cells": sum(c.cell_type == "code" for c in notebook.cells),
                "download_cells_executed": False, "fred_network_and_credentials_blocked": True,
                "snapshots_unchanged": True, "snapshot_sha256": before,
                "interactive_hover_verified": False})
(RUN / "saved_notebook.json").write_text(json.dumps(summary, indent=2) + "\n")
print(json.dumps(summary, indent=2))
