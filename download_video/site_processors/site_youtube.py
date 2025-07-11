from __future__ import annotations

import re
from typing import TYPE_CHECKING

from icecream import ic

from ..site_processors.formats import FormatSelector
from ._utils import InvalidURLError
from .formats import Format, FormatSelectionFlags

if TYPE_CHECKING:
    from . import SiteInfo
    from .formats import FormatSelectionStrategy

NETLOC: str = "www.youtube.com"
SPECS: list[str] = [
    "https​://www.youtube.com/watch?v=XXXXXXXXXXX",
    "youtube.be/XXXXXXXXXXX",
    "yt:XXXXXXXXXXX",
]
REGEX = re.compile(r"(?:https://www\.youtube\.com/watch\?v=|youtu.be/|yt:)([a-zA-Z0-9_-]{11})")

### Strategies

def audio_video_strategy(selector: FormatSelector, info: SiteInfo) -> Format:
    ...

def audio_video_no_height_strategy(selector: FormatSelector, info: SiteInfo) -> Format:
    ...

def audio_only_strategy(selector: FormatSelector, info: SiteInfo) -> Format:
    ...

def video_only_strategy(selector: FormatSelector, info: SiteInfo) -> Format:
    ...

def video_only_no_height_strategy(selector: FormatSelector, info: SiteInfo) -> Format:
    ...

_STRATEGIES: dict[int, FormatSelectionStrategy] = {
    (FormatSelectionFlags.AUDIO & FormatSelectionFlags.VIDEO
     & FormatSelectionFlags.HEIGHT): audio_video_strategy,
    (FormatSelectionFlags.AUDIO & FormatSelectionFlags.VIDEO): audio_video_no_height_strategy,
    (FormatSelectionFlags.VIDEO & FormatSelectionFlags.HEIGHT): video_only_strategy,
    FormatSelectionFlags.VIDEO: video_only_no_height_strategy,
}

##############

def normalize_url(url: str, /) -> str:
    if (m := REGEX.fullmatch(url)) is None:
        raise InvalidURLError(url, *SPECS)

    return f"https://{NETLOC}/watch?v={m[1]}"

def extract_info(url: str, /) -> SiteInfo:
    ...

def _get_strategy(selector: FormatSelector) -> FormatSelectionStrategy:
    return _STRATEGIES[FormatSelectionFlags.from_selector(selector)]

def select_format(info: SiteInfo, selector: FormatSelector) -> Format:
    st = _get_strategy(selector)


def download(url: str, fmt: str) -> None:
    pass

if __name__ == '__main__':
    def test():
        ic(normalize_url("yt:xxxxxxxxxxx"), normalize_url("youtu.be/xxxxxxxxxxx"))

    test()
