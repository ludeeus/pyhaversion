"""pyhaversion package."""
import asyncio

import async_timeout
from awesomeversion import AwesomeVersion

from .base import HaVersionBase
from .consts import DEFAULT_HEADERS, DEFAULT_IMAGE, HaVersionChannel
from .exceptions import HaVersionInputException

URL = "https://registry.hub.docker.com/v2/repositories/homeassistant/{image}/tags"


class HaVersionContainer(HaVersionBase):
    """Handle versions for the Container source."""

    def validate_input(self) -> None:
        """Raise HaVersionInputException if expected input are missing."""
        if self.session is None:
            raise HaVersionInputException("Missing aiohttp.ClientSession")
        if self.image is None or self.image == DEFAULT_IMAGE:
            self.image = "home-assistant"

    async def fetch(self, url: str = None):
        """Logic to fetch new version data."""
        url = url if url is not None else URL.format(image=self.image)
        async with async_timeout.timeout(self.timeout, loop=asyncio.get_event_loop()):
            request = await self.session.get(url=url, headers=DEFAULT_HEADERS)
            self._data = await request.json()
        self.parse()
        if not self.version:
            await self.fetch(self.data.get("next"))

    def parse(self):
        """Logic to parse new version data."""
        for image in self.data["results"]:
            version = image["name"]
            if not version.startswith("2"):
                continue
            if not len(version.split(".")) >= 3:
                continue

            version = AwesomeVersion(version)
            if version.dev:
                if self.channel == HaVersionChannel.DEV:
                    self._version = version
                    break
            elif version.beta:
                if self.channel == HaVersionChannel.BETA:
                    self._version = version
                    break
            else:
                self._version = version
                break
