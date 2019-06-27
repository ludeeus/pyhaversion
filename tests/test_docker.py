"""Tests for Docker."""

import json

import aiohttp
import pytest
from pyhaversion import DockerVersion
from .const import (
    HEADERS,
    STABLE_VERSION,
    STABLE_VERSION_BETA_WEEK,
    BETA_VERSION,
    BETA_VERSION_BETA_WEEK,
)
from .fixtures.fixture_docker import docker_response, docker_response_beta_week


@pytest.mark.asyncio
async def test_stable_version(aresponses, event_loop, docker_response):
    """Test docker stable."""
    aresponses.add(
        "registry.hub.docker.com",
        "/v2/repositories/homeassistant/home-assistant/tags",
        "get",
        aresponses.Response(
            text=json.dumps(docker_response), status=200, headers=HEADERS
        ),
    )

    async with aiohttp.ClientSession(loop=event_loop) as session:
        haversion = DockerVersion(event_loop, session)
        await haversion.get_version()
        assert haversion.version == STABLE_VERSION


@pytest.mark.asyncio
async def test_beta_version(aresponses, event_loop, docker_response):
    """Test docker beta."""
    aresponses.add(
        "registry.hub.docker.com",
        "/v2/repositories/homeassistant/home-assistant/tags",
        "get",
        aresponses.Response(
            text=json.dumps(docker_response), status=200, headers=HEADERS
        ),
    )

    async with aiohttp.ClientSession(loop=event_loop) as session:
        haversion = DockerVersion(event_loop, session, "beta")
        await haversion.get_version()
        assert haversion.version == BETA_VERSION


@pytest.mark.asyncio
async def test_stable_version_beta_week(
    aresponses, event_loop, docker_response_beta_week
):
    """Test docker stable during beta week."""
    aresponses.add(
        "registry.hub.docker.com",
        "/v2/repositories/homeassistant/home-assistant/tags",
        "get",
        aresponses.Response(
            text=json.dumps(docker_response_beta_week), status=200, headers=HEADERS
        ),
    )

    async with aiohttp.ClientSession(loop=event_loop) as session:
        haversion = DockerVersion(event_loop, session)
        await haversion.get_version()
        assert haversion.version == STABLE_VERSION_BETA_WEEK


@pytest.mark.asyncio
async def test_beta_version_beta_week(
    aresponses, event_loop, docker_response_beta_week
):
    """Test docker beta during beta week."""
    aresponses.add(
        "registry.hub.docker.com",
        "/v2/repositories/homeassistant/home-assistant/tags",
        "get",
        aresponses.Response(
            text=json.dumps(docker_response_beta_week), status=200, headers=HEADERS
        ),
    )

    async with aiohttp.ClientSession(loop=event_loop) as session:
        haversion = DockerVersion(event_loop, session, "beta")
        await haversion.get_version()
        assert haversion.version == BETA_VERSION_BETA_WEEK
