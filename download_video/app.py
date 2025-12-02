from __future__ import annotations

import logging
from typing import Annotated, Optional

import click
import typer
from result import Err, Ok

from . import APP
from .my_logging import setup_logging, LogLevel
from .site_processors import match_url, register_site_processors
from .site_processors.formats import FormatSelector, FormatType

CONTEXT_SETTINGS = {
    'help_option_names': ["--help", "-h"],
}
app = typer.Typer(context_settings=CONTEXT_SETTINGS)
_logger: logging.Logger

class MutuallyExclusiveParameters(click.UsageError):
    def __init__(self, option_names: list[str], ctx: click.Context | None = None) -> None:
        assert len(option_names) >= 2
        msg: str
        match option_names:
            case [n1, n2]:
                msg = f"{n1} and {n2} are mutually exclusive"

            case _:
                *option_names, last_name = option_names
                msg = f"{', '.join(option_names)}, and {last_name} are mutually exclusive"

        super().__init__(msg, ctx)

@app.callback()
def main(
    ctx: typer.Context,
    loglevel: Annotated[
        LogLevel,
        typer.Option(show_default=False,
                     help="Set the logging level.",
                     envvar="JDV_LOGLEVEL",
                     metavar="LEVEL")
    ] = LogLevel.INFO,
    debug: Annotated[
        bool,
        typer.Option("--debug",
                     show_default=False,
                     help="Enter debug mode.")
    ] = False
):
    """
    Jdv is a video downloader based on Yt-Dlp.  To put it a
    different way, jdv is a simpliifed version of Yt-dlp.  The
    options listed below are applied globally.

    The --loglevel option accepts one of DEBUG, INFO, WARN,
    ERROR, or CRITICAL.
    """
    # Setup logging system
    global _logger
    setup_logging(APP, loglevel)
    _logger = logging.getLogger(APP)
    _logger.info("Logging system activated")

    ctx.obj = {'debug': debug}

@app.command()
def ost(
    url: Annotated[
        str,
        typer.Argument(show_default=False, help="The URL to parse.")
    ],
    title: Annotated[
        Optional[str],
        typer.Option(show_default=False, help="Embed TITLE in the output.")
    ]=None,
    artist: Annotated[
        Optional[str],
        typer.Option(show_default=False, help="Embed ARTIST in the output.")
    ]=None,
    album: Annotated[
        Optional[str],
        typer.Option(show_default=False, help="Embed ALBUM in the output.")
    ]=None,
    genre: Annotated[
        Optional[str],
        typer.Option(show_default=False, help="Embed GENRE in the output.")
    ]=None
) -> int:
    register_site_processors()

    sp = None
    match match_url(url):
        case Ok(tp):
            sp, url = tp

        case Err(e):
            raise typer.BadParameter(str(e), param_hint="URL")

    info = sp.extract_info(url)
    fmt = sp.select_format(info, FormatSelector(None, FormatType.AUDIO_ONLY))

    return 0

@app.command()
def video(
    ctx: typer.Context,
    url_or_file: Annotated[
        str,
        typer.Argument(show_default=False, help="The URL or file to parse.")
    ],
    video_only: Annotated[
        bool,
        typer.Option("--video-only", show_default=False, help="Select a video-only format.")
    ] = False,
    height: Annotated[
        Optional[int],
        typer.Option(show_default=False, help="For video formats, select based on height.")
    ] = None,
    audio_only: Annotated[
        bool,
        typer.Option("--audio-only", show_default=False, help="Select an audio-only format.")
    ] = False,
    rename: Annotated[
        bool,
        typer.Option("--rename", show_default=False, help="Rename a file.")
    ] = False
) -> int:
    """
    Download a video from the internet using certain criteria.
    """
    if video_only and audio_only:
        raise MutuallyExclusiveParameters(["--video-only", "--audio-only"])

    register_site_processors()

    # If not video only, will either be audio only or have both
    temp = FormatType.VIDEO_ONLY
    if not video_only:
        temp = FormatType.AUDIO_ONLY if audio_only else FormatType.AUDIO_VIDEO
    selector = FormatSelector(height, temp)

    if rename:
        raise NotImplementedError

    url = url_or_file
    sp = None
    match match_url(url):
        case Ok(tp):
            sp, url = tp

        case Err(e):
            raise typer.BadParameter(str(e), param_hint="URL_OR_FILE")

    info = sp.extract_info(url)
    fmt = sp.select_format(info, selector)
    sp.download(url, fmt)

    return 0
