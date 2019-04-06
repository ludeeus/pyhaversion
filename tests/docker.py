"""Tests for docker version."""
import asyncio
import aiohttp
import pytest
from pyhaversion import Version


@pytest.mark.asyncio
async def test_docker():
    """Test docker."""
    async with aiohttp.ClientSession() as session:
        haversion = Version(asyncio.get_event_loop(), session=session)
        await haversion.get_docker_version()
        print(haversion.version)
        print(haversion.version_data)


@pytest.mark.asyncio
async def test_docker_beta():
    """Test docker."""
    async with aiohttp.ClientSession() as session:
        haversion = Version(asyncio.get_event_loop(), branch='beta',
        session=session)
        await haversion.get_docker_version()
        print(haversion.version)
        print(haversion.version_data)


@pytest.mark.asyncio
async def test_docker_valid_image():
    """Test docker."""
    async with aiohttp.ClientSession() as session:
        haversion = Version(
            asyncio.get_event_loop(), image='raspberrypi3-homeassistant',
            session=session)
        await haversion.get_docker_version()
        print(haversion.version)
        print(haversion.version_data)


@pytest.mark.asyncio
async def test_docker_not_valid_image():
    """Test docker."""
    async with aiohttp.ClientSession() as session:
        haversion = Version(
            asyncio.get_event_loop(), image='not_valid', session=session)
        await haversion.get_docker_version()
        print(haversion.version)
        print(haversion.version_data)


@pytest.mark.asyncio
async def test_docker_valid_image_beta():
    """Test docker."""
    async with aiohttp.ClientSession() as session:
        haversion = Version(
            asyncio.get_event_loop(), branch='beta',
            image='raspberrypi3-homeassistant', session=session)
        await haversion.get_docker_version()
        print(haversion.version)
        print(haversion.version_data)


@pytest.mark.asyncio
async def test_docker_not_valid_image_beta():  # pylint: disable=invalid-name
    """Test docker."""
    async with aiohttp.ClientSession() as session:
        haversion = Version(
            asyncio.get_event_loop(), branch='beta', image='not_valid',
            session=session)
        await haversion.get_docker_version()
        print(haversion.version)
        print(haversion.version_data)
