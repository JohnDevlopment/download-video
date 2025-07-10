from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum, IntFlag, auto
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from typing import Self
    from .sites import SiteInfo

type Format = str

class FormatType(Enum):
    AUDIO_ONLY = auto()
    VIDEO_ONLY = auto()
    AUDIO_VIDEO = auto()

# TODO: Document in design doc
class FormatSelectionFlags(IntFlag):
    HEIGHT = auto()
    AUDIO = auto()
    VIDEO = auto()

    @classmethod
    def from_selector(cls, selector: FormatSelector) -> int:
        flags = 0
        if selector.height is not None:
            flags = flags & cls.HEIGHT

        ft = selector.format_type
        if ft == FormatType.AUDIO_VIDEO:
            flags = flags & (cls.AUDIO & cls.VIDEO)
        elif ft == FormatType.AUDIO_ONLY:
            flags = flags & cls.AUDIO
        elif ft == FormatType.VIDEO_ONLY:
            flags = flags & cls.VIDEO
        else:
            raise RuntimeError("Ran into unreachable code")

        return flags

@dataclass(slots=True)
class FormatSelector:
    height: Optional[int]
    format_type: FormatType

type FormatSelectionStrategy = Callable[[FormatSelector, SiteInfo], Format]
