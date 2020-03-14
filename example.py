"""Example usage of pyhaversion."""
import asyncio
import aiohttp

# from pyhaversion import HassioVersion
from pyhaversion import PyPiVersion


async def test():
    """Example usage of pyhaversion."""
    async with aiohttp.ClientSession() as session:
        # data = HassioVersion(loop, branch="beta", session=session, image="raspberrypi4")
        # data = PyPiVersion(loop, branch="beta", session=session)
        data = PyPiVersion(loop, session=session)
        await data.get_version()

        print("Version:", data.version)
        print("Attributes:", data.version_data)


loop = asyncio.get_event_loop()
loop.run_until_complete(test())
