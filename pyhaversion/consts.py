"""Constants for pyhaversion."""

BOARDS = {
    "default": "ova",
    "intel-nuc": "intel-nuc",
    "odroid-c2": "odroid-c2",
    "odroid-xu": "odroid-c2",
    "orangepi-prime": "opi-prime",
    "raspberrypi": "rpi",
    "raspberrypi2": "rpi2",
    "raspberrypi3-64": "rpi3-64",
    "raspberrypi3": "rpi3",
    "tinker": "tinker",
}

IMAGES = {
    "default": {"docker": "home-assistant", "hassio": "default"},
    "intel-nuc": {"docker": "intel-nuc-homeassistant", "hassio": "intel-nuc"},
    "odroid-c2": {"docker": "odroid-c2-homeassistant", "hassio": "odroid-c2"},
    "odroid-xu": {"docker": "odroid-xu-homeassistant", "hassio": "odroid-xu"},
    "orangepi-prime": {
        "docker": "orangepi-prime-homeassistant",
        "hassio": "orangepi-prime",
    },
    "qemuarm-64": {"docker": "qemuarm-64-homeassistant", "hassio": "qemuarm-64"},
    "qemuarm": {"docker": "qemuarm-homeassistant", "hassio": "qemuarm"},
    "qemux86-64": {"docker": "qemux86-64-homeassistant", "hassio": "qemux86-64"},
    "qemux86": {"docker": "qemux86-homeassistant", "hassio": "qemux86"},
    "raspberrypi": {"docker": "raspberrypi-homeassistant", "hassio": "raspberrypi"},
    "raspberrypi2": {"docker": "raspberrypi2-homeassistant", "hassio": "raspberrypi2"},
    "raspberrypi3-64": {
        "docker": "raspberrypi3-64-homeassistant",
        "hassio": "raspberrypi3-64",
    },
    "raspberrypi3": {"docker": "raspberrypi3-homeassistant", "hassio": "raspberrypi3"},
    "tinker": {"docker": "tinker-homeassistant", "hassio": "tinker"},
}

URL = {
    "docker": "https://registry.hub.docker.com/v2/repositories/homeassistant/{}/tags",
    "hassio": {
        "stable": "https://s3.amazonaws.com/hassio-version/stable.json",
        "beta": "https://s3.amazonaws.com/hassio-version/beta.json",
    },
    "pypi": "https://pypi.org/pypi/homeassistant/json",
}
