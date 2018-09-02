"""
A python module to the newest version number of Home Assistant.

This code is released under the terms of the MIT license. See the LICENSE
file for more details.
"""
import requests


def get_version_number(source, branch, image='default'):
    """Return the version number based on args."""
    if source == 'pip':
        if branch == 'beta':
            version = get_pip_beta()
        elif branch == 'stable':
            version = get_pip_stable()
    elif source == 'docker':
        if branch == 'beta':
            version = get_docker_beta()
        elif branch == 'stable':
            version = get_docker_stable()
    elif source == 'hassio':
        if branch == 'beta':
            version = get_hassio_beta(image)
        elif branch == 'stable':
            version = get_hassio_stable(image)
    return version


def get_pip_stable():
    """Pip stable."""
    base_url = 'https://pypi.org/pypi/homeassistant/json'
    version = requests.get(base_url, timeout=5).json()['info']['version']
    return {'homeassistant': version}


def get_pip_beta():
    """Pip beta."""
    base_url = 'https://pypi.org/pypi/homeassistant/json'
    get_version = requests.get(base_url, timeout=5).json()['releases']
    all_versions = []
    for versions in sorted(get_version, reverse=True):
        all_versions.append(versions)
    num = 0
    controll = 0
    while controll < 1:
        name = all_versions[num]
        if '.8.' in name or '.9.' in name:
            num = num + 1
        else:
            controll = 1
            version = name
    return {'homeassistant': version}


def get_docker_stable():
    """Docker stable."""
    base = 'https://registry.hub.docker.com/v1/repositories/'
    url = base + 'homeassistant/home-assistant/tags'
    get_version = requests.get(url, timeout=5).json()
    num = -1
    controll = 0
    while controll < 1:
        name = get_version[num]['name']
        if 'b' in name or 'd' in name or 'r' in name:
            num = num - 1
        else:
            controll = 1
            version = name
    return {'homeassistant': version}


def get_docker_beta():
    """Docker beta."""
    base = 'https://registry.hub.docker.com/v1/repositories/'
    url = base + 'homeassistant/home-assistant/tags'
    get_version = requests.get(url, timeout=5).json()
    num = -1
    controll = 0
    while controll < 1:
        name = get_version[num]['name']
        if 'd' in name or 'r' in name:
            num = num - 1
        else:
            controll = 1
            version = name
    return {'homeassistant': version}


def get_hassio_stable(image='default'):
    """Hassio stable."""
    base_url = 'https://s3.amazonaws.com/hassio-version/stable.json'
    data = requests.get(base_url, timeout=5).json()
    haversion = data['homeassistant'][image]
    suversion = data['supervisor']
    cliversion = data['hassos-cli']
    board = get_image(image)
    hassos = data['hassos'][board]
    return {'homeassistant': haversion, 'supervisor': suversion,
            'hassos-cli': cliversion, 'hassos': hassos}


def get_hassio_beta(image='default'):
    """Hassio beta."""
    base_url = 'https://s3.amazonaws.com/hassio-version/beta.json'
    data = requests.get(base_url, timeout=5).json()
    haversion = data['homeassistant'][image]
    suversion = data['supervisor']
    cliversion = data['hassos-cli']
    board = get_image(image)
    hassos = data['hassos'][board]
    return {'homeassistant': haversion, 'supervisor': suversion,
            'hassos-cli': cliversion, 'hassos': hassos}


def run_test():
    """Run tests."""
    sources = ['pip', 'docker', 'hassio']
    branches = ['stable', 'beta']
    images = get_boards()
    for source in sources:
        for branch in branches:
            if source == 'hassio':
                for image in images:
                    version = get_version_number(source, branch, image)
                    print(source + ' - ' +
                          image + ' - ' +
                          branch + ': ' +
                          str(version))
            else:
                version = get_version_number(source, branch)
                print(source + ' - ' + branch + ': ' + str(version))


def get_image(image):
    """Return image for hassio."""
    boards = get_boards()
    if image not in boards:
        ret_val = boards['default']
    else:
        ret_val = boards[image]
    return ret_val


def get_boards():
    """Return boards for hassio."""
    boards = {
        "default": "ova",
        "raspberrypi": "rpi",
        "raspberrypi2": "rpi2",
        "raspberrypi3": "rpi3",
        "raspberrypi3-64": "rpi3-64",
        "tinker": "tinker",
        "odroid-c2": "odroid-c2",
        "odroid-xu": "odroid-c2"
    }
    return boards
