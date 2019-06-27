"""Tests for Hassio."""

import json

import aiohttp
import pytest
from pyhaversion import HassioVersion
from .const import (
    HEADERS,
    STABLE_VERSION,
    STABLE_VERSION_BETA_WEEK,
    BETA_VERSION,
    BETA_VERSION_BETA_WEEK,
)
from .fixtures.fixture_hassio import (
    hassio_response,
    hassio_response_beta_week,
    hassio_beta_response,
    hassio_beta_response_beta_week,
)


@pytest.mark.asyncio
async def test_stable_version(aresponses, event_loop, hassio_response):
    """Test hassio stable."""
    aresponses.add(
        "s3.amazonaws.com",
        "/hassio-version/stable.json",
        "get",
        aresponses.Response(
            text=json.dumps(hassio_response), status=200, headers=HEADERS
        ),
    )

    async with aiohttp.ClientSession(loop=event_loop) as session:
        haversion = HassioVersion(event_loop, session)
        await haversion.get_version()
        assert haversion.version == STABLE_VERSION


@pytest.mark.asyncio
async def test_beta_version(aresponses, event_loop, hassio_beta_response):
    """Test hassio beta."""
    aresponses.add(
        "s3.amazonaws.com",
        "/hassio-version/beta.json",
        "get",
        aresponses.Response(
            text=json.dumps(hassio_beta_response), status=200, headers=HEADERS
        ),
    )

    async with aiohttp.ClientSession(loop=event_loop) as session:
        haversion = HassioVersion(event_loop, session, "beta")
        await haversion.get_version()
        assert haversion.version == BETA_VERSION


@pytest.mark.asyncio
async def test_stable_version_beta_week(
    aresponses, event_loop, hassio_response_beta_week
):
    """Test hassio stable during beta week."""
    aresponses.add(
        "s3.amazonaws.com",
        "/hassio-version/stable.json",
        "get",
        aresponses.Response(
            text=json.dumps(hassio_response_beta_week), status=200, headers=HEADERS
        ),
    )

    async with aiohttp.ClientSession(loop=event_loop) as session:
        haversion = HassioVersion(event_loop, session)
        await haversion.get_version()
        assert haversion.version == STABLE_VERSION_BETA_WEEK


@pytest.mark.asyncio
async def test_beta_version_beta_week(
    aresponses, event_loop, hassio_beta_response_beta_week
):
    """Test hassio beta during beta week."""
    aresponses.add(
        "s3.amazonaws.com",
        "/hassio-version/beta.json",
        "get",
        aresponses.Response(
            text=json.dumps(hassio_beta_response_beta_week), status=200, headers=HEADERS
        ),
    )

    async with aiohttp.ClientSession(loop=event_loop) as session:
        haversion = HassioVersion(event_loop, session, "beta")
        await haversion.get_version()
        assert haversion.version == BETA_VERSION_BETA_WEEK
