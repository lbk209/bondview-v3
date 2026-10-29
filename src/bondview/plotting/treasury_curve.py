"""Ordinary Plotly historical lines; date selections are explicit call inputs."""

from datetime import timedelta

import plotly.graph_objects as go
from plotly.subplots import make_subplots

from bondview.analysis.treasury_curve import analyze_kw_decomposition
from bondview.data.fred import SERIES, exact_date, validate_treasury_observations
from bondview.labels import load_labels


_KW_COMPONENTS = (
    ("fitted_yield", "#636EFA"),
    ("expected_rate", "#EF553B"),
    ("term_premium", "#00A080"),
)
_KW_CHANGES = (
    ("expected_change_bp", "#EF553B", "expected_change"),
    ("premium_change_bp", "#00A080", "premium_change"),
)



def _add_kw_traces(figure, result, plot, *, column, show_legend):
    """Add original levels above cumulative changes in a subplot column."""
    for field, color in _KW_COMPONENTS:
        figure.add_trace(go.Scatter(
            x=result.index, y=result[field],
            name=plot["traces"][field],
            mode="lines+markers" if len(result) == 1 else "lines",
            line={"color": color}, connectgaps=False,
            legendgroup=field, showlegend=show_legend,
        ), row=1, col=column)

    for field, color, _ in _KW_CHANGES:
        figure.add_trace(go.Scatter(
            x=result.index, y=result[field],
            name=plot["traces"][field],
            mode="lines+markers" if len(result) == 1 else "lines",
            line={"color": color}, connectgaps=False,
            legendgroup=field, showlegend=show_legend,
        ), row=2, col=column)

    first, last = result.index[0], result.index[-1]
    # Give a lone observation visible horizontal space as well as a marker.
    date_range = ([str((first - timedelta(days=1)).date()),
                   str((first + timedelta(days=1)).date())]
                  if first == last else [str(first.date()), str(last.date())])

    for row in (1, 2):
        figure.update_xaxes(
            type="date", matches=None, range=date_range,
            showticklabels=True, hoverformat="%Y-%m-%d",
            title_text=plot["xaxis"] if row == 2 else None,
            row=row, col=column,
        )

    figure.update_yaxes(title_text=plot["level_axis"], row=1, col=column)
    figure.update_yaxes(title_text=plot["change_axis"], row=2, col=column)



def plot_kw_comparison(results, *, labels_path=None, width=1200, height=600):
    """Compare 2Y/10Y KW components with synchronized vertical hover."""
    maturities = ("2Y", "10Y")
    if any(m not in results or results[m].empty for m in maturities):
        raise ValueError(
            "KW comparison requires eligible observations for 2Y and 10Y."
        )

    plot = load_labels(labels_path)["analyses"]["kw_decomposition"]["plot"]

    figure = make_subplots(
        rows=2, cols=2,
        row_heights=[0.7, 0.3], vertical_spacing=0.13,
        horizontal_spacing=0.02,
        subplot_titles=[plot["titles"][m] for m in maturities],
    )

    for col, maturity in enumerate(maturities, start=1):
        _add_kw_traces(
            figure, results[maturity], plot,
            column=col, show_legend=col == 1,
        )

    # Hide change-series legends and old per-line hover entries.
    figure.update_traces(showlegend=False, row=2)
    figure.update_traces(hovertemplate=None, hoverinfo="skip")

    # One hover entry for levels and one for changes per maturity.
    for col, maturity in enumerate(maturities, start=1):
        path = results[maturity]

        figure.update_traces(
            selector=dict(name=plot["traces"]["fitted_yield"]),
            row=1, col=col,
            customdata=path[
                ["expected_rate", "term_premium"]
            ].to_numpy(),
            hovertemplate=plot["hover"]["levels_summary"],
            hoverinfo="all",
        )

        figure.update_traces(
            selector=dict(name=plot["traces"]["expected_change_bp"]),
            row=2, col=col,
            customdata=path[
                ["fitted_change_bp", "premium_change_bp"]
            ].to_numpy(),
            hovertemplate=plot["hover"]["changes_summary"],
            hoverinfo="all",
        )

    # Preserve the working synchronized x-axis arrangement.
    figure.update_traces(xaxis="x", row=2, col=1)
    figure.update_traces(xaxis="x2", row=2, col=2)

    figure.update_xaxes(
        showspikes=True, spikemode="across",
        spikesnap="cursor", spikedash="dot",
        row=1,
    )
    figure.update_xaxes(visible=False, row=2)

    figure.update_layout(
        template="plotly_white", width=width, height=height,
        hovermode="x unified", hoversubplots="axis",
        xaxis=dict(anchor="y3", showticklabels=True),
        xaxis2=dict(anchor="y4", showticklabels=True),
        yaxis3=dict(anchor="x"),
        yaxis4=dict(anchor="x2"),
    )

    # Share y-axis scales within each row.
    figure.update_yaxes(matches="y", row=1, col=2)
    figure.update_yaxes(matches="y3", row=2, col=2)

    # Display y-axis labels only on the left.
    for row in (1, 2):
        figure.update_yaxes(
            title_text="",
            showticklabels=False,
            row=row, col=2,
        )

    return figure



def show_kw_decomposition(data, start, end, width=1200, height=600):
    """Calculate and display the 2Y/10Y KW decomposition in one figure."""
    results = analyze_kw_decomposition(data, start, end)
    figure = plot_kw_comparison(results, width=width, height=height)
    figure.show()


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
