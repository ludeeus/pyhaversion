import asyncio
import logging

from socket import gaierror
from typing import Tuple

from aiohttp import ClientError, ClientSession
from awesomeversion import AwesomeVersion

from .base import HaVersionBase
from .consts import DEFAULT_TIMEOUT, HaVersionBoard, HaVersionChannel, HaVersionSource
from .local import HaVersionLocal
from .supervised import HaVersionSupervised
from .docker import HaVersionDocker
from .haio import HaVersionHaio
from .pypi import HaVersionPypi

_LOGGER = logging.getLogger(__package__)


class HaVersion:
    def __init__(
        self,
        session: ClientSession = None,
        source: HaVersionSource = HaVersionSource.DEFAULT,
        channel: HaVersionChannel = HaVersionChannel.DEFAULT,
        board: HaVersionBoard = HaVersionBoard.DEFAULT,
        image: str = None,
        timeout: int = DEFAULT_TIMEOUT,
    ):
        self.board = board
        self.channel = channel
        self.session = session
        self.source = source
        self.image = image
        self.timeout = timeout

        handler_args = {
            "board": board,
            "channel": channel,
            "session": session,
            "image": image,
            "source": source,
            "timeout": timeout,
        }
        if self.source == HaVersionSource.DOCKER:
            self._handler = HaVersionDocker(**handler_args)
        elif self.source == HaVersionSource.PYPI:
            self._handler = HaVersionPypi(**handler_args)
        elif self.source == HaVersionSource.SUPERVISED:
            self._handler = HaVersionSupervised(**handler_args)
        elif self.source == HaVersionSource.HAIO:
            self._handler = HaVersionHaio(**handler_args)
        else:
            self._handler = HaVersionLocal(**handler_args)

    @property
    def handler(self) -> HaVersionBase:
        """Return the requested handler."""
        return self._handler

    @property
    def version(self) -> AwesomeVersion:
        """Return the version."""
        return self.handler.version

    @property
    def version_data(self) -> dict:
        """Return extended version data for supported sources."""
        return self.handler.version_data

    async def get_version(self) -> Tuple[AwesomeVersion, dict]:
        try:
            await self.handler.fetch()
        except asyncio.TimeoutError as exception:
            _LOGGER.error(
                "Timeout of %s seconds was reached while fetching version for %s",
                self.timeout,
                self.source,
            )
        except (ClientError, gaierror) as exception:
            _LOGGER.error(
                "Error fetching version information from %s, %s",
                self.source,
                exception,
            )

        try:
            self.handler.parse()
        except (KeyError, TypeError) as exception:
            _LOGGER.error(
                "Error parsing version information for %s, %s",
                self.source,
                exception,
            )

        _LOGGER.debug("Version: %s", self.version)
        _LOGGER.debug("Version data: %s", self.version_data)
        return self.version, self.version_data
