"""
A python module to the newest version number of Home Assistant.

This code is released under the terms of the MIT license. See the LICENSE
file for more details.
"""
import asyncio
import logging
import socket
import re

import aiohttp
import async_timeout
from pyhaversion.consts import BOARDS, IMAGES, URL


_LOGGER = logging.getLogger(__name__)


class Version:
    """A class for returning HA version information from different sources."""

    def __init__(self, loop, session, branch="stable", image="default"):
        """Initialize the class."""
        self.loop = loop
        self.session = session
        self.branch = branch
        self.image = image
        self._version = None
        self._version_data = {}

    @property
    def beta(self):
        """Return bool if beta versions should be returned."""
        return self.branch != "stable"

    @property
    def version(self):
        """Return the version."""
        return self._version

    @property
    def version_data(self):
        """Return extended version data for supported sources."""
        return self._version_data


class LocalVersion(Version):
    """Local version."""

    async def get_version(self):
        """Get version."""
        self._version_data["source"] = "Local"
        try:
            from homeassistant.const import __version__ as localversion

            self._version = localversion

            _LOGGER.debug("Version: %s", self.version)
            _LOGGER.debug("Version data: %s", self.version_data)

        except ImportError as error:
            _LOGGER.critical("Home Assistant not found - %s", error)
        except Exception as error:  # pylint: disable=broad-except
            _LOGGER.critical("Something really wrong happend! - %s", error)


class DockerVersion(Version):
    """Docker version."""

    async def get_version(self):
        """Get version."""
        if self.image not in IMAGES:
            _LOGGER.warning("%s is not a valid image using default", self.image)
            self.image = "default"

        self._version_data["beta"] = self.beta
        self._version_data["source"] = "Docker"
        self._version_data["image"] = IMAGES[self.image]["docker"]
        try:
            async with async_timeout.timeout(5, loop=self.loop):
                response = await self.session.get(
                    URL["docker"].format(IMAGES[self.image]["docker"])
                )
                data = await response.json()
                for version in data["results"]:
                    if version["name"] in [
                        "latest",
                        "landingpage",
                        "rc",
                        "dev",
                        "beta",
                        "stable",
                    ]:
                        continue
                    elif re.search(r"\b.+b\d", version["name"]):
                        if self.beta:
                            self._version = version["name"]
                            break
                        else:
                            continue
                    else:
                        self._version = version["name"]

                    if self._version is not None:
                        break
                    else:
                        continue

            _LOGGER.debug("Version: %s", self.version)
            _LOGGER.debug("Version data: %s", self.version_data)

        except asyncio.TimeoutError as error:
            _LOGGER.error(
                "Timeouterror fetching version information from %s, %s",
                self._version_data["source"],
                error,
            )
        except (KeyError, TypeError) as error:
            _LOGGER.error(
                "Error parsing version information from %s, %s",
                self._version_data["source"],
                error,
            )
        except (aiohttp.ClientError, socket.gaierror) as error:
            _LOGGER.error(
                "Error fetching version information from %s, %s",
                self._version_data["source"],
                error,
            )
        except Exception as error:  # pylint: disable=broad-except
            _LOGGER.critical("Something really wrong happend! - %s", error)


class HassioVersion(Version):
    """Local version."""

    async def get_version(self):
        """Get version."""
        if self.image not in IMAGES:
            _LOGGER.warning("%s is not a valid image using default", self.image)
            self.image = "default"

        board = BOARDS.get(self.image, BOARDS["default"])

        self._version_data["source"] = "Hassio"
        self._version_data["beta"] = self.beta
        self._version_data["board"] = board
        self._version_data["image"] = IMAGES[self.image]["hassio"]

        try:
            async with async_timeout.timeout(5, loop=self.loop):
                response = await self.session.get(
                    URL["hassio"]["beta" if self.beta else "stable"]
                )
                data = await response.json()

                self._version = data["homeassistant"][IMAGES[self.image]["hassio"]]

                self._version_data["hassos"] = data["hassos"][board]
                self._version_data["supervisor"] = data["supervisor"]
                self._version_data["hassos-cli"] = data["hassos-cli"]

            _LOGGER.debug("Version: %s", self.version)
            _LOGGER.debug("Version data: %s", self.version_data)

        except asyncio.TimeoutError as error:
            _LOGGER.error(
                "Timeouterror fetching version information from %s, %s",
                self._version_data["source"],
                error,
            )
        except (KeyError, TypeError) as error:
            _LOGGER.error(
                "Error parsing version information from %s, %s",
                self._version_data["source"],
                error,
            )
        except (aiohttp.ClientError, socket.gaierror) as error:
            _LOGGER.error(
                "Error fetching version information from %s, %s",
                self._version_data["source"],
                error,
            )
        except Exception as error:  # pylint: disable=broad-except
            _LOGGER.critical("Something really wrong happend! - %s", error)


class PyPiVersion(Version):
    """Local version."""

    async def get_version(self):
        """Get version."""
        self._version_data["beta"] = self.beta
        self._version_data["source"] = "PyPi"

        info_version = None
        last_release = None

        try:
            async with async_timeout.timeout(5, loop=self.loop):
                response = await self.session.get(URL["pypi"])
            data = await response.json()

            info_version = data["info"]["version"]
            releases = data["releases"]

            for version in sorted(releases, reverse=True):
                if re.search(r"^(\\d+\\.)?(\\d\\.)?(\\*|\\d+)$", version):
                    continue
                else:
                    last_release = version
                    break

            self._version = info_version

            if self.beta:
                if info_version in last_release:
                    self._version = info_version
                else:
                    self._version = last_release

            _LOGGER.debug("Version: %s", self.version)
            _LOGGER.debug("Version data: %s", self.version_data)

        except asyncio.TimeoutError as error:
            _LOGGER.error(
                "Timeouterror fetching version information from %s, %s",
                self._version_data["source"],
                error,
            )
        except (KeyError, TypeError) as error:
            _LOGGER.error(
                "Error parsing version information from %s, %s",
                self._version_data["source"],
                error,
            )
        except (aiohttp.ClientError, socket.gaierror) as error:
            _LOGGER.error(
                "Error fetching version information from %s, %s",
                self._version_data["source"],
                error,
            )
        except Exception as error:  # pylint: disable=broad-except
            _LOGGER.critical("Something really wrong happend! - %s", error)
