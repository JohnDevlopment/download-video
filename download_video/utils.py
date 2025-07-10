from __future__ import annotations

import logging
import time
from collections.abc import Callable
from typing import cast

def only_once[T, **P](func: Callable[P, T]) -> Callable[P, T]:
    _init = False
    _result = None

    def _only_once(*args, **kwargs) -> T:
        nonlocal _init, _result
        if not _init:
            _result = func(*args, **kwargs)
            _init = True
        return cast('T', _result)

    return _only_once

def timeof[T, **P](func: Callable[P, T]) -> Callable[P, T]:
    def _timeof(*args: P.args, **kwargs: P.kwargs) -> T:
        tm = time.process_time_ns()
        result = func(*args, **kwargs)
        tm = time.process_time_ns() - tm
        logging.info("")
        return result

    _timeof.__doc__ = func.__doc__
    _timeof.__name__ = func.__name__

    return _timeof
