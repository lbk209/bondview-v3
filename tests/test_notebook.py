"""Execute the current Treasury notebook offline with per-ID snapshots."""

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
    """Omit optional acquisition; retain setup and all analysis cells."""
    notebook = nbformat.read(NOTEBOOK, as_version=4)
    first = next(i for i, c in enumerate(notebook.cells) if c.source.startswith("### Donwload"))
    last = next(i for i, c in enumerate(notebook.cells) if c.source.startswith("## A."))
    del notebook.cells[first:last]
    config = next(c for c in notebook.cells if c.cell_type == "code" and "SNAPSHOT_DIR =" in c.source)
    config.source = config.source.replace('SNAPSHOT_DIR = PROJECT_ROOT / "data/fred"', f'SNAPSHOT_DIR = Path({str(directory)!r})')
    return notebook


def network_guard():
    return nbformat.v4.new_code_cell('''
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
''')


class NotebookTests(unittest.TestCase):
    def test_explicit_acquisition_and_current_sections(self):
        notebook = nbformat.read(NOTEBOOK, as_version=4)
        sources = [c.source for c in notebook.cells if c.cell_type == "code"]
        code = "\n".join(sources)
        for forbidden in ("DATA_MODE", "load_or_download", "FigureWidget", "anywidget", ".observe(", "on_click"):
            self.assertNotIn(forbidden, code)
        for source in sources:
            ast.parse(source)
        self.assertIn('fred.download(series_ids=FRED_SERIES, start=start, end=end)', code)
        self.assertIn('fred.save()', code)
        self.assertIn('DateRangePicker(observations)', code)
        self.assertIn('DateRangePicker(kw_observations)', code)
        self.assertIn('yield_change_tolerance_bp=5', code)
        self.assertIn('slope_tolerance_bp=5', code)
        self.assertIn('start = None\nend = None', code)
        for series in ("DGS2", "DGS10", "DGS30", "THREEFY2", "THREEFYTP2", "THREEFY10", "THREEFYTP10"):
            self.assertIn(f'"{series}"', code)
        b = next(i for i,c in enumerate(notebook.cells) if c.source.startswith('## B.'))
        c = next(i for i,c in enumerate(notebook.cells) if c.source.startswith('## C.'))
        b_code = '\n'.join(cell.source for cell in notebook.cells[b:c] if cell.cell_type == 'code')
        self.assertIn('kw_observations = fred.load(', b_code)
        self.assertIn('show_kw_decomposition(kw_observations, *date_range.get_dates()', b_code)
        self.assertEqual(code.count('DateRangePicker('), 2)

    def test_offline_execution_and_independent_widget_reruns(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp) / 'fred'
            for fixture in (example_frame(), kw_frame()):
                for series in fixture.columns:
                    info = fixture.attrs['metadata'][series]
                    day = info['retrieved_at_utc'][:10].replace('-', '')
                    save_observations(fixture[[series]], directory / f'{series}_{day}.csv', metadata={series: info})
            before = {p.name:p.read_bytes() for p in directory.iterdir()}
            notebook = offline_notebook(directory)
            b = next(i for i,c in enumerate(notebook.cells) if c.source.startswith('## B.'))
            a_cells = notebook.cells[:b]
            b_cells = notebook.cells[b:]
            plot = next(c.source for c in a_cells if c.source.startswith('history_figure ='))
            analysis = next(c.source for c in a_cells if c.source.startswith('result ='))
            notebook.cells = [network_guard(), *a_cells]
            def add(source):
                notebook.cells.append(nbformat.v4.new_code_cell(source))
            add('''
import pandas as pd
assert result.change_bp.tolist() == [84, 116, 103, 32, -13]
assert result.iloc[3].movement == "bear"
assert result.iloc[4].slope == "flattening"
date_range.start_picker.value = date(2024, 10, 1)
date_range.end_picker.value = date(2025, 1, 1)
''')
            add(plot)
            add('''
assert list(history_figure.layout.xaxis.range) == ["2024-10-01", "2025-01-01"]
assert result.attrs['start'] == '2024-09-16'
date_range.start_picker.value = date(2024, 9, 15)
date_range.end_picker.value = date(2025, 1, 13)
observations.loc[pd.Timestamp('2024-09-16'), 'DGS30'] = float('nan')
''')
            add(analysis)
            add('''
assert pd.isna(result.loc['DGS30', 'change_bp'])
assert result.loc['DGS10_DGS2', 'change_bp'] == 32
assert list(history_figure.layout.xaxis.range) == ["2024-10-01", "2025-01-01"]
''')
            notebook.cells.extend(b_cells)
            add('''
assert pd.isna(result.loc['DGS30', 'change_bp'])
assert 'anywidget' not in sys.modules
''')
            NotebookClient(notebook, timeout=90, kernel_name='python3').execute(cwd=temp)
            self.assertEqual(before, {p.name:p.read_bytes() for p in directory.iterdir()})


if __name__ == '__main__':
    unittest.main()
