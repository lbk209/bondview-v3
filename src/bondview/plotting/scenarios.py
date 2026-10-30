"""One Plotly scatter of stored complete historical vectors."""

import plotly.express as px

from bondview.labels import load_labels


def plot_scenarios(
    result, *, labels_path=None, width=1200, height=600
):
    labels = load_labels(labels_path)
    text = labels["analyses"]["conditional_scenarios"]
    condition = result.metadata["condition"]["tenor"]
    x = "DGS2" if condition == "DGS10" else "DGS10"
    frame = result.scenarios.copy()

    for column in ("start_date", "target_end_date", "end_date"):
        frame[column] = frame[column].dt.strftime("%Y-%m-%d")

    names = {
        f"{s}_change_bp": text["change"].format(tenor=tenor)
        for s, tenor in labels["common"]["tenors"].items()
    }
    names.update(text["fields"])

    return px.scatter(
        frame,
        x=f"{x}_change_bp",
        y="DGS30_change_bp",
        color=f"{condition}_change_bp",
        hover_name="scenario_id",
        hover_data={
            "start_date": True,
            "end_date": True,
            "target_end_date": True,
            "elapsed_days": True,
        },
        labels=names,
        title=text["plot_title"],
        width=width,
        height=height,
    )
