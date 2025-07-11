from __future__ import annotations

import logging
import os

from ..utils import only_once

@only_once
def setup_logging(_appname: str):
    level = os.getenv('DV_LEVEL', "INFO")
    logging.basicConfig(level=level)
