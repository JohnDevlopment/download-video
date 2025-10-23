from __future__ import annotations

from typing import Protocol, runtime_checkable

from result import Result

from ..site_processors._utils import InvalidURLError
from .formats import (
    Format,
    FormatSelectionStrategy,
    FormatSelector,
)

__all__ = [
    "SiteInfo",
    "SiteProcessor",
]

class SiteInfo(Protocol):
    def get_url(self) -> str:
        ...

@runtime_checkable
class SiteProcessor(Protocol):
    _STRATEGIES: dict[int, FormatSelectionStrategy]

    def normalize_url(self, url: str, /) -> Result[str, InvalidURLError]:
        ...

    def extract_info(self, url: str, /) -> SiteInfo:
        ...

    def select_format(self, info: SiteInfo, selector: FormatSelector) -> Format:
        ...

    def download(self, url: str, fmt: Format):
        ...

    def name(self) -> str:
        ...

if __name__ == '__main__':
    from . import site_youtube
    temp: SiteProcessor = site_youtube
