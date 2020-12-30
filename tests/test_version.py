import asyncio
from socket import gaierror
from unittest.mock import patch

import pytest
from aiohttp import ClientError

from pyhaversion import HaVersion
from pyhaversion.exceptions import HaVersionFetchException, HaVersionParseException


@pytest.mark.asyncio
async def test_timeout_exception():
    async def mocked_fetch_TimeoutError(_args):
        raise asyncio.TimeoutError

    with patch("pyhaversion.local.HaVersionLocal.fetch", mocked_fetch_TimeoutError):
        haversion = HaVersion()
        with pytest.raises(HaVersionFetchException):
            await haversion.get_version()


@pytest.mark.asyncio
async def test_fetch_exception():
    haversion = HaVersion()

    async def mocked_fetch_ImportError(_args):
        raise ImportError

    async def mocked_fetch_ModuleNotFoundError(_args):
        raise ModuleNotFoundError

    async def mocked_fetch_gaierror(_args):
        raise gaierror

    async def mocked_fetch_ClientError(_args):
        raise ClientError

    with patch("pyhaversion.local.HaVersionLocal.fetch", mocked_fetch_ImportError):
        with pytest.raises(HaVersionFetchException):
            await haversion.get_version()

    with patch(
        "pyhaversion.local.HaVersionLocal.fetch", mocked_fetch_ModuleNotFoundError
    ):
        with pytest.raises(HaVersionFetchException):
            await haversion.get_version()

    with patch("pyhaversion.local.HaVersionLocal.fetch", mocked_fetch_gaierror):
        with pytest.raises(HaVersionFetchException):
            await haversion.get_version()

    with patch("pyhaversion.local.HaVersionLocal.fetch", mocked_fetch_ClientError):
        with pytest.raises(HaVersionFetchException):
            await haversion.get_version()


@pytest.mark.asyncio
async def test_parse_exception():
    haversion = HaVersion()

    async def mocked_fetch(_args):
        pass

    def mocked_parse_KeyError(_args):
        raise KeyError

    def mocked_parse_TypeError(_args):
        raise TypeError

    with patch("pyhaversion.local.HaVersionLocal.fetch", mocked_fetch):
        with patch("pyhaversion.local.HaVersionLocal.parse", mocked_parse_KeyError):
            with pytest.raises(HaVersionParseException):
                await haversion.get_version()

        with patch("pyhaversion.local.HaVersionLocal.parse", mocked_parse_TypeError):
            with pytest.raises(HaVersionParseException):
                await haversion.get_version()
