"""Tests for Hassio."""

from unittest.mock import patch

import aiohttp
import pytest

from pyhaversion import (
    HaVersion,
    HaVersionChannel,
    HaVersionInputException,
    HaVersionNotModifiedException,
    HaVersionSource,
)
from tests.common import fixture

from .const import HEADERS, STABLE_VERSION


@pytest.mark.asyncio
async def test_stable_version(aresponses):
    """Test hassio stable."""
    aresponses.add(
        "version.home-assistant.io",
        "/stable.json",
        "get",
        aresponses.Response(
            text=fixture("supervisor/default", False), status=200, headers=HEADERS
        ),
    )
    async with aiohttp.ClientSession() as session:
        haversion = HaVersion(session=session, source=HaVersionSource.SUPERVISOR)
        await haversion.get_version()
        assert haversion.version == STABLE_VERSION


@pytest.mark.asyncio
async def test_beta_version(HaVersion):
    """Test hassio beta."""
    with patch(
        "pyhaversion.supervisor.HaVersionSupervisor.data",
        fixture("supervisor/default"),
    ):
        async with aiohttp.ClientSession() as session:
            haversion = HaVersion(
                session=session,
                source=HaVersionSource.SUPERVISOR,
                channel=HaVersionChannel.BETA,
                board="test",
                image="test",
            )
            await haversion.get_version()
            assert haversion.version == STABLE_VERSION


@pytest.mark.asyncio
async def test_input_exception(HaVersion):
    """Test input exception."""
    with pytest.raises(HaVersionInputException):
        HaVersion(source=HaVersionSource.SUPERVISOR)


@pytest.mark.asyncio
async def test_etag(aresponses):
    """Test hassio etag."""
    aresponses.add(
        "version.home-assistant.io",
        "/stable.json",
        "get",
        aresponses.Response(
            text=fixture("supervisor/default", False),
            status=200,
            headers={**HEADERS, "Etag": "test"},
        ),
    )
    aresponses.add(
        "version.home-assistant.io",
        "/stable.json",
        "get",
        aresponses.Response(status=304, headers=HEADERS),
    )
    async with aiohttp.ClientSession() as session:
        haversion = HaVersion(session=session, source=HaVersionSource.SUPERVISOR)
        await haversion.get_version(etag=haversion.etag)
        assert haversion.version == STABLE_VERSION

        with pytest.raises(HaVersionNotModifiedException):
            await haversion.get_version(etag=haversion.etag)
