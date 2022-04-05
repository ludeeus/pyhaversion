"""Tests for Container."""

import json
from unittest.mock import patch

import aiohttp
import pytest

from pyhaversion import HaVersion, HaVersionException
from pyhaversion.consts import HaVersionChannel, HaVersionSource
from tests.common import fixture

from .const import (
    BETA_VERSION,
    BETA_VERSION_BETA_WEEK,
    DEV_VERSION,
    HEADERS,
    STABLE_VERSION,
    STABLE_VERSION_BETA_WEEK,
)


@pytest.mark.asyncio
async def test_stable_version(HaVersion):
    """Test container stable."""
    with patch(
        "pyhaversion.container.HaVersionContainer.data",
        fixture("container/default"),
    ):
        async with aiohttp.ClientSession() as session:
            haversion = HaVersion(session=session, source=HaVersionSource.CONTAINER)
            await haversion.get_version()
            assert haversion.version == STABLE_VERSION


@pytest.mark.asyncio
async def test_beta_version(HaVersion):
    """Test container beta."""
    with patch(
        "pyhaversion.container.HaVersionContainer.data",
        fixture("container/beta_week"),
    ):
        async with aiohttp.ClientSession() as session:
            haversion = HaVersion(
                session=session,
                source=HaVersionSource.CONTAINER,
                channel=HaVersionChannel.BETA,
            )
            await haversion.get_version()
            assert haversion.version == BETA_VERSION


@pytest.mark.asyncio
async def test_dev_version(HaVersion):
    """Test container dev."""
    with patch(
        "pyhaversion.container.HaVersionContainer.data",
        fixture("container/default"),
    ):
        async with aiohttp.ClientSession() as session:
            haversion = HaVersion(
                session=session,
                source=HaVersionSource.CONTAINER,
                channel=HaVersionChannel.DEV,
            )
            await haversion.get_version()
            assert haversion.version == DEV_VERSION


@pytest.mark.asyncio
async def test_stable_version_beta_week(HaVersion):
    """Test container stable during beta week."""
    with patch(
        "pyhaversion.container.HaVersionContainer.data",
        fixture("container/beta_week"),
    ):
        async with aiohttp.ClientSession() as session:
            haversion = HaVersion(
                session=session,
                source=HaVersionSource.CONTAINER,
            )
            await haversion.get_version()
            assert haversion.version == STABLE_VERSION_BETA_WEEK


@pytest.mark.asyncio
async def test_beta_version_beta_week(HaVersion):
    """Test container beta during beta week."""
    with patch(
        "pyhaversion.container.HaVersionContainer.data",
        fixture("container/beta_week"),
    ):
        async with aiohttp.ClientSession() as session:
            haversion = HaVersion(
                session=session,
                source=HaVersionSource.CONTAINER,
                channel=HaVersionChannel.BETA,
            )
        await haversion.get_version()
        assert haversion.version == BETA_VERSION_BETA_WEEK


@pytest.mark.asyncio
async def test_stable_version_pagination(aresponses):
    """Test container beta during beta week."""
    aresponses.add(
        "registry.hub.docker.com",
        "/v2/repositories/homeassistant/home-assistant/tags",
        "get",
        aresponses.Response(
            text=fixture("container/page1", False), status=200, headers=HEADERS
        ),
    )
    aresponses.add(
        "registry.hub.docker.com",
        "/v2/repositories/homeassistant/home-assistant/tags/page2",
        "get",
        aresponses.Response(
            text=fixture("container/page2", False), status=200, headers=HEADERS
        ),
    )
    async with aiohttp.ClientSession() as session:
        haversion = HaVersion(
            session=session,
            source=HaVersionSource.CONTAINER,
        )
        await haversion.get_version()
        assert haversion.version == STABLE_VERSION


@pytest.mark.asyncio
async def test_beta_version_pagination(aresponses):
    """Test container beta during beta week."""
    aresponses.add(
        "registry.hub.docker.com",
        "/v2/repositories/homeassistant/home-assistant/tags",
        "get",
        aresponses.Response(
            text=fixture("container/beta_week_page1", False),
            status=200,
            headers=HEADERS,
        ),
    )
    aresponses.add(
        "registry.hub.docker.com",
        "/v2/repositories/homeassistant/home-assistant/tags/page2",
        "get",
        aresponses.Response(
            text=fixture("container/beta_week_page2", False),
            status=200,
            headers=HEADERS,
        ),
    )
    async with aiohttp.ClientSession() as session:
        haversion = HaVersion(
            session=session,
            source=HaVersionSource.CONTAINER,
            channel=HaVersionChannel.BETA,
        )
        await haversion.get_version()
        assert haversion.version == BETA_VERSION


@pytest.mark.asyncio
async def test_stable_version_beta_week_pagination(aresponses):
    """Test container beta during beta week."""
    aresponses.add(
        "registry.hub.docker.com",
        "/v2/repositories/homeassistant/home-assistant/tags",
        "get",
        aresponses.Response(
            text=fixture("container/beta_week_page1", False),
            status=200,
            headers=HEADERS,
        ),
    )
    aresponses.add(
        "registry.hub.docker.com",
        "/v2/repositories/homeassistant/home-assistant/tags/page2",
        "get",
        aresponses.Response(
            text=fixture("container/beta_week_page2", False),
            status=200,
            headers=HEADERS,
        ),
    )

    async with aiohttp.ClientSession() as session:
        haversion = HaVersion(
            session=session,
            source=HaVersionSource.CONTAINER,
        )
        await haversion.get_version()
        assert haversion.version == STABLE_VERSION_BETA_WEEK


@pytest.mark.asyncio
async def test_beta_version_beta_week_pagination(aresponses):
    """Test container beta during beta week."""
    aresponses.add(
        "registry.hub.docker.com",
        "/v2/repositories/homeassistant/home-assistant/tags",
        "get",
        aresponses.Response(
            text=fixture("container/beta_week_page1", False),
            status=200,
            headers=HEADERS,
        ),
    )
    aresponses.add(
        "registry.hub.docker.com",
        "/v2/repositories/homeassistant/home-assistant/tags/page2",
        "get",
        aresponses.Response(
            text=fixture("container/beta_week_page2", False),
            status=200,
            headers=HEADERS,
        ),
    )

    async with aiohttp.ClientSession() as session:
        haversion = HaVersion(
            session=session,
            source=HaVersionSource.CONTAINER,
            channel=HaVersionChannel.BETA,
        )
        await haversion.get_version()
        assert haversion.version == BETA_VERSION_BETA_WEEK


@pytest.mark.asyncio
async def test_keyerror(aresponses):
    """Test container KeyError."""
    aresponses.add(
        "registry.hub.docker.com",
        "/v2/repositories/homeassistant/home-assistant/tags",
        "get",
        aresponses.Response(
            text="{}",
            status=200,
            headers=HEADERS,
        ),
    )

    async with aiohttp.ClientSession() as session:
        haversion = HaVersion(
            session=session,
            source=HaVersionSource.CONTAINER,
            channel=HaVersionChannel.BETA,
        )
        with pytest.raises(HaVersionException):
            await haversion.get_version()
            assert haversion.version is None

        haversion._handler._version = "1.2.3"

        with pytest.raises(HaVersionException):
            await haversion.get_version()
            assert haversion.version == "1.2.3"
