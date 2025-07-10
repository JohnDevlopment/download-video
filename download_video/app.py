from __future__ import annotations

import logging
from typing import Annotated, Optional

import typer
from result import Err, Ok
from typer import Argument, Option, Typer

from . import APP
from .my_logging import setup_logging
from .site_processors import match_url, register_site_processors
from .site_processors.formats import FormatSelector, FormatType

CONTEXT_SETTINGS = {
    'help_option_names': ["--help", "-h"],
}
app = Typer(context_settings=CONTEXT_SETTINGS)
_logger = logging.getLogger(APP)

@app.command()
def ost(
    url_or_file: Annotated[str, Argument(show_default=False)],
    title: Annotated[Optional[str], Option("-t", "--title", show_default=False,
                                           help="Embed title into file.")]=None,
    artist: Annotated[Optional[str], Option("-a", "--artist", show_default=False,
                                            help="Embed artist into file.")]=None,
    album: Annotated[Optional[str], Option("-A", "--album", show_default=False,
                                           help="Embed album into file.")]=None,
    genre: Annotated[Optional[str], Option("-g", "--genre", show_default=False,
                                           help="Embed genre into file.")]=None
):
    """
    Download audio from the internet with optional metadata.
    """
    pass

@app.command()
def video(
    url_or_file: Annotated[str, Argument(show_default=False)],
    rename: Annotated[bool, typer.Option("--rename", "-r",
                                         help="Rename file.")]=False
) -> int:
    """
    Download a video from the internet using certain criteria.
    """
    setup_logging()
    register_site_processors()

    selector = FormatSelector(None, FormatType.VIDEO_ONLY)

    if rename:
        return 0

    url = url_or_file
    sp = None
    match match_url(url):
        case Ok(tp):
            sp, url = tp

        case Err(e):
            _logger.error(e)
            return 1

    info = sp.extract_info(url)
    fmt = sp.select_format(info, selector)
    sp.download(url, fmt)

    return 0
