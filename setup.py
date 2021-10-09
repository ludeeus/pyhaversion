"""The setup script."""
from setuptools import find_packages, setup

with open("README.md") as readme_file:
    readme = readme_file.read()

setup(
    author_email="hi@ludeeus.dev",
    author="Joakim Sorensen",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    description="Get the latest Home Assistant version from various sources.",
    install_requires=[
        "aiohttp>=3.6.1,<4.0",
        "async_timeout<=3.0.1",
        "awesomeversion>=21.8.1",
    ],
    keywords=["homeassistant", "version", "update"],
    license="MIT license",
    long_description_content_type="text/markdown",
    long_description=readme,
    name="pyhaversion",
    packages=find_packages(include=["pyhaversion"]),
    python_requires=">=3.8.0",
    url="https://github.com/ludeeus/pyhaversion",
    version="main",
)
