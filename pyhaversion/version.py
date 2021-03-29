import asyncio
from socket import gaierror
from typing import Tuple

from aiohttp import ClientError, ClientSession
from awesomeversion import AwesomeVersion

from pyhaversion.exceptions import HaVersionFetchException, HaVersionParseException

from .base import HaVersionBase
from .consts import (
    DEFAULT_BOARD,
    DEFAULT_TIMEOUT,
    LOGGER,
    HaVersionChannel,
    HaVersionSource,
)
from .container import HaVersionContainer
from .haio import HaVersionHaio
from .local import HaVersionLocal
from .pypi import HaVersionPypi
from .supervisor import HaVersionSupervisor


class HaVersion(HaVersionBase):
    def __init__(
        self,
        session: ClientSession = None,
        source: HaVersionSource = HaVersionSource.DEFAULT,
        channel: HaVersionChannel = HaVersionChannel.DEFAULT,
        board: str = DEFAULT_BOARD,
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
        if self.source == HaVersionSource.CONTAINER:
            self._handler = HaVersionContainer(**handler_args)
        elif self.source == HaVersionSource.PYPI:
            self._handler = HaVersionPypi(**handler_args)
        elif self.source == HaVersionSource.SUPERVISOR:
            self._handler = HaVersionSupervisor(**handler_args)
        elif self.source == HaVersionSource.HAIO:
            self._handler = HaVersionHaio(**handler_args)
        else:
            self._handler = HaVersionLocal(**handler_args)

    @property
    def version(self) -> AwesomeVersion:
        """Return the version."""
        return self._handler.version

    @property
    def version_data(self) -> dict:
        """Return extended version data for supported sources."""
        return self._handler.version_data

    async def get_version(self) -> Tuple[AwesomeVersion, dict]:
        try:
            await self._handler.fetch()

        except asyncio.TimeoutError as exception:
            raise HaVersionFetchException(
                f"Timeout of {self.timeout} seconds was reached while fetching version for {self.source}"
            ) from exception

        except (ClientError, gaierror, ImportError, ModuleNotFoundError) as exception:
            raise HaVersionFetchException(
                f"Error fetching version information from {self.source} {exception}"
            ) from exception

        try:
            self._handler.parse()

        except (KeyError, TypeError) as exception:
            raise HaVersionParseException(
                f"Error parsing version information for {self.source} - {exception}"
            ) from exception

        LOGGER.debug("Version: %s", self.version)
        LOGGER.debug("Version data: %s", self.version_data)
        return self.version, self.version_data
