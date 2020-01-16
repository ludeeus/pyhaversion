"""Example usage of pyhaversion."""
import asyncio
import aiohttp

from pyhaversion import HassioVersion


async def test():
    """Example usage of pyhaversion."""
    async with aiohttp.ClientSession() as session:
        data = HassioVersion(loop, branch="beta", session=session, image="raspberrypi4")
        await data.get_version()

        print("Version:", data.version)
        print("Attributes:", data.version_data)


loop = asyncio.get_event_loop()
loop.run_until_complete(test())
