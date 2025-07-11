from __future__ import annotations

import importlib
import logging
from pathlib import Path

from result import Err, Ok, Result, is_err

from .sites import SiteInfo, SiteProcessor

__all__ = [
    "SiteInfo",
    "SiteProcessor",
    "match_url",
    "register_site_processors",
]

_site_processors: list[SiteProcessor] = []
_logger = logging.getLogger(__name__)

def match_url(url: str) -> Result[tuple[SiteProcessor, str], str]:
    if not _site_processors:
        return Err("Site processors are not registered")

    _logger.debug("Attempting to find a site processor for '%s'", url)

    for sp in _site_processors:
        match sp.normalize_url(url):
            case Ok(u):
                return Ok((sp, u))

            case Err(e):
                return Err(str(e))

    return Err("Could not find matching site processor")

def register_site_processors() -> None:
    global _site_processors
    _logger.debug("Registering site processors")

    for _module in Path(__file__).parent.iterdir():
        module = f".{_module.stem}"
        if module.startswith(".site_"):
            module = importlib.import_module(module, "download_video.site_processors")
            _logger.debug("Found site processor %s", module.__name__)
            assert isinstance(module, SiteProcessor)
            _site_processors.append(module)
