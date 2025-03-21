"""Tests for base."""

import asyncio
from socket import gaierror
from typing import NoReturn
from unittest.mock import patch

import pytest
from aiohttp import ClientError

from pyhaversion import (
    HaVersion,
    HaVersionFetchException,
    HaVersionNotModifiedException,
    HaVersionParseException,
)


@pytest.mark.asyncio
async def test_timeout_exception() -> None:
    """Test timeout exception."""

    async def mocked_fetch_timeouterror(*_, **__) -> NoReturn:
        """Mocked."""
        raise asyncio.TimeoutError

    with patch("pyhaversion.local.HaVersionLocal.fetch", mocked_fetch_timeouterror):
        haversion = HaVersion()
        with pytest.raises(HaVersionFetchException):
            await haversion.get_version()


@pytest.mark.asyncio
async def test_fetch_exception() -> None:
    """Test fetch exception."""
    haversion = HaVersion()

    async def mocked_fetch_gaierror(*_, **__) -> NoReturn:
        """Mocked."""
        raise gaierror

    async def mocked_fetch_clienterror(*_, **__) -> NoReturn:
        """Mocked."""
        raise ClientError

    with (
        patch("pyhaversion.local.HaVersionLocal.fetch", mocked_fetch_gaierror),
        pytest.raises(HaVersionFetchException),
    ):
        await haversion.get_version()

    with (
        patch("pyhaversion.local.HaVersionLocal.fetch", mocked_fetch_clienterror),
        pytest.raises(HaVersionFetchException),
    ):
        await haversion.get_version()


@pytest.mark.asyncio
async def test_parse_exception() -> None:
    """Test parse exception."""
    haversion = HaVersion()

    async def mocked_fetch(*_, **__) -> None:
        """Mocked."""

    def mocked_parse_keyerror(*_) -> NoReturn:
        """Mocked."""
        raise KeyError

    def mocked_parse_typeerror(*_) -> NoReturn:
        """Mocked."""
        raise TypeError

    with (
        patch("pyhaversion.local.HaVersionLocal.fetch", mocked_fetch),
        patch("pyhaversion.local.HaVersionLocal.parse", mocked_parse_keyerror),
        pytest.raises(HaVersionParseException),
    ):
        await haversion.get_version()

    with (
        patch("pyhaversion.local.HaVersionLocal.fetch", mocked_fetch),
        patch("pyhaversion.local.HaVersionLocal.parse", mocked_parse_typeerror),
        pytest.raises(HaVersionParseException),
    ):
        await haversion.get_version()


@pytest.mark.asyncio
async def test_not_modified_exception() -> None:
    """Test not_modified exception."""

    async def mocked_fetch_not_modified(*_, **__) -> NoReturn:
        """Mocked."""
        raise HaVersionNotModifiedException

    with patch("pyhaversion.local.HaVersionLocal.fetch", mocked_fetch_not_modified):
        haversion = HaVersion()
        with pytest.raises(HaVersionNotModifiedException):
            await haversion.get_version()
