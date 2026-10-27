"""Read presentation terminology on each call so edits apply on cell reruns."""

from pathlib import Path

import yaml

DEFAULT_LABELS_PATH = Path(__file__).resolve().parent / "config" / "labels.yaml"


def load_labels(path=None):
    with Path(path or DEFAULT_LABELS_PATH).open(encoding="utf-8") as stream:
        labels = yaml.safe_load(stream)
    if not isinstance(labels, dict):
        raise ValueError("Labels must be a YAML mapping.")
    return labels
