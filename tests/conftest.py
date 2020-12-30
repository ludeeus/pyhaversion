import pytest
import logging
from unittest.mock import patch

from pyhaversion import HaVersion as PyHaVersion

logging.basicConfig(level=logging.DEBUG)
pytestmark = pytest.mark.asyncio


async def mocked_fetch(self):
    pass


@pytest.fixture
def HaVersion():
    with patch(
        "pyhaversion.docker.HaVersionDocker.fetch", return_value=mocked_fetch
    ), patch("pyhaversion.haio.HaVersionHaio.fetch", return_value=mocked_fetch), patch(
        "pyhaversion.local.HaVersionLocal.fetch", return_value=mocked_fetch
    ), patch(
        "pyhaversion.pypi.HaVersionPypi.fetch", return_value=mocked_fetch
    ), patch(
        "pyhaversion.supervised.HaVersionSupervised.fetch", return_value=mocked_fetch
    ):
        yield PyHaVersion
