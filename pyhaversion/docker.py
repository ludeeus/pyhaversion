"""pyhaversion package."""
import asyncio

import async_timeout
from attr import dataclass
from awesomeversion import AwesomeVersion

from .base import HaVersionBase
from .consts import DEFAULT_HEADERS, HaVersionChannel
from .exceptions import HaVersionInputException

URL = "https://registry.hub.docker.com/v2/repositories/homeassistant/{image}/tags"
IMAGES = {
    "default": "home-assistant",
    "intel-nuc": "intel-nuc-homeassistant",
    "odroid-c2": "odroid-c2-homeassistant",
    "odroid-n2": "odroid-n2-homeassistant",
    "odroid-xu": "odroid-xu-homeassistant",
    "qemuarm-64": "qemuarm-64-homeassistant",
    "qemuarm": "qemuarm-homeassistant",
    "qemux86-64": "qemux86-64-homeassistant",
    "qemux86": "qemux86-homeassistant",
    "raspberrypi": "raspberrypi-homeassistant",
    "raspberrypi2": "raspberrypi2-homeassistant",
    "raspberrypi3-64": "raspberrypi3-64-homeassistant",
    "raspberrypi3": "raspberrypi3-homeassistant",
    "raspberrypi4-64": "raspberrypi4-64-homeassistant",
    "raspberrypi4": "raspberrypi4-homeassistant",
    "tinker": "tinker-homeassistant",
}


class HaVersionDocker(HaVersionBase):
    """Handle versions for the Docker source."""

    def validate_input(self) -> None:
        """Raise HaVersionInputException if expected input are missing."""
        if self.session is None:
            raise HaVersionInputException("Missing aiohttp.ClientSession")
        if self.image is None or self.image not in IMAGES:
            self.image = "default"

    async def fetch(self, url: str = None):
        """Logic to fetch new version data."""
        url = url if url is not None else URL.format(image=IMAGES[self.image])
        async with async_timeout.timeout(self.timeout, loop=asyncio.get_event_loop()):
            request = await self.session.get(url=url, headers=DEFAULT_HEADERS)
            self._data = await request.json()
        self.parse()
        if not self.version:
            await self.fetch(self.data.get("next"))

    def parse(self):
        """Logic to parse new version data."""
        for image in self.data["results"]:
            if not image["name"].startswith("2"):
                continue

            version = AwesomeVersion(image["name"])
            if version.dev:
                if self.channel == HaVersionChannel.DEV:
                    self._version = version
                    break
            elif version.beta:
                if self.channel == HaVersionChannel.BETA:
                    self._version = version
                    break
            elif self.channel == HaVersionChannel.STABLE:
                self._version = version
                break
