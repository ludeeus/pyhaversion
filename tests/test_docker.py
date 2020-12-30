"""Tests for Docker."""

import json
from pyhaversion.exceptions import HaVersionInputException
from unittest.mock import patch
from tests.common import fixture
from pyhaversion.consts import HaVersionChannel, HaVersionSource

import aiohttp
import pytest

from pyhaversion import HaVersion

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
    """Test docker stable."""
    with patch(
        "pyhaversion.docker.HaVersionDocker.data",
        fixture("docker/default"),
    ):
        async with aiohttp.ClientSession() as session:
            haversion = HaVersion(session=session, source=HaVersionSource.DOCKER)
            await haversion.get_version()
            assert haversion.version == STABLE_VERSION


@pytest.mark.asyncio
async def test_beta_version(HaVersion):
    """Test docker beta."""
    with patch(
        "pyhaversion.docker.HaVersionDocker.data",
        fixture("docker/default"),
    ):
        async with aiohttp.ClientSession() as session:
            haversion = HaVersion(
                session=session,
                source=HaVersionSource.DOCKER,
                channel=HaVersionChannel.BETA,
            )
            await haversion.get_version()
            assert haversion.version == BETA_VERSION


@pytest.mark.asyncio
async def test_beta_version(HaVersion):
    """Test docker beta."""
    with patch(
        "pyhaversion.docker.HaVersionDocker.data",
        fixture("docker/default"),
    ):
        async with aiohttp.ClientSession() as session:
            haversion = HaVersion(
                session=session,
                source=HaVersionSource.DOCKER,
                channel=HaVersionChannel.DEV,
            )
            await haversion.get_version()
            assert haversion.version == DEV_VERSION


@pytest.mark.asyncio
async def test_stable_version_beta_week(HaVersion):
    """Test docker stable during beta week."""
    with patch(
        "pyhaversion.docker.HaVersionDocker.data",
        fixture("docker/beta_week"),
    ):
        async with aiohttp.ClientSession() as session:
            haversion = HaVersion(
                session=session,
                source=HaVersionSource.DOCKER,
            )
            await haversion.get_version()
            assert haversion.version == STABLE_VERSION_BETA_WEEK


@pytest.mark.asyncio
async def test_beta_version_beta_week(HaVersion):
    """Test docker beta during beta week."""
    with patch(
        "pyhaversion.docker.HaVersionDocker.data",
        fixture("docker/beta_week"),
    ):
        async with aiohttp.ClientSession() as session:
            haversion = HaVersion(
                session=session,
                source=HaVersionSource.DOCKER,
                channel=HaVersionChannel.BETA,
            )
        await haversion.get_version()
        assert haversion.version == BETA_VERSION_BETA_WEEK


@pytest.mark.asyncio
async def test_stable_version_pagination(aresponses):
    """Test docker beta during beta week."""
    aresponses.add(
        "registry.hub.docker.com",
        "/v2/repositories/homeassistant/home-assistant/tags",
        "get",
        aresponses.Response(
            text=fixture("docker/page1", False), status=200, headers=HEADERS
        ),
    )
    aresponses.add(
        "registry.hub.docker.com",
        "/v2/repositories/homeassistant/home-assistant/tags/page2",
        "get",
        aresponses.Response(
            text=fixture("docker/page2", False), status=200, headers=HEADERS
        ),
    )
    async with aiohttp.ClientSession() as session:
        haversion = HaVersion(
            session=session,
            source=HaVersionSource.DOCKER,
        )
        await haversion.get_version()
        assert haversion.version == STABLE_VERSION


@pytest.mark.asyncio
async def test_beta_version_pagination(aresponses):
    """Test docker beta during beta week."""
    aresponses.add(
        "registry.hub.docker.com",
        "/v2/repositories/homeassistant/home-assistant/tags",
        "get",
        aresponses.Response(
            text=fixture("docker/page1", False), status=200, headers=HEADERS
        ),
    )
    aresponses.add(
        "registry.hub.docker.com",
        "/v2/repositories/homeassistant/home-assistant/tags/page2",
        "get",
        aresponses.Response(
            text=fixture("docker/page2", False), status=200, headers=HEADERS
        ),
    )
    async with aiohttp.ClientSession() as session:
        haversion = HaVersion(
            session=session,
            source=HaVersionSource.DOCKER,
            channel=HaVersionChannel.BETA,
        )
        await haversion.get_version()
        assert haversion.version == BETA_VERSION


@pytest.mark.asyncio
async def test_stable_version_beta_week_pagination(aresponses):
    """Test docker beta during beta week."""
    aresponses.add(
        "registry.hub.docker.com",
        "/v2/repositories/homeassistant/home-assistant/tags",
        "get",
        aresponses.Response(
            text=fixture("docker/beta_week_page1", False),
            status=200,
            headers=HEADERS,
        ),
    )
    aresponses.add(
        "registry.hub.docker.com",
        "/v2/repositories/homeassistant/home-assistant/tags/page2",
        "get",
        aresponses.Response(
            text=fixture("docker/beta_week_page2", False),
            status=200,
            headers=HEADERS,
        ),
    )

    async with aiohttp.ClientSession() as session:
        haversion = HaVersion(
            session=session,
            source=HaVersionSource.DOCKER,
        )
        await haversion.get_version()
        assert haversion.version == STABLE_VERSION_BETA_WEEK


@pytest.mark.asyncio
async def test_beta_version_beta_week_pagination(aresponses):
    """Test docker beta during beta week."""
    aresponses.add(
        "registry.hub.docker.com",
        "/v2/repositories/homeassistant/home-assistant/tags",
        "get",
        aresponses.Response(
            text=fixture("docker/beta_week_page1", False),
            status=200,
            headers=HEADERS,
        ),
    )
    aresponses.add(
        "registry.hub.docker.com",
        "/v2/repositories/homeassistant/home-assistant/tags/page2",
        "get",
        aresponses.Response(
            text=fixture("docker/beta_week_page2", False),
            status=200,
            headers=HEADERS,
        ),
    )

    async with aiohttp.ClientSession() as session:
        haversion = HaVersion(
            session=session,
            source=HaVersionSource.DOCKER,
            channel=HaVersionChannel.BETA,
        )
        await haversion.get_version()
        assert haversion.version == BETA_VERSION_BETA_WEEK


@pytest.mark.asyncio
async def test_input_exception(HaVersion):
    with pytest.raises(HaVersionInputException):
        HaVersion(source=HaVersionSource.DOCKER)