"""setup winwifi library"""

from typing import List
from setuptools import setup, find_packages
PKG = 'winwifi'
VERSION = __import__(PKG).get_version()

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

setup(
    name=PKG,
    version=VERSION,
    author="Alex Puffer",
    description="WiFi for Windows",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/arpuffer/win-wifi",
    packages=find_packages(),
    provides=[PKG],
    test_suite='tests',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)
