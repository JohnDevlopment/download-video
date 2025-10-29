from __future__ import annotations

import re
from typing import TYPE_CHECKING, Annotated, Optional

from pydantic import BaseModel, Field
from result import Err, Ok, Result

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

class _Format(BaseModel):
    # Audio
    abr: Optional[float] = None
    acodec: Optional[str] = None
    asr: Optional[float] = None
    audio_ext: Optional[str] = None

    # Video
    width: Optional[int] = None
    height: Optional[int] = None
    video_ext: Optional[str] = None

    # General
    ext: str
    tbr: Optional[float] = None
    format_id: str
    filesize: Optional[int] = None
    filesize_approx: Optional[int] = None
    url: str

class _SiteInfo(BaseModel):
    title: str
    video_id: Annotated[str, Field(alias="id")]
    formats: list[_Format]
    age_limit: int
    url: Annotated[str, Field(alias="webpage_url")]

    def get_url(self) -> str:
        return self.url

### Strategies

def audio_video_strategy(selector: FormatSelector, info: SiteInfo) -> Format:
    raise NotImplementedError("audio_video_strategy")

def audio_video_no_height_strategy(selector: FormatSelector, info: SiteInfo) -> Format:
    raise NotImplementedError("audio_video_no_height_strategy")

def audio_only_strategy(selector: FormatSelector, info: SiteInfo) -> Format:
    raise NotImplementedError("audio_only_strategy")

def video_only_strategy(selector: FormatSelector, info: SiteInfo) -> Format:
    raise NotImplementedError("video_only_strategy")

def video_only_no_height_strategy(selector: FormatSelector, info: SiteInfo) -> Format:
    raise NotImplementedError("video_only_no_height_strategy")

_STRATEGIES: dict[int, FormatSelectionStrategy] = {
    (FormatSelectionFlags.AUDIO | FormatSelectionFlags.VIDEO
     | FormatSelectionFlags.HEIGHT): audio_video_strategy,
    (FormatSelectionFlags.AUDIO | FormatSelectionFlags.VIDEO): audio_video_no_height_strategy,
    (FormatSelectionFlags.VIDEO | FormatSelectionFlags.HEIGHT): video_only_strategy,
    FormatSelectionFlags.VIDEO: video_only_no_height_strategy,
}

##############

def normalize_url(url: str, /) -> Result[str, InvalidURLError]:
    if (m := REGEX.fullmatch(url)) is None:
        return Err(InvalidURLError(url, *SPECS))

    return Ok(f"https://{NETLOC}/watch?v={m[1]}")

def extract_info(url: str, /) -> SiteInfo:
    raise NotImplementedError

def _get_strategy(selector: FormatSelector) -> FormatSelectionStrategy:
    return _STRATEGIES[FormatSelectionFlags.from_selector(selector)]

def select_format(info: SiteInfo, selector: FormatSelector) -> Format:
    st = _get_strategy(selector)
    return st(selector, info)

def download(url: str, fmt: str) -> None:
    raise NotImplementedError

def name():
    return "youtube"

if __name__ == '__main__':
    from icecream import ic
    def test():
        ic(normalize_url("yt:xxxxxxxxxxx"), normalize_url("youtu.be/xxxxxxxxxxx"))

    test()
