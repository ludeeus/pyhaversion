"""
A python module to the newest version number of Home Assistant.

This code is released under the terms of the MIT license. See the LICENSE
file for more details.
"""
import asyncio
import logging
import socket

import aiohttp
import async_timeout


_LOGGER = logging.getLogger(__name__)


class Version(object):
    """A class for returning HA version information from different sources."""

    def __init__(self, loop, session='none', branch='', image='default'):
        """Initialize the class."""
        self._loop = loop
        self._session = session
        self._branch = branch
        self._image = image
        self._version = None
        self._version_data = {}

    async def get_local_version(self):
        """Get the local installed version."""
        try:
            from homeassistant.const import __version__ as localversion
            self._version = localversion
            self._version_data['source'] = 'Local'
        except ImportError:
            _LOGGER.critical('Home Assistant installation not found.')

    async def get_pypi_version(self):
        """Get version published to PyPi."""
        base_url = 'https://pypi.org/pypi/homeassistant/json'
        try:
            async with async_timeout.timeout(5, loop=self._loop):
                response = await self._session.get(base_url)
            data = await response.json()
            if self._branch == 'beta':
                releases = data['releases']
                all_versions = []
                for versions in sorted(releases, reverse=True):
                    all_versions.append(versions)
                num = 0
                controll = 0
                while controll < 1:
                    name = all_versions[num]
                    if '.8.' in name or '.9.' in name:
                        num = num + 1
                    else:
                        controll = 1
                        self._version = name
                        self._version_data['beta'] = True
            else:
                self._version = data['info']['version']
                self._version_data['source'] = 'PyPi'
            _LOGGER.debug('Pip version: %s', self._version)
        except (asyncio.TimeoutError,
                aiohttp.ClientError, socket.gaierror) as error:
            _LOGGER.error('Error fetching version from PyPi, %s', error)

    async def get_hassio_version(self):
        """Get version published for hassio."""
        url_stable = 'https://s3.amazonaws.com/hassio-version/stable.json'
        url_beta = 'https://s3.amazonaws.com/hassio-version/beta.json'
        boards = {
            "default": "ova",
            "raspberrypi": "rpi",
            "raspberrypi2": "rpi2",
            "raspberrypi3": "rpi3",
            "raspberrypi3-64": "rpi3-64",
            "tinker": "tinker",
            "odroid-c2": "odroid-c2",
            "odroid-xu": "odroid-c2"
        }
        try:
            async with async_timeout.timeout(5, loop=self._loop):
                if self._branch == 'beta':
                    response = await self._session.get(url_beta)
                    self._version_data['beta'] = True
                else:
                    response = await self._session.get(url_stable)
            data = await response.json()
            self._version = data['homeassistant'][self._image]
            self._version_data['source'] = 'Hassio'
            board = boards.get(self._image, boards['default'])
            self._version_data['hassos'] = data['hassos'][board]
            self._version_data['supervisor'] = data['supervisor']
            self._version_data['hassos-cli'] = data['hassos-cli']
            _LOGGER.debug('Hassio version: %s', self._version)
        except (asyncio.TimeoutError,
                KeyError, TypeError,
                aiohttp.ClientError, socket.gaierror) as error:
            _LOGGER.error('Error fetching version information for hassio, %s',
                          error)

    async def get_docker_version(self):
        """Get version published for docker."""
        if self._image == 'default':
            self._image = 'home-assistant'
        url = "https://registry.hub.docker.com/v1/repositories/homeassistant/"
        url += "{}/tags".format(self._image)
        try:
            async with async_timeout.timeout(5, loop=self._loop):
                response = await self._session.get(url)
                if response.status == 404:
                    self._version = None
                    self._version_data = {'error': 'image not supported',
                                          'image': self._image}
                    _LOGGER.critical("image not supported '%s'", self._image)
                else:
                    data = await response.json()
                    num = -1
                    controll = 0
                    if self._branch == 'beta':
                        self._version_data['beta'] = True
                        while controll < 1:
                            name = data[num]['name']
                            if 'd' in name or 'r' in name:
                                num = num - 1
                            else:
                                controll = 1
                                self._version = name
                    else:
                        while controll < 1:
                            name = data[num]['name']
                            if 'd' in name or 'r' in name or 'b' in name:
                                num = num - 1
                            else:
                                controll = 1
                                self._version = name
            self._version_data['source'] = 'Docker'
            _LOGGER.debug('Docker version: %s', self._version)
        except (asyncio.TimeoutError,
                KeyError, TypeError,
                aiohttp.ClientError, socket.gaierror) as error:
            _LOGGER.error('Error fetching version from dockerhub, %s',
                          error)

    @property
    def version(self):
        """Return the version."""
        return self._version

    @property
    def version_data(self):
        """Return extended version data for supported sources."""
        return self._version_data
