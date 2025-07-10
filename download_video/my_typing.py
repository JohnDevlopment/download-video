from __future__ import annotations

from typing import Protocol


class Pathlike(Protocol):
    def __fspath__(self) -> str:
        ...

type StrPath = str | Pathlike
