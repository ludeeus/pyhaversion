"""HaVersionLocal class."""
from dataclasses import dataclass

from .base import HaVersionBase
from .consts import LOGGER

try:
    from homeassistant.const import __version__ as localversion
except (ModuleNotFoundError, ImportError):
    localversion = None


@dataclass
class HaVersionLocal(HaVersionBase):
    """HaVersionLocal class."""

    async def fetch(self, **kwargs):
        """Logic to fetch new version data."""
        if localversion is None:
            LOGGER.error("No homeassistant installation found")
        self._data = localversion

    def parse(self):
        """Logic to parse new version data."""
        self._version = self.data

    @property
    def version_data(self) -> None:
        """Return extended version data."""
        return None
