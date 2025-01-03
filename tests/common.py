"""Common test utilities."""

from __future__ import annotations

import json
from pathlib import Path


def fixture(filename: str, asjson: bool = True) -> str | dict:
    """Load a fixture."""
    path = Path(Path(__file__).parent, "fixtures", f"{filename}.json")
    with path.open(encoding="utf-8") as fptr:
        if asjson:
            return json.loads(fptr.read())
        return fptr.read()
