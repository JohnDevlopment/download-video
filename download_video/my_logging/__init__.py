from __future__ import annotations

import logging
from enum import StrEnum

from ..utils import only_once


class LogLevel(StrEnum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

@only_once
def setup_logging(_appname: str, level: LogLevel):
    logging.basicConfig(level=level)
