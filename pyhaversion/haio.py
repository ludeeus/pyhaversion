"""pyhaversion package."""
from dataclasses import dataclass

from aiohttp.client import ClientTimeout

from .base import HaVersionBase
from .consts import (
    DATA_CURRENT_VERSION,
    DATA_RELEASE_DATE,
    DATA_RELEASE_DESCRIPTION,
    DATA_RELEASE_NOTES,
    DATA_RELEASE_TITLE,
    DEFAULT_HEADERS,
    HaVersionSource,
)

URL = "https://www.home-assistant.io/version.json"


@dataclass
class HaVersionHaio(HaVersionBase):
    """Handle versions for the home-assistant.io source."""

    source = HaVersionSource.HAIO

    async def fetch(self, **kwargs):
        """Logic to fetch new version data."""
        request = await self.session.get(
            url=URL,
            headers=DEFAULT_HEADERS,
            timeout=ClientTimeout(total=self.timeout),
        )
        self._data = await request.json()

    def parse(self):
        """Logic to parse new version data."""
        self._version = self.data.get(DATA_CURRENT_VERSION)
        self._version_data = {
            DATA_RELEASE_DATE: self.data.get(DATA_RELEASE_DATE),
            DATA_RELEASE_NOTES: self.data.get(DATA_RELEASE_NOTES),
            DATA_RELEASE_TITLE: self.data.get(DATA_RELEASE_TITLE),
            DATA_RELEASE_DESCRIPTION: self.data.get(DATA_RELEASE_DESCRIPTION),
        }
