"""Tests for docker version."""
import asyncio
import aiohttp
import pytest
from pyhaversion import Version
from pyhaversion.consts import IMAGES


@pytest.mark.asyncio
async def test_docker():
    """Test docker."""

    async def run_docker_test(image, branch):
        """Run the test."""
        print()
        print("Testing", image, branch)
        async with aiohttp.ClientSession() as session:
            haversion = Version(
                asyncio.get_event_loop(), session=session, image=image, branch=branch
            )
            await haversion.get_docker_version()
            print("Version:", haversion.version)
            print("Version data:", haversion.version_data)
            print()

    for image in IMAGES:
        await run_docker_test(image, "stable")
        await run_docker_test(image, "beta")


@pytest.mark.asyncio
async def test_docker_not_validimage():
    """Test docker."""
    async with aiohttp.ClientSession() as session:
        haversion = Version(
            asyncio.get_event_loop(), image="not_valid", session=session
        )
        await haversion.get_docker_version()
        print(haversion.version)
        print(haversion.version_data)
