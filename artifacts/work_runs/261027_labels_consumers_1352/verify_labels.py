"""Offline, run-specific verification; run from the repository via Poetry."""

import ast
from contextlib import redirect_stdout
from copy import deepcopy
from io import StringIO
import json
from pathlib import Path
import subprocess
import tempfile
from unittest.mock import patch

import numpy as np
import pandas as pd
import yaml

from bondview.analysis.treasury_curve import analyze_curve
from bondview.data.fred import SERIES, FredDataManager, save_observations
from bondview.labels import load_labels
from bondview.plotting.treasury_curve import plot_yield_history, show_yield_history
from bondview.presentation.treasury_curve import display_table, interpret_curve, show_curve_results
from bondview.presentation.widgets import DateRangePicker, date_picker_defaults


ROOT = Path.cwd()
RUN = Path(__file__).resolve().parent
BASE = "693bf09c32607705d1bc926258d0dfad00ef67b1"
MODIFIED = [
    "src/bondview/data/fred.py",
    "src/bondview/plotting/treasury_curve.py",
    "src/bondview/presentation/treasury_curve.py",
    "src/bondview/presentation/widgets.py",
]
checks = []
labels = load_labels()
common = labels["common"]
curve = labels["analyses"]["treasury_curve"]


def frame(values=None):
    data = pd.DataFrame(
        values if values is not None else [[3.56, 3.63, 3.94], [4.40, 4.79, 4.97]],
        columns=SERIES, index=pd.to_datetime(["2024-09-16", "2025-01-13"]),
    )
    data.index.name = "date"
    data.attrs["metadata"] = {
        "source": "Synthetic verification fixture; not market retrieval",
        "retrieved_at_utc": "2026-10-27T00:00:00+00:00",
        "series": {s: {"units": "Percent", "frequency": "D"} for s in SERIES},
    }
    return data


data = frame()
result = analyze_curve(data, *data.index)
before = result.copy(deep=True)
table = display_table(result)
assert result.change_bp.tolist() == [84, 116, 103, 32, -13]
assert table.index.tolist() == ["2Y yield", "10Y yield", "30Y yield", "10Y−2Y spread", "30Y−10Y spread"]
assert table.columns.tolist() == ["2024-09-16", "2025-01-13", "Change", "Curve configuration", "Movement / regime"]
assert table.iloc[:, 0].tolist() == ["3.56%", "3.63%", "3.94%", "+7 bp", "+31 bp"]
assert table.iloc[:, 1].tolist() == ["4.40%", "4.79%", "4.97%", "+39 bp", "+18 bp"]
assert table["Change"].tolist() == ["+84 bp", "+116 bp", "+103 bp", "+32 bp", "-13 bp"]
assert table.iloc[:3, -2].tolist() == ["—"] * 3
assert table.iloc[3:, -1].tolist() == ["Bear steepening", "Bear flattening"]
assert table.iloc[3, -2] == "Upward-sloping → Upward-sloping"
interpretation = interpret_curve(result)
assert interpretation == (
    "Greatest upward yield movement among available tenors: 10Y (+116 bp). "
    "10Y−2Y spread: Bear steepening. 30Y−10Y spread: Bear flattening. "
    "These are net endpoint movements, not the full path or a forecast. ETF rate-price effects depend on duration and other product characteristics."
)
pd.testing.assert_frame_equal(result, before)
checks.append("Hand-checked table, signed zero-decimal bp, two-decimal percent, full interpretation, no result mutation")

cases = [
    (10, 20, "Bear steepening"), (20, 10, "Bear flattening"),
    (-20, -10, "Bull steepening"), (-10, -20, "Bull flattening"),
    (-10, 10, "Opposing-direction twist steepening"), (10, -10, "Opposing-direction twist flattening"),
    (10, 10, "Yields rose; little slope change"), (-10, -10, "Yields fell; little slope change"),
    (0, 0, "Little yield movement"),
    (0, 10, "Long yield rose, other little change; steepening"),
    (0, -10, "Long yield fell, other little change; flattening"),
    (10, 0, "Short yield rose, other little change; flattening"),
    (-10, 0, "Short yield fell, other little change; steepening"),
]
for short, long, expected in cases:
    sample = frame([[4., 4., 4.], [4 + short / 100, 4 + long / 100, 4.]])
    comparison = analyze_curve(sample, *sample.index)
    assert display_table(comparison).iloc[3, -1] == expected
    assert expected in interpret_curve(comparison)
