"""Constants for pyhaversion."""
import logging
from enum import Enum

LOGGER: logging.Logger = logging.getLogger(__package__)

DEFAULT_BOARD = "ova"
DEFAULT_IMAGE = "default"
DEFAULT_TIMEOUT = 10
DEFAULT_HEADERS = {
    "User-Agent": "python/pyharversion",
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


class HaVersionSource(str, Enum):
    """Valid sources for pyhaversion."""

    CONTAINER = "container"
    HAIO = "haio"
    LOCAL = "local"
    PYPI = "pypi"
    SUPERVISOR = "supervisor"

    DEFAULT = LOCAL


class HaVersionChannel(str, Enum):
    """Valid version channels."""

    BETA = "beta"
    DEV = "dev"
    STABLE = "stable"

    DEFAULT = STABLE
