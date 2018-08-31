"""
A python module to the newest version number of Home Assistant.
This code is released under the terms of the MIT license. See the LICENSE
file for more details.
"""
import requests


class HAVersion:
    """This class is for this module"""

    def __init__(self):
        """Initialize"""

    def get_version_number(self, source, branch, image='default'):
        """This method gets the version number based on args"""
        if source == 'pip':
            if branch == 'beta':
                version = get_pip_beta()
            elif branch == 'stable':
                version = get_pip_stable()
            else:
                print('The defined branch is not valid: ' + branch)
        elif source == 'docker':
            if branch == 'beta':
                version = get_docker_beta()
            elif branch == 'stable':
                version = get_docker_stable()
            else:
                print('The defined branch is not valid: ' + branch)
        elif source == 'hassio':
            if branch == 'beta':
                version = get_hassio_beta(image)
            elif branch == 'stable':
                version = get_hassio_stable(image)
            else:
                print('The defined branch is not valid: ' + branch)
        else:
            print('The defined source is not valid: ' + source)
        return version


def get_pip_stable():
    """pip stable"""
    base_url = 'https://pypi.org/pypi/homeassistant/json'
    version = requests.get(base_url, timeout=5).json()['info']['version']
    return {'homeassistant': version}


def get_pip_beta():
    """pip beta"""
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
    """docker Stable"""
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
    """docker beta"""
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
    """hassio Stable"""
    base_url = 'https://s3.amazonaws.com/hassio-version/stable.json'
    data = requests.get(base_url, timeout=5).json()
    haversion = data['homeassistant'][image]
    suversion = data['supervisor']
    cliversion = data['hassos-cli']
    hassos = data['hassos']
    return {'homeassistant': haversion, 'supervisor': suversion,
            'hassos-cli': cliversion, 'hassos': hassos}


def get_hassio_beta(image='default'):
    """hassio beta"""
    base_url = 'https://s3.amazonaws.com/hassio-version/beta.json'
    data = requests.get(base_url, timeout=5).json()
    haversion = data['homeassistant'][image]
    suversion = data['supervisor']
    cliversion = data['hassos-cli']
    hassos = data['hassos']
    return {'homeassistant': haversion, 'supervisor': suversion,
            'hassos-cli': cliversion, 'hassos': hassos}