down = frame([[5., 4., 4.], [4.5, 3., 3.5]])
down_result = analyze_curve(down, *down.index)
assert display_table(down_result).iloc[3, -2] == "Inverted → Inverted"
assert display_table(down_result).iloc[4, -2] == "Flat → Upward-sloping"
assert "10Y (-100 bp)" in interpret_curve(down_result)
unchanged = analyze_curve(data, data.index[0], data.index[0])
assert display_table(unchanged)["Change"].tolist() == ["+0 bp"] * 5
assert curve["interpretation"]["unchanged"] in interpret_curve(unchanged)
tie = frame([[4., 4., 4.], [4.1, 4.1, 3.9]])
assert "2Y, 10Y (+10 bp)" in interpret_curve(analyze_curve(tie, *tie.index))
tolerated = analyze_curve(tie, *tie.index, yield_change_tolerance_bp=10)
assert curve["interpretation"]["unchanged"] in interpret_curve(tolerated)
checks.append("13 movement cases; three configurations; upward/downward/tied/unchanged interpretations; tolerance retained")

for endpoint in range(2):
    for tenor in range(3):
        partial = frame()
        partial.iloc[endpoint, tenor] = np.nan
        partial_result = analyze_curve(partial, *partial.index)
        partial_table = display_table(partial_result)
        assert partial_table.iloc[tenor, endpoint] == "N/A"
        assert partial_table.iloc[tenor, 2] == "N/A"
        assert partial_table.iloc[tenor, -1] == "N/A"
        assert curve["interpretation"]["partial"] in interpret_curve(partial_result)
no_pairs = frame([[4., np.nan, np.nan], [np.nan, 4., 5.]])
no_pairs_result = analyze_curve(no_pairs, *no_pairs.index)
assert interpret_curve(no_pairs_result) == curve["interpretation"]["no_data"]
assert display_table(no_pairs_result)["Change"].tolist() == ["N/A"] * 5
checks.append("Six independent missing endpoints and no paired tenor observations")

history = data.reindex(pd.to_datetime(["2024-09-16", "2024-12-25", "2025-01-13"]))
figure = plot_yield_history(history, *data.index)
assert [trace.name for trace in figure.data] == ["2Y (DGS2)", "10Y (DGS10)", "30Y (DGS30)"]
for i, trace in enumerate(figure.data):
    assert list(trace.x) == list(history.index)
    np.testing.assert_equal(trace.y, history.iloc[:, i].to_numpy())
    assert trace.mode == "lines" and trace.connectgaps is False
    assert trace.line.dash == ["solid", "dash", "dot"][i]
    assert trace.hovertemplate == curve["plot"]["hover"]
assert figure.layout.title.text == curve["plot"]["title"]
assert figure.layout.xaxis.title.text == curve["plot"]["xaxis"]
assert figure.layout.yaxis.title.text == curve["plot"]["yaxis"]
assert figure.layout.legend.title.text == curve["plot"]["legend"]
assert list(figure.layout.xaxis.range) == ["2024-09-16", "2025-01-13"]
selected = plot_yield_history(history, "2024-10-01", "2025-01-01")
assert all(len(trace.x) == 1 and pd.isna(trace.y[0]) for trace in selected.data)
with patch("plotly.graph_objects.Figure.show") as show:
    shown = show_yield_history(data, *data.index)
    assert len(shown.data) == 3
    show.assert_called_once()
with patch("IPython.display.display") as display:
    show_curve_results(result)
    assert display.call_count == 2
    pd.testing.assert_frame_equal(display.call_args_list[0].args[0], table)
    assert display.call_args_list[1].args[0].data == interpretation
checks.append("Plot labels, hover, three traces, dates, values, gaps, selected-period slicing and both display wrappers")

