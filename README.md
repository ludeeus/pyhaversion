# pyhaversion [![Build Status](https://travis-ci.com/ludeeus/pyhaversion.svg?branch=master)](https://travis-ci.com/ludeeus/pyhaversion)

_A python module to the newest version number of Home Assistant._

## Install

```bash
pip install pyhaversion
```

## Example usage

```python
from pyhaversion import HAVersion

source = 'pip'
branch = 'stable'
image = 'default'

ha_version = HAVersion()
result = ha_version.get_version_number(source, branch, image)

#Print results:
print('HA version: ' + result['homeassistant'])
```

## Valid options for source

- pip
- docker
- hassio

## Valid options for branch

- stable
- beta

## Optional valid options for image (hassio)

- default
- qemux86
- qemux86-64
- qemuarm
- qemuarm-64
- intel-nuc
- raspberrypi
- raspberrypi2
- raspberrypi3
- raspberrypi3-64
- tinker