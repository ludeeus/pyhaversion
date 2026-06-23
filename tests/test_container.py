"""Tests for Container."""

from unittest.mock import patch

import aiohttp
import pytest
from aresponses import ResponsesMockServer

from pyhaversion import HaVersion, HaVersionException
from pyhaversion.consts import DATA_RELEASE_DATE, HaVersionChannel, HaVersionSource
from tests.common import fixture

from .const import (
    BETA_RELEASE_DATE,
    BETA_VERSION,
    BETA_VERSION_BETA_WEEK,
    DEV_RELEASE_DATE,
    DEV_VERSION,
    HEADERS,
    STABLE_RELEASE_DATE,
    STABLE_VERSION,
    STABLE_VERSION_BETA_WEEK,
)


@pytest.mark.asyncio
async def test_stable_version(HaVersion: HaVersion) -> None:
    """Test container stable."""
    with patch(
        "pyhaversion.container.HaVersionContainer.fetch",
        return_value=fixture("container/default"),
    ):
        async with aiohttp.ClientSession() as session:
            haversion = HaVersion(session=session, source=HaVersionSource.CONTAINER)
            await haversion.get_version()
            assert haversion.version == STABLE_VERSION


@pytest.mark.asyncio
async def test_beta_version(HaVersion: HaVersion) -> None:
    """Test container beta."""
    with patch(
        "pyhaversion.container.HaVersionContainer.fetch",
        return_value=fixture("container/beta_week"),
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
async def test_dev_version(HaVersion: HaVersion) -> None:
    """Test container dev."""
    with patch(
        "pyhaversion.container.HaVersionContainer.fetch",
        return_value=fixture("container/default"),
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
async def test_stable_version_beta_week(HaVersion: HaVersion) -> None:
    """Test container stable during beta week."""
    with patch(
        "pyhaversion.container.HaVersionContainer.fetch",
        return_value=fixture("container/beta_week"),
    ):
        async with aiohttp.ClientSession() as session:
            haversion = HaVersion(
                session=session,
                source=HaVersionSource.CONTAINER,
            )
            await haversion.get_version()
            assert haversion.version == STABLE_VERSION_BETA_WEEK


@pytest.mark.asyncio
async def test_beta_version_beta_week(HaVersion: HaVersion) -> None:
    """Test container beta during beta week."""
    with patch(
        "pyhaversion.container.HaVersionContainer.fetch",
        return_value=fixture("container/beta_week"),
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
async def test_stable_version_pagination(aresponses: ResponsesMockServer) -> None:
    """Test container beta during beta week."""
    aresponses.add(
        "registry.hub.docker.com",
        "/v2/repositories/homeassistant/home-assistant/tags",
        "get",
        aresponses.Response(
            text=fixture("container/page1", asjson=False),
            status=200,
            headers=HEADERS,
        ),
    )
    aresponses.add(
        "registry.hub.docker.com",
        "/v2/repositories/homeassistant/home-assistant/tags/page2",
        "get",
        aresponses.Response(
            text=fixture("container/page2", asjson=False),
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
        assert haversion.version == STABLE_VERSION


@pytest.mark.asyncio
async def test_beta_version_pagination(aresponses: ResponsesMockServer) -> None:
    """Test container beta during beta week."""
    aresponses.add(
        "registry.hub.docker.com",
        "/v2/repositories/homeassistant/home-assistant/tags",
        "get",
        aresponses.Response(
            text=fixture("container/beta_week_page1", asjson=False),
            status=200,
            headers=HEADERS,
        ),
    )
    aresponses.add(
        "registry.hub.docker.com",
        "/v2/repositories/homeassistant/home-assistant/tags/page2",
        "get",
        aresponses.Response(
            text=fixture("container/beta_week_page2", asjson=False),
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
async def test_stable_version_beta_week_pagination(aresponses: ResponsesMockServer) -> None:
    """Test container beta during beta week."""
    aresponses.add(
        "registry.hub.docker.com",
        "/v2/repositories/homeassistant/home-assistant/tags",
        "get",
        aresponses.Response(
            text=fixture("container/beta_week_page1", asjson=False),
            status=200,
            headers=HEADERS,
        ),
    )
    aresponses.add(
        "registry.hub.docker.com",
        "/v2/repositories/homeassistant/home-assistant/tags/page2",
        "get",
        aresponses.Response(
            text=fixture("container/beta_week_page2", asjson=False),
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
async def test_beta_version_beta_week_pagination(aresponses: ResponsesMockServer) -> None:
    """Test container beta during beta week."""
    aresponses.add(
        "registry.hub.docker.com",
        "/v2/repositories/homeassistant/home-assistant/tags",
        "get",
        aresponses.Response(
            text=fixture("container/beta_week_page1", asjson=False),
            status=200,
            headers=HEADERS,
        ),
    )
    aresponses.add(
        "registry.hub.docker.com",
        "/v2/repositories/homeassistant/home-assistant/tags/page2",
        "get",
        aresponses.Response(
            text=fixture("container/beta_week_page2", asjson=False),
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
async def test_keyerror(aresponses: ResponsesMockServer) -> None:
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


@pytest.mark.asyncio
async def test_stable_release_date(HaVersion: HaVersion) -> None:
    """Test container stable release date."""
    with patch(
        "pyhaversion.container.HaVersionContainer.fetch",
        return_value=fixture("container/default"),
    ):
        async with aiohttp.ClientSession() as session:
            haversion = HaVersion(session=session, source=HaVersionSource.CONTAINER)
            await haversion.get_version()
            assert haversion.version == STABLE_VERSION
            assert haversion.version_data[DATA_RELEASE_DATE] == STABLE_RELEASE_DATE


@pytest.mark.asyncio
async def test_beta_release_date(HaVersion: HaVersion) -> None:
    """Test container beta release date."""
    with patch(
        "pyhaversion.container.HaVersionContainer.fetch",
        return_value=fixture("container/beta_week"),
    ):
        async with aiohttp.ClientSession() as session:
            haversion = HaVersion(
                session=session,
                source=HaVersionSource.CONTAINER,
                channel=HaVersionChannel.BETA,
            )
            await haversion.get_version()
            assert haversion.version == BETA_VERSION
            assert haversion.version_data[DATA_RELEASE_DATE] == BETA_RELEASE_DATE


@pytest.mark.asyncio
async def test_dev_release_date(HaVersion: HaVersion) -> None:
    """Test container dev release date."""
    with patch(
        "pyhaversion.container.HaVersionContainer.fetch",
        return_value=fixture("container/default"),
    ):
        async with aiohttp.ClientSession() as session:
            haversion = HaVersion(
                session=session,
                source=HaVersionSource.CONTAINER,
                channel=HaVersionChannel.DEV,
            )
            await haversion.get_version()
            assert haversion.version == DEV_VERSION
            assert haversion.version_data[DATA_RELEASE_DATE] == DEV_RELEASE_DATE
