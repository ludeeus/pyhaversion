"""Constants for pyhaversion."""
from __future__ import annotations

import logging
from enum import Enum
from typing import Any

LOGGER: logging.Logger = logging.getLogger(__package__)

DEFAULT_BOARD = "ova"
DEFAULT_IMAGE = "default"
DEFAULT_TIMEOUT = 10
DEFAULT_HEADERS = {
    "User-Agent": "python/pyhaversion",
    "Content-Type": "application/json",
}

DATA_AUDIO = "audio"
DATA_BOARD = "board"
DATA_CHANNEL = "channel"
DATA_CLI = "cli"
DATA_CURRENT_VERSION = "current_version"
DATA_DNS = "dns"
DATA_HASSOS = "hassos"
DATA_HOMEASSISTANT = "homeassistant"
DATA_IMAGE = "image"
DATA_INFO = "info"
DATA_MULTICAST = "multicast"
DATA_OBSERVER = "observer"
DATA_OS = "os"
DATA_RAW = "raw"
DATA_RELEASE_DATE = "release_date"
DATA_RELEASE_DESCRIPTION = "release_description"
DATA_RELEASE_NOTES = "release_notes"
DATA_RELEASE_TITLE = "release_title"
DATA_RELEASES = "releases"
DATA_SOURCE = "source"
DATA_SUPERVISOR = "supervisor"
DATA_VERSION = "version"


class StrEnum(str, Enum):
    """Partial backport of Python 3.11's StrEnum."""

    def __new__(cls, value: str, *args: Any, **kwargs: Any) -> StrEnum:
        """Create a new StrEnum instance."""
        if not isinstance(value, str):
            raise TypeError(f"{value!r} is not a string")
        return super().__new__(cls, value, *args, **kwargs)

    def __str__(self) -> str:
        """Return self.value."""
        return str(self.value)


class HaVersionSource(StrEnum):
    """Valid sources for pyhaversion."""

    CONTAINER = "container"
    HAIO = "haio"
    LOCAL = "local"
    PYPI = "pypi"
    SUPERVISOR = "supervisor"

    DEFAULT = LOCAL


class HaVersionChannel(StrEnum):
    """Valid version channels."""

    BETA = "beta"
    DEV = "dev"
    STABLE = "stable"

    DEFAULT = STABLE
