"""Format structured Treasury results using configurable terminology."""

import pandas as pd

from bondview.data.fred import SERIES
from bondview.labels import load_labels


def _label(labels, group, identifier):
    if identifier == "unavailable":
        return labels["na"]
    if identifier == "not_applicable":
        return labels["not_applicable"]
    return labels[group][identifier]


def _movement(row, labels):
    if row.movement == "unavailable":
        return labels["na"]
    if row.name in SERIES:
        return labels["direction"][row.movement]
    moving_direction = row.short_direction if row.movement == "short_only" else row.long_direction
    return labels["movement"][row.movement].format(
        slope=_label(labels, "slope", row.slope).lower(),
        direction=_label(labels, "direction", moving_direction).lower(),
    )


def _display_table(result, labels):
    rows = []
    for measure, row in result.iterrows():
        def level(value):
            if pd.isna(value):
                return labels["na"]
            return labels["units"]["percent" if row.level_unit == "%" else "bp"].format(value=value)
        config = labels["not_applicable"] if measure in SERIES else labels["configuration_transition"].format(
            start=_label(labels, "configuration", row.configuration_start),
            end=_label(labels, "configuration", row.configuration_end),
        )
        rows.append({labels["table"]["measure"]: labels["measures"][measure],
                     result.attrs["start"]: level(row.start),
                     labels["table"]["end"].format(date=result.attrs["end"]): level(row.end),
                     labels["table"]["change"]: labels["na"] if pd.isna(row.change_bp) else labels["units"]["bp"].format(value=row.change_bp),
                     labels["table"]["configuration"]: config,
                     labels["table"]["movement"]: _movement(row, labels)})
    return pd.DataFrame(rows).set_index(labels["table"]["measure"])


def display_table(result, *, labels_path=None):
    """Format units and N/A without modifying the structured result."""
    return _display_table(result, load_labels(labels_path))


def _interpret_curve(result, labels):
    text = labels["interpretation"]
    changes = result.loc[list(SERIES), "change_bp"].dropna()
    if changes.empty:
        return text["no_data"]
    statements = []
    for predicate, extreme, direction in ((changes > 0, max, "upward"), (changes < 0, min, "downward")):
        subset = changes[predicate]
        if not subset.empty:
            value = extreme(subset)
            names = ", ".join(labels["tenors"][s] for s in subset.index[subset == value])
            statements.append(text[direction].format(names=names, change=labels["units"]["bp"].format(value=value)))
    if not statements:
        statements.append(text["unchanged"])
    if len(changes) < 3:
        statements.append(text["partial"])
    statements.extend(text["segment"].format(measure=labels["measures"][s], movement=_movement(row, labels))
                      for s, row in result.iloc[3:].iterrows())
    statements.append(text["qualification"])
    return " ".join(statements)


def interpret_curve(result, *, labels_path=None):
    return _interpret_curve(result, load_labels(labels_path))


def show_curve_results(result, *, labels_path=None):
    from IPython.display import Markdown, display
    labels = load_labels(labels_path)
    display(_display_table(result, labels))
    display(Markdown(_interpret_curve(result, labels)))
