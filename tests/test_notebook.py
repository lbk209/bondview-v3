"""Execute the delivered notebook in a fresh kernel, using fixture data only."""

from pathlib import Path
import tempfile
import unittest

from nbclient import NotebookClient
import nbformat

from bondview.data.fred import save_observations
from test_treasury_curve import example_frame

NOTEBOOK = Path(__file__).resolve().parents[1] / "notebooks/analysis1_curve.ipynb"


class NotebookTests(unittest.TestCase):
    def test_both_modes_and_manual_date_rerun_without_network(self):
        for mode in ("file", "download"):
            with self.subTest(mode=mode), tempfile.TemporaryDirectory() as temp:
                path = Path(temp) / "fixture.json"
                save_observations(example_frame(), path)
                notebook = nbformat.read(NOTEBOOK, as_version=4)
                # Inject only external inputs and the transport fixture; execute all
                # delivered cells unchanged, in their intended order, in a new kernel.
                notebook.cells[1].source += f'\nDATA_MODE = {mode!r}\nDATA_PATH = Path({str(path)!r})'
                setup = '''
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
                notebook.cells.append(nbformat.v4.new_code_cell('''
assert result.change_bp.tolist() == [84, 116, 103, 32, -13]
assert len(history_figure.data) == 3
assert start_picker.value.isoformat() == "2024-09-16"
assert len(transport_calls) == (1 if DATA_MODE == "download" else 0)
fred_transport._read_url = reject_network
start_picker.value = date(2024, 9, 15)  # Sunday, never replaced with Monday
'''))
                analysis_source = next(
                    cell.source for cell in notebook.cells
                    if cell.cell_type == "code" and cell.source.startswith("result = analyze_curve(")
                )
                notebook.cells.append(nbformat.v4.new_code_cell(analysis_source))
                notebook.cells.append(nbformat.v4.new_code_cell('''
assert result.change_bp.isna().all()
assert result.end.notna().all()
assert result.attrs["start"] == "2024-09-15"
'''))
                NotebookClient(notebook, timeout=90, kernel_name="python3").execute(cwd=temp)
                self.assertFalse(any(output.output_type == "error" for cell in notebook.cells
                                     if cell.cell_type == "code" for output in cell.outputs))


if __name__ == "__main__":
    unittest.main()
