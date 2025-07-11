from __future__ import annotations

import logging
from typing import Optional, cast

import click
import typer
from click_option_group import MutuallyExclusiveOptionGroup, optgroup
from result import Err, Ok

from .my_logging import setup_logging
from .site_processors import match_url, register_site_processors
from .site_processors.formats import FormatSelector, FormatType

CONTEXT_SETTINGS = {
    'help_option_names': ["--help", "-h"],
}

@app.callback()
def main():
    """
    Video downloader.
    """

@click.command()
@optgroup("Group 1", cls=MutuallyExclusiveOptionGroup)
@optgroup.option("--video-only", is_flag=True, default=False,)
@optgroup.option("--audio-only", is_flag=True, default=False,)
@click.argument("url_or_file")
@click.option("-r", "--rename", is_flag=True, default=False,
              help="Rename file; treats URL_OR_FILE as FILE.")
@click.option("--height", type=int, default=None,
              help="Maximum height of the video; ignored if --audio-only.")
def video(
    url_or_file: str,
    video_only: bool,
    height: Optional[int],
    audio_only: bool,
    rename: bool
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
            raise typer.BadParameter(f"Bad URL: {e}")

    info = sp.extract_info(url)
    fmt = sp.select_format(info, selector)
    sp.download(url, fmt)

    return 0

cli = cast("click.Group", typer.main.get_command(app))
cli.add_command(video)
