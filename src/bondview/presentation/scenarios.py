"""Compact scenario statistics and interpretation using stored joint vectors."""

from bondview.labels import load_labels


def show_scenario_summary(result, *, labels_path=None):
    from IPython.display import Markdown, display

    labels = load_labels(labels_path)
    text = labels["analyses"]["conditional_scenarios"]
    info = result.metadata
    condition = info["condition"]
    description = text["summary"].format(
        tenor=labels["common"]["tenors"][condition["tenor"]],
        lower=condition["lower_bp"], upper=condition["upper_bp"],
        months=info["horizon_months"], sampling_step_observations=info["sampling_step_observations"],
        start=info["reference"]["effective_start"], end=info["reference"]["effective_end"],
        selected=info["counts"]["selected_scenarios"], eligible=info["counts"]["eligible_windows"],
    )
    table = result.summary()
    table.index = [labels["common"]["tenors"][s] for s in table.index]
    table.index.name = text["tenor_axis"]
    table = table.rename(columns=text["statistics"])
    display(Markdown(description))
    display(table.round(2))
    display(Markdown(text["qualification"]))
    return table
