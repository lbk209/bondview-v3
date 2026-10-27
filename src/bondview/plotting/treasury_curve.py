"""Ordinary Plotly historical lines; date selections are explicit call inputs."""

import plotly.graph_objects as go

from bondview.data.fred import SERIES, exact_date, validate_treasury_observations
from bondview.labels import load_labels


def plot_yield_history(data, start, end, *, labels_path=None, metadata=None):
    data = validate_treasury_observations(data, metadata)
    start, end = exact_date(start), exact_date(end)
    if start > end:
        raise ValueError("Selected start must be on or before end.")

    # Plot only observations inside the selected period so the Y-axis
    # automatically rescales to the yields visible in that period.
    selected = data.loc[(data.index >= start) & (data.index <= end)]

    labels = load_labels(labels_path)
    figure = go.Figure()
    for series_id, dash in zip(SERIES, ("solid", "dash", "dot")):
        figure.add_trace(go.Scatter(
            x=selected.index, y=selected[series_id],
            name=labels["plot"]["trace"].format(tenor=labels["tenors"][series_id], series_id=series_id),
            mode="lines", line={"dash": dash}, connectgaps=False,
            hovertemplate=labels["plot"]["hover"],
        ))
    figure.update_layout(
        title=labels["plot"]["title"],
        xaxis_title=labels["plot"]["xaxis"], yaxis_title=labels["plot"]["yaxis"],
        hovermode="x unified", template="plotly_white",
        xaxis={"type": "date", "range": [str(start.date()), str(end.date())]},
        yaxis={"autorange": True},
        legend_title_text=labels["plot"]["legend"], height=520,
    )
    return figure


def show_yield_history(data, start, end, *, labels_path=None, metadata=None):
    figure = plot_yield_history(data, start, end, labels_path=labels_path, metadata=metadata)
    figure.show()
    return figure
