"""Tests for PyPi."""

import json

import aiohttp
import pytest
from pyhaversion import PyPiVersion
from .const import (
    HEADERS,
    STABLE_VERSION,
    STABLE_VERSION_BETA_WEEK,
    BETA_VERSION,
    BETA_VERSION_BETA_WEEK,
)
from .fixtures.fixture_pypi import pypi_response, pypi_response_beta_week


@pytest.mark.asyncio
async def test_stable_version(aresponses, event_loop, pypi_response):
    """Test pypi stable."""
    aresponses.add(
        "pypi.org",
        "/pypi/homeassistant/json",
        "get",
        aresponses.Response(
            text=json.dumps(pypi_response), status=200, headers=HEADERS
        ),
    )

    async with aiohttp.ClientSession(loop=event_loop) as session:
        haversion = PyPiVersion(event_loop, session)
        await haversion.get_version()
        assert haversion.version == STABLE_VERSION


@pytest.mark.asyncio
async def test_beta_version(aresponses, event_loop, pypi_response):
    """Test pypi beta."""
    aresponses.add(
        "pypi.org",
        "/pypi/homeassistant/json",
        "get",
        aresponses.Response(
            text=json.dumps(pypi_response), status=200, headers=HEADERS
        ),
    )

    async with aiohttp.ClientSession(loop=event_loop) as session:
        haversion = PyPiVersion(event_loop, session, "beta")
        await haversion.get_version()
        assert haversion.version == BETA_VERSION


@pytest.mark.asyncio
async def test_stable_version_beta_week(
    aresponses, event_loop, pypi_response_beta_week
):
    """Test pypi stable during beta week."""
    aresponses.add(
        "pypi.org",
        "/pypi/homeassistant/json",
        "get",
        aresponses.Response(
            text=json.dumps(pypi_response_beta_week), status=200, headers=HEADERS
        ),
    )

    async with aiohttp.ClientSession(loop=event_loop) as session:
        haversion = PyPiVersion(event_loop, session)
        await haversion.get_version()
        assert haversion.version == STABLE_VERSION_BETA_WEEK


@pytest.mark.asyncio
async def test_beta_version_beta_week(aresponses, event_loop, pypi_response_beta_week):
    """Test pypi beta during beta week."""
    aresponses.add(
        "pypi.org",
        "/pypi/homeassistant/json",
        "get",
        aresponses.Response(
            text=json.dumps(pypi_response_beta_week), status=200, headers=HEADERS
        ),
    )

    async with aiohttp.ClientSession(loop=event_loop) as session:
        haversion = PyPiVersion(event_loop, session, "beta")
        await haversion.get_version()
        assert haversion.version == BETA_VERSION_BETA_WEEK
