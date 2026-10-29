"""Ordinary Plotly historical lines; date selections are explicit call inputs."""

import plotly.graph_objects as go

from bondview.data.fred import SERIES, exact_date, validate_treasury_observations
from bondview.labels import load_labels


def plot_kw_decomposition(result, maturity, *, labels_path=None):
    """Plot an analyzed KW path on two y domains sharing one native x-axis."""
    if result.empty:
        raise ValueError("KW plotting requires eligible observations.")
    plot = load_labels(labels_path)["analyses"]["kw_decomposition"]["plot"]
    figure = go.Figure()
    for column, color in (
        ("fitted_yield", "#636EFA"),
        ("expected_rate", "#EF553B"),
        ("term_premium", "#00A080"),
    ):
        figure.add_trace(go.Scatter(
            x=result.index, y=result[column], xaxis="x", yaxis="y",
            name=plot["traces"][column], mode="lines", line={"color": color},
            connectgaps=False, hovertemplate=plot["hover"]["level"],
        ))
    for column, color, hover in (
        ("expected_change_bp", "#EF553B", "expected_change"),
        ("premium_change_bp", "#00A080", "premium_change"),
    ):
        figure.add_trace(go.Scatter(
            x=result.index, y=result[column], xaxis="x", yaxis="y2",
            name=plot["traces"][column], mode="lines", line={"color": color},
            connectgaps=False, hovertemplate=plot["hover"][hover],
            customdata=result[["fitted_change_bp"]].to_numpy() if hover == "expected_change" else None,
        ))
    figure.update_layout(
        title=plot["titles"][maturity], template="plotly_white", height=720,
        hovermode="x", hoversubplots="axis",
        xaxis={
            "type": "date", "domain": [0, 1], "anchor": "y2",
            "title": plot["xaxis"], "side": "bottom", "showticklabels": True,
            "range": [str(result.index[0].date()), str(result.index[-1].date())],
            "showspikes": True, "spikemode": "across", "spikesnap": "data",
            "spikethickness": 1, "spikedash": "dot",
        },
        yaxis={"domain": [0.349, 1], "anchor": "x", "title": plot["level_axis"]},
        yaxis2={"domain": [0, 0.279], "anchor": "x", "title": plot["change_axis"]},
        legend={"orientation": "h", "y": 1.12},
    )
    return figure


def plot_yield_history(data, start, end, *, labels_path=None, metadata=None):
    data = validate_treasury_observations(data, metadata)
    start, end = exact_date(start), exact_date(end)
    if start > end:
        raise ValueError("Selected start must be on or before end.")

    # Plot only observations inside the selected period so the Y-axis
    # automatically rescales to the yields visible in that period.
    selected = data.loc[(data.index >= start) & (data.index <= end)]

    labels = load_labels(labels_path)
    tenors = labels["common"]["tenors"]
    plot = labels["analyses"]["treasury_curve"]["plot"]
    figure = go.Figure()
    for series_id, dash in zip(SERIES, ("solid", "solid", "solid")):
        figure.add_trace(go.Scatter(
            x=selected.index, y=selected[series_id],
            name=plot["trace"].format(tenor=tenors[series_id], series_id=series_id),
            mode="lines", line={"dash": dash}, connectgaps=False,
            hovertemplate=plot["hover"],
        ))
    figure.update_layout(
        title=plot["title"],
        xaxis_title=plot["xaxis"], yaxis_title=plot["yaxis"],
        hovermode="x unified", template="plotly_white",
        xaxis={"type": "date", "range": [str(start.date()), str(end.date())]},
        yaxis={"autorange": True},
        legend_title_text=plot["legend"], height=520,
    )
    return figure


def show_yield_history(data, start, end, *, labels_path=None, metadata=None):
    figure = plot_yield_history(data, start, end, labels_path=labels_path, metadata=metadata)
    figure.show()
    return figure
