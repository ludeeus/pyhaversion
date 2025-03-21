"""Tests for PyPi."""

from unittest.mock import patch

import aiohttp
import pytest
from aresponses import ResponsesMockServer

from pyhaversion import (
    HaVersion,
    HaVersionChannel,
    HaVersionInputException,
    HaVersionNotModifiedException,
    HaVersionSource,
)
from tests.common import fixture

from .const import BETA_VERSION, HEADERS, STABLE_VERSION, STABLE_VERSION_BETA_WEEK


@pytest.mark.asyncio
async def test_stable_version(HaVersion: HaVersion) -> None:
    """Test pypi stable."""
    with patch(
        "pyhaversion.pypi.HaVersionPypi.fetch",
        return_value=fixture("pypi/default"),
    ):
        async with aiohttp.ClientSession() as session:
            haversion = HaVersion(
                session=session,
                source=HaVersionSource.PYPI,
            )
            await haversion.get_version()
            assert haversion.version == STABLE_VERSION
            assert haversion.source == HaVersionSource.PYPI


@pytest.mark.asyncio
async def test_beta_version(HaVersion: HaVersion) -> None:
    """Test pypi beta."""
    with patch(
        "pyhaversion.pypi.HaVersionPypi.fetch",
        return_value=fixture("pypi/beta"),
    ):
        async with aiohttp.ClientSession() as session:
            haversion = HaVersion(
                session=session,
                source=HaVersionSource.PYPI,
                channel=HaVersionChannel.BETA,
            )
            await haversion.get_version()
            assert haversion.version == BETA_VERSION


@pytest.mark.asyncio
async def test_stable_version_beta_week(aresponses: ResponsesMockServer) -> None:
    """Test pypi stable during beta week."""
    aresponses.add(
        "pypi.org",
        "/pypi/homeassistant/json",
        "get",
        aresponses.Response(
            text=fixture("pypi/beta", asjson=False),
            status=200,
            headers=HEADERS,
        ),
    )
    async with aiohttp.ClientSession() as session:
        haversion = HaVersion(
            session=session,
            source=HaVersionSource.PYPI,
        )
        await haversion.get_version()
        assert haversion.version == STABLE_VERSION_BETA_WEEK


@pytest.mark.asyncio
async def test_input_exception(HaVersion: HaVersion) -> None:
    """Test input exception."""
    with pytest.raises(HaVersionInputException):
        HaVersion(source=HaVersionSource.PYPI)


@pytest.mark.asyncio
async def test_etag(aresponses: ResponsesMockServer) -> None:
    """Test pypi etag."""
    aresponses.add(
        "pypi.org",
        "/pypi/homeassistant/json",
        "get",
        aresponses.Response(
            text=fixture("pypi/default", asjson=False),
            status=200,
            headers={**HEADERS, "etag": "test"},
        ),
    )
    aresponses.add(
        "pypi.org",
        "/pypi/homeassistant/json",
        "get",
        aresponses.Response(status=304, headers=HEADERS),
    )
    async with aiohttp.ClientSession() as session:
        haversion = HaVersion(session=session, source=HaVersionSource.PYPI)
        await haversion.get_version(etag=haversion.etag)
        assert haversion.version == STABLE_VERSION

        with pytest.raises(HaVersionNotModifiedException):
            await haversion.get_version(etag=haversion.etag)