options = date_picker_defaults(data)
assert options == ({"description": "Start", "value": data.index[0].date()}, {"description": "End", "value": data.index[1].date()})
picker = DateRangePicker(data)
assert picker.start_picker.description == "Start" and picker.end_picker.description == "End"
assert picker.get_dates() == tuple(data.index.date)
for widget in (picker.start_picker, picker.end_picker, picker.widget):
    widget.close()
checks.append("Date defaults and actual DateRangePicker descriptions and selected dates")

with tempfile.TemporaryDirectory() as temp:
    path = Path(temp) / "snapshot.csv"
    save_observations(history, path)
    manager = FredDataManager(path)
    with patch("bondview.data.fred._read_url", side_effect=AssertionError("Offline verification")):
        manager.load()
    snapshot_before = path.read_bytes()
    output = StringIO()
    with redirect_stdout(output):
        manager.report()
    expected = (
        "Synthetic verification fixture; not market retrieval | Retrieved: 2026-10-27T00:00:00+00:00\n"
        f"Loaded coverage: 2024-09-16 to 2025-01-13 | 3 rows | {path}\n"
        "DGS2: Percent, D; missing: 1\nDGS10: Percent, D; missing: 1\nDGS30: Percent, D; missing: 1\n"
        "Retrieval-time snapshot; historical data availability at the observation date is not reconstructed.\n"
    )
    assert output.getvalue() == expected
    assert path.read_bytes() == snapshot_before
    report_example = output.getvalue().replace(str(path), "<temporary snapshot.csv>")
    checks.append("Exact multiline FRED report, provenance, coverage, rows, per-series metadata/missing counts; snapshot unchanged")

    # A separate temporary YAML exercises nested customization and rereading.
    custom = deepcopy(labels)
    custom["common"].update(na="MISSING", not_applicable="NONE")
    custom["common"]["units"] = {"percent_2dp": "P{value:.3f}", "bp_signed_0dp": "B{value:+.1f}"}
    custom["common"]["tenors"]["DGS10"] = "TEN"
    custom["widgets"]["dates"] = {"start": "FROM", "end": "TO"}
    c = custom["analyses"]["treasury_curve"]
    c["measures"]["DGS10_DGS2"] = "SEGMENT"
    c["movement"]["bear"] = "RISING {slope}"
    c["slope"]["steepening"] = "WIDER"
    c["direction"]["rose"] = "UP"
    c["configuration"]["upward"] = "POSITIVE"
    c["configuration_transition"] = "{start} / {end}"
    c["table"] = {"measure": "MEASURE", "change": "DELTA", "configuration": "SHAPE", "movement": "REGIME"}
    c["interpretation"]["upward"] = "UPWARD {names} {change}"
    c["plot"] = {"title": "HISTORY", "xaxis": "DATE", "yaxis": "RATE", "legend": "TENOR", "trace": "{series_id}/{tenor}", "hover": "%{y} CUSTOM"}
    custom["data"]["fred"] = {"summary": "SUMMARY {source} {rows}", "series": "SERIES {series_id} {units} {frequency} {missing}", "snapshot": "SNAPSHOT"}
    custom_path = Path(temp) / "labels.yaml"
    custom_path.write_text(yaml.safe_dump(custom), encoding="utf-8")
    custom_table = display_table(result, labels_path=custom_path)
    assert custom_table.index.name == "MEASURE" and custom_table.index[3] == "SEGMENT"
    assert custom_table.iloc[0, 0] == "P3.560" and custom_table.iloc[3, 0] == "B+7.0"
    assert custom_table.iloc[0, 2] == "B+84.0" and custom_table.iloc[0, -2] == "NONE"
    assert custom_table.iloc[0, -1] == "UP" and custom_table.iloc[3, -1] == "RISING wider"
    assert custom_table.iloc[3, -2] == "POSITIVE / POSITIVE"
    assert display_table(no_pairs_result, labels_path=custom_path).iloc[0, 2] == "MISSING"
    assert "UPWARD TEN B+116.0" in interpret_curve(result, labels_path=custom_path)
    custom_fig = plot_yield_history(data, *data.index, labels_path=custom_path)
    assert custom_fig.layout.title.text == "HISTORY" and custom_fig.data[1].name == "DGS10/TEN"
    assert custom_fig.layout.xaxis.title.text == "DATE" and custom_fig.layout.yaxis.title.text == "RATE"
    assert custom_fig.layout.legend.title.text == "TENOR" and custom_fig.data[0].hovertemplate == "%{y} CUSTOM"
    assert [option["description"] for option in date_picker_defaults(data, labels_path=custom_path)] == ["FROM", "TO"]
    custom_picker = DateRangePicker(data, labels_path=custom_path)
    assert custom_picker.start_picker.description == "FROM" and custom_picker.end_picker.description == "TO"
    for widget in (custom_picker.start_picker, custom_picker.end_picker, custom_picker.widget):
        widget.close()
    custom_output = StringIO()
    with redirect_stdout(custom_output):
        manager.report(labels_path=custom_path)
    assert custom_output.getvalue() == (
        "SUMMARY Synthetic verification fixture; not market retrieval 3\n"
        "SERIES DGS2 Percent D 1\nSERIES DGS10 Percent D 1\nSERIES DGS30 Percent D 1\nSNAPSHOT\n"
    )
    c["measures"]["DGS2"] = "SECOND EDIT"
    custom_path.write_text(yaml.safe_dump(custom), encoding="utf-8")
    assert display_table(result, labels_path=custom_path).index[0] == "SECOND EDIT"
    pd.testing.assert_frame_equal(analyze_curve(data, *data.index), before)
