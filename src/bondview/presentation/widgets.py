"""Reusable notebook widgets, independent of Treasury-specific calculations."""

import ipywidgets as widgets
import pandas as pd
from IPython.display import display

from bondview.labels import load_labels


def date_picker_defaults(observations, *, labels_path=None):
    """Build DatePicker options using the date coverage of any dated pandas data.

    Deliberately do not set min/max widget limits: callers may need to select
    dates with missing observations or dates outside the loaded sample.
    """
    if not isinstance(observations, (pd.DataFrame, pd.Series)):
        raise ValueError("Date selection requires a pandas DataFrame or Series.")
    index = observations.index
    if not isinstance(index, pd.DatetimeIndex) or index.empty or index.hasnans:
        raise ValueError("Date selection requires a nonempty DatetimeIndex without missing dates.")

    labels = load_labels(labels_path)["widgets"]["dates"]
    return (
        {"description": labels["start"], "value": index.min().date()},
        {"description": labels["end"], "value": index.max().date()},
    )


class DateRangePicker:
    """Two date controls whose current selections can be read on demand."""

    def __init__(self, observations, *, labels_path=None):
        start_options, end_options = date_picker_defaults(
            observations, labels_path=labels_path
        )
        self.start_picker = widgets.DatePicker(**start_options)
        self.end_picker = widgets.DatePicker(**end_options)
        self.widget = widgets.HBox([self.start_picker, self.end_picker])

    def get_dates(self):
        """Return the current (start, end) dates, including any later edits."""
        start, end = self.start_picker.value, self.end_picker.value
        if start is None or end is None:
            raise ValueError("Select both start and end dates.")
        if start > end:
            raise ValueError("Start date must be on or before end date.")
        return start, end
        
    def _ipython_display_(self):
        display(self.widget)
