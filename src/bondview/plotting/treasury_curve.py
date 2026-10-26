"""Historical yield lines used to inspect and choose endpoint dates."""

import plotly.graph_objects as go

from bondview.data.fred import SERIES, exact_date, validate_observations


def plot_yield_history(data, display_start="2024-09-01", display_end="2025-01-31"):
    data = validate_observations(data)
    if not set(SERIES).issubset(data.columns):
        raise ValueError("Plot requires DGS2, DGS10 and DGS30 columns.")
    start, end = exact_date(display_start), exact_date(display_end)
    if start >= end:
        raise ValueError("Display start must precede display end.")
    figure = go.Figure()
    for series_id, tenor, dash in zip(SERIES, ("2Y", "10Y", "30Y"), ("solid", "dash", "dot")):
        figure.add_trace(go.Scatter(
            x=data.index, y=data[series_id], name=f"{tenor} ({series_id})",
            mode="lines", line={"dash": dash}, connectgaps=False,
            hovertemplate="%{x|%Y-%m-%d}<br>%{y:.2f}%<extra>%{fullData.name}</extra>",
        ))
    figure.update_layout(
        title="U.S. Treasury constant-maturity yield history — FRED/H.15",
        xaxis_title="Observation date", yaxis_title="Yield (%)",
        hovermode="x unified", template="plotly_white",
        xaxis={"type": "date", "range": [str(start.date()), str(end.date())],
               "rangeslider": {"visible": True}},
        legend_title_text="Treasury tenor", height=520,
    )
    return figure
