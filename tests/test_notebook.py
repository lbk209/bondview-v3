"""Fresh-kernel notebook tests with real DatePickers and blocked anywidget."""

import ast
from pathlib import Path
import tempfile
import unittest

from nbclient import NotebookClient
import nbformat

from bondview.data.fred import save_observations
from test_treasury_curve import example_frame

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "notebooks/analysis1_curve.ipynb"


class NotebookTests(unittest.TestCase):
    def test_concise_manual_steps_use_widgets_directly(self):
        notebook = nbformat.read(NOTEBOOK, as_version=4)
        sources = [c.source for c in notebook.cells if c.cell_type == "code"]
        self.assertEqual(len(sources), 5)  # Configuration, A, B, C, D.
        for forbidden in ("DISPLAY_START", "DISPLAY_END", "FigureWidget", "anywidget", ".observe(", "on_click", "Dash"):
            self.assertNotIn(forbidden, "\n".join(sources))
        for source in sources:
            tree = ast.parse(source)
            self.assertFalse(any(isinstance(n, (ast.If, ast.For, ast.While, ast.Try, ast.FunctionDef, ast.ClassDef))
                                 for n in ast.walk(tree)))
        self.assertIn("start_picker.value, end_picker.value", sources[3])
        self.assertIn("start_picker.value, end_picker.value", sources[4])
        self.assertIn("widgets.DatePicker", sources[2])
        self.assertIn("date_picker_defaults(observations)", sources[2])

    def test_both_modes_and_independent_manual_reruns_without_anywidget(self):
        for mode in ("file", "download"):
            with self.subTest(mode=mode), tempfile.TemporaryDirectory() as temp:
                path = Path(temp) / "fixture.csv"
                save_observations(example_frame(), path)
                notebook = nbformat.read(NOTEBOOK, as_version=4)
                configuration = next(c for c in notebook.cells if c.cell_type == "code")
                configuration.source += f'\nDATA_MODE = {mode!r}\nDATA_PATH = Path({str(path)!r})\nPROJECT_ROOT = Path({str(ROOT)!r})'
                plot_source = next(c.source for c in notebook.cells if c.cell_type == "code" and c.source.startswith("history_figure ="))
                analysis_source = next(c.source for c in notebook.cells if c.cell_type == "code" and c.source.startswith("result ="))
                setup = '''
import importlib.abc
import sys
from datetime import date
class BlockAnywidget(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname == "anywidget" or fullname.startswith("anywidget."):
            raise AssertionError("Notebook must run without anywidget")
sys.meta_path.insert(0, BlockAnywidget())
import bondview.data.fred as fred_transport
transport_calls = []
def fixture_request(url):
    transport_calls.append(url)
    return b"observation_date,DGS2,DGS10,DGS30\\n2024-09-16,3.56,3.63,3.94\\n2025-01-13,4.40,4.79,4.97\\n"
def reject_network(url):
    raise AssertionError("Unexpected network request")
fred_transport._read_url = fixture_request if MODE == "download" else reject_network
import os
os.environ.pop("FRED_API_KEY", None)
'''.replace('MODE', repr(mode))
                notebook.cells.insert(0, nbformat.v4.new_code_cell(setup))
                def add(source):
                    notebook.cells.append(nbformat.v4.new_code_cell(source))
                add('''
import plotly.graph_objects as go
assert result.change_bp.tolist() == [84, 116, 103, 32, -13]
assert type(history_figure) is go.Figure
assert list(history_figure.layout.xaxis.range) == ["2024-09-16", "2025-01-13"]
assert start_picker.value.isoformat() == "2024-09-16"
assert end_picker.value.isoformat() == "2025-01-13"
assert len(transport_calls) == (1 if DATA_MODE == "download" else 0)
fred_transport._read_url = reject_network
# Change BOTH widgets, then rerun only the plot cell.
start_picker.value = date(2024, 10, 1)
end_picker.value = date(2025, 1, 1)
''')
                add(plot_source)
                add('''
assert list(history_figure.layout.xaxis.range) == ["2024-10-01", "2025-01-01"]
assert result.attrs["start"] == "2024-09-16"  # Analysis was not rerun.
# Change dates again, then rerun only analysis, leaving an older plot in place.
start_picker.value = date(2024, 9, 15)  # Sunday, no substitution.
end_picker.value = date(2025, 1, 13)
''')
                add(analysis_source)
                add('''
assert result.change_bp.isna().all()
assert result.end.notna().all()
assert result.attrs["start"] == "2024-09-15"
assert result.attrs["end"] == "2025-01-13"
assert list(history_figure.layout.xaxis.range) == ["2024-10-01", "2025-01-01"]
# Figure zoom/pan/range changes have no path to selected widget dates.
history_figure.update_xaxes(range=["2024-12-01", "2024-12-31"])
assert start_picker.value == date(2024, 9, 15)
assert end_picker.value == date(2025, 1, 13)
''')
                add(analysis_source)
                add('''
assert result.attrs["start"] == "2024-09-15"
assert result.change_bp.isna().all()
# Restore both endpoints and rerun both output cells.
start_picker.value = date(2024, 9, 16)
''')
                add(plot_source)
                add(analysis_source)
                add('''
assert result.change_bp.tolist() == [84, 116, 103, 32, -13]
assert list(history_figure.layout.xaxis.range) == ["2024-09-16", "2025-01-13"]
assert history_figure.layout.xaxis.rangeslider.visible
assert len(transport_calls) == (1 if DATA_MODE == "download" else 0)
assert "anywidget" not in sys.modules
''')
                NotebookClient(notebook, timeout=90, kernel_name="python3").execute(cwd=temp)
                self.assertFalse(any(output.output_type == "error" for cell in notebook.cells
                                     if cell.cell_type == "code" for output in cell.outputs))


if __name__ == "__main__":
    unittest.main()
