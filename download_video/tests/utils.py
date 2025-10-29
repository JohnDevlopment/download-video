from __future__ import annotations

import base64
import json
import os


def json_from_base64(s: str):
    data = base64.b64decode(s)
    data = data.decode()
    return json.loads(data)

def load_env(name: str):
    value = os.getenv(name)
    if value is None:
        raise EnvironmentError(f"{name} is not defined in the environment")
    return value
