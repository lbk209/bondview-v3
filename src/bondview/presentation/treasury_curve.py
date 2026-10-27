"""Format structured Treasury results using configurable terminology."""

import pandas as pd

from bondview.data.fred import SERIES
from bondview.labels import load_labels


def _label(labels, group, identifier):
    if identifier == "unavailable":
        return labels["common"]["na"]
    if identifier == "not_applicable":
        return labels["common"]["not_applicable"]
    return labels["analyses"]["treasury_curve"][group][identifier]


def _movement(row, labels):
    curve = labels["analyses"]["treasury_curve"]
    if row.movement == "unavailable":
        return labels["common"]["na"]
    if row.name in SERIES:
        return curve["direction"][row.movement]
    moving_direction = row.short_direction if row.movement == "short_only" else row.long_direction
    return curve["movement"][row.movement].format(
        slope=_label(labels, "slope", row.slope).lower(),
        direction=_label(labels, "direction", moving_direction).lower(),
    )


def _display_table(result, labels):
    common = labels["common"]
    curve = labels["analyses"]["treasury_curve"]
    rows = []
    for measure, row in result.iterrows():
        def level(value):
            if pd.isna(value):
                return common["na"]
            return common["units"]["percent_2dp" if row.level_unit == "%" else "bp_signed_0dp"].format(value=value)
        config = common["not_applicable"] if measure in SERIES else curve["configuration_transition"].format(
            start=_label(labels, "configuration", row.configuration_start),
            end=_label(labels, "configuration", row.configuration_end),
        )
        rows.append({curve["table"]["measure"]: curve["measures"][measure],
                     result.attrs["start"]: level(row.start),
                     result.attrs["end"]: level(row.end),
                     curve["table"]["change"]: common["na"] if pd.isna(row.change_bp) else common["units"]["bp_signed_0dp"].format(value=row.change_bp),
                     curve["table"]["configuration"]: config,
                     curve["table"]["movement"]: _movement(row, labels)})
    return pd.DataFrame(rows).set_index(curve["table"]["measure"])


def display_table(result, *, labels_path=None):
    """Format units and N/A without modifying the structured result."""
    return _display_table(result, load_labels(labels_path))


def _interpret_curve(result, labels):
    common = labels["common"]
    curve = labels["analyses"]["treasury_curve"]
    text = curve["interpretation"]
    changes = result.loc[list(SERIES), "change_bp"].dropna()
    if changes.empty:
        return text["no_data"]
    tolerance = result.attrs.get("yield_change_tolerance_bp", 0.0)
    statements = []
    for predicate, extreme, direction in (
        (changes > tolerance, max, "upward"),
        (changes < -tolerance, min, "downward"),
    ):
        subset = changes[predicate]
        if not subset.empty:
            value = extreme(subset)
            names = ", ".join(common["tenors"][s] for s in subset.index[subset == value])
            statements.append(text[direction].format(names=names, change=common["units"]["bp_signed_0dp"].format(value=value)))
    if not statements:
        statements.append(text["unchanged"])
    if len(changes) < 3:
        statements.append(text["partial"])
    statements.extend(text["segment"].format(measure=curve["measures"][s], movement=_movement(row, labels))
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
