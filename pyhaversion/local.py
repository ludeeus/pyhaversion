"""HaVersionLocal class."""
from .base import HaVersionBase


class HaVersionLocal(HaVersionBase):
    """HaVersionLocal class."""

    async def fetch(self):
        """Logic to fetch new version data."""
        from homeassistant.const import __version__ as localversion

        self._data = localversion

    def parse(self):
        """Logic to parse new version data."""
        self._version = self.data
