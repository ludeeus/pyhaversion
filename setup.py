"""Setup configuration."""
import setuptools

with open("README.md", "r") as fh:
    LONG = fh.read()
setuptools.setup(
    name="pyhaversion",
    version="3.2.0",
    author="Joakim Sorensen",
    author_email="hi@ludeeus.dev",
    description="",
    long_description=LONG,
    install_requires=["aiohttp", "async_timeout<=3.0.1", "pytest-runner"],
    long_description_content_type="text/markdown",
    url="https://github.com/ludeeus/pyhaversion",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
