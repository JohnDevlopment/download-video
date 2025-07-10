from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterable

class InvalidURLError(ValueError):
    def __init__(self, url: str, spec, *specs: str):
        msg = f"'{url}' does not match "
        if specs:
            temp = ", ".join([spec, *specs])
            msg += f"any of the specs {temp}"
        else:
            msg += f"the spec '{spec}'"

        super().__init__(msg)
        self.url = url
        self.specs = specs
