"""pyhaversion package."""
from __future__ import annotations

from dataclasses import dataclass

from aiohttp.client import ClientTimeout
from awesomeversion import AwesomeVersion

from .base import HaVersionBase
from .consts import DEFAULT_HEADERS, DEFAULT_IMAGE, HaVersionChannel
from .exceptions import HaVersionFetchException

URL = "https://registry.hub.docker.com/v2/repositories/homeassistant/{image}/tags"


@dataclass
class HaVersionContainer(HaVersionBase):
    """Handle versions for the Container source."""

    def validate_input(self) -> None:
        """Raise HaVersionInputException if expected input are missing."""
        if self.image is None or self.image == DEFAULT_IMAGE:
            self.image = "home-assistant"

    async def fetch(self, **kwargs):
        """Logic to fetch new version data."""
        request = await self.session.get(
            url=kwargs.get("url", URL.format(image=self.image)),
            headers=DEFAULT_HEADERS,
            timeout=ClientTimeout(total=self.timeout),
        )
        self._data = await request.json()
        try:
            self.parse()
        except KeyError as exception:
            raise HaVersionFetchException(
                "Could not handle response from Docker Hub"
            ) from exception
        if not self.version and (next_url := self.data.get("next")):
            await self.fetch(**{"url": next_url})

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
