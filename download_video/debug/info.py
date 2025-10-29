from __future__ import annotations

from pathlib import Path
import json

def load_info_dict(site_name: str):
    fp = (Path(__file__).parent / site_name).with_suffix(".json")
    with fp.open() as fd:
        return json.load(fd)
