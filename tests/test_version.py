"""Tests for base"""

import asyncio
from socket import gaierror
from unittest.mock import patch

import pytest
from aiohttp import ClientError, ClientResponse

from pyhaversion import (
    HaVersion,
    HaVersionFetchException,
    HaVersionNotModifiedException,
    HaVersionParseException,
)


@pytest.mark.asyncio
async def test_timeout_exception():
    """Test timeout exception."""

    async def mocked_fetch_TimeoutError(*_, **__):
        """mocked"""
        raise asyncio.TimeoutError

    with patch("pyhaversion.local.HaVersionLocal.fetch", mocked_fetch_TimeoutError):
        haversion = HaVersion()
        with pytest.raises(HaVersionFetchException):
            await haversion.get_version()


@pytest.mark.asyncio
async def test_fetch_exception():
    """Test fetch exception."""
    haversion = HaVersion()

    async def mocked_fetch_gaierror(*_, **__):
        """mocked"""
        raise gaierror

    async def mocked_fetch_ClientError(*_, **__):
        """mocked"""
        raise ClientError

    with patch("pyhaversion.local.HaVersionLocal.fetch", mocked_fetch_gaierror):
        with pytest.raises(HaVersionFetchException):
            await haversion.get_version()

    with patch("pyhaversion.local.HaVersionLocal.fetch", mocked_fetch_ClientError):
        with pytest.raises(HaVersionFetchException):
            await haversion.get_version()


@pytest.mark.asyncio
async def test_parse_exception():
    """Test parse exception."""
    haversion = HaVersion()

    async def mocked_fetch(*_, **__):
        """mocked"""
        pass

    def mocked_parse_KeyError(*_):
        """mocked"""
        raise KeyError

    def mocked_parse_TypeError(*_):
        """mocked"""
        raise TypeError

    with patch("pyhaversion.local.HaVersionLocal.fetch", mocked_fetch):
        with patch("pyhaversion.local.HaVersionLocal.parse", mocked_parse_KeyError):
            with pytest.raises(HaVersionParseException):
                await haversion.get_version()

        with patch("pyhaversion.local.HaVersionLocal.parse", mocked_parse_TypeError):
            with pytest.raises(HaVersionParseException):
                await haversion.get_version()


@pytest.mark.asyncio
async def test_not_modified_exception():
    """Test not_modified exception."""

    async def mocked_fetch_not_modified(*_, **__):
        """mocked"""
        raise HaVersionNotModifiedException

    with patch("pyhaversion.local.HaVersionLocal.fetch", mocked_fetch_not_modified):
        haversion = HaVersion()
        with pytest.raises(HaVersionNotModifiedException):
            await haversion.get_version()
