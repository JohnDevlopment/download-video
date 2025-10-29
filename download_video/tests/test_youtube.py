from __future__ import annotations

from typing import Any

import pytest
from dotenv import load_dotenv

from download_video.site_processors import SiteInfo, SiteProcessor, site_youtube
from download_video.site_processors.formats import Format, FormatSelector, FormatType

from .utils import json_from_base64, load_env

type _Info = site_youtube._SiteInfo

load_dotenv()

@pytest.fixture
def info() -> site_youtube._SiteInfo:
    s = load_env('YOUTUBEDATA')
    info = json_from_base64(s)
    return site_youtube._SiteInfo(**info)

@pytest.mark.parametrize(
    "selector",
    [FormatSelector(None, FormatType.AUDIO_ONLY)]
)
def test_format_selection(
    selector: FormatSelector,
    info: _Info,
    capsys: pytest.CaptureFixture
) -> None:
    sp: SiteProcessor = site_youtube
    fmt = sp.select_format(info, selector)
    with capsys.disabled():
        print(f"{fmt=}")
