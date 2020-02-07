"""setup winwifi library"""

import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

PKG = "winwifi"
VERSION = __import__(PKG).get_version()

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest

        errcode = pytest.main(self.test_args)
        sys.exit(errcode)


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
    tests_require=["pytest"],
    cmdclass={"test": PyTest},
    test_suite="tests",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.5",
    extras_require={"testing": ["pytest"]},
)
