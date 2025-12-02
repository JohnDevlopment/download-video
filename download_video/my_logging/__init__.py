from __future__ import annotations

import logging
import logging.config
from enum import StrEnum
from io import StringIO
from pathlib import Path
from string import Template
from typing import TYPE_CHECKING

import yaml
from platformdirs import user_log_path

from ..utils import only_once

if TYPE_CHECKING:
    from typing import Any


class LogLevel(StrEnum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


@only_once
def setup_logging(appname: str, level: LogLevel):
    logdir = user_log_path(appname)
    logdir.mkdir(parents=True, exist_ok=True)

    # Load template from logging config file
    fp = Path(__file__).parent / "logging.yaml"
    tmpl = Template(fp.read_text())
    mapping = {
        "LOG_DIR": str(logdir),
        "APPNAME": appname,
        "LEVEL": str(level),
    }
    yaml_string = tmpl.substitute(mapping)

    # Load YAML config
    with StringIO(yaml_string) as fd:
        LOGGING_CONFIG: dict[str, Any] = yaml.safe_load(fd)
        logging.config.dictConfig(LOGGING_CONFIG)
