"""HaVersionLocal class."""
from dataclasses import dataclass

from pyhaversion.consts import HaVersionSource

from .base import HaVersionBase


@dataclass
class HaVersionLocal(HaVersionBase):
    """HaVersionLocal class."""

    source = HaVersionSource.LOCAL

    async def fetch(self, **kwargs):
        """Logic to fetch new version data."""
        from homeassistant.const import (
            __version__ as localversion,
        )  # pylint: disable=import-error

        self._data = localversion

    def parse(self):
        """Logic to parse new version data."""
        self._version = self.data