checks.append("Temporary nested YAML customization across all four consumers and shared formats; rereading; calculations unchanged")


def signatures(source):
    return {node.name: ast.dump(node.args) for node in ast.walk(ast.parse(source)) if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))}


for filename in MODIFIED:
    original = subprocess.check_output(["git", "show", f"{BASE}:{filename}"], text=True)
    assert signatures(original) == signatures(Path(filename).read_text())
# Root lookup names are constrained to the new namespaces, without old units.
obsolete = {"na", "not_applicable", "units", "tenors", "dates", "measures", "configuration", "configuration_transition", "direction", "slope", "movement", "table", "interpretation", "plot"}
tracked_python = subprocess.check_output(["git", "ls-files", "src/**/*.py"], text=True).splitlines()
for relative in tracked_python:
    filename = ROOT / relative
    for node in ast.walk(ast.parse(filename.read_text())):
        if isinstance(node, ast.Subscript) and isinstance(node.value, ast.Name) and node.value.id == "labels" and isinstance(node.slice, ast.Constant):
            # widgets/FRED bind their local `labels` to their nested namespace.
            if str(filename.relative_to(ROOT)) not in ("src/bondview/presentation/widgets.py", "src/bondview/data/fred.py"):
                assert node.slice.value not in obsolete, (filename, node.lineno)
        if isinstance(node, ast.Subscript) and isinstance(node.value, ast.Subscript) and isinstance(node.value.slice, ast.Constant) and node.value.slice.value == "units" and isinstance(node.slice, ast.Constant):
            assert node.slice.value not in {"percent", "bp"}
checks.append("All function signatures unchanged; AST scan rejects obsolete root lookups and old unit keys")

protected = subprocess.check_output(["git", "diff", "--name-only", BASE, "--", "src/bondview/config/labels.yaml", "AGENTS.md", "docs", "workflow", "tests", "notebooks", "src/bondview/analysis", "src/bondview/utils.py"], text=True)
assert not protected, protected
checks.append("Protected YAML, instructions, docs, workflow, tests, notebooks, analysis and utilities unchanged from the authorized source")

evidence = {"status": "PASS", "source_revision": BASE, "checks": checks, "movement_cases": len(cases), "missing_endpoint_cases": 6, "example_table": table.reset_index().to_dict(orient="records"), "example_interpretation": interpretation, "example_fred_report": report_example}
(RUN / "evidence" / "focused_verification.json").write_text(json.dumps(evidence, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(json.dumps({"status": "PASS", "checks": checks}, indent=2))
