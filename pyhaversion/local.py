"""HaVersionLocal class."""
import logging
from .base import HaVersionBase

_LOGGER = logging.getLogger(__package__)


class HaVersionLocal(HaVersionBase):
    """HaVersionLocal class."""

    async def fetch(self):
        """Logic to fetch new version data."""
        try:
            from homeassistant.const import __version__ as localversion

            self._data = localversion
        except ImportError as error:
            _LOGGER.critical("Home Assistant not found - %s", error)

    def parse(self):
        """Logic to parse new version data."""
        self._version = self.data
