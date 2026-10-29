"""Execute the current Treasury notebook offline with saved per-ID snapshots."""

import ast
from pathlib import Path
import tempfile
import unittest

from nbclient import NotebookClient
import nbformat

from bondview.data.fred import save_observations
from test_treasury_curve import example_frame
from test_kw_decomposition import kw_frame

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "notebooks/analysis1_treasury_market.ipynb"


def offline_notebook(directory):
    """Skip the existing optional acquisition section in the execution copy only."""
    notebook = nbformat.read(NOTEBOOK, as_version=4)
    first = next(i for i, c in enumerate(notebook.cells) if c.source.startswith("### Donwload"))
    last = next(i for i, c in enumerate(notebook.cells) if c.source.startswith("### Load Treasury"))
    del notebook.cells[first:last]
    config = next(c for c in notebook.cells if c.cell_type == "code" and "SNAPSHOT_DIR =" in c.source)
    config.source = config.source.replace('SNAPSHOT_DIR = PROJECT_ROOT / "data/fred"', f'SNAPSHOT_DIR = Path({str(directory)!r})')
    return notebook


class NotebookTests(unittest.TestCase):
    def test_explicit_acquisition_and_current_sections(self):
        notebook = nbformat.read(NOTEBOOK, as_version=4)
        sources = [c.source for c in notebook.cells if c.cell_type == "code"]
        code = "\n".join(sources)
        markdown = "\n".join(c.source for c in notebook.cells if c.cell_type == "markdown")
        for forbidden in ("DATA_MODE", "load_or_download", "FigureWidget", "anywidget", ".observe(", "on_click"):
            self.assertNotIn(forbidden, code)
        calls = [n for source in sources for n in ast.walk(ast.parse(source)) if isinstance(n, ast.Call)]
        self.assertTrue(any(isinstance(n.func, ast.Attribute) and n.func.attr == "download" for n in calls))
        self.assertIn('fred.download(series_ids=FRED_SERIES, start=start, end=end)', code)
        self.assertIn('fred.save()', code)
        self.assertIn('DateRangePicker(observations)', code)
        self.assertIn('fred.load(series_ids=["DGS2", "DGS10", "DGS30"])', code)
        self.assertIn('yield_change_tolerance_bp=5', code)
        self.assertIn('slope_tolerance_bp=5', code)
        self.assertIn('start = None\nend = None', code)
        for series_id in ("DGS2", "DGS10", "DGS30", "THREEFY2", "THREEFYTP2", "THREEFY10", "THREEFYTP10"):
            self.assertIn(f'"{series_id}"', code)
        b_index = next(i for i,c in enumerate(notebook.cells) if c.source.startswith('## B.'))
        c_index = next(i for i,c in enumerate(notebook.cells) if c.source.startswith('## C.'))
        b_code = "\n".join(c.source for c in notebook.cells[b_index:c_index] if c.cell_type == "code")
        self.assertIn('kw_observations = fred.load(', b_code)
        self.assertIn('analyze_kw_decomposition(kw_observations, *date_range.get_dates())', b_code)
        self.assertEqual(code.count('DateRangePicker('), 1)
        self.assertTrue(all(c.cell_type == "markdown" for c in notebook.cells[c_index:]))
        self.assertIn('## C. Conditional joint yield movements', markdown)
        self.assertTrue(all(not c.outputs and c.execution_count is None
                            for c in notebook.cells[b_index:c_index] if c.cell_type == "code"))

    def test_offline_execution_and_independent_widget_reruns(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp) / 'fred'
            for fixture in (example_frame(), kw_frame()):
                for series in fixture.columns:
                    metadata = {series: fixture.attrs["metadata"][series]}
                    day = metadata[series]["retrieved_at_utc"][:10].replace("-", "")
                    save_observations(fixture[[series]], directory / f"{series}_{day}.csv", metadata=metadata)
            before = {p.name:p.read_bytes() for p in directory.iterdir()}
            notebook = offline_notebook(directory)
            plot_source = next(c.source for c in notebook.cells if c.cell_type == 'code' and c.source.startswith('history_figure ='))
            kw_source = next(c.source for c in notebook.cells if c.cell_type == 'code' and 'kw_results = ' in c.source)
            analysis_source = next(c.source for c in notebook.cells if c.cell_type == 'code' and c.source.startswith('result ='))
            notebook.cells.insert(0, nbformat.v4.new_code_cell('''
import importlib.abc
import sys
from datetime import date
class BlockAnywidget(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname == "anywidget" or fullname.startswith("anywidget."):
            raise AssertionError("Notebook must run without anywidget")
sys.meta_path.insert(0, BlockAnywidget())
import bondview.data.fred as fred_transport
def reject_network(*args, **kwargs):
    raise AssertionError("Normal notebook execution must stay offline")
fred_transport._read_url = reject_network
fred_transport.download_fred = reject_network
fred_transport.dotenv_values = reject_network
'''))
            def add(source):
                notebook.cells.append(nbformat.v4.new_code_cell(source))
            add('''
import pandas as pd
import plotly.graph_objects as go
assert result.change_bp.tolist() == [84, 116, 103, 32, -13]
assert result.iloc[3].movement == "bear"
assert result.iloc[4].slope == "flattening"
assert type(history_figure) is go.Figure
assert list(history_figure.layout.xaxis.range) == ["2024-09-16", "2025-01-13"]
assert date_range.get_dates() == (date(2024, 9, 16), date(2025, 1, 13))
assert fred.snapshot_dates == dict.fromkeys(("THREEFY2", "THREEFYTP2", "THREEFY10", "THREEFYTP10"), "20261029")
assert len(kw_figures) == 2
for maturity, figure in kw_figures.items():
    assert type(figure) is go.Figure
    assert len(figure.data) == 5
    assert len(kw_results[maturity]) == 4
    assert figure.layout.hoversubplots == "axis"
# Change widgets and rerun only the plot.
date_range.start_picker.value = date(2024, 10, 1)
date_range.end_picker.value = date(2025, 1, 1)
''')
            add(plot_source)
            add('''
assert list(history_figure.layout.xaxis.range) == ["2024-10-01", "2025-01-01"]
assert result.attrs["start"] == "2024-09-16"
# The existing analysis uses first/last available dates inside the interval.
date_range.start_picker.value = date(2024, 9, 15)
date_range.end_picker.value = date(2025, 1, 13)
''')
            add(analysis_source)
            add('''
assert result.change_bp.tolist() == [84, 116, 103, 32, -13]
assert result.attrs["start"] == "2024-09-16"
assert list(history_figure.layout.xaxis.range) == ["2024-10-01", "2025-01-01"]
history_figure.update_xaxes(range=["2024-12-01", "2024-12-31"])
assert date_range.start_picker.value == date(2024, 9, 15)
assert date_range.end_picker.value == date(2025, 1, 13)
# A missing tenor at an available endpoint remains missing in the result.
observations.loc[pd.Timestamp("2024-09-16"), "DGS30"] = float("nan")
''')
            add(analysis_source)
            add('''
assert pd.isna(result.loc["DGS30", "change_bp"])
assert result.loc["DGS10_DGS2", "change_bp"] == 32
assert "anywidget" not in sys.modules
''')
            add('''
date_range.start_picker.value = date(2024, 12, 22)
date_range.end_picker.value = date(2024, 12, 28)
''')
            add(kw_source)
            add('''
import numpy as np
assert kw_results["2Y"].index.tolist() == list(pd.to_datetime(["2024-12-23", "2024-12-24", "2024-12-27"]))
np.testing.assert_allclose(kw_results["2Y"].expected_change_bp, [0, -40, -25], atol=1e-12)
assert list(kw_figures["10Y"].layout.xaxis.range) == ["2024-12-23", "2024-12-27"]
# Rerunning B leaves A's previously computed result and figure alone.
assert pd.isna(result.loc["DGS30", "change_bp"])
assert list(history_figure.layout.xaxis.range) == ["2024-12-01", "2024-12-31"]
''')
            NotebookClient(notebook, timeout=90, kernel_name="python3").execute(cwd=temp)
            self.assertFalse(any(output.output_type == "error" for cell in notebook.cells
                                 if cell.cell_type == "code" for output in cell.outputs))
            self.assertEqual(before, {p.name:p.read_bytes() for p in directory.iterdir()})


if __name__ == "__main__":
    unittest.main()
